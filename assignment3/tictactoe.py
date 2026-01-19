#Task 6

class TictactoeException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class Board:
    valid_moves = [
        "upper left", "upper center", "upper right",
        "middle left", "center", "middle right",
        "lower left", "lower center", "lower right"
    ]

    def __init__(self):
        self.board_array = [[" "]*3 for _ in range(3)]
        self.turn = "X"
        self.last_move = None

    # String representation
    def __str__(self):
        lines = []
        lines.append(f" {self.board_array[0][0]} | {self.board_array[0][1]} | {self.board_array[0][2]} \n")
        lines.append("-----------\n")
        lines.append(f" {self.board_array[1][0]} | {self.board_array[1][1]} | {self.board_array[1][2]} \n")
        lines.append("-----------\n")
        lines.append(f" {self.board_array[2][0]} | {self.board_array[2][1]} | {self.board_array[2][2]} \n")
        return "".join(lines)

    # Make a move
    def move(self, move_string):
        if move_string not in Board.valid_moves:
            raise TictactoeException("That's not a valid move.")
        move_index = Board.valid_moves.index(move_string)
        row = move_index // 3
        col = move_index % 3
        if self.board_array[row][col] != " ":
            raise TictactoeException("That spot is taken.")
        self.board_array[row][col] = self.turn
        self.last_move = move_string
        self.turn = "O" if self.turn == "X" else "X"

    # Check game status
    def whats_next(self):
        # Check for empty spots
        if all(self.board_array[i][j] != " " for i in range(3) for j in range(3)):
            cat = True
        else:
            cat = False

        if cat:
            return (True, "Cat's Game.")

        # Check rows
        for i in range(3):
            if self.board_array[i][0] != " " and self.board_array[i][0] == self.board_array[i][1] == self.board_array[i][2]:
                return (True, f"{self.board_array[i][0]} wins!")

        # Check columns
        for i in range(3):
            if self.board_array[0][i] != " " and self.board_array[0][i] == self.board_array[1][i] == self.board_array[2][i]:
                return (True, f"{self.board_array[0][i]} wins!")

        # Check diagonals
        if self.board_array[1][1] != " ":
            if self.board_array[0][0] == self.board_array[1][1] == self.board_array[2][2]:
                return (True, f"{self.board_array[1][1]} wins!")
            if self.board_array[0][2] == self.board_array[1][1] == self.board_array[2][0]:
                return (True, f"{self.board_array[1][1]} wins!")

        # Game not over
        return (False, f"{self.turn}'s turn.")


# Main game loop
if __name__ == "__main__":
    board = Board()
    print("Welcome to Tic Tac Toe!\n")
    
    game_over = False
    while not game_over:
        print(board)
        move = input(f"{board.turn}'s move (choose from {Board.valid_moves}): ").strip().lower()
        try:
            board.move(move)
        except TictactoeException as e:
            print("Error:", e.message)
            continue

        game_over, message = board.whats_next()
        if game_over:
            print(board)
            print("Game Over:", message)
