"""
=============================================================================
  Game Board & Pattern Generator Toolkit — Interactive Edition
=============================================================================
"""

import matplotlib
matplotlib.use("TkAgg")

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import ListedColormap

# ─── Colour maps ────────────────────────────────────────────────────────────
CHESS_CMAP = ListedColormap(["#F0D9B5", "#B58863"])
TTT_CMAP   = ListedColormap(["#FFFFFF", "#3B82F6", "#EF4444"])
CHECK_CMAP = ListedColormap(["#FAFAFA", "#1E293B"])

PIECE_SYMBOLS = {
    0: " ",
    1: "♙", -1: "♟",
    2: "♘", -2: "♞",
    3: "♗", -3: "♝",
    4: "♖", -4: "♜",
    5: "♕", -5: "♛",
    6: "♔", -6: "♚",
}
TTT_SYMBOLS = {0: " ", 1: "X", 2: "O"}


# ═══════════════════════════════════════════════════════════════════════════
#  HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def make_chessboard(n=8):
    board = np.zeros((n, n), dtype=int)
    board[::2, 1::2] = 1
    board[1::2, ::2] = 1
    return board


def print_chess_board(board):
    print("  ┌" + "───┬" * 7 + "───┐")
    for r in range(8):
        row_str = " │ ".join(PIECE_SYMBOLS.get(int(board[r, c]), "?") for c in range(8))
        print(f"{8 - r} │ {row_str} │")
        if r < 7:
            print("  ├" + "───┼" * 7 + "───┤")
    print("  └" + "───┴" * 7 + "───┘")
    print("    a   b   c   d   e   f   g   h")


def print_ttt(board):
    for r in range(3):
        row = " | ".join(TTT_SYMBOLS[int(board[r, c])] for c in range(3))
        print(f" {row} ")
        if r < 2:
            print("───┼───┼───")


def check_winner(board):
    for player in [1, 2]:
        for r in range(3):
            if np.all(board[r, :] == player): return player
        for c in range(3):
            if np.all(board[:, c] == player): return player
        if np.all(board.diagonal() == player): return player
        if np.all(np.fliplr(board).diagonal() == player): return player
    return 0


# ═══════════════════════════════════════════════════════════════════════════
#  OPTION 1: Tic-Tac-Toe Board
# ═══════════════════════════════════════════════════════════════════════════

def option_ttt_board():
    print("\n── Create Tic-Tac-Toe Board ──")
    print("  a) Using np.zeros((3,3), dtype=int)")
    print("  b) From a nested Python list")
    choice = input("Choose method (a/b): ").strip().lower()

    if choice == "b":
        nested = [[0,0,0],[0,0,0],[0,0,0]]
        board = np.array(nested, dtype=int)
        print("\nCreated from nested list:")
    else:
        board = np.zeros((3, 3), dtype=int)
        print("\nCreated with np.zeros:")

    print(board)
    print_ttt(board)


# ═══════════════════════════════════════════════════════════════════════════
#  OPTION 2: Chessboard Pattern
# ═══════════════════════════════════════════════════════════════════════════

def option_chessboard():
    print("\n── Generate Chessboard ──")
    n = input("Board size (default 8): ").strip()
    n = int(n) if n.isdigit() and int(n) > 0 else 8

    board = make_chessboard(n)
    print(f"\n{n}×{n} Chessboard (stepped slicing: board[::2,1::2]=1, board[1::2,::2]=1):")
    print(board)

    show = input("Show plot? (y/n): ").strip().lower()
    if show == "y":
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.imshow(board, cmap=CHESS_CMAP, interpolation="nearest")
        ax.set_xticks(range(n))
        ax.set_yticks(range(n))
        if n == 8:
            ax.set_xticklabels(list("abcdefgh"))
            ax.set_yticklabels(range(8, 0, -1))
        ax.tick_params(length=0)
        ax.set_title(f"{n}×{n} Chessboard", fontweight="bold")
        plt.tight_layout()
        plt.show()


# ═══════════════════════════════════════════════════════════════════════════
#  OPTION 3: Diagonal & Anti-diagonal Patterns
# ═══════════════════════════════════════════════════════════════════════════

