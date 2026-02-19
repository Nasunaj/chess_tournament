import unittest
from models.player import Player
from models.match import Match

class TestMatch(unittest.TestCase):
    def setUp(self):
        #create two players
        self.player1 = Player("AB001", "NameA", "FirstnameA", "1990-01-01",  "Club A")
        self.player2 = Player("AB002", "NameB", "FirstnameB", "1995-02-02", "Club B")
        #create match between these two players
        self.match = Match(self.player1, self.player2)

    #Test for the constructor
    #verified initialization of matches
    def test_match_initialization(self):
        self.assertEqual(self.match.to_dict()["player1"], "AB001","Wrong id for player1")
        self.assertEqual(self.match.to_dict()["player2"], "AB002","Wrong id for player2")
        self.assertIsNone(self.match.to_dict()["result"],"Initial result should be None")

    #test for set_result
    #player1 win
    def test_set_result_player1_win(self):
        self.match.set_result(1,0)
        self.assertEqual(self.match._result,(1,0),"Result should be (1,0)")
        #score player
        self.assertEqual(self.player1.score,1,"Score should be 1")
        self.assertEqual(self.player2.score,0,"Score should be 1")
        #match add
        self.assertEqual(len(self.player1._match_history),1,"Match history should be 1")
        self.assertEqual(len(self.player1._match_history), 1, "Match history should be 1")

    #draw
    def test_set_result_draw(self):
        self.match.set_result(0.5,0.5)
        self.assertEqual(self.match._result,(0.5,0.5),"Result should be (0.5,0.5)")
        self.assertEqual(self.player1.score,0.5,"Score should be 0.5")
        self.assertEqual(self.player2.score,0.5,"Score should be 0.5")

    #invalid result
    def test_set_result_invalid(self):
        with self.assertRaises(ValueError,msg="must be show the error"):
            self.match.set_result(1,2)

    def test_match_history(self):
        self.match.set_result(1, 0)
        self.assertEqual(self.player1._match_history[0]["opponent_id"], "AB002")
        self.assertEqual(self.player1._match_history[0]["result"], 1)
        self.assertEqual(self.player2._match_history[0]["opponent_id"], "AB001")
        self.assertEqual(self.player2._match_history[0]["result"], 0)


if __name__ == '__main__':
    unittest.main()
