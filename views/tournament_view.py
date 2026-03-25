# Afficher les sous menus pour gérer les tournois
def display_tournament_menu():
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
    """Demande à l'utilisateur de sélectionner un tournoi."""
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


# Liste des tournois à afficher par ordre en se basant sur les indices. Dans controller/ il faudra lire le fichier json et faire la liste tournaments
def display_tournament_list(tournaments):
    print("\n-----------Liste des tournois-----------")
    for idx, tournament in enumerate(tournaments, 1):  # here start=1 else index start to 0
        print(f"{idx}. Tournoi {tournament['name']} à {tournament['location']} (id: {tournament['id_tournament']})")


def display_tournament_details(tournament):
    print(f"\n--- Détails du Tournoi : {tournament['name']} ---")
    print(f"Lieu : {tournament['location']}")
    print(f"Date de début : {tournament['start_date']}")
    print(f"Date de fin : {tournament['end_date']}")
    print(f"Nombre de tours : {tournament['rounds']}")

    if tournament['players']:
        print("\nListe des joueurs :")
        for player in tournament['players']:
            print(f"- {player['first_name']} {player['last_name']} (Score : {player['score']})")

    if 'rounds_list' in tournament and tournament['rounds_list']:
        print("\nListe des tours :")
        for round in tournament['rounds_list']:
            print(f"- {round['name']} (Début : {round['start_time']})")
            for match in round['matches']:
                player1 = f"{match['player1']} ({match.get('color_player1', '?')})"  # par defaut si la clé n'existe pas retourne '?'.
                player2 = f"{match['player2']} ({match.get('color_player2', '?')})"
                result = f"Résultat : {match['result']}" if match['result'] else "Non joué"
                print(f"  - {player1} vs {player2} ({result})")


# Focntion pour générer un 1er tour
def confirm_generate_first_round(tournament_name):
    """Demander confirmation pour générer le 1er tour"""
    return input("Générer le 1er tour pour le tournoi '{tournament_name}'? (o/n) : ").lower() == "o"


def prompt_match_results(match):
    print("Demande les résultats d'un match")
    print("\n_____Résultat du match: {match['player1']} vs {match['player2']}_____")
    print("1. Victoire de {match['player1']}")
    print("2. Victoire de {match['player2']}")
    print("3. Match nul")
    choice = input("Choisissez le résultat du match (1-3): ")
    return choice


def prompt_select_match(round):
    """Affiche les matchs d'un tour et demande à l'utilisateur d'en sélectionner un."""
    print("\n--- Matchs disponibles ---")
    matches = []
    for i, match in enumerate(round._matches, start=1):
        player1 = f"{match._player1.first_name} {match._player1.last_name}"
        player2 = f"{match._player2.first_name} {match._player2.last_name}"
        result = "Non joué" if not match._result else f"Résultat : {match._result}"
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
    """Afficher le classement des joueurs triés par score décroissant"""
    print("\n____Classement des joueurs____")
    if not players:
        print("Aucun joueur dans le tournoi")
        return

    # tri par score décroissant puis par nom
    sorted_players = sorted(players, key=lambda p: (-p["score"], p["last_name"], p["first_name"]))  # ici -p  décroissant ne peut pas etre appliqué à un str, donc laissons pour nom et prénom l'ordre croissant.
    print("{:<5} {:<20} {:<20} {:>10}".format("Rang", "Nom", "Prenom", "Score"))  # alignement text et nb caractères
    print("-" * 60)
    for rank, player in enumerate(sorted_players, start=1):
        # print("{:<5} {:<20} {:<20} {:>10.1f}".format(rank,player["first_name"], player["last_name"], player["score"])) # 1.f arrondi au dixième (1 chiffre après la virgule)
        print("{:<5} {:<20} {:<20} {:>10}".format(rank, player["first_name"], player["last_name"], player["score"]))
