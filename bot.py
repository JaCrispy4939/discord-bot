#Made by Ja'Crispy
#Please do not steal this code and call it yours
import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
import os
import json
import time
import random
import datetime
import requests
import praw
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import wolframalpha
import asyncio
from craiyon import Craiyon
from craiyon import Craiyon, craiyon_utils
import base64


start_time = datetime.datetime.now()


with open('economy.json', 'r') as f:
    economy = json.load(f)

with open('config.json', 'r') as f:
    config = json.load(f)

with open('stats.json', 'r') as f:
    stats = json.load(f)


client = discord.Client(intents=discord.Intents.default())
client = commands.Bot(command_prefix=".", intents=discord.Intents.all())

client.remove_command('help')  

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=".help"))

@client.command()
async def help(ctx):
    await ctx.send("**Fun**\n.image (promt)\n.meme\n.gif term\n.trivia\n.mystats\n.level\n.inspire\nmagic8ball (question here)\n.coinflip\n.quote\n.fact\n**Economy**\n.earn\n.blackjack (amount)\n.balance\n.crime\n.gamble (amount here)\n**Useful**\n.serverinfo\n.userinfo @user\n.botinfo\n.uptime\n.sourcecode\n**Moderation**\n.clear (amount)\n.kick @user\n.mute @user\n.unmute @user\n")

@commands.cooldown(1, 3600, commands.BucketType.user)
@client.command()
async def earn(ctx):
    user = str(ctx.author.id)
    if user not in economy:
        economy[user] = {'username': ctx.message.author.name, 'coins': 1000, 'commands_used': 0, 'level': 1}
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

@client.command()
async def leaderboard(ctx):
    
    data = economy
    sorted_data = sorted(data.items(), key=lambda x: x[1].get('level', 0), reverse=True)

    
    leaderboard_message = "**Leaderboard:**\n"
    for i, (user_id, data) in enumerate(sorted_data[:10]): # Only display top 10 users
        
        user_name = data.get('username', 'Unknown')

        leaderboard_message += f"{i+1}. {user_name}: Level {data.get('level', 0)} - {data.get('commands_used', 0)} commands used\n"
        
    
    await ctx.send(leaderboard_message)
    user = str(ctx.author.id)
    economy[user]['commands_used'] += 1
    with open('economy.json', 'w') as f:
        json.dump(economy, f)

@commands.cooldown(1, 5400, commands.BucketType.user)
@client.command()
async def crime(ctx):
    user = str(ctx.author.id)
    if user not in economy:
        economy[user] = {'username': ctx.message.author.name, 'coins': 1000, 'commands_used': 0, 'level': 1}
    amount = random.randint(100, 300)
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


@client.command()
async def level(ctx):
    user = str(ctx.author.id)
    if user not in economy:
        economy[user] = {'username': ctx.message.author.name, 'coins': 1000, 'commands_used': 0, 'level': 1}
    current_level = economy[user]['level']
    commands_used = economy[user]['commands_used']
    required_commands = 10 * (current_level ** 2)
    next_level_commands = required_commands - commands_used
    await ctx.send(f'You are at level {current_level}, and have used {commands_used} commands. You need {next_level_commands} more commands to reach level {current_level+1}.')
    economy[user]['commands_used'] += 1
    with open('economy.json', 'w') as f:
        json.dump(economy, f)
        

@client.command()
async def balance(ctx):
    user = str(ctx.author.id)
    if user not in economy:
        economy[user] = {'username': ctx.message.author.name, 'coins': 1000, 'commands_used': 0, 'level': 1}
    await ctx.send(f'You have {economy[user]["coins"]} coins')
    economy[user]['commands_used'] += 1
    with open('economy.json', 'w') as f:
        json.dump(economy, f)


@client.command()
async def gamble(ctx, amount: int):
    user = str(ctx.author.id)
    if user not in economy:
        economy[user] = {'username': ctx.message.author.name, 'coins': 1000, 'commands_used': 0, 'level': 1}
    if amount is None:
        ctx.send("You need to specify the amount of coins you want to gamble!\nExample: .gamble 300")
        return
    if amount == 0:
        await ctx.send("You cant gamble with 0 coins!")
        return
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

    
    poll_message = f"**{question}**\n\n"

    for i, option in enumerate(options):
        emoji = chr(0x1f1e6 + i)  
        poll_message += f"{emoji} {option}\n"

    poll_message += "\nReact to this message to vote!"

    
    message = await ctx.send(poll_message)

    for i in range(len(options)):
        emoji = chr(0x1f1e6 + i)  
        await message.add_reaction(emoji)

    await ctx.message.delete()  
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
    version = "1.4"
    #source_code = "[]"

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

