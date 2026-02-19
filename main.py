from models.player import Player
from models.tournament import Tournament
from models.round import Round
from models.match import Match
from datetime import datetime, timedelta
import random

def main():
    # creation 8 players
    players = [
        Player("AB12345", "NameA", "FirstnameA", "1990-01-01", "Club A"),
        Player("CD67890", "NameB", "FirstnameB", "1995-02-02", "Club B"),
        Player("EF12345", "NameC", "FirstnameC", "1992-03-03", "Club C"),
        Player("GH67890", "NameD", "FirstnameD", "1988-04-04", "Club D"),
        Player("IJ12345", "NameE", "FirstnameE", "1993-05-05", "Club A"),
        Player("KL67890", "NameF", "FirstnameF", "1989-06-06", "Club B"),
        Player("MN12345", "NameG", "FirstnameG", "1991-07-07", "Club C"),
        Player("OP67890", "NameH", "FirstnameH", "1994-08-08", "Club D"),
        Player("QR12345", "NameI", "FirstnameI", "1996-09-09", "Club A")
    ]

    # creation a tournament
    tournament = Tournament(
        name="Summer tournament",
        location="Paris",
        start_date=datetime(2026, 8, 1),
        end_date=datetime(2026, 8, 7),
        rounds=4
    )

    # Ajout des joueurs au tournoi
    for player in players:
        tournament.add_player(player)

    print("Tournoi create with 8 players :")
    for player in tournament._players:
        print(f"  - {player}")

    # generation of round
    for round_num in range(1, 3):
        print(f"\n--- Round {round_num} ---")
        current_round = tournament.generate_next_round()

        # Simulation result
        for match in current_round._matches:
            # random result
            result = random.choice([(1, 0), (0.5, 0.5), (0, 1)])
            match.set_result(*result)
            print(f"  Match : {match._player1.last_name} vs {match._player2.last_name} → Résultat : {result}")

        # end of round (1h after start)
        current_round.end_round(current_round._start_time + timedelta(hours=1))

    # final scores
    print("\n scores after 2 rounds:")
    sorted_players = sorted(tournament._players, key=lambda p: p.score, reverse=True)
    for player in sorted_players:
        print(f"  {player.last_name} {player.first_name} (Score: {player.score})")

    # Save the data
    tournament_data = tournament.to_dict()
    print(f"\n save the data : {tournament_data}")

if __name__ == "__main__":
    main()

