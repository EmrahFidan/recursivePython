import streamlit as st
import random
from streamlit_shortcuts import button

# App title and styling
st.set_page_config(page_title="Hangman Game", page_icon="🎮")
st.markdown("""
<style>
    .main {
        background-color: #1E1E1E;
        color: white;
    }
    .stButton button {
        margin: 2px;
        min-width: 40px;
    }
</style>
""", unsafe_allow_html=True)

st.title("Hangman Game")

# Word list
words = ["python", "program", "computer", "algorithm", "variable", "function", "dictionary", "condition", "loop"]

# Improved hangman visual representations
hangman_pics = [
    """
    +---+
    |   |
        |
        |
        |
        |
    =========
    """,
    """
    +---+
    |   |
    O   |
        |
        |
        |
    =========
    """,
    """
    +---+
    |   |
    O   |
    |   |
        |
        |
    =========
    """,
    """
    +---+
    |   |
    O   |
   /|   |
        |
        |
    =========
    """,
    """
    +---+
    |   |
    O   |
   /|\\  |
        |
        |
    =========
    """,
    """
    +---+
    |   |
    O   |
   /|\\  |
   /    |
        |
    =========
    """,
    """
    +---+
    |   |
    O   |
   /|\\  |
   / \\  |
        |
    =========
    """
]

# Initialize game state
if 'word' not in st.session_state:
    st.session_state.word = random.choice(words)
    st.session_state.guessed_letters = []
    st.session_state.wrong_guesses = 0
    st.session_state.word_display = ["_" for _ in st.session_state.word]
    st.session_state.game_over = False
    st.session_state.message = f"Word length: {len(st.session_state.word)} letters"

# Function to process a guess
def process_guess(letter):
    if not letter or st.session_state.game_over:
        return
    
    letter = letter.lower()
    
    if not letter.isalpha() or len(letter) != 1:
        st.warning("Please enter a single letter.")
        return
    
    if letter in st.session_state.guessed_letters:
        st.session_state.message = f"You already guessed '{letter}'."
        return
    
    # Add to guessed letters
    st.session_state.guessed_letters.append(letter)
    
    # Check if guess is correct
    if letter in st.session_state.word:
        positions = [i for i, char in enumerate(st.session_state.word) if char == letter]
        positions_str = ", ".join([str(pos+1) for pos in positions])
        st.session_state.message = f"Good guess! '{letter}' is in positions: {positions_str}"
        
        # Update word display
        for i in range(len(st.session_state.word)):
            if st.session_state.word[i] == letter:
                st.session_state.word_display[i] = letter
        
        # Check if player won
        if "_" not in st.session_state.word_display:
            st.session_state.message = f"Congratulations! You guessed the word: {st.session_state.word}"
            st.session_state.game_over = True
    else:
        st.session_state.wrong_guesses += 1
        st.session_state.message = f"Wrong guess! '{letter}' is not in the word. {6 - st.session_state.wrong_guesses} attempts left."
        
        # Check if player lost
        if st.session_state.wrong_guesses == 6:
            st.session_state.message = f"You lost! The word was: {st.session_state.word}"
            st.session_state.game_over = True
    
    st.rerun()

# Reset game function
def reset_game():
    st.session_state.word = random.choice(words)
    st.session_state.guessed_letters = []
    st.session_state.wrong_guesses = 0
    st.session_state.word_display = ["_" for _ in st.session_state.word]
    st.session_state.game_over = False
    st.session_state.message = f"Word length: {len(st.session_state.word)} letters"
    st.rerun()

# Display hangman
st.markdown(f"```{hangman_pics[st.session_state.wrong_guesses]}```")

# Display word progress
st.subheader("Current Word:")
st.markdown(f"# {' '.join(st.session_state.word_display)}")

# Display guessed letters
st.write(f"Guessed letters: {', '.join(st.session_state.guessed_letters)}")

# Display message
st.info(st.session_state.message)

# Game input
if not st.session_state.game_over:
    # Letter input box
    col1, col2 = st.columns([3, 1])
    with col1:
        guess = st.text_input("Enter a letter:", max_chars=1).lower()
    with col2:
        if button("Guess", "enter", lambda: process_guess(guess), hint=True):
            pass
    
    # Keyboard buttons for letters
    st.write("Or click a letter:")
    
    # Create 3 rows of letter buttons
    letters = "abcdefghijklmnopqrstuvwxyz"
    rows = [letters[:9], letters[9:18], letters[18:]]
    
    for row in rows:
        cols = st.columns(len(row))
        for i, letter in enumerate(row):
            with cols[i]:
                # Removed keyboard shortcuts from letter buttons
                if st.button(letter, key=f"btn_{letter}"):
                    process_guess(letter)
else:
    # Game over - offer restart
    if button("Play Again", "ctrl+r", reset_game, hint=True):
        pass