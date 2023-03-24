#Made by Ja'Crispy
#Please do not steal this code and call it yours
import discord
from discord.ext import commands
import os
import json
import time
import random
import datetime
import requests
import praw

start_time = datetime.datetime.now()

# Load economy data from economy.json
with open('economy.json', 'r') as f:
    economy = json.load(f)

# Initialize bot with a command prefix
client = discord.Client(intents=discord.Intents.default())
client = commands.Bot(command_prefix=".", intents=discord.Intents.all())

client.remove_command('help')  # Removes the default help command

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=".help"))

@client.command()
async def help(ctx):
    await ctx.send("**Fun**\n.meme\n.level\n.inspire\nmagic8ball (question here)\n.coinflip\n**Economy**\n.earn\n.balance\n.crime\n.gamble (amount here)\n**Useful**\n.serverinfo\n.userinfo @user\n.botinfo\n.uptime\n.sourcecode")

@commands.cooldown(1, 3600, commands.BucketType.user)
@client.command()
async def earn(ctx):
    user = str(ctx.author.id)
    if user not in economy:
        economy[user] = {'coins': 1000, 'commands_used': 0, 'level': 1}
    amount = random.randint(100, 300)
    economy[user]['coins'] += amount
    economy[user]['commands_used'] += 1
    current_level = economy[user]['level']
    required_commands = 10 * (current_level ** 2)
    if economy[user]['commands_used'] >= required_commands:
        economy[user]['level'] += 1
        economy[user]['coins'] += economy[user]['level'] * 100
        await ctx.send(f'Congratulations, you leveled up to level {economy[user]["level"]}!')
    await ctx.send(f'You earned {amount} coins')
    with open('economy.json', 'w') as f:
        json.dump(economy, f)

@commands.cooldown(1, 5400, commands.BucketType.user)
@client.command()
async def crime(ctx):
    user = str(ctx.author.id)
    if user not in economy:
        economy[user] = {'coins': 1000, 'commands_used': 0, 'level': 1}
    chance = random.randint(1, 100)
    if chance <= 30:
        amount = random.randint(1, 500)
        economy[user]['coins'] -= amount
        await ctx.send(f'You were caught in the crime and lost {amount} coins')
    else:
        amount = random.randint(300, 500)
        economy[user]['coins'] += amount
        await ctx.send(f'You successfully committed the crime and earned {amount} coins')
    economy[user]['commands_used'] += 1
    with open('economy.json', 'w') as f:
        json.dump(economy, f)

@client.command()
async def uptime(ctx):
    user = str(ctx.author.id)
    now = datetime.datetime.now()
    uptime = now - start_time
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    await ctx.send(f"Bot uptime: {uptime.days} days, {hours} hours, {minutes} minutes, and {seconds} seconds")
    economy[user]['commands_used'] += 1
    with open('economy.json', 'w') as f:
        json.dump(economy, f)

# Command to check your level
@client.command()
async def level(ctx):
    user = str(ctx.author.id)
    if user not in economy:
        economy[user] = {'coins': 1000, 'commands_used': 0, 'level': 1}
    current_level = economy[user]['level']
    commands_used = economy[user]['commands_used']
    required_commands = 10 * (current_level ** 2)
    next_level_commands = required_commands - commands_used
    await ctx.send(f'You are at level {current_level}, and have used {commands_used} commands. You need {next_level_commands} more commands to reach level {current_level+1}.')
    economy[user]['commands_used'] += 1
    with open('economy.json', 'w') as f:
        json.dump(economy, f)
        
# Command to check your balance
@client.command()
async def balance(ctx):
    user = str(ctx.author.id)
    if user not in economy:
        economy[user] = {'coins': 1000, 'commands_used': 0, 'level': 1}
    await ctx.send(f'You have {economy[user]["coins"]} coins')
    economy[user]['commands_used'] += 1
    with open('economy.json', 'w') as f:
        json.dump(economy, f)

