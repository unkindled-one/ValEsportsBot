import os
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks


class Bot(discord.Client):
    async def on_ready(self):
        """Runs as soon as the bot starts"""
        print(f'Logged on as {self.user}')

    @tasks.loop(minutes=1)
    async def send_upcoming(self):
        """Sends the upcoming games"""
        raise NotImplementedError()

    async def get_upcoming(self):
        """Gets the upcoming games to send to the servers"""
        raise NotImplementedError()


if __name__ == '__main__':
    load_dotenv('.env')
    token = os.getenv('TOKEN')
    bot = Bot(intents=discord.Intents.default())
    bot.run(token)
