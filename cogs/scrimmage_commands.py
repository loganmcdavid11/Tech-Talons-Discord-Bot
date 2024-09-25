"""
Name: Logan McDavid
Filename: scrimmage_commands.py    
Purpose: Contains commands associated with
scrimamge scheduling
"""

import discord
import random
from discord.ext import commands


class ScrimmageCommands(commands.Cog):
    # Constructor
    def __init__(self, bot):
        self.bot = bot
        
    
        
        
        
        
        
        
        
        
        
        
        
# Set up Tournament bot
async def setup(bot):
    await bot.add_cog(ScrimmageCommands(bot))
