import random
import streamlit as st
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# BUG FIX: Detect when the player changes difficulty mid-session.
#
# (1) Bug this fixes:
#     The secret number was generated only once on first load and never
#     regenerated when the difficulty selectbox changed. Switching to "Easy"
#     (range 1–20) still kept a secret that could be 79 — outside the new range.
#
# (2) How the previous code was affected:
#     The guard `if "secret" not in st.session_state` ran exactly once. After
#     that, `secret` existed in session state forever, so every subsequent
#     Streamlit rerun (including difficulty changes) skipped regeneration
#     entirely. The displayed range in the sidebar updated, but the secret did
#     not, making the game unwinnable or trivially easy depending on the value.
#
# (3) Expected behavior:
#     Whenever the player picks a different difficulty, the secret is immediately
#     re-rolled within the correct range for that difficulty, attempts and
#     history are reset, and a fresh game begins automatically.
difficulty_changed = st.session_state.get("current_difficulty") != difficulty

if "secret" not in st.session_state or difficulty_changed:
    st.session_state.secret = random.randint(low, high)
    st.session_state.current_difficulty = difficulty
    st.session_state.attempts = 1
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []

if "attempts" not in st.session_state:
    st.session_state.attempts = 1

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    low, high = get_range_for_difficulty(difficulty) # BUG FIX: Previously, it was hard-coded to (1, 100). Changing it to low, high, uses the previous range, therefore we must recalculate here. 
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high) # BUG FIX: Previously, it was hard-coded to (1, 100). Tying it back to the previous logic with low, high predeclared variable
    st.session_state.status = "playing" # BUG FIX: Previously, the status was not reset to "playing" when starting a new game, which could cause the game to be stuck in a "won" or "lost" state.
    st.session_state.history = [] # BUG FIX: Previously, the history was not reset when starting a new game, which could cause confusion with previous guesses being displayed.
    st.session_state.current_difficulty = difficulty # BUG FIX: Previously, the current_difficulty was not updated when starting a new game, which could cause the game to be stuck in a previous difficulty state.
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        # BUG FIX: Previously, the secret was passed as a string to check_guess if attempts were % 2 , which caused incorrect comparisons. I've completely removed that logic
        secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
