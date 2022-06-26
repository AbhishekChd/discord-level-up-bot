import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
import random
import sqlite3

user_rank_info = {}




intents = discord.Intents().all()
load_dotenv()
bot = commands.Bot(command_prefix="n?",
intents = intents,
case_insensitive=False,
)
bot.remove_command('help')
@bot.event


async def on_ready():
    print("My name is {0.user} and i am ready to go".format(bot))
    await bot.change_presence(activity=discord.Game('n?help'))
      

@bot.command(aliases=['h'])
async def help(ctx: commands.Context):
    print("need help")
    embed = discord.Embed(
        title = "🤖 Help has arrived",
        description = "Hello! I am currently under development by Nikkk †",
        color= 0xFF5733
    )
    embed.set_author(name=ctx.author,
    icon_url=ctx.author.avatar_url)
    embed.add_field(name="Prefix", value="My prefix is `n?`\n\n", inline=False)
    embed.add_field(name="Commands", value="`n?rank`, `n?leaderboard`\n\nThat's it for now, working on new commands !", inline=False)
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/708412887915298910/2840c49ac54bf671deca31f77e14d993.webp?size=1024")
    embed.set_image(url= "https://c.tenor.com/5hKPyupKGWMAAAAC/robot-hello.gif")
    embed.set_footer(text="Nice to meet you!")
    await ctx.send(embed=embed)
    

@bot.command(aliases=['lb'])
async def leaderboard(ctx):



    list_limit = 0
    mem_str = " "


    for user in list(ctx.guild.members):
        if user.bot :
            continue
        else : 
            list_limit = list_limit + 1
            if list_limit == 1 :
                 mem_str = mem_str + '\n\n' + ':first_place:  ' + str("`00` - ") +  str(user)
            if list_limit == 2 :
                 mem_str = mem_str + '\n' + ':second_place:  '+ str("`00` - ") +  str(user)
            if list_limit == 3 :
                 mem_str = mem_str + '\n' + ':third_place:  ' + str("`00` - ") +  str(user)
            elif list_limit > 3 and list_limit < 11 : 
                mem_str = mem_str + '\n' + ':small_blue_diamond:  ' + str("`00` - ") +  str(user)
            elif list_limit > 11 :
                break
         

    embed = discord.Embed(
        title= "Leaderboard",
        description= mem_str,
        colour=  0xFF5733
                )
    embed.set_image(url="https://c.tenor.com/JwxZhUN9MKgAAAAM/4%C2%BApr%C3%AAmio-bloxy-anual.gif")
    embed.set_footer(text="Top 10 memebers of the server")

    await ctx.send(embed=embed)






@bot.command(aliases=['r'])
async def rank(ctx: commands.Context, ):
    def get_formatted_xp(user_rank_info):
        xp = user_rank_info[str(ctx.author)]["xp"]
        level = user_rank_info[str(ctx.author)]["level"]
        xp_required = (level + 1) ** 4
        output = "`{xp}/{xp_required}`".format(xp=xp, xp_required=xp_required)
        return output
    def get_formatted_level(user_rank_info):
        level = user_rank_info[str(ctx.author)]["level"]
        output = "`{level}`".format(level=level)
        return output
    print("making embed")
    xp_rank = get_formatted_xp(user_rank_info=user_rank_info)
    level_rank = get_formatted_level(user_rank_info=user_rank_info)
    embed = discord.Embed(
        title= "*Server Rank of -* " + str(ctx.author) ,
        description= "**Your server rank increases as you chat, increase your rank to get high reward roles and flex on your friends** <:2940coolpepe:988766350430322738> ",
        colour=  0xFF5733
    )
    embed.add_field(name="Rank", value="00", inline=False)
    embed.add_field(name="Current level", value= level_rank, inline=True)
    embed.add_field(name="xp", value=xp_rank, inline=True)
    embed.add_field(name="Awarded role", value="<role>", inline=False)
    embed.set_author(name=ctx.author,
    icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.set_image(url="https://i.imgur.com/cerqOld.gif")
    await ctx.send(embed=embed)
            
@bot.event
async def on_message(context) :
    human_memebers = []
    for user in list(context.guild.members):
        if user.bot :
            continue
        else:
            human_memebers.append(user)
    if context.author in human_memebers :

        if str(context.author) in user_rank_info :
            user_rank_info[str(context.author)]["xp"] = int(user_rank_info[str(context.author)]["xp"]) + random.randint(0,(5 + 2*(int(user_rank_info[str(context.author)]["level"]))))
            if int(user_rank_info[str(context.author)]["xp"]) > 0 :
                if int(user_rank_info[str(context.author)]["level"]) < int((int(user_rank_info[str(context.author)]["xp"]))**(1/4)) :
                    #lvl_up = "congrats {user} !! your have leveled up to".format + str(int((int(user_rank_info["xp"]))**(1/4)))
                    await context.channel.send(str("You leveled up !!"))
                    print(user_rank_info)

            user_rank_info[str(context.author)]["level"] = int((int(user_rank_info[str(context.author)]["xp"]))**(1/4))



        if str(context.author) not in user_rank_info :
            user_rank_info[str(context.author)] = {"level" : 1, "xp" : 0, }
            print(user_rank_info)
            return user_rank_info
    
        
        else : 
            await bot.process_commands(context)
     


token = os.environ['discord-token']
bot.run(token)
