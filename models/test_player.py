from player import Player

#Creating a player
player1 = Player("ID001", "Nom_A", "Prenom_A","1995-08-23",1200,"Club_A")

#Displaying player information
print(player1)

#Updating elo rating
player1.update_elo(1500)
print(f"new rating elo: {player1.elo}")

#Adding a match result
player1.add_match({"opponent": "ID002", "result": "win", "elo_change": +20})
print(f"match history:{player1.match_history}")

#Conversion to dictionary
player_dict = player1.to_dict()
print(player_dict)

