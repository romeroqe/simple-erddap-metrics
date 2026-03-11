import altair as alt
import pandas as pd


def most_viewed_chart(views):

    view_counts = views["dataset"].value_counts().head(10).reset_index()
    view_counts.columns = ["dataset", "count"]

    chart = alt.Chart(view_counts).mark_arc().encode(
        theta="count:Q",
        color="dataset:N"
    )

    return chart


def most_downloaded_chart(downloads):

    dataset_counts = downloads["dataset"].value_counts().head(10).reset_index()
    dataset_counts.columns = ["dataset", "count"]

    chart = alt.Chart(dataset_counts).mark_arc().encode(
        theta="count:Q",
        color="dataset:N"
    )

    return chart


def downloads_format_chart(downloads):

    format_counts = downloads["format"].value_counts().reset_index()
    format_counts.columns = ["format", "count"]

    chart = alt.Chart(format_counts).mark_arc().encode(
        theta="count:Q",
        color="format:N"
    )

    return chart


def views_over_time(views, scale):

    views_time = views.set_index("date")

    if scale == "Daily":
        freq = "D"
        data_views = views_time.resample("D").size()
        data_views.index = data_views.index.strftime("%Y-%m-%d")

    elif scale == "Monthly":
        freq = "MS"
        data_views = views_time.resample("MS").size()
        data_views.index = data_views.index.strftime("%Y-%m")

    elif scale == "Yearly":
        freq = "YS"
        data_views = views_time.resample("YS").size()
        data_views.index = data_views.index.strftime("%Y")

    data_views = data_views.rename("views").to_frame()

    return data_views, freq


def downloads_over_time(downloads, scale):

    downloads_time = downloads.set_index("date")

    if scale == "Daily":
        data = downloads_time.resample("D").size()
        data.index = data.index.strftime("%Y-%m-%d")

    elif scale == "Monthly":
        data = downloads_time.resample("MS").size()
        data.index = data.index.strftime("%Y-%m")

    elif scale == "Yearly":
        data = downloads_time.resample("YS").size()
        data.index = data.index.strftime("%Y")

    data = data.rename("downloads").to_frame()

    return data

def downloads_by_dataset_over_time(downloads, scale, top_n=10):

    top_datasets = downloads["dataset"].value_counts().head(top_n).index
    downloads = downloads[downloads["dataset"].isin(top_datasets)]

    if scale == "Daily":
        freq = "D"
        fmt = "%Y-%m-%d"

    elif scale == "Monthly":
        freq = "MS"
        fmt = "%Y-%m"

    elif scale == "Yearly":
        freq = "YS"
        fmt = "%Y"

    data = (
        downloads
        .groupby([pd.Grouper(key="date", freq=freq), "dataset"])
        .size()
        .unstack("dataset")
        .fillna(0)
    )

    data.index = data.index.strftime(fmt)

    return data