reddit = praw.Reddit(client_id=config['redditclientid'],
                     client_secret=config['redditclientseceret'],
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

INSPIROBOT_API_URL = "https://inspirobot.me/api?generate=true"

@client.command()
async def quote(ctx):
    user = str(ctx.author.id)

    response = requests.get(INSPIROBOT_API_URL)
    if response.status_code == 200:
        image_url = response.text.strip()
    else:
        await ctx.send("Sorry, I cant get a quote right now")
        return

    image_data = requests.get(image_url).content

    file = discord.File(BytesIO(image_data), filename="inspirobot.jpg")
    await ctx.send(file=file)
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

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    user = str(ctx.author.id)
    if ctx.author == member:
        await ctx.send("You can't kick yourself!")
        return
    if ctx.guild.owner == member:
        await ctx.send("You can't kick the server owner!")
        return
    if not ctx.me.guild_permissions.kick_members:
        await ctx.send("I don't have the necessary permissions to kick users.")
        return

    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} has been kicked from the server.")
    economy[user]['commands_used'] += 1
    with open('economy.json', 'w') as f:
        json.dump(economy, f)

@client.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    user = str(ctx.author.id)
    if ctx.author == member:
        await ctx.send("You can't mute yourself!")
        return

    if ctx.guild.owner == member:
        await ctx.send("You can't mute the server owner!")
        return

    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not muted_role:
        muted_role = await ctx.guild.create_role(name="Muted")

        for channel in ctx.guild.channels:
            await channel.set_permissions(muted_role, speak=False, send_messages=False)
        await ctx.send('There was no role called "Muted", So I made one for you with the correct permissions!')
    await member.add_roles(muted_role, reason=reason)
    await ctx.send(f"{member.mention} has been muted.")
    economy[user]['commands_used'] += 1
    with open('economy.json', 'w') as f:
        json.dump(economy, f)

@client.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    user = str(ctx.author.id)
    if ctx.author == member:
        await ctx.send("You can't unmute yourself!")
        return
    if ctx.guild.owner == member:
        await ctx.send("You can't unmute the server owner!")
        return
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not muted_role:
        await ctx.send("There's no Muted role to remove.")
        return

    await member.remove_roles(muted_role)
    await ctx.send(f"{member.mention} has been unmuted.")
    economy[user]['commands_used'] += 1
    with open('economy.json', 'w') as f:
        json.dump(economy, f)

@client.command()
@commands.check_any(commands.is_owner(), commands.has_permissions(administrator=True))
async def clear(ctx, amount: int):
    user = str(ctx.author.id)
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"Cleared {amount} messages!")
    time.sleep(1)
    await ctx.channel.purge(limit=1)
    economy[user]['commands_used'] += 1
    with open('economy.json', 'w') as f:
        json.dump(economy, f)

@client.command()
async def fact(ctx):
    user = str(ctx.author.id)
    response = requests.get('https://uselessfacts.jsph.pl/random.json?language=en')

    fact = response.json()['text']

    await ctx.send(fact)

    economy[user]['commands_used'] += 1
    with open('economy.json', 'w') as f:
        json.dump(economy, f)

@client.command()
async def gif(ctx, search_term):
        user = str(ctx.author.id)
        gifapikey = config['gifapi']
            
        response = requests.get(f'https://api.giphy.com/v1/gifs/search?q={search_term}&api_key={gifapikey}&limit=1')
        
        data = response.json()['data']
        if len(data) > 0:
            
            gif_url = data[0]['images']['original']['url']
            
            await ctx.send(gif_url)
        else:
            
            await ctx.send('Sorry, I couldn\'t find a GIF for that search term.')
        
        economy[user]['commands_used'] += 1
        with open('economy.json', 'w') as f:
            json.dump(economy, f)



app_id = config['wolframid']


wolframclient = wolframalpha.Client(app_id)
@client.command()
async def wolfram(ctx, *,question):
    user = str(ctx.author.id)
    res = wolframclient.query(question)
    
    
    try:
        
        answer = next(res.results).text
        
        
        await ctx.send(answer)
    except StopIteration:
        
        await ctx.send("Sorry, I couldn't find an answer to that question.")
        economy[user]['commands_used'] += 1
        with open('economy.json', 'w') as f:
            json.dump(economy, f)

