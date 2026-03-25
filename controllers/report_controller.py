from controllers.tournament_controller import TournamentController
from views.report_view import (
    display_report_menu,
    get_report_menu_choice,
    display_tournament_list,
    prompt_select_tournament,
    display_tournament_history
)


class ReportController:
    def __init__(self, tournament_controller: TournamentController):  # Passe le contrôleur entier, pas juste la
        self.tournament_controller = tournament_controller  # Stocke le contrôleur

    def generate_reports(self):
        self.tournament_controller.load_tournaments()  # Chargement des tournois
        self.tournaments = self.tournament_controller.tournaments  # Mets à jour les listes
        while True:
            display_report_menu()
            choice = get_report_menu_choice()

            match choice:
                case "1":
                    self.list_all_tournaments()
                case "2":
                    self.show_tournament_history()
                case "3":
                    break
                case _:
                    print("Choix invalide. Réessayez.")

    def list_all_tournaments(self):
        # Convertit chaque objet Tournament en dictionnaire pour l'affichage
        tournaments_data = [tournament.to_dict() for tournament in self.tournaments]  # Convertit les tournois en dictionnaires pour la sélection
        display_tournament_list(tournaments_data)  # Appelle la vue

    def show_tournament_history(self):
        if not self.tournaments:
            print("Aucun tournoi existant.")
            return

        tournaments_data = [t.to_dict() for t in self.tournaments]
        selected_tournament = prompt_select_tournament(tournaments_data)  # Demande à l'utilisateur de sélectionner un tournoi
        if selected_tournament:
            display_tournament_history(selected_tournament)  # Affiche l'historique du tournoi sélectionné
