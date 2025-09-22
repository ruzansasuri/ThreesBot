from src.logs import Logs


logs = Logs()

class Tile:
    """A class representing a tile in Threes!."""
    _value = None
    _accepted_basics = [0, 1, 2]

    def __init__(self, value):
        if value not in self._accepted_basics and (value < 3 or value % 3 != 0):
            return
        self._value = value

    def get_value(self):
        return self._value
    
    def canMerge(self, other):
        if self._value is None or other._value is None or self._value <= 0 or other._value <= 0 :
            return False
        if (self._value == 1 and other._value == 2) or (self._value == 2 and other._value == 1):
            return True
        if self._value < 3 or other._value < 3:
            return False
        if self._value >= 3 and other._value >=3 and self._value == other._value:
            return True
        return False
    
    def _merge(self, other):
        newTile = Tile(self._value + other._value)
        return newTile
    
    def merge(self, other):
        if not self.canMerge(other):
            logs.getError("Tiles cannot be merged")
            return None
        return self._merge(other)
    
    def is_empty(self):
        if self._value is None:
            logs.getWarning("Tile value is None")
            return True
        return self._value == 0