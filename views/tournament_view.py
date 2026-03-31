def display_tournament_menu():
    """Display the submenu to manage the tournaments"""
    print("\n-----------Gestion des tournois-----------")
    print("1. Créer un tournoi")
    print("2. Voir les tournois existants")
    print("3. Voir les détails d'un tournoi")
    print("4. Ajouter un joueur à un tournoi")
    print("5. Générer le 1er tour")
    print("6. Générer le tour suivant")
    print("7. Saisir les résultats d'un match")
    print("8. Voir le classement")
    print("9. Retour au menu principal")


# Récupérer le choix de l'utilisateur
def get_tournament_menu_choice():
    """Get the user's choice from the menu"""
    return input("Choisissez une option entre 1 et 9: ")


# Demander à l'utilisateur les informations pour créer le tournoi
def prompt_tournament_creation():
    print("\n-----------Création d'un nouveau tournoi-----------")
    name = input("Nom du tournoi : ")
    location = input("Lieu du tournoi : ")
    start_date = input("Date de début du tournoi (format : YYYY-MM-DD): ")
    end_date = input("Date de fin du tournoi (format : YYYY-MM-DD): ")
    rounds = input("Nombre de tour (par défaut 4) : ") or "4"

    return {
        "name": name,
        "location": location,
        "start_date": start_date,
        "end_date": end_date,
        "rounds": rounds
    }


def prompt_select_tournament(tournaments):
    """Ask the user to select a tournament"""
    display_tournament_list(tournament.to_dict() for tournament in tournaments)
    try:
        choice = int(input("Saisir le numéro correspondant au tournoi : "))
        if 1 <= choice <= len(tournaments):
            return tournaments[choice - 1]
        else:
            print("Numéro du tournoi invalide")
            return None
    except ValueError:
        print("Saisie invalide, veuillez saisir un numéro.")
        return None


def display_tournament_list(tournaments):
    """List of tournaments to display in order based on indices.
    In the controller/, you will need to read the JSON file and
    create the tournaments list."""
    print("\n-----------Liste des tournois-----------")
    # here start=1 else index start to 0
    for idx, tournament in enumerate(tournaments, 1):
        print(f"{idx}. Tournoi {tournament['name']} à "
              f"{tournament['location']} (id: {tournament['id_tournament']})")


def display_tournament_details(tournament):
    """Display the tournament details"""
    print(f"\n--- Détails du Tournoi : {tournament['name']} ---")
    print(f"Lieu : {tournament['location']}")
    print(f"Date de début : {tournament['start_date']}")
    print(f"Date de fin : {tournament['end_date']}")
    print(f"Nombre de tours : {tournament['rounds']}")

    if tournament['players']:
        print("\nListe des joueurs :")
        for player in tournament['players']:
            print(f"- {player['first_name']} {player['last_name']} (Score : "
                  f"{player['score']})")

    if 'rounds_list' in tournament and tournament['rounds_list']:
        print("\nListe des tours :")
        for round in tournament['rounds_list']:
            print(f"- {round['name']} (Début : {round['start_time']})")
            for match in round['matches']:
                # By default, if the key not exist return ?.
                player1 = (f"{match['player1']} "
                           f"({match.get('color_player1', '?')})")
                player2 = (f"{match['player2']} "
                           f"({match.get('color_player2', '?')})")
                if match['result']:
                    result = f"Résultat : {match['result']}"
                else:
                    result = "Non joué"
                print(f"  - {player1} vs {player2} ({result})")


def confirm_generate_first_round(tournament_name):
    """Ask a confirmation to generate first round."""
    return input("Générer le 1er tour pour le tournoi "
                 "'{tournament_name}'? (o/n) : ").lower() == "o"


def prompt_match_results(match):
    """Display the match results"""
    print("Demande les résultats d'un match")
    print("\n_____Résultat du match: {match['player1']} vs "
          "{match['player2']}_____")
    print("1. Victoire de {match['player1']}")
    print("2. Victoire de {match['player2']}")
    print("3. Match nul")
    choice = input("Choisissez le résultat du match (1-3): ")
    return choice


def prompt_select_match(round):
    """Display the matchs of a round and ask user to select one."""
    print("\n--- Matchs disponibles ---")
    matches = []
    for i, match in enumerate(round._matches, start=1):
        player1 = f"{match._player1.first_name} {match._player1.last_name}"
        player2 = f"{match._player2.first_name} {match._player2.last_name}"
        result = "Non joué" if not match._result else (f"Résultat : "
                                                       f"{match._result}")
        print(f"{i}. {player1} vs {player2} ({result})")
        matches.append(match)

    try:
        choice = int(input("\nSélectionnez un match (numéro) : ")) - 1
        if 0 <= choice < len(matches):
            return matches[choice]
        else:
            print("Numéro de match invalide.")
            return None
    except ValueError:
        print("Saisie invalide. Veuillez entrer un numéro.")
        return None


def display_ranking(players):
    """Display the ranking of the players (decreasing value score)"""
    print("\n____Classement des joueurs____")
    if not players:
        print("Aucun joueur dans le tournoi")
        return

    # tried by first decreasing score , second increasing name
    sorted_players = sorted(players,
                            key=lambda p: (-p["score"], p["last_name"],
                                           p["first_name"]))
    # Align text et nb characters
    print("{:<5} {:<20} {:<20} {:>10}".format("Rang", "Nom",
                                              "Prenom", "Score"))
    print("-" * 60)
    for rank, player in enumerate(sorted_players, start=1):
        print("{:<5} {:<20} {:<20} {:>10}".format(rank,
                                                  player["first_name"],
                                                  player["last_name"],
                                                  player["score"]))
