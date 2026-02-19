from datetime import datetime
from typing import List
from models.player import Player
from models.match import Match
from models.round import Round
import random


class Tournament:
    def __init__(self,name:str,location:str,start_date:datetime,end_date:datetime,rounds:int=4) :
        self._name = name
        self._location = location
        self._start_date = start_date
        self._end_date = end_date
        self._rounds : List[Round] = []
        self._players: List[Player] = []

    def add_player(self,player:Player) -> None:
        """Add a player to the tournament"""
        self._players.append(player)

    def generate_next_round(self):
        """Generate next round of the tournament"""
        round_number = len(self._rounds)+1
        round_name = f"Round {round_number}"
        round_1 = Round(round_name,datetime.now())

        #range player by score (decreasing)
        #sorted_players = sorted(self._players, key=lambda p:p.score, reverse=True)
        sorted_players = sorted(self._players, key=lambda p: (-p.score, random.random()))
        #Sorts first by descending score (`-p.score`).In case of a tie, sorts randomly (`random.random()`)

        for ind in range(0,len(sorted_players)-1,2):
            match=Match(sorted_players[ind],sorted_players[ind+1])
            round_1.add_match_to_round(match)

        self._rounds.append(round_1)
        return round_1

    def to_dict(self)->dict:
        return {
            "name": self._name,
            "location": self._location,
            "start_date": self._start_date.isoformat(),
            "end_date": self._end_date.isoformat(),
            "rounds": [rounds.to_dict() for rounds in self._rounds],
            "players": [rounds.to_dict() for rounds in self._players]
        }
