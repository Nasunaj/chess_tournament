from views.menu_view import (display_menu, get_user_choice,
                             display_option_selected)
from controllers.tournament_controller import TournamentController
from controllers.report_controller import ReportController
from controllers.player_controller import PlayerController


class MenuController:
    def __init__(self):
        """We initialize the controllers for tournaments,
        players and reports"""
        # Instantiation of the tournaments controller
        self.tournament_controller = TournamentController()
        self.report_controller = ReportController(self.tournament_controller)
        self.player_controller = PlayerController()

    def run(self):
        while True:
            display_menu()
            choice = get_user_choice()
            match choice:
                case "1":
                    # Call the tournaments submenu—entering a sub-loop here
                    self.tournament_controller.manage_tournaments()

                case "2":
                    self.player_controller.manage_players()

                case "3":
                    self.report_controller.generate_reports()

                case "4":
                    display_option_selected("Quitter l'application")
                    break
                case _:
                    display_option_selected("Choix invalide. Réessayez.")
