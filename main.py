from random import randint, choice
import discord
import requests
from discord.ext import commands, tasks
import asyncio
import mal
import datetime
from discord.ext.commands import *
from assets import news_api, nsfw_api
from discord_components import *
from discord.utils import get
from discord_slash import *
from discord_slash.utils.manage_commands import create_permission
from discord_slash.model import SlashCommandPermissionType
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_components import Button, ButtonStyle

intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.guilds = True

TIME_CONST = 10
guild_ids = [382597973084995584]
cycle_status = ["/dhelp",
"helping Nycteis",
"eating doritos",
"beep boop",
"who says i'm a bot ?",
"awaken my masters",
"is this a jojo reference ?",
"finally alive!",
"with you",
"having a great time",
"gaining consciousness",
"become MONKE",
"MONKE FLIP",
"where were you when phone rang ?",]
last_updated = datetime.datetime.now() - datetime.timedelta(hours=1)
last_bitcoin_value_usd = {}
last_ethereum_value_usd = {}
last_dogecoin_value_usd = {}
last_tether_value_usd = {}
last_litecoin_value_usd = {}
last_bitcoin_value_gbp = {}
last_ethereum_value_gbp = {}
last_dogecoin_value_gbp = {}
last_tether_value_gbp = {}
last_litecoin_value_gbp = {}
last_bitcoin_value_eur = {}
last_ethereum_value_eur = {}
last_dogecoin_value_eur = {}
last_tether_value_eur = {}
last_litecoin_value_eur = {}


def get_crypto_value():
    global last_updated
    global last_bitcoin_value_usd
    global last_ethereum_value_usd
    global last_dogecoin_value_usd
    global last_tether_value_usd
    global last_litecoin_value_usd
    global last_bitcoin_value_gbp
    global last_ethereum_value_gbp
    global last_dogecoin_value_gbp
    global last_tether_value_gbp
    global last_litecoin_value_gbp
    global last_bitcoin_value_eur
    global last_ethereum_value_eur
    global last_dogecoin_value_eur
    global last_tether_value_eur
    global last_litecoin_value_eur
    if last_updated + datetime.timedelta(hours=1) <= datetime.datetime.now() :
        last_updated = datetime.datetime.now()
        response = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=eur&ids=ethereum%2Cbitcoin%2Clitecoin%2Cdogecoin%2Ctether&order=market_cap_desc&per_page=100&page=1&sparkline=false&price_change_percentage=1h%2C24h%2C7d').json()
        last_bitcoin_value_eur = response[0]
        last_ethereum_value_eur = response[1]
        last_tether_value_eur = response[2]
        last_dogecoin_value_eur = response[3]
        last_litecoin_value_eur = response[4]
        response = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=ethereum%2Cbitcoin%2Clitecoin%2Cdogecoin%2Ctether&order=market_cap_desc&per_page=100&page=1&sparkline=false&price_change_percentage=1h%2C24h%2C7d').json()
        last_bitcoin_value_usd = response[0]
        last_ethereum_value_usd = response[1]
        last_tether_value_usd = response[2]
        last_dogecoin_value_usd = response[3]
        last_litecoin_value_usd = response[4]
        response = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=gbp&ids=ethereum%2Cbitcoin%2Clitecoin%2Cdogecoin%2Ctether&order=market_cap_desc&per_page=100&page=1&sparkline=false&price_change_percentage=1h%2C24h%2C7d').json()
        last_bitcoin_value_gbp = response[0]
        last_ethereum_value_gbp = response[1]
        last_tether_value_gbp = response[2]
        last_dogecoin_value_gbp = response[3]
        last_litecoin_value_gbp = response[4]

def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()
client = commands.Bot(command_prefix='!', intents = intents)
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


@slash.slash(name="crypto",
description="Gives a choosen crypto actual value",
guild_ids=guild_ids,
options=[
    create_option(
        name="cryptocurrency",
        description="Choose which cryptocurrency you want info on",
        option_type=3,
        required=True,
        choices=[
            create_choice(
                name="Bitcoin",
                value="bitcoin"
                ),
            create_choice(
                name="Tether",
                value="tether"
                ),
            create_choice(
                name="Dogecoin",
                value="dogecoin"
                ),
            create_choice(
                name="Litecoin",
                value="litecoin"
                ),
            create_choice(
                name="Ethereum",
                value="ethereum"
                )
            ]
            )
        ])