def option_diagonals():
    print("\n── Diagonal Patterns (np.eye) ──")
    n = input("Matrix size (default 8): ").strip()
    n = int(n) if n.isdigit() and int(n) > 0 else 8

    print("  a) Main diagonal")
    print("  b) Anti-diagonal")
    print("  c) X pattern (both)")
    choice = input("Choose (a/b/c): ").strip().lower()

    diag = np.eye(n, dtype=int)
    anti = np.fliplr(np.eye(n, dtype=int))
    x_pat = np.clip(diag + anti, 0, 1)

    if choice == "a":
        print(f"\nMain Diagonal ({n}×{n}) — np.eye({n}):")
        print(diag)
        mat, title = diag, "Main Diagonal"
    elif choice == "b":
        print(f"\nAnti-Diagonal ({n}×{n}) — np.fliplr(np.eye({n})):")
        print(anti)
        mat, title = anti, "Anti-Diagonal"
    else:
        print(f"\nX Pattern ({n}×{n}) — np.eye + np.fliplr:")
        print(x_pat)
        mat, title = x_pat, "X Pattern"

    show = input("Show plot? (y/n): ").strip().lower()
    if show == "y":
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.imshow(mat, cmap="Blues", interpolation="nearest")
        ax.set_title(title, fontweight="bold")
        ax.set_xticks(range(n)); ax.set_yticks(range(n))
        ax.tick_params(length=0)
        plt.tight_layout()
        plt.show()


# ═══════════════════════════════════════════════════════════════════════════
#  OPTION 4: Identity-Style Grids
# ═══════════════════════════════════════════════════════════════════════════

def option_identity_grids():
    print("\n── Identity-Style Grids ──")
    n = input("Grid size (default 5): ").strip()
    n = int(n) if n.isdigit() and int(n) > 0 else 5

    print("  a) np.zeros")
    print("  b) np.ones")
    print("  c) np.full (you pick the fill value)")
    print("  d) np.eye")
    print("  e) np.arange reshaped")
    print("  f) Show ALL side by side")
    choice = input("Choose (a/b/c/d/e/f): ").strip().lower()

    grids = {}
    if choice == "a":
        grids["np.zeros"] = np.zeros((n, n), dtype=int)
    elif choice == "b":
        grids["np.ones"] = np.ones((n, n), dtype=int)
    elif choice == "c":
        v = input("Fill value: ").strip()
        v = int(v) if v.lstrip("-").isdigit() else 7
        grids[f"np.full({v})"] = np.full((n, n), v, dtype=int)
    elif choice == "d":
        grids["np.eye"] = np.eye(n, dtype=int)
    elif choice == "e":
        grids["np.arange reshaped"] = np.arange(n * n).reshape(n, n)
    else:
        grids = {
            "np.zeros": np.zeros((n, n), dtype=int),
            "np.ones":  np.ones((n, n), dtype=int),
            "np.full(7)": np.full((n, n), 7, dtype=int),
            "np.eye":   np.eye(n, dtype=int),
            "np.arange": np.arange(n * n).reshape(n, n),
        }

    for label, mat in grids.items():
        print(f"\n─── {label} ({n}×{n}) ───")
        print(mat)

    show = input("Show plot? (y/n): ").strip().lower()
    if show == "y":
        cols = len(grids)
        fig, axes = plt.subplots(1, cols, figsize=(3.5 * cols, 3.5))
        if cols == 1:
            axes = [axes]
        for ax, (label, mat) in zip(axes, grids.items()):
            ax.imshow(mat, cmap="YlGnBu", interpolation="nearest")
            for i in range(n):
                for j in range(n):
                    ax.text(j, i, str(mat[i, j]), ha="center", va="center", fontsize=9)
            ax.set_title(label, fontweight="bold", fontsize=10)
            ax.set_xticks([]); ax.set_yticks([])
        plt.tight_layout()
        plt.show()


# ═══════════════════════════════════════════════════════════════════════════
#  OPTION 5: Chess — Place & Move Pieces
# ═══════════════════════════════════════════════════════════════════════════

