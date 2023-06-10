import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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

# Define the SQL query to retrieve the data
query = 'SELECT name, lon, lat, song1, song1_lon, song1_lat, song2, song2_lon, song2_lat, song3, song3_lon, song3_lat FROM LatLon'

# Fetch data from MySQL into a pandas DataFrame
df = pd.read_sql(query, connection)

# Create a new DataFrame to store the coordinates of all points
points_df = pd.DataFrame(columns=['name', 'lon', 'lat', 'color'])

# Define a color palette
color_palette = px.colors.qualitative.Set1

# Iterate over the rows of the DataFrame and extract the coordinates for each point
for index, row in df.iterrows():
    color_index = index % len(color_palette)
    points_df = pd.concat([points_df,
                           pd.DataFrame({'name': [row['name'], row['song1'], row['song2'], row['song3']],
                                         'lon': [row['lon'], row['song1_lon'], row['song2_lon'], row['song3_lon']],
                                         'lat': [row['lat'], row['song1_lat'], row['song2_lat'], row['song3_lat']],
                                         'color': [color_palette[color_index]] * 4})],
                          ignore_index=True)

# Create a scatter map using Plotly Express and Mapbox
fig = px.scatter_mapbox(points_df, lat='lat', lon='lon', hover_name='name', color='color',
                        mapbox_style='open-street-map', zoom=10, title='Locations')

# Add lines to connect the points
for index, row in df.iterrows():
    color_index = index % len(color_palette)
    fig.add_trace(go.Scattermapbox(
        mode='lines',
        lon=[row['lon'], row['song1_lon'], row['song2_lon'], row['song3_lon'], row['lon']],
        lat=[row['lat'], row['song1_lat'], row['song2_lat'], row['song3_lat'], row['lat']],
        line=dict(color=color_palette[color_index]),
        showlegend=False
    ))

# Display the map
fig.show()

# Close the MySQL connection
connection.close()
