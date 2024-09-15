import discord
import requests
from discord.ext import commands
import apikeys
from tournament import Tournament

# Members intent
intents = discord.Intents.default()
intents.members = True

# Initializing instance of bot and the prefix command
client = commands.Bot(command_prefix = '!', intents = discord.Intents.all())


# Example of a simple in-memory tournament list (could be extended to a database)
tournament_list = []



"""
Here is everything I've messed with when learning
"""
# Bot turning on
@client.event
async def on_ready():
    print('The bot is now ready for use captain!')
    print('--------------------------------------')
    

# Basic example
# If one were to say !hello then this will run
@client.command()
async def hello(ctx):
    await ctx.send("Hello, I am the Tech Talons bot")
    
    
# !dog
# Pulls a random picture of a dog. Click web link to understand how I got what I needed
@client.command()
async def dog(ctx):
    response = requests.get("https://dog.ceo/api/breeds/image/random")
    res = response.json()
    em = discord.Embed()  # Makes the photo look nice and dandy
    em.set_image(url=res['message'])
    await ctx.send(embed=em)


# Example of an embedded command
@client.command()
async def cat(ctx):
    embed = discord.Embed(title="Title", url="https://www.google.com/search?q=Cute+kittens&sca_esv=719ed570ba997555&sca_upv=1&udm=2&biw=1703&bih=1306&sxsrf=ADLYWILLLDUJH0ZgxPD7SnZFGLLl_IzHTQ%3A1725337114674&ei=Go7WZqnxKMbGkPIP5dPdSQ&ved=0ahUKEwip5tnO9aWIAxVGI0QIHeVpNwkQ4dUDCBE&uact=5&oq=Cute+kittens&gs_lp=Egxnd3Mtd2l6LXNlcnAiDEN1dGUga2l0dGVuczIIEAAYgAQYsQMyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgARI4xlQgwtYrxdwAngAkAEAmAFooAGfCaoBAzkuM7gBA8gBAPgBAZgCDqACvwnCAg0QABiABBixAxhDGIoFwgILEAAYgAQYsQMYgwHCAgQQIxgnwgIKEAAYgAQYQxiKBZgDAIgGAZIHAzYuOKAHyz8&sclient=gws-wiz-serp", description="This one for all my cat lovers", color=0x4d8b6a)
    embed.set_author(name="Author", url="https://www.youtube.com/watch?v=jwerp2SNiTQ", icon_url="https://a.espncdn.com/photo/2018/0917/r432464_1600x800cc.jpg") # At icon_url, you can also do "ctx.author.avatar_url" To get their profile picture there\
    # Set thumbnail
    embed.set_thumbnail(url="https://i.ytimg.com/vi/iOztnsBPrAA/sddefault.jpg")
    # Extra Fields
    embed.add_field(name="Field_Name", value="Description", inline=False) # If true, then fields will be on the same lines
    embed.add_field(name="Field_name", value="Description", inline=True)
    # Final message at bottom
    embed.set_footer(text="Footer")
    await ctx.send(embed=embed)
    
    
"""
Tournament
Purpose: Add and remove tournaments for members
to view at any time
"""
# Captains Add Tournament
# !add_tournament "tournament_name" "start_date" etc
@client.command()
@commands.has_role('Captain')
async def add_tournament(ctx, name: str, start_date: str, end_date: str, location: str, aof_time: str, field_address: str, lodging_address: str):
    # Check if tournament is already in list
    for tournament in tournament_list: 
        if tournament.name.strip().lower() == name.lower():
            await ctx.send(f"Tournament '{name}' already exists.")
            return
    
    # Create the Tournament object
    tournament = Tournament(name, start_date, end_date, location, aof_time, field_address, lodging_address)
    # Add the tournament to the list
    tournament_list.append(tournament)
    await ctx.send(f"Tournament '{name}' added successfully!")
    
# Delete a Tournament
# !delete_tournament name_of_tournament
@client.command()
@commands.has_role('Captain')
async def delete_tournament(ctx, *, name: str):
    name = name.strip()  # Trim leading and trailing spaces
    global tournament_list
    
    # No tournaments in list
    if not tournament_list:
        await ctx.send("No tournaments to delete.")
        return

    # Create new list without the tournament to be deleted
    new_tournament_list = []
    found = False
    for tournament in tournament_list:
        if tournament.name.strip().lower() == name.lower(): # Normalize the names for comparison
            # Set found to True and do not add to new_tournament_list
            found = True
        else:
            
            new_tournament_list.append(tournament)
    
    # Tournament found
    if found:
        tournament_list = new_tournament_list
        await ctx.send(f"Tournament '{name}' successfully deleted.")
    # No tournament found
    else:
        await ctx.send(f"Tournament '{name}' not found.")
    
    
# Edit a Tournament
# !edit_tournament "tournament_name" "start_date" etc
@client.command()
@commands.has_role('Captain')
async def edit_tournament(ctx, name: str, start_date: str, end_date: str, location: str, aof_time: str, field_address: str, lodging_address: str):
    # Find the tournament by looking for inputted name
    for tournament in tournament_list:
        if tournament.name == name:
            # Update the tournament details
            tournament.start_date = start_date
            tournament.end_date = end_date
            tournament.location = location
            tournament.aof_time = aof_time
            tournament.field_address = field_address
            tournament.lodging_address = lodging_address
            await ctx.send(f"Tournament '{name}' updated successfully!")
            return

    # If tournament was not found
    await ctx.send(f"Tournament '{name}' not found.")

   
    
