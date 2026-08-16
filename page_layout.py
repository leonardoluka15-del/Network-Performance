import streamlit as st      # Streamlit Library for the web page
def settings():
    st.markdown("""
        <style>
        [data-testid="stHeader"] {
            height: 40px;
            min-height: 40px;
            background-color: #000000;
        }
        [data-testid="stHeader"]::before {
            content: "Network Performance Dashboard";
            color: white;
            font-family: 'Arial', sans-serif;
            font-size: 18px;
            font-weight: 600;
            position: absolute;
            left: 20px;
            top: 8px;
        }
        [data-testid="stToolbar"] {
            background-color: transparent;
        }
        </style>
        """, unsafe_allow_html=True)