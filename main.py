from controllers.menu_controller import MenuController


def main():
    """Application entry point."""
    print("Welcome to the chess tournament management application !")
    '''Creates an instance of MenuController and calls the run()
    method to start the application'''
    menu_controller = MenuController()
    menu_controller.run()


if __name__ == "__main__":
    main()
