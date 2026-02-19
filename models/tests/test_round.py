import unittest
from datetime import datetime
from models.round import Round
from models.match import Match
from models.player import Player

class TestRound(unittest.TestCase):
    def setUp(self):
        # create players and matches
        self.player1 = Player("AB001", "NameA", "FirstnameA", "1990-01-01",  "Club A")
        self.player2 = Player("AB002", "NameB", "FirstnameB", "1995-02-02", "Club B")
        self.match = Match(self.player1, self.player2)
        self.match.set_result(1.0, 0.0)  # Défine a result of match

        #create a round with a start time
        self.round = Round("Round 1",datetime(2026,2,15,10,30))

    #test for constructor and properties
    def test_round_initialization(self):
        """Test if round is correctly initialized."""
        self.assertEqual(self.round.name, "Round 1")
        self.assertEqual(self.round.start_time, datetime(2026,2,15,10,30))
        self.assertIsNone(self.round._end_time)
        self.assertEqual(len(self.round._matches), 0)

    #verification property end_time before the end of round
    def test_end_time_not_finished(self):
        with self.assertRaises(ValueError,msg="round is not yet finished"):
            self.round.end_time

    #test for end_round
    def test_end_round_valid(self):
        end_time = datetime(2026,2,15,11,30)
        self.round.end_round(end_time)
        self.assertEqual(self.round._end_time, end_time)

    #end round with invalid time
    def test_end_round_invalid(self):
        end_time = datetime(2026,2,15,9,30)
        with self.assertRaises(ValueError,msg="invalid end time"):
            self.round.end_round(end_time)


    #test for add_match_to_round
    def test_add_match_to_round(self):
        self.round.add_match_to_round(self.match)
        self.assertEqual(len(self.round._matches), 1)
        self.assertEqual(self.round._matches[0], self.match)



if __name__ == '__main__':
    unittest.main()
