import discord
import os
import time
import asyncio
import json
from discord.ext import commands
from rolecommands import roles, addrole, removerole
from apod import apodLoad, apodSend
from purge import purge
from iss import iss

intents = discord.Intents.all()
client = commands.Bot(intents=intents, command_prefix = '-')
client.remove_command('help')

with open('config.json', 'r') as f:
    config = json.load(f)

@client.event
async def on_ready():
    print("AstroBot is online!")
    await client.wait_until_ready()

    while not client.is_closed():
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)

        if current_time == "15:59:30":
            apodLoad(config["NASA API KEY"])
        if current_time == "16:00:00":
            await apodSend(client, config)

        await asyncio.sleep(1)

@client.event
async def on_message(message):
    print('User %s just sent this message in %s: %s' % (message.author, message.channel.name, message.content))

    if message.author == client.user:
        return
    
    if message.content.startswith('-ping'):
        await message.channel.send('pong!')

    elif message.content.startswith('-roles'):
        await roles(message, client)

    elif message.content.startswith('-addrole'):
        str = message.content[9:]
        await addrole(message, str, client)

    elif message.content.startswith('-removerole'):
        str = message.content[12:]
        await removerole(message, str, client)

    elif message.content.startswith('-apod-load'):
        if not message.author.guild_permissions.administrator:
            await message.reply('Sorry, you do not have permission to use this command!')
            return
        apodLoad(config["NASA API KEY"])

    elif message.content.startswith('-apod-send'):
        if not message.author.guild_permissions.administrator:
            await message.reply('Sorry, you do not have permission to use this command!')
            return
        await apodSend(client, config)

    elif message.content.startswith('-purge'):
        if not message.author.guild_permissions.administrator:
            await message.reply('Sorry, you do not have permission to use this command!')
            return
        str = message.content[7:]
        await purge(message, str)

    elif message.content.startswith('-iss'):
        await iss(message, client, config["ISS CHANNEL ID"])
    

client.run(config["TOKEN"])