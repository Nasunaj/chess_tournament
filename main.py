from controllers.menu_controller import MenuController


def main():
    """Point d'entrée de l'application."""
    print("Bienvenue dans l'application de gestion de tournois d'échecs !")
    menu_controller = MenuController()  # Creates an instance of MenuController and calls the run() method to start the application
    menu_controller.run()


if __name__ == "__main__":
    main()
