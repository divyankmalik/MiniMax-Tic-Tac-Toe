import math
import copy

class TicTacToe:
    
    
    def __init__(self):
        # Initialize empty 3x3 board
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'  # X always goes first
        self.ai_player = 'O'
        self.human_player = 'X'
        
    def print_board(self):
        ## Displays the board
        print("\n")
        print("  0   1   2")
        for i, row in enumerate(self.board):
            print(f"{i} {row[0]} | {row[1]} | {row[2]}")
            if i < 2:
                print("----")
        print("\n")
    
    def is_valid_move(self, row, col):
       ## checks if the move is within the bounds
        return 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == ' '
    
    def make_move(self, row, col, player):
        ## places the players move on the board
        if self.is_valid_move(row, col):
            self.board[row][col] = player
            return True
        return False
    
    def get_available_moves(self):
        ## get the position of empty cells on the board
        moves = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    moves.append((i, j))
        return moves
    
    def check_winner(self):
        ## thye function checks for winners here
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != ' ':
                return row[0]
        
        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != ' ':
                return self.board[0][col]
        
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[1][1]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[1][1]
        
        # Check for draw
        if not self.get_available_moves():
            return 'Draw'
        
        return None
    
    def is_terminal(self):
        # calls the check_winner func to determine to close or run the tab
        return self.check_winner() is not None
    
    def evaluate(self):

        winner = self.check_winner()
        if winner == self.ai_player:
            return 10
        elif winner == self.human_player:
            return -10
        else:
            return 0


class MinimaxAI:
    """
    AI agent that uses Minimax algorithm with Alpha-Beta Pruning.
    """
    
    def __init__(self, game):
        self.game = game
        self.nodes_explored = 0
        self.nodes_pruned = 0
    
    def minimax(self, board_state, depth, alpha, beta, is_maximizing):
        """
        Minimax algorithm with Alpha-Beta Pruning.
        
        Args:
            board_state: Current game state
            depth: Current depth in the game tree
            alpha: Best value for maximizer (alpha cutoff)
            beta: Best value for minimizer (beta cutoff)
            is_maximizing: True if maximizing player's turn, False otherwise
            
        Returns:
            Best score achievable from this state
        """
        self.nodes_explored += 1
        
        # Terminal state check
        if board_state.is_terminal():
            score = board_state.evaluate()
            # Adjust score based on depth to prefer quicker wins
            if score > 0:
                return score - depth
            elif score < 0:
                return score + depth
            return 0
        
        if is_maximizing:
            # AI's turn (maximizing player)
            max_eval = -math.inf
            
            for move in board_state.get_available_moves():
                # Create a copy of the board for simulation
                temp_board = copy.deepcopy(board_state)
                temp_board.make_move(move[0], move[1], self.game.ai_player)
                
                # Recursive call
                eval_score = self.minimax(temp_board, depth + 1, alpha, beta, False)
                max_eval = max(max_eval, eval_score)
                
                # Alpha-Beta Pruning
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    self.nodes_pruned += 1
                    break  # Beta cutoff
            
            return max_eval
        else:
            # Human's turn (minimizing player)
            min_eval = math.inf
            
            for move in board_state.get_available_moves():
                # Create a copy of the board for simulation
                temp_board = copy.deepcopy(board_state)
                temp_board.make_move(move[0], move[1], self.game.human_player)
                
                # Recursive call
                eval_score = self.minimax(temp_board, depth + 1, alpha, beta, True)
                min_eval = min(min_eval, eval_score)
                
                # Alpha-Beta Pruning
                beta = min(beta, eval_score)
                if beta <= alpha:
                    self.nodes_pruned += 1
                    break  # Alpha cutoff
            
            return min_eval
    
    def find_best_move(self):
        """
        Find the optimal move for the AI using Minimax with Alpha-Beta Pruning.
        
        Returns:
            Tuple (row, col) representing the best move
        """
        best_move = None
        best_value = -math.inf
        self.nodes_explored = 0
        self.nodes_pruned = 0
        
        print("AI's Turn...")
        
        for move in self.game.get_available_moves():
            # Simulate the move
            temp_board = copy.deepcopy(self.game)
            temp_board.make_move(move[0], move[1], self.game.ai_player)
            
            # Evaluate using Minimax with Alpha-Beta Pruning
            move_value = self.minimax(temp_board, 0, -math.inf, math.inf, False)
            
            if move_value > best_value:
                best_value = move_value
                best_move = move
        
        print(f"Nodes explored: {self.nodes_explored}")
        print(f"Nodes pruned: {self.nodes_pruned}")
        print(f"Best move value: {best_value}")
        
        return best_move


def play_game():
    #Main game loop for playing Tic-Tac-Toe against the AI.
    print("="*50)
    print("Welcome to Tic-Tac-Toe!")
    print("="*50)
    print("\nYou are X and the Minimax AI is O")
    print("Enter your moves as 'row col' (e.g., '0 1' for top middle)")
    print("="*50)
    
    game = TicTacToe()
    ai = MinimaxAI(game)
    
    # Ask who goes first
    while True:
        first = input("\nWho goes first? (h for human, a for AI): ").lower()
        if first in ['h', 'a']:
            break
        print("Invalid input. Please enter 'h' or 'a'")
    
    current_turn = 'X' if first == 'h' else 'O'
    
    while not game.is_terminal():
        game.print_board()
        
        if current_turn == game.human_player:
            # Human's turn
            print("Your turn (X)")
            while True:
                try:
                    move_input = input("Enter move (row col): ").strip().split()
                    if len(move_input) != 2:
                        print("Please enter two numbers separated by space")
                        continue
                    
                    row, col = int(move_input[0]), int(move_input[1])
                    
                    if game.make_move(row, col, game.human_player):
                        break
                    else:
                        print("Invalid move! Try again.")
                except (ValueError, IndexError):
                    print("Invalid input! Enter row and column as numbers (0-2)")
            
            current_turn = game.ai_player
        else:
            # AI's turn
            print("AI's turn (O)")
            move = ai.find_best_move()
            game.make_move(move[0], move[1], game.ai_player)
            print(f"AI placed O at position ({move[0]}, {move[1]})")
            
            current_turn = game.human_player
    
    # Game over
    game.print_board()
    winner = game.check_winner()
    
    print("="*50)
    if winner == 'Draw':
        print("It's a draw!")
    elif winner == game.human_player:
        print("Congratulations! You won!")
    else:
        print("AI wins! Better luck next time!")
    print("="*50)


if __name__ == "__main__":
    while True:
        play_game()
        
        play_again = input("\nPlay again? (y/n): ").lower()
        if play_again != 'y':
            print("\nThanks for playing!")
            break