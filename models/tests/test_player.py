import unittest
from models.player import Player  # step 2
'''
what's a unit test :
- Definition : a unit test checks a small part of your code (a class, a method) does what is it to do (in isolation)

Why use unittest :
- Goal : Structure your tests in a professional and scalable way. (vs assert)
- Advantages :
    - Clear organization (one test class per class to test)
    - Built-in-tools to avoid repetitions
    - More detailed error messages
    - Automatic execution of all tests


step 1) create a test file
step 2) Import unittest and the class to test
step 3) create a test class
step 4) prepare the data test with setUp
step 5) write the first test
step 6) run the tests
step 6) understand the errors
'''


class TestPlayer(unittest.TestCase):
    """
    Test player class
    """
    # Testplayer : a class dedicated to testing the player class
    # unittest.TestCase : The base class provided by unittest for writing test
    # unittest organizes tests into classes, allowing logical groupîng of tests for the same class'''
    def setUp(self):
        # this method is run before each test
        # Role of setUp : creates a Player object before each test, using known values. Advantage : avoids repeating the player creation in every test
        self.player = Player("AB12345", "NameA", "FirstnameA", "1990-08-01", "Club A")

    # step 5
    # Test 1 : verify attribute initialization
    # Test national_id : name of the test method (must start with test_)
    # self.assertEqual(a,b,message): checks that a==b. If not, it's display the message
    # We are testing national_id attribute is correctly initialized and accessible via the national_id property

    def test_national_id(self):
        self.assertEqual(self.player.national_id, "AB12345", "National ID should be 'AB12345'")

    def test_lastname(self):
        self.assertEqual(self.player.last_name, "NameA", "Last name should be 'NameA'")

    def test_birthdate(self):
        self.assertEqual(self.player.birth_date, "1990-08-01", "Birth date should be '1990-08-01'")
        # Attention ici datetime donc si on met en caractère ça ne fonctionnera pas car il manquera les heures minutes secondes qui sont par défaut 00:00:00

    def test_firstname(self):
        self.assertEqual(self.player.first_name, "FirstnameA", "Firstname should be 'FirstnameA'")

    def test_club(self):
        self.assertEqual(self.player.club, "Club A", "Club should be 'Club A'")
    print("Test US 1.1 : creating player with valid information : OK!")

    def test_invalide_national_id(self):
        with self.assertRaises(ValueError):
            Player("A12345", "NomA", "FirstnameA", "1990-01-01", "Club A")
    print("Test US 1.2 : Rejecting an invalid ID : OK!")

    def test_invalide_birth_date(self):
        with self.assertRaises(ValueError):
            Player("AB12345", "A", "B", "10/12/1914", "Club A")
    print("Test US 1.3 : rejecting an invalid date : OK!")

    def test_add_match_update_score(self):
        """ Test add match update score and history (US 1.4)"""
        self.player._add_match("BC12345", 1, color="white")  # win
        self.assertEqual(self.player.score, 1, "Score should be in [0,0.5,1]")
        self.assertEqual(len(self.player.to_dict()["match_history"]), 1)
        self.assertEqual(self.player.to_dict()["match_history"][0], {'opponent_id': "BC12345", "result": 1, 'color': 'white'})

    print("Test US 1.4 : add_match update score OK!")

    def test_add_match_invalid_result(self):
        """ Test add match rejecting invalid result """
        with self.assertRaises(ValueError):
            self.player._add_match("AB12345", 2, color="white")

    print("Test US 1.4 and 1.8 : rejecting invalid score OK!")

    def test_score_implement(self):
        """Test score is implemented"""
        self.player._add_match("BC12345", 1, color="white")
        self.player._add_match("AC12345", 0.5, color="black")
        self.assertEqual(self.player.score, 1.5, "Score should be in [0,0.5,1]")
        # print(self.player.to_dict())

    print("Test US 1.4  : score is implemented OK!")

    def test_get_match_history(self):
        """Test view match history"""
        self.player._add_match("AC12345", 1, color="white")
        self.player._add_match("AD12345", 0.5, color="black")
        # history verification
        history = self.player.get_match_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0], {'opponent_id': "AC12345", "result": 1, "color": "white"})
        self.assertEqual(history[1], {'opponent_id': "AD12345", "result": 0.5, "color": "black"})

    print("Test US 1.5: view match history OK!")

    def test_empty_get_match_history(self):
        history = self.player.get_match_history()
        self.assertEqual(history, [])

    print("Test US 1.5: empty view match history OK!")


if __name__ == '__main__':
    unittest.main()
