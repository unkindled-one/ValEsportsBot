import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dataclasses import dataclass


@dataclass
class Game:
    """Class that represents an upcoming valorant esports game"""
    id: int
    url: str
    team1: str
    team2: str
    time: datetime

    def get_time_to_game(self) -> timedelta:
        return self.time - datetime.now()


async def get_upcoming_games() -> list[Game]:
    """Gets a list of all upcoming games to notify the guilds of"""
    event_urls = await get_events()
    upcoming_games = []
    for event_url in event_urls:
        games = await get_games(event_url)
        upcoming_games.extend(games)
    return upcoming_games


async def get_events(starting_url: str = 'https://www.vlr.gg/events') -> list[str]:
    """Gets a list of links to the match lists of major events on https://www.vlr.gg/events"""
    base_url = 'https://www.vlr.gg/event/matches'
    events = []
    html = requests.get(starting_url).text
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a', {'class': 'wf-card mod-flex event-item'}, href=True)
    for link in links:
        if 'champions-tour' not in link['href'] or link.find('span').text != 'ongoing':
            continue
        events.append(base_url + link['href'][6:] + '/?group=upcoming')
    return events


async def get_games(event_url: str) -> list[Game]:
    """Given an event on https://www.vlr.gg, get all games in that event"""
    html = requests.get(event_url).text
    soup = BeautifulSoup(html, 'html.parser')
    game_css_class_1 = 'wf-module-item match-item mod-color mod-left mod-bg-after-orange mod-first'
    game_css_class_2 = 'wf-module-item match-item mod-color mod-left mod-bg-after-orange'
    game_htmls = soup.find_all('a', {'class': [game_css_class_1, game_css_class_2]})
    games = []
    for game in game_htmls:
        eta = game.find('div', {'class': 'ml-eta'})
        # Filters all games further than an hour away
        if eta is None or len(eta.text.split()) != 1 or 'm' not in eta.text:
            continue
        names = game.find_all('div', {'class': 'match-item-vs-team-name'})
        time = datetime.strptime(game.find('div', {'class': 'match-item-time'}).text.strip(), '%I:%M %p')
        now = datetime.now()
        time = time.replace(day=now.day, year=now.year, month=now.month)
        game_id = game['href'].split('/')[1]
        url = 'https://www.vlr.gg' + game['href']
        games.append(Game(game_id, url, names[0].text.strip(), names[1].text.strip(), time))
    return games


async def get_game_winner(game: Game):
    # TODO: Implement checking the winner of a game
    pass