@client.command()
async def remind(ctx, time, *, reminder):
    user = str(ctx.author.id)
    await ctx.send(f"Okay, I will remind you to {reminder} in {time}.")
    time = time.lower()

    if time.endswith("s"):
        seconds = int(time[:-1])
    elif time.endswith("m"):
        seconds = int(time[:-1]) * 60
    elif time.endswith("h"):
        seconds = int(time[:-1]) * 3600
    elif time.endswith("d"):
        seconds = int(time[:-1]) * 86400
    else:
        await ctx.send("Sorry, I didn't understand the time format. Please use seconds (s), minutes (m), hours (h), or days (d).")
        return

    await asyncio.sleep(seconds)
    await ctx.send(f"{ctx.author.mention}, you asked me to remind you to {reminder} {time} ago.")
    economy[user]['commands_used'] += 1
    with open('economy.json', 'w') as f:
        json.dump(economy, f)


@client.command()
async def trivia(ctx):
    user = str(ctx.author.id)
    if user not in economy:
        economy[user] = {'username': ctx.message.author.name, 'coins': 1000, 'commands_used': 0, 'level': 1}
    trivia_api_url = "https://opentdb.com/api.php?amount=1&type=boolean"
    response = requests.get(trivia_api_url)
    data = json.loads(response.text)

    # Extract the question and answer from the API response
    question = data["results"][0]["question"]
    correct_answer = data["results"][0]["correct_answer"]
    
    # Send the question to the chat
    await ctx.send(f"Here's your question: True or False, {question}")
    
    # Wait for the user to answer
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    
    user_answer = await client.wait_for('message', check=check)
    
    # Check if the user's answer is correct and display the result in the chat
    if user_answer.content.lower() == correct_answer.lower():
        coinwinamount = random.randint(20, 70)
        await ctx.send(f"Congratulations! You got it right.\nYou won {coinwinamount} Coins!")
        economy[user]['coins'] += coinwinamount
        if user not in stats:
            stats[user] = {'username': ctx.message.author.name, 'triviawins': 0, 'blackjackwins': 0}

        stats[user]['triviawins'] += 1
        with open('stats.json', 'w') as f:
            json.dump(stats, f)
    else:
        await ctx.send(f"Sorry, the correct answer was {correct_answer}.\nYou did not win any Coins.")
    economy[user]['commands_used'] += 1
    with open('economy.json', 'w') as f:
        json.dump(economy, f)

@client.command()
async def mystats(ctx):
    user = str(ctx.author.id)
    if user not in stats:
        stats[user] = {'username': ctx.message.author.name, 'triviawins': 0, 'blackjackwins': 0}

    triviawincount = stats[user]['triviawins']
    blackjackwincount = stats[user]['blackjackwins']
    usersname = stats[user]['username']

    await ctx.send(f"**Stats for {usersname}**\nTrivia Wins: {triviawincount}\nBlackjack Wins: {blackjackwincount}")

    economy[user]['commands_used'] += 1
    with open('economy.json', 'w') as f:
        json.dump(economy, f)


