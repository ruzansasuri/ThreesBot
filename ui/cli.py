
import os
from src.enums import GameState, Messages
from src.game import GameEngine
from src.logs import LEVELS, Logs


logs = Logs()


class GameRunner:
    _game_engine: GameEngine = None

    def __init__(self):
        """Initialize the GameEngine class."""
        self._game_engine = GameEngine()

    def start_game(self):
        """Start and run the game."""
        # Create new game
        if self._game_engine is None:
            logs.getError("Game engine not initialized")
            return       
        self._game_engine.setup_initial_state()
        print("🎮 Welcome to Threes!")
        print("Controls: l=Left, r=Right, u=Up, d=Down, q=Quit")
        print("-" * 40)
        
        # Main game loop
        while True:
            # Clear screen and show current state
            self.clear_screen()
            self._game_engine.display()
            game_info = self._game_engine.get_game_info()
            # Check if game is over
            if game_info and game_info['state'] != GameState.ONGOING:
                self.display_game_over()
                break
            
            # Get user input
            move = input("\nEnter move (l/r/u/d) or 'q' to quit: ").strip().lower()
            
            # Handle quit
            if move == 'q':
                print("Thanks for playing!")
                break
            
            # Parse and execute move
            direction = self._game_engine.parse_move_lrud(move)
            if direction:
                success = self._game_engine.make_move(direction)
                if not success:
                    logs.getInfo(f"Invalid move in the {direction} direction.")
                    input(f"❌ {Messages.BAD_MOVE} Press Enter...")
            else:
                logs.getWarning(f"Invalid input {move}")
                input(f"❓ {Messages.BAD_INPUT} Press Enter...")
    
    def display_game_info(self):
        """Display current score and game info."""
        info = self._game_engine.get_game_info()
        print(f"\nScore: {info['score']}")
        print(f"Moves: {info['moves']}")
        print(f"Next tile: {info['next_tile']}")

    def display_game_over(self):
        """Display game over message."""
        info = self._game_engine.get_game_info()
        print("\n" + "=" * 40)
        if info['state'] == 'WON':
            print("🎉 Congratulations! You won! 🎉")
        else:
            print("💀 GAME OVER! 💀")
        print(f"Final Score: {info['score']}")
        print(f"Total Moves: {info['moves']}")
        print("=" * 40)
    
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    logs.setLevel(LEVELS.DEBUG)
    game_runner = GameRunner()
    game_runner.clear_screen()
    game_runner.start_game()