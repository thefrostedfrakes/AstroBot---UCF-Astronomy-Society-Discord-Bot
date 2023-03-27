import discord
from discord.utils import get
import json

with open('config.json', 'r') as f:
    config = json.load(f)

channel_id = config["ROLE CHANNEL ID"]

async def roles(message, client):

    if message.channel.id != channel_id:
        return
    
    embed = discord.Embed(
        title = "Select your role based on your current status in the club!",
        description = "Available roles:\n\n"
            + "+ undergrad\n\n"
            + "+ grad\n\n"
            + "+ alumni\n\n"
            + "+ kuts-volunteer\n\n"
            + "+ colloquium\n\n"
            + "+ projects\n\n"
            + "+ trips\n\n"
            + "+ apod\n\n"
            + "to add a role, type -addrole, followed by one of the roles listed above. To remove a role, use -removerole followed by the role you wish to remove.",
        color = discord.Color.red()
    )

    message_embed = await message.channel.send(embed=embed)

async def addrole(message, str, client):
    channel = client.get_channel(channel_id)

    undergrad = get(message.guild.roles, name='Undergrad')
    grad = get(message.guild.roles, name='Grad Student')
    kutsVolunteer = get(message.guild.roles, name='KUTS Volunteer')
    alumni = get(message.guild.roles, name='Alumni')
    colloquium = get(message.guild.roles, name='Colloquium')
    projects = get(message.guild.roles, name='Projects')
    trips = get(message.guild.roles, name='Trips')
    apod_role = get(message.guild.roles, name='apod')

    if message.channel != channel:
        return
    
    if str == '':
        return await message.reply('Please enter the role you wish to add! For a list of roles, use -roles')
    if str == 'undergrad':
        await message.author.add_roles(undergrad)
    elif str == 'grad':
        await message.author.add_roles(grad)
    elif str == 'kuts-volunteer':
        await message.author.add_roles(kutsVolunteer)
    elif str == 'alumni':
        await message.author.add_roles(alumni)
    elif str == 'colloquium':
        await message.author.add_roles(colloquium)
    elif str == 'projects':
        await message.author.add_roles(projects)
    elif str == 'trips':
        await message.author.add_roles(trips)
    elif str == 'apod':
        await message.author.add_roles(apod_role)
    else:
        return await message.reply('That role does not exist! For a list of available roles, use -roles')
    
    print('%s successfully added role %s' % (message.author, str))
    await message.reply('Role successfully added!')

async def removerole(message, str, client):
    channel = client.get_channel(channel_id)

    undergrad = get(message.guild.roles, name='Undergrad')
    grad = get(message.guild.roles, name='Grad Student')
    kutsVolunteer = get(message.guild.roles, name='KUTS Volunteer')
    alumni = get(message.guild.roles, name='Alumni')
    colloquium = get(message.guild.roles, name='Colloquium')
    projects = get(message.guild.roles, name='Projects')
    trips = get(message.guild.roles, name='Trips')
    apod_role = get(message.guild.roles, name='apod')

    if message.channel != channel:
        return
    
    if str == '':
        return await message.reply('Please enter the role you wish to add! For a list of roles, use -roles')
    if str == 'undergrad':
        await message.author.remove_roles(undergrad)
    elif str == 'grad':
        await message.author.remove_roles(grad)
    elif str == 'kuts-volunteer':
        await message.author.remove_roles(kutsVolunteer)
    elif str == 'alumni':
        await message.author.remove_roles(alumni)
    elif str == 'colloquium':
        await message.author.remove_roles(colloquium)
    elif str == 'projects':
        await message.author.remove_roles(projects)
    elif str == 'trips':
        await message.author.remove_roles(trips)
    elif str == 'apod':
        await message.author.remove_roles(apod_role)
    else:
        return await message.reply('That role does not exist! For a list of available roles, use -roles')
    
    print('%s successfully removed role %s' % (message.author, str))
    await message.reply('Role successfully removed!')