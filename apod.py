import requests
import json
import discord
import asyncio
import datetime
import os
import time
from bs4 import BeautifulSoup

# Downloads APOD to local system and also writes copyright holder and image explanation.
def apodLoad(API_KEY):
    # API URL to access image
    url = 'https://api.nasa.gov/planetary/apod'

    # Parameters (must include api_key)
    params = {
        'hd':'True',
        'api_key':API_KEY,
    }

    # Request response from url and write response to json file. If json data not present
    # due to server outage, web scraper is executed as a backup.
    response = requests.get(url, params=params)
    try:
        json_data = json.loads(response.text)

    except json.decoder.JSONDecodeError:
        return apodScrape()
    
    try:
        print(json_data)
    except UnicodeEncodeError:
        print("UnicodeEncodeError detected... not printing JSON data")

    # Load title and explanation into a string
    # Note that strings are encoded in utf-8 and not ASCII to display special characters
    title = json_data['title'].encode('utf-8', errors='ignore').decode()
    explanation = json_data['explanation'].encode('utf-8', errors='ignore').decode()

    # Write copyright holder if it exists. If not, message is displayed to console.
    copyrightFlag = False
    try:
        copyright = json_data['copyright'].encode('utf-8', errors='ignore').decode()
        copyrightFlag = True

    except KeyError:
        print("No author or copyright holder found. Not adding to apod.txt.")

    # Download image
    if json_data['media_type'] == 'image':
        try:
            image_url = json_data['hdurl']
        except KeyError:
            image_url = json_data['url']

        img_data = requests.get(image_url).content
        with open('apod.jpg', 'wb') as handler:
            handler.write(img_data)

        # Write title, explanation, and copyright if it exists to apod.txt file
        with open('apod.txt', mode='a', encoding='utf-8') as f:
            f.truncate(0)

            f.write('Title: "' + title + '"\n\n')

            if (copyrightFlag):
                f.write('Copyright: ' + copyright + '\n\n')

            f.write(explanation)
            f.close()

        return True

    # If media type is video link, paste url to apod.txt and send instead
    else:
        video_url = json_data['url']

        with open('apod.txt', mode='a', encoding='utf-8') as f:
            f.truncate(0)

            f.write(video_url + '\n\n')
            f.write('Title: "' + title + '"\n\n')

            if (copyrightFlag):
                f.write('Copyright: ' + copyright + '\n\n')

            f.write(explanation)
            f.close()

            return False

# Web scraper using BeautifulSoup to extract apod image from main website if API server
# is down.
def apodScrape():
    url = 'https://apod.nasa.gov/apod/'

    # Load response from apod.nasa.gov url and parse using BeautifulSoup. Find image tags.
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    img_tags = soup.findAll('img')

    if len(img_tags) == 0:
        return
    
    # Load first image tags as apod and append apod source to main url for final url
    apod = img_tags[0]
    apod_src = apod.attrs['src']
    image_url = url + apod_src

    # Extract title and explanation by finding <b> tag labeled " Explanation: "
    title = soup.findAll('title')[0].get_text().replace('\n', '').encode('utf-8', errors='ignore').decode()
    def findExlTag(tag):
        return tag.name == 'p' and tag.b and tag.b.string == ' Explanation: '
    
    explanation = soup.find(findExlTag).get_text().replace('\n', ' ').encode('utf-8', errors='ignore').decode()

    # Write image to local system
    img_data = requests.get(image_url).content
    with open('apod.jpg', 'wb') as handler:
        handler.write(img_data)

    # Write title and explanation to local system
    with open('apod.txt', 'a', encoding='utf-8') as f:
        f.truncate(0)
        f.write('Title: "' + title + '"\n\n')
        f.write(explanation)

# Send apod.jpg and apod.txt to UCF Astronomy Society Discord server.
async def apodSend(client, config, isImg):
    date = datetime.datetime.now()
    today = date.strftime("%A, %B %d, %Y")

    # Extract guild, role, and channel from supplied config file.
    guild = client.get_guild(config["GUILD"])
    apodRole = discord.utils.get(guild.roles, name='apod')
    apodChannel = client.get_channel(config["APOD CHANNEL ID"])

    # Send date, apod.jpg, and apod.txt
    if isImg:
        await apodChannel.send(f"<@&{apodRole.id}> Astronomy Picture of the Day for {today}:", file=discord.File("./apod.jpg"))
    else:
        await apodChannel.send(f"<@&{apodRole.id}> Astronomy Picture of the Day for {today}:")

    with open('apod.txt', mode='r', encoding='utf-8') as f:
        data = f.read()
        await apodChannel.send(data)
