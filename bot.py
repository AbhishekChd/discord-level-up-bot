
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
import random
import sqlite3
from flask import Flask
from threading import Thread
from discord.ext import tasks
from itertools import cycle
from discord.ext.commands import cooldown, BucketType
from discord.ext.commands import has_permissions, MissingPermissions

app = Flask('')

@app.route('/')
def main():
  return "Your Bot Is Ready"

def run():
  app.run(host="0.0.0.0", port=8000)

def keep_alive():
  server = Thread(target=run)
  server.start()



intents = discord.Intents().all()
load_dotenv()
bot = commands.Bot(command_prefix="n?",
intents = intents,
case_insensitive=False,
)
bot.remove_command('help')

status = cycle(['n?help','n?h'])



@bot.event
async def on_ready():
    print("My name is {0.user} and i am ready to go".format(bot))
    change_status.start()
    print("Your bot is ready")
    conn = sqlite3.connect('user_level_data.sqlite')
    cur = conn.cursor()
    try :
        cur.execute('CREATE TABLE rankings (rank INTEGER, user_id STRING, level INTEGER, xp INTEGER, awarded_role INTEGER)')
    except :
        print("database exists")
    conn.close()

@tasks.loop(seconds=10)
async def change_status():
  await bot.change_presence(activity=discord.Game(next(status)))

      

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
    embed.add_field(name="Commands", value="`n?rank`, `n?leaderboard`", inline=False)
    embed.add_field(name="Admin only commands", value="`n?givexp @user ammount`, `n?resetxp @user`, `n?setlevel @user`\n\nThat's it for now, working on new commands !", inline=False)
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/708412887915298910/2840c49ac54bf671deca31f77e14d993.webp?size=1024")
    embed.set_image(url= "https://c.tenor.com/5hKPyupKGWMAAAAC/robot-hello.gif")
    embed.set_footer(text="Nice to meet you!")
    await ctx.send(embed=embed)


@commands.cooldown(1, 30, commands.BucketType.user)
@bot.command(aliases=['lb'])
async def leaderboard(ctx):

    conn = sqlite3.connect('user_level_data.sqlite', timeout = 10)
    cur = conn.cursor()
    test = 'SELECT user_id, level from rankings ORDER BY level DESC LIMIT 10'
    
    list_limit = 0
    mem_str = " "


    for row in cur.execute(test) :
            list_limit = list_limit + 1
            if list_limit == 1 :
                 mem_str = mem_str + '\n\n' + ':first_place:  ' +'`lvl: {level}` - '.format(level=row[1]) +  '<@{user}>'.format(user=str(row[0]))
            if list_limit == 2 :
                 mem_str = mem_str + '\n' + ':second_place:  '+'`lvl: {level}` - '.format(level=row[1]) +  '<@{user}>'.format(user=str(row[0]))
            if list_limit == 3 :
                 mem_str = mem_str + '\n' + ':third_place:  ' +'`lvl: {level}` - '.format(level=row[1]) +  '<@{user}>'.format(user=str(row[0]))
            elif list_limit > 3 and list_limit < 11 : 
                mem_str = mem_str + '\n' + ':small_blue_diamond:  ' +'`lvl: {level}` - '.format(level=row[1]) +  '<@{user}>'.format(user=str(row[0]))
            elif list_limit > 11 :
                break
    conn.commit()
    cur.close()

    embed = discord.Embed(
        title= "Leaderboard",
        description= mem_str,
        colour=  0xFF5733
                )
    embed.set_image(url="https://c.tenor.com/JwxZhUN9MKgAAAAM/4%C2%BApr%C3%AAmio-bloxy-anual.gif")
    embed.set_footer(text="Top 10 memebers of the server")

    await ctx.send(embed=embed)




@leaderboard.error
async def leaderboard_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"Slow it down bro!",description=f"Try again in {error.retry_after:.2f}s.", color=0xFF5733)
            await ctx.send(embed=em)


@commands.cooldown(1, 10, commands.BucketType.user)
@bot.command(aliases=['r'])
async def rank(ctx: commands.Context):
    conn = sqlite3.connect('user_level_data.sqlite', timeout = 60)
    cur = conn.cursor()
    def get_formatted_xp():
        conn = sqlite3.connect('user_level_data.sqlite', timeout = 60)
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
        conn = sqlite3.connect('user_level_data.sqlite', timeout = 60)
        cur = conn.cursor()
        cur.execute('SELECT level FROM rankings WHERE user_id = ?', (str(ctx.author.id), ))
        level = cur.fetchone()
        output = "`{level}`".format(level=int(level[0]))
        cur.close()
        return output
    def get_formatted_rank():
        conn = sqlite3.connect('user_level_data.sqlite', timeout = 60)
        cur = conn.cursor()
        cur.execute('SELECT rank FROM rankings WHERE user_id = ?', (str(ctx.author.id), ))
        rank = cur.fetchone()
        output = "`{rank}`".format(rank=int(rank[0]))
        cur.close()
        return output
    cur.execute('SELECT awarded_role FROM rankings WHERE user_id= ?',(str(ctx.author.id), ) )
    awarded_role_rank = cur.fetchone()
    formatted_role_Rank = "<@&{awarded_role}>".format(awarded_role=awarded_role_rank[0])
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
    embed.add_field(name="Awarded role", value=formatted_role_Rank, inline=False)
    embed.set_author(name=ctx.author,
    icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.set_image(url="https://i.imgur.com/cerqOld.gif")
    await ctx.send(embed=embed)




@rank.error
async def rank_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"Slow it down bro!",description=f"Try again in {error.retry_after:.2f}s.", color=0xFF5733)
            await ctx.send(embed=em)




