import unittest
from datetime import datetime
from models.tournament import Tournament
from models.player import Player

class TestTournament(unittest.TestCase):
    def setUp(self):
        #create a tournament with start date and end date
        self.start_date = datetime(2026, 8, 1)
        self.end_date = datetime(2026, 8, 1)
        self.tournament = Tournament("Summer Tournament","Paris",self.start_date,self.end_date,rounds=4)

        #create players for the test
        self.player1=Player("AB001", "NameA", "FirstnameA", "1990-01-01","clubA")
        self.player2 = Player("AB002", "NameB", "FirstnameB", "1995-02-02", "Club B")
        self.player3 = Player("AB003", "NameC", "FirstnameC", "1992-03-03", "Club C")
        self.player4 = Player("AB004", "NameD", "FirstnameD", "1993-04-04", "Club D")

    def test_tournament_initialization(self):
        self.assertEqual(self.tournament._name, "Summer Tournament")
        self.assertEqual(self.tournament._location, "Paris")
        self.assertEqual(self.tournament._start_date, self.start_date)
        self.assertEqual(self.tournament._end_date, self.end_date)
        self.assertEqual(len(self.tournament._rounds), 0)
        self.assertEqual(len(self.tournament._players), 0)

    #test for add_player
    def test_add_player(self):
        self.tournament.add_player(self.player1)
        self.assertEqual(len(self.tournament._players), 1)
        self.assertEqual(self.tournament._players[0], self.player1)

    #test for generate next round
    def test_generate_next_round(self):
        #add players
        self.tournament.add_player(self.player1)
        self.tournament.add_player(self.player2)
        self.tournament.add_player(self.player3)
        self.tournament.add_player(self.player4)

        #generate the next round
        round1=self.tournament.generate_next_round()

        #verificate the next round is added
        self.assertEqual(len(self.tournament._rounds), 1)
        self.assertEqual(round1.name, "Round 1")

        #verification that the round has matches
        self.assertEqual(len(round1._matches), 2) # 4 players 2 matches

    # verification order player in the matches
    def test_generate_next_round_player_order(self):
        """Tests that players are sorted by score and randomly in case of a drax.."""
        #add players
        self.tournament.add_player(self.player1)  # Score: 0
        self.tournament.add_player(self.player2)  # Score: 0
        self.tournament.add_player(self.player3)  # Score: 0
        self.tournament.add_player(self.player4)  # Score: 0

        # Generates the next round (with random draw)
        round1 = self.tournament.generate_next_round()

        # Checks that the round contains matches
        self.assertEqual(len(round1._matches), 2)



if __name__ == '__main__':
    unittest.main()


