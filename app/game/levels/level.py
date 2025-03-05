from monsters import Monster
class Level:
    def __init__(self,difficulty,level):
        # each difficulty level has 10 different levels
        self.difficulty = difficulty
        self.level = level
        self.monsters = []

    def addMonster(self,monster):
        self.monsters.append(monster)

    def returnMonsters(self):
        return self.monsters
