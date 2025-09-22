import random

from src.logs import Logs, LEVELS


logs = Logs()

class Deck:
    """A class representing a deck of tiles in Threes!."""
    _tiles = None

    def __init__(self):
        self._tiles = []
        for _ in range(4):
            self.add_tile(1)
        for _ in range(4):
            self.add_tile(2)
        for _ in range(4):
            self.add_tile(3)
        logs.getInfo(f"Deck initialized with tiles: {self._tiles}")
        logs.getInfo("Shuffling the deck...")
        self.shuffle()

    def shuffle(self):
        random.shuffle(self._tiles)

    def draw_tile(self):
        if self._tiles:
            return self._tiles.pop()
        else:
            logs.getWarning("No more tiles to draw.")
            return None
    
    def add_tile(self, tile):
        self._tiles.append(tile)

    def is_empty(self):
        return len(self._tiles) == 0
    
    def getTiles(self):
        if self._tiles is None:
            return "None"
        return self._tiles
    
def main():
    deck = Deck()
    logs.getInfo(f"Deck: {deck.getTiles()}")

if __name__ == "__main__":
    logs.setLevel(LEVELS.DEBUG)
    main()