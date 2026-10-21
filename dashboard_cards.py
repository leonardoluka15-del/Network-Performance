"""Responsive, consistently typeset summary cards with real source-data sparklines."""
from html import escape
import base64
import math
import re
import pandas as pd
import streamlit as st
from performance_insights import summarize

ICONS = {
 'availability':'<path d="M3 12h4l3-8 4 16 3-8h4"/>',
 'data_mb':'<rect x="4" y="3" width="16" height="7" rx="2"/><rect x="4" y="14" width="16" height="7" rx="2"/><path d="M8 6.5h.01M8 17.5h.01M12 7h4M12 18h4"/>',
 'voice_erlang':'<path d="M6 3h4l1 5-3 2a15 15 0 0 0 6 6l2-3 5 1v4a3 3 0 0 1-3 3A18 18 0 0 1 3 6a3 3 0 0 1 3-3Z"/>',
 'accessibility':'<path d="M12 3 4 7v5c0 5 8 9 8 9s8-4 8-9V7l-8-4Z"/><path d="m8 12 3 3 5-6"/>',
 'drop_rate':'<path d="m3 6 6 6 4-4 8 10M15 18h6v-6"/>',
 'mobility':'<path d="M3 7h17m-5-4 5 4-5 4M21 17H4m5-4-5 4 5 4"/>',
}


def _svg_image(svg, css_class, alt):
    # Streamlit sanitizes inline SVG in st.html. An SVG image preserves its
    # shape without JavaScript or external requests.
    encoded = base64.b64encode(svg.encode()).decode()
    return f'<img class="{css_class}" src="data:image/svg+xml;base64,{encoded}" alt="{escape(alt)}"/>'


def _sparkline(values, color):
    values = [float(v) for v in values if v is not None and math.isfinite(float(v))]
    if len(values) < 2:
        return '<span class="metric-no-trend">Not enough trend data</span>'
    low, high = min(values), max(values)
    span = high-low or 1
    points = [(i*156/(len(values)-1), 34-(v-low)/span*26) for i,v in enumerate(values)]
    line = ' '.join(f'{x:.1f},{y:.1f}' for x,y in points)
    area = '0,42 '+line+' 156,42'
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 156 44"><polygon points="{area}" fill="{color}" opacity=".08"/><polyline points="{line}" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    return _svg_image(svg, 'metric-spark', 'Source window trend')


def render_metric_cards(frame, summary):
    history = {key:[] for key in ICONS}
    if not frame.empty and 'time' in frame:
        dates = pd.to_datetime(frame['time'], errors='coerce')
        for _,group in frame.groupby(dates.dt.normalize(), sort=True):
            day = summarize(group)
            for key in history: history[key].append(day.get(key))
    definitions = [
        ('availability','Network availability', summary.get('network_availability'), '%', 'Cross-technology average', '#70e1c4'),
        ('data_mb','Data traffic', summary.get('total_data_mb'), 'volume', '2G, 3G, 4G & 5G', '#86adff'),
        ('voice_erlang','Voice traffic', summary.get('total_voice_erlang'), 'voice', '2G, 3G & VoLTE', '#bda2ff'),
        ('accessibility','Accessibility', summary.get('accessibility'), '%', 'Call & radio setup success', '#70e1c4'),
        ('drop_rate','Drop call rate', summary.get('drop_rate'), '%', 'Lower values are better', '#f2bc79'),
        ('mobility','Handover success', summary.get('hosr'), '%', 'Cross-technology mobility', '#86adff'),
    ]
    cards = []
    for key,label,value,unit,note,color in definitions:
        if value is None or pd.isna(value): number,suffix='—',''
        elif unit == '%': number,suffix=f'{value:.2f}','%'
        elif unit == 'volume':
            gb = value/1024; value, suffix=(gb/1024,'TB') if gb>=1024 else (gb,'GB')
            number=f'{value:,.0f}' if value>=100 else f'{value:,.2f}'
        else:
            value,suffix=(value/1_000_000,'M Erl') if value>=1_000_000 else (value/1000,'K Erl') if value>=1000 else (value,'Erl')
            number=f'{value:,.2f}'
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{ICONS[key]}</svg>'
        icon=_svg_image(svg, 'metric-icon-image', '')
        cards.append(f'<article class="metric-tile" style="--tile-accent:{color}"><div class="metric-tile-top"><span class="metric-tile-label">{label}</span><span class="metric-tile-icon">{icon}</span></div><div class="metric-tile-number">{escape(number)}<span>{escape(suffix)}</span></div><div class="metric-tile-bottom"><span>{note}</span>{_sparkline(history[key],color)}</div></article>')
    st.html('<div class="metric-grid">'+''.join(cards)+'</div>')
    st.caption('Latest reporting day · Sparklines show the selected source-data window')
