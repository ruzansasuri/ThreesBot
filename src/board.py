

import random
from typing import List, Tuple
from src.enums import GameState
from src.enums import Directions
from src.logs import LEVELS, Logs
from src.tile import Tile


logs = Logs()

class Board:
    _board = None
    _numTiles = 0
    _lenght = None
    _width = None

    def __init__(self, length=4, width=4) -> None:
        self._board = [[Tile(0) for _ in range(width)] for _ in range(length)] # Initialize an empty board 
        self._numTiles = 0
        self.length = length
        self.width = width

    def reset(self) -> None:
        self.force_state([[0 for _ in range(self.width)] for _ in range(self.length)])

    def force_state(self, state) -> bool:
        if len(state) != self.length or any(len(row) != self.width for row in state):
            return False
        self._board = state
        self._numTiles = sum(1 for row in state for cell in row if cell != 0)
        return True
    
    def set_start_tiles(self, num_each_tiles=4) -> bool:
        tiles = [1] * num_each_tiles + [2] * num_each_tiles + [3] * num_each_tiles
        for tile in tiles:
            random_pos = (random.randint(0, self.length - 1), random.randint(0, self.width - 1))
            while self.is_occupied(*random_pos):
                random_pos = (random.randint(0, self.length - 1), random.randint(0, self.width - 1))
            self.set_tile(random_pos[0], random_pos[1], Tile(tile))

        self._numTiles = len(tiles)
        return True
    
    def get_tile(self, row, col) -> Tile:
        if not self._is_valid_position(row, col):
            return None
        return self._board[row][col]
    
    def is_occupied(self, row, col) -> bool:
        if self._is_valid_position(row, col) is False:
            logs.getError(f"is_occupied: Coordinates ({row}, {col}) out of bounds")
            return False
        return self._board[row][col] is not None and not self._board[row][col].is_empty()
    
    def set_tile(self, row, col, tile: Tile = None) -> bool:
        if not self._is_valid_position(row, col):
            logs.getError(f"set_tile: Coordinates ({row}, {col}) out of bounds")
            return False
        if self.is_occupied(row, col):
            logs.getWarning(f"set_tile: Position ({row}, {col}) is already occupied")
            return False
        self._board[row][col] = tile
        self._numTiles += 1
        return True
    
    def count_ones_twos(self):
        ones = sum(1 for row in self._board for tile in row if tile.get_value() == 1)
        twos = sum(1 for row in self._board for tile in row if tile.get_value() == 2)
        return ones, twos
    
    def can_move(self, direction: Directions) -> bool:
        # Check if any move is possible in the given direction
        for row in range(len(self._board)):
            for col in range(len(self._board[row])):
                tile = self.get_tile(row, col)
                
                # Skip empty cells
                if not tile or tile.is_empty():
                    continue
                
                # Check if this tile can move in the given direction
                if self._can_tile_move(row, col, direction):
                    return True
        
        return False
    
    def _can_tile_move(self, row, col, direction: Directions):
        """
        Check if a specific tile can move in the given direction.
        
        Args:
            row, col: Position of the tile
            direction: Direction to check
            
        Returns:
            bool: True if tile can move
        """
        current_tile = self.get_tile(row, col)
        
        # Get the next position in the direction
        next_row, next_col = row + direction.value[0], col + direction.value[1]  
        
        # If next position is out of bounds, can't move
        if not self._is_valid_position(next_row, next_col):
            return False
        
        next_tile = self.get_tile(next_row, next_col)
        
        # Can move if next position is empty
        if next_tile.is_empty():
            return True
        
        # Can move if tiles can merge (Threes rules)
        return self._can_tiles_merge(current_tile, next_tile)
    
    def _can_tiles_merge(self, tile1: Tile, tile2: Tile) -> bool:
        if not tile1 or not tile2:
            return False
        return tile1.canMerge(tile2)

    def _is_valid_position(self, row, col):
        return 0 <= row < self.length and 0 <= col < self.width
    
    def merge_tiles(self, tile1: Tile, tile2: Tile) -> Tuple[Tile, Tile]:
        if not tile1 or not tile2:
            return None
        return Tile(0), tile1.merge(tile2)
        
    def get_empty_positions_on_edge(self, edge: str) -> List[Tuple[int, int]]:
        positions = []
        if edge == 'top':
            row = 0
            for col in range(self.width):
                if not self.is_occupied(row, col):
                    positions.append((row, col))
        elif edge == 'bottom':
            row = self.length - 1
            for col in range(self.width):
                if not self.is_occupied(row, col):
                    positions.append((row, col))
        elif edge == 'left':
            col = 0
            for row in range(self.length):
                if not self.is_occupied(row, col):
                    positions.append((row, col))
        elif edge == 'right':
            col = self.width - 1
            for row in range(self.length):
                if not self.is_occupied(row, col):
                    positions.append((row, col))
        return positions
        
    def move(self, direction: Directions) -> bool:
        """
        Move and merge tiles in the given direction.
        
        Args:
            direction: Direction to move (DIRECTIONS enum)
        Returns:
            bool: True if any tiles moved or merged
        """
        moved = False
        range_start, range_end, step = (0, self.length, 1) if direction in (Directions.UP, Directions.LEFT) else (self.length - 1, -1, -1)
        
        for i in range(range_start, range_end, step):
            for j in range(range_start, range_end, step):
                row, col = (i, j) if direction in (Directions.UP, Directions.DOWN) else (j, i)
                tile = self.get_tile(row, col)
                
                if not tile or tile.is_empty():
                    continue
                
                next_row, next_col = row + direction.value[0], col + direction.value[1]
                
                while self._is_valid_position(next_row, next_col):
                    next_tile = self.get_tile(next_row, next_col)
                    
                    if next_tile.is_empty():
                        # Move to empty space
                        self._board[next_row][next_col] = tile
                        self._board[row][col] = Tile(0)
                        row, col = next_row, next_col
                        next_row += direction.value[0]
                        next_col += direction.value[1]
                        moved = True
                    elif self._can_tiles_merge(tile, next_tile):
                        # Merge tiles
                        new_tile = tile.merge(next_tile)
                        self._board[next_row][next_col] = new_tile
                        self._board[row][col] = Tile(0)
                        moved = True
                        break
                    else:
                        break
        
        if moved:
            logs.getInfo(f"Board changed after moving {direction.name}")
        else:
            logs.getInfo(f"No tiles moved when moving {direction.name}")
        
        return moved

    def get_all_tiles(self) -> List[Tile]:
        return [tile for row in self._board for tile in row if tile and not tile.is_empty()]

    def is_full(self) -> bool:
        return self._numTiles >= self.length * self.width

    def print_board(self, score=None, moves=None) -> None:
        """
        Print a Threes game board with dynamic column width to handle large numbers.
        
        Args:
            board: 4x4 list of lists representing the game board
            score: Optional score to display
            moves: Optional move count to display
        """
        # Find the maximum number of digits needed
        max_value = max(
            tile.get_value() 
            for row in self._board 
            for tile in row
        )   
             
        if max_value == 0:
            cell_width = 3  # Minimum width for empty cells
        else:
            cell_width = max(3, len(str(max_value)))  # At least 3 characters wide
        
        # Print header info if provided
        if score is not None or moves is not None:
            header_parts = []
            if score is not None:
                header_parts.append(f"Score: {score}")
            if moves is not None:
                header_parts.append(f"Moves: {moves}")
            print(" | ".join(header_parts))
        
        # Calculate total board width for borders
        inner_width = cell_width * 4 + 3  # 4 cells + 3 separators
        border = "+" + "=" * inner_width + "+"
        print(border)
        
        # Print each row
        for row in self._board:
            print("|", end="")
            for i, tile in enumerate(row):
                if tile == 0:
                    # Empty cell
                    content = " " * cell_width
                else:
                    # Center the number in the cell
                    content = str(tile.get_value()).center(cell_width)
                
                print(content, end="")
                
                # Add separator except for last column
                if i < 3:
                    print("|", end="")
            
            print("|")  # End of row
        
        print(border)
        print()  # Extra line for spacing


############################Tests############################
def forced_states_test():
    print(f"====== FORCED STATES TEST ======")
    states = GameState
    for state in states[:10]:
        print(f"=== {state['name']} ===")
        board = Board()
        board.force_state(state['board'])
        board.print_board(score=12345, moves=67)

def random_start_test():
    print(f"====== RANDOM START TEST ======")
    board = Board()
    board.set_start_tiles()
    print('Game Ready!')
    board.print_board(score=0, moves=0)

def main():
    logs.setLevel(LEVELS.DEBUG)
    # forced_states_test()
    random_start_test()

if __name__ == "__main__":
    main()