# View Tournaments
# !tournaments
@client.command()
async def tournaments(ctx):
    if not tournament_list:
        await ctx.send("No tournaments scheduled.")
    else:
        # Title message
        embed = discord.Embed(title="Upcoming Tournaments", color=0xffd700)
        
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
                    "\u200B" # Add separation between each tournament
                ),
                inline=False
            )
            
        # Send tournaments to channel
        await ctx.send(embed=embed)
        
        
# RSVP for Tournament
# !rsvp_tournament tournament_name
@client.command()
async def rsvp_tournament(ctx, *, name: str):
    # Send alerts to captains channel
    channel = client.get_channel(apikeys.CAPTAIN_CHANNEL_ID)
    
    name = name.strip()  # Trim leading and trailing spaces
    global tournament_list
    member_name = ctx.author.display_name  # Get username for user RSVPing

    # Check for tournaments
    if not tournament_list:
        await ctx.send("No tournaments available to RSVP for.")
        return
    
    # Iterate through tournaments
    for tournament in tournament_list:
        if tournament.name.strip().lower() == name.lower():  # Compare names (case-insensitive)
            # Case 1: User already RSVP'd
            if member_name in tournament.rsvp_list:
                await ctx.send(f"{member_name} has already RSVP'd for '{tournament.name}'.")
            # Case 2: Add user to RSVP list
            else:
                tournament.rsvp_list.append(member_name)
                await channel.send(f"{member_name} has successfully RSVP'd for '{tournament.name}'.")
                await ctx.send(f"You successfully RSVP'd for '{tournament.name}'.")
            return
    
    # If tournament is not found
    await ctx.send(f"Tournament '{name}' not found.")


# Un-RSVP from tournament
@client.command()
async def unrsvp_tournament(ctx, *, name: str):
    channel = client.get_channel(apikeys.CAPTAIN_CHANNEL_ID)
    
    name = name.strip() # Trim leading and trailing spaces
    global tournament_list
    member_name = ctx.author.display_name
    
    # Check if tournaments exists in list
    if not tournament_list: 
        await ctx.send("No tournaments available to un-RSVP from.")
        return
    
    # Find tournament user wants to un-RSVP from
    for tournament in tournament_list:
        if tournament.name.strip().lower() == name.lower():
            # Case 1: User is in list, so remove them
            if member_name in tournament.rsvp_list: 
                tournament.rsvp_list.remove(member_name)
                await channel.send(f"{member_name} has un-RSVP'd from '{tournament.name}'.")
                await ctx.send(f"You successfully un-RSVP'd from '{tournament.name}'.")
            # Case 2: User is not in list
            else:
                await ctx.send(f"You are not on the RSVP list for '{tournament.name}'.")
            return
        
    # Tournament not found
    await ctx.send("f{member_name}")

# View list of RSVP's for a tournament
# view_rsvp_list tournament_name
@client.command()
@commands.has_role('Captain')
async def view_rsvp_list(ctx, *, name: str):
    name = name.strip()  # Trim leading and trailing spaces
    
    for tournament in tournament_list:
        if tournament.name.strip().lower() == name.lower():
            # Case 1: There are RSVP's
            if tournament.rsvp_list:
                # List of players who rsvp'd
                rsvp_names = '\n'.join([f"• {player}" for player in tournament.rsvp_list])
                
                # Embed for list of players who rsvp'd
                embed = discord.Embed(title=f"RSVP List for {tournament.name}", color=0xffd700)
                embed.add_field(name="**Players**", value=rsvp_names, inline=False)
                embed.add_field(name="**Total RSVPs**", value=str(len(tournament.rsvp_list)), inline=False)
                
                # Send tournaments to channel
                await ctx.send(embed=embed)
                
            # Case 2: No RSVP's
            else:
                await ctx.send(f"No RSVPs for '{tournament.name}' yet.")
            return
        
    # If tournament is not found
    await ctx.send(f"Tournament '{name}' not found.")
        
    
        
        
'''
Other Commands
'''
# Ultimate Frisbee Rulebook
# !rulebook
@client.command()
async def rulebook(ctx):
    embed = discord.Embed(title="College Ultimate Frisbee Rulebook", url="https://usaultimate.org/rules/", description="USA Ultimate Official Rules of Ultimate", color=0xe6451f)
    embed.set_thumbnail(url="https://usaultimate.org/wp-content/uploads/2020/12/D1Nats_2019_PMR_5-27-19_3-20-53-PM-ZF-7045-98232-1-003-e1607747796388.jpg")
    await ctx.send(embed=embed)
    
    
    
    
    
'''
EVENTS
'''
# Welcome new member
@client.event
async def on_member_join(member):
    channel = client.get_channel(apikeys.WELCOME_CHANNEL_ID)
    await channel.send("Welcome to the Tennessee Tech Talons!")


# Run client with discord bot token
client.run(apikeys.BOT_TOKEN)

