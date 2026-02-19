import unittest
from datetime import date
from models.player import Player #step 2
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
   '''Testplayer : a class dedicated to testing the player class
    unittest.TestCase : The base class provided by unittest for writing test
    unittest organizes tests into classes, allowing logical groupîng of tests for the same class'''
   def setUp(self):
        #this method is run before each test
        #Role of setUp : creates a Player object before each test, using known values. Advantage : avoids repeating the player creation in every test
        self.player = Player("AB001","NameA","FirstnameA",date(1995, 8, 1),"clubA")

   #step 5
   #Test 1 : verify attribute initialization
   # Test national_id : name of the test method (must start with test_)
   #self.assertEqual(a,b,message): checks that a==b. If not, it's display the message
   #We are testing national_id attribute is correctly initialized and accessible via the national_id property
   def test_national_id(self):
       self.assertEqual(self.player._national_id,"AB001","National ID should be 'AB001'")

   def test_lastname(self):
       self.assertEqual(self.player._last_name,"NameA","Last name should be 'NameA'")

   def test_firstname(self):
       self.assertEqual(self.player._first_name,"FirstnameA","Firstname should be 'FirstnameA'")

   def test_score(self):
       self.assertEqual(self.player._score,0,"Score should be 0")

   '''def test_birth_date(self):
       self.assertIsInstance(self.player._birth_date,date,"Birth date should be a date") #test if birth_date is a date
       self.assertEqual(self.player._birth_date,date(1995,8,1),"Birth date should be 1995-08-01") # test the value

   # test if birthdate is not a date
   def test_birth_date_invalid_format(self):
       # Checks that a block of code raises a specific exception.
       # with : allows you to group multiple lines of code that are expected to raise the exception.
       with self.assertRaises(ValueError,msg="Must raise an error if the format is invalid."):
           Player("AB001","NameA","FirstnameA","01-08-1995","clubA")
  '''
   def test_birth_date_valid_formats(self):
       self.assertEqual(self.player._birth_date, date(1995, 8, 1), "Birth date should be 1995-08-01")  # test the value


   def test_birth_date_invalid_format(self):
       with self.assertRaises(ValueError):
           Player("ID004", "G", "H", "32/01/2000", "Club W")  # Date invalide
       with self.assertRaises(ValueError):
           Player("ID004", "G", "H", "01/01", "Club W")

   def test_update_score(self):
       self.player.update_score(1)
       self.assertEqual(self.player._score,1,"Score should be 1")

   #test if value write is  not in the right list [0,0.5,1]
   def test_update_score_no_in_list(self):
       self.player.update_score(0.75)
       self.assertEqual(self.player._score,0,"Score should not change if the value not in the list [0,0.5,1]")

   def test_add_match(self):
       self.player.add_match("AB002",1)
       self.assertEqual(len(self.player._match_history),1,"Match history should be 1 result")
       self.assertEqual(self.player._match_history[0],{"opponent_id":"AB002", "result":1},"the match add is incorrect")

   def test_add_match_multiple(self):
       self.player.add_match("AB003",0.5)
       self.player.add_match("AB004",0)
       self.assertEqual(len(self.player._match_history),2,"Match history should be 2 results")


if __name__ == '__main__':
    unittest.main()








