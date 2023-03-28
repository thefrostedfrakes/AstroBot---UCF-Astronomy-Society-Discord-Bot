import requests
import json
import discord
import asyncio
import datetime
import os
import time

def apodLoad(API_KEY):
    # API URL to access image
    url = 'https://api.nasa.gov/planetary/apod'
    KEY_url = 'https://api.nasa.gov/planetary/apod?api_key=P2uKHMPtRKAw5aagztya0EdzBsmaYU66IfjMpuyY'

    # Parameters
    params = {
        'hd':'True',
        'api_key':API_KEY,
    }

    response = requests.get(url, params=params)
    json_data = json.loads(response.text)
    try:
        print(json_data)
    except UnicodeEncodeError:
        print("UnicodeEncodeError detected... not printing JSON data")

    # Load HD image url from json data and extract title and explanation into a string
    # Note that strings are encoded in utf-8 and not ASCII to display special characters
    image_url = json_data['url']
    title = json_data['title'].encode('utf-8', errors='ignore').decode()
    explanation = json_data['explanation'].encode('utf-8', errors='ignore').decode()

    # Write copyright holder if it exists. If not, message is displayed to console.
    x = False
    try:
        copyright = json_data['copyright'].encode('utf-8', errors='ignore').decode()
        x = True

    except KeyError:
        print("No author or copyright holder found. Not adding to apod.txt.")


    # Download image
    imgFlag = False
    try:
        img_data = requests.get(image_url).content
        with open('apod.jpg', 'wb') as handler:
            handler.write(img_data)
        imgFlag = True

    except requests.exceptions.MissingSchema:
        print("No image detected. Sending URL of link instead.")

    # Write title, explanation, and copyright if it exists (x == True) to apod.txt file
    with open('apod.txt', mode='a', encoding='utf-8') as f:
        f.truncate(0)
        if (not imgFlag):
            f.write('https://' + image_url[2:] + '\n')

        f.write('Title: "' + title + '"\n\n')

        if (x):
            f.write('Copyright: ' + copyright + '\n\n')

        f.write(explanation)
        f.close()

async def apodSend(client, config):
    date = datetime.datetime.now()
    today = date.strftime("%A, %B %d, %Y")

    guild = client.get_guild(config["GUILD"])
    apodRole = discord.utils.get(guild.roles, name='apod')
    apodChannel = client.get_channel(config["APOD CHANNEL ID"])

    mod_time = os.path.getmtime('./apod.jpg')
    readable_time = time.ctime(mod_time)
    stripped_time = time.strptime(readable_time)
    formatted_time = time.strftime("%m/%d/%y", stripped_time)

    if formatted_time == datetime.datetime.now().strftime("%m/%d/%y"):
        await apodChannel.send(f"<@&{apodRole.id}> Astronomy Picture of the Day for {today}:", file=discord.File("./apod.jpg"))
    else:
        await apodChannel.send(f"<@&{apodRole.id}> Astronomy Picture of the Day for {today}:")

    with open('apod.txt', mode='r', encoding='utf-8') as f:
        data = f.read()
        await apodChannel.send(data)
