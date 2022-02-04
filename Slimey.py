from ast import alias
from lzma import PRESET_DEFAULT
from ntpath import altsep
import discord
from discord import embeds
from discord import colour
from discord import asset
from discord import message
from discord import channel
from discord import emoji
from discord import components
from discord.colour import Color
from discord.embeds import Embed
from discord.enums import Status
from discord.errors import ClientException
from discord.ext import commands, tasks
from discord.ui import Button, View
import json
from discord.ext.commands.bot import Bot
from discord.ext.commands.core import guild_only
from discord.ui import Button, View
from discord.utils import V
import requests
import random
from requests.models import Response
import datetime
import os
import sys
import string
import secrets
import asyncio
from discord.commands import Option
import time
import psutil
import platform
import shutil
from PIL import Image
from io import BytesIO
import typing
import socket
import sqlite3
import struct


# seting up the database

conn = sqlite3.connect("slimeybot.db")
curs = conn.cursor()


curs.execute(f"CREATE TABLE IF NOT EXISTS custom_prefixes (guild INT PRIMARY KEY NOT NULL, prefix TEXT)")
curs.execute(f"CREATE TABLE IF NOT EXISTS economy_responses (response TEXT, type INT)")
curs.execute(f"""
CREATE TABLE IF NOT EXISTS tags
(guild INT,
creator INT, creation_time INT,
current_owner INT,
last_edited INT,
last_edited_from INT,
name TEXT,
description TEXT,
aliases TEXT)""")
curs.execute("CREATE TABLE IF NOT EXISTS chatbot (serverID integer, channelID integer)")


def load_prefix(self,ctx):
    prefix = curs.execute(f"SELECT prefix FROM custom_prefixes WHERE guild IS {ctx.guild.id}").fetchone()
    if not prefix:
        pref = "<"
    else:
        pref = prefix
    return pref


bot = commands.Bot(command_prefix=load_prefix, help_command=None)
#opening the json file that contains the bot token and owner ID's

config_json = {"token":"","owners":[]}
if not os.path.exists('config.json'):
    with open ("config.json", 'w') as f:
        f.write(json.dumps(config_json, indent=4))
    
    print("WARNING: It looks like the configuration file does not exists. Please enter the Bot-Token and Owner IDs in the config.json file.")
    exit("Run the bot again after you entered the config values")

with open("config.json", 'r') as f:
    conf = json.load(f)
    
#start up of the bot

@bot.event
async def on_ready():
    
    #f"{len(bot.guilds)} servers | <help"
    # status=discord.Status.idle
    # await bot.change_presence(status=discord.Status.online, activity=discord.ActivityType.watching, name=f"{len(bot.guilds)} servers | <help")
    Bot_Status = f"{len(bot.guilds)} servers | <help"
    
    global members
    global stats
    global channels
    global start_time
    members = sum([guild.member_count for guild in bot.guilds])
    channels = 0
    for guild in bot.guilds:
        channels += len(guild.channels)
    stats = {"guilds": len(bot.guilds), "users": members, "channels": channels}
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=Bot_Status))
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Current stats:", stats)
    global bot_version
    bot_version = "6.9.1"
    global cpu_usage, ram_usage, python_version, os_system, os_release, disk_stats
    start_time = int(time.time())
    cpu_usage = psutil.cpu_percent(4)
    ram_usage = psutil.virtual_memory()[2]
    python_version = platform.python_version()
    os_system = platform.system()
    os_release = platform.release()
    total, used, free = shutil.disk_usage("/")
    disk_stats = f"**Disk** Total: %d GB" % (total // (2**30))+"\n Used: %d GB" % (used // (2**30)) + "\n Free: %d GB" % (free // (2**30))+"\n"
    print("All stats loaded\n----------")

    
    global bottleflipvar
    global megaflip

    bottleflipvar = random.randint(30, 80)
    megaflip = random.randint(20, 60)
    
    # initialization of cogs
    bot.load_extension('cogs.Economy')
    bot.load_extension('cogs.Tags')
    bot.load_extention('cogs.Chatbot')

    # uploading backup to cloud
    host = socket.gethostname()
    if host != 'pons': # if the bot didn't started from the server with the main database, do not create a backup.
        return
    else:
        try:
            print("Creating backup of database... (Uploading to cloud)")
            db_location = {'file': open('slimeybot.db' ,'rb')}
            resp = requests.post(f'https://transfer.sh/', files=db_location)
            print(f"Done: {resp.text}")
            backup = bot.get_channel(935981038415532060)
            em = discord.Embed(color=discord.Color.gold(), title="New backup!", description=f"**`Bot-Version:`** {bot_version}\n**`Hostname:`** {host}\n**`Created at:`** <t:{int(time.time())}:f>\nThis backup will stay in the cloud for 14 days.\nLink to the backup: {resp.text}")
            em.set_thumbnail(url="https://i.ibb.co/zGcnFhD/1635141.png")
            await backup.send(embed = em)
          
        except:
            print("Something went wrong. Backup could not be created.")
#sending a message when pinged

@bot.event
async def on_message(message):
    if message.content == "<@!915488552568123403>" or message.content == "<@915488552568123403>":
        prefix = curs.execute(f"SELECT prefix FROM custom_prefixes WHERE guild IS {message.guild.id}").fetchall()
        if not prefix:
            pref = "<"
        else:
            pref = prefix[0][0]
        await message.channel.send(f'My prefix is **`{pref}`**. Type "{pref}help" for all the commands!\n:bulb: **Tip:** you can use "{pref}prefix" to change my prefix in this server!')
    await bot.process_commands(message)
#defining all the important functions

def is_it_me(ctx):
    owners = conf["owners"]
    if ctx.author.id in owners:
        return ctx.author.id


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return(quote)


class Joke:
    setup = ""
    punchline = ""

    def __init__(self, setup, punchline):
        self.setup = setup
        self.punchline = punchline


def get_Joke():
    url = "https://dad-jokes.p.rapidapi.com/random/joke"
    headers = {
        'x-rapidapi-host': "dad-jokes.p.rapidapi.com",
        'x-rapidapi-key': "f54cc328d6msh97c78a7088ae219p185068jsn07d335d78fe6"
    }
    response = requests.request("GET", url, headers=headers)
    json_data = json.loads(response.text)
    setup = json_data["body"][0]["setup"]
    punchline = json_data["body"][0]["punchline"]
    joke = Joke(setup, punchline)
    return(joke)


#send a message when the bot joins a server

@bot.event
async def on_guild_join(guild): 
    
    embed = discord.Embed(color=discord.Color(0xC77FF3), title="Hey! I'm Slimey", description="Thanks for adding me to your server!\nType `<help` for commands and `<info` for some information on the bot and the owners of this bot!")
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/934713054678118500/9a79eebc8700d854ae683f7f2e8b1360.webp")
    embed.set_footer(icon_url="https://cdn.discordapp.com/avatars/934713054678118500/9a79eebc8700d854ae683f7f2e8b1360.webp", text="Slimey bot")
    try:
        joinchannel = guild.system_channel
        await joinchannel.send(embed=embed)
    except:
        await guild.text_channels[0].send(embed=embed)

#commands
@bot.command()
async def ping(ctx):
    em = discord.Embed(
        title="Pong !!", description=f"{round(bot.latency*1000)}ms", color=discord.Colour.blue())

    await ctx.reply(embed=em)


@bot.command(aliases=["ball", "8ball"])
async def magic8ball(ctx, *, question: str):

    responses = ["It is certain.",
                 "It is decidedly so.",
                 "Without a doubt.",
                 "Yes - definitely.",
                 "You may rely on it.",
                 "As I see it, yes.",
                 "Most likely.",
                 "Get out before I eat your cat",
                 "Yes.",
                 "Signs point to yes.",
                 "Reply hazy, try again.",
                 "Ask again later.",
                 "Cannot predict now.",
                 "Concentrate and ask again.",
                 "Don't count on it.",
                 "My reply is no.",
                 "My sources say no.",
                 "Very doubtful.",
                 "nerd",
                 "I AM TRYING TO SLEEP",
                 "idk",
                 "sorry I dont answer nerds"]

    await ctx.reply(f"Question: {question}\nAnswer: {random.choice(responses)}")


@bot.command(aliases=["yorn", "YorN"])
async def yesorno(ctx):

    responses = ["Yes.", "No.", "nerd", "probs", "prob yes",
                 "prob no", "idk nerd", "most prob yes", "most prob no"]

    await ctx.reply(random.choice(responses))


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):

    await ctx.channel.purge(limit=amount + 1)


