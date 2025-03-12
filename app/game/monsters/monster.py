import random
import string

class Monster:
    def __init__(self,cps,monsterDifficulty,isHeal,isDoublePoints):
        # cps stands for characters per second
        # monsterDifficulty levels start from 1 to 4
        self.monsterDifficulty = monsterDifficulty
        self.ranString = ''.join(random.choice(string.ascii_letters) for _ in range(12))
        self.stringLength = len(self.ranString)
        self.timer = self.stringLength / (cps + (self.monsterDifficulty-1))
        self.points = monsterDifficulty *  100
        self.isHeal = isHeal
        self.isDoublePoints = isDoublePoints
        self.status = 'alive'
        self.avatar = None

    def terminateMonster(self):
        self.status = 'terminated'
