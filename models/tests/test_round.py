import unittest
from datetime import datetime,timedelta

from models.player import Player
from models.round import Round

class TestRound(unittest.TestCase):
    def setUp(self):
        # create players for the test
        self.player1 = Player("AB00001", "NameA", "FirstnameA", "1990-01-01", "clubA")
        self.player2 = Player("AB00002", "NameB", "FirstnameB", "1995-02-02", "Club B")
        self.round = Round("Round 1",datetime(2025,12,20,10,30))

    #Attributs verification
    def test_attributes(self):
        self.assertEqual(self.round.name, "Round 1")
        self.assertEqual(self.round.start_time, datetime(2025,12,20,10,30))
        self.assertIsNone(self.round.end_time)
        self.assertEqual(self.round.matches, [])

    def test_end_time(self):
        end_time=self.round._start_time+timedelta(hours=1)
        self.round.end_round(end_time)
        self.assertEqual(self.round.end_time,end_time)
    print("Test US 3.6: closing round with valid time OK!")

    def test_invalid_end_time(self):
        with self.assertRaises(ValueError):
            self.round.end_round(self.round._start_time)
    print("Test US 3.6: Rejecting invalid time OK!")


if __name__ == "__main__":
    unittest.main()
