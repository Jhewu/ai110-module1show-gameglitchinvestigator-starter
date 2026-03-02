def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    # BUG FIX: Previously, guess and secret were not converted to integers, which could cause incorrect comparisons if they were passed as strings. Now we ensure both are integers for accurate comparison.
    guess, secret = int(guess), int(secret)  # Ensure guess and secret are integers for comparison

    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        if guess > secret:
            # BUG FIX: was "📈 Go HIGHER!" — if guess is too high, player must go lower, not higher
            return "Too High", "📉 Go LOWER!"
        else:
            # BUG FIX: was "📉 Go LOWER!" — if guess is too low, player must go higher, not lower
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        # Fallback: secret was passed as a str (see caller), so compare as strings
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            # BUG FIX: same inversion as above — too high means go lower
            return "Too High", "📉 Go LOWER!"
        # BUG FIX: same inversion as above — too low means go higher
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
