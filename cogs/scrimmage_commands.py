"""
Name: Logan McDavid
Filename: scrimmage_commands.py    
Purpose: Contains commands associated with
scrimamge scheduling
"""
import discord
import asyncio
import random
import json
from discord.ext import commands

# Scrimmage Commands Class
class ScrimmageCommands(commands.Cog):
    # Constructor
    def __init__(self, bot):
        self.bot = bot
        
    # Players Rsvp for Purple vs. Gold Scrimamge
    # !rsvp_scrimmage position-name
    # position_name = 'handler', 'cutter', or 'hybrid'
    @commands.command()
    async def rsvp_scrimmage(self, ctx, *, position: str=None): 
        # Get username for player RSVPing
        member_name = ctx.author.name
        normalized_position = position.lower() if position else None # Normalize name
        
        # Player did not specify position to sign up for
        if normalized_position is None:
            await ctx.send("Please specify 'handler', 'cutter', or 'hybrid'.")
            return
            
        # Player entered invalid position
        if normalized_position not in ['handler', 'cutter', 'hybrid']:
            await ctx.send("Invalid position. Please specify 'handler', 'cutter', or 'hybrid'.")
            return
        
        # Read the JSON file
        with open('scrimmage.json', 'r') as f:
            data = json.load(f)
            
        # Initialize the position lists in the JSON file if not already present
        if 'cutters' not in data:
            data['cutters'] = []
        if 'handlers' not in data:
            data['handlers'] = []
        if 'hybrids' not in data:
            data['hybrids'] = []
            
        # Player already signed up for specified position
        if member_name in data[normalized_position + 's']:
            await ctx.send(f"{member_name}, you are already signed up as a '{normalized_position}'.")
            return
        
        # Remove user from any other position list
        for pos in ['cutters', 'handlers', 'hybrids']:
            if member_name in data[pos]:
                data[pos].remove(member_name)

        # Append user to the new desired position list
        data[normalized_position + 's'].append(member_name)
        
        # Write the updated data back to the JSON file
        with open('scrimmage.json', 'w') as f:
            json.dump(data, f, indent=4)
            
        await ctx.send(f"{ctx.author.mention} has signed up as a '{normalized_position}' for Purple vs. Gold")
        
    # Players unRSVP from Purple vs. Gold Scrimmage
    # unrsvp_scrimmage
    @commands.command()
    async def unrsvp_scrimmage(self, ctx):
        # Get username for player unRSVPing
        member_name = ctx.author.name
        
        # Read the JSON file
        with open('scrimmage.json', 'r') as f:
            data = json.load(f)
            
        # Initialize the position lists in the JSON file if not already present
        if 'cutters' not in data:
            data['cutters'] = []
        if 'handlers' not in data:
            data['handlers'] = []
        if 'hybrids' not in data:
            data['hybrids'] = []
        
        # Remove player from scrimmage
        # Member is cutter
        if member_name in data['cutters']:
            data['cutters'].remove(member_name)
            response = f"{ctx.author.mention} has been removed from the RSVP list."
        # Member is handler
        elif member_name in data['handlers']:
            data['handlers'].remove(member_name)
            response = f"{ctx.author.mention} has been removed from the RSVP list."
        # Member is hybrid
        elif member_name in data['hybrids']:
            data['hybrids'].remove(member_name)
            response = f"{ctx.author.mention} has been removed from the RSVP list."
        # Not a member of any list
        else:
            response = f"{ctx.author.mention} is not a part of the RSVP list"
            
        # Write the updated data back to the JSON file
        with open('scrimmage.json', 'w') as f:
            json.dump(data, f, indent=4)
            
        await ctx.send(response)
        
    # Modify rsvp status for Purple vs. Gold Scrimmage
    # !modify_scrimmage_rsvp_list rsvp username 
    # !modify_scrimmage_rsvp_list unrsvp username
    @commands.command()
    @commands.has_role('Captain') # Captain permissions 
    async def modify_scrimmage_rsvp_list(self, ctx, action: str, username: str):
        # Check to see if user exists
        member = ctx.guild.get_member_named(username)
        if member is None:
            await ctx.send(f"{username} is not a member of the server.")
            return
        
        # Read the JSON file
        with open('scrimmage.json', 'r') as f:
            data = json.load(f)
            
        # Initialize the position lists in the JSON file if not already present
        if 'cutters' not in data:
            data['cutters'] = []
        if 'handlers' not in data:
            data['handlers'] = []
        if 'hybrids' not in data:
            data['hybrids'] = []
            
        # Load in position lists
        handlers = data.get('handlers', [])
        cutters = data.get('cutters', [])
        hybrids = data.get('hybrids', [])
        
        # RSVP player
        if action.lower() == 'rsvp':
            # Player already RSVP'd
            if username in handlers or username in cutters or username in hybrids:
                await ctx.send(f"{username} is already RSVP'd.")
    
            # RSVP player now
            else: 
                # Ask for position name
                await ctx.send(f"Please specify whether {username} is a 'handler', 'cutter', or 'hybrid' by simply typing one of the following within the next 45 seconds.")
                
                # Wait 30 seconds for response 
                try:
                    # https://stackoverflow.com/questions/66393331/how-can-i-use-the-wait-for-in-my-clearall-command-discord-py
                    response = await self.bot.wait_for('message', # Wait for message event
                                                       timeout = 45.0, # 45 second buffer
                                                       check=lambda m: # Take one argument
                                                           m.author == ctx.author # Same user from original command call
                                                           and m.content.lower() in ['handler', 'cutter', 'hybrid'])
                
                    # Await for handler, cutter, or hybrid 
                    if response.content.lower() == 'handler':
                        handlers.append(username)
                        await ctx.send(f"{username} has been added to the handler list.")
                    elif response.content.lower() == 'cutter':
                        cutters.append(username)
                        await ctx.send(f"{username} has been added to the cutter list.")
                    elif response.content.lower() == 'hybrid':
                        hybrids.append(username)
                        await ctx.send(f"{username} has been added to the hybrid list.")

                # Time runs out
                except asyncio.TimeoutError:
                    await ctx.send("You took too long to respond. The RSVP was not completed.")
                    return
            
        # UnRSVP player
        elif action.lower() == 'unrsvp':
            # Check if user is in handler, cutter, or hybrid list, if so remove them
            if username in handlers:
                handlers.remove(username)
                await ctx.send(f"{username} has been removed from the scrimmage.")
            elif username in cutters:
                cutters.remove(username)
                await ctx.send(f"{username} has been removed from the scrimmage.")
            elif username in hybrids:
                hybrids.remove(username)
                await ctx.send(f"{username} has been removed from the scrimmage.")
            # Not in RSVP list
            else:
                await ctx.send(f"{username} is not in the scrimmage RSVP list.")
    
        # Write the updated data back to the JSON file
        with open('scrimmage.json', 'w') as f:
            json.dump(data, f, indent=4)
    


    # View RSVPs for Purple vs. Gold Scrimmage
    # !view_scrimmage_rsvp_list
    @commands.command()
    @commands.has_role('Captain') # Captain permissions
    async def view_scrimmage_rsvp_list(self, ctx):
        # Read the JSON file
        with open('scrimmage.json', 'r') as f:
            data = json.load(f)
        
        # Total RSVPs
        total = len(data['cutters']) + len(data['handlers']) + len(data['hybrids'])
        
        # If there is an RSVP
        if total != 0:
        
            # Embed list of players who RSVP'd
            embed = discord.Embed(
                title="Purple vs. Gold RSVP Summary",
                color=0x816CB4
            )
            
            # Handlers
            embed.add_field(
                name="Handlers", 
                value="\n".join(data['handlers']) or "N/A",
                inline=False
            )
            # Cutters
            embed.add_field(
                name="Cutters", 
                value="\n".join(data['cutters']) or "N/A",
                inline=False
            )
            # Hybrids
            embed.add_field(
                name="Hybrids", 
                value="\n".join(data['hybrids']) or "N/A",
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
        # Read the JSON file
        with open('scrimmage.json', 'r') as f:
            data = json.load(f)
        
        # Store in temp list in order to not manipulate original list
        temp_cutters = data.get('cutters', [])
        temp_handlers = data.get('handlers', [])
        temp_hybrids = data.get('hybrids', [])
        
        # Check if any player exists
        if not temp_cutters and not temp_handlers and not temp_hybrids:
            await ctx.send("No players available to sort into teams.")
            return
        
        """
        # Find number of each position
        num_cutters = len(temp_cutters)
        num_handlers = len(temp_handlers)
        num_hybrids = len(temp_hybrids)
        """
        
        # Randomize lists
        random.shuffle(temp_cutters)
        random.shuffle(temp_handlers)
        random.shuffle(temp_hybrids)
        
        """
        Function: split_even
        Purpose: Split the number of players 
        in a list in half 
        """
        def split_even(player_list):
            # Odd number of players
            if len(player_list) % 2 != 0:
                odd_player = player_list[-1]  # Take the last player as the odd player
                player_list = player_list[:-1]  # Remove the odd player from the list
                return player_list[:len(player_list) // 2], player_list[len(player_list) // 2:], odd_player
            else:
                return player_list[:len(player_list) // 2], player_list[len(player_list) // 2:], None
                
        # Initialize teams
        gold_team = []
        purple_team = []
        
        # Split handlers
        purple_handlers, gold_handlers, odd_handler = split_even(temp_handlers)
        purple_team.extend(purple_handlers)
        gold_team.extend(gold_handlers)
        
        # Split hybrids
        purple_hybrids, gold_hybrids, odd_hybrids = split_even(temp_hybrids)
        purple_team.extend(purple_hybrids)
        gold_team.extend(gold_hybrids)
        
        # Split cutters
        purple_cutters, gold_cutters, odd_cutters = split_even(temp_cutters)
        purple_team.extend(purple_cutters)
        gold_team.extend(gold_cutters)
        
        # Handle odd players
        for odd_player in [odd_handler, odd_hybrids, odd_cutters]:
            if odd_player:
                if len(purple_team) <= len(gold_team):
                    purple_team.append(odd_player)
                else:
                    gold_team.append(odd_player)
        
        # Embed list of purple and gold teams
        embed = discord.Embed(
            title="Purple vs. Gold Teams",
            description="Randomly generated teams based on position:",
            color=0x816CB4
        )
        # Purple team
        embed.add_field(
            name="Purple Team", 
            value="\n".join(purple_team) or "N/A",
            inline=False
        )
        # Gold team
        embed.add_field(
            name="Gold Team",
            value="\n".join(gold_team) or "N/A",
            inline=False
        )
        
        # Output list to channel
        await ctx.send(embed=embed)
            
        # JSON instances of purple and gold team
        data['purple_team'] = purple_team
        data['gold_team'] = gold_team
        
        # Write the updated data back to the JSON file
        with open('scrimmage.json', 'w') as f:
            json.dump(data, f, indent=4)
    
    @commands.command()
    @commands.has_role('Captain')  # Captain permissions
    async def approve_teams(self, ctx):
        # Read the JSON file
        with open('scrimmage.json', 'r') as f:
            data = json.load(f)
        
        # Not enough players to schedule event
        if not data.get('purple_team') or not data.get('gold_team'):
            await ctx.send("Not enough players to schedule this event")
            return
        
        # Roles
        purple_team_role = discord.utils.get(ctx.guild.roles, name='Team Purple')
        gold_team_role = discord.utils.get(ctx.guild.roles, name='Team Gold')
        
        # Check if the roles exist
        if not purple_team_role or not gold_team_role:
            await ctx.send("One or both team roles do not exist. Please create them first.")
            return

        # Assign purple team roles
        for player_name in data['purple_team']:
            player = discord.utils.get(ctx.guild.members, name=player_name)
            if player:  # If player is found
                await player.add_roles(purple_team_role)
        
        # Assign gold team roles
        for player_name in data['gold_team']:
            player = discord.utils.get(ctx.guild.members, name=player_name)
            if player:  # If player is found
                await player.add_roles(gold_team_role)
        
        await ctx.send("Players have been assigned to their respective teams.")

      
    @commands.command()
    @commands.has_role('Captain')
    async def reset_teams(self, ctx):
        # Read the JSON file
        with open('scrimmage.json', 'r') as f:
            data = json.load(f)
        
        # Clear all rsvp lists in memory
        data['cutters'] = []
        data['handlers'] = []
        data['hybrids'] = []
        
        # Get roles from server
        purple_team_role = discord.utils.get(ctx.guild.roles, name='Team Purple')
        gold_team_role = discord.utils.get(ctx.guild.roles, name='Team Gold')
        
        # Check if the roles exist
        if not purple_team_role or not gold_team_role:
            await ctx.send("One or both of the team roles do not exist.")
            return
        
        # Nobody has purple or gold role
        if not purple_team_role.members and not gold_team_role.members:
            await ctx.send("One or both of the roles are already empty")
        else:
            # Remove players on purple team
            for player in purple_team_role.members:
                await player.remove_roles(purple_team_role)
            
            # Remove players on gold team
            for player in gold_team_role.members:
                await player.remove_roles(gold_team_role)
        
        # Empty teams
        data['purple_team'] = []
        data['gold_team'] = []
        
        # Write the updated data back to the JSON file
        with open('scrimmage.json', 'w') as f:
            json.dump(data, f, indent=4)
        
        await ctx.send("Players have been removed from purple and gold successfully")

            
        
# Set up Tournament bot
async def setup(bot):
    await bot.add_cog(ScrimmageCommands(bot))
