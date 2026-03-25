# Chess tournament management application (Chess tournament)

## Table of contents
<!-- TOC -->
  * [Table of contents](#table-of-contents)
  * [Description](#description)
  * [Installation](#installation)
  * [Running the application](#running-the-application)
  * [Using the application](#using-the-application)
  * [Project structure](#project-structure)
  * [Generate a flake8 Report](#generate-a-flake8-report)
  * [Deliverables](#deliverables-)
<!-- TOC -->
## Description
This application allow you to manage chess tournaments in console mode. It includes :
- Creation and management of tournaments
- Adding and managing players
- Automatic generation of rounds and matches
- Input of results and score calculation
- Report generation (list of tournaments, match history, rankings)

## Installation
1) Clone the repository : https://github.com/Nasunaj/chess_tournament.git  
2) Create a virtual environment
3) Install the dependencies : ```pip install -r requirements.txt```  

## Running the application
1) Launch the application : ```python main.py```
2) Main menu<br>
The application offers a main menu with the following option :
```
---------Menu principal--------
1. Gérer les tournois
2. Gérer les joueurs
3. Générer des rapports
4. Quitter
Choisi une option entre 1 et 4: 
```
## Using the application
1) Manage tournaments (```1. Gérer les tournois```)
   - Create a Tournament (```1. Créer un tournoi```) : Enter the details (name, location, date, number of rounds).<br>
     *Note : each created tournament is saved in ```data/tournaments/``` as the json file. The filename corresponds to the tournaments ID (the first 3 letters of the tournaments name, followed by the 3 letters of the location and the date without separators. Example :```tespar20260325.json``` name : ```Test```, location: ```Paris```, start_date : ```2026-03-25```)*<br>
   - Add players ( ```4. Ajouter un joueur à un tournoi```) : Select a tournament and add players from the list of registered players (in data/players/)<br>
   - Generate rounds and enter the results : 
     1) Generate the first round (```5. Générer le 1er tour```) 
     2) Enter the results (```7. Saisir les resultats d'un match```) : after each match, input the results (win, draw or loss)
     3) Generate the others rounds (```6. Générer le tour suivant```)
     4) Enter for each round all the results before generate the following round.<br>
   - Others possibilities :
     - View existing tournaments (```2. Voir les tournois existants```<br>
     - View tournament details (```3. Voir les détails d'un tournoi```)<br>
     - View rankings (```8. Voir le classement```)<br><br>
   
2) Manage players (```2. Gérer les joueurs```)
   - Create a player (```1. Créer un joueur```) : register a new player with their details (national ID, first name, last name, birthdate : format ```YYYY-MM-DD```, club), saved in ```data/players/``` as the json file. The filename corresponds player's last name and his national ID.
```json
{
    "national_id": "AA12345",
    "last_name": "NomA",
    "first_name": "prenomA",
    "birth_date": "2015-11-14",
    "club": "A"
}
```
   - View player list (```2. Voir la liste des joueurs```) : display all registered players
   - View player history matches (```3. Voir l'historique d'un joueur```) : display all matches of the player selected.<br><br>
3) Generate reports (```3. Générer des rapports```)
   - Tournament list (```1. Liste de tous les tournois```) :  display a summary of all created tournaments.
   - Tournament history (```2. Historique d'un tournoi```) : select a tournament to view its rounds, matches and results.

## Project structure
```
.
├── controllers                                    # Controllers (Business Logic)                                
│   ├── menu_controller.py
│   ├── player_controller.py
│   ├── report_controller.py
│   └── tournament_controller.py
├── data                                           # Data (JSON files with examples)
│   ├── players
│   │   ├── NomA_AA12345.json
│   │   ├── NomB_BB12345.json
│   │   ├── NomC_CC23456.json
│   │   └── NomD_DD45789.json
│   └── tournaments
│       └── demtho20260322.json                
├── flake8_report                                   # Flake8 Report (generated) 
│   ├── back.svg
│   ├── file.svg
│   ├── index.html
│   └── styles.css
├── models                                          # Models (business classes)                                     
│   ├── tests
│   │   ├── test_match.py
│   │   ├── test_player.py
│   │   ├── test_round.py
│   │   └── test_tournament.py
│   ├── __init__.py
│   ├── match.py
│   ├── player.py
│   ├── round.py
│   └── tournament.py
├── views                                            # User interface
│   ├── menu_view.py
│   ├── player_view.py
│   ├── report_view.py
│   └── tournament_view.py
├── main.py                                          # Application entry point
├── README.md                                        # This file (README.md)
├── requirements.txt                                 
```
## Generate a flake8 Report
1) Install flake8 and flake8-html : ```pip install flake8 flake8-html```
2) Configure flake8 in file ```.flake8```
```
[flake8]
exclude =
    .git,
    __pycache__,
    .venv,
    cours/,
    Spécification+technique_Développez+un+programme+logiciel+en+Python.pdf,
    users_stories,
    data/,
    models/__init__.py
include =
    models/,
    views/,
    controllers/,
    main.py
ignore =
    E501,              # Ignore long lines
    W5                 # Ignore warnings about binary operators
```
3) Generate the html report ```flake8 --format=html --htmldir=flake8_report```
   - A flake8_report folder will be created at the root of the project.
   - Open ```flake8_report/index.html``` in your web browser to view the report.
   
## Deliverables 
- Source code: available in this GitHub repository.
- Flake8 report: In flake8_report/index.html (no errors). 
- Instructions: See this README.md.





