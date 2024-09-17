"""
Name: Logan McDavid
Filename: learning_commands.py    
Purpose: Contains commands associated with
me learning and experimenting with the 
discord bot
"""
import discord
import requests
from discord.ext import commands

# Learning Commands Class
class LearningCommands(commands.Cog):
    # Constructor
    def __init__(self, bot):
        self.bot = bot
        
    # Learning bot turning on 
    @commands.Cog.listener()
    async def on_ready(self):
        print("Learning Bot is Online!")
        
    # !ping
    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong") 
        
    # !dog
    @commands.command()
    async def dog(self, ctx):
        response = requests.get("https://dog.ceo/api/breeds/image/random")
        res = response.json()
        em = discord.Embed()  # Makes the photo look nice and dandy
        em.set_image(url=res['message'])
        await ctx.send(embed=em)
        
    # !cat
    @commands.command()
    async def cat(self, ctx):
        embed = discord.Embed(
            title="Title",
            url="https://www.google.com/search?q=Cute+kittens&sca_esv=719ed570ba997555&sca_upv=1&udm=2&biw=1703&bih=1306&sxsrf=ADLYWILLLDUJH0ZgxPD7SnZFGLLl_IzHTQ%3A1725337114674&ei=Go7WZqnxKMbGkPIP5dPdSQ&ved=0ahUKEwip5tnO9aWIAxVGI0QIHeVpNwkQ4dUDCBE&uact=5&oq=Cute+kittens&gs_lp=Egxnd3Mtd2l6LXNlcnAiDEN1dGUga2l0dGVuczIIEAAYgAQYsQMyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgARI4xlQgwtYrxdwAngAkAEAmAFooAGfCaoBAzkuM7gBA8gBAPgBAZgCDqACvwnCAg0QABiABBixAxhDGIoFwgILEAAYgAQYsQMYgwHCAgQQIxgnwgIKEAAYgAQYQxiKBZgDAIgGAZIHAzYuOKAHyz8&sclient=gws-wiz-serp",
            description="This one for all my cat lovers",
            color=0x4d8b6a
        )
        embed.set_author(
            name="Author",
            url="https://www.youtube.com/watch?v=jwerp2SNiTQ",
            icon_url="https://a.espncdn.com/photo/2018/0917/r432464_1600x800cc.jpg"
        )
        embed.set_thumbnail(url="https://i.ytimg.com/vi/iOztnsBPrAA/sddefault.jpg")
        embed.add_field(name="Field_Name", value="Description", inline=False)
        embed.add_field(name="Field_name", value="Description", inline=True)
        embed.set_footer(text="Footer")
        await ctx.send(embed=embed)
        
            

"""
    # Welcome new member
    @commands.event
    async def on_member_join(member, self):
        channel = self.bot.get_channel(apikeys.WELCOME_CHANNEL_ID)
        await channel.send("Welcome to the Tennessee Tech Talons!")
"""


# Set up Learning bot
async def setup(bot):
    await bot.add_cog(LearningCommands(bot))