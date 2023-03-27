import requests
import json
import csv
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import re
import discord

# Uses open-notify API and Heavens Above to request ISS latitude, longitude,
# and orbital data, then write to iss.txt and iss.csv
def get_iss():
    # Get requests for lat & long response as well as orbital parameters
    latlon_response = requests.get('http://api.open-notify.org/iss-now.json')
    orbital_response = requests.get('https://www.heavens-above.com/orbit.aspx?satid=25544&lat=28.6144&lng=-81.1965&loc=Unnamed&alt=0&tz=EST')

    json_data = json.loads(latlon_response.text)

    latitude = json_data['iss_position']['latitude']
    longitude = json_data['iss_position']['longitude']

    column_name = ["Latitude", "Longitude"]
    csv_data = [latitude, longitude]

    print("Latitude: " + latitude)
    print("Longitude: " + longitude)

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
        f.write("Latitude: " + latitude + "\n")
        f.write("Longitude: " + longitude + "\n\n")

        for keys, value in orbital_parameters.items():
            f.write(keys + ": " + value + "\n")
        
        # f.write(json.dumps(orbital_parameters, ensure_ascii=False).encode('utf-8').decode())
        f.close()

    with open('iss.csv', mode='w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(column_name)
        writer.writerow(csv_data)

# Creates matplotlib graph using geopandas that graphs coordinate data on world map
def map():
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

async def iss(message, client, channel_id):
    issChannel = client.get_channel(channel_id)
    get_iss()
    map()

    with open('iss.txt', mode='r', encoding='utf-8') as f:
        data = f.read()
        await issChannel.send(data)

    await issChannel.send(file=discord.File("./iss.png"))