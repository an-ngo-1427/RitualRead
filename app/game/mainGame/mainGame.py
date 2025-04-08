class MainGame:
    def __init__(self,playerGames):
        self.status = 'started'
        self.playerGames = playerGames

    def isEnded(self):
        for playerGame in self.playerGames:
            if not playerGame.isEnded():
                self.status = 'pending'
                return False
        self.status = 'ended'
        return True

    def getPlayers(self):
        players = []
        for playerGame in self.playerGames:
            players.append(playerGame.player)
        return [player.to_dict() for player in players]

    def gameStatus(self):
        return {
            'status':self.status,
            'player games':[playerGame.gameStatus() for playerGame in self.playerGames],
        }