@bot.command(aliases=["cointos", "cointoss", "flipcoin"])
@commands.cooldown(1, 10, commands.BucketType.user)
async def coinflip(ctx):
    x = random.randint(1, 2)

    if (x == 1):
        em = discord.Embed(
            title="Heads!", description="The coin fliped HEADS!", color=discord.Colour.green())
        em.set_thumbnail(url="https://i.postimg.cc/mkt4HwWN/Heads.jpg")

        await ctx.reply(embed=em)
    else:
        em = discord.Embed(
            title="Tails!", description="The coin fliped TAILS!", color=discord.Colour.green())
        em.set_thumbnail(url="https://i.postimg.cc/DZCF0NHw/Tails.jpg")

        await ctx.reply(embed=em)


@bot.command()
async def dadjoke(ctx):
    joke = get_Joke()
    sending_joke = joke.setup + "." + joke.punchline

    await ctx.reply(sending_joke)


@bot.command()
async def inspire(ctx):
    quote = get_quote()
    await ctx.reply(quote)

@bot.command()
async def twitch(ctx):
    await ctx.reply("GO FOLLOW ME ON TWITCH RIGHT NOW: https://www.twitch.tv/theslimeydevloper")


@bot.command()
async def youtube(ctx):
    await ctx.reply("The youtube channel of TheSlimeyDevloper is - https://www.youtube.com/channel/UCH-QFhiX-G8FFjQp8oL9_2A SO GO SUB!")


@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def bottleflip(ctx):
    y = random.randint(1, 101)
    z = random.randint(1, 101)

    if (z < megaflip):
        em = discord.Embed(title="Triple Mega Flip!",
                           description="Wait it can't be.....**YOU JUST GOT THE TRIPPLE MEGA FLIP!!**The bottle landed on its cap after it fliped **THRICE**!!", color=discord.Colour.blue())
        await ctx.reply(embed=em)

    else:
        if (y < bottleflipvar):
            em = discord.Embed(
                title="Bottle Fliped!", description="THE BOTTLE FLIPED AND FELL UP RIGHT! Bravo!", color=discord.Colour.green())

            await ctx.reply(embed=em)

        else:
            em = discord.Embed(title="Bottle did not flip...",
                               description="The bottle did not fall upright...Better luck next time!", color=discord.Colour.red())

            await ctx.reply(embed=em)


@bot.command(aliases=["about", "botinfo", "bot"])
@commands.cooldown(1, 10, commands.BucketType.user)

