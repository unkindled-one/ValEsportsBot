import os
from discord import app_commands
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
from scraper import get_upcoming_games, Game


intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='/', intents=intents)


@client.event
async def on_ready() -> None:
    """Syncs commands and starts tasks when the bot starts up"""
    print(f'Logged on as {client.user}')
    try:
        synced = await client.tree.sync()
        print(f'synced {len(synced)} commands')
    except Exception as e:
        print(e)
    send_upcoming.start()


@tasks.loop(minutes=1)
async def send_upcoming() -> None:
    """Sends the upcoming games to the guilds."""
    games = await get_upcoming_games()
    for guild in client.guilds:
        channel = await get_channel(guild)
        for game in games:
            await channel.send(await create_game_embed(game))


async def get_channel(guild: discord.Guild) -> discord.TextChannel:
    """Get the bot specific channel from the guild, if the channel does not exist it creates one and returns the ID."""
    text_channel = None
    for channel in guild.text_channels:
        if channel.name == 'ValEsportsBot':
            text_channel = channel
    if text_channel is None:
        text_channel = await guild.create_text_channel('ValEsportsBot')
    return text_channel


async def create_game_embed(game: Game) -> None:
    """Creates a discord embed based on the game."""
    pass


@client.tree.command(name='bet')
@app_commands.describe(amount='amount', team='team')
async def make_bet(interaction: discord.Interaction, amount: int, match_number: int, team_number: int) -> None:
    # Make a bet, double amount if correct half it otherwise
    # Keeps a database table with all bets, when the game is finished, pay out
    raise NotImplementedError()


@client.tree.command(name='balance')
async def balance(interaction: discord.Interaction) -> None:
    """Gets the balance of the user from the database."""
    pass


load_dotenv('.env')
token = os.getenv('TOKEN')
client.run(token)
