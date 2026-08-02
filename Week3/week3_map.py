import geopandas as gpd
import pandas as pd
import folium
from folium.plugins import MiniMap, Fullscreen

# ------------------------------------------------------------
# Function: load_shapefile
# ------------------------------------------------------------
def load_shapefile(path):
    """
    This function loads a shapefile using GeoPandas. It reads the file from the path I have given it, and returns a GeoDataFrame containing the geodata from the shapefile.
    """
    return gpd.read_file(path)


# ------------------------------------------------------------
# Function: convert_to_wgs84
# ------------------------------------------------------------
def convert_to_wgs84(gdf):
    """
   In order to run correctly, folium requires coordinates in WGS84 (EPSG:4326)
    input: GeoDataFrame (gdf)
    output: gdf in WSG84
    """
    return gdf.to_crs(epsg=4326)


# ------------------------------------------------------------
# Function: join_transport_data
# ------------------------------------------------------------
def join_transport_data(wards, transport_df):
    """
	This function joins transport data to the wards layer using the Ward Code column found in both layer files.
	input: wards (gdf of ward polygons), transport_df (DataFrame with bus, train, and distance info)
	output: a merged gdf containing both spatial and transport information.
    """
    return wards.merge(transport_df, on="Ward Code", how="left")


# ------------------------------------------------------------
# Function: create_base_map
# ------------------------------------------------------------
def create_base_map():
    """
	This function creates the main folium base map. 
    """
    return folium.Map(location=[54.7, -6.5], zoom_start=8, tiles="cartodbpositron")


# ------------------------------------------------------------
# Function: add_wards_layer
# ------------------------------------------------------------
def add_wards_layer(map_obj, wards):
    """
    This function adds the ward polygons to the map. It includes tooltips (ward names appear when hovered over with your mouse), pop-ups (population and transport info appear when ward is clicked on) and styles the polygons.
	Input: map_obj(the folium map), wards (the gsf of wards)
	Outputs: modifies the preexisitng map
    """
    folium.GeoJson(
        wards,
        name="Wards",
        style_function=lambda feature: {
            "fillColor": "#3186cc",
            "color": "black",
            "weight": 1,
            "fillOpacity": 0.4,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["Ward"],
            aliases=["Ward:"]
        ),
        popup=folium.GeoJsonPopup(
            fields=["Ward", "Population", "NumBus", "NearestTrain", "Distance"],
            aliases=["Ward:", "Population:", "Bus Routes:", "Nearest Train:", "Distance (km):"]
        )
    ).add_to(map_obj)


# ------------------------------------------------------------
# Function: add_choropleth
# ------------------------------------------------------------
def add_choropleth(map_obj, wards):
    """
   This creates a choropleth layer based on population by colouring wards on a scale of lowest population to highest population.
	Input: map_obj (the folium map), wards (gdf with population field)
	Output: Adds a layer to the map
    """
    folium.Choropleth(
        geo_data=wards,
        data=wards,
        columns=["Ward Code", "Population"],
        key_on="feature.properties.Ward Code",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Population"
    ).add_to(map_obj)


# ------------------------------------------------------------
# Function: add_counties_layer
# ------------------------------------------------------------
def add_counties_layer(map_obj, counties):
    """
	This fuction adds an overlay layer of county boundaries with green outlines.
	Input: map_obj (the folium map), counties (gdf of counties)
	Output: adds a layer to map
    """
    folium.GeoJson(
        counties,
        name="Counties",
        style_function=lambda feature: {
            "color": "green",
            "weight": 2,
            "fillOpacity": 0
        }
    ).add_to(map_obj)


# ------------------------------------------------------------
# Function: add_roads_layer
# ------------------------------------------------------------
def add_roads_layer(map_obj, roads):
    """
  	This adds a layer of red lines showing roads. It is useful for showing transport routes.
	Input: map_obj (the folium map), roads (gdf of roads)
	Output: Adds layer to map
    """
    folium.GeoJson(
        roads,
        name="Roads",
        style_function=lambda feature: {
            "color": "red",
            "weight": 1
        }
    ).add_to(map_obj)


# ------------------------------------------------------------
# Function: add_airports_layer
# ------------------------------------------------------------
def add_airports_layer(map_obj, airports_df):
    """
  	This function adds airport markers to the map using lat/lon from the airport csv provided in wekk 3 data files. When pop-ups are clicked they will show the airport name and website link.
	Input: map_obj (the folium map), airports_df (DataFrame with airport info)
	Output: adds a layer to map
    """
    for _, row in airports_df.iterrows():
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=f"{row['name']}<br><a href='{row['website']}' target='_blank'>Website</a>",
            icon=folium.Icon(color="blue", icon="plane", prefix="fa")
        ).add_to(map_obj)


# ------------------------------------------------------------
# Function: add_plugins
# ------------------------------------------------------------
def add_plugins(map_obj):
    """
    This function will add extra map features to make the map look more professional - a minimap, fullscreen button, and layer control.
    """
    MiniMap().add_to(map_obj)
    Fullscreen().add_to(map_obj)
    folium.LayerControl().add_to(map_obj)


# ------------------------------------------------------------
# MAIN FUNCTION
# ------------------------------------------------------------
def main():
    """
	Below is the full script workflow:
    """

    # Load shapefiles
    wards = load_shapefile("data_files/NI_Wards.shp")
    counties = load_shapefile("data_files/Counties.shp")
    roads = load_shapefile("data_files/NI_roads.shp")

    # Convert to WGS84
    wards = convert_to_wgs84(wards)
    counties = convert_to_wgs84(counties)
    roads = convert_to_wgs84(roads)

    # Load CSVs
    airports = pd.read_csv("data_files/Airports.csv")
    transport = pd.read_csv("data_files/transport_data.csv")

    # Join transport data to wards
    wards = join_transport_data(wards, transport)

    # Create base map
    m = create_base_map()

    # Add layers
    add_wards_layer(m, wards)
    add_choropleth(m, wards)
    add_counties_layer(m, counties)
    add_roads_layer(m, roads)
    add_airports_layer(m, airports)

    # Add plugins
    add_plugins(m)

    # Save map
    m.save("map.html")
    print("Map created and saved as map.html")


# ------------------------------------------------------------
# Run main
# ------------------------------------------------------------
if __name__ == "__main__":
    main()
