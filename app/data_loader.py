import streamlit as st
from simple_erddap_metrics import parse_logs

@st.cache_data(show_spinner="Parsing ERDDAP logs...")
def load_logs(folder, geolocate, config_path):
    return parse_logs(folder, geolocate=geolocate, config_path=config_path)