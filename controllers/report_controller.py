from controllers.tournament_controller import TournamentController
from views.report_view import (
    display_report_menu,
    get_report_menu_choice,
    display_tournament_list,
    prompt_select_tournament,
    display_tournament_history
)


class ReportController:
    """ReportController class."""

    # Pass the entier controller
    def __init__(self, tournament_controller: TournamentController):
        # store the controller
        self.tournament_controller = tournament_controller

    def generate_reports(self):
        """Generate reports from the tournament."""
        # Load tournament
        self.tournament_controller.load_tournaments()
        # Update the list
        self.tournaments = self.tournament_controller.tournaments
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
        """Convert each Tournament object to a dictionary for display."""
        # Convertit chaque objet Tournament en dictionnaire pour l'affichage
        tournaments_data = [
            tournament.to_dict()
            for tournament in self.tournaments
        ]
        display_tournament_list(tournaments_data)  # Call the view

    def show_tournament_history(self):
        """For the selected tournament, display the tournament history."""
        if not self.tournaments:
            print("Aucun tournoi existant.")
            return

        tournaments_data = [t.to_dict() for t in self.tournaments]
        # Ask the user to select a tournament
        selected_tournament = prompt_select_tournament(tournaments_data)
        if selected_tournament:
            # Display the history of the selected tournament
            display_tournament_history(selected_tournament)
