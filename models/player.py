class Player:
    def __init__(self, national_id:str, last_name:str, first_name:str,birth_date:str,elo:int,club:str):
        self.national_id = national_id
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.elo = elo
        self.club = club
        self.match_history = []

    def update_elo(self,new_elo:int):
        """Mets à jour le classement elo du joueur"""
        self.elo = new_elo

    def add_match(self,match_result:dict):
        """Ajoute un résultat de match à l'historique du joueur."""
        self.match_history.append(match_result)

    def to_dict(self):
        """Convertit l'objet Player en dictionnaire pour la sérialisation JSON."""
        return {
            "national_id": self.national_id,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birth_date": self.birth_date,
            "elo": self.elo,
            "club": self.club,
            "match_history": self.match_history
        }

    def __repr__(self):
        """Représentation textuelle de l'objet Player."""
        return f"Player(national_id={self.national_id}, last_name={self.last_name}, first_name={self.first_name}, elo={self.elo})"