async def info(ctx):
    info = (f"Information on the bot: This bot was made using VS Code using the language Python. It's maintained by `TheSlimeyDev_YT#8584`.\n**Our website:** <https://www.slimey.tk>\n"
    f':information_source: __**Stats**__\n\nTotal users: {stats["users"]}\nTotal channels: {stats["channels"]}\nGuilds: {stats["guilds"]}\n--------------------\n'
    
    f"**Last restarted** <t:{start_time}:R>\n"
    f"**CPU usage** {cpu_usage}%\n"
    f"**RAM usage** {ram_usage}%\n"
    f"{disk_stats}\n"
    f"**Python-Version** {python_version}\n"
    f"**Bot-Version** {bot_version}\n"
    f"**OS info** {os_system} {os_release}\n\n"
    f"**API connection ping** {round(bot.latency * 1000)}ms\n\n"
    f":information_source: **Note:** Because of performance reasons, the most stats are last updated on <t:{start_time}>."
    )
    
    await ctx.reply(info)

@bot.command()
@commands.check(is_it_me)
async def stats(ctx):
    await ctx.message.add_reaction('🔄')
    members = sum([guild.member_count for guild in bot.guilds])
    channels = 0
    for guild in bot.guilds:
        channels += len(guild.channels)
    
    stats = {"guilds": len(bot.guilds), "users": members, "channels": channels}
    total, used, free = shutil.disk_usage("/")
    disk_stats = f"**Disk**"+"\n"+"Total: %d GiB" % (total // (2**30))+"\n Used: %d GiB" % (used // (2**30)) + "\n Free: %d GiB" % (free // (2**30))+"\n"

    info = (f'__**CURRENT Stats**__\n\nTotal users: {stats["users"]}\nTotal channels: {stats["channels"]}\nGuilds: {stats["guilds"]}\n--------------------\n'
    
    f"**Last restarted** <t:{start_time}:R>\n"
    f"**CPU usage** {psutil.cpu_percent(4)}%\n"
    f"**RAM usage** {psutil.virtual_memory()[2]}%\n"
    f"{disk_stats}\n"
    f"**Python-Version** {platform.python_version()}\n"
    f"**Bot-Version** {bot_version}\n"
    f"**OS info** {platform.system()} {platform.release()}\n\n"
    f"**API connection ping** {round(bot.latency * 1000)}ms"
    )
    
    await ctx.send(info)
    await ctx.message.remove_reaction("🔄", bot.user)


@bot.command()
async def help(ctx, mode: typing.Optional[str]):
    prefix = curs.execute(f"SELECT prefix FROM custom_prefixes WHERE guild IS {ctx.guild.id}").fetchall()
    if not prefix:
        show_prefix = "<"
    else:
        show_prefix = prefix[0][0]
    if mode == None:
        em = discord.Embed(title="Current commands:", description=f"`{show_prefix}help fun`, `{show_prefix}help moderation`, `{show_prefix}help minigame`, `{show_prefix}help utility`, `{show_prefix}help chatbot`, `{show_prefix}help economy`, `{show_prefix}help tags`", color = discord.Color.gold())
        em.add_field(name="Prefix", value=f"My prefix on this server is currently '`{show_prefix}`'. To change it, use the command `{show_prefix}prefix`.", inline=False)
        em.add_field(name="Support server", value="[Click here](https://discord.gg/eHteZEmfXe)", inline=False)
        em.add_field(name="website", value="[Click here](https://www.slimey.tk/)", inline=False)
        await ctx.reply(embed=em)
    else:
        if mode == "fun":
            em = discord.Embed(title="😂 Fun commands:", description=f"`{show_prefix}dadjoke`\n`{show_prefix}inspire`\n`{show_prefix}magic8ball`\n`{show_prefix}yesorno`\n`{show_prefix}sayweird`\n`{show_prefix}say`\n`/send_meme`\n`/send_password`\n`{show_prefix}rip`\n`{show_prefix}kill`\n`{show_prefix}ping`\n`{show_prefix}fox`\n`{show_prefix}foxshow`\n`{show_prefix}hack`\n`{show_prefix}ip`", color=discord.Color.green())
    
            await ctx.reply(embed=em)
        
        elif mode == "moderation":
            em = discord.Embed(title="🔒 Moderation commands:", description=f"`{show_prefix}kick`\n`{show_prefix}ban`\n`/timeout`\n`{show_prefix}clear`\n`{show_prefix}slowmode`", color=discord.Color.red())
            
            await ctx.reply(embed=em)
        
        elif mode == "minigame":
            em = discord.Embed(title="🎲 Minigames commands:", description = f"`{show_prefix}coinflip`\n`{show_prefix}bottleflip`\n`{show_prefix}rps`\n`{show_prefix}odds`", color=discord.Color.blue())
    
            await ctx.reply(embed=em)
        
        elif mode == "utility":
            em = discord.Embed(title="👀 Utility/other commands:", description=f"`{show_prefix}youtube`\n`{show_prefix}twitch`\n`{show_prefix}invite`\n`{show_prefix}report`\n`{show_prefix}info`\n`{show_prefix}weather`\n`{show_prefix}avatar`\n`{show_prefix}countdown`\n`{show_prefix}discord`", color=discord.Color.purple())
    
            await ctx.reply(embed=em)
        elif mode == "chatbot":
            em = discord.Embed(title="💬 Chatbot commands:", description="*Coming soon!*", color=discord.Color.dark_orange())
    
            await ctx.reply(embed=em)
        elif mode == "economy":
            em = discord.Embed(title="💰 Economy commands:", description=f"*Note: these are beta commands.*\n{show_prefix}work", color=discord.Color.dark_magenta())
    
            await ctx.reply(embed=em)
        elif mode == "tags":
            em = discord.Embed(title="#️⃣ Tag commands:", description=f"*Note: This is a beta feature.*\n`{show_prefix}tag_create`\n`{show_prefix}tag_edit`\n`{show_prefix}tag`", color=discord.Color.dark_teal())
    
            await ctx.reply(embed=em)
@bot.command()
async def invite(ctx):
    await ctx.reply("Heaad over to https://slimey.tk and invite our bot!")


@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def rps(ctx, response=None):
    if response == "rock" or response == "paper" or response == "scissor" or response == "scissors":

        botRes = random.choice(["rock", "paper", "scissor"])
        await ctx.reply(botRes)

        if botRes == response:
            await ctx.send("ITS A TIE!")
        elif botRes == "rock" and response == "paper":
            await ctx.send("You win!")
        elif botRes == "paper" and response == "rock":
            await ctx.send("I win!")
        elif botRes == "scissor" and response == "rock":
            await ctx.send("You win!")
        elif botRes == "rock" and response == "scissor":
            await ctx.send("I win!")
        elif botRes == "rock" and response == "scissors":
            await ctx.send("I win!")
        elif botRes == "paper" and response == "scissors":
            await ctx.send("You win!")
        elif botRes == "scissor" and response == "paper":
            await ctx.send("I win!")

    else:
        em = discord.Embed(
            title="<:Slimey_x:933232568055267359> Oops!", description="Invalid respons! Please type a response that contains rock, paper, scissor and remember its case sensitive!", color=discord.Color.red())
        await ctx.reply(embed=em)


@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def report(ctx):
    em = discord.Embed(title="Report problems!", url="https://forms.gle/zwioTfRoErEZfTim6",
                       description="Click the title to report a bug/problem!", color=discord.Color.gold())
    await ctx.reply(embed=em)


@bot.command()
async def odds(ctx):

    em = discord.Embed(title="channces of getting bottle flip -", description="Normal bottle flip - " + str(
        bottleflipvar) + " in 100\nTriple mega bottle flip - " + str(megaflip) + " in 100", color=discord.Color.gold())
    em.add_field(name="These odds will randomize every 12 hours",
                 value="To make it a little bit more fun the bottleflip chances will randomize every 12 hours!", inline=False)

    await ctx.reply(embed=em)


@bot.command()
async def say(ctx, *, message: str = None):

    if message == None:
        await ctx.send("<:Slimey_x:933232568055267359> Please enter a message to send!")
    
    else:
        await ctx.message.delete()
        await ctx.send(message, allowed_mentions=discord.AllowedMentions.none())


@bot.command()
async def password(ctx):
    await ctx.reply("<:slash:928599693984944138> Please use the **slash command**! (`/send_password`)")

# slash command version of <password:


@bot.slash_command()
async def send_password(ctx, length):
    length = int(length)
    if length <= 100:
        if length < 4:
            embed = discord.Embed(
                title="Error", color=discord.Colour.red(), description=f"Too small... :joy:")
            await ctx.respond(embed=embed)
            return
        chars = string.digits + string.ascii_letters + string.punctuation

        passwords = []

        for i in range(5):
            password = ''.join(secrets.choice(chars) for _ in range(length))
            passwords.append(password)

        embed = discord.Embed(title="Generated passwords", color=discord.Colour.blue(), description=f"I generated **5** passwords for you, which are **{length}** characters long.\n\n"
                              f"```txt\n{passwords[0]}\n{passwords[1]}\n{passwords[2]}\n{passwords[3]}\n{passwords[4]}```")

        await ctx.respond(embed=embed)
    else:
        embed = discord.Embed(title="<:Slimey_x:933232568055267359> Error", color=discord.Colour.red(
        ), description=f"Please don't go higher than 100!")
        await ctx.respond(embed=embed)


@bot.slash_command()
async def send_meme(ctx):
    url = "https://meme-api.herokuapp.com/gimme/memes"
    resp = requests.get(url=url)
    meme_json = resp.json()
    random_meme = meme_json["url"]

    meme_subreddit = meme_json["subreddit"]
    meme_author = meme_json["author"]
    meme_title = meme_json["title"]
    meme_link = meme_json["postLink"]
    meme_upvotes = meme_json["ups"]
    if meme_upvotes > 1000:
        meme_upvotes = round(meme_json["ups"], -3)

    api_meme = discord.Embed(title="Meme", colour=discord.Colour.blue(), description=(f"**`Subreddit`** „r/{meme_subreddit}“\n**`Title`** „[{meme_title}]({meme_link})“\n\n"
                                                                                      f"**`Post-Creator`** „{meme_author}“\n**`Upvotes`** {meme_upvotes}"), timestamp=datetime.datetime.now())
    api_meme.set_image(url=random_meme)
    await ctx.respond(embed=api_meme)
    m = await ctx.interaction.original_message()
    await m.add_reaction("👍")
    await m.add_reaction("👎")


@bot.command()
async def meme(ctx):
    await ctx.reply("<:slash:928599693984944138> Please use the **slash command**! (`/send_meme`)")


@bot.command()
@commands.check(is_it_me)
async def test(ctx):
    button = Button(label="Test button!", style=discord.ButtonStyle.green, emoji="👋")
    button2 = Button(emoji="😊")
    button3 = Button(label="red", style=discord.ButtonStyle.red)
    button4 = Button(label="my yt", url="https://www.youtube.com/channel/UCH-QFhiX-G8FFjQp8oL9_2A")

    view = View()
    view.add_item(button)
    view.add_item(button2)
    view.add_item(button3)
    view.add_item(button4)

    await ctx.send("Test button command!", view = view)


@bot.command()
@commands.check(is_it_me)
async def modapps(ctx):
    await ctx.send("Mod apps are now **OPEN**: https://forms.gle/kDBwcC8BQHe2YQkX9")


@bot.slash_command(pass_context=True)
async def timeout(ctx, target: Option(discord.Member, "The member you want to timeout"), time: Option(int, "Time you want to time them out for"), time_unit: Option(str, "Time unit", choices=["s", "min", "h", "d"]),  reason: Option(str, "Reason", required=False, default="No reason was specified.")):
    if not ctx.author.guild_permissions.moderate_members:
        await ctx.respond("<:Slimey_x:933232568055267359> You have no permission to timeout members!", ephemeral=True)
        return

    duration = None
    time_unit_text = None

    if time_unit == "s":
        duration = time * 1
        time_unit_text = "Second(s)"
    elif time_unit == "min":
        duration = time * 60
        time_unit_text = "Minute(s)"
    elif time_unit == "h":
        duration = time * 3600
        time_unit_text = "Hour(s)"
    elif time_unit == "d":
        duration = time * 86400
        time_unit_text = "Day(s)"

    time_to_timeout = datetime.timedelta(seconds=duration)
    try:
        await target.timeout_for(time_to_timeout, reason=reason)
    except discord.HTTPException:
        await ctx.respond("I don't have the permission to do that.", ephemeral=True)
        return

    timeout_embed = discord.Embed(
        title=f"Timed {target} out", color=discord.Colour.blue())
    timeout_embed.add_field(
        name="Server", value=f"{ctx.guild.name}", inline=True)
    timeout_embed.add_field(
        name="Responsible moderator", value=f"<@{ctx.author.id}>", inline=True)
    timeout_embed.add_field(
        name="Target", value=f"<@{target.id}>", inline=True)
    timeout_embed.add_field(
        name="Time", value=f"{time} {time_unit_text}", inline=True)
    timeout_embed.add_field(
        name="Reason", value=f"```{reason}```", inline=True)

    await ctx.respond(embed=timeout_embed)

    try:
        timeout_embed = discord.Embed(
            title=f"You have been timed out!", description=f"You have been timed-out on {ctx.guild.name} for {time} {time_unit_text}!\nReason: ```{reason}```", color=discord.Colour.blue())
        await target.send(embed=timeout_embed)
    except discord.errors.DiscordException:
        pass

    await asyncio.sleep(duration)
    try:
        timeout_over_embed = discord.Embed(
            title=f"Your timeout has expired", description=f"Your timeout on {ctx.guild.name} for {time} {time_unit_text} has expired.", color=discord.Colour.blue())
        await target.send(embed=timeout_over_embed)
    except discord.errors.DiscordException:
        pass



@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member = None, *, reason=None):

    if member==None:
        await ctx.reply("<:Slimey_x:933232568055267359> Please specify a member to kick")
    
    else:

        if reason==None:

            reason="No reason was specified"

        await ctx.guild.kick(member)
        
        em = discord.Embed(title = f"<:Slimey_tick:933232568210436136> Kicked successfully", color = discord.Color.green())
        em.add_field(name = "Member", value = f"Name: {member.name}" + "\n" + f"ID: {member.id}")
        em.add_field(name = "Reason", value = f"{reason}")
        
        await ctx.send(embed = em)


