import discord
import psycopg2
from discord.ext import commands
import os
from database import *

#get the API key
from dotenv import load_dotenv
load_dotenv()

#set up discord intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.moderation = True

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='$', description='funny little fedor bot', intents=intents)

#connect to postgres database
conn = psycopg2.connect(f"dbname={os.getenv('DBNAME')} user={os.getenv('USER')} password={os.getenv('PASSWORD')}")
cur = conn.cursor() # create cursor
print('Connected to database.')

def isFedor(ctx):
    if ctx.author.id == 919372259842465893:
        return True
    else:
        return False
    
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('with your mom'))

@bot.command()
async def table(ctx, *, arg):
    await ctx.send(arg)

@bot.command()
async def mystery(ctx):
    print(await bot.fetch_channel(668178989583695886))

@bot.command()
async def turnoff(ctx):
    if isFedor(ctx):
        await ctx.send("shutting down database...")
        cur.close()
        conn.close()
        await ctx.send("closing bot connection...")
        await bot.close()
    else:
        await ctx.send("oopsy! FedorBot had a fucky wucky because you're not fedor! try asking fedor to be able to do this command.")
        return
        

bot.run(os.getenv('KEY'))



