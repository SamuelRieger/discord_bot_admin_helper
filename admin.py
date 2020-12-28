
import discord
import os
import time
import random
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv, find_dotenv
from threading import Thread
from time import sleep
from typing import Awaitable

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN_ADMIN')
intents = discord.Intents.default()
intents.members = True

# Set prefix for bot commands.
client = commands.Bot(command_prefix = ',', intents=intents)

# ** Bot Online ** #
@client.event
async def on_ready():
    print('Bot Online')

# ** Kick User ** #
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member = None):
    if user:    
        await ctx.send(f':boot: {user.mention} has been successfully **kicked**.')
        await user.kick(reason='Kicked by bot.')
        print (f'Kicked {user.name}.')
        return
    await ctx.say('Please @ a user to kick.')

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, discord.ext.commands.BadArgument):
        await ctx.send(f'{ctx.message.author.mention} please @ a valid user.')
    if isinstance(error, discord.ext.commands.MissingPermissions):
        await ctx.send(f'{ctx.message.author.mention} you don\'t have permission to do that!') 

# ** Ban User ** #
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member = None):
    if user: 
        await ctx.send(f':no_entry: {user.mention} has been successfully **banned**.')
        await user.ban(reason='Banned by bot.')
        print (f'Banned {user.name}.')
        return
    await ctx.say('Please @ a user to ban.')

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, discord.ext.commands.BadArgument):
        await ctx.send(f'{ctx.message.author.mention} please @ a valid user.')
    if isinstance(error, discord.ext.commands.MissingPermissions):
        await ctx.send(f'{ctx.message.author.mention} you don\'t have permission to do that!') 

# ** Mute User ** #
@client.command()
@commands.has_guild_permissions(mute_members=True)
async def mute(ctx, user: discord.Member = None):
    if user:
        role = discord.utils.get(ctx.guild.roles, name='Muted')
        if not role:
            # Create mute role if one does not exist.
            role = await ctx.guild.create_role(name='Muted', permissions=discord.Permissions(speak=False, send_messages=False))
            await ctx.send(f'New role {role.mention} created!')
            text_channels = ctx.guild.text_channels
            voice_channels = ctx.guild.voice_channels
            for text_channel in text_channels:
                mute_permissions = discord.PermissionOverwrite()
                mute_permissions.send_messages = False
                await text_channel.set_permissions(role, overwrite=mute_permissions)
            for voice_channel in voice_channels:
                mute_permissions = discord.PermissionOverwrite()
                mute_permissions.speak = False
                await voice_channel.set_permissions(role, overwrite=mute_permissions)
        if role not in user.roles:
            await user.add_roles(role) 
            print('suer')
            await user.edit(mute=True)
            await ctx.send(f':mute: {user.mention} has been successfully **muted**.')
            print (f'Muted {user.name}.')
            return
        await ctx.send(f':warning: {user.mention} is already **muted**.')
        return
    await ctx.send('Please @ a user to mute.')

@mute.error
async def mute_error(ctx, error):
    if isinstance(error, discord.ext.commands.BadArgument):
        await ctx.send(f'{ctx.message.author.mention} please @ a valid user.')
    if isinstance(error, discord.ext.commands.MissingPermissions):
        await ctx.send(f'{ctx.message.author.mention} you don\'t have permission to do that!') 

# ** Unmute User ** #
@client.command()
@commands.has_guild_permissions(mute_members=True)
async def unmute(ctx, user: discord.Member = None):
    if user:
        role = discord.utils.get(ctx.guild.roles, name='Muted')
        if not role:
            # Create mute role if one does not exist.
            role = await ctx.guild.create_role(name='Muted', permissions=discord.Permissions(speak=False, send_messages=False))
            await ctx.send(f'New role {role.mention} created!')
            text_channels = ctx.guild.text_channels
            voice_channels = ctx.guild.voice_channels
            for text_channel in text_channels:
                mute_permissions = discord.PermissionOverwrite()
                mute_permissions.send_messages = False
                await text_channel.set_permissions(role, overwrite=mute_permissions)
            for voice_channel in voice_channels:
                mute_permissions = discord.PermissionOverwrite()
                mute_permissions.speak = False
                await voice_channel.set_permissions(role, overwrite=mute_permissions)
        if role in user.roles:
            await user.remove_roles(role)
            await user.edit(mute=False)
            await ctx.send(f':speaker: {user.mention} has been successfully **unmuted**.')
            print(f'Unmuted {user.name}.')
            return
        await ctx.send(f':warning: {user.mention} is already **unmuted**.')
        return
    await ctx.send('Please @ a user to mute.')

@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, discord.ext.commands.BadArgument):
        await ctx.send(f'{ctx.message.author.mention} please @ a valid user.')
    if isinstance(error, discord.ext.commands.MissingPermissions):
        await ctx.send(f'{ctx.message.author.mention} you don\'t have permission to do that!') 

# ** Deafen User ** #
@client.command()
@commands.has_guild_permissions(deafen_members=True)
async def deafen(ctx, user: discord.Member = None):
    if user:
        if user.voice.deaf == False:
            await user.edit(deafen=True)
            await ctx.send(f':mute: {user.mention} has been successfully **deafened**.')
            print (f'Deafened {user.name}.')
            return
        await ctx.send(f':warning: {user.mention} is already **deafened**.') 
        return
    await ctx.send('Please @ a user to deafen.')

@deafen.error
async def deafen_error(ctx, error):
    if isinstance(error, discord.ext.commands.BadArgument):
        await ctx.send(f'{ctx.message.author.mention} please @ a valid user.')
    if isinstance(error, discord.ext.commands.MissingPermissions):
        await ctx.send(f'{ctx.message.author.mention} you don\'t have permission to do that!') 

# ** Undeafen User ** #
@client.command()
@commands.has_guild_permissions(deafen_members=True)
async def undeafen(ctx, user: discord.Member = None):
    if user:
        if user.voice.deaf == True:
            await user.edit(deafen=False)
            await ctx.send(f':speaker: {user.mention} has been successfully **undeafened**.')
            print (f'Deafened {user.name}.')
            return
        await ctx.send(f':warning: {user.mention} is already **undeafened**.') 
        return
    await ctx.send('Please @ a user to deafen.')

@undeafen.error
async def undeafen_error(ctx, error):
    if isinstance(error, discord.ext.commands.BadArgument):
        await ctx.send(f'{ctx.message.author.mention} please @ a valid user.')
    if isinstance(error, discord.ext.commands.MissingPermissions):
        await ctx.send(f'{ctx.message.author.mention} you don\'t have permission to do that!') 

# ** Disconnect User ** #
@client.command()
@commands.has_guild_permissions(move_members=True)
async def disconnect(ctx, user: discord.Member = None):
    if user:
        if user.voice:
            await user.edit(voice_channel=None)
            await ctx.send(f':electric_plug: {user.mention} has been successfully **disconnected**.')
            print(f'Disconnected {user.name}.')
            return
        await ctx.send(f':warning: {user.mention} is not currently in a voice channel.')
        return
    await ctx.send('Please @ a user to disconnect.')

@disconnect.error
async def disconnect_error(ctx, error):
    if isinstance(error, discord.ext.commands.BadArgument):
        await ctx.send(f'{ctx.message.author.mention} please @ a valid user.')
    if isinstance(error, discord.ext.commands.MissingPermissions):
        await ctx.send(f'{ctx.message.author.mention} you don\'t have permission to do that!') 

# Run bot using token.
client.run(TOKEN)
