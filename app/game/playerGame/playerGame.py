class PlayerGame:
    def __init__(self,player,level):
        self.level = level
        self.player = player
        self.playerHealth = 5
        self.scores = 0

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
