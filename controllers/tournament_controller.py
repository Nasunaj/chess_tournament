from controllers.player_controller import PlayerController
from views.player_view import prompt_select_player
from views.tournament_view import (display_tournament_menu, get_tournament_menu_choice, prompt_tournament_creation,
                                   display_tournament_list, display_tournament_details, prompt_select_tournament,
                                   prompt_select_match, prompt_match_results, display_ranking)
import os
from models.tournament import Tournament
from datetime import datetime


class TournamentController:
    def __init__(self):
        self.tournaments = []  # initialisation (vérification si l'instance existe.)

    def load_tournaments(self):
        """ Chargement des tournois depuis des fichiers Json du dossier data/tournaments"""
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
                        tournament = Tournament.load_from_json(file_path)  # appel de la méthode du modèle class Tournament
                        self.tournaments.append(tournament)
                        print(f"Tournoi chargé : {tournament.name}")  # Débogage
                    except Exception as e:
                        print(f"Erreur during loading tournament {file_path}: {e}")
        except FileNotFoundError:
            print("Aucun tournoi trouvé.")  # Le dossier n'existe pas encore

    def create_tournament(self):
        """Créer un nouveau tournoi à partir des données saisies par l'utilisateur"""
        tournament_data = prompt_tournament_creation()

        # conversion et validation des données
        try:
            tournament_data["start_date"] = datetime.strptime(tournament_data["start_date"], "%Y-%m-%d")
            tournament_data["end_date"] = datetime.strptime(tournament_data["end_date"], "%Y-%m-%d")
            tournament_data["rounds"] = int(tournament_data["rounds"])

            if not tournament_data["name"].strip():  # supprime l'espace avant et après le nom
                print("Erreur: le nom du tournoi ne peut pas être vide.")
                return  # arrête la méthode : le tournoi n'est pas créé, et l'utilisateur retourne au menu des tournois.

            if tournament_data["rounds"] < 4:
                print("Le nombre de tour doit être d'au moins de 4.")
                return

            # la validation end_date > start_date est gérée dans models dans la class Tournament.

        except ValueError as e:
            print(f"Erreur de saisie: {e}")
            return

        try:
            new_tournament = Tournament(**tournament_data)  # ** est un opérateur qui dépaquette un dictionnaire en arguments nommés pour une fonction ou un constructeur.
            # new_tournament.save_to_json(f"data/tournaments/{new_tournament.name}.json")  # sauvegarde dans un nouveau fichier
            new_tournament.save_to_json()  # sauvegarde dans un nouveau fichier
            self.load_tournaments()  # recharge pour inclure le nouveau tournoi : met à jour immédiatement la liste self.tournaments en mémoire.
            print(f"Tournoi {tournament_data['name']} a été créé avec succès et a été enregistré dans le dossier data/tournaments/.")
        except Exception as e:
            print(f"Erreur lors de la création du tournoi : {e}")

    def display_tournament(self):
        """ Affiche la liste des tournois chargés"""
        if not self.tournaments:
            print("Aucun tournoi existant.")
        else:
            # Parcourt chaque objet Tournament dans self.tournaments.
            # Pour chaque objet, appelle sa méthode to_dict() pour le convertir en dictionnaire.
            display_tournament_list([tournament.to_dict() for tournament in self.tournaments])

    def show_tournament_details(self):
        """Affiche les détails du tournoi choisi"""
        if not self.tournaments:
            print("Aucun tournoi existant.")
            return
        selected_tournament = prompt_select_tournament(self.tournaments)
        if selected_tournament:
            display_tournament_details(selected_tournament.to_dict())

    def add_player_to_tournament(self):
        """Ajoute un joueur à un tournoi sélectionné"""
        if not self.tournaments:
            print("Aucun tournoi existant.")
            return

        # Sélectionne un tournoi
        selected_tournament = prompt_select_tournament(self.tournaments)
        if not selected_tournament:
            return

        # Charger la liste des joueurs disponibles
        player_controller = PlayerController()
        available_players = player_controller.players
        if not available_players:
            print("Aucun joueur enregistré. Utilisez d'abord le menu des joueurs pour en créer.")
            return

        # Sélection du joueur
        selected_player_data = prompt_select_player([p.to_dict() for p in available_players])
        if not selected_player_data:
            return

        # Vérifier que le joueur n'est pas déjà inscrit
        if any(
                hasattr(p, 'national_id') and p.national_id == selected_player_data['national_id']
                for p in selected_tournament._players
        ):
            print("Ce joueur est déjà inscrit à ce tournoi.")
            return

        # Trouver l'objet Player complet dans player_controller.players
        selected_player = next(
            p for p in available_players
            if p.national_id == selected_player_data['national_id']
        )

        # Ajouter le joueur existant au tournoi (pas de nouvelle instance)
        selected_tournament._players.append(selected_player)  # ✅ Utilise l'objet existant

        # Sauvegarder le tournoi
        selected_tournament.save_to_json(f"data/tournaments/{selected_tournament.name}.json")
        print(f"Joueur {selected_player.first_name} {selected_player.last_name} ajouté au tournoi !")

    def generate_first_round(self):
        """Générer le 1er tour pour un tournoi sélectionné"""
        if not self.tournaments:
            print("Aucun tournoi existant.")
            return
        selected_tournament = prompt_select_tournament(self.tournaments)
        if not selected_tournament:
            return

        try:
            selected_tournament.generate_first_round()
            selected_tournament.save_to_json(f"data/tournaments/{selected_tournament.name}.json")
            print("Premier tour généré avec succès.")
        except ValueError as e:
            print(f"Erreur : {e}")

    def enter_match_results(self):
        """Permet de saisir les résultats d'un match"""
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
            "player1": f"{selected_match._player1.first_name} {selected_match._player1.last_name}",
            "player2": f"{selected_match._player2.first_name} {selected_match._player2.last_name}"
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
        selected_match._player1._add_match(selected_match._player2.national_id, selected_match._result[0], selected_match._color_player1)
        selected_match._player2._add_match(selected_match._player1.national_id, selected_match._result[1], selected_match._color_player2)

        selected_tournament.save_to_json(f"data/tournaments/{selected_tournament.name}.json")
        print("Résultat enregistré avec succès !")

    def generate_next_round(self):
        """Générer le tour suivant pour un tournoi sélectionné"""
        if not self.tournaments:
            print("Aucun tournoi existant.")
            return

        selected_tournament = prompt_select_tournament(self.tournaments)
        if not selected_tournament:
            return

        # Vérification qu'il y ait au moins un tour existant
        if not selected_tournament._rounds_list:
            print("erreur aucun tour n'a encore été généré pour ce tournoi. Utiliser d'abord générer le tour")

        else:
            # Vérification que tous les matchs du dernier tour ont un résultat
            last_round = selected_tournament._rounds_list[-1]
            for match in last_round._matches:
                if not match._result:
                    print("Tous les matchs de ce tour doivent avoir un résultat avant de générer un tour.")
                    return

            try:
                selected_tournament.generate_next_round()
                selected_tournament.save_to_json(f"data/tournaments/{selected_tournament.name}.json")
                print(f"Tour {len(selected_tournament._rounds_list)} généré avec succès.")
            except ValueError as e:
                print(f"Erreur : {e}")

    def show_ranking(self):
        """Affiche le classement des joueurs d'un tournoi sélectionné"""
        if not self.tournaments:
            print("Aucun tournoi existant.")
            return
        selected_tournament = prompt_select_tournament(self.tournaments)
        if not selected_tournament:
            return
        if not selected_tournament._players:
            print("Aucun joueur dans ce tournoi.")
            return

        # convertir les objets Player en dictionnaires pour l'affichage
        player_data = [player.to_dict() for player in selected_tournament._players]
        display_ranking(player_data)

    def manage_tournaments(self):
        """ gestion des sous menus des tournois."""
        self.load_tournaments()
        # print(f"DEBUG: {len(self.tournaments)} tournois chargés.")  # Affiche le nombre de tournois chargés
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
                    break  # quitte cette boucle donc revient à la boucle principale
                case _:
                    print("Choix invalide")
