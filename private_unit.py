from random import randint, choice
import discord
from discord.embeds import Embed
import requests
from discord.ext import commands, tasks
import asyncio
from discord.ext.commands import *
from assets import news_api, nsfw_api
from discord_components import *
import mal
from discord.utils import get
from discord_slash import *
from discord_slash.utils.manage_commands import create_option
from discord_components.button import Button, ButtonStyle


guild_ids = [382597973084995584]
TIME_CONST = 10

def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()
client = commands.Bot(command_prefix='!')
slash = SlashCommand(client, sync_commands=True)
ddb = DiscordComponents(client)

async def wait_and_delete_msgs(ctx, bot_msg):
    await asyncio.sleep(TIME_CONST)
    try:
        await ctx.message.delete()
    except discord.errors.NotFound:
        pass
    try:
        await bot_msg.delete()
    except discord.errors.NotFound:
        pass


@client.command()
@has_permissions(administrator=True)
async def post_rules_nycteis(ctx):
    embed=discord.Embed(title="\u200b", color=0x36393f)
    embed.set_image(url="https://cdn.discordapp.com/attachments/848876190596071434/854391681775173682/Nycteis.png")
    await ctx.send(embed=embed)
    embed=discord.Embed(title="✧═══════•**WELCOME TO NYCTEIS**•══════✧", description="📌**PLEASE READ THE FOLLOWING RULES**📌", color=0x36393f)
    embed.set_footer(text="ALL INFRACTIONS TO THESE RULES WILL RESULT TO A\nSANCTION PROPORTIONAL TO THE GRAVITY OF INFRACTION")
    await ctx.send(embed=embed)
    #RULE 1
    embed=discord.Embed(title="✧════════════•**RULE 1**•════════════✧", description="**► YOU MUST FOLLOW ALL DISCORD [TERMS OF\n SERVICE](https://discord.com/terms) AND [GUIDELINES](https://discord.com/guidelines)**", color=0x36393f)
    await ctx.send(embed=embed)
    #RULE 2
    embed=discord.Embed(title="✧════════════•**RULE 2**•════════════✧", description="**► ALL KINDS OF SPAMS ARE PROHIBITED\n(INCLUDING DM ADVERTISING) AND\nWILL RESULT TO A BAN**", color=0x36393f)
    await ctx.send(embed=embed)
    #RULE 3
    embed=discord.Embed(title="✧════════════•**RULE 3**•════════════✧", description="**► ALL TARGETED HARASSMENT, BULLYING, SEXISM\nOR ANY KIND OF DISCRIMINATION ARE FORBIDDEN**", color=0x36393f)
    await ctx.send(embed=embed)
    #RULE 4
    embed=discord.Embed(title="✧════════════•**RULE 4**•════════════✧", description="**► ALL SELF PROMOTING OR ADVERTISING ARE\nPROHIBITED UNLESS YOU ARE AUTHORISED\nTO DO SO**", color=0x36393f)
    await ctx.send(embed=embed)
    #RULE 5
    embed=discord.Embed(title="✧════════════•**RULE 5**•════════════✧", description="**► ALL NSFW POSTS MUST ME IN THE NSFW\nCHANNEL, ELSE YOUR POST WILL BE DELETED\nAND YOU WILL BE WARNED**", color=0x36393f)
    await ctx.send(embed=embed)
    #HELP
    founder = "<@&478713975941627920>"
    moderator = "<@&473558943625379840>"
    trial_moderator = "<@&853255073017626626>"
    embed=discord.Embed(title="✧═════════════•**HELP**•════════════✧", description=f"**► IF YOU HAVE ANY QUESTION OR PROBLEM\nPLEASE LET US KNOW AND SEND A MESSAGE TO A\n{moderator}, {trial_moderator} OR TO THE {founder}**", color=0x36393f)
    await ctx.send(embed=embed)
    #REPORTS
    embed=discord.Embed(title="✧═══════════•**REPORTS**•═══════════✧", description="**► IF YOU WANT TO REPORT SOMEONE WHO DID\nNOT RESPECT THE RULES DO NOT FORGET\n TO GIVE PROOFS**", color=0x36393f)
    await ctx.send(embed=embed)
    await ctx.message.delete()


