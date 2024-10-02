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
    LIBRARY COMMANDS   
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
        
    @commands.command()
    async def help(self, ctx):
        # Title message
        embed = discord.Embed(
            title="Helpful Commands",
            color=0xC0C0C0
        )
        
        # Tournament Help
        embed.add_field(
            name="Tournament Help",
            value="`!tournament_commands`",
            inline=False
        )
        
        # Scrimmage Help
        embed.add_field(
            name="Scrimmage Help",
            value="`!scrimmage_commands`",
            inline=False
        )
        
        # Channel Help
        embed.add_field(
            name="Channel Help",
            value="`!channel_commands`",
            inline=False
        )
        
        # Send the embed message
        await ctx.send(embed=embed)
        
    @commands.command()
    @commands.has_role('Captain')
    async def help_captain(self, ctx):
        # Title message
        embed = discord.Embed(
            title="Helpful Captain Commands",
            color=0xC0C0C0
        )
        
        # Tournament Help
        embed.add_field(
            name="Tournament Help for Captains",
            value="`!tournament_commands_captain`",
            inline=False
        )
        
        # Scrimmage Help
        embed.add_field(
            name="Scrimmage Help for Captains",
            value="`!scrimmage_commands_captain`",
            inline=False
        )
        
        # Send the embed message
        await ctx.send(embed=embed)
    
    
# Set up Library bot
async def setup(bot):
    await bot.add_cog(LibraryCommands(bot))
    