import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import mysql.connector

# MySQL database connection details
host = 'localhost'
user = 'root'
password = ''
database = 'DeMa'
port = '3308'

# Establish a connection to the MySQL database
connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database,
    port=port
)

# Retrieve data from MySQL table
query = 'SELECT name, lon, lat, song1, song1_lon, song1_lat, song2, song2_lon, song2_lat, song3, song3_lon, song3_lat FROM LatLon'
df = pd.read_sql(query, connection)

# Generate four points for each row
points = []
for _, row in df.iterrows():
    name = row['name']
    lat = row['lat']
    lon = row['lon']
    
    # Generate four points by modifying the latitude and longitude
    #point1 = (lat, lon)
    point2 = (row['song1_lat'], row['song1_lon'])
    point3 = (row['song2_lat'], row['song2_lon'])
    point4 = (row['song3_lat'], row['song3_lon'])
    
    # Append the points to the list
    points.append([name, point2, point3, point4])

# Create a new DataFrame with the points
points_df = pd.DataFrame(points, columns=['name', 'point2', 'point3', 'point4'])

# Reshape the DataFrame to have one point per row
points_df = points_df.melt(id_vars='name', value_name='point').drop(columns='variable')

# Extract latitude and longitude from the 'point' column
points_df[['lat', 'lon']] = pd.DataFrame(points_df['point'].tolist(), index=points_df.index)
points_df = points_df.drop(columns='point')

# Convert DataFrame to GeoDataFrame
gdf = gpd.GeoDataFrame(points_df, geometry=gpd.points_from_xy(points_df.lon, points_df.lat))

# Read the shapefile or GeoJSON file for Greece
greece_map = gpd.read_file('france-regions.geojson')

# Plot the base map of Greece
greece_map.plot(color='lightgray')

# Customize visualization settings
unique_names = points_df['name'].unique()
num_colors = len(unique_names)
color_map = plt.get_cmap('tab20')
colors = [color_map(i / num_colors) for i in range(num_colors)]

# Create a dictionary mapping each name to its corresponding color
name_color_dict = dict(zip(unique_names, colors))

# Add a new column to the GeoDataFrame to store colors
gdf['color'] = gdf['name'].map(name_color_dict)

# Display the graph map
gdf.plot(color=gdf['color'], ax=plt.gca())

# Set labels for x and y axes
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Create a legend for the colors
legend_elements = [plt.Line2D([0], [0], marker='o', color='w', label=name, markerfacecolor=color)
                   for name, color in name_color_dict.items()]
plt.legend(handles=legend_elements, title='Names', loc='upper right')

# Show the plot
plt.show()

# Close the MySQL connection
connection.close()
