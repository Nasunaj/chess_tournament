from views.player_view import display_player_menu, get_player_menu_choice, prompt_player_data, display_player_list, prompt_select_player
from models.player import Player
import os
import json
import glob


class PlayerController:
    def __init__(self):
        self.players = []
        self.load_players()  # Charge tous les joueurs au démarrage

    def load_players(self):
        """Charge tous les joueurs depuis les fichiers JSON individuels."""
        self.players.clear()
        player_dir = "data/players"

        # Crée le dossier s'il n'existe pas
        os.makedirs(player_dir, exist_ok=True)

        # Charge chaque fichier JSON dans le dossier
        for file_path in glob.glob(os.path.join(player_dir, "*.json")):
            try:
                with open(file_path, "r") as file:
                    player_data = json.load(file)

                    # Filtre les champs pour ne garder que ceux attendus par Player
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
        """Sauvegarde tous les joueurs dans des fichiers JSON individuels."""
        player_dir = "data/players"
        os.makedirs(player_dir, exist_ok=True)  # Crée le dossier s'il n'existe pas

        for player in self.players:
            file_name = f"{player.last_name}_{player.national_id}.json"
            file_path = os.path.join(player_dir, file_name)

            try:
                with open(file_path, "w") as file:
                    json.dump(player.to_dict(), file, indent=4)
            except Exception as e:
                print(f"Erreur lors de la sauvegarde du joueur {player.last_name}: {e}")

    # 20-03-2026 modif
    def update_player_after_match(self, national_id, opponent_id, result, color):
        """Met à jour le score et l'historique d'un joueur après un match."""
        for player in self.players:
            if player.national_id == national_id:
                # Utilise la méthode existante _add_match du modèle Player
                player._add_match(opponent_id, result, color)
                self.save_players()  # Sauvegarde tous les joueurs
                break

    # 20-03-2026 fin modif
    def manage_players(self):
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
                    self.show_player_history()  # Option pour voir l'historique
                case "4":
                    break
                case _:
                    print("Choix invalide. Réessayez.")

    def create_player(self):
        player_data = prompt_player_data()
        try:
            # Vérifie que le national_id est unique
            if any(p.national_id == player_data["national_id"] for p in self.players):
                print("Erreur : Un joueur avec cet identifiant national existe déjà.")
                return

            new_player = Player(
                first_name=player_data["first_name"],
                last_name=player_data["last_name"],
                national_id=player_data["national_id"],
                birth_date=player_data["birth_date"],
                club=player_data["club"]
            )
            self.players.append(new_player)
            self.save_players()  # Sauvegarde tous les joueurs (y compris le nouveau)
            print(f"Joueur {new_player.first_name} {new_player.last_name} créé avec succès !")
        except Exception as e:
            print(f"Erreur lors de la création du joueur : {e}")

    def show_player_history(self):
        """Affiche l'historique des matchs d'un joueur sélectionné."""
        if not self.players:
            print("Aucun joueur enregistré.")
            return
        player_dir_tournament = "data/tournaments/"

        selected_player = prompt_select_player([p.to_dict() for p in self.players])
        if selected_player:
            print(f"\n--- Historique de {selected_player['first_name']} {selected_player['last_name']} ---")
            history_list_match_index = 0
            for file_path in glob.glob(os.path.join(player_dir_tournament, "*.json")):
                try:
                    with open(file_path, "r") as file:
                        data_tournament = json.load(file)
                    player_tournament = data_tournament['players']
                    for player in player_tournament:
                        if selected_player['national_id'] == player['national_id']:
                            history_list_match_index += 1
                            print(f"--Tournoi : {data_tournament['name']}")
                            for match_history in player['match_history']:
                                print(f"- Contre {match_history['opponent_id']} : {match_history['result']} ({match_history['color']})")

                    if history_list_match_index == 0:
                        print("Aucun match joué.")

                except Exception as e:
                    print(f"Erreur load tournament {e}")
            '''
            print(selected_player['national_id'])
            player = next(p for p in self.players if p.national_id == selected_player['national_id'])
            print(f"\n--- Historique de {player.first_name} {player.last_name} ---")
            if not player._match_history:
                print(player)
                print("Aucun match joué.")
            else:
                print(player)
                for match in player.match_history:
                    print(f"- Contre {match['opponent_id']} : {match['result']} ({match['color']})")
            '''
