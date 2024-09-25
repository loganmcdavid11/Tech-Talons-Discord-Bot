"""
Name: Logan McDavid    
Filename: channel_commands.py
Purpose: Contains commands associated
with adding and removing yourself 
to and from specific roles
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
            if cutter not in member_name.roles:
                await member_name.add_roles(cutter)
                await ctx.send(f"{member_name.mention} is now a 'cutter'")
            else:
                await ctx.send(f"{member_name.mention} is already a 'cutter'")
                
        if 'handler' in normalized_position:
            if handler not in member_name.roles:
                await member_name.add_roles(handler)
                await ctx.send(f"{member_name.mention} is now a 'handler'")
            else:
                await ctx.send(f"{member_name.mention} is already a 'handler'")
                
        if not ('cutter' in normalized_position or 'handler' in normalized_position):
            await ctx.send("Error: Please specify 'cutter', 'handler' or both")
            
    @commands.command()
    async def remove_position(self, ctx, *position):
        member_name = ctx.author
        
        cutter = discord.utils.get(ctx.guild.roles, name='Cutter')
        handler = discord.utils.get(ctx.guild.roles, name='Handler')
    
        normalized_position = [pos.lower() for pos in position]
        
        if 'cutter' in normalized_position:
            if cutter in member_name.roles:
                await member_name.remove_roles(cutter)
                await ctx.send(f"{member_name.mention} is no longer a 'cutter'")
            else:
                await ctx.send(f"{member_name.mention} does not have 'cutter' permissions")
                
        if 'handler' in normalized_position:
            if handler in member_name.roles:
                await member_name.remove_roles(handler)
                await ctx.send(f"{member_name.mention} is no longer a 'handler'")
            else:
                await ctx.send(f"{member_name.mention} does not have 'handler' positions")
                
        if not ('cutter' in normalized_position or 'handler' in normalized_position):
            await ctx.send("Error: Please specify 'cutter', 'handler' or both")
         
    @commands.command()
    async def add_tournament_role(self, ctx):
        member_name = ctx.author
        
        tournament = discord.utils.get(ctx.guild.roles, name='Tournament')
        
        
        if tournament not in member_name.roles:
            await member_name.add_roles(tournament)
            await ctx.send(f"{member_name.mention} is now in the 'tournament' chat!")
        else:
            await ctx.send(f"{member_name.mention} is already in the 'tournament' chat")
            
    @commands.command()
    async def remove_tournament_role(self, ctx):
        member_name = ctx.author
        
        tournament = discord.utils.get(ctx.guild.roles, name='Tournament')
        
        
        if tournament in member_name.roles:
            await member_name.remove_roles(tournament)
            await ctx.send(f"{member_name.mention} has been removed from the 'tournament' chat!")
        else:
            await ctx.send(f"{member_name.mention} is already not in the 'tournament' chat")
                
    @commands.command()
    async def add_purple_gold(self, ctx, team):
        member_name = ctx.author
        
        purple_team = discord.utils.get(ctx.guild.roles, name='Team Purple')
        gold_team = discord.utils.get(ctx.guild.roles, name='Team Gold')
        
        normalized_team = team.lower()
        
        if 'purple' in normalized_team:
            if purple_team not in member_name.roles:
                if gold_team in member_name.roles:
                    await ctx.send(f"{member_name.mention}, please leave gold team before you can join purple")
                else:
                    await member_name.add_roles(purple_team)
                    await ctx.send(f"{member_name.mention} has joined the purple team")
        
        if 'gold' in normalized_team:
            if gold_team not in member_name.roles:
                if purple_team in member_name.roles:
                    await ctx.send(f"{member_name.mention}, please leave purple team before you can join gold") 
                else:
                    await member_name.add_roles(gold_team)
                    await ctx.send(f"{member_name.mention} has joined the gold team")
                
        if not('purple' in normalized_team or 'gold' in normalized_team):
            await ctx.send("Error: Please specify 'purple' or 'gold'")
            
    @commands.command()
    async def remove_purple_gold(self, ctx, team):
        member_name = ctx.author
        
        purple_team = discord.utils.get(ctx.guild.roles, name='Team Purple')
        gold_team = discord.utils.get(ctx.guild.roles, name='Team Gold')
        
        normalized_team = team.lower()
        
        if 'purple' in normalized_team: 
            if purple_team in member_name.roles:
                await member_name.remove_roles(purple_team)
                await ctx.send(f"{member_name.mention} has left the purple team")
            else:
                await ctx.send(f"{member_name.mention} does not have 'purple' permissions")

        
        if 'gold' in normalized_team:
            if gold_team in member_name.roles:
                await member_name.remove_roles(gold_team)
                await ctx.send(f"{member_name.mention} has left the gold team")
            else:
                await ctx.send(f"{member_name.mention} does not have 'gold' permissions")
                
        if not('purple' in normalized_team or 'gold' in normalized_team):
            await ctx.send("Error: Please specify 'purple' or 'gold'")
                
        
# Set up Channel Bot
async def setup(bot):
    await bot.add_cog(ChannelCommands(bot))