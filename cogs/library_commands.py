"""
Name: Logan McDavid
Filename: library_commands.py    
Purpose: Contains commands asociated with
the library, such as drills, formations, 
rules etc.
"""
import discord
from discord.ext import commands

# Library Commands Class
class LibraryCommands(commands.Cog):
    # Constructor
    def __init__(self, bot):
        self.bot = bot
        
    # Library bot turning on
    commands.Cog.listener()
    async def on_ready(self):
        print("Library Bot is Online")
        
        
    """
    TOURNAMENT LIBRARY COMMANDS
    """    
    # Member permissions
    @commands.command()
    async def tournament_commands(self, ctx):
        # Title message
        embed = discord.Embed(
            title="Tournament Commands", 
            color=0xffd700
        )

        # View tournament command
        embed.add_field(
            name="**View Tournaments**",
            value="`!tournaments`",
            inline=False
        )

        # RSVP/unRSVP tournament commands
        embed.add_field(
            name="**RSVP/UnRSVP to a Tournament**",
            value=(
                "`!rsvp_tournament <Tournament Name>`\n"
                "`!unrsvp_tournament <Tournament Name>`"
            ),
            inline=False
        )

        # Tournament packing list
        embed.add_field(
            name="**Tournament Packing List**",
            value="`!tournament_packing_list`",
            inline=False
        )

        # Send the embed message
        await ctx.send(embed=embed)
        
    # Captain Permissions
    @commands.command()
    @commands.has_role('Captain')
    async def tournament_commands_captain(self, ctx):
        # Title message
        embed = discord.Embed(
            title="Tournament Commands for Captains",
            color=0xffd700
        )
        
        # Add tournament command
        embed.add_field(
            name="Add a Tournament",
            value="`!add_tournament \"Tournament Name\" \"Start Date\" \"End Date\" \"Location\" \"Arrival on Field Time\" \"Field Address\" \"Lodging Address\"`",
            inline=False
        )
        
        # Delete tournament command
        embed.add_field(
            name="Delete a Tournament",
            value="`!delete_tournament <Tournament Name>`",
            inline=False
        )
        
        # Edit tournament command
        embed.add_field(
            name="Edit a Tournament",
            value="`!edit_tournament \"Tournament Name\" \"Start Date\" \"End Date\" \"Location\" \"Arrival on Field Time\" \"Field Address\" \"Lodging Address\"`",
            inline=False
        )
        
        # View tournament rsvp list command
        embed.add_field(
            name="View List of RSVPs for Tournament",
            value="`!view_tournament_rsvp_list <Tournament Name>`",
            inline=False
        )
        
        # Send the embed message
        await ctx.send(embed=embed)

    
    """
    PURPLE VS. GOLD LIBRARY COMMANDS
    """
    # Member permissions
    @commands.command()
    async def scrimmage_commands(self, ctx):
        # Title message
        embed = discord.Embed(
            title="Scrimamge Commands",
            color=0x816CB4
        )
        
        # RSVP/unRSVP from scrimmage
        embed.add_field(
            name="**RSVP/unRSVP from Scrimmage**",
            value=(
                "`!rsvp_scrimmage`\n"
                "`!unrsvp_scrimmage`"
            ),
            inline=False
        )
        
        # Send the embed message
        await ctx.send(embed=embed)
        
    # Captain Permissions
    @commands.command()
    @commands.has_role('Captain')
    async def scrimmage_commands_captain(self, ctx):
        # Title message
        embed = discord.Embed(
            title="Scrimmage Commands for Captains",
            color=0x816CB4
        )
        
        # View scrimmage rsvp list
        embed.add_field(
            name="View Scrimmage RSVP List",
            value="`!view_scrimmage_rsvp_list`",
            inline=False
        )
        
        # Randomly sort teams
        embed.add_field(
            name="Randomly Sort Purple and Gold Teams",
            value="`!sort_teams`",
            inline=False
        )
        
        # Approve sorted teams
        embed.add_field(
            name="Approve and Assign Purple & Gold Roles",
            value="`!approve_teams`",
            inline=False
        )
        
        # Reset teams 
        embed.add_field(
            name="Reset Purple and Gold Teams",
            value="`!reset_teams`",
            inline=False
        )
        
        # Send the embed message
        await ctx.send(embed=embed)
        
        
    
    """
    CHANNEL LIBRARY COMMANDS
    """
    @commands.command()
    async def channel_commands(self, ctx):
        # Title message
        embed = discord.Embed(
            title="Channel Commands",
            color=0xFFB6C1
        )
        
        # Choose/Remove Position
        embed.add_field(
            name="Choose/Remove Position",
            value=(
                "`!choose_position <position name>`\n"
                "`!remove_position <position name>`\n"
                "**<position name>** = *cutter*, *handler* or *cutter handler*"
            ),
            inline=False
        )
        
        # Add/Remove Tournament Role
        embed.add_field(
            name="Add/Remove Tournament Role",
            value=(
                "`!add_tournament_role`\n"
                "`!remove_tournament_role`"
            ),
            inline=False
        )
        
        # Add/Remove Purple or Gold Team
        embed.add_field(
            name="Add/Remove Purple or Gold Team",
            value=(
                "`!add_purple_gold <team name>`\n"
                "`!remove_pruple_gold <team name>`\n"
                "**<team name>** = *purple* or *gold*"              
            ),
            inline=False
        )
        
        # Send the embed message
        await ctx.send(embed=embed)
    
    
    
    """
    OTHER LIBRARY COMMANDS   
    """
    # Ultimate Frisbee Rulebook
    # !rulebook
    @commands.command()
    async def rulebook(self, ctx):
        # Title message
        embed = discord.Embed(
            title="College Ultimate Frisbee Rulebook",
            url="https://usaultimate.org/rules/", 
            description="USA Ultimate Official Rules of Ultimate", 
            color=0xe6451f
        )
        
        # Thumbnail
        embed.set_thumbnail(
            url="https://usaultimate.org/wp-content/uploads/2020/12/D1Nats_2019_PMR_5-27-19_3-20-53-PM-ZF-7045-98232-1-003-e1607747796388.jpg"
        )
        
        # Send the embed message
        await ctx.send(embed=embed)
    
    # Talons Playbook
    # !playbook
    @commands.command()
    async def playbook(self, ctx):
        # Title message
        embed = discord.Embed(
            title="Talons Playbook",
            url="https://www.ultiplays.com/invite/lnB2g3PPDrskWpx03q31",
            description="Tech Talons Official Playbook",
            color=0xe6451f
        )
        
        # Thumbnail
        embed.set_thumbnail(
            url="https://cdn.ultiworld.com/wordpress/wp-content/uploads/2016/01/WUCC_Day5_Wed_20140806_135745_BC4_182-ZF-9554-89220-1-001.jpg?x58670"
        )
        
        # Send the embed message
        await ctx.send(embed=embed)
        
    
# Set up Library bot
async def setup(bot):
    await bot.add_cog(LibraryCommands(bot))
    