
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

load_dotenv(find_dotenv())
TOKEN = os.getenv('DISCORD_TOKEN')
print(TOKEN)
intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = ',', intents=intents)
stop = False

@client.event
async def on_ready():
    print('Bot Online')

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member = None):
    if user:    
        await ctx.send(f':boot: **{user.name}** has been successfully **kicked**.')
        await user.kick(reason='Kicked by bot.')
        print (f'Kicked {user.name}.')
    else:
        await ctx.say("Please @ a user to kick.")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, discord.ext.commands.BadArgument):
        await ctx.send(f'{ctx.message.author.mention} please @ a valid user.')
    if isinstance(error, discord.ext.commands.MissingPermissions):
        await ctx.send(f'{ctx.message.author.mention} you don\'t have permission to do that!') 

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member = None):
    if user: 
        await ctx.send(f':no_entry: **{user.name}** has been successfully **banned**.')
        await user.ban(reason='Banned by bot.')
        print (f'Banned {user.name}.')
    else:
        await ctx.say("Please @ a user to ban.")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, discord.ext.commands.BadArgument):
        await ctx.send(f'{ctx.message.author.mention} please @ a valid user.')
    if isinstance(error, discord.ext.commands.MissingPermissions):
        await ctx.send(f'{ctx.message.author.mention} you don\'t have permission to do that!') 

client.run('NzgxMzE0NDQ1OTU1NTYzNTYx.X771yA.9VhlBLMb4FRixio-RldBatwqMm0')
