import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium


def render_download_map(city_data):

    center_lat = city_data["lat"].mean()
    center_lon = city_data["lon"].mean()

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=2,
        tiles="CartoDB positron"
    )

    cluster = MarkerCluster(
        name="Downloads by city",
        showCoverageOnHover=False,
        spiderfyOnMaxZoom=True,
        disableClusteringAtZoom=8,
        icon_create_function="""
        function(cluster) {

            var markers = cluster.getAllChildMarkers();
            var total = 0;

            for (var i = 0; i < markers.length; i++) {

                var tt = markers[i].getTooltip();

                if (tt && tt.getContent) {

                    var content = tt.getContent();
                    var match = content.match(/\\((\\d+)\\)/);

                    if (match) {
                        total += parseInt(match[1]);
                    }
                }
            }

            return L.divIcon({
                html: '<div><span>' + total + '</span></div>',
                className: 'marker-cluster marker-cluster-medium',
                iconSize: new L.Point(40, 40)
            });
        }
        """
    ).add_to(m)

    dmin = city_data["downloads"].min()
    dmax = city_data["downloads"].max()

    def scale_radius(x, xmin, xmax, rmin=5, rmax=18):
        if xmax == xmin:
            return (rmin + rmax) / 2
        return rmin + (x - xmin) * (rmax - rmin) / (xmax - xmin)

    for _, row in city_data.iterrows():

        radius = scale_radius(row["downloads"], dmin, dmax)

        popup_html = f"""
        <b>City:</b> {row['city']}<br>
        <b>Country:</b> {row['country']}<br>
        <b>Downloads:</b> {int(row['downloads'])}
        """

        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=radius,
            popup=popup_html,
            tooltip=f"{row['city']} ({int(row['downloads'])})",
            color="#cc7000",
            weight=1,
            fill=True,
            fill_color="#ff8c00",
            fill_opacity=0.75
        ).add_to(cluster)

    st_folium(m, use_container_width=True, height=600)