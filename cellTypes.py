from enum import Enum

class Type(Enum):
    WALL = 'wall'
    EMPTY = 'empty'
    PLAYER = 'player'
    GOAL = 'goal'
    
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

