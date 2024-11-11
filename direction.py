from enum import Enum

class Direction(Enum):
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'
    
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))