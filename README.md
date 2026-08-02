EGM733 Resubmission Project - Interactive Folium Map of Northern Ireland Wards

This project creates an interactive folium map of Northern Ireland using ward polygons, counties, roads, airport location, and transport data. The final map includes tooltips, pop-ups, choropleth, as well as additional features such as a minimap and fullscreen toggle mode.
The provided script creates a file called map.html which can be opened in any web browser, although this was trialled in Google Chrome during creation.

Repository Contents;
- week3_map.py -> main python script
- environment.yml -> conda environment file
- LICENSE 
- .gitignore -> ignored file
- data_files -> shapefiles & CSVs
- README.md -> documentation of project


Installation Instructions:

(All of the below steps were carried out on Anaconda Prompt, which was installed via Anaconda Navigator desktop app)

Step 1 - Install Conda

Step 2 - Create the Environment
Run the following code:
	
	conda env create -f environment.yml

Step 3 = Activate the Environent
run:

	conda activate egm722resub 


How to Run This Script:
- Download repository and files and script
- Activate conda environment
- Run:
	python week3_map.py
- Open map.html in a web browser


Data Sources:
- NI_Wards.shp
- Counties.shp
- NI_roads.shp
- Airports.csv
- transport_data.csv

Notes:
- This script requires all files to be inside a file named data_files
- This map uses WGS84 (EPSG:4326)

Author - Aoibh Coogan
