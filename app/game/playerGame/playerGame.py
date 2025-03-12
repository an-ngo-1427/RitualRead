from levels import Level
class PlayerGame:
    def __init__(self,player):
        self.level = Level()
        self.player = player
        self.playerHealth = 5
        self.scores = 0
        self.status = 'started'

    @property
    def scores(self):
        return self.scores
    @scores.setter
    def scores(self,points):
        self.scores = self.scores + points


    @property
    def playerHealth(self):
        return self.playerHealth
    @playerHealth.setter
    def playerHealth(self,value):
        self.playerHealth = self.playerHealth + value

    def isEnded(self):
        if self.playerHealth == 0:
            self.status = 'ended'
            return True
        self.status = 'pending'
        return False

    # creating monsters for the game based on level
