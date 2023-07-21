from apihandler import *
import discord
from discord.ext import commands
from discord.ext import tasks
from dotenv import load_dotenv
from datetime import datetime
import requests
import asyncio
import logging
import math
import os

import tracemalloc
tracemalloc.start()


load_dotenv()
commandPrefix = '$'
discordBotkey = os.getenv('BOTKEY')
botDescription = 'Hypixel utility bot'
error = "Oops! Error occured!"
logFile = 'bot.log'

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.moderation = True

handler = logging.FileHandler(filename=logFile, encoding='utf-8', mode='w')
bot = commands.Bot(command_prefix=f'{commandPrefix}', description=f'{botDescription}', intents=intents, status=discord.Status.online, activity=discord.Game('Hypixel'))
    
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

async def getPlayerStatus(username):
    playerStatus = await getPlayerData(username, "status")
    if playerStatus["session"]["online"]:
        result = f"{username} is online."
    else:
        playerData = await getPlayerData(username, "player")
        lastLogout = playerData["player"]["lastLogout"]
        result = f"{username} was last online at {datetime.fromtimestamp(math.floor(lastLogout/1000))}"
    return result

@bot.command()
async def lastOnline(ctx, username):
    try:
        playerStatus = await getPlayerStatus(username)
        await ctx.send(playerStatus)
    except KeyError:
        await ctx.send(f"Hypixel API does not have login info about {username}")
    except:
        await ctx.send(error)

@bot.command()
async def isOnline(ctx, username):
    try:
        playerData = await getPlayerData(username, "status")
        if playerData["session"]["online"]:
            await ctx.send(f"{username} is online.")
        else:
            await ctx.send(f"{username} is offline.")     
    except:
        await ctx.send(error)

async def watchUser(ctx, username):
    switch_state = None
    await bot.wait_until_ready()
    while not bot.is_closed():
        data = await getPlayerData(username, "status")
        if data["session"]["online"]:
            if switch_state != 1:
                embed=discord.Embed(title=f"Online status of {username}", description="Online", color=0x00ff00)
                await ctx.send(embed=embed)
                switch_state = 1
        else:
            if switch_state != 0:
                embed=discord.Embed(title=f"Online status of {username}", description="Offline", color=0xff0000)
                await ctx.send(embed=embed)
                switch_state = 0
        await asyncio.sleep(20)


@bot.command()
async def createWatchPoint(ctx, username):
    bot.loop.create_task(watchUser(ctx, username))

bot.run(discordBotkey, log_handler=handler)




