"""Decision-oriented presentation built on pure, independently tested calculations."""
from html import escape
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from performance_insights import compare_days, quality, exceptions, numeric, AVAILABILITY
from sentinel_theme import style_chart


def render_briefing(frame):
    comparison, trust, queue = compare_days(frame), quality(frame), exceptions(frame)
    with st.container(border=True, key='overview_panel_briefing'):
        st.markdown('<div class="panel-title">Operational briefing</div><div class="panel-subtitle">Evidence from the selected reporting window · indicative engineering thresholds</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.metric('Sites with threshold breaches', queue['Site'].nunique() if not queue.empty else 0,
                  help='Unique sites crossing an availability, accessibility or drop-rate policy on the latest reporting date.')
        c2.metric('High-priority findings', int(queue['Priority'].eq('P1').sum()) if not queue.empty else 0,
                  help='P1: availability below 95% or drop rate above 5%. Findings are not confirmed incidents.')
        c3.metric('Latest reporting date', trust['latest_day'] or 'Unavailable',
                  help='Date in the data, not the last time this page was rendered.')
        age = trust['age_days']
        if age is not None and age > 1:
            st.caption(f'Data is {age} calendar days old relative to today (UTC). This portfolio dataset is not a live network feed.')
        elif age is not None and age < 0:
            st.warning('The latest reporting date is in the future. Check source timestamps before interpreting freshness.')
        changes, investigations, data_trust = st.tabs(['What changed', 'Investigation queue', 'Data trust'])
        with changes:
            if not comparison['available']:
                st.info(comparison['reason'])
            else:
                st.caption(f"{comparison['latest_day']} vs {comparison['previous_day']} · {comparison['matched_sites']} matched sites · {comparison['gap_days']}-day gap. This is the previous available reporting date, not necessarily yesterday.")
                rows = []
                labels = {'availability':'Availability', 'accessibility':'Accessibility', 'drop_rate':'Drop rate',
                          'mobility':'Mobility / HOSR', 'data_mb':'Data traffic', 'voice_erlang':'Voice traffic'}
                for metric, result in comparison['metrics'].items():
                    unit = 'MB' if metric == 'data_mb' else 'Erlang' if metric == 'voice_erlang' else '%'
                    delta = result['delta']
                    percent = metric in ('data_mb', 'voice_erlang')
                    meaning = 'No comparable measurements'
                    if delta is not None:
                        if percent: meaning = 'Higher volume' if delta > 0 else 'Lower volume' if delta < 0 else 'Unchanged volume'
                        else: meaning = 'Improved' if (delta < 0 if metric == 'drop_rate' else delta > 0) else 'Unchanged' if delta == 0 else 'Degraded'
                    elif result['current'] is not None: meaning = 'Percentage change undefined: zero baseline'
                    rows.append({'Metric':labels[metric], 'Previous':_value(result['previous'], unit),
                                 'Latest':_value(result['current'], unit),
                                 'Change':f'{delta:+.2f} '+('%' if percent else 'pp') if delta is not None else '—',
                                 'Interpretation':meaning, 'Matched measurements':result['pairs']})
                st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
                st.caption(f"Coverage changes: {comparison['added_sites']} added sites; {comparison['removed_sites']} removed sites. Comparisons exclude unmatched sites and missing measurements. Percentage metrics give equal weight to technologies. Traffic uses matched site/counter totals; duplicate rows are averaged per site before comparison. pp = percentage points.")
        with investigations:
            st.caption('Rules: availability <99%, accessibility <98%, drop rate >2%. P1 escalation uses <95% availability or >5% drops. These are illustrative thresholds, not contractual SLAs or proven root causes.')
            if queue.empty:
                st.info('No threshold breaches were detected in the available latest-day measurements. Missing measurements do not count as passing.')
            else:
                st.dataframe(queue, hide_index=True, use_container_width=True)
                st.download_button('Download investigation queue', queue.to_csv(index=False).encode('utf-8'),
                                   'network-investigations.csv', 'text/csv', key='export_investigations')
                sites = sorted(queue['Site'].unique())
                chosen = st.selectbox('Inspect source telemetry for a flagged site', sites, key='briefing_site')
                selected = frame[frame['ihs_id'].astype(str) == chosen].copy()
                _site_evidence(selected, chosen)
        with data_trust:
            a,b,c,d = st.columns(4)
            a.metric('Valid KPI cells', f"{trust['percent_completeness']:.1f}%" if trust['percent_completeness'] is not None else '—')
            b.metric('Out-of-range percentages', trust['invalid_percentages'])
            c.metric('Repeated site/timestamps', trust['duplicates'])
            d.metric('Missing site IDs', trust['missing_site_ids'])
            st.caption('Valid KPI cells measures numeric values from 0–100 across percentage columns containing at least one source value in this window. Missing/nonnumeric cells reduce coverage; wholly absent optional technology columns are excluded. Repeated site/timestamps are a review signal, not automatic deletions. Out-of-range values are excluded from the new comparisons and investigations; existing legacy charts retain their original calculations.')
            with st.expander('Calculation methods and limitations'):
                st.markdown('''- Overview cards show the latest reporting day; trend charts use the selected window.
- The new comparison table restricts both dates to common site/counter pairs.
- Zero traffic is retained; missing traffic is never converted to zero.
- Traffic changes describe volume, not improved or degraded service quality.
- Investigations use latest-day site averages, then equal weight across available technologies.
- Suggested checks are rule-based guidance; the dashboard does not diagnose confirmed faults or execute remediation.
- Data remains sample/uploaded KPI data. Demo technology and alarm pages can use their own generated datasets.''')


def _value(value, unit):
    return '—' if value is None else f'{value:,.2f} {unit}'


def _site_evidence(frame, site):
    st.markdown(f'**Source evidence / {escape(site)}**')
    available = [column for column in AVAILABILITY if column in frame and frame[column].notna().any()]
    if available:
        values = numeric(frame, available, percentage=True)
        values['date'] = pd.to_datetime(frame['time'], errors='coerce', utc=True)
        daily = values.groupby('date').mean().sort_index()
        chart = go.Figure()
        for column in available:
            chart.add_trace(go.Scatter(x=daily.index, y=daily[column], name=column.replace('availability_', '').upper(), mode='lines+markers'))
        chart.update_yaxes(title_text='Availability (%)')
        st.plotly_chart(style_chart(chart, height=250, legend=True), use_container_width=True)
    columns = [c for c in ['time','ihs_id','vendor',*AVAILABILITY,'cssr_2g','rrc_success_4g','drop_call_rate_2g','dcr_volte'] if c in frame]
    st.dataframe(frame[columns].sort_values('time', ascending=False).head(30), hide_index=True, use_container_width=True)
