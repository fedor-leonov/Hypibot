import discord
from discord.ext import commands
import os

#get the API key
from dotenv import load_dotenv
load_dotenv()


intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.moderation = True

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='$', description="funny little fedor bot", intents=intents)
    

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("with your mom"))

@bot.event
async def on_reaction_add(reaction, user):
    print(reaction)
    dmuser = await bot.fetch_user(user.id)
    await dmuser.send(f"Do you think you're funny? I know where you live. I'll kill you. Stop adding {reaction} to my messages or else.")

@bot.event
async def on_guild_channel_create(channel):
    print(f'{channel} has been created in {channel.category}')
async def on_error(event, *args, **kwargs):
    message = args[0] 
    await bot.send(message.channel, "oopsy! FedorBot had a fucky wucky because you typed in a wrong command or used a command incorrectly! try again!")

@bot.command()
async def foo(ctx, *, arg):
    await ctx.send(arg)

@bot.command()
async def mystery(ctx):
    print(await bot.fetch_channel(668178989583695886))

@bot.command()
async def turnoff(ctx):
    if ctx.author.id != 919372259842465893:
        await ctx.send("oopsy! FedorBot had a fucky wucky because you're not fedor! try asking fedor to be able to do this command.")
        return
    else:
        await ctx.send("shutting down...")
        await bot.close()

bot.run(os.getenv('KEY'))