@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member = None, *, reason = None):

    if member==None:
        await ctx.reply("<:Slimey_x:933232568055267359> Please specify a member to ban")
    
    else:

        if reason==None:

            reason="No reason was specified"
            
        await member.ban(reason = reason)

        em = discord.Embed(title = f"<:Slimey_tick:933232568210436136> Banned successfully", color = discord.Color.green())
        em.add_field(name = "Member", value = f"Name: {member.name}" + "\n" + f"ID: {member.id}")
        em.add_field(name = "Reason", value = f"{reason}")

        await ctx.send(embed = em)


@bot.command()
async def vote(ctx):

    button = Button(label="Top.gg", url="https://top.gg/bot/915488552568123403/vote")

    view = View()
    view.add_item(button)

    await ctx.reply("Vote this bot on top.gg!", view = view)

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)

async def rip(ctx, target: discord.Member = None):
    if target == None:
        target = ctx.author
    rip = Image.open("rip.jpg")
    asset = target.avatar
    data = BytesIO(await asset.read())
    pic = Image.open(data)
    pic = pic.resize((213, 213))
    rip.paste(pic, (337, 215))
    rip.save("rip_gen.jpg")
    await ctx.send(file = discord.File("rip_gen.jpg", filename="rip.jpg"))


@bot.command()
async def kill(ctx, target: discord.Member = None):
    if target == None:
        target = ctx.author
    
    kill = [
        " choked on a lego and died",
        " stepped on a lego and died",
        " died when they were writing their death note",
        " died.",
        " choked on a carrot and died",
        " died eating expired choclate",
        " tripped and died",
        " died due to WiLd DoG AtAcK",
        " died because they were looking at the microwave while cooking burrito's",
        " drowned to death ",
        " died because there mom killed them",
        " died because of shame",
        " died due to cold",
        " died because they were noob",
        " died after he found out he was alergic to air"
    ]

    message = f"{target}{random.choice(kill)}"

    await ctx.send(message)

