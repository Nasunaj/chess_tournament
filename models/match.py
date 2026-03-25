from typing import Optional, Tuple
from models.player import Player
import random


class Match:
    """Represents a match between two players with its result
    (US 3.2 : recording result , US 3.3 : automatically upload scores and US 3.7 : rejecting invalid results)
    US 3.8 : random colors (white pr black) for player1 and player2
    """
    def __init__(self, player1: Player, player2: Player):
        self._player1 = player1
        self._player2 = player2
        self._result: Optional[Tuple[float, float]] = None  # Result undefined at creation
        self._color_player1: str = random.choice(['white', 'black'])  # Random color for player1
        self._color_player2: str = "black" if self._color_player1 == "white" else "white"  # opposite color for player2

    def set_result(self, score_player1: float, score_player2: float) -> None:
        """
        Sets the match result.
        Args:
             score_player1 (float): First player's score (1.0, 0.5, or 0.0).
             score_player2 (float): Second player's score (1.0, 0.5, or 0.0).
        """
        if (score_player1, score_player2) not in [(1, 0), (0, 1), (0.5, 0.5)]:
            raise ValueError("Invalid result use (1,0),(0,1),(0.5,0.5)")
        self._result = (score_player1, score_player2)
        # update scores and add history
        self._player1._add_match(self._player2.national_id, score_player1, self._color_player1)
        self._player2._add_match(self._player1.national_id, score_player2, self._color_player2)

    @property
    def color_player1(self) -> str:
        """Returns the color of the first player."""
        return self._color_player1

    @property
    def color_player2(self) -> str:
        """Returns the color of the second player."""
        return self._color_player2

    def to_dict(self) -> dict:
        return {
            "player1": self._player1.national_id,
            "player2": self._player2.national_id,
            "result": self._result,
            "color_player1": self._color_player1,
            "color_player2": self._color_player2
        }
