def display_player_menu():
    """Display the submenu to manage players"""
    print("\n---Gestion des joeurs---")
    print("1. Créer un joueur")
    print("2. Voir la liste des joueurs")
    print("3. Voir l'historique d'un joueur")
    print("4. Retour au menu principal")


def get_player_menu_choice():
    """Get the user's choice from the menu"""
    """Retourne le choix du joueur."""
    return input("Choisissez une option (1-3): ").strip()


def prompt_player_data():
    """Prompt the user to enter their data"""
    print("\n---Nouveau joueur---")
    first_name = input("Prénom du joueur: ")
    last_name = input("Nom du joueur: ")
    national_id = input("Identifiant national (ex: AB12345) : ")
    birth_date = input("Date de naissance (yyyy-mm-dd) : ")
    club = input("Club : ")
    return {
        "first_name": first_name,
        "last_name": last_name,
        "national_id": national_id,
        "birth_date": birth_date,
        "club": club
    }


def display_player_list(players):
    """Display the players list"""
    print("\n---Liste des joueurs---")
    if not players:
        print("Aucun joueur enregistré")
        return

    for idx, player in enumerate(players, start=1):
        print(f"{idx}. {player['first_name']} {player['last_name']} "
              f"({player['national_id']} - {player['club']})")


def prompt_select_player(players):
    """Prompt the user to select a player"""
    if not players:
        print("Aucun joueur disponible.")
        return None

    display_player_list(players)

    try:
        choice = int(input("\nSélectionnez un joueur (numéro) : ")) - 1
        if 0 <= choice < len(players):
            # Return the dictionary of the selected player.
            return players[choice]
        else:
            print("Numéro invalide.")
            return None
    except ValueError:
        print("Saisie invalide. Veuillez entrer un numéro.")
        return None
