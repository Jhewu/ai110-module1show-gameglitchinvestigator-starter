# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it? **(TF Skipped)**
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

**Bugs**
- After the game launches, the logic automatically pre-generates a "secret" number to guess. But when you select difficulty to "easy," it should update the "secret" number to range `1` to `20`, instead it's still stuck at `79`. Expected behavior, should change the "secret" number to the expected range (from all difficulty selections) **[FIXED & CONFIRMED]**
- After utilizing all the attempts and clicking "New Game," the game resets the "Attempt left: x" front-facing counter, but the player is unable to submit new request. It seems like the game state is locked after finishing. Expected behavior, game should reset and player should be able to submit new guesses. **[FIXED & CONFIRMED]**
- The hint is incorrectly implemented. Expected behavior is the hint will be calculated based on the guess and the secret number, whether it's "Go Lower" or "Go Higher," instead it always says "Go Lower." **[FIXED & CONFIRMED]**
- In the Developer Debug Info, when "New Game" is pressed, the history is not reset. Expected behavior is that the history should be reset for every game, otherwise, the program will have a growing history stack across all games. **[FIXED & CONFIRMED]**
- In the Developer Debug Info, "Attempts" does not register until the first "Submit Guess." Expected behavior, it should register on the first "Submit Guess." 
- In the Developer Debug Info, a "History" entry does not register after a "Submit Guess." Instead what happens is the current guess is stored off-screen and added when the player press "Submit Guess" again. Expected behavior should be it would add it to the history stack right away.
- Difficulty range, should be linear. Currently, easy is (1, 20), normal is (1, 100), and hard is (1, 50). Instead normal should be swapped with hard **[FIXED & COMPLETED]**
- The check_guess function has an intentional quirk that carries over from app.py — on even-numbered attempts, the caller passes secret as a str instead of an int (app.py:192-195). This causes string comparison ("9" > "79" is True because "9" > "7" lexicographically), which can produce incorrect hints. This appears to be one of the intentional "glitches" in the game, so it's preserved as-is — but if you ever want the game to behave correctly on all attempts, the str(secret) branch in app.py should be removed **[FIXED & COMPLETED]**

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)? 

  Claude Code

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

  Most of it was correct. Claude was able to identify a quirky behavior of the code where it will pass a str to check_guess() if the guess was even, which I did not notice. It was definitively useful as a "reviewer" as well. 


- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

  Since I am using Claude Code on a relatively small project, Claude Code was actually pretty good and did not give me misleading or incorrect information
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed? 

  Test it manually through UI. Use Pytest created by Claude to see if behavior works as expected. 

- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.

  One bug I tackled is the New Game not rerunning streamlit. I basically tested if the bug was fixed by using all attempts and see if I can still play after clicking on "New Game" 

- Did AI help you design or understand any tests? How? **(TF Skippped)**

  Claude Code fixed the previous pytest that were incorrectly set up.... 

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app. 

  Bug 1: New Game resets to wrong range (ignores difficulty)
  Bug 2: The secret number changes meaning every other guess because of this behavior: 

  if st.session_state.attempts % 2 == 0:
    secret = str(st.session_state.secret)   # even attempts: string
  else:
    secret = st.session_state.secret         # odd attempts: integer

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

  Basically, streamlit works by "re-rendering" the UI every time there's an event. Status variables from streamlit is stateless while local variables change from each render. 

- What change did you make that finally gave the game a stable secret number?

  I updated the New Game logic with a state to track the difficulty change. I also removed the conditional block to check if the number was even, and ensure the parameter for check_guess() are always casted to int

---

## 5. Looking ahead: your developer habits (TF Skipped)

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

## 6. TF ONLY - Draft a short guiding hint they would give a student

If you've never worked with streamlit, it operates on an event basis. Whenever python detects an event, it reruns streamlit. Streamlit keeps two different variables, stateless variables and local variables. Do asks Claude to further explain Streamlit for beginners. 
