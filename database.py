import sqlite3
from scraper import Game


con = sqlite3.connect('valesportsbot.db')
cur = con.cursor()


def user_exists(user_id: int) -> bool:
    res = list(cur.execute(f'SELECT 1 FROM users WHERE ID={user_id}'))
    return False if not res else True


def add_user(user_id: int):
    cur.execute(f'INSERT INTO users VALUES ({user_id}, 1000) ON CONFLICT (ID) DO NOTHING')
    con.commit()


def add_ongoing_game(game_id: int):
    cur.execute(f'INSERT INTO games VALUES ({game_id}) ON CONFLICT (game_id) DO NOTHING')


def get_ongoing_games():
    return list(x[0] for x in cur.execute('SELECT * from games'))


def is_ongoing_game(game_id: int) -> bool:
    games = list(cur.execute(f'SELECT (game_id) from games WHERE game_id={game_id}'))
    if games:
        return True
    else:
        return False


def remove_game(game_id: int):
    cur.execute(f'DELETE FROM games WHERE game_id={game_id}')
    con.commit()


def get_balance(user_id: int) -> int:
    value = cur.execute(f'SELECT (balance) from users WHERE ID={user_id}')
    return list(value)[0][0]


def add_balance(user_id: int, amount: int) -> None:
    cur.execute(f'UPDATE users SET balance=balance+{amount} WHERE ID={user_id}')
    con.commit()


def subtract_balance(user_id: int, amount: int) -> None:
    cur.execute(f'UPDATE users SET balance=balance-{amount} WHERE ID={user_id}')
    con.commit()


def add_bet(game_id: int, user_id: int, team: int, amount: int) -> bool:
    if get_balance(user_id) < amount:
        return False
    subtract_balance(user_id, amount)
    cur.execute(f'INSERT INTO bet VALUES ({game_id}, {user_id}, {team}, {amount})')
    con.commit()
    return True


def get_bets(game_id: int):
    return list(cur.execute(f'SELECT * FROM bet WHERE game_id={game_id}'))


def clear_bets(game_id: int):
    cur.execute(f'DELETE FROM bet WHERE game_id={game_id}')
    con.commit()


def payout_bets(game_id: int, winner: int) -> list[str]:
    outcomes = []
    bets = get_bets(game_id)
    for bet in bets:
        if bet[2] == winner:
            add_balance(bets[1], bets[3] * 2)
    return outcomes


# TODO: Add database functions for seeing when the user last claimed a daily reward
