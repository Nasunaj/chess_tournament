import unittest
from datetime import datetime
import os
import json
from models.tournament import Tournament
from models.player import Player


class TestTournament(unittest.TestCase):
    def setUp(self):
        # create a tournament with start date and end date
        self.start_date = datetime(2026, 8, 1)
        self.end_date = datetime(2026, 8, 1)
        self.tournament = Tournament("Summer Tournament", "Paris", self.start_date, self.end_date, rounds=4)

        # create players for the test
        self.player1 = Player("AB00001", "NameA", "FirstnameA", "1990-01-01", "clubA")
        self.player2 = Player("AB00002", "NameB", "FirstnameB", "1995-02-02", "Club B")
        self.player3 = Player("AB00003", "NameC", "FirstnameC", "1992-03-03", "Club C")
        self.player4 = Player("AB00004", "NameD", "FirstnameD", "1993-04-04", "Club D")

    def test_attributes(self):
        self.assertEqual(self.tournament.name, "Summer Tournament")
        self.assertEqual(self.tournament.start_date, self.start_date)
        self.assertEqual(self.tournament.end_date, self.end_date)
        self.assertEqual(self.tournament.rounds, 4)
        print("Test US 2.1 attributs ok!")

    # test for add_player
    def test_add_player(self):
        self.tournament.add_player(self.player1)
        self.tournament.add_player(self.player2)
        self.assertEqual(len(self.tournament._players), 2)
        self.assertEqual(self.tournament._players[0], self.player1)
        # print(self.tournament.to_dict()['players'])
        print("Test US 2.2 add player ok!")

    def test_duplicate_player(self):
        self.tournament.add_player(self.player1)
        with self.assertRaises(ValueError):
            self.tournament.add_player(self.player1)
        print("Test US 2.2 Rejecting if player 1 already exists Ok!")

    def test_first_round_add(self):
        for player in [self.player1, self.player2, self.player3, self.player4]:
            self.tournament.add_player(player)
            # print(self.tournament._players)

        round = self.tournament.generate_first_round()
        self.assertEqual(round.name, "Round 1")
        self.assertEqual(len(round.matches), 2)  # 4 players 2 matchs
        # print(round.to_dict())

        # test round_list
        self.assertEqual(len(self.tournament._rounds_list), 1)
        self.assertEqual(self.tournament._rounds_list[0], round)
        print("Test US 2.3: first round generated - OK")

    def test_first_round_not_enough_players(self):
        self.tournament.add_player(self.player1)
        with self.assertRaises(ValueError):
            self.tournament.generate_first_round()
        print("Test US 2.3: rejecting if there are fewer than 2 players OK!")

    def test_generate_next_round(self):
        for player in [self.player1, self.player2, self.player3, self.player4]:
            self.tournament.add_player(player)
        self.tournament.generate_first_round()

        # simulation results of first round (always first player win
        for match in self.tournament._rounds_list[0]._matches:
            match.set_result(1, 0)
            # print(match._result)

        # generate next round
        round = self.tournament.generate_next_round()
        self.assertEqual(round.name, "Round 2")
        self.assertEqual(len(round.matches), 2)
        print("Test US 3.4: Generation next round OK!")

    def test_generate_next_round_odd_players(self):
        for player in [self.player1, self.player2, self.player3]:
            self.tournament.add_player(player)

        with self.assertRaises(ValueError):
            self.tournament.generate_next_round()
        print("Test US 3.4: Rejecting if the number of player is odd OK!")

    def test_generate_next_round_impossible_pairing(self):
        for player in [self.player1, self.player2]:
            self.tournament.add_player(player)

        first_round = self.tournament.generate_first_round()
        for match in first_round._matches:
            match.set_result(0.5, 0.5)
        # This 3rd round will produce an error because each player has already played against all the other players.
        with self.assertRaises(ValueError):
            self.tournament.generate_next_round()

    def test_save_to_json(self):
        """ Tests saving a tournament to a JSON file"""
        for player in [self.player1, self.player2]:
            self.tournament.add_player(player)
        self.tournament.generate_first_round()
        file_path = self.tournament.save_to_json()
        self.assertTrue(os.path.exists(file_path))  # verification if file exists.
        # verifcation data
        with open(file_path, mode="r") as file:
            saved_data = json.load(file)

        self.assertEqual(saved_data["name"], "Summer Tournament")
        self.assertEqual(saved_data["location"], "Paris")
        self.assertEqual(len(saved_data["players"]), 2)
        self.assertEqual(len(saved_data["rounds_list"]), 1)
        # print(self.tournament.to_dict())

    print("✅ Test US 4.1: Saving tournament to file OK!")

    def test_load_from_json(self):
        """ Tests loading a tournament from a JSON file"""
        loaded_tournament = Tournament.load_from_json("data/tournaments/sumpar20260801.json")
        print(loaded_tournament.to_dict())
        self.assertEqual(loaded_tournament.name, "Summer Tournament")
        # verification attributs
        self.assertEqual(loaded_tournament.name, "Summer Tournament")
        self.assertEqual(loaded_tournament.location, "Paris")
        self.assertEqual(len(loaded_tournament._players), 2)  # attention players is private
        self.assertEqual(len(loaded_tournament._rounds_list), 1)  # rounds_list is private

        print(loaded_tournament.to_dict())
        for player in loaded_tournament._players:
            self.assertTrue(player.national_id in ["AB00001", "AB00002"])
            self.assertTrue(player.score == 0)
            print(player.get_match_history())

        print("Test US 4.2: tournament load - OK")


if __name__ == '__main__':
    unittest.main()
