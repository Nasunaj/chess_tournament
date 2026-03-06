# Chess tournament

```mermaid
classDiagram
    %% Classes
    class Player {
        +str national_id
        +str last_name
        +str first_name
        +date birth_date
        +int elo
        +str club
        +list match_history
        +to_dict() dict
    }

    class Tournament {
        +str name
        +str location
        +datetime start_date
        +datetime end_date
        +int number_of_rounds
        +list~Player~ players
        +list~Round~ rounds
        +add_player(Player)
        +start_round()
        +to_dict() dict
    }

    class Round {
        +str name
        +list~Match~ matches
        +datetime start_time
        +datetime end_time
        +add_match(Match)
        +to_dict() dict
    }

    class Match {
        +Player player1
        +Player player2
        +str result
        +set_result(str)
        +to_dict() dict
    }

    %% Relations
    Tournament "1" --> "0..8" Round : contains
    Tournament "1" --o "2..*" Player : registers
    Round "1" --> "1..*" Match : organizes
    Match "1" -- "2" Player : matches


```

**Relation**
- A standard chess tournament has 4 to 8 rounds. If the tournament is deleted, its rounds are also deleted.
- At least 2 players are registered in a tournament. Players exist independently of the tournament. A player can participate in multiple tournaments.
- A Round organizes 1 or more Matches. If the Round is deleted, its Matches are also deleted.
- A Match opposes exactly 2 Players. Players exist independently of the Match.

| symbol | type of relation   | explication                                                                    |
|--------|--------------------|--------------------------------------------------------------------------------|
| -->    | Composition        | Strong link: the "parent" object owns the "child" objects.                     |
| --0    | Aggregation        | Weak link: the "parent" object uses the "child" objects but does not own them. |
| --     | Simple association | Logical link whitout ownership                                                 |
