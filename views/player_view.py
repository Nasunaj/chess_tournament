def display_player_menu():
    print("\n---Gestion des joeurs---")
    print("1. Créer un joueur")
    print("2. Voir la liste des joueurs")
    print("3. Voir l'historique d'un joueur")
    print("4. Retour au menu principal")


def get_player_menu_choice():
    """Retourne le choix du joueur."""
    return input("Choisissez une option (1-3): ").strip()


def prompt_player_data():
    print("\n---Nouveau joueur---")
    first_name = input("Prénom du joueur: ")
    last_name = input("Nom du joueur: ")
    national_id = input("Identifiant national (ex: AB12345) : ")
    birth_date = input("Date de naissance (JJ/MM/AAAA) : ")
    club = input("Club : ")
    return {
        "first_name": first_name,
        "last_name": last_name,
        "national_id": national_id,
        "birth_date": birth_date,
        "club": club
    }


def display_player_list(players):
    print("\n---Liste des joueurs---")
    if not players:
        print("Aucun joueur enregistré")
        return

    for idx, player in enumerate(players, start=1):
        print(f"{idx}. {player['first_name']} {player['last_name']} ({player['national_id']} - {player['club']})")


def prompt_select_player(players):
    """Demande à l'utilisateur de sélectionner un joueur."""
    if not players:
        print("Aucun joueur disponible.")
        return None

    display_player_list(players)  # Affiche la liste des joueurs

    try:
        choice = int(input("\nSélectionnez un joueur (numéro) : ")) - 1
        if 0 <= choice < len(players):
            return players[choice]  # Retourne le dictionnaire du joueur sélectionné
        else:
            print("Numéro invalide.")
            return None
    except ValueError:
        print("Saisie invalide. Veuillez entrer un numéro.")
        return None
