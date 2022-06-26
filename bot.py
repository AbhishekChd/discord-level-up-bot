import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
import aiosqlite
import random
import asyncio



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
    setattr(bot, "conn", await aiosqlite.connect("level.db"))
    setattr(bot, "cursor", bot.conn.cursor)
    # await asyncio.sleep(3)
    # if bot.db_con is None:
    #     print("bot.db_con is None")
    #     bot.db_con =  await aiosqlite.connect("level.db")1
    # print(bot)
    # print(bot.db)
    # print(bot.db.cursor)
    async with bot.cursor as cursor:
        await cursor.execute('CREATE TABLE IF NOT EXISTS levels(level INTEGER, xp INTEGER, user INTEGER, guild, INTEGER)')

 

@bot.command(aliases=['h'])
async def help(ctx: commands.Context):
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

@bot.event
async def message(message):
    if message.author.bot :
        return
    author = message.author
    guild = message.guild
    
    async with bot.cursor as cursor:
        await cursor.execute('SELECT xp FROM levels WHERE use = ? AND guild = ?', (author.id, guild.id,))
        xp = await cursor.fetchone()
        await cursor.execute('SELECT xp FROM levels WHERE use = ? AND guild = ?', (author.id, guild.id,))
        level = await cursor.fetchone()


        if not xp or not level :
            await cursor.execute('INSET INTO levels (level, xp, user, guild) VALUE (?,?,?,?)',(0, 0, author.id, guild.id,))
            await bot.commit()
        try :
            xp = xp[0]
            level = level[0]
        except TypeError:
            xp = 0 
            level = 0
        if level < 5 :
            xp += random.randint(1,3)
            await cursor.execute('INSET INTO levels (level, xp, user, guild) VALUE (?,?,?,?)',(xp, level, author.id, guild.id,))
        else :
            rand = random.randint(1, level//4)
            if rand == 1 :
                xp += random.randint(1,3)
                await cursor.execute('INSET INTO levels (level, xp, user, guild) VALUE (?,?,?,?)',(xp, level, author.id, guild.id,))
        if level >= 100:
                await cursor.execute('INSET INTO levels (level, xp, user, guild) VALUE (?,?,?,?)',( level, author.id, guild.id,))
                await cursor.execute('INSET INTO levels (level, xp, user, guild) VALUE (?,?,?,?)',(0, level, author.id, guild.id,))
                await message.channel.send(f'{author.mention} has leveled up to **{level}** !!')
    await bot.db.commit()



@bot.command(aliases=['r'])
async def rank(ctx: commands.Context, message = discord.user):
    #if message.mentions :
        #print("mention detected")
        #title_id = message.id
        #print("id retrieved")
   # else :
        #title_id = ctx.author
        #print("no mention")
    #async with bot.cursor as cursor :
        #await cursor.execute('SELECT xp FROM levels WHERE use = ? AND guild = ?', (member.id, ctx.id,))
        #xp = await cursor.fetchone()
        #await cursor.execute('SELECT xp FROM levels WHERE use = ? AND guild = ?', (member.id, ctx.id,))
        #level = await cursor.fetchone()
        #if not xp or not level :
            #await cursor.execute('INSET INTO levels (level, xp, user, guild) VALUE (?,?,?,?)',(0, 0, member.id, ctx.id))
            #await bot.commit()
        #try :
            #xp = xp[0]
            #level = level[0]
        #except TypeError:
            #xp = 0 
            #level = 0

    print("making embed")
    embed = discord.Embed(
        title= "*Server Rank of -* " + str(ctx.author) ,
        description= "**Your server rank increases as you chat, increase your rank to get high reward roles and flex on your friends** <:2940coolpepe:988766350430322738> ",
        colour=  0xFF5733
    )
    embed.add_field(name="Rank", value="12", inline=False)
    embed.add_field(name="Current level", value="10", inline=True)
    embed.add_field(name="xp", value="1200/3500", inline=True)
    embed.add_field(name="Awarded role", value="<role>", inline=False)
    embed.set_author(name=ctx.author,
    icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.set_image(url="https://i.imgur.com/cerqOld.gif")
    await ctx.send(embed=embed)
            
       


token = os.environ['discord-token']
bot.run(token)