# Command to gamble coins
@client.command()
async def gamble(ctx, amount: int):
    user = str(ctx.author.id)
    if user not in economy:
        economy[user] = {'coins': 1000, 'commands_used': 0, 'level': 1}
    if economy[user]['coins'] < amount:
        await ctx.send('You do not have enough coins')
        return
    result = random.choice(['win', 'lose'])
    if result == 'win':
        economy[user]['coins'] += amount
        await ctx.send(f'You won {amount} coins')
        with open('economy.json', 'w') as f:
            json.dump(economy, f)
    else:
        economy[user]['coins'] -= amount
        await ctx.send(f'You lost {amount} coins')
        with open('economy.json', 'w') as f:
            json.dump(economy, f)
    economy[user]['commands_used'] += 1
    with open('economy.json', 'w') as f:
        json.dump(economy, f)


@client.command()
async def poll(ctx, question, *options: str):
    user = str(ctx.author.id)
    """
    Creates a poll with the given question and options.
    Usage: !poll "What's your favorite color?" "Red" "Blue" "Green"
    """
    if not question:
        await ctx.send("You need to provide a question and at least 2 options. Usage: `.poll \"Question must be in quotation marks\" Option1 Option2 ...`")
        return
    if len(options) > 10:
        await ctx.send("You can only provide up to 10 options.")
        return

    if len(options) < 2:
        await ctx.send("You need to provide at least 2 options.")
        return

    # Create the poll message
    poll_message = f"**{question}**\n\n"

    for i, option in enumerate(options):
        emoji = chr(0x1f1e6 + i)  # A through J emoji
        poll_message += f"{emoji} {option}\n"

    poll_message += "\nReact to this message to vote!"

    # Send the poll message and add reactions to it
    message = await ctx.send(poll_message)

    for i in range(len(options)):
        emoji = chr(0x1f1e6 + i)  # A through J emoji
        await message.add_reaction(emoji)

    await ctx.message.delete()  # Delete the command message to keep the channel clean
    economy[user]['commands_used'] += 1
    with open('economy.json', 'w') as f:
        json.dump(economy, f)

@client.command()
async def magic8ball(ctx, *, question: str):
    user = str(ctx.author.id)
    responses = ['It is certain.', 'Without a doubt.', 'You may rely on it.', 'Yes, definitely.',
                 'It is decidedly so.', 'As I see it, yes.', 'Most likely.', 'Yes.',
                 'Outlook good.', 'Signs point to yes.', 'Reply hazy, try again.',
                 'Better not tell you now.', 'Ask again later.', 'Cannot predict now.',
                 'Concentrate and ask again.', 'Don’t count on it.', 'Outlook not so good.',
                 'My sources say no.', 'Very doubtful.', 'My reply is no.']
    response = random.choice(responses)
    embed = discord.Embed(title='Magic 8-Ball', description=response, color=0x00ff00)
    embed.set_footer(text=f'Question: {question}')
    await ctx.send(embed=embed)
    economy[user]['commands_used'] += 1
    with open('economy.json', 'w') as f:
        json.dump(economy, f)

@client.command()
async def inspire(ctx):
    user = str(ctx.author.id)
    response = requests.get('https://api.quotable.io/random')
    data = response.json()
    quote = data['content']
    author = data['author']
    embed = discord.Embed(title='Get Inspired', description=quote, color=0x00ff00)
    embed.set_footer(text=f'- {author}')
    await ctx.send(embed=embed)
    economy[user]['commands_used'] += 1
    with open('economy.json', 'w') as f:
        json.dump(economy, f)

@client.command()
async def botinfo(ctx):
    user = str(ctx.author.id)
    servers = len(client.guilds)
    commands = len(client.commands)
    author = "Ja'Crispy#3192"
    version = "1.0"
    #source_code = "[GitHub Repo Link Here]"

    embed = discord.Embed(title="Bot Information", color=0x00ff00)
    embed.add_field(name="Servers", value=servers, inline=False)
    embed.add_field(name="Commands", value=commands, inline=False)
    embed.add_field(name="Author", value=author, inline=False)
    embed.add_field(name="Version", value=version, inline=False)
    #embed.add_field(name="Source Code", value=source_code, inline=False)

    await ctx.send(embed=embed)
    economy[user]['commands_used'] += 1
    with open('economy.json', 'w') as f:
        json.dump(economy, f)