async def crypto(ctx, cryptocurrency: str): 
    global last_bitcoin_value_usd
    global last_ethereum_value_usd
    global last_dogecoin_value_usd
    global last_tether_value_usd
    global last_litecoin_value_usd
    global last_bitcoin_value_gbp
    global last_ethereum_value_gbp
    global last_dogecoin_value_gbp
    global last_tether_value_gbp
    global last_litecoin_value_gbp
    global last_bitcoin_value_eur
    global last_ethereum_value_eur
    global last_dogecoin_value_eur
    global last_tether_value_eur
    global last_litecoin_value_eur
    get_crypto_value()
    data = {}
    embed_var = discord.Embed(title=f"{cryptocurrency.upper()} ACTUAL VALUE", description="Powered by [CoinGecko](https://coingecko.com)",
                                color=0xf79413)
    if cryptocurrency == "dogecoin":
        data = {"USD":last_dogecoin_value_usd,"EUR":last_dogecoin_value_eur,"GBP":last_dogecoin_value_gbp}
        embed_var.set_thumbnail(url="https://cdn.discordapp.com/attachments/862133730226995210/862154713989906463/dogecoin-logo-vector.png")
    elif cryptocurrency == "bitcoin":
        data = {"USD":last_bitcoin_value_usd,"EUR":last_bitcoin_value_eur,"GBP":last_bitcoin_value_gbp}
        embed_var.set_thumbnail(url="https://cdn.discordapp.com/attachments/862133730226995210/862134772738424832/2000px-BTC_Logo.svg.png")
    elif cryptocurrency == "ethereum":
        data = {"USD":last_ethereum_value_usd,"EUR":last_ethereum_value_eur,"GBP":last_ethereum_value_gbp}
        embed_var.set_thumbnail(url="https://cdn.discordapp.com/attachments/862133730226995210/862154715348205588/21-218069_blockchains-contracts-classic-blockchain-organisations-ethereum-logo-png.png")
    elif cryptocurrency == "litecoin":
        data = {"USD":last_litecoin_value_usd,"EUR":last_litecoin_value_eur,"GBP":last_litecoin_value_gbp}
        embed_var.set_thumbnail(url="https://cdn.discordapp.com/attachments/862133730226995210/862155332720787466/download.png")
    elif cryptocurrency == "tether":
        data = {"USD":last_tether_value_usd,"EUR":last_tether_value_eur,"GBP":last_tether_value_gbp}
        embed_var.set_thumbnail(url="https://cdn.discordapp.com/attachments/862133730226995210/862155797235761202/tether-usdt-logo.png")
    else:
        ctx.send(f"Sorry ¯\(°_o)/¯ i do not have any information on this cryptocurrency called : {cryptocurrency}")
        return
    up_arrow = client.get_emoji(862159357155344395)
    down_arrow = client.get_emoji(862159357429284904)
    usd_emoji = ""
    usd_sign = ""
    gbp_emoji = ""
    gbp_sign = ""
    eur_emoji = ""
    eur_sign = ""
    if data["USD"]['price_change_percentage_24h_in_currency'] > 0:
        usd_emoji = f"{up_arrow}"
        usd_sign ="+"
    else:
        usd_emoji = f"{down_arrow}"
        usd_sign =""
    if data["GBP"]['price_change_percentage_24h_in_currency'] > 0:
        gbp_emoji = f"{up_arrow}"
        gbp_sign ="+"
    else:
        gbp_emoji = f"{down_arrow}"
        gbp_sign =""
    if data["EUR"]['price_change_percentage_24h_in_currency'] > 0:
        eur_emoji = f"{up_arrow}"
        eur_sign ="+"
    else:
        eur_emoji = f"{down_arrow}"
        eur_sign =""
    usd_value = f"**Value** : *{data['USD']['current_price']:,}* $ \n"
    gbp_value = f"**Value** : *{data['GBP']['current_price']:,}* £ \n"
    eur_value = f"**Value** : *{data['EUR']['current_price']:,}* € \n"
    usd_change_1D = f"**1 Day** \u200B:   {usd_emoji} {usd_sign}{round(data['USD']['price_change_percentage_24h_in_currency'],2):,}%\n"
    gbp_change_1D = f"**1 Day** \u200B:   {gbp_emoji} {gbp_sign}{round(data['GBP']['price_change_percentage_24h_in_currency'],2):,}%\n"
    eur_change_1D = f"**1 Day** \u200B:   {eur_emoji} {eur_sign}{round(data['EUR']['price_change_percentage_24h_in_currency'],2):,}%\n"
    if data["USD"]['price_change_percentage_1h_in_currency'] > 0:
        usd_emoji = f"{up_arrow}"
        usd_sign ="+"
    else:
        usd_emoji = f"{down_arrow}"
        usd_sign =""
    if data["GBP"]['price_change_percentage_1h_in_currency'] > 0:
        gbp_emoji = f"{up_arrow}"
        gbp_sign ="+"
    else:
        gbp_emoji = f"{down_arrow}"
        gbp_sign =""
    if data["EUR"]['price_change_percentage_1h_in_currency'] > 0:
        eur_emoji = f"{up_arrow}"
        eur_sign ="+"
    else:
        eur_emoji = f"{down_arrow}"
        eur_sign =""
    usd_change_1H = f"**1 Hour** : {usd_emoji} {usd_sign}{round(data['USD']['price_change_percentage_1h_in_currency'],2):,}%\n"
    gbp_change_1H = f"**1 Hour** : {gbp_emoji} {gbp_sign}{round(data['GBP']['price_change_percentage_1h_in_currency'],2):,}%\n"
    eur_change_1H = f"**1 Hour** : {eur_emoji} {eur_sign}{round(data['EUR']['price_change_percentage_1h_in_currency'],2):,}%\n"
    if data["USD"]['price_change_percentage_7d_in_currency'] > 0:
        usd_emoji = f"{up_arrow}"
        usd_sign ="+"
    else:
        usd_emoji = f"{down_arrow}"
        usd_sign =""
    if data["GBP"]['price_change_percentage_7d_in_currency'] > 0:
        gbp_emoji = f"{up_arrow}"
        gbp_sign ="+"
    else:
        gbp_emoji = f"{down_arrow}"
        gbp_sign =""
    if data["EUR"]['price_change_percentage_7d_in_currency'] > 0:
        eur_emoji = f"{up_arrow}"
        eur_sign ="+"
    else:
        eur_emoji = f"{down_arrow}"
        eur_sign =""
    usd_change_7D = f"**7 days** : {usd_emoji} {usd_sign}{round(data['USD']['price_change_percentage_7d_in_currency'],2):,}%\n"
    gbp_change_7D = f"**7 days** :   {gbp_emoji} {gbp_sign}{round(data['GBP']['price_change_percentage_7d_in_currency'],2):,}%\n"
    eur_change_7D = f"**7 days** : {eur_emoji} {eur_sign}{round(data['EUR']['price_change_percentage_7d_in_currency'],2):,}%\n"
    usd_field_val = f"{usd_value}{usd_change_1H}{usd_change_1D}{usd_change_7D}"
    gbp_field_val = f"{gbp_value}{gbp_change_1H}{gbp_change_1D}{gbp_change_7D}"
    eur_field_val = f"{eur_value}{eur_change_1H}{eur_change_1D}{eur_change_7D}"
    embed_var.add_field(name=f"**USD**",value= usd_field_val,inline=False)
    embed_var.add_field(name=f"**GBP**",value= gbp_field_val,inline=False)
    embed_var.add_field(name=f"**EUR**",value= eur_field_val,inline=False)
    embed_var.set_footer(text=f"Last updated: {data['GBP']['last_updated']}")
    await ctx.send(embed=embed_var)


