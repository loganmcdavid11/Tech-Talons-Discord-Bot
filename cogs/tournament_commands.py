"""
Name: Logan McDavid
Filename: tournament_commands.py    
Purpose: Contains commands associated with
tournament scheduling and RSVPing for a 
specific tournament
"""
import discord
import json
import os
import keys_ids.channel_ids as channel_ids
from discord.ext import commands
from classes.tournament import Tournament

# List of tournaments
tournament_list = []

# Tournament Commands Class
class TournamentCommands(commands.Cog):
    # Constructor
    def __init__(self, bot):
        self.bot = bot
        
    # Tournament bot turning on
    @commands.Cog.listener()
    async def on_ready(self):
        print("Tournament Bot is Online!")
        

    # Add a tournament
    # !add_tournament "tournament_name" "start_date" etc
    @commands.command()
    @commands.has_role('Captain')
    async def add_tournament(self, ctx, name: str, start_date: str, end_date: str, location: str, aof_time: str, field_address: str, lodging_address: str):
        # Read the JSON file
        with open('tournaments.json', 'r') as f:
                data = json.load(f)

        # Check if the tournament already exists
        if name.lower() in data:
            await ctx.send(f"Tournament '{name}' already exists.")
            return

        # Create the tournament entry
        data[name.lower()] = {
            "name": name,
            "start_date": start_date,
            "end_date": end_date,
            "location": location,
            "aof_time": aof_time,
            "field_address": field_address,
            "lodging_address": lodging_address,
            "rsvp_list": []
        }

        # Write the updated data back to the JSON file
        with open('tournaments.json', 'w') as f:
            json.dump(data, f, indent=4)

        await ctx.send(f"Tournament '{name}' added successfully!")
            
    
        
    # Delete a Tournament
    # !delete_tournament name_of_tournament
    @commands.command()
    @commands.has_role('Captain') # Captain permissions
    async def delete_tournament(self, ctx, *, name: str):
        temp_name = name.strip().lower()
        
        # Read the JSON file
        with open('tournaments.json', 'r') as f:
                data = json.load(f)
                
        # NOTE: Should I make a feature for if there are no tournaments at all?
                
        # Tournament not found
        if temp_name not in data:
            await ctx.send(f"Tournament '{name}' not found.") 
            return

        # Delete the tournament
        del data[temp_name]
        
        # Write the updated data back to the JSON file
        with open('tournaments.json', 'w') as f:
            json.dump(data, f, indent=4)
            
        await ctx.send(f"Tournament '{name}' successfully deleted.")
            
            
    # Edit a Tournament
    # !edit_tournament "tournament_name" "start_date" etc
    @commands.command()
    @commands.has_role('Captain') # Captain permissions
    async def edit_tournament(self, ctx, name: str, start_date: str, end_date: str, location: str, aof_time: str, field_address: str, lodging_address: str):
        temp_name = name.strip().lower()
        
        # Read the JSON file
        with open('tournaments.json', 'r') as f:
                data = json.load(f)
                
        # Tournament not found
        if temp_name not in data:
            await ctx.send(f"Tournament '{name}' not found.") 
            return
        
        # Update tournament details
        data[temp_name].update({
            "start_date": start_date,
            "end_date": end_date,
            "location": location,
            "aof_time": aof_time,
            "field_address": field_address,
            "lodging_address": lodging_address
        })
        
        # Write the updated data back to the JSON file
        with open('tournaments.json', 'w') as f:
            json.dump(data, f, indent=4)

        await ctx.send(f"Tournament '{name}' updated successfully!")
            
    
    # View Tournaments
    # !tournaments
    @commands.command()
    async def tournaments(self, ctx):
        # Read the JSON file
        with open('tournaments.json', 'r') as f:
                data = json.load(f)
                
        # No tournaments scheduled
        if not data:
            await ctx.send("No tournaments currently scheduled")
            return
            
        # Display all tournaments
        else:
            # Title message
            embed = discord.Embed(
                title="Upcoming Tournaments", 
                color=0xffd700
            )
        
            # Loop through each tournament
            for tournament in data.values():
                embed.add_field(
                    name=tournament['name'],
                    value=(
                        f"**Start Date:** {tournament['start_date']}\n"
                        f"**End Date:** {tournament['end_date']}\n"
                        f"**Location:** {tournament['location']}\n"
                        f"**AOF Time:** {tournament['aof_time']}\n"
                        f"**Field Address:** {tournament['field_address']}\n"
                        f"**Lodging Address:** {tournament['lodging_address']}\n"
                        "\u200B" # Add separation
                    ),
                    inline=False
                )
            
            # Output list to channel
            await ctx.send(embed=embed)
            
            
    # RSVP for Tournament
    # !rsvp_tournament tournament name
    @commands.command()
    async def rsvp_tournament(self, ctx, *, name: str):
        channel = self.bot.get_channel(channel_ids.CAPTAIN_CHANNEL_ID)  # Captains channel
        temp_name = name.strip().lower()  # Trim leading and trailing spaces
        member_name = ctx.author.display_name  # Get username for user RSVPing
    
        # Read the JSON file
        with open('tournaments.json', 'r') as f:
                data = json.load(f)
        
        # Tournament not found
        if temp_name not in data:
            await ctx.send(f"Tournament '{name}' not found.")
            return
        
        # Ensure rsvp_list exists
        if "rsvp_list" not in data[temp_name]:
            data[temp_name]["rsvp_list"] = []

        # User already RSVP'd
        if member_name in data[temp_name]["rsvp_list"]:
            await ctx.send(f"{member_name} has already RSVP'd for '{name}'.")
            return
            
        # RSVP user
        data[temp_name]["rsvp_list"].append(member_name)
        
        # Write the updated data back to the JSON file
        with open('tournaments.json', 'w') as f:
            json.dump(data, f, indent=4)
        
        # Send to captains chat and user's chat
        await channel.send(f"{member_name} has RSVP'd for '{data[temp_name]['name']}'.")
        await ctx.send(f"{member_name} has RSVP'd for '{data[temp_name]['name']}'.")


    
    # Un-RSVP from tournament
    # !unrsvp_tournament tournament name
    @commands.command()
    async def unrsvp_tournament(self, ctx, *, name: str):
        channel = self.bot.get_channel(channel_ids.CAPTAIN_CHANNEL_ID)  # Captains channel
        temp_name = name.strip().lower()  # Normalize to lowercase to match the keys
        member_name = ctx.author.display_name  # Get username for user RSVPing
        
        # Read the JSON file
        with open('tournaments.json', 'r') as f:
            data = json.load(f)
        
        # Tournament not found
        if temp_name not in data:
            await ctx.send(f"Tournament '{name}' not found.")
            return

        # Ensure rsvp_list exists
        if "rsvp_list" not in data[temp_name]:
            data[temp_name]["rsvp_list"] = []

        # User not RSVP'd
        if member_name not in data[temp_name]["rsvp_list"]:
            await ctx.send(f"{member_name} has not RSVP'd for '{name}'.")
            return
        
        # Remove user from RSVP list
        data[temp_name]["rsvp_list"].remove(member_name)
        
        # Write the updated data back to the JSON file
        with open('tournaments.json', 'w') as f:
            json.dump(data, f, indent=4)
        
        # Ensure captains channel exists
        if channel is None:
            await ctx.send("Captains channel not found.")
            return
        
        # Send to captains chat and user's chat
        await channel.send(f"{member_name} is no longer RSVP'd for '{data[temp_name]['name']}'.")
        await ctx.send(f"{member_name} is no longer RSVP'd for '{data[temp_name]['name']}'.")


    # View list of RSVP's for a tournament
    # view_tournament_rsvp_list tournament_name
    @commands.command()
    @commands.has_role('Captain') # Captain permissions
    async def view_tournament_rsvp_list(self, ctx, *, name: str):
        temp_name = name.strip().lower()  # Trim leading and trailing spaces
    
        # Read the JSON file
        with open('tournaments.json', 'r') as f:
                data = json.load(f)
        
        # Tournament exists or not
        if temp_name not in data:
            await ctx.send(f"Tournament '{name}' not found.") 
            return
        
        # Ensure rsvp_list exists
        if "rsvp_list" not in data[temp_name]:
            data[temp_name]["rsvp_list"] = []
        
        # Save rsvp_list
        rsvp_list = data[temp_name]["rsvp_list"]
        
        # Check for any RSVP's in tournament
        if not rsvp_list:
            await ctx.send(f"No RSVPs for '{data[temp_name]['name']}' yet.")
            return
        
        # Create an embed to display the RSVP list
        embed = discord.Embed(
            title=f"RSVP List for {data[temp_name]['name']}",
            color=0xffd700
        )
        embed.add_field(
            name="**Players**",
            value='\n'.join([f"• {player}" for player in rsvp_list]),
            inline=False
        )
        embed.add_field(
            name="**Total RSVPs**",
            value=str(len(rsvp_list)),
            inline=False
        )
        
        await ctx.send(embed=embed)
       
    # View Tournament Packing List
    # !tournament_packing_list
    @commands.command()
    async def tournament_packing_list(self, ctx):
        # Embed list
        embed = discord.Embed(title="Tournament Packing List", color=0xffd700)
        # Clothing items
        embed.add_field(
            name="Clothing",
            value=(
                "• 1 Light and Dark Shirt per day\n"
                "• 3 pairs of socks per day\n"
                "• Extra layers (if cold/windy/rainy)\n"
            ),
            inline=False
        )
        # Gear
        embed.add_field(
            name="Gear",
            value=(
                "• Cleats\n"
                "• Frisbee\n"
                "• Gloves\n"
                "• Hat\n"
                "• Any braces for injuries\n"
            ),
            inline=False
        )
        # Hydration and energy
        embed.add_field(
            name="Hydration / Energy",
            value=(
                "• Snacks\n"
                "  • Sugars for quick energy\n"
                "  • Carbs before and for throughout the day\n"
                "• Electrolytes\n"
                "• Water Bottle\n"
            ),
            inline=False
        )
        # Miscellaneous
        embed.add_field(
            name="Miscellaneous",
            value=(
                "• Sunscreen\n"
                "• Nail clippers\n"
                "• Wallet\n"
                "• Toiletries\n"
                "• Deodorant for frisbee bag\n"
                "• Advil\n"
                ),
            inline=False
        )
    
        # Output list to channels
        await ctx.send(embed=embed)

        
# Set up Tournament bot
async def setup(bot):
    await bot.add_cog(TournamentCommands(bot))
    