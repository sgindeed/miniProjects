import os

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_board(board):
    clear_screen()
    print("\nTic-Tac-Toe\n")
    print("Player 1 (X)  -  Player 2 (O)\n")
    print("     |     |")
    for row in board:
        print("  " + "  |  ".join(row))
        if row != board[-1]:
            print("_____|_____|_____")
    print("     |     |")

def check_winner(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True

    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True

    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True

    return False

def is_board_full(board):
    return all(cell != " " for row in board for cell in row)

def get_player_move(board, player):
    while True:
        try:
            row = int(input(f"Player {player}, enter the row (0, 1, 2): "))
            col = int(input(f"Player {player}, enter the column (0, 1, 2): "))

            if 0 <= row <= 2 and 0 <= col <= 2 and board[row][col] == " ":
                return row, col
            else:
                print("Invalid move. Try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def tic_tac_toe():
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"

    print("Welcome to Tic-Tac-Toe!\n")
    input("Press Enter to start...")

    while True:
        print_board(board)
        row, col = get_player_move(board, current_player)
        board[row][col] = current_player

        if check_winner(board, current_player):
            print_board(board)
            print(f"\nPlayer {current_player} wins! Congratulations!")
            break

        if is_board_full(board):
            print_board(board)
            print("\nIt's a draw!")
            break

        current_player = "O" if current_player == "X" else "X"

if __name__ == "__main__":
    tic_tac_toe()