@bot.command()
async def weather(ctx, location = None):
    if location == None:
        await ctx.message.add_reaction('❌')

        await ctx.send("Please include a location, friend!")
        return

    response = requests.get(f"https://pixel-api-production.up.railway.app/data/weather/?location={location}")
    json_data = json.loads(response.text)
    if "error" in json_data:
        await ctx.message.add_reaction('❌')
        if json_data["error"] == "Location not found":
            await ctx.send("I didn't found that city/location.")
        else:
            await ctx.send("Unknown Error. :person_shrugging:")
        return

    await ctx.message.add_reaction('🔄')
    resp_location = json_data["info"]["location"]
    resp_country = json_data["info"]["country"]
    #resp_region = json_data["info"]["region"]
    resp_temp = json_data["weather"]["temp_c"]
    resp_temp_feel = json_data["weather"]["feels_c"]
    resp_desc = json_data["weather"]["condition"]
    resp_ico = json_data["weather"]["icon"]

    if float(resp_temp_feel) <4:
        color = 0x153db0
    elif float(resp_temp_feel) <4:
        color = 0x3a80d3
    elif float(resp_temp_feel) <8:
        color = 0x3ad3c5
    elif float(resp_temp_feel) <15:
        color = 0xf0da3d
    elif float(resp_temp_feel) <20:
        color = 0xf08e3d
    elif float(resp_temp_feel) <25:
        color = 0xf0633d
    elif float(resp_temp_feel) <30:
        color = 0xf31106
    elif float(resp_temp_feel) <35:
        color = 0xc40900
    embed = discord.Embed(color=discord.Colour(color), title=f"Weather in {resp_location} ({resp_country})", description=f"**`Temperatur`:** {resp_temp} °C\n"
    f"**`Feels like`:** {resp_temp_feel} °C\n"
    f"**`Description`:** {resp_desc}\n\nWind and humidity coming soon!")
    embed.set_thumbnail(url=resp_ico)
    embed.set_footer(icon_url=ctx.author.avatar.url, text=f"Requested by {ctx.author.name}")

    await ctx.send(embed=embed)
    await ctx.message.remove_reaction('🔄', bot.user)

