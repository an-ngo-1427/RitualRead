import random
import string

class Monster:
    def __init__(self,cps,difficulty,isHeal,isDoublePoints):
        self.difficulty = difficulty
        self.ranString = ''.join(random.choice(string.ascii_letters) for _ in range(12))
        self.stringLength = len(self.ranString)
        self.timer = self.stringLength / (cps + (self.difficulty-1))
        self.points = difficulty *  100
        self.isHeal = isHeal
        self.isDoublePoints = isDoublePoints
        self.avatar = None
