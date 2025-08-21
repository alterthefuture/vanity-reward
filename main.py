import os
import discord
from discord.ext import commands
import asyncio
import os

os.system(f'cls & mode 85,20 & title [DISCORD.GG/WRD] - PLAYEDYABTCH')

intents = discord.Intents.all() # TURN ON INTENTS IN DISCORD DEVELOPER PORTAL FOR YOUR BOT INSTANCE
client = commands.Bot(command_prefix="!",intents=intents,case_insensitive=True)

token = "token-here" # REPLACE WITH YOUR BOT TOKEN

@client.event
async def on_ready():
    print("bot is online.")

@client.event 
async def on_message(message):
    if message.author.bot:
        return

    await client.process_commands(message) 

async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            await client.load_extension(f'cogs.{filename[:-3]}')

async def main():
    async with client:
        await load_cogs()
        await client.start(token)

asyncio.run(main()) # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
