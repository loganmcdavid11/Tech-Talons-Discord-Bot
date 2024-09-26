"""
Name: Logan McDavid    
Filename: channel_commands.py
Purpose: Contains commands associated
with adding and removing yourself 
to and from specific roles
"""
import discord
from discord.ext import commands

# Channel Commands Class
class ChannelCommands(commands.Cog):
    # Constructor
    def __init__(self, bot):
        self.bot = bot
        
    # Channel bot turning on
    commands.Cog.listener()
    async def on_ready(self):
        print("Library Bot is Online")
    
    # Gain Handler and / or Cutter Role
    # !choose_position position-name
    # NOTE: User could also enter 'handler cutter' to join both
    @commands.command()
    async def choose_position(self, ctx, *position):
        # Get username for player choosing position
        member_name = ctx.author
        
        # Get roles from server
        cutter = discord.utils.get(ctx.guild.roles, name='Cutter')
        handler = discord.utils.get(ctx.guild.roles, name='Handler')
        
        # Normalize position(s)
        normalized_position = [pos.lower() for pos in position]
        
        # Role assignment
        # Cutter
        if 'cutter' in normalized_position:
            # Not already cutter
            if cutter not in member_name.roles:
                await member_name.add_roles(cutter)
                await ctx.send(f"{member_name.mention} is now a 'cutter'")
            # Already a cutter
            else:
                await ctx.send(f"{member_name.mention} is already a 'cutter'")
                
        # Handler
        if 'handler' in normalized_position:
            # Not already handler
            if handler not in member_name.roles:
                await member_name.add_roles(handler)
                await ctx.send(f"{member_name.mention} is now a 'handler'")
            # Already handler
            else:
                await ctx.send(f"{member_name.mention} is already a 'handler'")
                
        # Position is invalid
        if not ('cutter' in normalized_position or 'handler' in normalized_position):
            await ctx.send("Error: Please specify 'cutter', 'handler' or both")
            
    # Remove Handler and / or Cutter Role
    # !remove_position position-name
    # NOTE: User could also enter 'handler cutter' to join both
    @commands.command()
    async def remove_position(self, ctx, *position):
        # Get username for player removing position
        member_name = ctx.author
        
        # Get roles from server
        cutter = discord.utils.get(ctx.guild.roles, name='Cutter')
        handler = discord.utils.get(ctx.guild.roles, name='Handler')
    
        # Normalize position(s)
        normalized_position = [pos.lower() for pos in position]
        
        # Role removal
        # Cutter
        if 'cutter' in normalized_position:
            # Has cutter role
            if cutter in member_name.roles:
                await member_name.remove_roles(cutter)
                await ctx.send(f"{member_name.mention} is no longer a 'cutter'")
            # Does not have cutter role
            else:
                await ctx.send(f"{member_name.mention} does not have 'cutter' permissions")
                
        # Handler
        if 'handler' in normalized_position:
            # Has handler role
            if handler in member_name.roles:
                await member_name.remove_roles(handler)
                await ctx.send(f"{member_name.mention} is no longer a 'handler'")
            # Does not have handler role
            else:
                await ctx.send(f"{member_name.mention} does not have 'handler' positions")
                
        # Position is invalid
        if not ('cutter' in normalized_position or 'handler' in normalized_position):
            await ctx.send("Error: Please specify 'cutter', 'handler' or both")
         
    # Add to Tournament Chat
    # !add_tournament_role
    @commands.command()
    async def add_tournament_role(self, ctx):
        # Get username for player adding tournament role
        member_name = ctx.author
        
        # Get role from server
        tournament = discord.utils.get(ctx.guild.roles, name='Tournament')
        
        # Player not assigned tournament role
        if tournament not in member_name.roles:
            await member_name.add_roles(tournament)
            await ctx.send(f"{member_name.mention} is now in the 'tournament' chat!")
        # Player already assigned tournament role
        else:
            await ctx.send(f"{member_name.mention} is already in the 'tournament' chat")
            
    # Remove from Tournament Chat
    # !remove_tournament_role
    @commands.command()
    async def remove_tournament_role(self, ctx):
        # Get username for player removing tournament role
        member_name = ctx.author
        
        # Get role from server
        tournament = discord.utils.get(ctx.guild.roles, name='Tournament')
        
        # Player is assigned tournament role
        if tournament in member_name.roles:
            await member_name.remove_roles(tournament)
            await ctx.send(f"{member_name.mention} has been removed from the 'tournament' chat!")
        # Tournament is not assigned tournament role
        else:
            await ctx.send(f"{member_name.mention} is already not in the 'tournament' chat")
                
    # Add to Purple or Gold Team
    # !add_purple_gold desired-team
    @commands.command()
    async def add_purple_gold(self, ctx, team):
        # Get username for player adding team role
        member_name = ctx.author
        
        # Get roles from server
        purple_team = discord.utils.get(ctx.guild.roles, name='Team Purple')
        gold_team = discord.utils.get(ctx.guild.roles, name='Team Gold')
        
        # Normalize position
        normalized_team = team.lower()
        
        # Role assignment
        # Team Purple
        if 'purple' in normalized_team:
            # Player not assigned to purple
            if purple_team not in member_name.roles:
                # Check to see if they are a part of gold 
                if gold_team in member_name.roles:
                    await ctx.send(f"{member_name.mention}, please leave gold team before you can join purple")
                # Add purple role
                else:
                    await member_name.add_roles(purple_team)
                    await ctx.send(f"{member_name.mention} has joined the purple team")
        
        # Team gold
        if 'gold' in normalized_team:
            # Player not assigned to gold
            if gold_team not in member_name.roles:
                # Check to see if they are a part of purple
                if purple_team in member_name.roles:
                    await ctx.send(f"{member_name.mention}, please leave purple team before you can join gold") 
                # Add gold role
                else:
                    await member_name.add_roles(gold_team)
                    await ctx.send(f"{member_name.mention} has joined the gold team")
                
        # Team is invalid
        if not('purple' in normalized_team or 'gold' in normalized_team):
            await ctx.send("Error: Please specify 'purple' or 'gold'")
            
    # Remove from Purple or Gold Team
    # !remove_purple_gold desired-team
    @commands.command()
    async def remove_purple_gold(self, ctx, team):
        # Get username for player removing team role
        member_name = ctx.author
        
        # Get roles from server
        purple_team = discord.utils.get(ctx.guild.roles, name='Team Purple')
        gold_team = discord.utils.get(ctx.guild.roles, name='Team Gold')
        
        # Normalize position
        normalized_team = team.lower()
        
        # Role removal
        # Team purple
        if 'purple' in normalized_team: 
            # Remove player from purple
            if purple_team in member_name.roles:
                await member_name.remove_roles(purple_team)
                await ctx.send(f"{member_name.mention} has left the purple team")
            # Player is not on purple
            else:
                await ctx.send(f"{member_name.mention} does not have 'purple' permissions")

        # Team gold
        if 'gold' in normalized_team:
            # Remove player from gold
            if gold_team in member_name.roles:
                await member_name.remove_roles(gold_team)
                await ctx.send(f"{member_name.mention} has left the gold team")
            # Player is not on gold
            else:
                await ctx.send(f"{member_name.mention} does not have 'gold' permissions")
                
        # Team is invalid 
        if not('purple' in normalized_team or 'gold' in normalized_team):
            await ctx.send("Error: Please specify 'purple' or 'gold'")
                
        
# Set up Channel Bot
async def setup(bot):
    await bot.add_cog(ChannelCommands(bot))