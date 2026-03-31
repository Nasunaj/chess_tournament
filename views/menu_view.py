def display_menu():
    """Display the menu"""
    print("\n---------Menu principal--------")
    print("1. Gérer les tournois")
    print("2. Gérer les joueurs")
    print("3. Générer des rapports")
    print("4. Quitter")


def get_user_choice():
    """Get the user's choice from the menu"""
    return input("Choisi une option entre 1 et 4: ")


def display_option_selected(option):
    """Display the option selected by the user"""
    print(f"Vous avez  choisi {option}")
