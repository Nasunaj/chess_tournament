import unittest
from models.player import Player
from models.match import Match

class TestMatch(unittest.TestCase):
    def setUp(self):
        #create two players
        self.player1 = Player("AB12345", "NameA", "FirstnameA", "1990-01-01",  "Club A")
        self.player2 = Player("AC12345", "NameB", "FirstnameB", "1995-02-02", "Club B")
        #create match between these two players
        self.match = Match(self.player1, self.player2)

    def test_set_result(self):
        """Tests the recording of a valid match result and the updating of score"""
        self.match.set_result(1,0)
        self.assertEqual(self.match._result, (1,0)) #resultat verification

        #scores verification
        self.assertEqual(self.player1.score, 1.0)
        self.assertEqual(self.player2.score, 0.0)


        #history verification
        #self.assertEqual(len(self.player1.get_match_history()), 1)
        #self.assertEqual(self.player2.get_match_history()[0], {'opponent_id':'AB12345', 'result':0})

        # History verification (with test color for players)
        self.assertEqual(len(self.player1.get_match_history()), 1)
        self.assertEqual(self.player1.get_match_history()[0], {'opponent_id': 'AC12345', 'result': 1.0, 'color': self.match.color_player1})
        self.assertEqual(len(self.player2.get_match_history()), 1)
        self.assertEqual(self.player2.get_match_history()[0], {'opponent_id': 'AB12345', 'result': 0.0, 'color': self.match.color_player2})

    print("Test US 3.2 and 3.3: recording of valid result and updating score/history OK!\nUS.8 color for player1 and player2 in  get_match_history ok!")

    def test_invalid_set_result(self):
        """Tests the recording of a invalid match result and the updating of score"""
        with self.assertRaises(ValueError):
            self.match.set_result(2, 0)

    print("Test US 3.7: invalid result OK!")

    def test_match_colors(self):
        """Tests random color (white or black) for player1 and player 2"""
        match=Match(self.player1, self.player2)
        #Check that colors are assigned and opposite
        self.assertIn(match.color_player1,["white","black"])
        self.assertIn(match.color_player2,["white","black"])
        self.assertNotEqual(match.color_player1,match.color_player2)



if __name__ == '__main__':
    unittest.main()
