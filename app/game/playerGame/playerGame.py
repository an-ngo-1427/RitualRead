from app.game.levels import Level
class PlayerGame:
    def __init__(self,player):
        self.level = Level()
        self.player = player
        self._playerHealth = 5
        self._scores = 0
        self.status = 'started'

    @property
    def scores(self):
        return self._scores
    @scores.setter
    def scores(self,points):
        self._scores = self._scores + points


    @property
    def playerHealth(self):
        return self._playerHealth
    @playerHealth.setter
    def playerHealth(self,value):
        self._playerHealth = self._playerHealth + value

    def gameStatus(self):
        return {
            'player':self.player.to_dict(),
            'scores':self.scores,
            'health':self.playerHealth,
            'monsters':[monster.to_dict() for monster in self.level.monsters],
        }

    def isEnded(self):
        if self.playerHealth == 0:
            self.status = 'ended'
            return True
        self.status = 'pending'
        return False

    # creating monsters for the game based on level
