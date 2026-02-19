from datetime import date  # for date without time
class Player:
    """Represents a chess player with their information and match history""" #Docstring (help(Player))
    #Encapsulation: Attributes are marked as 'private' with an underscore (_) to indicate they should not be accessed directly from outside
    def __init__(self, national_id:str, last_name:str, first_name:str,birth_date:str,club:str):
        """Initializes a player with their private attributes"""
        self._national_id = national_id #unique national id
        self._last_name = last_name
        self._first_name = first_name
        self._birth_date = self._validate_birth_date(birth_date) #immediatly validation
        self._score = 0
        self._club = club
        self._match_history = [] #match history (list of dictionary)

    def _validate_birth_date(self, birth_date_input) -> date: #private method
        """Validates the birthdate (format YYYY-MM-DD)"""
        if isinstance(birth_date_input, date):
            return birth_date_input
        elif isinstance(birth_date_input, str):
            try:
                # Replaces possible separators with '-'
                normalized_date = birth_date_input.replace('/', '-').replace('.', '-')
                parts=normalized_date.split('-')
                if len(parts) != 3:
                    raise ValueError('Invalid birth date')

                #determines the format
                if len(parts[0])==4:
                    year,month,day = map(int,parts) #map converts each element of the list to an integer (`int`)
                else:
                    day,month,year = map(int,parts)

                return date(year,month,day)
            except (ValueError, AttributeError,IndexError):
                raise ValueError('Invalid birth date : use YYYY-MM-DD or DD/MM/YYYY')
        else:
            raise ValueError('birthdate must be date or string')

    @property
    def national_id(self) -> str:
        """Returns the national id of the player (read only)- str"""
        return self._national_id

    @property
    def last_name(self) -> str:
        """Returns the last name of the player (read only) - str"""
        return self._last_name

    @property
    def first_name(self) -> str:
        """Returns the first name of the player (read only)"""
        return self._first_name

    @property
    def birth_date(self) -> date:
        """Returns the birth date of the player (read only)"""
        return self._birth_date

    @property
    def score(self) -> float:
        """Returns the elo value of the player (read only)"""
        return self._score

    def update_score(self,points:float) -> None:
        """Updates the player's total score (public method)"""
        #Abstraction :  hide the calcul of points.
        if points in [0,0.5,1]: # possibility of points 0 defeat, 0.5 draw et 1 victory
            self._score += points #No return, so return None by default

    def add_match(self,opponent_id:str,result:float) -> None:
        """Adds a match result to the player's match_history"""
        self._match_history.append({"opponent_id":opponent_id, "result":result})

    def to_dict(self):
        """Convert the player's match_history to a dictionary"""
        return {
            "national_id": self._national_id,
            "last_name": self._last_name,
            "first_name": self._first_name,
            "birth_date": self._birth_date,
            "score": self._score,
            "club": self._club,
            "match_history": self._match_history
        }

    def __repr__(self):
        """Représentation textuelle de l'objet Player."""
        return f"Player(national_id={self._national_id}, last_name={self._last_name}, first_name={self._first_name}, score={self._score})"


