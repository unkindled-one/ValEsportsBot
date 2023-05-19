import os
from dotenv import load_dotenv
import discord


class Bot(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}')


if __name__ == '__main__':
    load_dotenv('.env')
    token = os.getenv('TOKEN')
    bot = Bot(intents=discord.Intents.default())
    bot.run(token)
