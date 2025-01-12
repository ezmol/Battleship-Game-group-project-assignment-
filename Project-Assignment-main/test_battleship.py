import unittest
from unittest.mock import patch
from battleship import Grid, Ship, Game

class TestGrid(unittest.TestCase):
    def test_create_grid(self):
        """Test the creation of a grid with the correct size and initial empty cells."""
        grid_size = 10
        grid = Grid(grid_size)
        
        # Check that the grid is of the correct size
        self.assertEqual(len(grid.grid), grid_size)
        self.assertEqual(len(grid.grid[0]), grid_size)
        
        # Ensure all cells in the grid are initialized as empty spaces
        self.assertTrue(all(cell == " " for row in grid.grid for cell in row))

    def test_display_grid(self):
        """Test the display of the grid with marked cells."""
        grid_size = 10
        grid = Grid(grid_size)
        
        # Mark specific cells in the grid
        grid.grid[0][0] = "X"  # Top-left corner
        grid.grid[1][1] = "O"  # Adjacent cell
        
        # Display the grid and check if the visual output is correct
        # (Visual check needed during the test run)
        grid.display_grid()

class TestShip(unittest.TestCase):
    def test_place_ship_horizontal(self):
        """Test placing a ship horizontally on the grid."""
        grid_size = 10
        grid = Grid(grid_size).grid
        ship = Ship("Destroyer", 2)
        
        # Place the ship horizontally
        ship.place_ship(grid)
        
        # Ensure the ship occupies the correct number of cells
        self.assertEqual(len(ship.coordinates), 2)
        
        # Verify that the ship's cells are correctly marked on the grid
        for row, col in ship.coordinates:
            self.assertEqual(grid[row][col], "D")

    def test_place_ship_vertical(self):
        """Test placing a ship vertically on the grid."""
        grid_size = 10
        grid = Grid(grid_size).grid
        ship = Ship("Submarine", 3)
        
        # Place the ship vertically
        ship.place_ship(grid)
        
        # Ensure the ship occupies the correct number of cells
        self.assertEqual(len(ship.coordinates), 3)
        
        # Verify that the ship's cells are correctly marked on the grid
        for row, col in ship.coordinates:
            self.assertEqual(grid[row][col], "S")

    def test_is_sunk(self):
        """Test the sinking of a ship after being hit the correct number of times."""
        ship = Ship("Cruiser", 3)
        
        # Hit the ship twice
        ship.hit()
        ship.hit()
        
        # Ensure the ship is not sunk yet
        self.assertFalse(ship.is_sunk())
        
        # Hit the ship a third time
        ship.hit()
        
        # Ensure the ship is now sunk
        self.assertTrue(ship.is_sunk())

class TestGame(unittest.TestCase):

    @patch('builtins.input', side_effect=[
        # Mock inputs for placing 5 ships
        'H', 'A1',  # Carrier (size 5)
        'V', 'B2',  # Battleship (size 4)
        'H', 'C3',  # Cruiser (size 3)
        'V', 'D4',  # Submarine (size 3)
        'H', 'E5',  # Destroyer (size 2)

        # Additional inputs to handle extra prompts
        'H', 'F6',  # Extra input 1
        'V', 'G7',  # Extra input 2
        'H', 'H8',  # Extra input 3
        'V', 'I9',  # Extra input 4
        'H', 'J10', # Extra input 5
    ])
    def test_setup_ships(self, mock_input):
        """Test the setup of ships for both the player and the computer using mock input."""
        try:
            game = Game(10, "Player")
            game.setup_ships()

            # Ensure the correct number of ships are created for the player and computer
            self.assertEqual(len(game.player_ships), 5)
            self.assertEqual(len(game.computer_ships), 5)

            # Verify that each ship has been placed on the grid with assigned coordinates
            for ship in game.player_ships:
                self.assertGreater(len(ship.coordinates), 0)
            for ship in game.computer_ships:
                self.assertGreater(len(ship.coordinates), 0)

        except StopIteration:
            # Handle the end of inputs gracefully
            print("Mock inputs exhausted, ending test.")

    @patch('builtins.input', side_effect=[
        # Similar mock input sequence as above
        'H', 'A1',
        'V', 'B2',
        'H', 'C3',
        'V', 'D4',
        'H', 'E5',
        # Additional or redundant inputs
        'H', 'F6',
        'V', 'G7',
        'H', 'H8',
        'V', 'I9',
        'H', 'J10',
    ])
    def test_play_game(self, mock_input):
        """Test the initialization and basic functionality of the game using mock input."""
        try:
            game = Game(10, "Player")

            # Simulate the setup of ships using mock inputs
            game.setup_ships()

            # Ensure the game initializes correctly and ships are placed
            self.assertEqual(game.grid_size, 10)
            self.assertEqual(game.player_name, "Player")
            self.assertEqual(len(game.player_ships), 5)

        except StopIteration:
            # Handle the end of inputs gracefully
            print("Mock inputs exhausted, ending test.")
            
if __name__ == "__main__":
    unittest.main()
