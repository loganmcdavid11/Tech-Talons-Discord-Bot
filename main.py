"""
Name: Logan McDavid
Filename: main.py    
Purpose: Startup for Tech Talons Discord
Bot as well as necessary bot token
"""
import discord
import asyncio
import os
from discord.ext import commands
import apikeys

# Members intents
intents = discord.Intents.default()
intents.members = True

# Initializing instance of bot and the prefix command
client = commands.Bot(command_prefix = '!', intents = discord.Intents.all(), help_command=None) # Disable help command

# Load all files from cog folder
async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')
            
# Turns the Talons Bot on
async def main():
    await load()
    await client.start(apikeys.BOT_TOKEN)
            


# Main bot turning on
@client.event
async def on_ready():
    print('The bot is now ready for use captain!')
    print('--------------------------------------')
    
    

# Execute main function and run the Talons Bot
asyncio.run(main())