@client.command()
async def blackjack(ctx, amount: int):
    user = str(ctx.author.id)
    if user not in economy:
        economy[user] = {'username': ctx.message.author.name, 'coins': 1000, 'commands_used': 0, 'level': 1}
    if amount == 0:
        await ctx.send("You cant play with 0 coins!")
        return
    if economy[user]['coins'] < amount:
        await ctx.send('You do not have enough coins')
        return

    deck = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] * 4
    random.shuffle(deck)

    player_hand = []
    bot_hand = []


    def calculate_hand(hand):
        value = 0
        aces = 0
        for card in hand:
            if card == 'A':
                aces += 1
            elif card in ['J', 'Q', 'K']:
                value += 10
            else:
                value += int(card)
        for i in range(aces):
            if value + 11 <= 21:
                value += 11
            else:
                value += 1
        return value


    player_hand.append(deck.pop())
    bot_hand.append(deck.pop())
    player_hand.append(deck.pop())
    bot_hand.append(deck.pop())


    await ctx.send(f"Your hand: {' '.join(player_hand)} Total: {calculate_hand(player_hand)}\nBot's hand: [{bot_hand[0]},] Total: {calculate_hand(bot_hand)} \nType hit or stand in chat")


    if calculate_hand(player_hand) == 21:
        await ctx.send("Blackjack! You win!")
        return


    while True:
        def check_hit_or_stand(message):
            return message.author == ctx.author and message.content.lower() in ['hit', 'stand']
        action_message = await client.wait_for('message', check=check_hit_or_stand)
        action = action_message.content.lower()
        if action == 'hit':
            player_hand.append(deck.pop())
            await ctx.send(f"You drew a {player_hand[-1]}.\nYour hand: {player_hand} Total: {calculate_hand(player_hand)}\nBot's hand: [{bot_hand[0]},] Total: {calculate_hand(bot_hand)}\nType hit or stand in chat")
            if calculate_hand(player_hand) > 21:
                await ctx.send("Bust! You lose.")
                await ctx.send(f"You lost {amount} coins!")
                economy[user]['coins'] -= amount
                return
        elif action == 'stand':
            break


    while calculate_hand(bot_hand) < 17:
        bot_hand.append(deck.pop())
    await ctx.send(f"Bot's hand: {bot_hand} Total: {calculate_hand(bot_hand)}")


    player_value = calculate_hand(player_hand)
    bot_value = calculate_hand(bot_hand)
    if player_value > bot_value or bot_value > 21:
        await ctx.send("You win!")
        if user not in stats:
            stats[user] = {'username': ctx.message.author.name, 'triviawins': 0, 'blackjackwins': 0}
        stats[user]['blackjackwins'] += 1

        economy[user]['coins'] += amount
        await ctx.send(f'You won {amount} coins')

    elif player_value == bot_value:
        await ctx.send("It's a tie!")
        await ctx.send("You got your coins back!")
    else:
        await ctx.send("You lose.")
        await ctx.send(f"You lost {amount} coins!")
        economy[user]['coins'] -= amount
    economy[user]['commands_used'] += 1
    with open('economy.json', 'w') as f:
        json.dump(economy, f)

    with open('stats.json', 'w') as f:
        json.dump(stats, f)
    with open('economy.json', 'w') as f:
        json.dump(economy, f)

generator = Craiyon() # Initialize Craiyon() class
@client.command()
async def image(ctx, *, prompt: str):
    user = str(ctx.author.id)
    await ctx.send(f"Please wait, this may take a minute or two\nGenerating prompt \"{prompt}\"...")
    
    generated_images = await generator.async_generate(prompt) 
    b64_list = await craiyon_utils.async_encode_base64(generated_images.images) # Download images from https://img.craiyon.com and store them as b64 bytestring object
    
    images1 = []
    for index, image in enumerate(b64_list): # Loop through b64_list, keeping track of the index
        img_bytes = BytesIO(base64.b64decode(image)) # Decode the image and store it as a bytes object
        image = discord.File(img_bytes)
        image.filename = f"result{index}.webp"
        images1.append(image) # Add the image to the images1 list
        
    await ctx.reply(files=images1) # Reply to the user with all 9 images in 1 message
    economy[user]['commands_used'] += 1
    with open('economy.json', 'w') as f:
        json.dump(economy, f)



def get_word_of_the_day():
    api_key = config['websterdictkey']
    url = f'https://www.dictionaryapi.com/api/v3/references/collegiate/json/wotd?key={api_key}'
    # Send a GET request to the Merriam-Webster API to fetch the word of the day
    response = requests.get(url)

    # Convert the response to a JSON object
    data = json.loads(response.text)

    # Extract the word and its definition from the JSON object
    word = data[0]['meta']['id']
    definition = data[0]['def'][0]['sseq'][0][0][1]['dt'][0][1]

    # Format the response string
    response_str = f'Word of the day: **{word.capitalize()}**\nDefinition: {definition}'

    return response_str

# Example command function
@client.command()
async def word(ctx):
    # Call the get_word_of_the_day function to fetch the word of the day
    response = get_word_of_the_day()

    # Send the response back to the Discord channel or user
    await ctx.send(response)

# Save all data when bot shuts down
@client.event
async def on_shutdown():
    with open('economy.json', 'w') as f:
        json.dump(economy, f)
    with open('stats.json', 'w') as f:
        json.dump(stats, f)

# Handle CommandOnCooldown exception
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        remaining = divmod(error.retry_after, 60)
        remaining_str = f"{int(remaining[0] // 60)} hours, {int(remaining[0] % 60)} minutes"
        await ctx.send(f"you can use that command again in {remaining_str}.")
    else:
        raise error
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Sorry, you need administrator permissions to use this command.")

# Start the bot
print("Bot Online")
client.run(config['token'])