@bot.command(aliases=["pref", "setprefix", "changeprefix"])
@commands.cooldown(1, 5, commands.BucketType.user)
@commands.has_permissions(kick_members=True)
async def prefix(ctx,*, pref=None):
    # await ctx.send("This command is currently unavailable!")
    check = curs.execute(f"SELECT * FROM custom_prefixes WHERE guild IS {ctx.guild.id}").fetchall()
    
    if not check:
        
        curs.execute(f"INSERT INTO custom_prefixes(guild) VALUES({ctx.guild.id})")
        conn.commit()

    if pref == None:
        await ctx.send("Please add a prefix!")
        return
    if len(pref) > 3:
        await ctx.send("Prefixes can't be longer than 3 characters.")
        return
    new_prefix = pref
    em = discord.Embed(color=discord.Color.red(), title="Prefix change", description=f"The prefix on this server is now **`{new_prefix}`**.")
    await ctx.send(embed=em)
    curs.execute(f"INSERT OR REPLACE INTO custom_prefixes(guild,prefix) VALUES({ctx.guild.id},'{new_prefix}')")
    conn.commit()

@bot.command(aliases=["weird", "weirdify", "upper_lower", "ul", "kek", "weirdsay"])
async def sayweird(ctx, *, message: str = None):
    if message == None:
        await ctx.send("<:Slimey_x:933232568055267359> Please enter a message to send!")
    
    else:
        await ctx.message.delete()
        message = "".join([x.upper() if i % 2 != 0 else x for i, x in enumerate(message)])

        await ctx.send(message, allowed_mentions=discord.AllowedMentions.none())

@bot.command(aliases=["randomfox"])
@commands.cooldown(1, 3, commands.BucketType.user)

async def fox(ctx):
    response = requests.get("https://randomfox.ca/floof/")
    json_data = json.loads(response.text)
    fox_image_url = json_data["image"]
    fox_link = json_data["link"]
    em = discord.Embed(color=discord.Colour(0xE97451), title="Random fox!", url=fox_link)
    em.set_image(url=fox_image_url)
    await ctx.send(embed=em)


@bot.command(aliases=["megafox", "ultrafox", "foxslideshow"])
@commands.cooldown(1, 18, commands.BucketType.user)
async def foxshow(ctx):
    response1 = requests.get("https://randomfox.ca/floof/")
    json_data1 = json.loads(response1.text)
    fox_image_url1 = json_data1["image"]
    fox_link1 = json_data1["link"]

    response2 = requests.get("https://randomfox.ca/floof/")
    json_data2 = json.loads(response2.text)
    fox_image_url2 = json_data2["image"]
    fox_link2 = json_data2["link"]

    response3 = requests.get("https://randomfox.ca/floof/")
    json_data3 = json.loads(response1.text)
    fox_image_url3 = json_data3["image"]
    fox_link3 = json_data3["link"]

    response4 = requests.get("https://randomfox.ca/floof/")
    json_data4 = json.loads(response4.text)
    fox_image_url4 = json_data4["image"]
    fox_link4 = json_data4["link"]

    response5 = requests.get("https://randomfox.ca/floof/")
    json_data5 = json.loads(response5.text)
    fox_image_url5 = json_data5["image"]
    fox_link5 = json_data5["link"]


    em1 = discord.Embed(color=discord.Colour(0xE97451), title="Fox show (1/5)", url=fox_link1)
    em1.set_image(url=fox_image_url1)
    
    em2 = discord.Embed(color=discord.Colour(0xE97451), title="Fox show (2/5)", url=fox_link2)
    em2.set_image(url=fox_image_url2)
    
    em3 = discord.Embed(color=discord.Colour(0xE97451), title="Fox show (3/5)", url=fox_link3)
    em3.set_image(url=fox_image_url3)
    
    em4 = discord.Embed(color=discord.Colour(0xE97451), title="Fox show (4/5)", url=fox_link4)
    em4.set_image(url=fox_image_url4)
    
    em5 = discord.Embed(color=discord.Colour(0xE97451), title="Fox show (5/5)", url=fox_link5)
    em5.set_image(url=fox_image_url5)

    m = await ctx.send(embed=em1)
    await asyncio.sleep(3)
    await m.edit(embed=em2)
    await asyncio.sleep(3)
    await m.edit(embed=em3)
    await asyncio.sleep(3)
    await m.edit(embed=em4)
    await asyncio.sleep(3)
    await m.edit(embed=em5)
    await ctx.send(":fox: = :smiling_face_with_3_hearts:")


