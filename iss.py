import requests
import json
import csv
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import re
import discord

# Converts latitude and longitude strings to floats, extracts direction from
# coordinate, then returns the abs. value of lat and lon, plus directions
def convert_coordinates(lat: str, lon: str) -> (float, float, str, str):
    lat = float(lat)
    lon = float(lon)
    lat_dir = 'N' if lat >= 0 else 'S'
    lon_dir = 'E' if lon >= 0 else 'W'

    return abs(lat), abs(lon), lat_dir, lon_dir

# Uses open-notify API and Heavens Above to request ISS latitude, longitude,
# and orbital data, then write to iss.txt and iss.csv
def get_iss() -> None:
    # Get requests for lat & long response as well as orbital parameters
    latlon_response = requests.get('http://api.open-notify.org/iss-now.json')
    orbital_response = requests.get('https://www.heavens-above.com/orbit.aspx?satid=25544&lat=28.6144&lng=-81.1965&loc=Unnamed&alt=0&tz=EST')

    json_data = json.loads(latlon_response.text)

    latitude = json_data['iss_position']['latitude']
    longitude = json_data['iss_position']['longitude']

    column_name = ["Latitude", "Longitude"]
    csv_data = [latitude, longitude]

    latitude, longitude, lat_dir, lon_dir = convert_coordinates(latitude, longitude)
    print(f"Latitude: {latitude}")
    print(f"Longitude: {longitude}")

    # Parse text and find parameter lines
    soup = BeautifulSoup(orbital_response.text, 'html.parser')
    txt = soup.get_text()
    matches = re.findall('^([\w\(\)\ ]+)\:\ (.+)$', txt, flags=re.M)

    # Make dict with regex groups from matches
    orbital_parameters = dict()
    for match in matches:
        orbital_parameters[match[0]] = match[1]
    
    print(orbital_parameters)

    with open('iss.txt', mode='a', encoding='utf-8') as f:
        f.truncate(0)
        f.write("Current ISS Coordinates:\n\n")
        f.write(f"Latitude: {latitude}° {lat_dir}\n")
        f.write(f"Longitude: {longitude}° {lon_dir}\n\n")

        for keys, value in orbital_parameters.items():
            f.write(keys + ": " + value + "\n")
        
        # f.write(json.dumps(orbital_parameters, ensure_ascii=False).encode('utf-8').decode())
        f.close()

    with open('iss.csv', mode='w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(column_name)
        writer.writerow(csv_data)

# Creates matplotlib graph using geopandas that graphs coordinate data on world map
def map() -> None:
    df = pd.read_csv('iss.csv', usecols=["Latitude", "Longitude"])

    # Initialize map w/ geopandas
    world_map = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
    ax = world_map.plot(color="grey", figsize=(20,10))
    ax.set_facecolor("#011c40")
    first_point = df.iloc[0]

    # Create map as scatter plot, plot saved as "iss.png"
    plt.scatter(first_point["Longitude"], first_point["Latitude"], s=100, color="red")
    plt.title("ISS Position")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.savefig("iss.png")

async def send_iss(interaction: discord.Interaction, client: discord.Client, channel_id: int) -> None:
    channel = client.get_channel(channel_id)
    if interaction.channel_id != channel_id:
        return await interaction.response.send_message(f"Please post in the {channel.mention} channel to use this command!",
                                                       ephemeral=True)
    
    await interaction.response.defer()
    get_iss()
    map()

    with open('iss.txt', mode='r', encoding='utf-8') as f:
        data = f.read()
        await interaction.followup.send(data, file=discord.File("./iss.png"))
        