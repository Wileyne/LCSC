import os
import requests
from dotenv import load_dotenv
from schemas import *
import sys

load_dotenv()
token = os.getenv("TOKEN")
base_url = os.getenv("BASE_URL")
header = {
    "Authorization": token,
}

session = requests.Session()
session.headers.update(header)

teams_id_by_name = dict()
matches_by_id = dict()
teams_by_id = dict()
statistic_team_by_name = dict()
players_by_id = dict()


def get_matches():
    url = base_url + "/matches"
    try:
        response = session.get(url)
        response.raise_for_status()
        r = response.json()
        for matches in r:
            id = matches["id"]
            team1 = matches["team1"]
            team2 = matches["team2"]
            team1_score = matches["team1_score"]
            team2_score = matches["team2_score"]
            match = Match(team1, team2, team1_score, team2_score)
            matches_by_id[id] = match
        return matches_by_id
    except requests.exceptions.RequestException as e:
        print(e)


def add_player_by_id(id):
    url = base_url + f"/players/{id}"
    try:
        response = session.get(url)
        response.raise_for_status()
        r = response.json()
        name = r["name"]
        surname = r["surname"]
        player = Player(name, surname)
        players_by_id[id] = player

    except requests.exceptions.RequestException as e:
        print(e)


def get_all_teams():
    url = base_url + "/teams"
    try:
        response = session.get(url)
        response.raise_for_status()
        r = response.json()
        for teams in r:
            id = teams["id"]
            name = teams["name"]
            teams_id_by_name[name] = id
            players = teams["players"]
            team = Team(name, players)
            teams_by_id[id] = team
            for player_id in players:
                if players_by_id.get(player_id) is None:
                    add_player_by_id(player_id)
    except requests.exceptions.RequestException as e:
        print(e)


def statistic_about_team(name):
    if not statistic_team_by_name.get(name) is None:
        statistic = statistic_team_by_name[name]
        print(*statistic)

    if teams_id_by_name.get(name) is None:
        print("0 0 0")
        return

    team_id = teams_id_by_name[name]
    cnt_win = 0
    cnt_loose = 0
    goals_balance = 0
    for id_matches in matches_by_id.keys():
        match = matches_by_id[id_matches]
        if match.get_id_team1() == team_id:
            if match.get_score_team1() > match.get_score_team2():
                cnt_win += 1
            elif match.get_score_team2() > match.get_score_team1():
                cnt_loose += 1
            goals_balance += match.get_score_team1()
            goals_balance -= match.get_score_team2()
        if match.get_id_team2() == team_id:
            if match.get_score_team1() > match.get_score_team2():
                cnt_loose += 1
            elif match.get_score_team2() > match.get_score_team1():
                cnt_win += 1
            goals_balance -= match.get_score_team1()
            goals_balance += match.get_score_team2()
    if (goals_balance >= 0):
        goals_balance = f"+{goals_balance}"
    else:
        goals_balance = f"{goals_balance}"
    statistic_team_by_name[name] = [cnt_win, cnt_loose, goals_balance]
    print(*statistic_team_by_name[name])


def print_all_players():
    res = []
    for i in players_by_id.keys():
        res.append(players_by_id[i])
    res.sort()
    for player in res:
        print(player.get_name(), player.get_surname())


def get_statistic_for_two_players(id_player1, id_player2):
    if players_by_id.get(id_player1) is None or players_by_id.get(id_player2) is None:
        print(0)

    cnt = 0
    for matches_id in matches_by_id.keys():
        if ((teams_by_id[matches_by_id[matches_id].get_id_team1()].find_player(id_player1) and
             teams_by_id[matches_by_id[matches_id].get_id_team2()].find_player(id_player2)) or
                (teams_by_id[matches_by_id[matches_id].get_id_team1()].find_player(id_player2) and
                 teams_by_id[matches_by_id[matches_id].get_id_team2()].find_player(id_player1))
        ):
            cnt += 1
    print(cnt)


if __name__ == "__main__":

    get_all_teams()
    get_matches()
    print_all_players()

    for line in sys.stdin:
        query = line.split()
        if len(query) == 0:
            continue
        if query[0] == "stats?":
            team_name = ""
            for i in range(1, len(query)):
                if (i == 1 and len(query) - 1 == i):
                    team_name += query[i][1:-1]
                elif (i == 1):
                    team_name += query[i][1:] + " "
                elif i == len(query) - 1:
                    team_name += query[i][:-1]
                else:
                    team_name += query[i]
                    team_name += " "
            statistic_about_team(team_name)
        elif query[0] == "versus?":
            get_statistic_for_two_players(int(query[1]), int(query[2]))
        else:
            print("incorrect query")


