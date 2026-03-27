import random
import os
import json
from datetime import datetime
from typing import List
from models.player import Player
from models.match import Match
from models.round import Round


class Tournament:
    """ Tournament class """
    def __init__(self, name: str, location: str, start_date: datetime, end_date: datetime, rounds: int = 4):
        """
        Initializes a tournament with parameters :
        :param name(str): tournament name
        :param location(str): tournament location
        :param start_date: start date of the tournament
        :param end_date: end date of the tournament
        :param rounds: number of rounds. By default, 4

        us 2.1 creation tournament with base parameters
        us 2.2 add players to a tournament
        us 2.3 random generation of the first round
        us 3.4 generate next round by score
        US 4.1 Saves the tournament to a JSON file.
        US 4.2 Load the tournament from a JSON file.
        """
        if end_date < start_date:
            raise ValueError("End date must be after start date")
        self._name = name
        self._location = location
        self._start_date = start_date
        self._end_date = end_date
        self._rounds = rounds
        self._players: List[Player] = []
        self._rounds_list: List = []
        self._id_tournament = self._generate_id()

    # dattributs read-only
    @property
    def name(self) -> str:
        return self._name

    @property
    def location(self) -> str:
        return self._location

    @property
    def start_date(self) -> datetime:
        return self._start_date

    @property
    def end_date(self) -> datetime:
        return self._end_date

    @property
    def rounds(self) -> int:
        return self._rounds

    def _generate_id(self):
        "Generates a unique id for this tournament"
        # takes 3 first characters from name and if necessary completing with '_'
        name_part = self.name.strip()[:3].lower()
        if len(name_part) < 3:
            name_part = name_part.ljust(3, '_')
        # takes 3 first characters from location and if necessary completing with '_'
        location_part = self.location.strip()[:3].lower()
        if len(location_part) < 3:
            location_part = location_part.ljust(3, '_')
        # date without spaces
        date_part = self.start_date.strftime("%Y%m%d")
        # combine 3 parts
        return f"{name_part}{location_part}{date_part}"

    @property
    def id_tournament(self):
        """Return tournament id for this tournament"""
        return self._id_tournament

    def add_player(self, player: Player) -> None:
        """
        Adds a player to the tournament
        :param player: player object
        raise ValueError if player already exists
        US 2.2
        """
        if player in self._players:
            raise ValueError(f"Player {player.national_id} already exists (record for this tournament)")
        self._players.append(player)

    def generate_first_round(self) -> Round:
        """Generates a first round of the tournament in randomly  shuffling the players
        :return: the generated round
        :raises ValueError: if fewer than 2 players are registered
        US 2.3
        """
        if len(self._rounds_list) > 0:
            raise ValueError("already a round is generated")
        if len(self._players) < 2:
            raise ValueError("At least 2 players are required to generate a round")
        if len(self._players) % 2 != 0:
            raise ValueError("The number of players must be even to generate a round")
        # Randomly shuffle the players
        shuffled_player = self._players.copy()
        random.shuffle(shuffled_player)
        # Create a round
        round_name = "Round 1"
        start_time = datetime.now()
        round = Round(round_name, start_time)
        # Pairing players
        for i in range(0, len(shuffled_player) - 1, 2):
            player1 = shuffled_player[i]
            player2 = shuffled_player[i + 1]
            match = Match(player1, player2)
            round._matches.append(match)
        # Add the round to the tournament's list of rounds
        self._rounds_list.append(round)
        return round

    def _has_played_before(self, player1: Player, player2: Player) -> bool:
        """Checks if two players have already played against each other in previous rounds.
        :param player1(Player): first player
        :param player2(Player): second player
        :return: bool True if the players have already played together, False otherwise
        """
        for round in self._rounds_list:
            for match in round._matches:
                if ((match._player1 == player1 and match._player2 == player2) or (match._player1 == player2 and match._player2 == player1)):
                    return True
        return False

    def generate_next_round(self) -> Round:
        """
        Generates next round by sorting players by score
        :return: the generated round
        :raises ValueError: if number of player is odd (3 or 5, 7 ,etc.) or if there are not enough players
        """
        if len(self._players) < 2:
            raise ValueError("At least 2 players are required to generate a round")
        if len(self._players) % 2 != 0:
            raise ValueError("The number of players must be even to generate a round")
        if len(self._rounds_list) == 0:
            raise ValueError("Generate before the first round.")
        if len(self._rounds_list) >= self.rounds:
            raise ValueError("All the rounds are generated for this tournament")

        # determine the round number
        round_number = len(self._rounds_list) + 1
        round_name = f"Round {round_number}"
        start_time = datetime.now()

        # Sort players by descending score, then randomly if scores are equal
        sorted_players = sorted(self._players, key=lambda p: (-p.score, random.random()))
        '''
        sorted(liste, key=fonction_de_tri)
        function key definie how to order players : each player p return a tupple (-p.score,random.random())
        - before p : decreasing order if only p : increasing
        random.ramdom() : if draw scores order ramdom.
        '''
        # Create a round
        round = Round(round_name, start_time)

        paired_players = []  # is an empty list that will contain players already paired in this round.

        # Pairing players
        for i in range(0, len(sorted_players), 2):  # We iterate through the players two by two (i = 0, 2, 4, etc.).
            player1 = sorted_players[i]  # The i-th player is taken as the first player of the match.

            if player1 in paired_players:
                continue  # if in this round player1 is already in paired_players so pass to next player

            # find another player for player1
            found_opponent = False
            for j in range(i + 1, len(sorted_players)):  # We look for an opponent among the remaining players (starting from i+1).
                if sorted_players[j] not in paired_players:  # We check that the potential player (sorted_players[j]) has not already been paired in this round.
                    player2 = sorted_players[j]
                    if player2 not in paired_players and not self._has_played_before(player1, player2):  # We check that player1 and player2 have not already played together in previous rounds.
                        match = Match(player1, player2)
                        round._matches.append(match)
                        paired_players.extend([player1, player2])  # add player1 and player2 individually
                        found_opponent = True
                        break  # As soon as the player is found, exit the loop early

            if not found_opponent:
                raise ValueError(f"Unable to pair the player {player1.national_id}. he has already played against all other players")

        # Add the round to the tournament's list of rounds
        self._rounds_list.append(round)
        return round

    def to_dict(self) -> dict:
        return {
            "id_tournament": self.id_tournament,
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date.isoformat(),  # convert datetime to ISO str. If not you can't save in.json
            "end_date": self.end_date.isoformat(),
            "rounds": self.rounds,
            "players": [player.to_dict() for player in self._players],
            # "players": [player.national_id for player in self._players],  # record only ID list of players who participe at this tournament
            "rounds_list": [round.to_dict() for round in self._rounds_list]
        }

    def save_to_json(self, file_path: str = None) -> str:  # return file path where the tournament is recorded
        """Saves the tournament to a JSON file.
        :param file_path: path to file (str optional): file path. If not specified, uses data/tournaments/{name}.json.
        :returns (str) : path of the recorded file"""

        # create directory if not exist
        if not os.path.exists("data/tournaments"):
            os.mkdir("data/tournaments")

        # determine the path of file
        if file_path is None:
            file_path = f"data/tournaments/{self.id_tournament}.json"

        # convert tournament to dictionary and save
        tournament_dict = self.to_dict()
        with open(file_path, mode="w", encoding="utf-8") as file:
            json.dump(tournament_dict, file, indent=4)  # important indent=4 it's more esay to read json file else all the date is in one lineS
        return file_path

    # @staticmethod is a decorator in Python that indicates the following method is a static method.
    # A static method does not have access to the class instance (it has no self parameter).
    # It is called directly on the class, without needing to create an instance.
    @staticmethod
    def load_from_json(file_path: str) -> "Tournament":
        """
        Loads a tournament from a JSON file.
        :param file_path: path to file (str optional): file path.
        :returns (Tournament) : tournament is loaded from JSON file
        """

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} does not exist")

        with open(file_path, 'r') as file:
            tournament_data = json.load(file)

        # keys verification
        required_keys = ["name", "location", "start_date", "end_date", "rounds", "players", "rounds_list"]
        for keys in required_keys:
            if keys not in tournament_data:
                raise ValueError(f"Json file invalid : missing required key {keys} in tournament JSON file")
        # dates conversion
        start_date = datetime.fromisoformat(tournament_data["start_date"])
        end_date = datetime.fromisoformat(tournament_data["end_date"])
        # Create tournament
        tournament = Tournament(
            name=tournament_data["name"],
            location=tournament_data["location"],
            start_date=start_date,
            end_date=end_date,
            rounds=tournament_data["rounds"],
        )
        tournament._id = tournament_data.get("id_tournament", tournament._generate_id())  # if id don't existe use method _generate_id
        # Dictionnaire pour stocker les joueurs par leur identifiant national
        players_dict = {}
        # load players
        for player_data in tournament_data["players"]:
            player = Player(
                national_id=player_data["national_id"],
                last_name=player_data["last_name"],
                first_name=player_data["first_name"],
                birth_date=player_data["birth_date"],
                club=player_data["club"],
            )

            player._score = player_data["score"]
            player._match_history = player_data["match_history"]
            players_dict[player.national_id] = player
            tournament._players.append(player)
        # load all match
        for round_data in tournament_data["rounds_list"]:
            round_start_time = datetime.fromisoformat(round_data["start_time"])
            round = Round(round_data["name"], round_start_time)

            if round_data['end_time']:
                round._end_time = datetime.fromisoformat(round_data["end_time"])

            for match_data in round_data["matches"]:
                player1 = players_dict[match_data["player1"]]
                player2 = players_dict[match_data["player2"]]
                match = Match(player1=player1, player2=player2)
                # load colors
                match._color_player1 = match_data["color_player1"]
                match._color_player2 = match_data["color_player2"]
                # load result if exist
                if match_data['result']:
                    match._result = tuple(match_data["result"])
                    # upload scores and history players
                    # player1._add_match(player2.national_id, match._result[0], match._color_player1)  # ici inutile sinon score double
                    # player2._add_match(player1.national_id, match._result[1], match._color_player2)

                round._matches.append(match)
            tournament._rounds_list.append(round)
        return tournament