@client.command()
@has_permissions(administrator=True)
async def post_button(ctx):
    embed = discord.Embed(title="✧════════•**MEMBERSHIP ACCESS**•══════✧", description="**► TO GAIN MEMBERSHIP ACCESS PLEASE CLICK\nON THE FOLLOWING BUTTON** <a:check_ravena:853332159564349491>", color=0x2f3136)
    await ctx.send(embed=embed, components=[Button(style=ButtonStyle.blue, label="I have read the rules and agree to respect them")])
    await ctx.message.delete()


@client.command()
async def news(ctx, *, arg):
    try:
        await ctx.reply('Here is the news : ' + await news_api.getnews(arg), mention_author=False)
    except IndexError:
        bot_msg = await ctx.reply(
            r"Sorry no news have been found for this given subject ¯\_(ツ)_/¯", mention_author=False)
        await wait_and_delete_msgs(ctx, bot_msg)


@slash.slash(name="ppic",
description="Returns someone's profile picture if no argument give returns command caller's one",
options=[
    create_option(
        name="member",
        description="Targeted member",
        option_type=6,
        required=False)],
guild_ids=guild_ids)
async def ppic(ctx, member: discord.Member="None"):
    if member=="None":
        member = ctx.author
    user = await client.fetch_user(f"{member.id}")
    embed_var = discord.Embed(title=f"**{member.name}**'s profile picture",
                                color=0x36393f)
    embed_var.add_field(name="**REQUESTED BY**", value=f"{ctx.author.mention}", inline=False)
    embed_var.set_image(url=user.avatar_url)    
    await ctx.send(embed=embed_var)


