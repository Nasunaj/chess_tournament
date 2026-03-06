from models import Player, Tournament
from datetime import datetime, timedelta
import random

def main():
    # Création de 8 joueurs
    players = [
        Player("AB12345", "NameA", "FirstnameA", "1990-01-01", "Club A"),
        Player("CD67890", "NameB", "FirstnameB", "1995-02-02", "Club B"),
        Player("EF12345", "NameC", "FirstnameC", "1992-03-03", "Club C"),
        Player("GH67890", "NameD", "FirstnameD", "1988-04-04", "Club D"),
        Player("IJ12345", "NameE", "FirstnameE", "1993-05-05", "Club A"),
        Player("KL67890", "NameF", "FirstnameF", "1989-06-06", "Club B"),
        Player("MN12345", "NameG", "FirstnameG", "1991-07-07", "Club C"),
        Player("OP67890", "NameH", "FirstnameH", "1994-08-08", "Club D")
    ]

    # Création d'un tournoi
    tournament = Tournament(
        name="Summer Tournament",
        location="Paris",
        start_date=datetime(2026, 8, 1),
        end_date=datetime(2026, 8, 7),
        rounds=4
    )

    # Ajout des joueurs au tournoi
    for player in players:
        tournament.add_player(player)

    print("🏆 Tournoi créé avec 8 joueurs :")
    for player in tournament._players:
        print(f"  - {player}")

    # Génération des tours (2 tours pour l'exemple)
    for round_num in range(1, 3):
        print(f"\n--- Round {round_num} ---")
        if round_num == 1:
            current_round = tournament.generate_first_round()
        else:
            current_round = tournament.generate_next_round()

        # Simulation des résultats pour chaque match du tour
        for match in current_round._matches:
            # Résultat aléatoire
            result = random.choice([(1.0, 0.0), (0.5, 0.5), (0.0, 1.0)])
            match.set_result(*result)
            print(f"  Match : {match._player1.last_name} vs {match._player2.last_name} → Résultat : {result} (Couleurs: {match.color_player1}/{match.color_player2})")

        # Fin du tour (1 heure après le début)
        current_round.end_round(current_round._start_time + timedelta(hours=1))

    # Affichage des scores finaux
    print("\n Résultats finaux après 2 tours :")
    sorted_players = sorted(tournament._players, key=lambda p: p.score, reverse=True)
    for player in sorted_players:
        print(f"  {player.last_name} {player.first_name} (Score: {player.score})")

    # Sauvegarde des données (exemple de dictionnaire)
    tournament_data = tournament.to_dict()
    print(f"\n Données du tournoi (pour sauvegarde JSON) :")
    print(tournament_data)

    # Sauvegarde du tournoi dans un fichier
    file_path = tournament.save_to_json()
    print(f"\n Tournoi sauvegardé dans : {file_path}")

if __name__ == "__main__":
    main()
