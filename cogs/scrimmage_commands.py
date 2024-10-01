"""
Name: Logan McDavid
Filename: scrimmage_commands.py    
Purpose: Contains commands associated with
scrimamge scheduling
"""
import discord
import random
from discord.ext import commands
from scrimmage import Scrimmage

# Scrimmage Commands Class
class ScrimmageCommands(commands.Cog):
    # Constructor
    def __init__(self, bot):
        self.bot = bot
        self.scrimmage_instance = Scrimmage() # Instance of scrimmage class 
        
    # Players Rsvp for Purple vs. Gold Scrimamge
    # !rsvp_scrimmage position-name
    # position_name = 'handler', 'cutter', or 'hybrid'
    @commands.command()
    async def rsvp_scrimmage(self, ctx, position):
        # Get username for player RSVPing
        member_name = ctx.author
        normalized_position = position.lower() # Normalize name

        # Player already signed up for specified position
        # Cutter
        if normalized_position == 'cutter' and member_name in self.scrimmage_instance.cutters:
            await ctx.send(f"{member_name.mention}, you are already signed up as a 'cutter'.")
            return
        # Handler
        elif normalized_position == 'handler' and member_name in self.scrimmage_instance.handlers:
            await ctx.send(f"{member_name.mention}, you are already signed up as a 'handler'.")
            return
        # Hybrid
        elif normalized_position == 'hybrid' and member_name in self.scrimmage_instance.hybrids:
            await ctx.send(f"{member_name.mention}, you are already signed up as a 'hybrid'.")
            return

        # Remove from existing position if signed up for other position previously
        # Cutter 
        if member_name in self.scrimmage_instance.cutters:
            self.scrimmage_instance.cutters.remove(member_name)
            # NOTE: I do not want these output lines in first launch
            await ctx.send(f"{member_name.mention} has been removed from the 'cutter' list.")
        # Handler
        elif member_name in self.scrimmage_instance.handlers:
            self.scrimmage_instance.handlers.remove(member_name)
            await ctx.send(f"{member_name.mention} has been removed from the 'handler' list.")
        # Hybrid
        elif member_name in self.scrimmage_instance.hybrids:
            self.scrimmage_instance.hybrids.remove(member_name)
            await ctx.send(f"{member_name.mention} has been removed from the 'hybrid' list.")

        # Validate player's position
        if normalized_position not in ['cutter', 'handler', 'hybrid']:
            await ctx.send("Error: Please specify 'cutter', 'handler', or 'hybrid'")
            return

        # Append user to the new desired position list
        # Cutter 
        if normalized_position == 'cutter':
            self.scrimmage_instance.cutters.append(member_name)
        # Handler
        elif normalized_position == 'handler':
            self.scrimmage_instance.handlers.append(member_name)
        # Hybrid
        else: 
            self.scrimmage_instance.hybrids.append(member_name)
            
        await ctx.send(f"{member_name.mention} has signed up as a '{normalized_position}' for gold vs. purple")
        
    # Players unRSVP from Purple vs. Gold Scrimmage
    # unrsvp_scrimmage
    @commands.command()
    async def unrsvp_scrimmage(self, ctx):
        # Get username for player unRSVPing
        member_name = ctx.author
        
        # Remove player from scrimmage
        # Member is cutter
        if member_name in self.scrimmage_instance.cutters:
            self.scrimmage_instance.cutters.remove(member_name)
            await ctx.send(f"{member_name.mention} has been removed from the 'cutter' list.")
        # Member is handler
        elif member_name in self.scrimmage_instance.handlers:
            self.scrimmage_instance.handlers.remove(member_name)
            await ctx.send(f"{member_name.mention} has been removed from the 'handler' list.")
        # Member is hybrid
        elif member_name in self.scrimmage_instance.hybrids:
            self.scrimmage_instance.hybrids.remove(member_name)
            await ctx.send(f"{member_name.mention} has been removed from the 'hybrid' list.")

    # View RSVPs for Purple vs. Gold Scrimmage
    # !view_scrimmage_rsvp_list
    @commands.command()
    @commands.has_role('Captain') # Captain permissions
    async def view_scrimmage_rsvp_list(self, ctx):
        # Get list of players for each position
        cutters = self.scrimmage_instance.cutters
        handlers = self.scrimmage_instance.handlers
        hybrids = self.scrimmage_instance.hybrids
        
        # Total RSVPs
        total = len(cutters) + len(handlers) + len(hybrids)
        
        # If there is an RSVP
        if total != 0:
        
            # Embed list of players who RSVP'd
            embed = discord.Embed(title="Purple vs. Gold RSVP Summary", color=0x816CB4)
            # Handlers
            embed.add_field(
                name="Handlers", 
                value="\n".join([player.name for player in handlers]) or "N/A",
                inline=False
            )
            # Cutters
            embed.add_field(
                name="Cutters", 
                value="\n".join([player.name for player in cutters]) or "N/A",
                inline=False
            )
            # Hybrids
            embed.add_field(
                name="Hybrids", 
                value="\n".join([player.name for player in hybrids]) or "N/A",
                inline=False
            )
            # Total count
            embed.add_field(
                name="Total RSVPs",
                value=str(total),
                inline=False
            )
            
            # Output list to channel
            await ctx.send(embed=embed)
        
        # No RSVP's yet
        else:
            await ctx.send("No RSVPs for Purple vs. Gold yet.")
        
    # Randomly Sort Purple vs. Gold Teams
    # !sort_teams
    # NOTE: I want to make it where I check for odd or even numbers in order to make sure there is not an imbalance of players on each team
    @commands.command()
    @commands.has_role('Captain') # Captain permissions
    async def sort_teams(self, ctx):
        # Find number of each position
        num_cutters = len(self.scrimmage_instance.cutters)
        num_handlers = len(self.scrimmage_instance.handlers)
        num_hybrids = len(self.scrimmage_instance.hybrids)
        
        # Check if any player exists
        if num_cutters == 0 and num_handlers == 0 and num_hybrids == 0:
            await ctx.send("No players available to sort into teams.")
            return
        
        """
        Function: split_even
        Purpose: Split the number of players 
        in a list in half 
        """
        def split_even(player_list):
            half = len(player_list) // 2
            return player_list[:half], player_list[half:]
        
        
        # Randomize lists
        random.shuffle(self.scrimmage_instance.cutters)
        random.shuffle(self.scrimmage_instance.handlers)
        random.shuffle(self.scrimmage_instance.hybrids)
        
        # Clear previous list
        self.scrimmage_instance.purple_team.clear()
        self.scrimmage_instance.gold_team.clear()
        
        # Split handlers
        purple_handlers, gold_handlers = split_even(self.scrimmage_instance.handlers)
        self.scrimmage_instance.purple_team.extend(purple_handlers)
        self.scrimmage_instance.gold_team.extend(gold_handlers)
        
        # Split hybrids
        purple_hybrids, gold_hybrids = split_even(self.scrimmage_instance.hybrids)
        self.scrimmage_instance.purple_team.extend(purple_hybrids)
        self.scrimmage_instance.gold_team.extend(gold_hybrids)
        
        # Split cutters
        purple_cutters, gold_cutters = split_even(self.scrimmage_instance.cutters)
        self.scrimmage_instance.purple_team.extend(purple_cutters)
        self.scrimmage_instance.gold_team.extend(gold_cutters)
        
        # Embed list of purple and gold teams
        embed = discord.Embed(
            title="Purple vs. Gold Teams",
            description="Randomly generated teams based on position:",
            color=0x816CB4
        )
        # Purple team
        embed.add_field(
            name="Purple Team", 
            value="\n".join(player.name for player in self.scrimmage_instance.purple_team) or "N/A",
            inline=False
        )
        # Gold team
        embed.add_field(
            name="Gold Team",
            value="\n".join(player.name for player in self.scrimmage_instance.gold_team) or "N/A",
            inline=False
        )
        
        # Output list to channel
        await ctx.send(embed=embed)
    
    # Approve Purple vs. Gold teams and Assign Players to Team
    # !approve_teams
    @commands.command()
    @commands.has_role('Captain') # Captain permissions
    async def approve_teams(self, ctx):
        # Not enough players to schedule event
        if not self.scrimmage_instance.purple_team and not self.scrimmage_instance.gold_team:
            await ctx.send("Not enough players to schedule this event")
            return
        
        # Roles
        purple_team_role = discord.utils.get(ctx.guild.roles, name='Team Purple')
        gold_team_role = discord.utils.get(ctx.guild.roles, name='Team Gold')
        
        # Assign purple team
        for player in self.scrimmage_instance.purple_team:
            await player.add_roles(purple_team_role)
            
        # Assign gold team
        for player in self.scrimmage_instance.gold_team:
            await player.add_roles(gold_team_role)
            
    
        await ctx.send("Players have been assigned purple or gold successfully")
      
    # Reset Purple and Gold Teams
    # !reset_teams
    @commands.command()
    @commands.has_role('Captain')
    async def reset_teams(self, ctx):
        # Get roles from server
        purple_team_role = discord.utils.get(ctx.guild.roles, name='Team Purple')
        gold_team_role = discord.utils.get(ctx.guild.roles, name='Team Gold')
        
        # Nobody has purple or gold role
        if not purple_team_role.members and not gold_team_role.members:
            await ctx.send("One or both of the roles are already empty")
            return
        
        # Remove players on purple team
        for player in purple_team_role.members:
            await player.remove_roles(purple_team_role)
            
        # Remove players on gold team
        for player in gold_team_role.members:
            await player.remove_roles(gold_team_role)
            
        # Empty lists
        self.scrimmage_instance.purple_team = []
        self.scrimmage_instance.gold_team = []
        self.scrimmage_instance.cutters = []
        self.scrimmage_instance.handlers = []
        self.scrimmage_instance.hybrids = []
        
        await ctx.send("Players have been removed from purple and gold successfully")
        
        
        
# Set up Tournament bot
async def setup(bot):
    await bot.add_cog(ScrimmageCommands(bot))
