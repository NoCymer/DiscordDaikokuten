import discord
from discord.ext import commands
import asyncio
from assets import news_api
from assets import nsfw_api
time_sleep_const = 10


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()
client = commands.Bot(command_prefix='!')


async def wait_and_delete_msgs(ctx, bot_msg):
    await asyncio.sleep(time_sleep_const)
    try:
        await ctx.message.delete()
    except discord.errors.NotFound:
        pass
    try:
        await bot_msg.delete()
    except discord.errors.NotFound:
        pass


@client.command()
async def news(ctx, *, arg):
    try:
        await ctx.reply('Here is the news : ' + news_api.getnews(arg), mention_author=False)
    except IndexError:
        bot_msg = await ctx.reply(
            "Sorry no news have been found for this given subject ¯\_(ツ)_/¯", mention_author=False)
        await wait_and_delete_msgs(ctx, bot_msg)


@client.command()
async def hentai(ctx, *, arg):
    if ctx.channel.nsfw:
        await ctx.reply('Here is the sauce : ' + await nsfw_api.get_hentai(arg), mention_author=False)
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
    bot_msg = await ctx.channel.send(f'{str(counter)} Messages from {member.display_name} have been deleted')
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

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#     else:
#         await process_command(message)


@client.event
async def on_ready():
    print('------------------')
    print('Logged as :')
    print(client.user.name)
    print(client.user.id)
    print('------------------')
    await client.change_presence(activity=discord.Game(name="rule over the world"))


client.run(token)
