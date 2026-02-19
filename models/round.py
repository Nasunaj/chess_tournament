from datetime import datetime
from typing import List
from models.match import Match

class Round:
    def __init__(self,name:str,start_time:datetime):
        self._name = name
        self._start_time = start_time
        self._end_time = None
        self._matches : List[Match] = []

    @property
    def name(self) -> str:
        """round name (read_only)."""
        return self._name

    @property
    def start_time(self) -> datetime:
        """time start (read_only)."""
        return self._start_time

    @property
    def end_time(self) -> datetime:
        """end time round (read-only). valueError if round is not yet finished."""
        if self._end_time is None:
            raise ValueError("the round is not yet finished")
        return self._end_time

    @end_time.setter
    def end_time(self, value: datetime) -> None:
        """Maybe you need validate endtime."""
        if value <= self._start_time:
            raise ValueError("End time must be after start time.")
        self._end_time = value

    def add_match_to_round(self,match:Match)->None:
        """Add match to round"""
        self._matches.append(match)

    def end_round(self,end_time:datetime)->None:
        """End round"""
        self.end_time = end_time #call the setter

    def to_dict(self)->dict:
        return {
            "name":self._name,
            "start_time":self._start_time,
            "end_time":self._end_time,
            "matches":[match.to_dict() for match in self._matches]
        }

