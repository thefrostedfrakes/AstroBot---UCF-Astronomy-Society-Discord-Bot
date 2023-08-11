import discord
import time
import asyncio
import json
from discord.ext import commands
from rolecommands import roles_command, addrole_command, removerole_command
from apod import apodLoad, apodSend
from purge import purge
from iss import send_iss

intents = discord.Intents.all()
client = commands.Bot(intents=intents, command_prefix='!')
client.remove_command('help')

with open('config.json', 'r') as f:
    config = json.load(f)

@client.event
async def on_ready():
    print("AstroBot is online!")
    await client.wait_until_ready()

    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} commands")
    
    except Exception as e:
        print(f"Error syncing commands: {e}")

    isImg = None

    while not client.is_closed():
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)

        if current_time == "11:58:00":
            if isImg is None:
                isImg = apodLoad(config["NASA API KEY"])
        if current_time == "12:00:00":
            if isImg is not None:
                await apodSend(client, config, isImg)
                isImg = None

        await asyncio.sleep(1)

@client.tree.command(name='ping', description="Ping the bot! (Just to test)")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"{interaction.user.mention} pong!", ephemeral=True)

@client.tree.command(name='iss', description="Find out where the ISS is currently overhead!")
async def iss(interaction: discord.Interaction):
    await send_iss(interaction, client, config["ISS CHANNEL ID"])

@client.tree.command(name='roles', description="View all available roles in the server.")
async def roles(interaction: discord.Interaction):
    await roles_command(interaction, client)

@client.tree.command(name='addrole', description="Assign yourself a role.")
async def roles(interaction: discord.Interaction, rolename: str):
    await addrole_command(interaction, rolename, client)

@client.tree.command(name='removerole', description="Remove a role from your account.")
async def roles(interaction: discord.Interaction, rolename: str):
    await removerole_command(interaction, rolename, client)

@client.event
async def on_message(message: discord.Message):
    try:
        print(f"User {message.author} just sent this message in {message.channel.name}: {message.content}")
    except AttributeError as e:
        print(f"Error displaying message sent by {message.author}: {e}")

    if message.author == client.user:
        return

    elif message.content.startswith('-apod-load'):
        if not message.author.guild_permissions.administrator:
            await message.reply('Sorry, you do not have permission to use this command!')
            return
        
        apodLoad(config["NASA API KEY"])

    elif message.content.startswith('-apod-send-img'):
        if not message.author.guild_permissions.administrator:
            await message.reply('Sorry, you do not have permission to use this command!')
            return
        
        await apodSend(client, config, isImg=True)

    elif message.content.startswith('-apod-send-vid'):
        if not message.author.guild_permissions.administrator:
            await message.reply('Sorry, you do not have permission to use this command!')
            return
        
        await apodSend(client, config, isImg=False)

    elif message.content.startswith('-purge'):
        if not message.author.guild_permissions.administrator:
            await message.reply('Sorry, you do not have permission to use this command!')
            return
        str = message.content[7:]
        await purge(message, str)
    

client.run(config["TOKEN"])
