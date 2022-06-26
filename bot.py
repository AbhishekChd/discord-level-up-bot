
from aiosqlite import Cursor
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
import random
import sqlite3



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
    conn = sqlite3.connect('user_level_data.sqlite')
    cur = conn.cursor()
    try :
        cur.execute('CREATE TABLE rankings (rank INTEGER, user_id STRING, level INTEGER, xp INTEGER)')
    except :
        print("database exists")

      

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

    conn = sqlite3.connect('user_level_data.sqlite')
    cur = conn.cursor()
    test = 'SELECT user_id, level from rankings ORDER BY level DESC LIMIT 10'
    
    list_limit = 0
    mem_str = " "


    for row in cur.execute(test) :
            list_limit = list_limit + 1
            if list_limit == 1 :
                 mem_str = mem_str + '\n\n' + ':first_place:  ' +'`lvl: {level} - `'.format(level=row[1]) +  '<@{user}>'.format(user=str(row[0]))
            if list_limit == 2 :
                 mem_str = mem_str + '\n' + ':second_place:  '+'`lvl: {level} - `'.format(level=row[1]) +  '<@{user}>'.format(user=str(row[0]))
            if list_limit == 3 :
                 mem_str = mem_str + '\n' + ':third_place:  ' +'`lvl: {level} - `'.format(level=row[1]) +  '<@{user}>'.format(user=str(row[0]))
            elif list_limit > 3 and list_limit < 11 : 
                mem_str = mem_str + '\n' + ':small_blue_diamond:  ' +'`lvl: {level} - `'.format(level=row[1]) +  '<@{user}>'.format(user=str(row[0]))
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
    def get_formatted_xp():
        conn = sqlite3.connect('user_level_data.sqlite')
        cur = conn.cursor()
        cur.execute('SELECT xp FROM rankings WHERE user_id = ?', (str(ctx.author.id), ))
        xp = cur.fetchone()
        cur.execute('SELECT level FROM rankings WHERE user_id = ?', (str(ctx.author.id), ))
        level = cur.fetchone()
        xp_required = (int(level[0]) + 1) ** 4
        output = "`{xp}/{xp_required}`".format(xp=int(xp[0]), xp_required=xp_required)
        cur.close()
        return output
    def get_formatted_level():
        conn = sqlite3.connect('user_level_data.sqlite')
        cur = conn.cursor()
        cur.execute('SELECT level FROM rankings WHERE user_id = ?', (str(ctx.author.id), ))
        level = cur.fetchone()
        output = "`{level}`".format(level=int(level[0]))
        cur.close()
        return output
    def get_formatted_rank():
        conn = sqlite3.connect('user_level_data.sqlite')
        cur = conn.cursor()
        cur.execute('SELECT rank FROM rankings WHERE user_id = ?', (str(ctx.author.id), ))
        rank = cur.fetchone()
        output = "`{rank}`".format(rank=int(rank[0]))
        cur.close()
        return output
    


    xp_rank = get_formatted_xp()
    level_rank = get_formatted_level()
    rank_rank = get_formatted_rank()
    embed = discord.Embed(
        title= "*Server Rank of -* " + str(ctx.author) ,
        description= "**Your server rank increases as you chat, increase your rank to get high reward roles and flex on your friends** <:2940coolpepe:988766350430322738> ",
        colour=  0xFF5733
    )
    embed.add_field(name="Rank", value=rank_rank, inline=False)
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
    conn = sqlite3.connect('user_level_data.sqlite')
    cur = conn.cursor()
    cur.execute('SELECT xp FROM rankings WHERE user_id = ?', (str(context.author.id),))
    row = cur.fetchone()

    if context.author in human_memebers :

        if context.content.startswith("n?") :

            await bot.process_commands(context)
        else :

        
            if row is None :
                cur.execute('INSERT INTO rankings (rank, user_id, level, xp) VALUES (0, {user}, 1, 1)'.format(user=str(context.author.id)))

            if row is not None :
                xp_upgrade = random.randint(0, 10)
                new_level = int(int(int(row[0]))**(1/4))
                cur.execute('SELECT level FROM rankings WHERE user_id = ?', (str(context.author.id),))
                level = cur.fetchone()
                if new_level > int(level[0]) :
                   await context.channel.send('Congratulations!! <@{user}> your have leveled up to **lvl.{level}**'.format(user=str(context.author.id), level=new_level))

                cur.execute('UPDATE rankings SET xp = xp + {xp_upgrade} WHERE user_id = ? '.format(xp_upgrade=xp_upgrade), (str(context.author.id), ))
                cur.execute('UPDATE rankings SET level = {new_level} WHERE user_id = ? '.format(new_level=new_level), (str(context.author.id), ))
                 
                rank_list=[]
                rank_num = 0
                for rank_extract in cur.execute( 'SELECT level, user_id from rankings ORDER BY level') :
                    rank_list.append(rank_extract)
                    rank_num = rank_num + 1
                rank_list.sort(reverse=True)
                for i in range (rank_num ) :
                   user_id = rank_list[i][1]
                   new_rank = i + 1
                   cur.execute('UPDATE rankings SET rank = {new_rank} WHERE user_id = ? '.format(new_rank=new_rank), (str(user_id), ))
                
                cur.execute('SELECT level FROM rankings WHERE user_id = ?', (str(context.author.id),))
                role_level = cur.fetchone()
                
                
                

                

                


            

    conn.commit()
    cur.close()
     


token = os.environ['discord-token']
bot.run(token)
