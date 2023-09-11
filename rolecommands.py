import discord
from discord.utils import get
from discord.ext import commands
import json

with open('config.json', 'r') as f:
    config = json.load(f)

channel_id = config["ROLE CHANNEL ID"]

def get_roles(interaction: discord.Interaction | discord.Message) -> dict:
    return {
        'undergrad': get(interaction.guild.roles, name='Undergrad'),
        'grad': get(interaction.guild.roles, name='Grad Student'),
        'kutsVolunteer': get(interaction.guild.roles, name='KUTS Volunteer'),
        'alumni': get(interaction.guild.roles, name='Alumni'),
        'colloquium': get(interaction.guild.roles, name='Colloquium'),
        'projects': get(interaction.guild.roles, name='Projects'),
        'trips': get(interaction.guild.roles, name='Trips'),
        'apod_role': get(interaction.guild.roles, name='apod')
    }

async def roles_command(interaction: discord.Interaction | discord.Message, client: commands.Bot) -> None:
    channel = client.get_channel(channel_id)
    if type(interaction) == discord.Interaction and interaction.channel_id != channel_id:
        return await interaction.response.send_message(f"Please post in the {channel.mention} channel to use this command!")
    elif type(interaction) == discord.Message and interaction.channel.id != channel_id:
        return await interaction.reply(f"Please post in the {channel.mention} channel to use this command!")
    
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
            + "to add a role, type /addrole, followed by one of the roles listed above. To remove a role, use /removerole followed by the role you wish to remove.",
        color = discord.Color.red()
    )

    if type(interaction) == discord.Interaction:
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.reply(embed=embed)

async def addrole_command(interaction: discord.Interaction | discord.Message, rolename: str, client: commands.Bot) -> None:
    channel = client.get_channel(channel_id)

    is_interaction = True if type(interaction) == discord.Interaction else False
    err_str = f"Please post in the {channel.mention} channel to use this command!"

    if is_interaction and interaction.channel_id != channel_id:
        return await interaction.response.send_message(err_str)
    elif not is_interaction and interaction.channel.id != channel_id:
        return await interaction.reply(err_str)

    roles_dict = get_roles(interaction)
    
    if rolename == '':
        err_str = 'Please enter the role you wish to add! For a list of roles, use /roles'
        if is_interaction:
            return await interaction.response.send_message(err_str, ephemeral=True)
        else:
            return await interaction.reply(err_str)

    if is_interaction:
        if rolename in roles_dict.keys():
            await interaction.user.add_roles(roles_dict[rolename])
        else:
            return await interaction.response.send_message('That role does not exist! For a list of available roles, use /roles',
                                                            ephemeral=True)

        print(f"{interaction.user} successfully added role {rolename}")
        await interaction.response.send_message('Role successfully added!')

    else:
        if rolename in roles_dict.keys():
            await interaction.author.add_roles(roles_dict[rolename])
        else:
            return await interaction.reply('That role does not exist! For a list of available roles, use /roles')
            
        print(f"{interaction.author} successfully added role {rolename}")
        await interaction.reply('Role successfully added!')
    
async def removerole_command(interaction: discord.Interaction | discord.Message, rolename: str, client: commands.Bot) -> None:
    channel = client.get_channel(channel_id)

    is_interaction = True if type(interaction) == discord.Interaction else False
    err_str = f"Please post in the {channel.mention} channel to use this command!"

    if is_interaction and interaction.channel_id != channel_id:
        return await interaction.response.send_message(err_str)
    elif not is_interaction and interaction.channel.id != channel_id:
        return await interaction.reply(err_str)

    roles_dict = get_roles(interaction)
    
    if rolename == '':
        err_str = 'Please enter the role you wish to remove! For a list of roles, use /roles'
        if is_interaction:
            return await interaction.response.send_message(err_str, ephemeral=True)
        else:
            return await interaction.reply(err_str)
        
    if is_interaction:
        if rolename in roles_dict.keys():
            await interaction.user.remove_roles(roles_dict[rolename])
        else:
            return await interaction.response.send_message('That role does not exist! For a list of available roles, use /roles',
                                                            ephemeral=True)

        print(f"{interaction.user} successfully removed role {rolename}")
        await interaction.response.send_message('Role successfully removed!')

    else:
        if rolename in roles_dict.keys():
            await interaction.author.remove_roles(roles_dict[rolename])
        else:
            return await interaction.reply('That role does not exist! For a list of available roles, use /roles')
            
        print(f"{interaction.author} successfully removed role {rolename}")
        await interaction.reply('Role successfully removed!')
