import discord
from discord.utils import get
from discord.ext import commands
import json

with open('config.json', 'r') as f:
    config = json.load(f)

channel_id = config["ROLE CHANNEL ID"]

async def roles_command(interaction: discord.Interaction, client: discord.Client) -> None:
    channel = client.get_channel(channel_id)
    if interaction.channel_id != channel_id:
        return await interaction.response.send_message(f"Please post in the {channel.mention} channel to use this command!")
    
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

    await interaction.response.send_message(embed=embed)

async def addrole_command(interaction: discord.Interaction, rolename: str, client: commands.Bot) -> None:
    channel = client.get_channel(channel_id)
    if interaction.channel_id != channel_id:
        return await interaction.response.send_message(f"Please post in the {channel.mention} channel to use this command!")

    undergrad = get(interaction.guild.roles, name='Undergrad')
    grad = get(interaction.guild.roles, name='Grad Student')
    kutsVolunteer = get(interaction.guild.roles, name='KUTS Volunteer')
    alumni = get(interaction.guild.roles, name='Alumni')
    colloquium = get(interaction.guild.roles, name='Colloquium')
    projects = get(interaction.guild.roles, name='Projects')
    trips = get(interaction.guild.roles, name='Trips')
    apod_role = get(interaction.guild.roles, name='apod')
    
    if rolename == '':
        return await interaction.response.send_message('Please enter the role you wish to add! For a list of roles, use -roles')
    if rolename == 'undergrad':
        await interaction.user.add_roles(undergrad)
    elif rolename == 'grad':
        await interaction.user.add_roles(grad)
    elif rolename == 'kuts-volunteer':
        await interaction.user.add_roles(kutsVolunteer)
    elif rolename == 'alumni':
        await interaction.user.add_roles(alumni)
    elif rolename == 'colloquium':
        await interaction.user.add_roles(colloquium)
    elif rolename == 'projects':
        await interaction.user.add_roles(projects)
    elif rolename == 'trips':
        await interaction.user.add_roles(trips)
    elif rolename == 'apod':
        await interaction.user.add_roles(apod_role)
    else:
        return await interaction.response.send_message('That role does not exist! For a list of available roles, use -roles')
    
    print(f"{interaction.user} successfully added role {rolename}")
    await interaction.response.send_message('Role successfully added!')

async def removerole_command(interaction: discord.Interaction, rolename: str, client: commands.Bot) -> None:
    channel = client.get_channel(channel_id)
    if interaction.channel_id != channel_id:
        return await interaction.response.send_message(f"Please post in the {channel.mention} channel to use this command!")

    undergrad = get(interaction.guild.roles, name='Undergrad')
    grad = get(interaction.guild.roles, name='Grad Student')
    kutsVolunteer = get(interaction.guild.roles, name='KUTS Volunteer')
    alumni = get(interaction.guild.roles, name='Alumni')
    colloquium = get(interaction.guild.roles, name='Colloquium')
    projects = get(interaction.guild.roles, name='Projects')
    trips = get(interaction.guild.roles, name='Trips')
    apod_role = get(interaction.guild.roles, name='apod')
    
    if rolename == '':
        return await interaction.response.send_message('Please enter the role you wish to add! For a list of roles, use -roles')
    if rolename == 'undergrad':
        await interaction.user.remove_roles(undergrad)
    elif rolename == 'grad':
        await interaction.user.remove_roles(grad)
    elif rolename == 'kuts-volunteer':
        await interaction.user.remove_roles(kutsVolunteer)
    elif rolename == 'alumni':
        await interaction.user.remove_roles(alumni)
    elif rolename == 'colloquium':
        await interaction.user.remove_roles(colloquium)
    elif rolename == 'projects':
        await interaction.user.remove_roles(projects)
    elif rolename == 'trips':
        await interaction.user.remove_roles(trips)
    elif rolename == 'apod':
        await interaction.user.remove_roles(apod_role)
    else:
        return await interaction.response.send_message('That role does not exist! For a list of available roles, use -roles')
    
    print(f"{interaction.user} successfully removed role {rolename}")
    await interaction.response.send_message('Role successfully removed!')
    