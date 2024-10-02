"""
Name: Logan McDavid
Filename: tournament_commands.py    
Purpose: Contains commands associated with
tournament scheduling and RSVPing for a 
specific tournament
"""
import discord
import channel_ids
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
    @commands.has_role('Captain') # Captain permissions
    async def add_tournament(self, ctx, name: str, start_date: str, end_date: str, location: str, aof_time: str, field_address: str, lodging_address: str):
        # Check if tournament is already in list
        for tournament in tournament_list: 
            if tournament.name.strip().lower() == name.lower():
                await ctx.send(f"Tournament '{name}' already exists.") 
                return
    
        # Create Tournament object
        tournament = Tournament(name, start_date, end_date, location, aof_time, field_address, lodging_address)
        tournament_list.append(tournament) # Add the tournament to the list
        await ctx.send(f"Tournament '{name}' added successfully!") 
        
        
    # Delete a Tournament
    # !delete_tournament name_of_tournament
    @commands.command()
    @commands.has_role('Captain') # Captain permissions
    async def delete_tournament(self, ctx, *, name: str):
        name = name.strip()  # Trim leading and trailing spaces
        
        global tournament_list # Import tournament list to function
    
        # No tournaments in list
        if not tournament_list:
            await ctx.send("No tournaments to delete.") 
            return

        # Create new list without the tournament to be deleted
        new_tournament_list = []
        found = False
        # Iterate through all tournament names in list
        for tournament in tournament_list:
            # Normalize the names for comparison
            if tournament.name.strip().lower() == name.lower(): 
                found = True # Tournament found
            else:
                new_tournament_list.append(tournament) # Add to new list if tournament not found
    
        # Tournament found
        if found:
            tournament_list = new_tournament_list # Update tournament list
            await ctx.send(f"Tournament '{name}' successfully deleted.")
        # No tournament found
        else:
            await ctx.send(f"Tournament '{name}' not found.") 
            
            
    # Edit a Tournament
    # !edit_tournament "tournament_name" "start_date" etc
    @commands.command()
    @commands.has_role('Captain') # Captain permissions
    async def edit_tournament(self, ctx, name: str, start_date: str, end_date: str, location: str, aof_time: str, field_address: str, lodging_address: str):
        # Find the tournament
        for tournament in tournament_list:
            # Look for tournament name
            if tournament.name == name:
                # Update tournament details
                tournament.start_date = start_date
                tournament.end_date = end_date
                tournament.location = location
                tournament.aof_time = aof_time
                tournament.field_address = field_address
                tournament.lodging_address = lodging_address
                await ctx.send(f"Tournament '{name}' updated successfully!")
                return

        # Tournament was not found
        await ctx.send(f"Tournament '{name}' not found.")
            
    
    # View Tournaments
    # !tournaments
    @commands.command()
    async def tournaments(self, ctx):
        # No tournaments in list
        if not tournament_list:
            await ctx.send("No tournaments scheduled.")
            
        # Display all tournaments
        else:
            # Title message
            embed = discord.Embed(
                title="Upcoming Tournaments", 
                color=0xffd700
            )
        
            # Loop through each tournament
            for tournament in tournament_list:
                embed.add_field(
                    name=f"{tournament.name}",
                    value=(
                        f"**Start Date:** {tournament.start_date}\n"
                        f"**End Date:** {tournament.end_date}\n"
                        f"**Location:** {tournament.location}\n"
                        f"**AOF Time:** {tournament.aof_time}\n"
                        f"**Field Address:** {tournament.field_address}\n"
                        f"**Lodging Address:** {tournament.lodging_address}\n"
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
        channel = self.bot.get_channel(channel_ids.CAPTAIN_CHANNEL_ID) # Captains channel
    
        name = name.strip()  # Trim leading and trailing spaces
        
        global tournament_list # Import tournament list to function
        
        member_name = ctx.author.display_name # Get username for user RSVPing

        # No tournaments in list
        if not tournament_list:
            await ctx.send("No tournaments available to RSVP for.")
            return
    
        # Find desired tournament
        for tournament in tournament_list:
            # Normalize name for comparrison
            if tournament.name.strip().lower() == name.lower(): 
                # User already RSVP for tournament
                if member_name in tournament.rsvp_list:
                    await ctx.send(f"{member_name} has already RSVP'd for '{tournament.name}'.")
                    
                # RSVP the user to tournament
                else:
                    tournament.rsvp_list.append(member_name)
                    await channel.send(f"{member_name} has successfully RSVP'd for '{tournament.name}'.") # Send message to captains channel
                    await ctx.send(f"You successfully RSVP'd for '{tournament.name}'.") # Send message to users channel
                return
    
        # Tournament not found
        await ctx.send(f"Tournament '{name}' not found.")

    
    # Un-RSVP from tournament
    # !unrsvp_tournament tournament name
    @commands.command()
    async def unrsvp_tournament(self, ctx, *, name: str):
        channel = self.bot.get_channel(channel_ids.CAPTAIN_CHANNEL_ID) # Captains channel
    
        name = name.strip() # Trim leading and trailing spaces
        
        global tournament_list # Import tournament list to function
        
        member_name = ctx.author.display_name # Get username for user RSVPing
    
        # No tournament in list
        if not tournament_list: 
            await ctx.send("No tournaments available to un-RSVP from.")
            return
    
        # Find desired tournament
        for tournament in tournament_list:
            # Normalize the names for comparison
            if tournament.name.strip().lower() == name.lower():
                # Remove user from RSVP list
                if member_name in tournament.rsvp_list: 
                    tournament.rsvp_list.remove(member_name)
                    await channel.send(f"{member_name} has un-RSVP'd from '{tournament.name}'.") # Send message to captains channel
                    await ctx.send(f"You successfully un-RSVP'd from '{tournament.name}'.") # Send message to users channel
                    
                # Not in RSVP list
                else:
                    await ctx.send(f"You are not on the RSVP list for '{tournament.name}'.")
                return
        
        # Tournament not found
        await ctx.send("f{member_name}")

    # View list of RSVP's for a tournament
    # view_tournament_rsvp_list tournament_name
    @commands.command()
    @commands.has_role('Captain') # Captain permissions
    async def view_tournament_rsvp_list(self, ctx, *, name: str):
        name = name.strip()  # Trim leading and trailing spaces
    
        # Find desired tournament
        for tournament in tournament_list:
            # Normalize the names for comparison
            if tournament.name.strip().lower() == name.lower():
                # Tournament has RSVP's
                if tournament.rsvp_list:
                    # List of players who RSVP'd
                    rsvp_names = '\n'.join([f"• {player}" for player in tournament.rsvp_list])
                
                    # Embed list of players who rsvp'd
                    embed = discord.Embed(
                        title=f"RSVP List for {tournament.name}",
                        color=0xffd700
                    )
                    # List of players
                    embed.add_field(
                        name="**Players**",
                        value=rsvp_names,
                        inline=False
                        )
                    # Total count
                    embed.add_field(
                        name="**Total RSVPs**",
                        value=str(len(tournament.rsvp_list)),
                        inline=False)
                
                    # Output list to channel
                    await ctx.send(embed=embed)
                
                # No RSVP's
                else:
                    await ctx.send(f"No RSVPs for '{tournament.name}' yet.")
                return
        
        # Tournament not found
        await ctx.send(f"Tournament '{name}' not found.")
       
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
    