@bot.event
async def on_message(context) :


    if int(context.channel.id) == 988711128106430484 :
        await bot.process_commands(context)
        return
    else :
        human_memebers = []
        for user in list(context.guild.members):
            if user.bot :
                continue
            else:
                human_memebers.append(user)
        conn = sqlite3.connect('user_level_data.sqlite', timeout = 60)
        cur = conn.cursor()
        cur.execute('SELECT xp FROM rankings WHERE user_id = ?', (str(context.author.id),))
        row = cur.fetchone()

        if context.author in human_memebers :

            if context.content.startswith("n?") :

                await bot.process_commands(context)
            else :

            
                if row is None :
                    cur.execute('INSERT INTO rankings (rank, user_id, level, xp, awarded_role) VALUES (0, {user}, 1, 1, 989839086036611092)'.format(user=str(context.author.id)))
                    role = context.guild.get_role(989839086036611092)
                    await context.author.add_roles(role)

                if row is not None :
                    xp_upgrade = random.randint(0, 10)
                    new_level = int(int(int(row[0]))**(1/4))
                    
                    cur.execute('SELECT level FROM rankings WHERE user_id = ?', (str(context.author.id),))
                    level = cur.fetchone()
                    cur.execute('UPDATE rankings SET xp = xp + {xp_upgrade} WHERE user_id = ? '.format(xp_upgrade=xp_upgrade), (str(context.author.id), ))
                    cur.execute('UPDATE rankings SET level = {new_level} WHERE user_id = ? '.format(new_level=new_level), (str(context.author.id), ))
                    if new_level > int(level[0]) :
                        channel = bot.get_channel(988718132841562112)
                        await channel.send('Congratulations!! <@{user}> your have leveled up to **lvl.{level}**'.format(user=str(context.author.id), level=new_level))
                    
                
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
                    
                    level_list = [988788954520223786, 988789087542607882, 988789327167361074, 988789558642638869, 988789361443237978, 988794780584669236, 988794832333996102, 988795209104097320, 988794902529863690, 988795128753827941, 988795479376670740, 988795479426998402, 988795480911794176, 988795479477325855, 988795962296238100, 988796013328359484, 988796062422675498, 988796151081869372, 991071423495806976, 988796343986298890]
                    cur.execute('SELECT level FROM rankings WHERE user_id = ?', (str(context.author.id), ))
                    current_level = cur.fetchone()
                    for level_role in level_list :                       
                        if (int(level_list.index(level_role)) + 1)*5 == int(current_level[0]) :

                                role = context.guild.get_role(int(level_role))
                                await context.author.add_roles(role)
                                cur.execute('UPDATE rankings SET awarded_role = {new_awarded_role} WHERE user_id= ?'.format(new_awarded_role=level_role),(str(context.author.id), ))
                        else :     
                                role = context.guild.get_role(level_role)
                                await context.author.remove_roles(role)

        conn.commit()
        cur.close()
     





@bot.command(aliases=['gx']) 
@commands.has_permissions(administrator=True)
async def givexp(context,user: discord.Member, *, xp_addition) :
    human_memebers = []
    for bot_check in list(context.guild.members):
            if bot_check.bot :
                continue
            else:
                human_memebers.append(bot_check)

    conn = sqlite3.connect('user_level_data.sqlite', timeout = 10)
    cur = conn.cursor()
    cur.execute('SELECT xp FROM rankings WHERE user_id = ?', (str(user.id),))
    xp = cur.fetchone()
    print(user)
    if user in human_memebers :
        if xp is None :
            await context.channel.send('User <@{user_id}> is not registered, you need to have texted atleast once in the server to register yourself !'.format(user_id=int(user.id)))
        else :
            cur.execute('UPDATE rankings SET xp = xp + {xp_addition} WHERE user_id = ? '.format(xp_addition=xp_addition), (str(user.id), ))
            
            new_level = int(int(int(xp[0]))**(1/4))       
            cur.execute('SELECT level FROM rankings WHERE user_id = ?', (str(user.id),))
            level = cur.fetchone()
            cur.execute('UPDATE rankings SET level = {new_level} WHERE user_id = ? '.format(new_level=new_level), (str(user.id), ))
            if new_level > int(level[0]) :
                channel = bot.get_channel(988718132841562112)
                await channel.send('Congratulations!! <@{user}> your have leveled up to **lvl.{level}**'.format(user=str(user.id), level=new_level))
            rank_list=[]
            rank_num = 0
            for rank_extract in cur.execute( 'SELECT level, user_id from rankings ORDER BY level') :
                rank_list.append(rank_extract)
                rank_num = rank_num + 1
            rank_list.sort(reverse=True)
            for i in range (rank_num ) :
                user_id = rank_list[i][1]
                new_rank = i + 1
                cur.execute('UPDATE rankings SET rank = {new_rank} WHERE user_id = ? '.format(new_rank=new_rank), (str(user.id), ))
            await context.channel.send('Added {xp_addition} xp to <@{user_id}> !'.format(user_id=int(user.id), xp_addition=xp_addition))

        conn.commit()
        cur.close()
    else :
        await context.channel.send("Can't give xp to a bot")




