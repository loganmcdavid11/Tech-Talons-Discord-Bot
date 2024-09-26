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


class ScrimmageCommands(commands.Cog):
    # Constructor
    def __init__(self, bot):
        self.bot = bot
        # Get the instance of your Scrimmage class
        self.scrimmage_instance = Scrimmage()
        
    # Players signup for scrimamge
    @commands.command()
    async def rsvp_scrimmage(self, ctx, position):
        member_name = ctx.author
        normalized_position = position.lower()

        # Check if they are already signed up for the same position
        if normalized_position == 'cutter' and member_name in self.scrimmage_instance.cutters:
            await ctx.send(f"{member_name.mention}, you are already signed up as a 'cutter'.")
            return
        elif normalized_position == 'handler' and member_name in self.scrimmage_instance.handlers:
            await ctx.send(f"{member_name.mention}, you are already signed up as a 'handler'.")
            return
        elif normalized_position == 'hybrid' and member_name in self.scrimmage_instance.hybrids:
            await ctx.send(f"{member_name.mention}, you are already signed up as a 'hybrid'.")
            return

        # Remove from existing position if necessary and notify the player
        if member_name in self.scrimmage_instance.cutters:
            self.scrimmage_instance.cutters.remove(member_name)
            await ctx.send(f"{member_name.mention} has been removed from the 'cutter' list.")
        elif member_name in self.scrimmage_instance.handlers:
            self.scrimmage_instance.handlers.remove(member_name)
            await ctx.send(f"{member_name.mention} has been removed from the 'handler' list.")
        elif member_name in self.scrimmage_instance.hybrids:
            self.scrimmage_instance.hybrids.remove(member_name)
            await ctx.send(f"{member_name.mention} has been removed from the 'hybrid' list.")

        # Validate the new position
        if normalized_position not in ['cutter', 'handler', 'hybrid']:
            await ctx.send("Error: Please specify 'cutter', 'handler', or 'hybrid'")
            return

        # Append the player to the new desired position list
        if normalized_position == 'cutter':
            self.scrimmage_instance.cutters.append(member_name)
        elif normalized_position == 'handler':
            self.scrimmage_instance.handlers.append(member_name)
        else:  # hybrid
            self.scrimmage_instance.hybrids.append(member_name)

        await ctx.send(f"{member_name.mention} has signed up as a '{normalized_position}' for gold vs. purple")
        
    # Players unrsvp from scrimmage
    @commands.command()
    async def unrsvp_scrimmage(self, ctx):
        member_name = ctx.author
        
        if member_name in self.scrimmage_instance.cutters:
            self.scrimmage_instance.cutters.remove(member_name)
            await ctx.send(f"{member_name.mention} has been removed from the 'cutter' list.")
        elif member_name in self.scrimmage_instance.handlers:
            self.scrimmage_instance.handlers.remove(member_name)
            await ctx.send(f"{member_name.mention} has been removed from the 'handler' list.")
        elif member_name in self.scrimmage_instance.hybrids:
            self.scrimmage_instance.hybrids.remove(member_name)
            await ctx.send(f"{member_name.mention} has been removed from the 'hybrid' list.")

    @commands.command()
    @commands.has_role('Captain')
    async def view_scrimmage_rsvp_list(self, ctx):
        cutters = self.scrimmage_instance.cutters
        handlers = self.scrimmage_instance.handlers
        hybrids = self.scrimmage_instance.hybrids
        
        total = len(cutters) + len(handlers) + len(hybrids)
        
        embed = discord.Embed(title="Purple vs. Gold RSVP Summary", color=0x816CB4)
        embed.add_field(
            name="Handlers", 
            value="\n".join([player.name for player in handlers]) or "N/A",
            inline=False
        )
        embed.add_field(
            name="Cutters", 
            value="\n".join([player.name for player in cutters]) or "N/A",
            inline=False
        )
        embed.add_field(
            name="Hybrids", 
            value="\n".join([player.name for player in hybrids]) or "N/A",
            inline=False
        )
        embed.add_field(
            name="Total RSVPs",
            value=str(total),
            inline=False
        )
        
        await ctx.send(embed=embed)
        
    # NOTE: I want to make it where i check for odd or even numbers in order to make sure there is not an imbalance of players on each team
    @commands.command()
    @commands.has_role('Captain')
    async def sort_teams(self, ctx):
        # Debugging outputs
        print(f"Handlers: {self.scrimmage_instance.handlers}")
        print(f"Cutters: {self.scrimmage_instance.cutters}")
        print(f"Hybrids: {self.scrimmage_instance.hybrids}")

        # Find number of each position
        num_cutters = len(self.scrimmage_instance.cutters)
        num_handlers = len(self.scrimmage_instance.handlers)
        num_hybrids = len(self.scrimmage_instance.hybrids)
        
        # Check if any player exists
        if num_cutters == 0 and num_handlers == 0 and num_hybrids == 0:
            await ctx.send("No players available to sort into teams.")
            return
        
        def split_even(player_list):
            half = len(player_list) // 2
            return player_list[:half], player_list[half:]
        
        # Randomize lists
        random.shuffle(self.scrimmage_instance.cutters)
        random.shuffle(self.scrimmage_instance.handlers)
        random.shuffle(self.scrimmage_instance.hybrids)
        
        # Clear list from before
        self.scrimmage_instance.purple_team.clear()
        self.scrimmage_instance.gold_team.clear()
        
        # Handlers
        purple_handlers, gold_handlers = split_even(self.scrimmage_instance.handlers)
        self.scrimmage_instance.purple_team.extend(purple_handlers)
        self.scrimmage_instance.gold_team.extend(gold_handlers)
        
        # Hybrids
        purple_hybrids, gold_hybrids = split_even(self.scrimmage_instance.hybrids)
        self.scrimmage_instance.purple_team.extend(purple_hybrids)
        self.scrimmage_instance.gold_team.extend(gold_hybrids)
        
        # Cutters
        purple_cutters, gold_cutters = split_even(self.scrimmage_instance.cutters)
        self.scrimmage_instance.purple_team.extend(purple_cutters)
        self.scrimmage_instance.gold_team.extend(gold_cutters)
        
        # Output Gold and Purple Teams
        embed = discord.Embed(title="Purple vs. Gold Teams", description="Randomly generated teams based on position:", color=0x816CB4)
        embed.add_field(
            name="Purple Team", 
            value="\n".join(player.name for player in self.scrimmage_instance.purple_team) or "N/A",
            inline=False
        )
        embed.add_field(
            name="Gold Team",
            value="\n".join(player.name for player in self.scrimmage_instance.gold_team) or "N/A",
            inline=False
        )
        
        await ctx.send(embed=embed)
        
    @commands.command()
    @commands.has_role('Captain')
    async def approve_teams(self, ctx):
        if not self.scrimmage_instance.purple_team and not self.scrimmage_instance.gold_team:
            await ctx.send("Not enough players to schedule this event")
            return
        
        purple_team_role = discord.utils.get(ctx.guild.roles, name='Team Purple')
        gold_team_role = discord.utils.get(ctx.guild.roles, name='Team Gold')
        
        for player in self.scrimmage_instance.purple_team:
            await player.add_roles(purple_team_role)
            
        for player in self.scrimmage_instance.gold_team:
            await player.add_roles(gold_team_role)
            
        await ctx.send("Players have been assigned purple or gold successfully")
        
    # NOTE: I want to make a function where we clear all purple and gold roles, resetting the process in case we want to do to again

        
        
# Set up Tournament bot
async def setup(bot):
    await bot.add_cog(ScrimmageCommands(bot))
