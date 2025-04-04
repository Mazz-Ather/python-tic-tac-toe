import streamlit as st
import numpy as np

# Initialize the game board
def Initialize_game():
    return np.full((3, 3), ' '), "X"  # Corrected np.full() instead of np.fall()

# Function to check if there is a winner
def check_winner(board):
    for i in range(3):
        # Check rows
        if board[i, 0] == board[i, 1] == board[i, 2] and board[i, 0] != ' ':
            return board[i, 0]
        # Check columns
        if board[0, i] == board[1, i] == board[2, i] and board[0, i] != ' ':
            return board[0, i]

    # Check diagonals
    if board[0, 0] == board[1, 1] == board[2, 2] and board[0, 0] != ' ':
        return board[0, 0]
    if board[0, 2] == board[1, 1] == board[2, 0] and board[0, 2] != ' ':
        return board[0, 2]

    return None  # No winner yet

# Function to display the board with buttons
def display_board(board):
    clicked_pos = None, None
    
    for i in range(3):
        cols = st.columns(3)  # Create 3 columns for the row
        for j in range(3):
            with cols[j]:
                button_key = f'button_{i}_{j}_{st.session_state.turn}'  # Unique button key
                # Make buttons more visually appealing and clearer
                if board[i, j] == ' ':
                    button_label = "   "
                    button_color = "gray"
                else:
                    button_label = board[i, j]
                    button_color = "blue" if board[i, j] == "X" else "red"
                
                # Use custom button styling to make X and O more visible
                if st.button(button_label, key=button_key):
                    clicked_pos = (i, j)
    
    return clicked_pos

# Main game function
def main():
    # Initialize session state variables
    if 'board' not in st.session_state:
        st.session_state.board, st.session_state.current_player = Initialize_game()
        st.session_state.game_over = False
        st.session_state.turn = 0
        st.session_state.move_made = False
        st.session_state.x_score = 0
        st.session_state.o_score = 0
        st.session_state.ties = 0
    # Ensure move_made exists in all cases
    elif 'move_made' not in st.session_state:
        st.session_state.move_made = False
    
    # Initialize scores if they don't exist
    if 'x_score' not in st.session_state:
        st.session_state.x_score = 0
    if 'o_score' not in st.session_state:
        st.session_state.o_score = 0
    if 'ties' not in st.session_state:
        st.session_state.ties = 0

    st.title("Tic-Tac-Toe")  # Game title
    
    # Display scoreboard
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Player X", st.session_state.x_score)
    with col2:
        st.metric("Ties", st.session_state.ties)
    with col3:
        st.metric("Player O", st.session_state.o_score)

    # Display current player's turn with more emphasis
    if not st.session_state.game_over:
        player_color = "blue" if st.session_state.current_player == "X" else "red"
        st.markdown(f"<h2 style='color:{player_color};'>Player {st.session_state.current_player}'s turn</h2>", unsafe_allow_html=True)
    else:
        # Display game result
        winner = check_winner(st.session_state.board)
        if winner:
            winner_color = "blue" if winner == "X" else "red"
            st.markdown(f"<h1 style='color:{winner_color};text-align:center;'>🏆 Player {winner} Wins! 🏆</h1>", unsafe_allow_html=True)
        else:
            st.markdown("<h1 style='color:gray;text-align:center;'>😲 It's a Tie! 😲</h1>", unsafe_allow_html=True)
    
    # Display the game board
    board = st.session_state.board
    current_player = st.session_state.current_player
    game_over = st.session_state.game_over

    # If the game is still ongoing
    if not game_over:
        i, j = display_board(board)  # Display board and get clicked position

        # Process the move if a valid cell was clicked
        if i is not None and j is not None and board[i, j] == ' ' and not st.session_state.move_made:
            # Update board with player move
            board[i, j] = current_player
            st.session_state.move_made = True
            
            # Check if there is a winner
            winner = check_winner(board)
            if winner:
                st.success(f"🎉 Player {winner} wins!")
                st.session_state.game_over = True
                # Update score
                if winner == "X":
                    st.session_state.x_score += 1
                else:
                    st.session_state.o_score += 1
            elif ' ' not in board:  # Check for a tie
                st.warning("😲 It's a tie!")
                st.session_state.game_over = True
                st.session_state.ties += 1
            else:
                # Switch player turn
                current_player = 'O' if current_player == 'X' else 'X'
                st.session_state.current_player = current_player
                # Reset move_made flag for the next player's turn
                st.session_state.move_made = False

            st.session_state.board = board  # Update board in session state
            st.rerun()  # Force a rerun to update the UI
    else:
        # Still display the board when game is over
        display_board(board)

    # Reset game button
    if st.button("🔄 New Game"):
        st.session_state.board, st.session_state.current_player = Initialize_game()
        st.session_state.game_over = False
        st.session_state.turn += 1  # Change turn count to reset button states
        st.session_state.move_made = False
        st.rerun()  # Force a rerun to update the UI
        
    # Reset scores button
    if st.button("🔄 Reset Scores"):
        st.session_state.x_score = 0
        st.session_state.o_score = 0
        st.session_state.ties = 0
        st.rerun()  # Force a rerun to update the UI

# Run the app
if __name__ == "__main__":
    main()
