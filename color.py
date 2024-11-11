from enum import Enum

class Color(Enum):
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'
    PURPLE = 'purple'
    ORANGE = 'orange'
    
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
    
    @classmethod
    def getColor(cls, color):
        if color == cls.RED.value:
            return {
                'r': 255,
                'g': 0,
                'b': 0
            }
        if color == cls.GREEN.value:
            return {
                'r': 0,
                'g': 255,
                'b': 0
            }
        if color == cls.BLUE.value:
            return {
                'r': 0,
                'g': 0,
                'b': 255
            }
        if color == cls.PURPLE.value:
            return {
                'r': 255,
                'g': 0,
                'b': 255
            }
        if color == cls.ORANGE.value:
            return {
                'r': 255,
                'g': 125,
                'b': 125
            }
        