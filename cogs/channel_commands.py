"""
Name:     
Filename: 
Purpose:
"""
import discord
from discord.ext import commands

class ChannelCommands(commands.Cog):
    # Constructor
    def __init__(self, bot):
        self.bot = bot
        
    # Channel bot turning on
    commands.Cog.listener()
    async def on_ready(self):
        print("Library Bot is Online")
    
    @commands.command()
    async def choose_position(self, ctx, *position):
        member_name = ctx.author
        # Get roles from server
        cutter = discord.utils.get(ctx.guild.roles, name='Cutter')
        handler = discord.utils.get(ctx.guild.roles, name='Handler')
        
        # Case insensitive 
        normalized_position = [pos.lower() for pos in position]
        
        # Role assignment
        if 'cutter' in normalized_position:
            if cutter not in member_name.position:
                await member_name.add_roles(cutter)
                await ctx.send(f"{member_name.mention} is now a 'cutter'")
            else:
                await ctx.send(f"{member_name.mention} is already a 'cutter'")
    
         
        
        
        
# Set up Channel Bot
async def setup(bot):
    await bot.add_cog(ChannelCommands(bot))