@bot.command(aliases = ["sm"])
@commands.cooldown(1, 5, commands.BucketType.user)
@commands.has_permissions(manage_messages=True)
async def slowmode(ctx, seconds: int = 0):

    if seconds > 21600:
        
        await ctx.reply("The limit for slow mode is 21600 seconds(6 hours)!")

    else:

        if seconds == 0:
            await ctx.channel.edit(slowmode_delay=seconds)
            await ctx.reply("Reset slow mode to 0 seconds!")
        
        else:
            await ctx.channel.edit(slowmode_delay=seconds)
            await ctx.send(f"Set the slowmode in this channel to {seconds} seconds!")

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def avatar(ctx, target: discord.Member = None):
    if target == None:
        target = ctx.author

        
    em = discord.Embed(title = f"{target.name}'s Avatar")
    em.set_footer(icon_url=ctx.author.avatar.url, text=f"Requested by {ctx.author.name}")
    em.set_image(url=target.avatar.url)
    await ctx.send(embed = em)

@bot.command()
@commands.cooldown(1, 35, commands.BucketType.user)
@commands.has_permissions(manage_messages=True)
async def countdown(ctx, count=10):
    if count > 30:
        await ctx.send("The maximum allowed value is 30.")
        return
    current_count = count+1

    for i in range(count):
        current_count += -1
        await ctx.send(str(current_count))
        await asyncio.sleep(1)
    await ctx.send("**0**")

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def hack(ctx, member : discord.Member = None):

    if member == None:
        await ctx.send("Please include the member you want to hack.")

    else:
        most_used_word = ["Chungus", "Big Chungus", "Me is nerd", "I like pinapples on pizzas", "I like homework"]
        most_used_app = ["Discord", "Facebook(damn what a dweeb)", "Instagram", "Twitter", "Tik Tok"]

        files = random.randint(2000,10000)
        em = discord.Embed(title = f"Hacking {member}.", description = f"hacking computer...({files} files)")
        word = random.choice(most_used_word)
        em2 = discord.Embed(title = f"Hacking {member}..", description = f"hacking epic games, roblox and minecraft account...(most used word in chat: {word})")
        app = random.choice(most_used_app)
        locations = ["Nerd island", "Stupid island", "parents house", "basement of a serial killer", "in space"]
        location_of_user = random.choice(locations)
        em3 = discord.Embed(title = f"Hacking {member}...", description = f"hacking their phone...(most used app: {app})")
        em4 = discord.Embed(title = f"Hacking {member}..", description = f"hacking their location...(location: {location_of_user})")
        em5 = discord.Embed(title = f"Succesfully hacked {member}!", description = f"Most used app: {app}\nMost used word: {word}\nlocation: ||{location_of_user}||")

        m = await ctx.reply(embed=em)
        await asyncio.sleep(random.randint(4, 6))
        await m.edit(embed = em2)
        await asyncio.sleep(random.randint(3, 6))
        await m.edit(embed = em3)
        await asyncio.sleep(random.randint(5, 8))
        await m.edit(embed = em4)
        await asyncio.sleep(random.randint(6, 9))
        await m.edit(embed = em5)


@bot.command(aliases=["economy_add", "response", "add_response"])
@commands.check(is_it_me)
async def eco_add(ctx, type = None, *,response = None):
    if type == "good" or "bad":
        if response == None:

            em = discord.Embed(color=discord.Color.dark_red(), title="Syntax Error", description="Please include a response AFTER the type.")
            await ctx.send(embed=em)
            return
        m = await ctx.send(f'I will add the response "{response}" with the type "{type}".\nStatus: In progress')
        if type == 'good':
            dbtype = 1
        if type == 'bad':
            dbtype = 2

        curs.execute(f"INSERT INTO economy_responses VALUES ('{response}', {dbtype})")
        conn.commit()
        await m.edit(f'I will add the response "{response}" with the type "{type}".\nStatus: Done, it\'s now in the database.')
    else:
        em = discord.Embed(color=discord.Color.dark_red(), title="Syntax Error", description="Please include a type BEFORE the response.")
        await ctx.send(embed=em)
        #error handling
@commands.cooldown(1, 90, commands.BucketType.user)

