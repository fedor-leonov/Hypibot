import discord
from discord.ext import commands
from discord.ext import tasks
from dotenv import load_dotenv
from datetime import datetime
import requests
import asyncio
import logging
import os


commandPrefix = '$'
load_dotenv() # load dotenv
discordBotkey = os.getenv('BOTKEY')
hypixelKey = os.getenv('HYPIXELKEY')
botDescription = 'Bday Gift for Dad'
error = "Oops! Error occured!"
logFile = 'bot.log'

#set up discord intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.moderation = True

#enable log
handler = logging.FileHandler(filename=logFile, encoding='utf-8', mode='w')
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix=f'{commandPrefix}', description=f'{botDescription}', intents=intents)
    
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('with Postgres Databases'))

@bot.command()
async def lastOnline(ctx, username):
    playerData = requests.get(
        url = "https://api.hypixel.net/player",
        params = {
            "key": f"{hypixelKey}",
            "name": f"{username}"
        }
    ).json()
    if playerData["success"]:
        if(playerData == "null"):
            await ctx.send(error)
        else:
            try:
                lastLogout = playerData["player"]["lastLogout"]
                await ctx.send(f"{username} was last online at {datetime.fromtimestamp(lastLogout/1000)}")
            except KeyError:
                await ctx.send(f"Hypixel API does not have online info about {username}")
    else:
        await ctx.send(error + "Have you searched this name recently?")


@bot.command()
async def isOnline(ctx, username):
    playerID = requests.get(
        url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    ).json()["id"]
    playerData = requests.get(
        url = "https://api.hypixel.net/status",
        params = {
            "key": f"{hypixelKey}",
            "uuid": f"{playerID}"
        }
    ).json()
    if playerData["success"]:
        if playerData["session"]["online"]:
            await ctx.send(f"{username} is currently online!")
        else:
                await ctx.send(f"{username} is currently not online!")
    else:
        await ctx.send(error + " Have you searched this name recently?")

@tasks.loop(seconds=10)
async def watchUser(ctx, username):
    playerID = requests.get(
        url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    ).json()["id"]
    playerData = requests.get(
        url = "https://api.hypixel.net/status",
        params = {
            "key": f"{hypixelKey}",
            "uuid": f"{playerID}"
        }
    ).json()
    if playerData["success"]:
        if playerData["session"]["online"]:
            await ctx.send(f"{username} is on!")
        else:
            await ctx.send(f"{username} is not on!")
    else:
        await ctx.send(error + " Have you searched this name recently?")


@bot.command()
async def createWatchPoint(ctx, username):
    watchUser(ctx, username).start()
    
@bot.command()
async def createChannel(ctx, category, channel):
    categoryName = category
    category = discord.utils.get(ctx.guild.categories, name=categoryName)
    await ctx.guild.create_text_channel(f'{channel}', category=category)

@bot.command()
async def createRole(ctx, roleName, perm):
    author = ctx.message.author
    await author.add_roles(await ctx.guild.create_role(name=f"{roleName}", permissions=discord.Permissions(permissions=int(perm))))
    
@bot.command()
async def turnOff(ctx):
    await ctx.send("Closing bot connection...")
    await bot.close()

bot.run(discordBotkey, log_handler=handler)



