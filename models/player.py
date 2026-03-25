import re
from datetime import datetime  # for date without time
from typing import List, Dict
# Why US 1.4 is in class Player:
# Single responsibility principe:
# - PLayer is responsible for its own data(name,score,match history)
# - Tournament or Round should not store a player's match history (this would violate the separation of responsibilities principle)


class Player:
    """Represents a chess player with their information and match history."""

    def __init__(self, national_id: str, last_name: str, first_name: str, birth_date: str, club: str):
        """Initializes a player with their private attributes
        Args :
            national_id(str) : National ID in the format AB12345
            last_name(str) : Player's last name
            first_name(str) : Player's first name
            birth_date(str) : Date of birth in the format YYYY-MM-DD
            club(str) : Player's club
        """
        self._validate_national_id(national_id)  # ID validation
        self._validate_birth_date(birth_date)  # date of birth validation

        # Encapsulation: Attributes are marked as 'private' with an underscore (_) to indicate they should not be accessed directly from outside.
        self._national_id = national_id
        self._last_name = last_name
        self._first_name = first_name
        self._birth_date = birth_date
        self._club = club

        # US.14
        self._score = 0  # player's total score
        self._match_history: List[Dict[str, float]] = []  # match history
        '''
        List[Dict] for _match_history
        - Type: List[Dict[str, float]] means a list of dictionaries, where each dictionary has:
          - A key "opponent_id" (str): Opponent's ID (e.g., "AB12345").
          - A key "result" (float): Match result for this player (example : 1.0 for a win).
        '''

    def _validate_national_id(self, national_id: str) -> None:
        """Validates the National ID in the format AB12345 (private method)"""
        if not re.match(r'^[A-Z]{2}\d{5}$', national_id):
            raise ValueError('National ID must be in the format AB12345')

    def _validate_birth_date(self, birth_date: str) -> None:
        """Validates the date of birth in the format YYYY-MM-DD (private method)"""
        try:
            datetime.strptime(birth_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError('Birth date must be in the format YYYY-MM-DD')

    @property
    def national_id(self) -> str:
        """Returns the national id of the player (read only)- str"""
        return self._national_id

    @property
    def last_name(self) -> str:
        """Returns the last name of the player (read only)- str"""
        return self._last_name

    @property
    def first_name(self) -> str:
        """Returns the first name of the player (read only)- str"""
        return self._first_name

    @property
    def birth_date(self) -> str:
        """Returns the birthdate of the player (read only)- str"""
        return self._birth_date

    @property
    def club(self) -> str:
        """Returns the club of the player (read only)- str"""
        return self._club

    @property
    def score(self) -> float:
        """Returns the score of the player (read only)- float"""
        return self._score

    def _update_score(self, points: float) -> None:
        """ Private method to update the player's total score. it's call in public method add_match_history (US 1.8)"""
        if points in [0, 0.5, 1]:
            self._score += points
        else:
            raise ValueError('Score must be in [0,0.5,1]')

    def _add_match(self, opponent_id: str, result: float, color: str) -> None:
        """Adds a match to the history and updates the score (private method US 1.4).
        This way, the result is only entered in the `Match` class's `set_result` method.
        Args:
            opponent_id (str): National ID of the opponent (e.g., "CD67890").
            result (float): Match result for this player (0.0, 0.5, or 1.0).
            color (str): Color assigned to the player ("white" or "black")..
        """
        if result not in [0, 0.5, 1]:
            raise ValueError('Result must be in [0,0.5,1]')
        self._match_history.append({'opponent_id': opponent_id, 'result': result, 'color': color})  # add a match in history
        self._update_score(result)  # update final score

    def to_dict(self) -> Dict:
        """Convertit le joueur en dictionnaire pour la sérialisation."""
        return {
            "national_id": self._national_id,
            "last_name": self._last_name,
            "first_name": self._first_name,
            "birth_date": self._birth_date,
            "club": self._club,
            "score": self._score,
            "match_history": self._match_history
        }

    def __str__(self) -> str:
        """Returns a readable string representation of the player."""
        return f"{self._first_name} {self._last_name} (ID: {self._national_id}, Score: {self._score})"

    def __repr__(self) -> str:
        """Returns a technical string representation of the player."""
        return f"Player(national_id={self._national_id!r}, last_name={self._last_name!r}, score={self._score})"

    # US 1.5
    def get_match_history(self) -> List[Dict[str, float]]:
        """Returns a copy of the player's match history (US 1.5).

        Returns:
            List[Dict[str, float]]: List of matches as dictionaries.
                Each dictionary contains:
                - "opponent_id" (str): Opponent's national ID.
                - "result" (float): Match result (1.0, 0.5, or 0.0).
        """
        return self._match_history.copy()  # Returns a copy to prevent external modifications
