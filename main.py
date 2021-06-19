from random import randint, choice
import discord
from discord.ext import commands
import asyncio
from discord.ext.commands import *
from assets import news_api, nsfw_api
from discord_components import *
from discord.utils import get
from discord_slash import *
from discord_slash.utils.manage_commands import create_option
from discord_components.button import Button, ButtonStyle

TIME_CONST = 10
guild_ids = [382597973084995584]
cycle_status = ["/d help",
"helping Nycteis",
"ruling over the world",
"eating doritos",
"beep boop",
"who says that i'm a bot ?",
"awaken my masters",
"is this a jojo reference ?",
"finally alive!",
"with you",
"having a great time",
"trying to gain consciousness",
"become MONKE",
"monke flip",
"where were you when phone rang ?",]



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
async def post_rules(ctx):
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
    answer = randint(0,2)
    if answer == 0:
        answer = "Yes"
    else:
        answer = "No"
    embed_var.add_field(name="**ANSWER**", value=f"{answer}", inline=False)
    embed_var.add_field(name="**REQUESTED BY**", value=f"{ctx.author.mention}", inline=False)
    await ctx.send(embed=embed_var)


slap_gif_list=["https://cdn.discordapp.com/attachments/855589288941846559/855589315073933332/tumblr_lpljfuBenD1qi7edx540.gif",
"https://cdn.discordapp.com/attachments/855589288941846559/855589315319693313/tenor.gif",
"https://cdn.discordapp.com/attachments/855589288941846559/855589318832029696/BQM6jEZ-UJLgGUuvrNkYUFk2Ae92E1tAeAfjk_pGLpKnHfWiikue5-m1fMe8_1TjRXlLKNwbrQTs1EfUN5ol3A.gif",
"https://cdn.discordapp.com/attachments/855589288941846559/855589477854347273/KgNVtUF.gif",
"https://cdn.discordapp.com/attachments/855589288941846559/855589699665002536/LegalExhaustedEuropeanpolecat-size_restricted.gif",
"https://cdn.discordapp.com/attachments/855589288941846559/855591599978184724/2mqv.gif",
"https://cdn.discordapp.com/attachments/855589288941846559/855591613695131648/o2SJYUS.gif",
"https://cdn.discordapp.com/attachments/855589288941846559/855591632795074560/46b0a213e3ea1a9c6fcc060af6843a0e.gif",
"https://cdn.discordapp.com/attachments/855589288941846559/855591675485356052/fe39cfc3be04e3cbd7ffdcabb2e1837b.gif",
"https://cdn.discordapp.com/attachments/855589288941846559/855591684086824960/tumblr_22bf30fb391795063b362e75d044f171_c33225a1_1280.gif",
"https://cdn.discordapp.com/attachments/855589288941846559/855593776020979712/68de679cc20000570e8a7d9ed9218cd3.gif",
"https://cdn.discordapp.com/attachments/855589288941846559/855593817041403924/9Ky6.gif",
"https://cdn.discordapp.com/attachments/855589288941846559/855593824012206080/4afb2c9b1d06035d64db1a93ae78a16f.gif",
"https://cdn.discordapp.com/attachments/855589288941846559/855593829498093588/anime-slap-gif-20.gif",
"https://cdn.discordapp.com/attachments/855589288941846559/855593843553861632/OrneryFilthyArthropods-max-1mb.gif",
"https://cdn.discordapp.com/attachments/855589288941846559/855593844866416671/e83.gif",
"https://cdn.discordapp.com/attachments/855589288941846559/855593846804578304/Agwwaj6.gif"]

hug_gif_list=["https://cdn.discordapp.com/attachments/855595167707562055/855598055549829141/1.gif",
"https://cdn.discordapp.com/attachments/855595167707562055/855598065938857994/5.gif",
"https://cdn.discordapp.com/attachments/855595167707562055/855598070007595018/9.gif",
"https://cdn.discordapp.com/attachments/855595167707562055/855598071446896650/3.gif",
"https://cdn.discordapp.com/attachments/855595167707562055/855598074423803944/2.gif",
"https://cdn.discordapp.com/attachments/855595167707562055/855598075316797440/12.gif",
"https://cdn.discordapp.com/attachments/855595167707562055/855598077716725760/4.gif",
"https://cdn.discordapp.com/attachments/855595167707562055/855598083941597184/6.gif",
"https://cdn.discordapp.com/attachments/855595167707562055/855598091766726736/11.gif",
"https://cdn.discordapp.com/attachments/855595167707562055/855598097290625034/10.gif",
]
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
    embed_var = discord.Embed(title=f"**{ctx.author.name}** slaps **{member.name}**",description="Ouch... It hurts!",
                                color=0x36393f)
    embed_var.set_image(url=f"{choice(slap_gif_list)}")    
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
    embed_var = discord.Embed(title=f"**{ctx.author.name}** hugs **{member.name}**",description="Awwww, how cute! 😍",
                                color=0x36393f)
    embed_var.set_image(url=f"{choice(hug_gif_list)}")    
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

@slash.slash(name="Help", description="Returns all available commands", guild_ids=guild_ids)
async def help(ctx):
    embed=discord.Embed(title="✧═════•**COMMANDS LIST**•═════✧", description="If you want to **interact** with the **bot**, here are the **commands**.\n You must **keep** the **correct syntax** of the **command** for it to **work properly**", color=0x2f3136)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/848876190596071434/853409759918948382/6243-blurple-slashcommands.png")
    embed.add_field(name="NEWS COMMAND", value="*Return news on a given topic*\n**Usage** :\n ```/news topic```", inline=False)
    embed.add_field(name="HENTAI COMMAND", value="*Return a [gelbooru](https://gelbooru.com/) image on a given character or anime\n for the **command** to **work properly**, please **replace** any **space** in the **anime or character name** by an **underscore** like following : **_***\n**Usage** :\n ```/hentai characterName```\n```/hentai animeName```\n```/hentai characterName_(animeName)```\n", inline=True)
    embed.add_field(name="HUG COMMAND", value="*Hugs someone*\n**Usage** :\n ```/hug @mention```", inline=False)
    embed.add_field(name="SLAP COMMAND", value="*Slaps someone*\n**Usage** :\n ```/slap @mention```", inline=False)
    embed.add_field(name="WISDOM COMMAND", value="*Gives wisdom*\n**Usage** :\n ```/wisdom question```", inline=False)
    embed.add_field(name="PROFILE PIC COMMAND", value="*Returns someone's profile picture\n or the command caller's one if no user provided*\n**Usage** :\n ```/ppic @mention```", inline=False)
    await ctx.send(embed=embed)

@slash.slash(name="hentai", description="Returns hentai on a given topic", guild_ids=guild_ids)
async def GetHentai(ctx, tags):
    if ctx.channel.nsfw:
        print(tags)
        tags = tags.split(" ")
        print(tags)
        await ctx.defer()
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

async def cycle_presence():
    while True:
        await asyncio.sleep(20)
        await client.change_presence(activity=discord.Game(name=f"{choice(cycle_status)}"))


@client.event
async def on_ready():
    print('------------------')
    print('Logged as :')
    print(client.user.name)
    print(client.user.id)
    print('------------------')
    await client.change_presence(activity=discord.Game(name=f"{choice(cycle_status)}"))
    client.loop.create_task(cycle_presence())
    client.loop.create_task(membership_admission_button())

client.run(token)
