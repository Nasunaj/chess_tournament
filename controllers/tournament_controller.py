from controllers.player_controller import PlayerController
from views.player_view import prompt_select_player
from views.tournament_view import (display_tournament_menu,
                                   get_tournament_menu_choice,
                                   prompt_tournament_creation,
                                   display_tournament_list,
                                   display_tournament_details,
                                   prompt_select_tournament,
                                   prompt_select_match, prompt_match_results,
                                   display_ranking)
import os
from models.tournament import Tournament
from datetime import datetime


class TournamentController:
    """TournamentController class"""
    def __init__(self):
        self.tournaments = []  # initialisation (check inf instance exists)

    def load_tournaments(self):
        """Load tournaments from JSON files in the data/tournaments folder"""
        self.tournaments.clear()  # vide la liste avant de recharger
        tournament_dir = "data/tournaments"

        if not os.path.exists(tournament_dir):
            os.makedirs(tournament_dir)
            return

        try:
            for filename in os.listdir(tournament_dir):
                if filename.endswith(".json"):
                    file_path = os.path.join(tournament_dir, filename)
                    try:
                        # Call the method from class Tournament
                        tournament = Tournament.load_from_json(file_path)
                        self.tournaments.append(tournament)
                    except Exception as e:
                        print(f"Erreur durant le chargement du tournoi "
                              f"{file_path}: {e}")
        except FileNotFoundError:
            print("Aucun tournoi trouvé.")  # Folder don't yet exist

    def create_tournament(self):
        """Create new tournament from user input data"""
        tournament_data = prompt_tournament_creation()

        # Data conversion and validation
        try:
            tournament_data["start_date"] = datetime.strptime(
                tournament_data["start_date"],
                "%Y-%m-%d")
            tournament_data["end_date"] = datetime.strptime(
                tournament_data["end_date"],
                "%Y-%m-%d")
            tournament_data["rounds"] = int(tournament_data["rounds"])

            if not tournament_data["name"].strip():
                print("Erreur: le nom du tournoi ne peut pas être vide.")
                '''Stop the method: the tournament didn't create and the user
                return to the menu choices.'''
                return

            if tournament_data["rounds"] < 4:
                print("Le nombre de tour doit être d'au moins de 4.")
                return

            '''The validation end_date > start_date is generated in the
            models class Tournament.'''

        except ValueError as e:
            print(f"Erreur de saisie: {e}")
            return

        try:
            ''' ** is an operator that unpacks a dictionary into names
            arguments for a function or contractor.'''
            new_tournament = Tournament(**tournament_data)
            new_tournament.save_to_json()  # Save in a new file
            '''Reload to include the new tournament : immediately updates
            the self.tournaments list in memory'''
            self.load_tournaments()
            print(f"Tournoi {tournament_data['name']} a été créé avec succès "
                  f"et a été enregistré dans le dossier data/tournaments/.")
        except Exception as e:
            print(f"Erreur lors de la création du tournoi : {e}")

    def display_tournament(self):
        """ Display the list of loaded tournaments"""
        if not self.tournaments:
            print("Aucun tournoi existant.")
        else:
            '''Iterate over each Tournament object in elf.tournaments.
            For each object, call its to_dict() method to covert it to
            a dictionary.'''
            display_tournament_list(
                [tournament.to_dict() for tournament in self.tournaments]
            )

    def show_tournament_details(self):
        """Display the details of the selected tournament"""
        if not self.tournaments:
            print("Aucun tournoi existant.")
            return
        selected_tournament = prompt_select_tournament(self.tournaments)
        if selected_tournament:
            display_tournament_details(selected_tournament.to_dict())

    def add_player_to_tournament(self):
        """Add a player to a selected tournament"""
        if not self.tournaments:
            print("Aucun tournoi existant.")
            return

        # Select a tournament
        selected_tournament = prompt_select_tournament(self.tournaments)
        if not selected_tournament:
            return

        # Charger la liste des joueurs disponibles
        player_controller = PlayerController()
        available_players = player_controller.players
        if not available_players:
            print("Aucun joueur enregistré. Utilisez d'abord "
                  "le menu des joueurs pour en créer.")
            return

        # Select a player
        selected_player_data = prompt_select_player(
            [p.to_dict() for p in available_players]
        )
        if not selected_player_data:
            return

        # Check if player is not already record.
        if any(
                hasattr(p, 'national_id')
                and p.national_id == selected_player_data['national_id']
                for p in selected_tournament._players
        ):
            print("Ce joueur est déjà inscrit à ce tournoi.")
            return

        # Trouver l'objet Player complet dans player_controller.players
        selected_player = next(
            p for p in available_players
            if p.national_id == selected_player_data['national_id']
        )

        # Add existant player to the tournament (not a new instance)
        # Use existant object
        selected_tournament._players.append(selected_player)

        '''Save the tournament le tournoi
        selected_tournament.save_to_json
        (f"data/tournaments/{selected_tournament.name}.json")'''
        selected_tournament.save_to_json()
        print(f"Joueur {selected_player.first_name} "
              f"{selected_player.last_name} ajouté au tournoi !")

    def generate_first_round(self):
        """ Generate the first round for a selected tournament"""
        if not self.tournaments:
            print("Aucun tournoi existant.")
            return
        selected_tournament = prompt_select_tournament(self.tournaments)
        if not selected_tournament:
            return

        try:
            selected_tournament.generate_first_round()
            selected_tournament.save_to_json()
            print("Premier tour généré avec succès.")
        except ValueError as e:
            print(f"Erreur : {e}")

    def enter_match_results(self):
        """Allow to write the results of a match"""
        if not self.tournaments:
            print("Aucun tournoi existant.")
            return

        selected_tournament = prompt_select_tournament(self.tournaments)
        if not selected_tournament:
            return

        if not selected_tournament._rounds_list:
            print("Erreur : Aucun tour n'a été généré pour ce tour")
            return

        # Sélection du dernier tour généré
        current_round = selected_tournament._rounds_list[-1]
        if not current_round._matches:
            print("Aucun match n'a été généré pour ce tour")
            return

        selected_match = prompt_select_match(current_round)
        if not selected_match:
            return

        result_choice = prompt_match_results({
            "player1": f"{selected_match._player1.first_name} "
                       f"{selected_match._player1.last_name}",
            "player2": f"{selected_match._player2.first_name} "
                       f"{selected_match._player2.last_name}"
        })

        if result_choice == "1":
            selected_match._result = (1, 0)
        elif result_choice == "2":
            selected_match._result = (0, 1)
        elif result_choice == "3":
            selected_match._result = (0.5, 0.5)
        else:
            print("Choix invalide.")
            return
        selected_match._player1._add_match(selected_match._player2.national_id,
                                           selected_match._result[0],
                                           selected_match._color_player1)
        selected_match._player2._add_match(selected_match._player1.national_id,
                                           selected_match._result[1],
                                           selected_match._color_player2)

        selected_tournament.save_to_json()
        print("Résultat enregistré avec succès !")

    def generate_next_round(self):
        """Generate the next round for a selected tournament"""
        if not self.tournaments:
            print("Aucun tournoi existant.")
            return

        selected_tournament = prompt_select_tournament(self.tournaments)
        if not selected_tournament:
            return

        # Vérification qu'il y ait au moins un tour existant
        if not selected_tournament._rounds_list:
            print("erreur aucun tour n'a encore été généré pour ce tournoi. "
                  "Utiliser d'abord générer le tour")

        else:
            # Check if all the matchs of the last round have a result
            last_round = selected_tournament._rounds_list[-1]
            for match in last_round._matches:
                if not match._result:
                    print("Tous les matchs de ce tour doivent avoir "
                          "un résultat avant de générer un tour.")
                    return

            try:
                selected_tournament.generate_next_round()
                selected_tournament.save_to_json()
                print(f"Tour {len(selected_tournament._rounds_list)} "
                      f"généré avec succès.")
            except ValueError as e:
                print(f"Erreur : {e}")

    def show_ranking(self):
        """Display the players ranking of a selected tournament"""
        if not self.tournaments:
            print("Aucun tournoi existant.")
            return
        selected_tournament = prompt_select_tournament(self.tournaments)
        if not selected_tournament:
            return
        if not selected_tournament._players:
            print("Aucun joueur dans ce tournoi.")
            return

        # convert the Player objects to a dictionary for display
        player_data = [
            player.to_dict() for player in selected_tournament._players
        ]
        display_ranking(player_data)

    def manage_tournaments(self):
        """ Tournament submenu management."""
        self.load_tournaments()
        while True:
            display_tournament_menu()
            choice = get_tournament_menu_choice()
            match choice:
                case "1":
                    self.create_tournament()
                case "2":
                    self.display_tournament()
                case "3":
                    self.show_tournament_details()
                case "4":
                    self.add_player_to_tournament()
                case "5":
                    self.generate_first_round()
                case "6":
                    self.generate_next_round()
                case "7":
                    self.enter_match_results()
                case "8":
                    self.show_ranking()
                case "9":
                    break  # Exit this loop and return to the main loop
                case _:
                    print("Choix invalide")