@bot.command(aliases=["get_ip"])
async def ip(ctx, member: discord.Member = None):
    if member == None:
        await ctx.send("Please specify a member to get its ip address.")
        return
    elif member == ctx.author:
        await ctx.send("Please specify a member to get its ip address.")
        return
    generated_ip = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
    m = await ctx.send("Starting IP grabber tool...")
    await asyncio.sleep(random.uniform(1, 2.5))
    await m.edit(f"Starting IP grabber tool... :white_check_mark:\nSending request to {member.id}...")
    await asyncio.sleep(random.uniform(0.5, 1.8))
    await m.edit(f"Starting IP grabber tool... :white_check_mark:\nSending request to {member.id}... :x: HTTP 403: _REQUEST DENIED_")
    await asyncio.sleep(random.uniform(0.6, 0.6))
    await m.edit(f"Starting IP grabber tool... :white_check_mark:\nSending request to {member.id}... :x: HTTP 403: _REQUEST DENIED_\nSearching opened ports...")
    await asyncio.sleep(random.uniform(0.9, 2.3))
    port = random.randint(0,3000)
    await m.edit(f"Starting IP grabber tool... :white_check_mark:\nSending request to {member.id}... :x: HTTP 403: _REQUEST DENIED_\nSearching opened ports... :white_check_mark:\nSuccess! Port **{port}**")
    await asyncio.sleep(random.uniform(0.5, 1.95))
    await m.edit(f"Starting IP grabber tool... :white_check_mark:\nSending request to {member.id}... :x: HTTP 403: _REQUEST DENIED_\nSearching opened ports... :white_check_mark:\nSuccess! Port **{port}**\nFetching IP...")
    await asyncio.sleep(random.uniform(0.5, 3.95))
    i = random.randint(1,4)
    if i != 4:
        await m.edit(f"Starting IP grabber tool... :white_check_mark:\nSending request to {member.id}... :x: HTTP 403: _REQUEST DENIED_\nSearching opened ports... :white_check_mark:\nSuccess! Port **{port}**\nFetching IP... :white_check_mark:\n**Result:** {member.name}'s IP is: `{generated_ip}`")
    else:
        await m.edit(f"Starting IP grabber tool... :white_check_mark:\nSending request to {member.id}... :x: HTTP 403: _REQUEST DENIED_\nSearching opened ports... :white_check_mark:\nSuccess! Port **{port}**\nFetching IP... :x:\n**FATAL ERROR** Something went wrong. The firewall blocked my `GET` request. Try again in some seconds.")

@bot.command(aliases=["discord", "isdiscorddown", "discorddown"])
@commands.cooldown(1, 3, commands.BucketType.user)
async def discordstatus(ctx):
    response = requests.get("https://discordstatus.com/api/v2/status.json")
    json_data = response.json()
    status = json_data["status"]["description"]
    if status == "All Systems Operational":
        color = 0xA9F37F
        text = f"Yeah! Discord works! – {status}"
    else:
        color = 0xF37F7F
        text = f"It looks like something is not working at the moment:\n{status}"
    em = discord.Embed(colour=discord.Colour(color), title="Discord Status", description=text)
    em.set_thumbnail(url="https://i.ibb.co/0Cz6QWz/Discord.png")
    await ctx.reply(embed=em, mention_author=False)

@discordstatus.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"<:Slimey_x:933232568055267359> Slow it down bro!",
                           description=f"Try again in {error.retry_after:.2f}s.", color=discord.Colour.red())
        await ctx.send(embed=em)

@ip.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"<:Slimey_x:933232568055267359> Slow it down bro, I'm still learning hacking!",
                           description=f"You can hack someone again in {error.retry_after:.2f}s.", color=discord.Colour.red())
        await ctx.send(embed=em)

@hack.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"<:Slimey_x:933232568055267359> Slow it down bro, I'm still learning hacking!",
                           description=f"You can hack someone again in {error.retry_after:.2f}s.", color=discord.Colour.red())
        await ctx.send(embed=em)

@avatar.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"<:Slimey_x:933232568055267359> Slow it down bro!",
                           description=f"Try again in {error.retry_after:.2f}s.", color=discord.Colour.red())
        await ctx.send(embed=em)

@countdown.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"<:Slimey_x:933232568055267359> Slow it down bro!",
                           description=f"Try again in {error.retry_after:.2f}s.", color=discord.Colour.red())
        await ctx.send(embed=em)

@fox.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"<:Slimey_x:933232568055267359> Slow it down bro!",
                           description=f"Try again in {error.retry_after:.2f}s.", color=discord.Colour.red())
        await ctx.send(embed=em)
@foxshow.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"<:Slimey_x:933232568055267359> Slow it down bro!",
                           description=f"Try again in {error.retry_after:.2f}s.", color=discord.Colour.red())
        await ctx.send(embed=em)


@bottleflip.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"<:Slimey_x:933232568055267359> Slow it down bro!",
                           description=f"Try again in {error.retry_after:.2f}s.", color=discord.Colour.red())
        await ctx.send(embed=em)

@prefix.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"<:Slimey_x:933232568055267359> Slow it down bro!",
                           description=f"Try again in {error.retry_after:.2f}s.", color=discord.Colour.red())
        await ctx.send(embed=em)



@report.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"<:Slimey_x:933232568055267359> Slow it down bro!",
                           description=f"Try again in {error.retry_after:.2f}s.", color=discord.Colour.red())
        await ctx.send(embed=em)


@rps.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"<:Slimey_x:933232568055267359> Slow it down bro!",
                           description=f"Try again in {error.retry_after:.2f}s.", color=discord.Colour.red())
        await ctx.send(embed=em)


@coinflip.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"<:Slimey_x:933232568055267359> Slow it down bro!",
                           description=f"Try again in {error.retry_after:.2f}s.", color=discord.Colour.red())
        await ctx.send(embed=em)
@info.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"<:Slimey_x:933232568055267359> Slow it down bro!",
                           description=f"Try again in {error.retry_after:.2f}s.", color=discord.Colour.red())
        await ctx.send(embed=em)
@rip.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"<:Slimey_x:933232568055267359> Slow it down bro!",
                           description=f"Try again in {error.retry_after:.2f}s.", color=discord.Colour.red())
        await ctx.send(embed=em)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):

        em = discord.Embed(title="<:Slimey_x:933232568055267359> Permission Error",
                           description="You don't have the permission(s) to do that!", color=discord.Colour.red())

        await ctx.reply(embed=em)



bot.run(conf["token"])
conn.close()