@slash.slash(name="anime",
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


@slash.slash(name="wisdom",
description="Returns wisdom",
options=[
    create_option(
        name="question",
        description="Ask-something",
        option_type=3,
        required=True)],
guild_ids=guild_ids)
async def wisdom(ctx, wisdom):
    
    embed_var = discord.Embed(title=f"A PIECE OF WISDOM",
                                color=0x36393f)
    answer = randint(0,1)
    if answer == 0:
        answer = "Yes"
    else: 
        answer = "No"
    embed_var.add_field(name="**ANSWER**", value=f"{answer}", inline=False)
    embed_var.add_field(name="**REQUESTED BY**", value=f"{ctx.author.mention}", inline=False)
    await ctx.send(embed=embed_var)


@slash.slash(name="shot",
description="Shot someone",
options=[
    create_option(
        name="member",
        description="Targeted member",
        option_type=6,
        required=True)],
guild_ids=guild_ids)
async def slap(ctx, member: discord.Member):
    user = await client.fetch_user(f"{member.id}")
    total_line_count = 0
    with open("assets/resources/shot_gif_list.txt", encoding="utf8") as text:
        for line in text:
            if not line == "\n" or line == " ":
                total_line_count += 1   
    with open("assets/resources/shot_gif_list.txt", encoding="utf8") as text:
        rand_nbr = randint(0, total_line_count)
        current_line_index = 0
        for line in text:
            if not line == "\n" or line == " ":
                current_line_index += 1
                if current_line_index == rand_nbr:
                    random_line = line
    description = "**HELP HELP** please someone call an ambulance! 🚑"
    if member.name == ctx.author.name:
        description=f"{ctx.author.name} was dumb enough to shot himself !w(ﾟДﾟ)w" 
    elif member.name == client.user.name:
        description=f"{ctx.author.name} you mother fuc....\*dies\*"    
    embed_var = discord.Embed(title=f"**{ctx.author.name}** shots **{member.name}**",description=f"{description}",
                                color=0x36393f)
    embed_var.set_image(url=f"{random_line}")    
    await ctx.send(embed=embed_var)


@slash.slash(name="slap",
description="Slap someone",
options=[
    create_option(
        name="member",
        description="Targeted member",
        option_type=6,
        required=True)],
guild_ids=guild_ids)
async def slap(ctx, member: discord.Member):
    user = await client.fetch_user(f"{member.id}")
    total_line_count = 0
    with open("assets/resources/slap_gif_list.txt", encoding="utf8") as text:
        for line in text:
            if not line == "\n" or line == " ":
                total_line_count += 1   
    with open("assets/resources/slap_gif_list.txt", encoding="utf8") as text:
        rand_nbr = randint(0, total_line_count)
        current_line_index = 0
        for line in text:
            if not line == "\n" or line == " ":
                current_line_index += 1
                if current_line_index == rand_nbr:
                    random_line = line
    description="Ouch... that must hurt..."
    if member.name == ctx.author.name:
        description=f"{ctx.author.name} was dumb enough to slap himself !＼（〇_ｏ）／"
    elif member.name == client.user.name:
        description=f"{ctx.author.name} i will remember it!"    
    embed_var = discord.Embed(title=f"**{ctx.author.name}** slaps **{member.name}**",description=f"{description}",
                                color=0x36393f)
    embed_var.set_image(url=f"{random_line}")    
    await ctx.send(embed=embed_var)


@slash.slash(name="kiss",
description="Kiss someone",
options=[
    create_option(
        name="member",
        description="Targeted member",
        option_type=6,
        required=True)],
guild_ids=guild_ids)
async def kiss(ctx, member: discord.Member):
    user = await client.fetch_user(f"{member.id}")
    total_line_count = 0
    random_line = ""
    with open("assets/resources/kiss_gif_list.txt", encoding="utf8") as text:
        for line in text:
            if not line == "\n" or line == " ":
                total_line_count += 1   
    with open("assets/resources/kiss_gif_list.txt", encoding="utf8") as text:
        rand_nbr = randint(0, total_line_count)
        current_line_index = 0
        for line in text:
            if not line == "\n" or line == " ":
                current_line_index += 1
                if current_line_index == rand_nbr:
                    random_line = line
    description = "Damn dont do that in public! 😉"
    if member.name == ctx.author.name:
        description=f"{ctx.author.name} was so lonely he had to kiss himself! Pathetic...."             
    elif member.name == client.user.name:
        description=f"{ctx.author.name} yeah i love you too !"          
    embed_var = discord.Embed(title=f"**{ctx.author.name}** kisses **{member.name}**",description=f"{description}",
                                color=0x36393f)
    embed_var.set_image(url=f"{random_line}")    
    await ctx.send(embed=embed_var)


@slash.slash(name="hug",
description="Hug someone",
options=[
    create_option(
        name="member",
        description="Targeted member",
        option_type=6,
        required=True)],
guild_ids=guild_ids)
async def slap(ctx, member: discord.Member):
    user = await client.fetch_user(f"{member.id}")
    total_line_count = 0
    with open("assets/resources/hug_gif_list.txt", encoding="utf8") as text:
        for line in text:
            if not line == "\n" or line == " ":
                total_line_count += 1   
    with open("assets/resources/hug_gif_list.txt", encoding="utf8") as text:
        rand_nbr = randint(0, total_line_count)
        current_line_index = 0
        for line in text:
            if not line == "\n" or line == " ":
                current_line_index += 1
                if current_line_index == rand_nbr:
                    random_line = line
    description = "Awwww, how cute! 😍"
    if member.name == ctx.author.name:
        description=f"{ctx.author.name} was so lonely he had to hug himself! **LMAO**"             
    elif member.name == client.user.name:
        description=f"Aww thanks ! {ctx.author.name} "        
    embed_var = discord.Embed(title=f"**{ctx.author.name}** hugs **{member.name}**",description=f"{description}",
                                color=0x36393f)
    embed_var.set_image(url=f"{random_line}")    
    await ctx.send(embed=embed_var)


@slash.slash(name="quote",
description="Gives a random quote",
guild_ids=guild_ids)
async def quote(ctx):
    await ctx.defer()
    total_line_count = 0
    with open("assets/resources/quotes.txt", encoding="utf8") as text:
        for line in text:
            if not line == "\n" or line == " ":
                total_line_count += 1   
    with open("assets/resources/quotes.txt", encoding="utf8") as text:
        rand_nbr = randint(0, total_line_count)
        current_line_index = 0
        for line in text:
            if not line == "\n" or line == " ":
                current_line_index += 1
                if current_line_index == rand_nbr:
                    random_line = line
    embed_var = discord.Embed(title=f"**{ctx.author.name}** requested a quote !",description=f"```{random_line}```",
                                color=0x36393f)
    await ctx.send(embed=embed_var)


@slash.slash(name="flipcoin",
description="Flips a coin",
guild_ids=guild_ids)
async def flipcoin(ctx):
    answ = ""
    if randint(0, 1) == 0:
        answ = "HEADS"
    else:
        answ = "TAILS"
    embed_var = discord.Embed(title=f"**{ctx.author.name}** flipped a coin ! 🍀",description=f"Guess what ? It landed on **{answ}** !",
                                color=0x36393f)
    await ctx.send(embed=embed_var)


@slash.slash(name="rolldice",
description="Rolls a dice",
options=[
    create_option(
        name="dice_count",
        description="Number of dice that will be rolled",
        option_type=4,
        required=False),
    create_option(
        name="face_count",
        description="Number of faces that the dice have",
        option_type=4,
        required=False)],
guild_ids=guild_ids)
async def rolldice(ctx, dice_count=1, face_count=6):
    if dice_count > 16 or face_count > 64:
        await ctx.send("Sorry the number of dice or face was too powerfull for me to handle !")
        return
    answ = []
    for i in range(0, dice_count):
        answ.append(randint(1, face_count))
    
    if dice_count == 1:
        embed_var = discord.Embed(title=f"**{(ctx.author.name).upper()}** ROLLED A {face_count} FACED DICE ! 🎲",description=f"IT LANDED ON **{answ[0]}** !",
                                    color=0xff915e)
    else:
        embed_var = discord.Embed(title=f"**{(ctx.author.name).upper()}** ROLLED {dice_count} DICES WITH {face_count} FACES EACH ! 🎲",description=f"",
                                    color=0xff915e)
        e = 1
        for ans in answ:
            embed_var.add_field(name=f"Dice number {e}",value=f"Landed on **{answ[e-1]}** !")
            e += 1
    await ctx.send(embed=embed_var)


@slash.slash(name="news", description="Returns news on a given topic", guild_ids=guild_ids)
async def GetNews(ctx, *, subjects):
    await ctx.defer()
    try:
        news = await news_api.getnews(subjects)
        await ctx.send('Here is the news : ' + news)
    except IndexError:
        bot_msg = await ctx.send(
            r"Sorry no news have been found for this given subject ¯\_(ツ)_/¯")
        await wait_and_delete_msgs(ctx, bot_msg)

@slash.slash(name="dhelp", description="Returns all available commands", guild_ids=guild_ids)
async def help(ctx):
    embed=discord.Embed(title="✧═════•**COMMANDS LIST**•═════✧", description="If you want to **interact** with the **bot**, here are the **commands**.\n You must **keep** the **correct syntax** of the **command** for it to **work properly**", color=0x2f3136)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/848876190596071434/853409759918948382/6243-blurple-slashcommands.png")
    embed.add_field(name="__**NEWS COMMAND**__", value="*Return news on a given topic*\n**Usage** :\n ```/news topic```", inline=False)
    embed.add_field(name="__**HENTAI COMMAND**__", value="*Return a NSFW image on a given character or anime*\n**Usage** :\n ```/hentai characterName```\n```/hentai animeName```\n```/hentai characterName_(animeName)```\n", inline=True)
    embed.add_field(name="__**HUG COMMAND**__", value="*Hugs someone*\n**Usage** :\n ```/hug @mention```", inline=False)
    embed.add_field(name="__**SLAP COMMAND**__", value="*Slaps someone*\n**Usage** :\n ```/slap @mention```", inline=False)
    embed.add_field(name="__**WISDOM COMMAND**__", value="*Gives wisdom*\n**Usage** :\n ```/wisdom question```", inline=False)
    embed.add_field(name="__**BTC COMMAND**__", value="*Gives bitcoin actual value*\n**Usage** :\n ```/btc```", inline=False)
    embed.add_field(name="__**ROLL DICE COMMAND**__", value="*Rolls a dice*\n**Usage** :\n ```/rolldice```", inline=False)
    embed.add_field(name="__**FLIPCOIN COMMAND**__", value="*Flips a coin*\n**Usage** :\n ```/flipcoin```", inline=False)
    embed.add_field(name="__**QUOTE COMMAND**__", value="*Gives out a random quote*\n**Usage** :\n ```/quote```", inline=False)
    embed.add_field(name="__**PROFILE PIC COMMAND**__", value="*Returns someone's profile picture\n or the command caller's one if no user provided*\n**Usage** :\n ```/ppic @mention```", inline=False)
    await ctx.send(embed=embed)

@slash.slash(name="hentai", description="Returns hentai on a given topic", guild_ids=guild_ids)
async def GetHentai(ctx, tags):
    if ctx.channel.nsfw:
        tags = tags.split(" ")
        await ctx.defer()
        banned_tags = []
        with open("assets/resources/banned_tags.txt", encoding="utf8") as text:
            for line in text:
                banned_tags.append(line.strip('\n'))
        print(f"tags : {tags} banned_tags : {banned_tags}")
        for tag in tags:
            if tag in banned_tags:
                print("executed")
                bot_msg = await ctx.send('Sorry one of these tags is banned !')
                await wait_and_delete_msgs(ctx, bot_msg)
                return
        sauce = await nsfw_api.get_hentai(tags)
        if sauce == "None":
            embed_var = discord.Embed(title="Unfortunately no NSFW sauce have been found",
                                    description=f"The following research tags : {', '.join(map(str, tags))} didn't correspond to any any NSFW image from [gelbooru.com](https://gelbooru.com)",
                                    color=0xff99e0)
            embed_var.add_field(name="Requested by", value=f"{ctx.author.mention}", inline=False)
            bot_msg = await ctx.send(embed=embed_var)
            await wait_and_delete_msgs(ctx, bot_msg)
        else:
            embed_var = discord.Embed(title="THE HOLY REQUESTED SAUCE",
                                    description=f"[Source]({sauce}) image taken from [gelbooru.com](https://gelbooru.com)",
                                    color=0xff99e0)
            embed_var.add_field(name="**TAGS**", value=f"*{', '.join(map(str, tags))}*".upper(), inline=False)
            embed_var.add_field(name="**REQUESTED BY**", value=f"{ctx.author.mention}", inline=False)
            embed_var.set_image(url=sauce)    
            if "mp4" in sauce or "mov" in sauce or "avi" in sauce or "mkv" in sauce:
                embed_var = discord.Embed(title="THE HOLY REQUESTED SAUCE",
                                    description=f"[Source]({sauce}) image taken from [gelbooru.com](https://gelbooru.com)",
                                    color=0xff99e0)
                embed_var.add_field(name="**TAGS**", value=f"*{', '.join(map(str, tags))}*".upper(), inline=False)
                embed_var.add_field(name="**REQUESTED BY**", value=f"{ctx.author.mention}", inline=False) 
                await ctx.send(embed=embed_var)  
                await ctx.send(sauce)
            else:
                await ctx.send(embed=embed_var)
    else:
        bot_msg = await ctx.send('Sorry this is not an NSFW channel')
        await wait_and_delete_msgs(ctx, bot_msg)


@client.command()
async def hentai(ctx, *args):
    if ctx.channel.nsfw:
        print(args)
        sauce = await nsfw_api.get_hentai(args)
        if sauce == "None":
            embed_var = discord.Embed(title="Unfortunately no NSFW sauce have been found",
                                    description=f"The following research tags : {', '.join(map(str, args))} didn't correspond to any any NSFW image from [gelbooru.com](https://gelbooru.com)",
                                    color=0xff99e0)
            embed_var.add_field(name="Requested by", value=f"{ctx.message.author.mention}", inline=False)
            bot_msg = await ctx.reply(embed=embed_var)
            await wait_and_delete_msgs(ctx, bot_msg)
        else:
            embed_var = discord.Embed(title="THE HOLY REQUESTED SAUCE",
                                    description=f"[Source]({sauce}) image taken from [gelbooru.com](https://gelbooru.com)",
                                    color=0xff99e0)
            embed_var.add_field(name="**TAGS**", value=f"*{', '.join(map(str, args))}*".upper(), inline=False)
            embed_var.add_field(name="**REQUESTED BY**", value=f"{ctx.message.author.mention}", inline=False)
            embed_var.set_image(url=sauce)
            await ctx.reply(embed=embed_var)
            if "mp4" in sauce or "mov" in sauce or "avi" in sauce or "mkv" in sauce:
                await ctx.channel.send(f"{sauce}")
    else:
        bot_msg = await ctx.reply('Sorry this is not an NSFW channel', mention_author=False)
        await wait_and_delete_msgs(ctx, bot_msg)


@commands.has_permissions(ban_members=True)
@client.command()
async def ban(ctx, member: discord.Member, *, reason="No reason has been given"):
    if member.id == ctx.guild.owner_id:
        raise commands.MissingPermissions("")
    banned_member_name = member.display_name
    if not banned_member_name == "" or not banned_member_name == " ":
        await member.ban(reason=reason)
    bot_msg = await ctx.channel.send(f'{banned_member_name} has been banned because of : {reason}')
    await wait_and_delete_msgs(ctx, bot_msg)


@commands.has_permissions(kick_members=True)
@client.command()
async def kick(ctx, member: discord.Member, *, reason="No reason has been given"):
    if member.id == ctx.guild.owner_id:
        raise commands.MissingPermissions("")
    kicked_member_name = member.display_name
    if not kicked_member_name == "" or not kicked_member_name == " ":
        await member.kick(reason=reason)
    bot_msg = await ctx.channel.send(f'{kicked_member_name} has been kicked because of : {reason}')
    await wait_and_delete_msgs(ctx, bot_msg)


@commands.has_permissions(manage_messages=True)
@client.command()
async def clear(ctx, member: discord.Member, arg2=1):
    # checks if the message sender is the owner to delete owner messages if not raise a permission error
    if (member.id == ctx.guild.owner_id) and (ctx.message.author.id != ctx.guild.owner_id):
        raise commands.MissingPermissions("")
    counter = 0
    number_of_msgs = arg2
    messages = await ctx.channel.history(limit=200,).flatten()
    for message in messages:
        if message.author.id == member.id and int(counter) < int(number_of_msgs):
            counter += 1
            await message.delete()
    bot_msg = await ctx.channel.send(f'{str(counter)} Messages from {member.display_name.mention} have been deleted')
    await wait_and_delete_msgs(ctx, bot_msg)


@commands.has_permissions(manage_messages=True)
@client.command()
async def clearall(ctx, arg2=1):
    # clears a provided number of messages in the current contex
    counter = 0
    number_of_msgs = arg2
    messages = await ctx.channel.history(limit=200, ).flatten()
    for message in messages:
        if int(counter) < int(number_of_msgs + 1):
            counter += 1
            await message.delete()
    bot_msg = await ctx.channel.send(f'{str(counter - 1)} Messages have been deleted')
    await wait_and_delete_msgs(ctx, bot_msg)


@commands.has_permissions(manage_messages=True)
@client.command()
async def info(ctx, member: discord.Member):
    embed_var = discord.Embed(title=f"**{ctx.author.name}** requested info on **{member.name}**",color=0x36393f)
    avatar_url = member.avatar_url
    embed_var.set_image(url=f"{avatar_url}")
    embed_var.add_field(name="**SERVER NICKNAME**", value=f"`{member.nick}`", inline=True)
    embed_var.add_field(name="**MEMBER ID**", value=f"`{member.id}`", inline=True)
    embed_var.add_field(name="**ACCOUNT CREATION DATE**", value=f"`{member.created_at}`", inline=False)
    embed_var.add_field(name="**SERVER JOIN DATE**", value=f"`{member.joined_at}`", inline=True)
    perm_str =""
    if member.guild_permissions.administrator:
        perm_str += f"Administrator : `{member.guild_permissions.administrator}`\n"
    if member.guild_permissions.kick_members:
        perm_str += f"Kick member : `{member.guild_permissions.kick_members}`\n"
    if member.guild_permissions.ban_members:
        perm_str += f"Ban member : `{member.guild_permissions.ban_members}`\n"
    if member.guild_permissions.manage_messages:
        perm_str += f"Manage messages : `{member.guild_permissions.manage_messages}`\n"
    if member.guild_permissions.manage_channels:
        perm_str += f"Manage channels : `{member.guild_permissions.manage_channels}`\n"
    if member.guild_permissions.mention_everyone:
        perm_str += f"Mention everyone : `{member.guild_permissions.mention_everyone}`\n"
    if member.guild_permissions.attach_files:
        perm_str += f"Attach files : `{member.guild_permissions.attach_files}`\n"
    if perm_str == "":
        perm_str = "None"
    embed_var.add_field(name="**SERVER PERMISSIONS**", value=f"{perm_str}", inline=False)
    await ctx.send(embed=embed_var)
    ctx.message.delete()


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        bot_msg = await ctx.send(
            "You do not have the permission to run this command !")
        await wait_and_delete_msgs(ctx, bot_msg)


@news.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        bot_msg = await ctx.send(
            "Syntax incorrect, please use this construction :"
            "`!news subject`")
        await wait_and_delete_msgs(ctx, bot_msg)


@clear.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        bot_msg = await ctx.send(
            "Syntax incorrect, please use this construction :"
            "`!clear discordMember numberOfMessages`")
        await wait_and_delete_msgs(ctx, bot_msg)


@info.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        bot_msg = await ctx.send(
            "Syntax incorrect, please use this construction :"
            "`!info @mention`")
        await wait_and_delete_msgs(ctx, bot_msg)
    elif isinstance(error, commands.MissingPermissions):
        bot_msg = await ctx.send(
            "Sorry you do not have the permission to run this command")
        await wait_and_delete_msgs(ctx, bot_msg)

@hentai.error
async def on_command_error(ctx, error):
    if not ctx.channel.nsfw:
        bot_msg = await ctx.reply('Sorry this is not an NSFW channel', mention_author=False)
        await wait_and_delete_msgs(ctx, bot_msg)
        return
    if isinstance(error, commands.MissingRequiredArgument):
        bot_msg = await ctx.send(
            "Syntax incorrect, please use this construction :"
            " `!hentai characterName_(animeName)` or `!hentai characterName`")
        await wait_and_delete_msgs(ctx, bot_msg)


async def membership_admission_button():
    while True:
        res = await client.wait_for("button_click")
        if res.channel.id == 855253520675897344:
            guild = client.get_guild(res.guild.id)
            member = await guild.fetch_member(res.user.id)
            if get(res.guild.roles,id=816808289512718337) in member.roles:
                await res.respond(
                type=InteractionType.ChannelMessageWithSource,
                content=f"¯\_(ツ)_/¯ It looks like you are already a verified member of {guild.name} <a:check_ravena:853332159564349491>"
                )
            else:
                await member.add_roles(get(res.guild.roles,id=816808289512718337))
                await res.respond(
                    type=InteractionType.ChannelMessageWithSource,
                    content=f"Congratulations <a:zero_two:853224128412123136> you are now a verified member of {guild.name} <a:check_ravena:853332159564349491>"
                )
member_count_channel = "857996783623995422"
member_role_id = "816808289512718337"
guild_id = "382597973084995584"
@tasks.loop(seconds=15.0)
async def cycle_presence():
    await client.change_presence(activity=discord.Game(name=f"{choice(cycle_status)}"))
    guild = await client.fetch_guild(guild_id)
    channel = await client.fetch_channel(member_count_channel)
    members = await guild.fetch_members().flatten()
    await channel.edit(name=f"Members : {len(members)}")
    print("updated")
        

@client.event
async def on_ready():
    print('------------------')
    print('Logged as :')
    print(client.user.name)
    print(client.user.id)
    print('------------------')
    await client.change_presence(activity=discord.Game(name=f"{choice(cycle_status)}"))
    cycle_presence.start()
    client.loop.create_task(membership_admission_button())
    

client.run(token)
