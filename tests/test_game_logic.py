from logic_utils import check_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    # BUG FIX: check_guess returns a tuple (outcome, message). Previously,
    # the result was compared directly as `result == "Win"`, which always
    # failed because a tuple is never equal to a string. Fixed by unpacking
    # the tuple — outcome holds the result string, _ discards the message.
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    # BUG FIX: same tuple-unpacking fix as test_winning_guess above.
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    # BUG FIX: same tuple-unpacking fix as test_winning_guess above.
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

def test_string_inputs_are_handled():
    # Passing str values should produce the same outcomes as int values
    # since check_guess now casts both arguments to int internally
    outcome_win, _ = check_guess("50", "50")
    assert outcome_win == "Win"

    outcome_high, _ = check_guess("60", "50")
    assert outcome_high == "Too High"

    outcome_low, _ = check_guess("40", "50")
    assert outcome_low == "Too Low"
