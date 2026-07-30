import geopandas as gpd
import folium

# Load the wards shapefile
wards = gpd.read_file("data_files/NI_Wards.shp")

# Convert to WGS84 (Folium requires lat/lon)
wards = wards.to_crs(epsg=4326)

# Create a base map centered roughly on Northern Ireland
m = folium.Map(location=[54.7, -6.5], zoom_start=8, tiles="cartodbpositron")

# Add the ward polygons to the map
folium.GeoJson(
    wards,
    name="NI Wards",
    style_function=lambda feature: {
        "fillColor": "#3186cc",
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.4,
    },
    tooltip=folium.GeoJsonTooltip(
        fields=["Ward"],        # ← FIXED
        aliases=["Ward:"]
    )
).add_to(m)

# Add layer control
folium.LayerControl().add_to(m)

# Save the map as an HTML file
m.save("map.html")

print("Map created and saved as map.html")
