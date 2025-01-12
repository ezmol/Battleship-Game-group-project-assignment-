import random
import mysql.connector
from mysql.connector import Error

# Welcome Message
def display_welcome_message():
    print(r"""
                ___________________________________________________________________
                ||     *                            *                    ((   *  ||
                ||        *                 *                *            ~      ||
                ||                ___.                          *          *     ||
                ||       *    ___.\__|.__.           *                           ||
                ||            \__|. .| \_|.                                      ||
                ||            . X|___|___| .                         *           ||
                ||          .__/_||____ ||__.            *                /\     ||
                ||  *     .  |/|____ |_\|_ |/ _                          /  \    ||
                ||        \ _/ |_X__\|_  |\||~,~{                       /    \   ||
                ||         \/\ |/|    |_ |/:|`X'{                   _ _/      \__||
                ||          \ \/ |___ |_\|_.|~~~                   /    . .. . ..||
                ||         _|X/\ |___\|_ :| |_.                  - .......... . .||
                ||         | __\_:____ |  ||o-|            ___/........ . . .. ..||
                ||         |/_-|-_|__ \|_ |/--|       ____/  . . .. . . .. ... . ||
                || ........:| -|- o-o\_:_\|o-/:....../...........................||
                || ._._._._._\=\====o==o==o=/:.._._._._._._._._._._._._._._._._._||
                || _._._._._._\_\ ._._._._.:._._._._._._._._._._._._._.P_._._._._||
                || ._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._||
                ||---------------------------------------------------------------||
                                                                -Manoj Jain

        """)
    print("Welcome to the Battleship game!")
    print("----------------------------------------------------\n")

