import os
from discord.ext import commands
from dotenv import load_dotenv
import discord

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("!"),
    intents=discord.Intents.all(),
)

@bot.event
async def on_ready():
    guilds = bot.guilds
    print()
    print("Logged in as " + bot.user.name)
    print("Bot is in " + str(len(guilds)) + " guilds")
    print()
    await bot.change_presence(status= discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="over the server"))


# load cogs
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

if __name__ == "__main__":
    load_dotenv()
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    bot.run(BOT_TOKEN)