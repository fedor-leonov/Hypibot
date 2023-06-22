import discord
from discord.ext import commands
import psycopg2
import os
from dotenv import load_dotenv
import logging

load_dotenv() #get .env file
#initialize all .env variables
ownerID = os.getenv('OWNERID')
dbName = os.getenv('DBNAME')
dbUser = os.getenv('DBUSER')
dbPass = os.getenv('DBPASSWORD')
key = os.getenv('KEY')

#set up discord intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.moderation = True

#variables
botDescription = 'Discord bot for managing PostgresSQL databases'
error = "oopsy! FedorBot had a fucky wucky! talk to fedor!"
logFile = 'bot.log'

#enable log
handler = logging.FileHandler(filename=logFile, encoding='utf-8', mode='w')

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='$', description=f'{botDescription}', intents=intents)

#connect to postgres database
conn = psycopg2.connect(f"dbname={dbName} user={dbUser} password={dbPass}")
cur = conn.cursor() # create cursor

def ownerCheck(ctx):
    if ctx.author.id == f"{ownerID}":
        return True
    else:
        return False
    
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('with your mom'))

@bot.command()
async def table(ctx, *args):
    if (len(args)/2).is_integer() != True: #check if the length of arguments is a multiple of two
        await ctx.send(error)
    else:
        await ctx.send(args)

@bot.command()
async def createChannel(ctx, category, channel):
    if ownerCheck(ctx):
        categoryName = category
        category = discord.utils.get(ctx.guild.categories, name=categoryName)
        await ctx.guild.create_text_channel(f'{channel}', category=category)
    else:
        await ctx.send(error)

@bot.command()
async def turnoff(ctx):
    if ownerCheck(ctx):
        await ctx.send("shutting down database...")
        cur.close()
        conn.close()
        await ctx.send("closing bot connection...")
        await bot.close()
    else:
        await ctx.send(error)
        return
        

bot.run(key, log_handler=handler)



