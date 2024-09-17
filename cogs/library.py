import discord
from discord.ext import commands

class LibraryCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    commands.Cog.listener()
    async def on_ready(self):
        print("Library Bot is Online")
        
        
    # Ultimate Frisbee Rulebook
    # !rulebook
    @commands.command()
    async def rulebook(self, ctx):
        embed = discord.Embed(title="College Ultimate Frisbee Rulebook", url="https://usaultimate.org/rules/", description="USA Ultimate Official Rules of Ultimate", color=0xe6451f)
        embed.set_thumbnail(url="https://usaultimate.org/wp-content/uploads/2020/12/D1Nats_2019_PMR_5-27-19_3-20-53-PM-ZF-7045-98232-1-003-e1607747796388.jpg")
        await ctx.send(embed=embed)
    
    
        
        
async def setup(bot):
    await bot.add_cog(LibraryCommands(bot))