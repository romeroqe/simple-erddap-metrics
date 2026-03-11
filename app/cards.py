import streamlit as st

def inject_card_css():

    st.markdown("""
    <style>

    .metric-card {
        background-color: var(--secondary-background-color);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid color-mix(in srgb, currentColor 20%, transparent);
    }

    .metric-title {
        font-size: 0.9rem;
        opacity: 0.7;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
    }

    </style>
    """, unsafe_allow_html=True)


def metric_card(title, value):

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)