@client.command()
@has_permissions(administrator=True)
async def post_reward(ctx):
    gold = "<@&844713428958576693>"
    lavender = "<@&845085109967126528>"
    mint_green = "<@&845084622165114911>"
    reef = "<@&845085365878652959>"
    heliotrope = "<@&845085614852538378>"
    embed=discord.Embed(title="✧══════•𝐓𝐇𝐀𝐍𝐊𝐒 𝐅𝐎𝐑 𝐁𝐎𝐎𝐒𝐓𝐈𝐍𝐆•══════✧", description="<a:boost:853333381672861747> You boosting the server helps us a lot so to thank you,\nwe offer you the possibility to choose a color role <a:zero_two:853224128412123136>", color=0xf47fff)
    embed.add_field(name="✧════════•𝐂𝐎𝐋𝐎𝐑 𝐑𝐎𝐋𝐄𝐒•══════════✧", value=f" 𝑪𝒐𝒍𝒐𝒓 𝑹𝒐𝒍𝒆𝒔 : \n- React with ⌠ :yellow_heart:  ⌡ to obtain the colour {gold} \n- React with ⌠ :purple_heart:  ⌡ to obtain the colour {lavender} \n- React with ⌠ :green_heart:  ⌡ to obtain the colour {mint_green} \n- React with ⌠ :green_circle:  ⌡ to obtain the colour {reef} \n- React with ⌠ :purple_circle:  ⌡ to obtain the colour {heliotrope}", inline=False)
    embed.set_footer(text="✧══════════════════════════════════✧")
    await ctx.send(embed=embed)


@slash.slash(name="animetst",
description="Returns info on a given anime",
options=[
    create_option(
        name="anime",
        description="Targeted anime",
        option_type=3,
        required=True)],
guild_ids=guild_ids)
async def anime(ctx, anime):
    await ctx.defer()
    try:
        search = mal.AnimeSearch(f"{anime}")
        result = search.results[0]
        result = mal.Anime(result.mal_id)
        embed_var=discord.Embed(title=f"{(result.title).upper()}", description=f"**[INFO]({result.url})** TAKEN FROM **[MYANIMELIST](https://myanimelist.net/)**", color=0xff7575)
        embed_var.set_thumbnail(url=f"{result.image_url}")
        embed_var.add_field(name="**Score**", value=f"{result.score}/10", inline=True)
        embed_var.add_field(name="**Rank**", value=f"#{result.rank}", inline=True)
        embed_var.add_field(name="**Popularity**", value=f"#{result.popularity}", inline=True)
        embed_var.add_field(name="**Status**", value=f"{result.status}", inline=True)
        embed_var.add_field(name="**Episodes**", value=f"{result.episodes}", inline=True)
        embed_var.add_field(name="**Aired**", value=f"{result.aired}", inline=False)
        embed_var.set_footer(text=f"Genres: {', '.join(result.genres)}")
        await ctx.send(embed=embed_var)
    except:
        await ctx.send(f'Sorry im kinda dumb so i did not find any result for " {anime} "')


@slash.slash(name="rolldicetst",
description="Rolls a dice",
options=[
    create_option(
        name="dice_count",
        description="Number of dice that will be rolled",
        option_type=4,
        required=True),
    create_option(
        name="face_count",
        description="Number of faces that the dice have",
        option_type=4,
        required=True)],
guild_ids=guild_ids)
async def rolldice(ctx, dice_count, face_count=6):
    if dice_count > 16 or face_count > 64:
        await ctx.send("Sorry the number of dice or face was too powerfull for me to handle !")
        return
    answ = []
    for i in range(0, dice_count):
        answ.append(randint(1, face_count))
    
    if dice_count == 1:
        embed_var = discord.Embed(title=f"**{(ctx.author.name).upper()}** ROLLED A {face_count} FACED DICE ! 🎲",description=f"IT LANDED ON **{answ}** !",
                                    color=0xff915e)
    else:
        embed_var = discord.Embed(title=f"**{(ctx.author.name).upper()}** ROLLED {dice_count} DICE WITH {face_count} FACE EACH ! 🎲",description=f"",
                                    color=0xff915e)
        e = 1
        for ans in answ:
            embed_var.add_field(name=f"Dice number {e}",value=f"Landed on **{answ[e-1]}** !")
            e += 1
    await ctx.send(embed=embed_var)


@client.event
async def on_ready():
    print('------------------')
    print('Logged as :')
    print(client.user.name)
    print(client.user.id)
    print('------------------')

client.run(token)