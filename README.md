# Mastermind
#### (https://en.wikipedia.org/wiki/Mastermind_(board_game))

#### Github repository: https://github.com/piotrusin/pk-2020-jezyki-symboiczne-mastermind

### Task description
* ~~Window with 4-digit text box, answer list, button
"Check" button "Cheater!" and the “Reset” button.~~
A window with a 4x12 ball game board (answers) and next to each row of balls, additional 4 balls for feedback. The whole thing was created as a real Mastermind board game.
* A random number (code) consisting of four digits from 1 is generated when the game starts
up to and including 6 (1111, 1112, 1113, …, 3455, 3456, 3461, 3462, …, 6665, 6666).
* ~~The player enters four numbers from 1 to 6 into the text box and presses
"Check" button.~~ The player selects four numbers, from 1 to 6, using the keyboard. SPACEBAR changes the active cell of the row, numbers 1-6 change the selection in the cell, and the ENTER key checks the current row.
* The answer containing: the entered number is added to the answer field
by the player, the number of digits in correct positions, and the number of digits present
in the code, but in the wrong positions.
* If the player has typed in a code number, a ~~window with is displayed
"WIN".~~ text that says "YOU WON" and the correct combination is displayed. Pressing R restarts the game.
* If the player has not guessed the code after 12 tries, ~~a window with is displayed
"Lost" text is displayed.~~ text is displayed with the words "YOU LOSE" followed by the correct combination. Pressing R restarts the game.
* The logic of the game should be implemented by a separate class, inheriting from the class
Game rules. The second class should also be disinherited from the RegulyGry class
class, generating incorrect answers. The rule set selection should be
done randomly before each game.
* If the player pressed the "Cheat!" with the correct rules of the game, the program
should display a window that says "Tere fere." and the drawn code.
* If the player pressed the "Cheat!" with incorrect rules of the game,
the program should display a window saying, "You caught me!"

### Tests
1. Displaying (printing in the console) the random code, entering the answer z
incorrect digits - expected information about the lack of correct matches.
2. Displaying the drawn code, entering the answer with correct numbers in
the wrong places - expected information about an incorrect location.
3. Displaying the random code, entering the answer with two correct 
digits in the right places and two correct ones in the wrong places -
expected information about two hits and two wrong positions.
4. Displaying the drawn code, entering the correct answer -
expected win information.
5. Entering an incorrect code 12 times - expected information about the loss
6. Attempt to enter an incorrect code into the answer field (less or more than 4
characters, characters that are not numbers from 1 to 6) - expected code not recognized (the player
does not lose a turn).
7. Pressing the "Cheat" button with the correct rules of the game -
expected information "tere fere".
8. Pressing the "Cheat" button with incorrect game rules -
expected information about cheating by the computer.
9. Entering 10 codes, resetting the game, entering 5 codes - expected
normal game operation (does the turn counter reset after pressing “Reset”)
