import discord
from discord.ext import commands
import requests

def ask_ollama(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3", "prompt": prompt, "stream": False}
        )
        data = response.json()
        return data["results"][0]["content"]
    except Exception as e:
        return f"Error: {e}"


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# ------------------ EVENTS ------------------

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.lower()

    if "hello" in content:
        await message.channel.send("Hey there! 👋")

    elif "how are you" in content:
        await message.channel.send("I'm just a bot, but I'm doing great!")

    elif "bye" in content:
        await message.channel.send("See you later!")

    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if channel:
        await channel.send(f"Welcome to the server, {member.mention}!")

# ------------------ COMMANDS ------------------

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def ai(ctx, *, prompt):
    await ctx.send("Thinking...")
    reply = ask_ollama(prompt)
    await ctx.send(reply)

# ------------------ RUN BOT ------------------

bot.run('Here')  # Put your token here
