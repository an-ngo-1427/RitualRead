class MainGame:
    def __init__(self,players,*playerGames):
        self.status = 'started'
        self.players = players
        self.playerGames = playerGames

    def isEnded(self):
        for playerGame in self.playerGames:
            if not playerGame.isEnded():
                self.status = 'pending'
                return False
        self.status = 'ended'
        return True
