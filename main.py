# This example requires the 'message_content' intent.

import discord
from discord.ext import commands 


intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='$', description="funny little fedor bot", intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_reaction_add(reaction, user):
    print(reaction)

@bot.event
async def on_guild_channel_create(channel):
    print(f'{channel} has been created in {channel.category}')

@bot.command()
async def foo(ctx, arg):
    await ctx.send(arg)

bot.run('MTEyMDkzNzA2Nzg4MzUzNjQ0NQ.GWUrWi.f6AjFk3wJRPDWOwkqGK64GD-5sYfffBDNF6gmY')
