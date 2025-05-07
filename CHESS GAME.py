import chess
import tkinter as tk
from tkinter import messagebox, Menu
import math

class ChessGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess vs AI")
        
        # Game settings
        self.difficulty = 3  #Default AI depth
        self.player_color = True  #True = White, False = Black
        self.show_legal_moves = True #shows legal moves for the select chess piece
        
        # Game state
        self.board = chess.Board() #creates a fresh chess board with pieces on initial setting,imports from chess library
        self.selected_square = None #to notify the selected square,highligh/legal moves
        self.move_history = [] #side wali list ke liye
        self.game_in_progress = True #bool flag, game chal raha hai, (not checkmate, draw, or resigned)
        self.last_move = None #track last move(highlights suares,jis point se move kiya hai and jaha pe move kiya hai, none hai kyuki initialize kiya hai)
        
        # UI settings
        self.square_size = 60 #side of square box (pixels)
        self.board_size = self.square_size * 8 #board size 8 square per side
        self.light_square_color = "#EEE8AA"
        self.dark_square_color = "#654321"
        self.selected_color = "#BACA2B"
        self.move_highlight_color = "#8BB24D"
        self.last_move_color = "#F7EC59"
        self.check_color = "#FF6B6B"
        
        # Create main frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=10, pady=10)
        
        # Create canvas for board
        self.canvas = tk.Canvas(  #board ko initialize kiya hai
            self.main_frame,
            width=self.board_size,
            height=self.board_size
        )
        self.canvas.pack(side=tk.LEFT) #place board on the left of frame
        
        # Create side panel
        self.side_panel = tk.Frame(self.main_frame)
        self.side_panel.pack(side=tk.LEFT, padx=10) #yaha par left hai,kyuki tk places the box immediate left of the sibling,agar right kiya toh the anchor will shift to the ver rught end and we will have a blank space in between
        
        # Status label
        self.status_label = tk.Label( 
            self.side_panel,
            text="White to move",
            font=("Arial", 12)
        )
        self.status_label.pack(pady=10)
        
        # Move history
        history_frame = tk.LabelFrame(self.side_panel, text="Move History")
        history_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.history_text = tk.Text(history_frame, width=15, height=15)
        self.history_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        
        # Control buttons
        button_frame = tk.Frame(self.side_panel)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.new_game_button = tk.Button(
            button_frame,
            text="New Game",
            command=self.new_game
        )
        self.new_game_button.pack(side=tk.LEFT, padx=5)
        
        self.resign_button = tk.Button(
            button_frame,
            text="Resign",
            command=self.resign_game
        )
        self.resign_button.pack(side=tk.RIGHT, padx=5)
        
        # Create menu
        self.create_menu() #calls create menu(file,setting,help wala bar)
        
        # Piece graphics
        self.piece_unicode = { #dictionary of pieces
            "P": "♙", "N": "♘", "B": "♗", "R": "♖", "Q": "♕", "K": "♔",
            "p": "♟", "n": "♞", "b": "♝", "r": "♜", "q": "♛", "k": "♚"
        }
        
        # Bind events
        self.canvas.bind("<Button-1>", self.on_square_click) #every left-click(button-1 indicates left click) on the board into a chess-board action: selecting your piece, highlighting it, showing its legal moves, and then—on the second click—actually moving it.
        
        # Initialize the board display
        self.draw_board() #calling drawboard
        
        # Start the game
        if not self.player_color: #if not white color
            self.root.after(100, self.make_ai_move) #after 0.1 sec ai moves first
    
    def create_menu(self):
        menubar = Menu(self.root) #initailizes menu wala bar
        
        # File menu
        file_menu = Menu(menubar, tearoff=0) #menu => dropdown submenu , tearoff=> disables floating window(to avoid pop out window)
        file_menu.add_command(label="New Game", command=self.new_game)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Settings menu
        settings_menu = Menu(menubar, tearoff=0)
        
        # Difficulty submenu
        difficulty_menu = Menu(settings_menu, tearoff=0)
        for level in range(1, 6):
            difficulty_menu.add_radiobutton(
                label=f"Level {level}", 
                variable=tk.IntVar(value=self.difficulty), 
                value=level,
                command=lambda l=level: self.set_difficulty(l)
            )
        settings_menu.add_cascade(label="AI Difficulty", menu=difficulty_menu)
        
        # Player color submenu
        color_menu = Menu(settings_menu, tearoff=0)
        color_menu.add_radiobutton(
            label="Play as White", 
            command=lambda: self.set_player_color(True)
        )
        color_menu.add_radiobutton(
            label="Play as Black", 
            command=lambda: self.set_player_color(False)
        )
        settings_menu.add_cascade(label="Player Color", menu=color_menu)
        
        # Legal moves option
        settings_menu.add_checkbutton( #checkbutton => use for creating checkbox
            label="Don't Show Legal Moves", 
            variable=tk.BooleanVar(value=self.show_legal_moves),
            command=lambda: self.toggle_show_legal_moves()
        )
        
        menubar.add_cascade(label="Settings", menu=settings_menu)
        
        # Help menu
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def set_difficulty(self, level): #set difficulty wala func
        self.difficulty = level
    
    def set_player_color(self, is_white): #color change karne ke liye
        # Only allow color change during a new game
        if len(self.move_history) > 0: #checks condition, agar gameshuru ho gay toh color change nahi hoga
            messagebox.showinfo("Info", "You can change color only before starting a new game.")
            return
        
        self.player_color = is_white
        
        # If switching to black and it's a new game, make AI move
        if not is_white and len(self.move_history) == 0:
            self.root.after(100, self.make_ai_move)
    
    def toggle_show_legal_moves(self):
        self.show_legal_moves = not self.show_legal_moves
        self.draw_board()
    
    def draw_board(self):
        self.canvas.delete("all")
        
        # Draw square backgrounds
        for row in range(8):
            for col in range(8):
                x1 = col * self.square_size
                y1 = row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                
                # Determine square color
                color = self.light_square_color if (row + col) % 2 == 0 else self.dark_square_color
                
                # Highlight selected square
                if self.selected_square is not None:
                    sel_col = chess.square_file(self.selected_square)
                    sel_row = 7 - chess.square_rank(self.selected_square)
                    if row == sel_row and col == sel_col: #If you’ve clicked a piece, override that square’s color with selected_color
                        color = self.selected_color 
                
                # Draw the square
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="") #square boxes filled with color without border
        
        # Draw rank and file labels
        for i in range(8):
            # Rank labels (1-8)
            x = 5 #used as padding
            y = i * self.square_size + self.square_size // 2
            color = self.dark_square_color if i % 2 == 0 else self.light_square_color
            self.canvas.create_text(x, y, text=str(8-i), fill=color, font=("Arial", 10))
         
            # File labels (a-h)
            x = i * self.square_size + self.square_size // 2
            y = self.board_size - 5
            color = self.dark_square_color if (7 + i) % 2 == 0 else self.light_square_color
            self.canvas.create_text(x, y, text=chr(97+i), fill=color, font=("Arial", 10))
        
        # Highlight legal moves for selected piece
        if self.selected_square is not None and self.show_legal_moves:
            self.highlight_legal_moves()
        
        # Highlight last move
        if self.last_move:
            for square in [self.last_move.from_square, self.last_move.to_square]:
                col = chess.square_file(square)
                row = 7 - chess.square_rank(square)
                x1 = col * self.square_size
                y1 = row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, 
                    fill="", 
                    outline=self.last_move_color,
                    width=3
                )
        
        # Highlight king in check
        if self.board.is_check():
            king_square = self.board.king(self.board.turn)
            col = chess.square_file(king_square)
            row = 7 - chess.square_rank(king_square)
            x1 = col * self.square_size
            y1 = row * self.square_size
            x2 = x1 + self.square_size
            y2 = y1 + self.square_size
            self.canvas.create_rectangle(
                x1, y1, x2, y2, 
                fill="", 
                outline=self.check_color,
                width=3
            )
        
        # Draw pieces
        for row in range(8):
            for col in range(8):
                square = chess.square(col, 7 - row)
                piece = self.board.piece_at(square)
                if piece:
                    x = col * self.square_size + self.square_size // 2
                    y = row * self.square_size + self.square_size // 2
                    piece_symbol = self.piece_unicode[piece.symbol()]
                    self.canvas.create_text(
                        x, y, 
                        text=piece_symbol, 
                        font=("Arial", 36),
                        fill="black" if piece.color == chess.WHITE else "black"
                    )
        
        # Update status
        self.update_status()
    
    def highlight_legal_moves(self):
        for move in self.board.legal_moves:
            if move.from_square == self.selected_square:
                to_square = move.to_square
                col = chess.square_file(to_square)
                row = 7 - chess.square_rank(to_square)
                x = col * self.square_size + self.square_size // 2
                y = row * self.square_size + self.square_size // 2
                
                # Check if square has an opponent's piece
                has_piece = self.board.piece_at(to_square) is not None
                
                if has_piece:
                    # Highlight captures with a circle outline
                    r = self.square_size // 2 - 4
                    self.canvas.create_oval(
                        x - r, y - r, x + r, y + r,
                        outline=self.move_highlight_color,
                        width=3
                    )
                else:
                    # Highlight empty squares with a dot
                    r = self.square_size // 6
                    self.canvas.create_oval(
                        x - r, y - r, x + r, y + r,
                        fill=self.move_highlight_color,
                        outline=""
                    )
    
    def on_square_click(self, event): #galti se click hone par check karne ke liye, if hamari move hogi toh piece select hoga and if computer ki turn hogi toh kuch nahi hoga hamare click se
        if not self.game_in_progress or (self.board.turn != chess.WHITE) != (not self.player_color):
            return
        
        col = event.x // self.square_size
        row = 7 - (event.y // self.square_size)
        
        # Make sure click is within board bounds
        if not (0 <= col < 8 and 0 <= row < 8): #click outside the chess board,ignore
            return
            
        square = chess.square(col, row)
        
        # If no square is selected, select this one if it has a piece of the player's color
        if self.selected_square is None:
            piece = self.board.piece_at(square) #checks piece at selected square
            if piece and piece.color == self.board.turn: #if piece present and its my turn then shows possible moves
                self.selected_square = square
                self.draw_board()
        else:
            # If a square is already selected, try to make a move
            move = chess.Move(self.selected_square, square)
            
            # Handle promotion
            if self.is_pawn_promotion(move):
                move = chess.Move(self.selected_square, square, promotion=chess.QUEEN)
            
            # Try to make the move
            if move in self.board.legal_moves:
                self.make_move(move)
                
                # If game is not over and it's AI's turn, make AI move
                if self.game_in_progress and (self.board.turn == chess.WHITE) != self.player_color:
                    self.root.after(500, self.make_ai_move)
            
            # Deselect the square
            self.selected_square = None
            self.draw_board()
    
    def is_pawn_promotion(self, move):
        piece = self.board.piece_at(move.from_square)
        if not piece or piece.piece_type != chess.PAWN:
            return False
        
        # Check if pawn is moving to the last rank
        to_rank = chess.square_rank(move.to_square)
        return (to_rank == 0 or to_rank == 7) and move in self.board.legal_moves
    
    def make_move(self, move):
        # Make the move
        self.board.push(move)
        self.move_history.append(move)
        self.last_move = move
        
        # Update move history display
        self.update_move_display()
        
        # Check for game over
        if self.board.is_game_over():
            self.game_in_progress = False
            self.show_result()
        
        # Redraw the board
        self.draw_board()
    
    def update_move_display(self):
        if not self.move_history:
            return
        
        self.history_text.delete(1.0, tk.END)
        
        move_pairs = []
        for i in range(0, len(self.move_history), 2):
            move_str = f"{i//2 + 1}. {self.move_history[i].uci()}"
            if i + 1 < len(self.move_history):
                move_str += f" {self.move_history[i+1].uci()}"
            move_pairs.append(move_str)
        
        self.history_text.insert(tk.END, "\n".join(move_pairs)) #each move is stored on next line
        self.history_text.see(tk.END) #auto scrolls and shows the last move
    
    def update_status(self):
        if not self.game_in_progress:
            return
        
        status = ""
        
        if self.board.is_check():
            status = "Check! "
        
        if self.board.turn == chess.WHITE:
            status += "White to move"
        else:
            status += "Black to move"
        
        self.status_label.config(text=status)
    
    def make_ai_move(self):
        if not self.game_in_progress:
            return
        
        # Start thinking animation
        self.status_label.config(text="AI is thinking...")
        self.root.update_idletasks() #process any pending UI updates, gives time to think for ai
        
        # Calculate best move
        _, best_move = self.minimax(
            self.board, 
            self.difficulty, 
            -math.inf, 
            math.inf, 
            self.board.turn == chess.WHITE
        )
        
        if best_move:
            self.make_move(best_move)
    
    def minimax(self, board, depth, alpha, beta, is_maximizing):
        # Return evaluation if we've reached max depth or game over
        if depth == 0 or board.is_game_over():
            return self.evaluate_position(board), None
        
        best_move = None
        
        if is_maximizing:
            max_eval = -math.inf
            for move in board.legal_moves:
                board.push(move)
                eval_score, _ = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
                    
            return max_eval, best_move
        else:
            min_eval = math.inf
            for move in board.legal_moves:
                board.push(move)
                eval_score, _ = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
                    
            return min_eval, best_move
    
    # Basic piece values
    piece_values = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 20000
    }
    
    # Piece-square tables for position evaluation
    pawn_table = [
        0,  0,  0,  0,  0,  0,  0,  0,
        50, 50, 50, 50, 50, 50, 50, 50,
        10, 10, 20, 30, 30, 20, 10, 10,
        5,  5, 10, 25, 25, 10,  5,  5,
        0,  0,  0, 20, 20,  0,  0,  0,
        5, -5,-10,  0,  0,-10, -5,  5,
        5, 10, 10,-20,-20, 10, 10,  5,
        0,  0,  0,  0,  0,  0,  0,  0
    ]
    
    knight_table = [
        -50,-40,-30,-30,-30,-30,-40,-50,
        -40,-20,  0,  0,  0,  0,-20,-40,
        -30,  0, 10, 15, 15, 10,  0,-30,
        -30,  5, 15, 20, 20, 15,  5,-30,
        -30,  0, 15, 20, 20, 15,  0,-30,
        -30,  5, 10, 15, 15, 10,  5,-30,
        -40,-20,  0,  5,  5,  0,-20,-40,
        -50,-40,-30,-30,-30,-30,-40,-50
    ]
    
    bishop_table = [
        -20,-10,-10,-10,-10,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0, 10, 10, 10, 10,  0,-10,
        -10,  5,  5, 10, 10,  5,  5,-10,
        -10,  0,  5, 10, 10,  5,  0,-10,
        -10,  5,  5,  5,  5,  5,  5,-10,
        -10,  0,  5,  0,  0,  5,  0,-10,
        -20,-10,-10,-10,-10,-10,-10,-20
    ]
    
    rook_table = [
        0,  0,  0,  0,  0,  0,  0,  0,
        5, 10, 10, 10, 10, 10, 10,  5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        0,  0,  0,  5,  5,  0,  0,  0
    ]
    
    queen_table = [
        -20,-10,-10, -5, -5,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5,  5,  5,  5,  0,-10,
        -5,  0,  5,  5,  5,  5,  0, -5,
        0,  0,  5,  5,  5,  5,  0, -5,
        -10,  5,  5,  5,  5,  5,  0,-10,
        -10,  0,  5,  0,  0,  0,  0,-10,
        -20,-10,-10, -5, -5,-10,-10,-20
    ]
    
    king_table = [
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -20,-30,-30,-40,-40,-30,-30,-20,
        -10,-20,-20,-20,-20,-20,-20,-10,
        20, 20,  0,  0,  0,  0, 20, 20,
        20, 30, 10,  0,  0, 10, 30, 20
    ]
    
    piece_tables = {
        chess.PAWN: pawn_table,
        chess.KNIGHT: knight_table,
        chess.BISHOP: bishop_table,
        chess.ROOK: rook_table,
        chess.QUEEN: queen_table,
        chess.KING: king_table
    }
    
    def evaluate_position(self, board):
        if board.is_checkmate():
            # Return a large negative value if the side to move is checkmated
            return -10000 if board.turn == chess.WHITE else 10000
            
        if board.is_stalemate() or board.is_insufficient_material():
            return 0
        
        # Material and position evaluation
        value = 0
        
        # Count material and position value
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                # Basic piece value
                piece_value = self.piece_values.get(piece.piece_type, 0)
                
                # Position value from piece-square tables
                position_value = 0
                piece_table = self.piece_tables.get(piece.piece_type)
                if piece_table:
                    # Get the square index (0-63) for the table lookup
                    # Flip the table for black pieces
                    square_idx = square
                    if piece.color == chess.BLACK:
                        square_idx = chess.square_mirror(square)
                    position_value = piece_table[square_idx]
                
                # Add to total evaluation (positive for white, negative for black)
                if piece.color == chess.WHITE:
                    value += piece_value + position_value
                else:
                    value -= piece_value + position_value
        
        return value
    
    def show_result(self):
        result = self.board.result()
        
        if result == "1-0":
            message = "White wins by checkmate!"
        elif result == "0-1":
            message = "Black wins by checkmate!"
        else:
            # Draw
            if self.board.is_stalemate():
                message = "Draw by stalemate!"
            elif self.board.is_insufficient_material():
                message = "Draw by insufficient material!"
            elif self.board.is_seventyfive_moves():
                message = "Draw by 75-move rule!"
            elif self.board.is_fivefold_repetition():
                message = "Draw by fivefold repetition!"
            else:
                message = "Draw!"
        
        messagebox.showinfo("Game Over", message)
    
    def new_game(self):
        # Reset the board
        self.board = chess.Board()
        
        # Reset game state
        self.selected_square = None
        self.move_history = []
        self.last_move = None
        self.game_in_progress = True
        
        # Reset UI
        self.history_text.delete(1.0, tk.END)
        
        # Redraw the board
        self.draw_board()
        
        # If player is black, make AI start
        if not self.player_color:
            self.root.after(100, self.make_ai_move)
    
    def resign_game(self):
        if not self.game_in_progress:
            return
            
        answer = messagebox.askyesno("Resign", "Are you sure you want to resign?")
        if answer:
            self.game_in_progress = False
            messagebox.showinfo("Game Over", "You resigned. Your opponent wins!")
    
    def show_about(self):
        messagebox.showinfo(
            "About",
            "Chess Game\n\n"
            "A chess application with minimax AI and various features.\n\n"
            "Built with Python and Tkinter."
        )


if __name__ == "__main__":
    root = tk.Tk()
    game = ChessGame(root)
    root.mainloop()