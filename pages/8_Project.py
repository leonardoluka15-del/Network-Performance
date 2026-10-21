"""A reviewable case study for hiring managers, clients and engineers."""
import streamlit as st
from navigation import navigation

st.set_page_config(page_title='Project case study | Leonard Oluka', page_icon='◈', layout='wide', initial_sidebar_state='expanded')
navigation('Project')
st.markdown('<div class="overview-wrapper"><div class="overview-title">From network signals to engineering decisions</div><div class="overview-subtitle">A Python engineering portfolio project by Leonard Oluka</div></div>', unsafe_allow_html=True)
with st.container(border=True, key='project_panel_story'):
    st.markdown('### The problem')
    st.write('Daily radio-network KPI files are difficult to compare consistently across sites, vendors and technologies. A useful operations dashboard must show coverage gaps alongside performance changes and give engineers evidence they can investigate.')
    st.markdown('### The solution')
    st.write('This application combines validated KPI imports, SQLite persistence, multi-technology views and exportable reports. The command centre adds matched-measurement comparisons, an explainable investigation queue and source-level drill-down, presented in a Sentinel-inspired interface.')
    st.caption('Portfolio demonstration: sample and uploaded data. No company-network access, production deployment outcomes or measured business savings are claimed.')
left, right = st.columns([1.4,1])
with left:
    with st.container(border=True, key='project_panel_tour'):
        st.markdown('### Review it in five minutes')
        st.markdown('''1. **Command centre:** review the reporting date, latest-day KPIs and operational briefing.
2. **What changed:** compare common site/counter pairs across the latest two reporting dates.
3. **Investigation queue:** select a flagged site, inspect source telemetry and export the queue.
4. **Data trust:** inspect missing measurements, invalid percentages and repeated source keys.
5. **Reports & exports:** review the existing filtered CSV, Excel and PDF workflows.''')
        if st.button('Explore the command centre', key='project_start', type='primary'):
            st.switch_page('pages/1_Overview.py')
with right:
    with st.container(border=True, key='project_panel_stack'):
        st.markdown('### Engineering demonstrated')
        st.markdown('''- **Python / Pandas:** schema-aware aggregation and matched-cohort comparisons.
- **SQLite:** persistent KPI storage and upload history.
- **Streamlit / Plotly:** multipage interactive analysis and shared visual tokens.
- **ReportLab / OpenPyXL:** export workflows.
- **Testing:** isolated application-page checks and analytical edge cases.''')
with st.container(border=True, key='project_panel_tradeoffs'):
    st.markdown('### Decisions and tradeoffs')
    st.markdown('''**Explainable rules before AI claims.** Thresholds and suggested investigations are visible. No trained model, causal diagnosis or outage prediction is claimed.

**Comparable evidence before headline deltas.** Site coverage and available counters can change between dates. The comparison table keeps common site/counter pairs and labels a reporting-date gap explicitly.

**Existing workflows before a platform rewrite.** The Sentinel visual language sits on the existing Streamlit app, preserving KPI imports and reports.

**Honest scope.** Some technology and alarm views generate their own demo data. These are not asserted to be the same dataset as database-backed overview calculations. Live telemetry, multi-user permissions and production service guarantees are future work.''')
st.markdown('[Source code](https://github.com/leonardoluka15-del/Network-Performance) · [LinkedIn / contact Leonard](https://www.linkedin.com/in/oluka-leonard-onyedikachi-5a9554194/)')
