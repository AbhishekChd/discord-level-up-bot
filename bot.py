import discord
import os
import requests
import json
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
bot = commands.Bot(command_prefix="$")
bot.remove_command('help')

@bot.command()
async def help(ctx: commands.Context):
    print("Help Me :(")
    embed = discord.Embed(
        title = "🤖 Help",
        description = help_text,
        color= 0xFF5733,
        _author="Abhishek"
    )
    embed.set_author(name=ctx.author)
    await ctx.send(embed=embed)
    
help_text = """
Hello I am a bot currently under development by Nikkk and Abhishek
My prefix is `$`
Nice to meet you!
"""


@bot.event
async def on_ready():
    print("My name is {0.user} and i am ready to go".format(bot))

token = os.environ['discord-token']
bot.run(token)
