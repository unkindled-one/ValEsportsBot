import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


class Game:
    """Class that represents an upcoming valorant esports game"""
    def __init__(self, team1: str, team2: str, time: datetime):
        self.team1: str = team1
        self.team2: str = team2
        self.time: datetime = time

    def get_time_to_game(self) -> timedelta:
        return datetime.now() - self.time


async def get_upcoming_games():
    """Gets a list of all upcoming games to notify the guilds of"""
    raise NotImplementedError()


async def get_events(starting_url: str) -> list[str]:
    """Gets a list of links to the top 5 events on https://www.vlr.gg/events"""
    raise NotImplementedError()


async def get_games(event_url: str) -> list[Game]:
    raise NotImplementedError()


if __name__ == '__main__':
    # Prototype scraping
    h = requests.get('https://www.vlr.gg/event/matches/1189/champions-tour-2023-americas-league/').text
    soup = BeautifulSoup(h, 'html.parser')
    div_data = soup.find_all('div', {'class': 'match-item-vs'})
    for div in div_data:
        team1 = None
        team2 = None
        for child in div.find_all('div', recursive=False):
            # Get rid of whitespace padding
            child_team = list(map(lambda x: x.strip(), child.text.rsplit(None, 1)[:]))
            print(child_team)
            # print(f'"{child.text.rsplit(None, 1)[:]}"')