@client.command()
async def userinfo(ctx, member: discord.Member = None):
    user = str(ctx.author.id)
    member = member or ctx.author
    joined_at = member.joined_at.strftime("%b %d %Y %H:%M:%S")
    created_at = member.created_at.strftime("%b %d %Y %H:%M:%S")

    embed = discord.Embed(title=f"{member.display_name} Info", color=0x00ff00)
    embed.add_field(name="Nickname", value=member.nick or "None", inline=False)
    embed.add_field(name="Joined At", value=joined_at, inline=False)
    embed.add_field(name="Account Created At", value=created_at, inline=False)
    embed.add_field(name="Roles", value=', '.join([role.mention for role in member.roles if not role.is_default()]), inline=False)

    await ctx.send(embed=embed)
    economy[user]['commands_used'] += 1
    with open('economy.json', 'w') as f:
        json.dump(economy, f) 

@client.command()
async def serverinfo(ctx):
    user = str(ctx.author.id)
    server = ctx.guild
    channels = len(server.channels)
    members = len(server.members)
    roles = len(server.roles)
    owner = server.owner.name
    created_at = server.created_at.strftime("%b %d %Y %H:%M:%S")

    embed = discord.Embed(title=f"{server.name} Info", color=0x00ff00)
    embed.add_field(name="Owner", value=owner, inline=False)
    embed.add_field(name="Created At", value=created_at, inline=False)
    embed.add_field(name="Members", value=members, inline=False)
    embed.add_field(name="Channels", value=channels, inline=False)
    embed.add_field(name="Roles", value=roles, inline=False)

    await ctx.send(embed=embed)
    economy[user]['commands_used'] += 1
    with open('economy.json', 'w') as f:
        json.dump(economy, f)

reddit = praw.Reddit(client_id='',
                     client_secret='',
                     user_agent='myBot/0.0.1')

@client.command()
async def coinflip(ctx):
    user = str(ctx.author.id)
    result = random.choice(['Heads', 'Tails'])
    main_message = await ctx.send('Flipping Coin')
    time.sleep(.5)
    await main_message.edit(content="Flipping Coin.")
    time.sleep(.5)
    await main_message.edit(content="Flipping Coin..")
    time.sleep(.5)
    await main_message.edit(content="Flipping Coin...")
    time.sleep(.5)
    await main_message.edit(content=f"The coin landed on {result}")
    economy[user]['commands_used'] += 1
    with open('economy.json', 'w') as f:
        json.dump(economy, f)

@client.command()
async def meme(ctx):
    user = str(ctx.author.id)

    subreddit = reddit.subreddit('memes')
    posts = subreddit.hot(limit=100)
    random_post = random.choice(list(posts))
    image_url = random_post.url
    await ctx.channel.send(image_url)
    economy[user]['commands_used'] += 1
    with open('economy.json', 'w') as f:
        json.dump(economy, f)

@client.command()
async def sourcecode(ctx):
    user = str(ctx.author.id)
    url = 'https://github.com/JaCrispy4939/discord-bot'
    await ctx.send("This project is fully open source, just please dont steal the code.")
    await ctx.send(f'The code: {url}')
    economy[user]['commands_used'] += 1
    with open('economy.json', 'w') as f:
        json.dump(economy, f)

# Save economy data when bot shuts down
@client.event
async def on_shutdown():
    with open('economy.json', 'w') as f:
        json.dump(economy, f)

# Handle CommandOnCooldown exception
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        remaining = divmod(error.retry_after, 60)
        remaining_str = f"{int(remaining[0] // 60)} hours, {int(remaining[0] % 60)} minutes"
        await ctx.send(f"you can use that command again in {remaining_str}.")
    else:
        raise error

# Start the bot
print("Bot Online")
client.run('notsharingthis')