@givexp.error
async def givexp_error(ctx, error):
        if isinstance(error,  MissingPermissions):
            em = discord.Embed(title=f"Watch out !",description="This is a admin only command !", color=0xFF5733)
            await ctx.send(embed=em)


@bot.command(aliases=['rx']) 
@commands.has_permissions(administrator=True)
async def resetxp(context,user: discord.Member) :
    human_memebers = []
    for bot_check in list(context.guild.members):
            if  bot_check.bot :
                continue
            else:
                human_memebers.append(bot_check)

    conn = sqlite3.connect('user_level_data.sqlite', timeout = 10)
    cur = conn.cursor()
    cur.execute('SELECT xp FROM rankings WHERE user_id = ?', (str(user.id), ))
    xp = cur.fetchone()
    if user in human_memebers :
        if xp is None :
            await context.channel.send('User <@{user_id}> is not registered, you need to have texted atleast once in the server to register yourself !'.format(user_id=int(user.id)))
        else :
            cur.execute('DELETE FROM rankings WHERE user_id = ?',(str(user.id), ))
            cur.execute('INSERT INTO rankings (rank, user_id, level, xp, awarded_role) VALUES (0, {user}, 1, 1, 989839086036611092)'.format(user=str(context.author.id)))
            role = context.guild.get_role(989839086036611092)
            await context.author.add_roles(role)
            await context.channel.send('Succsefullly reseted xp info of user <@{user}>'.format(user=str(user.id)))
    else :
        await context.channel.send("Can't reset bot's exp")
    conn.commit()
    cur.close()




@resetxp.error
async def resetxp_error(ctx, error):
        if isinstance(error,  MissingPermissions ):
            em = discord.Embed(title=f"Watch out !",description="This is a admin only command !", color=0xFF5733)
            await ctx.send(embed=em)

@bot.command(aliases=['sl']) 
@commands.has_permissions(administrator=True)
async def setlevel(context,user: discord.Member, *, set_level) :
    human_memebers = []
    for bot_check in list(context.guild.members):
            if  bot_check.bot :
                continue
            else:
                human_memebers.append(bot_check)

    conn = sqlite3.connect('user_level_data.sqlite', timeout = 10)
    cur = conn.cursor()
    cur.execute('SELECT xp FROM rankings WHERE user_id = ?', (str(user.id), ))
    xp = cur.fetchone()
    if xp is None :
        await context.channel.send('User <@{user_id}> is not registered, you need to have texted atleast once in the server to register yourself !'.format(user_id=int(user.id)))
    else :
        new_xp = int(set_level)**4
        cur.execute('UPDATE rankings SET xp ={new_xp} WHERE user_id = ? '.format(new_xp=new_xp), (str(user.id), ))
        new_level = int(int(int(xp[0]))**(1/4))       
        cur.execute('SELECT level FROM rankings WHERE user_id = ?', (str(user.id),))
        level = cur.fetchone()
        cur.execute('UPDATE rankings SET level = {new_level} WHERE user_id = ? '.format(new_level=new_level), (str(user.id), ))
        if new_level > int(level[0]) :
                channel = bot.get_channel(988718132841562112)
                await channel.send('Congratulations!! <@{user}> your have leveled up to **lvl.{level}**'.format(user=str(user.id), level=new_level))
        rank_list=[]
        rank_num = 0
        for rank_extract in cur.execute( 'SELECT level, user_id from rankings ORDER BY level') :
                rank_list.append(rank_extract)
                rank_num = rank_num + 1
        rank_list.sort(reverse=True)
        for i in range (rank_num ) :
                user_id = rank_list[i][1]
                new_rank = i + 1
                cur.execute('UPDATE rankings SET rank = {new_rank} WHERE user_id = ? '.format(new_rank=new_rank), (str(user.id), ))
        await context.channel.send('Succsesfully set level <@{user_id}> to {set_level} !'.format(user_id=int(user.id),set_level=set_level))
    conn.commit()
    cur.close()









@setlevel.error
async def setlevel_error(ctx, error):
        if isinstance(error,  MissingPermissions ):
            em = discord.Embed(title=f"Watch out !",description="This is a admin only command !", color=0xFF5733)
            await ctx.send(embed=em)

keep_alive()
token = os.environ['discord_token']
bot.run(token)