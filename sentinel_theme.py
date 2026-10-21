"""Shared Sentinel visual tokens and Plotly styling for the Streamlit dashboard."""
import streamlit as st

DARK = dict(page='#090d14', panel='#101720', text='#e7edf6', secondary='#9aa9bd',
            muted='#8390a4', border='#222c3a', input='#141d29', grid='#253040', accent='#64e9b1')
LIGHT = dict(page='#f4f7fb', panel='#ffffff', text='#172536', secondary='#526377',
             muted='#617286', border='#d8e1ec', input='#ffffff', grid='#e6edf4', accent='#087952')
COLORS = ['#64e9b1', '#6d9fff', '#eebe6a', '#b9a0ff', '#ff7285', '#57c9d9']


def palette():
    return LIGHT if st.session_state.get('dashboard_theme', 'Dark') == 'Light' else DARK


def style_chart(figure, height=250, legend=False):
    """Apply one palette to every dashboard chart, including hover labels and axes."""
    p = palette()
    colors = COLORS if p is DARK else ['#087952', '#366cd4', '#a56d12', '#8058c7', '#c53a55', '#168194']
    figure.update_layout(
        template='plotly_dark' if p is DARK else 'plotly_white',
        paper_bgcolor=p['panel'], plot_bgcolor=p['panel'],
        colorway=colors, height=height,
        margin=dict(l=12, r=12, t=18, b=12),
        font=dict(family='Inter, Segoe UI, Arial', size=11, color=p['secondary']),
        hoverlabel=dict(bgcolor=p['input'], bordercolor=p['border'], font_color=p['text']),
        showlegend=legend,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='left', x=0,
                    font=dict(color=p['secondary']))
    )
    figure.update_xaxes(showgrid=False, zeroline=False, linecolor=p['grid'], tickfont_color=p['muted'])
    figure.update_yaxes(showgrid=True, gridcolor=p['grid'], zeroline=False, tickfont_color=p['muted'])
    for trace in figure.data:
        if trace.type == 'pie':
            trace.update(marker=dict(colors=colors, line=dict(color=p['panel'], width=3)))
    return figure
