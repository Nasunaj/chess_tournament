from views.player_view import (display_player_menu, get_player_menu_choice,
                               prompt_player_data, display_player_list,
                               prompt_select_player)
from models.player import Player
import os
import json
import glob


class PlayerController:
    """ PLayerController class """
    def __init__(self):
        self.players = []
        self.load_players()  # Load all players at startup

    def load_players(self):
        """Load all players from individual JSON files."""
        self.players.clear()
        player_dir = "data/players"

        # Create folder if it not exist
        os.makedirs(player_dir, exist_ok=True)

        # Load each JSON file in the folder
        for file_path in glob.glob(os.path.join(player_dir, "*.json")):
            try:
                with open(file_path, "r") as file:
                    player_data = json.load(file)

                    # Filter fields to keep only those expected by Player
                    filtered_data = {
                        "national_id": player_data["national_id"],
                        "last_name": player_data["last_name"],
                        "first_name": player_data["first_name"],
                        "birth_date": player_data["birth_date"],
                        "club": player_data["club"]
                    }

                    self.players.append(Player(**filtered_data))
            except Exception as e:
                print(f"Erreur lors du chargement du joueur {file_path}: {e}")

    def save_players(self):
        """Save all players to individual JSON file."""
        player_dir = "data/players"
        os.makedirs(player_dir, exist_ok=True)  # Create folder if it not exist

        for player in self.players:
            file_name = f"{player.last_name}_{player.national_id}.json"
            file_path = os.path.join(player_dir, file_name)

            try:
                with open(file_path, "w") as file:
                    json.dump(player.to_dict(), file, indent=4)
            except Exception as e:
                print(f"Erreur lors de la sauvegarde du joueur "
                      f"{player.last_name}: {e}")

    # 20-03-2026 modif
    def update_player_after_match(self, national_id, opponent_id,
                                  result, color):
        """Update a player's score and match history after a match."""
        for player in self.players:
            if player.national_id == national_id:
                # Use the existing _add_match method from the Player
                player._add_match(opponent_id, result, color)
                self.save_players()  # Save all players
                break

    def manage_players(self):
        """Perform tasks based on the user's choice"""
        self.load_players()
        while True:
            display_player_menu()
            choice = get_player_menu_choice()

            match choice:
                case "1":
                    self.create_player()
                case "2":
                    display_player_list([p.to_dict() for p in self.players])
                case "3":
                    self.show_player_history()  # Option to view history
                case "4":
                    break
                case _:
                    print("Choix invalide. Réessayez.")

    def create_player(self):
        """Create a new player and save it to the JSON file."""
        player_data = prompt_player_data()
        try:
            # Check if national_id is unique
            if any(
                    p.national_id == player_data["national_id"]
                    for p in self.players
            ):
                print("Erreur : Un joueur avec cet identifiant "
                      "national existe déjà.")
                return

            new_player = Player(
                first_name=player_data["first_name"],
                last_name=player_data["last_name"],
                national_id=player_data["national_id"],
                birth_date=player_data["birth_date"],
                club=player_data["club"]
            )
            self.players.append(new_player)
            self.save_players()  # Save all the players (including the new one)
            print(f"Joueur {new_player.first_name} "
                  f"{new_player.last_name} créé avec succès !")
        except Exception as e:
            print(f"Erreur lors de la création du joueur : {e}")

    def show_player_history(self):
        """Display the match history of a selected player."""
        if not self.players:
            print("Aucun joueur enregistré.")
            return
        player_dir_tournament = "data/tournaments/"

        selected_player = prompt_select_player(
            [p.to_dict() for p in self.players]
        )
        if selected_player:
            print(f"\n--- Historique de {selected_player['first_name']}"
                  f" {selected_player['last_name']} ---")
            history_list_match_index = 0
            for file_path in glob.glob(
                    os.path.join(player_dir_tournament, "*.json")
            ):
                try:
                    with open(file_path, "r") as file:
                        data_tournament = json.load(file)
                    player_tournament = data_tournament['players']
                    for player in player_tournament:
                        if (
                                selected_player['national_id']
                                == player['national_id']
                        ):
                            history_list_match_index += 1
                            print(f"--Tournoi : {data_tournament['name']}")
                            for match_history in player['match_history']:
                                print(f"- Contre "
                                      f"{match_history['opponent_id']} : "
                                      f"{match_history['result']} "
                                      f"({match_history['color']})")

                    if history_list_match_index == 0:
                        print("Aucun match joué.")

                except Exception as e:
                    print(f"Erreur load tournament {e}")