# Database Handling
class DatabaseHandler:
    def __init__(self, host, user, password, database):
        """Initializes the DatabaseHandler with connection details."""
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def create_connection(self):
        """Establishes a connection to the MySQL database."""
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None

    def create_results_table(self):
        """Creates the game_results table if it doesn't exist."""
        connection = self.create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS game_results (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    player_name VARCHAR(255),
                    result VARCHAR(50),
                    moves INT
                )
                """)
                connection.close()
            except Error as e:
                print(f"Error creating table: {e}")
        else:
            print("Failed to create table due to database connection issues.")

    def insert_game_result(self, player_name, result, moves):
        """Inserts a new game result into the game_results table."""
        connection = self.create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO game_results (player_name, result, moves) VALUES (%s, %s, %s)",
                               (player_name, result, moves))
                connection.commit()
                connection.close()
            except Error as e:
                print(f"Error inserting game result: {e}")
        else:
            print("Failed to insert game result due to database connection issues.")

# Grid Handling and Game Logic
class Grid:
    def __init__(self, size):
        """Initializes the grid with a specified size."""
        self.size = size
        self.grid = self.create_grid()

    def create_grid(self):
        """Creates a 2D grid initialized with spaces."""
        return [[" " for _ in range(self.size)] for _ in range(self.size)]

    def display_grid(self):
        """Displays the grid with headers and row labels."""
        header = self.create_header()  # Create header for the grid columns
        row_label = self.create_row_label()  # Create row labels (A, B, C, etc.)

        print(header)  # Print the header
        print(f" {'+' + '-'*(self.size*6 - 1) + '+'}")  # Print the top border of the grid

        for i, row in enumerate(self.grid):
            # Create row display with row label and grid cells
            row_display = f"{row_label[i]}" + "".join(f"|{cell:5}" for cell in row) + "|"
            print(row_display)  # Print the row with the grid cells
            print(f" {'+' + '-'*(self.size*6 - 1) + '+'}")  # Print the row separator

    def create_header(self):
        """Generates a header for the grid."""
        return " ".join(f"{i+1:5}" for i in range(self.size))

    def create_row_label(self):
        """Creates row labels (A, B, C, ...) for the grid."""
        letters = "ABCDEFGHIJ"
        return letters[:self.size]

# Clas Ship
class Ship:
    def __init__(self, ship_type, size):
        """Initializes a ship with type, size, and default values for hits and orientation."""
        self.ship_type = ship_type
        self.size = size
        self.hits = 0  # Track the number of hits the ship has taken
        self.orientation = None  # Track the orientation (horizontal or vertical) of the ship
        self.coordinates = []  # Store the coordinates of the ship's placement on the grid

    def place_ship(self, grid):
        """Places the ship on the grid."""
        ship_placed = False
        while not ship_placed:
            # Randomly choose the orientation of the ship
            orientation = random.choice(['horizontal', 'vertical'])
            self.orientation = orientation

            if orientation == 'horizontal':
                # Place the ship horizontally if there's enough space
                row = random.randint(0, len(grid) - 1)
                col = random.randint(0, len(grid) - self.size)
                if all(grid[row][col + i] == " " for i in range(self.size)):
                    for i in range(self.size):
                        grid[row][col + i] = self.ship_type[0]
                        self.coordinates.append((row, col + i))
                    ship_placed = True
            else:
                # Place the ship vertically if there's enough space
                row = random.randint(0, len(grid) - self.size)
                col = random.randint(0, len(grid) - 1)
                if all(grid[row + i][col] == " " for i in range(self.size)):
                    for i in range(self.size):
                        grid[row + i][col] = self.ship_type[0]
                        self.coordinates.append((row + i, col))
                    ship_placed = True
        return grid

    def is_sunk(self):
        """Checks if the ship is sunk (i.e., all parts have been hit)."""
        return self.hits == self.size

    def hit(self):
        """Registers a hit on the ship."""
        self.hits += 1

# Class Game
class Game:
    def __init__(self, grid_size, player_name):
        """Initializes the game with the grid size and player name."""
        self.grid_size = grid_size
        self.player_name = player_name
        self.player_grid = Grid(grid_size)  # Create the player's grid
        self.computer_grid = Grid(grid_size)  # Create the computer's grid
        self.player_ships = []  # Store the player's ships
        self.computer_ships = []  # Store the computer's ships
        self.player_moves = 0  # Track the number of moves made by the player

    def place_ship_manually(self, grid, ship):
            """Allows the player to manually place a ship on the grid and updates the display after each placement."""
            ship_placed = False
            while not ship_placed:
                try:
                    # Ask for the ship's orientation
                    orientation = input(f"Enter orientation for your {ship.ship_type} (size {ship.size}) "
                                        "(H for horizontal, V for vertical): ").strip().upper()
                    if orientation not in ['H', 'V']:
                        print("Invalid orientation. Please enter 'H' or 'V'.")
                        continue

                    # Ask for the starting coordinates
                    coordinates = input(f"Enter the starting coordinates for your {ship.ship_type} (e.g., A5): ").upper().strip()
                    
                    # Validate the coordinate format
                    if len(coordinates) < 2 or not coordinates[0].isalpha() or not coordinates[1:].isdigit():
                        print("Invalid coordinates. Please enter a letter followed by a number (e.g., A5).")
                        continue
                    
                    row = "ABCDEFGHIJ".index(coordinates[0])
                    col = int(coordinates[1:]) - 1

                    # Validate the ship placement
                    if orientation == 'H':
                        if col + ship.size > len(grid[0]) or any(grid[row][col + i] != " " for i in range(ship.size)):
                            print("Invalid placement. The ship either goes out of bounds or overlaps another ship.")
                            continue
                        for i in range(ship.size):
                            grid[row][col + i] = ship.ship_type[0]
                            ship.coordinates.append((row, col + i))
                    else:
                        if row + ship.size > len(grid) or any(grid[row + i][col] != " " for i in range(ship.size)):
                            print("Invalid placement. The ship either goes out of bounds or overlaps another ship.")
                            continue
                        for i in range(ship.size):
                            grid[row + i][col] = ship.ship_type[0]
                            ship.coordinates.append((row + i, col))

                    ship_placed = True

                    # Display the grid after each successful placement
                    self.display_grids()

                except (ValueError, IndexError):
                    print("Invalid input. Please try again.")

    def setup_ships(self):
        """Sets up ships for both the player and the computer."""
        # Define ship types and sizes
        ship_definitions = [("Carrier", 5), ("Battleship", 4), ("Cruiser", 3), ("Submarine", 3), ("Destroyer", 2)]

        # Display the empty grids before ship placement
        print("Your grid and the computer's grid (hidden):")
        self.display_grids()
        
        # Manually place player's ships
        self.player_ships = [Ship(name, size) for name, size in ship_definitions]
        print("Place your ships on the grid.")
        for ship in self.player_ships:
            self.place_ship_manually(self.player_grid.grid, ship)

        # Automatically place computer's ships (hidden from the player)
        self.computer_ships = [Ship(name, size) for name, size in ship_definitions]
        for ship in self.computer_ships:
            self.computer_grid.grid = ship.place_ship(self.computer_grid.grid)

    def display_grids(self):
        """Displays the player's and computer's grids side by side."""
        grid_size = len(self.player_grid.grid)
        header = self.player_grid.create_header()
        row_label = self.player_grid.create_row_label()

        print(f"{header}       {header}")
        print(f" {'+' + '-'*(grid_size*6 - 1) + '+'}     {'+' + '-'*(grid_size*6 - 1) + '+'}")

        for i, (player_row, computer_row) in enumerate(zip(self.player_grid.grid, self.computer_grid.grid)):
            # Mask the computer's grid: show only hits ('X') and misses ('O')
            masked_computer_row = [" " if cell not in ["X", "O"] else cell for cell in computer_row]

            player_row_display = f"{row_label[i]}" + "".join(f"|{cell:5}" for cell in player_row) + "|"
            computer_row_display = f"{row_label[i]}" + "".join(f"|{cell:5}" for cell in masked_computer_row) + "|"

            print(f"{player_row_display}    {computer_row_display}")
            print(f" {'+' + '-'*(grid_size*6 - 1) + '+'}     {'+' + '-'*(grid_size*6 - 1) + '+'}")

    def play_game(self):
        """Main game loop."""
        display_welcome_message()  # Display the welcome message
        self.setup_ships()  # Set up the ships for both the player and the computer

        # Game loop: player and computer take turns until one wins
        while True:
            # Display both grids
            print("\nYour grid and the computer's grid:")
            self.display_grids()

            # Player's turn
            self.player_turn()
            player_wins, computer_wins = self.check_win_condition()  # Check if the player has won
            if player_wins:
                print("Congratulations! You've won the game!")
                self.end_game("win")
                break

            # Computer's turn
            self.computer_turn()
            player_wins, computer_wins = self.check_win_condition()  # Check if the computer has won
            if computer_wins:
                print("The computer has won the game!")
                self.end_game("lose")
                break


    def end_game(self, result):
        """Handles the end game logic and stores the result in the database."""
        db_handler = DatabaseHandler("localhost", "yourusername", "yourpassword", "battleship")
        db_handler.insert_game_result(self.player_name, result, self.player_moves)
        print(f"Game Over. You {result.upper()}! Moves taken: {self.player_moves}")

# Main 
if __name__ == "__main__":
    try:
        player_name = input("Enter your name: ")
        game = Game(grid_size=10, player_name=player_name)  # Initialize the game

        # Setup the database and results table
        db_handler = DatabaseHandler("localhost", "yourusername", "yourpassword", "battleship")
        db_handler.create_results_table()

        # Start the game
        game.play_game()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