def option_chess_pieces():
    print("\n── Chess: Place & Move Pieces (Fancy Indexing) ──")
    board = np.zeros((8, 8), dtype=int)

    # Setup standard position using fancy indexing
    rows = np.array([0]*8)
    cols = np.arange(8)
    board[rows, cols] = [-4, -2, -3, -5, -6, -3, -2, -4]
    board[1, np.arange(8)] = -1
    board[6, np.arange(8)] = 1
    board[np.full(8, 7), np.arange(8)] = [4, 2, 3, 5, 6, 3, 2, 4]

    print("\nStarting position (placed with fancy indexing):")
    print_chess_board(board)

    # Interactive move loop
    while True:
        cmd = input("\nEnter move as 'r1,c1 r2,c2' (e.g. '6,4 4,4' for e4) or 'q' to quit: ").strip()
        if cmd.lower() == "q":
            break
        try:
            parts = cmd.split()
            fr = tuple(int(x) for x in parts[0].split(","))
            to = tuple(int(x) for x in parts[1].split(","))
            piece = board[fr]
            if piece == 0:
                print("No piece at that square!")
                continue
            board[to] = board[fr]
            board[fr] = 0
            sym = PIECE_SYMBOLS.get(piece, "?")
            print(f"Moved {sym} from {fr} → {to}")
            print_chess_board(board)
        except Exception:
            print("Invalid format. Use: row,col row,col  (e.g. 6,4 4,4)")

    show = input("Show board plot? (y/n): ").strip().lower()
    if show == "y":
        bg = make_chessboard(8)
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.imshow(bg, cmap=CHESS_CMAP, interpolation="nearest")
        for r in range(8):
            for c in range(8):
                s = PIECE_SYMBOLS.get(int(board[r, c]), "")
                if s.strip():
                    ax.text(c, r, s, ha="center", va="center", fontsize=22)
        ax.set_xticks(range(8)); ax.set_yticks(range(8))
        ax.set_xticklabels(list("abcdefgh"))
        ax.set_yticklabels(range(8, 0, -1))
        ax.tick_params(length=0)
        ax.set_title("Chess Position", fontweight="bold", fontsize=14)
        plt.tight_layout()
        plt.show()


# ═══════════════════════════════════════════════════════════════════════════
#  OPTION 6: Checkerboard with Pieces
# ═══════════════════════════════════════════════════════════════════════════

def option_checkerboard():
    print("\n── Checkerboard with Pieces ──")
    board = np.zeros((8, 8), dtype=int)
    for r in range(3):
        dark_cols = np.arange(1 - r % 2, 8, 2)
        board[np.full_like(dark_cols, r), dark_cols] = 1
    for r in range(5, 8):
        dark_cols = np.arange(1 - r % 2, 8, 2)
        board[np.full_like(dark_cols, r), dark_cols] = 2

    print("Piece array (1=red, 2=black):")
    print(board)

    show = input("Show plot? (y/n): ").strip().lower()
    if show == "y":
        bg = make_chessboard(8)
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.imshow(bg, cmap=CHECK_CMAP, interpolation="nearest")
        for r in range(8):
            for c in range(8):
                if board[r, c] == 1:
                    ax.add_patch(plt.Circle((c, r), 0.35, color="#DC2626", ec="white", lw=1.5))
                elif board[r, c] == 2:
                    ax.add_patch(plt.Circle((c, r), 0.35, color="#111827", ec="white", lw=1.5))
        ax.set_xlim(-0.5, 7.5); ax.set_ylim(7.5, -0.5)
        ax.set_xticks(range(8)); ax.set_yticks(range(8))
        ax.tick_params(length=0)
        ax.set_title("Checkers", fontweight="bold", fontsize=14)
        plt.tight_layout()
        plt.show()


# ═══════════════════════════════════════════════════════════════════════════
#  OPTION 7: Tic-Tac-Toe — Play & Win-Check
# ═══════════════════════════════════════════════════════════════════════════

def option_ttt_play():
    print("\n── Play Tic-Tac-Toe ──")
    print("Players take turns. X=1, O=2. Enter row,col (0-2).\n")

    board = np.zeros((3, 3), dtype=int)
    print_ttt(board)

    current = 1  # X goes first
    for move_num in range(1, 10):
        sym = "X" if current == 1 else "O"
        while True:
            pos = input(f"\n{sym}'s turn — enter row,col (e.g. 0,2) or 'q' to quit: ").strip()
            if pos.lower() == "q":
                print("Game ended.")
                return
            try:
                r, c = [int(x) for x in pos.split(",")]
                if not (0 <= r <= 2 and 0 <= c <= 2):
                    print("Row and col must be 0-2!")
                    continue
                if board[r, c] != 0:
                    print("That cell is taken!")
                    continue
                break
            except Exception:
                print("Invalid format. Use: row,col (e.g. 1,1)")

        board[r, c] = current
        print_ttt(board)

        winner = check_winner(board)
        if winner:
            print(f"\n🎉  {'X' if winner == 1 else 'O'} wins!")
            break

        if move_num == 9:
            print("\nIt's a draw!")
            break

        current = 2 if current == 1 else 1

    show = input("\nShow board plot? (y/n): ").strip().lower()
    if show == "y":
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.imshow(board, cmap=TTT_CMAP, vmin=0, vmax=2, interpolation="nearest")
        for i in range(1, 3):
            ax.axhline(i - 0.5, color="black", lw=2)
            ax.axvline(i - 0.5, color="black", lw=2)
        for r2 in range(3):
            for c2 in range(3):
                s = TTT_SYMBOLS[int(board[r2, c2])]
                if s != " ":
                    ax.text(c2, r2, s, ha="center", va="center",
                            fontsize=36, fontweight="bold", color="white")
        ax.set_xticks(range(3)); ax.set_yticks(range(3))
        w = check_winner(board)
        title = "Tic-Tac-Toe"
        if w: title += f"  — {'X' if w==1 else 'O'} wins!"
        ax.set_title(title, fontweight="bold", fontsize=13)
        ax.tick_params(length=0)
        plt.tight_layout()
        plt.show()


