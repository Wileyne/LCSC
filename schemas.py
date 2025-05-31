class Player:
    def __init__(self, name, surname):
        self.__name = name
        self.__surname = surname

    def get_name(self):
        return self.__name

    def get_surname(self):
        return self.__surname

    def __lt__(self, other):
        return self.__name < other.get_name()

    def __hash__(self):
        return (self.__name, self.__surname).__hash__()


class Team:
    def __init__(self, name, players: list):
        self.__name = name
        self.__players = set(players)

    def get_name(self):
        return self.__name

    def find_player(self, player_id):
        return player_id in self.__players


class Match:
    def __init__(self, team1, team2, score_team1, score_team2):
        self.__id_team1 = team1
        self.__id_team2 = team2
        self.__score_team1 = score_team1
        self.__score_team2 = score_team2

    def get_id_team1(self):
        return self.__id_team1

    def get_id_team2(self):
        return self.__id_team2

    def get_score_team1(self):
        return self.__score_team1

    def get_score_team2(self):
        return self.__score_team2

