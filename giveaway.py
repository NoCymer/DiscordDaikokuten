import discord
from discord.ext import commands, tasks
import asyncio
import string
import datetime


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.guilds = True
guild = ""
giveaway_manager = ""
token = read_token()
client = commands.Bot(command_prefix='!', intents = intents)


async def fetch_guild():
    global guild
    global giveaway_manager
    guild = await client.fetch_guild(382597973084995584)


@commands.has_permissions(kick_members=True)
@client.command()
async def start_giveaway(ctx):
    def check(msg):
        return msg.author.id == ctx.author.id and msg.channel.id == ctx.channel.id

    await ctx.send("In which channel do you wanna do the giveaway ?")

    answermsg = await client.wait_for('message', check = check)
    channel = ""
    channel_id = ""
    for char in answermsg.content:
        if char != "<" and char != ">" and char != "#":
            channel_id += char
    channel = await client.fetch_channel(channel_id)
    await ctx.send("What will be the prize of the giveaway ?")
    giveaway_price = await client.wait_for('message', check = check)

    await ctx.send("What is the description of the giveaway ?")
    giveaway_description = await client.wait_for('message', check = check)

    await ctx.send("What is the requirements of the giveaway ?")
    giveaway_req = await client.wait_for('message', check = check)

    await ctx.send("How long will the giveaway last ? please use (1month or 1day or 1hr or 1min)")
    giveaway_date = await client.wait_for('message', check = check)
    d = "0"
    h = "0"
    mn = "0"
    if "day" in giveaway_date.content:
        d = ""
        for char in giveaway_date.content:
            if char not in list(string.ascii_lowercase):
                d += char
    elif "hr" in giveaway_date.content:
        h = ""
        for char in giveaway_date.content:
            if char not in list(string.ascii_lowercase):
                h += char
    elif "min" in giveaway_date.content:
        mn = ""
        for char in giveaway_date.content:
            if char not in list(string.ascii_lowercase):
                mn += char
    print(f"d:{d}")
    print(f"h:{h}")
    print(f"mn:{mn}")
    d = int(d)
    h = int(h)
    mn = int(mn)
    giveaway_date = datetime.datetime.now() + datetime.timedelta(days=d, hours=h, minutes=mn)

    embed = discord.Embed(
        title=f"🎉 {str(giveaway_price.content).lower().capitalize()} Giveaway! 🎉",
        description=f"{str(giveaway_description.content).lower().capitalize()} \n React with 🎉 to join the giveaway")
    embed.add_field(name=f"Requirements", value=f"{str(giveaway_req.content).capitalize()}")
    embed.add_field(name=f"Giveaway end date", value=f"{giveaway_date}")
    await channel.send(embed=embed)


@client.event
async def on_ready():
    print('------------------')
    print('Logged as :')
    print(client.user.name)
    print(client.user.id)
    print('------------------')
    await fetch_guild()
    

client.run(token)
