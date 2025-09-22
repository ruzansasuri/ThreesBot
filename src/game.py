import random
from typing import List, Tuple
from src.board import Board
from src.enums import Directions, GameState
from src.logs import Logs

logs = Logs()

class GameEngine:
    _board: Board = None
    _score = 0
    _moves = 0
    _state = 0
    _next_tile = None

    def __init__(self, length=4, width=4):
        """Initialize game with board and tile class, set up initial state."""
        self._board = Board(length, width)
            
    def make_move(self, direction: Directions):
        """
        Attempt to make a move in the given direction.

        Args:
            direction: Direction to move
            
        Returns:
            bool: True if move was successful, False otherwise
        """
        if self._state != GameState.ONGOING:
            return False

        # Check if move is valid
        if not self._is_valid_move(direction):
            return False

        # Perform the move
        moved = self._execute_move(direction)

        if moved:
            self.move_count += 1
            self._add_new_tile(direction)
            self._update_score()
            self._check_game_state()
            return True

        return False
    
    def setup_initial_state(self):
        """Place starting tiles on board (typically 9 tiles: four 1s, four 2s, one 3)."""
        if self._board is not None:
            self._board.set_start_tiles()
            self._state = GameState.ONGOING
            self._next_tile = self._generate_next_tile_chance()
        else:
            logs.getError("Board not initialized")

    def _generate_next_tile_chance(self):
        tile = random.choices(
            population=[1, 2, 3],
            weights=[0.245, 0.245, 0.01],
            k=1
        )[0]
        return tile
    
    def _get_next_tile_value_adaptive(self):
        """Adaptive tile generation based on board state."""
        # Count existing 1s and 2s
        ones, twos = self._board.count_ones_twos()
        
        # Adjust probabilities to maintain balance
        if ones > twos * 2:  # Too many 1s
            return 2
        elif twos > ones:    # Too many 2s  
            return 1
        else:
            # Default weighted random
            return self._generate_next_tile_chance()
    
    def _generate_next_tile(self):
        self._nextTile = self._get_next_tile_value_adaptive()
        return self._nextTile
    
    def _is_valid_move(self, direction):
        """Check if any tiles can move/merge in given direction."""
        self._board.can_move(direction)

    def _execute_move(self, direction: Directions) -> bool:
        """Execute the move and return if anything actually moved."""
        return self._board.move(direction)
    
    def _add_new_tile(self, direction):
        """Add new tile on opposite edge from move direction."""
        pass

    def _get_spawn_positions(self, direction: Directions) -> List[Tuple[int, int]]:
        """Get valid positions where new tiles can spawn based on move direction."""
        # New tiles spawn on the opposite edge of the move direction
        if direction == Directions.UP:
            return self._board.get_empty_positions_on_edge('bottom')
        elif direction == Directions.DOWN:
            return self._board.get_empty_positions_on_edge('top')
        elif direction == Directions.LEFT:
            return self._board.get_empty_positions_on_edge('right')
        elif direction == Directions.RIGHT:
            return self._board.get_empty_positions_on_edge('left')
    
    def _update_score(self):
        """Update the current score based on board state."""
        # Score is typically sum of all tiles >= 3
        total = 0
        for tile in self.board.get_all_tiles():
            if tile and tile.value >= 3:
                # Threes scoring: 3^(log2(value/3) + 1)
                if tile.value == 3:
                    total += 3
                else:
                    # For merged tiles: 6, 12, 24, etc.
                    power = (tile.value // 3).bit_length() - 1
                    total += 3 ** (power + 1)
        
        self.score = total
    
    def _check_game_state(self):
        """Check if the game is over or won."""
        if self.board.is_full() and not self._has_valid_moves():
            self.state = GameState.GAME_OVER
        
        # Optional: Check for win condition (e.g., reaching 6144 tile)
        max_tile = max((tile.value for tile in self.board.get_all_tiles() if tile), default=0)
        if max_tile >= 6144:  # Adjust this threshold as needed
            self.state = GameState.WON

    def _has_valid_moves(self) -> bool:
        """Check if any valid moves remain."""
        for direction in Directions:
            if self._is_valid_move(direction):
                return True
        return False
    
    def get_game_info(self):
        """Return dict with current score, moves, state, next tile, board."""
        if self._board is None:
            logs.getError("Board not initialized")
            return None

        return {
            "score": self._score,
            "moves": self._moves,
            "state": self._state,
            "next_tile": self._next_tile
        }
    
    def reset_game(self):
        """Clear board and reset state for new game."""
        self._board.reset()
        self._score = 0
        self._moves = 0
        self._state = GameState.ONGOING
        self._next_tile = None
        self.setup_initial_state()

    def display(self):
        self._board.print_board()

    def parse_move_lrud(self, move):
        """Convert user input to Direction enum."""
        move_map = {
            'l': Directions.LEFT,
            'r': Directions.RIGHT, 
            'u': Directions.UP,
            'd': Directions.DOWN
        }
        return move_map.get(move)

def main():
    game = GameState()
    game.printCurrentState()
    logs.getInfo(game.generate_next_tile())
    # game.start()

if __name__ == "__main__":
    main()