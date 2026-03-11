import argparse
import streamlit as st
import pandas as pd

from simple_erddap_metrics.cards import metric_card, inject_card_css
from simple_erddap_metrics.data_loader import load_logs
from simple_erddap_metrics.charts import *
from simple_erddap_metrics.map_view import render_download_map

parser = argparse.ArgumentParser()
parser.add_argument("--logs")
parser.add_argument("--config")
parser.add_argument("--enable-geo", action="store_true")

args, _ = parser.parse_known_args()

st.set_page_config(
    page_title="Simple ERDDAP Metrics",
    page_icon="📊",
    layout="wide"
)

st.title("Simple ERDDAP metrics")

inject_card_css()

# Inputs

col0, col1, col2, col3 = st.columns([3,1,1,1])

with col0:
    log_dir = st.text_input(
        "Log directory", 
        value=args.logs,
        help="Directory containing ERDDAP log files (i.e., files starting with 'log')."
    )

# Advanced configuration

with st.expander("⚙ Advanced configuration", expanded=False):

    config_path = st.text_input(
        "Configuration file (YAML)",
        value=args.config,
        help="Optional YAML file. If left empty, the default configuration will be used."
    )

    config_path = config_path.strip() if isinstance(config_path, str) else None

    geolocate = st.toggle(
        "Enable IP geolocation",
        value=args.enable_geo,
        help="Enable IP geolocation lookup (may significantly slow parsing of large logs)."
    )

st.caption("Filters affect all charts and tables below.")

# Run parser

if log_dir:

    df, _, _ = load_logs(log_dir, geolocate, config_path)

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    date_min = df["date"].min().date()
    date_max = df["date"].max().date()

    # Filters

    with col1:
        scale = st.selectbox(
            "Time scale",
            ["Daily","Monthly","Yearly"],
            index=2,
            help="Aggregation level used to display activity over time."
                " Daily shows individual days, Monthly groups by month,"
                " and Yearly groups by year."
        )

    with col2:
        date_min_filter = st.date_input(
            "Start date",
            value=date_min,
            min_value=date_min,
            max_value=date_max,
            help="Start date of the analysis period. Only log entries after this date will be included."
        )

    with col3:
        date_max_filter = st.date_input(
            "End date",
            value=date_max,
            min_value=date_min,
            max_value=date_max,
            help="End date of the analysis period. Only log entries before this date will be included."
        )

    mask = (
        (df["date"] >= pd.to_datetime(date_min_filter)) &
        (df["date"] <= pd.to_datetime(date_max_filter))
    )

    df_filtered = df[mask]
    downloads = df_filtered[df_filtered["type"] == "download"]
    views = df_filtered[df_filtered["type"] == "view"]

    period = f"{date_min_filter} - {date_max_filter}"

    # Metrics

    c1,c2,c3 = st.columns(3)

    with c1:
        metric_card("Period",period)

    with c2:
        metric_card("Total views",(df_filtered["type"]=="view").sum())

    with c3:
        metric_card("Total downloads",(df_filtered["type"]=="download").sum())

    st.subheader("Parsed data")

    df_table = (
        df_filtered
        .drop(columns=["ip","lat","lon"],errors="ignore")
        .set_index("date")
        .sort_index(ascending=False)
    )

    st.dataframe(df_table,use_container_width=True)

    # Charts

    col1,col2,col3 = st.columns(3)

    with col1:
        st.subheader("Most viewed datasets")
        st.altair_chart(most_viewed_chart(views),use_container_width=True)

    with col2:
        st.subheader("Most downloaded datasets")
        st.altair_chart(most_downloaded_chart(downloads),use_container_width=True)

    with col3:
        st.subheader("Downloads by format")
        st.altair_chart(downloads_format_chart(downloads),use_container_width=True)

    st.subheader("Views over time")

    data_views,freq = views_over_time(views,scale)
    st.line_chart(data_views)

    st.subheader("Downloads over time")

    data_downloads = downloads_over_time(downloads,scale)
    st.line_chart(data_downloads)

    st.subheader("Top 10 datasets downloads over time")

    data_dataset = downloads_by_dataset_over_time(downloads, scale)
    st.line_chart(data_dataset)

    # Map

    if {"lat","lon"}.issubset(downloads.columns):
        downloads_geo = downloads.dropna(subset=["lat","lon"])
    else:
        downloads_geo = pd.DataFrame()

    if downloads_geo.empty:

        st.info("No geolocation information available for the selected filters.")

    else:

        col_chart,col_table = st.columns([4,1])

        top_countries = (
            downloads_geo
            .groupby("country")
            .size()
            .sort_values(ascending=False)
            .head(10)
            .index
        )

        with col_chart:

            st.subheader("Top 10 countries by downloads")

            country_data = (
                downloads_geo[downloads_geo["country"].isin(top_countries)]
                .set_index("date")
                .groupby([pd.Grouper(freq=freq), "country"])
                .size()
                .unstack(level="country")
                .fillna(0)
            )

            if scale=="Daily":
                country_data.index = country_data.index.strftime("%Y-%m-%d")
            elif scale=="Monthly":
                country_data.index = country_data.index.strftime("%Y-%m")
            elif scale=="Yearly":
                country_data.index = country_data.index.strftime("%Y")

            st.line_chart(country_data)

        with col_table:

            country_summary = (
                downloads_geo
                .groupby("country")
                .size()
                .sort_values(ascending=False)
                .head(10)
                .to_frame("downloads")
            )

            st.dataframe(country_summary, use_container_width=True)

        city_data = (
            downloads_geo
            .dropna(subset=["lat","lon"])
            .groupby(["city","country"],as_index=False)
            .agg(
                lat=("lat","mean"),
                lon=("lon","mean"),
                downloads=("dataset","count")
            )
            .sort_values("downloads",ascending=False)
        )

        city_data["lat"]=pd.to_numeric(city_data["lat"],errors="coerce")
        city_data["lon"]=pd.to_numeric(city_data["lon"],errors="coerce")
        city_data=city_data.dropna(subset=["lat","lon"])

        if city_data.empty:
            st.warning("No city coordinates available for the selected filters.")
        else:
            render_download_map(city_data)

        st.write("Total downloads with coordinates:",len(downloads_geo.dropna(subset=["lat","lon"])))