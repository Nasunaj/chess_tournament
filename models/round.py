from datetime import datetime
from typing import List, Optional

class Round:
    """Represents a round in a tournament with its matchs and its schedules"""
    def __init__(self,name:str,start_time:datetime):
        """
        Initializes a round with a name and start time.
        :param name (str): round name (e.g.,"Round 1")
        :param start_time: Start time of the round
        """
        self._name = name
        self._start_time = start_time
        self._end_time :Optional[datetime]= None #To be set when the round is completed
        self._matches: List = []

    @property
    def name(self):
        return self._name

    @property
    def start_time(self):
        return self._start_time

    @property
    def end_time(self):
        return self._end_time

    @property
    def matches(self):
        return self._matches

    def end_round(self,end_time:datetime)->None:
        """
        Marks the round as completed with an end time.
        :param end_time (datetime): End time of the round:
        :raises ValueError: If the end time is earlier than or equal to the start time.
        US 3.6: closing round with end time
        """
        if end_time<=self._start_time:
            raise ValueError("End time cannot be earlier than start time")
        self._end_time = end_time

    def to_dict(self) -> dict:
        return {
            "name":self._name,
            "start_time":self._start_time.isoformat(), #isofrmat in necessary becouse tournament is saved in .json and datetime don't work so need to convert ISO str
            "end_time":self._end_time.isoformat() if self._end_time is not None else None,
            "matches":[match.to_dict() for match in self._matches] # need to convert each match to dictionary  to save injson
        }