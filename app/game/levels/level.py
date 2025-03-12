from monsters import Monster
import random
class Level:
    def __init__(self):
        # each levelDifficulty level has 4 different levels (level #1 -> level #4)
        # each level has +1 monster amount from previous level
        #
        self.levelDifficulty = 1
        self.monsters = []
        self.passed = False

    def advanceLevel(self):
        if(len(self.monsters) >= 4):
            self.levelDifficulty += 1
            self.monsters = []

        newMonster = Monster(cps=5, monsterDifficulty=self.levelDifficulty, isHeal = random.choice([True, False]), isDoublePoints= random.choice([True,False]))


        self.monsters.append(newMonster)

    def returnMonsters(self):
        return self.monsters
