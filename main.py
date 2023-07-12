import discord
from discord.ext import commands
import psycopg2
import os
import asyncio
from dotenv import load_dotenv
import logging

commandPrefix = '$'
load_dotenv() # load dotenv
botOwnerDiscordID = os.getenv('OWNERID')
databaseName = os.getenv('DBNAME')
databaseUser = os.getenv('DBUSER')
databasePass = os.getenv('DBPASSWORD')
discordBotkey = os.getenv('KEY')
botDescription = 'Discord bot for managing PostgresSQL databases'
error = "oopsy! FedorBot had a fucky wucky! talk to fedor!"
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

def checkIfUserIsBotOwner(ctx):
    return ctx.author.id == int(botOwnerDiscordID)
    
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('with Postgres Databases'))

@bot.command()
async def foo(ctx, arg):
    await ctx.send(*arg)

@bot.command()
async def createRole(ctx, roleName, perm):
    if checkIfUserIsBotOwner(ctx):
        author = ctx.message.author
        await author.add_roles(await ctx.guild.create_role(name=f"{roleName}", permissions=discord.Permissions(permissions=int(perm))))
    else:
        await ctx.send(error)

@bot.command()
async def createChannel(ctx, category, channel):
    if checkIfUserIsBotOwner(ctx):
        categoryName = category
        category = discord.utils.get(ctx.guild.categories, name=categoryName)
        await ctx.guild.create_text_channel(f'{channel}', category=category)
    else:
        await ctx.send(error)

@bot.command()
async def turnoff(ctx):
    if checkIfUserIsBotOwner(ctx):
        await ctx.send("shutting down database...")
        cur.close()
        conn.close()
        await ctx.send("closing bot connection...")
        await bot.close()
    else:
        await ctx.send(error)
        return
        

bot.run(key, log_handler=handler)



