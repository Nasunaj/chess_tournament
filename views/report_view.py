def display_report_menu():
    """Display the submenu for report"""
    print("\n--- Génération des rapports ---")
    print("1. Liste de tous les tournois")
    print("2. Historique d'un tournoi")
    print("3. Retour au menu principal")


def get_report_menu_choice():
    """Get the user's choice from the menu"""""
    return input("Choisissez une option (1-3) : ").strip()


def display_tournament_list(tournaments):
    """Display tournaments list"""
    print("\n--- Liste de tous les tournois ---")
    if not tournaments:
        print("Aucun tournoi existant.")
        return

    for idx, tournament in enumerate(tournaments, start=1):
        print(f"{idx}. {tournament['name']} ({tournament['location']})")
        print(f"   - Dates : {tournament['start_date']} -> "
              f"{tournament['end_date']}")
        print(f"   - Nombre de joueurs : {len(tournament['players'])}")
        print(f"   - Nombre de tours : {tournament['rounds']}\n")


def prompt_select_tournament(tournaments):
    """Prompt the user to select a tournament"""
    if not tournaments:
        print("Aucun tournoi existant.")
        return None

    for idx, tournament in enumerate(tournaments, start=1):
        print(f"{idx}. {tournament['name']}")

    try:
        choice = int(input("\nSélectionnez un tournoi (numéro) : ")) - 1
        if 0 <= choice < len(tournaments):
            return tournaments[choice]
        else:
            print("Numéro de tournoi invalide.")
            return None
    except ValueError:
        print("Saisie invalide. Veuillez entrer un numéro.")
        return None


def display_tournament_history(tournament):
    """Display tournament history"""
    print(f"\n--- Historique du Tournoi : {tournament['name']} ---")
    print(f"Lieu : {tournament['location']}")
    print(f"Dates : {tournament['start_date']} → {tournament['end_date']}")
    print(f"Nombre de joueurs : {len(tournament['players'])}")

    # Use .get() to avoid KeyError + check if the list not empty
    if tournament.get('rounds_list'):
        print("\n--- Tours et Matchs ---")
        for round in tournament['rounds_list']:
            print(f"\n{round['name']} (Début : {round['start_time']})")
            for match in round['matches']:
                player1 = match['player1']
                player2 = match['player2']
                if not match['result']:
                    result = "Non joué"
                else:
                    result = f"Résultat : {match['result']}"
                print(f"  - {player1} vs {player2} ({result})")
    else:
        print("\nAucun tour généré pour ce tournoi.")
