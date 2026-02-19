from models.player import Player
class Match :
    def __init__(self, player1 : Player, player2 : Player):
        self._player1 = player1
        self._player2 = player2
        self._result=None
        #Tuple (score player1, score player2) so the result can't be changed after to write.
        # and here with _result you can't modify from outside only inside set_result (encapsulation)

    def set_result(self, score_player1:float, score_player2:float)->None:
        if (score_player1,score_player2) in [(1,0),(0.5,0.5),(0,1)]:
            self._result=(score_player1,score_player2)
            #update scores
            self._player1.update_score(score_player1)
            self._player2.update_score(score_player2)
            #add history
            self._player1.add_match(self._player2.national_id,score_player1)
            self._player2.add_match(self._player1.national_id,score_player2)
        else:
            raise ValueError("Invalid result. Use (1,0), (0.5,0.5) or (0,1)")

    def to_dict(self):
        return {
            "player1":self._player1.national_id,
            "player2":self._player2.national_id,
            "result":self._result
        }