# ═══════════════════════════════════════════════════════════════════════════
#  OPTION 8: Win-Condition Tester
# ═══════════════════════════════════════════════════════════════════════════

def option_win_tester():
    print("\n── Win-Condition Tester ──")
    print("Enter a 3×3 board row by row (0=empty, 1=X, 2=O).")
    print("Example row: 1 0 2\n")

    rows = []
    for i in range(3):
        while True:
            line = input(f"Row {i}: ").strip()
            try:
                vals = [int(x) for x in line.split()]
                if len(vals) != 3 or not all(v in [0, 1, 2] for v in vals):
                    print("Enter exactly 3 values, each 0/1/2")
                    continue
                rows.append(vals)
                break
            except Exception:
                print("Invalid input. Example: 1 0 2")

    board = np.array(rows, dtype=int)
    print("\nYour board:")
    print_ttt(board)

    w = check_winner(board)
    if w:
        print(f"\nResult: {'X' if w == 1 else 'O'} wins!")
        print(f"  (Checked rows via board[r,:], columns via board[:,c],")
        print(f"   diagonal via board.diagonal(), anti-diag via np.fliplr(board).diagonal())")
    else:
        print("\nResult: No winner yet.")

    show = input("Show plot? (y/n): ").strip().lower()
    if show == "y":
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.imshow(board, cmap=TTT_CMAP, vmin=0, vmax=2, interpolation="nearest")
        for i in range(1, 3):
            ax.axhline(i - 0.5, color="black", lw=2)
            ax.axvline(i - 0.5, color="black", lw=2)
        for r in range(3):
            for c in range(3):
                s = TTT_SYMBOLS[int(board[r, c])]
                if s != " ":
                    ax.text(c, r, s, ha="center", va="center",
                            fontsize=36, fontweight="bold", color="white")
        ax.set_xticks(range(3)); ax.set_yticks(range(3))
        title = "Win Checker"
        if w: title += f"  — {'X' if w==1 else 'O'} wins!"
        ax.set_title(title, fontweight="bold")
        ax.tick_params(length=0)
        plt.tight_layout()
        plt.show()


# ═══════════════════════════════════════════════════════════════════════════
#  MAIN MENU
# ═══════════════════════════════════════════════════════════════════════════

def main():
    menu = """
╔══════════════════════════════════════════════════╗
║   Game Board & Pattern Generator Toolkit         ║
╠══════════════════════════════════════════════════╣
║  1. Create Tic-Tac-Toe board (zeros / nested)    ║
║  2. Generate chessboard pattern                  ║
║  3. Diagonal / anti-diagonal patterns (np.eye)   ║
║  4. Identity-style grids (zeros/ones/full/eye)   ║
║  5. Chess — place & move pieces                  ║
║  6. Checkerboard with pieces                     ║
║  7. Play Tic-Tac-Toe (interactive)               ║
║  8. Win-condition tester                         ║
║  0. Exit                                         ║
╚══════════════════════════════════════════════════╝"""

    options = {
        "1": option_ttt_board,
        "2": option_chessboard,
        "3": option_diagonals,
        "4": option_identity_grids,
        "5": option_chess_pieces,
        "6": option_checkerboard,
        "7": option_ttt_play,
        "8": option_win_tester,
    }

    while True:
        print(menu)
        choice = input("\nChoose an option (0-8): ").strip()
        if choice == "0":
            print("\nGoodbye! 👋")
            break
        elif choice in options:
            options[choice]()
        else:
            print("Invalid choice. Enter 0-8.")


if __name__ == "__main__":
    main()
