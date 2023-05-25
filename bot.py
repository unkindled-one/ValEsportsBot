import os
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
from scraper import get_upcoming_games, Game
import database as db


intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='/', intents=intents)
val_color = discord.Color.from_rgb(250, 64, 84)

sent_embeds: list = list()
matches: dict = dict()


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
    payout_bets.start()


@tasks.loop(minutes=1)
async def send_upcoming() -> None:
    """Sends the upcoming games to the guilds."""
    games = await get_upcoming_games()
    for guild in client.guilds:
        channel = await get_channel(guild)
        for game in games:
            await channel.send(await create_game_embed(game))


@tasks.loop(minutes=1)
async def payout_bets() -> None:
    pass


async def get_channel(guild: discord.Guild) -> discord.TextChannel:
    """Get the bot specific channel from the guild, if the channel does not exist it creates one and returns the ID."""
    text_channel = None
    for channel in guild.text_channels:
        if channel.name == 'valesportsbot':
            text_channel = channel
    if text_channel is None:
        text_channel = await guild.create_text_channel('valesportsbot')
    return text_channel


async def create_game_embed(game: Game) -> None:
    """Creates a discord embed based on the game."""
    pass


@client.tree.command(name='bet')
async def make_bet(interaction: discord.Interaction, amount: int, match_number: int, team_number: int) -> None:
    # Make a bet, double amount if correct half it otherwise
    # Keeps a database table with all bets, when the game is finished, pay out
    # TODO: Add check to see if match actually exists
    if not db.user_exists(interaction.user.id):
        db.add_user(interaction.user.id)
    result = db.add_bet(match_number, interaction.user.id, team_number, amount)
    if not result:
        embed = discord.Embed(title=f'You have insufficient credits to make this bet', color=val_color)
    else:
        embed = discord.Embed(title=f'{amount} credits placed on {team_number}', color=val_color)
    await interaction.response.send_message(embed=embed)


@client.tree.command(name='balance')
async def balance(interaction: discord.Interaction) -> None:
    """Returns the number of credits in your account"""
    if not db.user_exists(interaction.user.id):
        db.add_user(interaction.user.id)
    bal = db.get_balance(interaction.user.id)
    embed = discord.Embed(title=f'You have {bal} credits', color=val_color)
    await interaction.response.send_message(embed=embed, ephemeral=True)


load_dotenv('.env')
token = os.getenv('TOKEN')
client.run(token)
