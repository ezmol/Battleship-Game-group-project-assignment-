# Project Assignment - Battleship

# Battleship Game

A command-line implementation of the classic Battleship game, with features such as player vs. computer gameplay, MySQL database integration for storing game results, and a comprehensive testing suite.

## Features
- **Player vs. Computer Gameplay**: Play the classic Battleship game against a computer opponent.
- **Ship Placement**: Manually place your ships on the grid with a simple, intuitive interface.
- **MySQL Database Integration**: Automatically store game results in a MySQL database.
- **Error Handling**: Robust error handling for invalid inputs and overlapping ship placements.
- **ASCII Art**: ASCII art to enhance the gaming experience.
- **Testing Suite**: A full suite of unit tests to ensure the game's core functionality.

## Installation

### Prerequisites
- Python 3.x
- MySQL Server

### Setup Instructions

1. **Clone the Repository**:
   ```
   git clone https://github.com/eavdi/Project-Assignment.git

2. Create a Virtual Environment:
    ````
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install the Required Dependencies
    ```
    pip install -r requirements.txt

4. Set Up the MySQL Database:

    - Log into your MySQL server and create a new database:

    ```CREATE DATABASE battleship; ```

    - Update the DatabaseHandler class in battleship.py with your MySQL credentials:
        ````
      db_handler = DatabaseHandler("localhost", "yourusername", "yourpassword", "battleship")

5. Run the Game:
    ```
    python battleship.py 

6. Run Tests
    ```
   python -m unittest discover 

## How to Play
1. Game Start: Upon starting the game, you'll be greeted with an ASCII art welcome message.
2. Ship Placement: You'll be prompted to place your ships on the grid by specifying the orientation (horizontal or vertical) and the starting coordinates.
3. Gameplay: After placing your ships, the game begins. Take turns with the computer to guess the locations of each other's ships.
4. Winning: The first to sink all opponent ships wins the game. The results will be stored in the MySQL database.

## Project Structure
- battleship.py: Main game logic and classes.
- test_battleship.py: Contains all unit tests for the game's functionality.
- utils.py: Utility functions for grid formatting and input validation.
- requirements.txt: Python dependencies required for the project.

## Troubleshooting
**Database Connection Issues:** Ensure that your MySQL server is running and that your credentials in battleship.py are correct.
**Invalid Inputs:** The game includes robust error handling, but ensure you input valid orientations and coordinates when prompted.
