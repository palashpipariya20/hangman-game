"""
Hangman - a terminal word guessing game for beginners.

How it works:
  1. Pick a category (Animals, Food, Technology, Nature or Mixed).
  2. A random secret word is chosen and shown as underscores.
  3. Guess one letter at a time. Wrong guesses draw the hangman.
  4. Type ? to see a hint (once per round).
  5. Win by revealing the whole word. Lose after 6 wrong guesses.

Only Python's standard library is used, so it runs on Replit as-is.
"""

import os
import random

# ---------------------------------------------------------------------------
# GAME DATA
# ---------------------------------------------------------------------------

MAX_WRONG = 6  # number of wrong guesses allowed before the player loses

# Each category maps to a list of (word, hint) pairs.
WORDS = {
    "Animals": [
        ("elephant", "The largest land animal."),
        ("giraffe", "It has a very long neck."),
        ("penguin", "A bird that cannot fly but swims well."),
        ("dolphin", "A smart sea mammal that clicks and whistles."),
        ("kangaroo", "It carries its baby in a pouch."),
        ("cheetah", "The fastest land animal."),
        ("octopus", "It has eight arms."),
        ("crocodile", "A large reptile with powerful jaws."),
    ],
    "Food": [
        ("pizza", "Round, cheesy and cut into slices."),
        ("burger", "A patty served inside a bun."),
        ("noodles", "Long strands, often eaten with chopsticks."),
        ("chocolate", "A sweet treat made from cocoa."),
        ("sandwich", "Filling between two slices of bread."),
        ("pancake", "A flat breakfast cake flipped in a pan."),
        ("biryani", "A spiced rice dish popular in South Asia."),
        ("avocado", "A green fruit used to make guacamole."),
    ],
    "Technology": [
        ("keyboard", "You type on it."),
        ("python", "A popular programming language (and a snake)."),
        ("internet", "A worldwide network connecting computers."),
        ("software", "Programs that run on a computer."),
        ("processor", "The 'brain' of a computer, also called the CPU."),
        ("battery", "Stores power for your phone or laptop."),
        ("algorithm", "A step-by-step set of instructions to solve a problem."),
        ("database", "An organized collection of stored data."),
    ],
    "Nature": [
        ("mountain", "A very high natural landform."),
        ("volcano", "A mountain that can erupt with lava."),
        ("rainbow", "Appears in the sky after rain and sunshine."),
        ("waterfall", "Water falling from a high place."),
        ("desert", "A very dry place with lots of sand."),
        ("glacier", "A huge, slow-moving river of ice."),
        ("thunder", "The loud sound that follows lightning."),
        ("forest", "A large area covered with trees."),
    ],
}

# "Mixed" combines every word from every category.
WORDS["Mixed"] = [pair for pairs in WORDS.values() for pair in pairs]

# Menu order: number -> category name.
CATEGORY_MENU = {
    "1": "Animals",
    "2": "Food",
    "3": "Technology",
    "4": "Nature",
    "5": "Mixed",
}

# The hangman drawing: one picture for each number of wrong guesses (0 to 6).
HANGMAN_PICS = [
    """
      +---+
      |   |
          |
          |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
          |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
      |   |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
     /|   |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
     /|\\  |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
     /|\\  |
     /    |
          |
    =========""",
    """
      +---+
      |   |
      O   |
     /|\\  |
     / \\  |
          |
    =========""",
]


# ---------------------------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------------------------

def clear_screen():
    """Clear the terminal so each turn looks fresh."""
    os.system("cls" if os.name == "nt" else "clear")


def choose_category():
    """Show the category menu and return the chosen category name."""
    print("Choose a category:")
    for number, name in CATEGORY_MENU.items():
        print(f"  {number}. {name}")

    while True:
        choice = input("Enter a number (1-5): ").strip()
        if choice in CATEGORY_MENU:
            return CATEGORY_MENU[choice]
        print("Invalid choice. Please type a number from 1 to 5.")


def get_masked_word(word, guessed_letters):
    """Return the word with unguessed letters hidden, e.g. 'p _ z z _'."""
    shown = [letter if letter in guessed_letters else "_" for letter in word]
    return " ".join(shown)


def draw_board(category, word, guessed_letters, wrong_letters, hint_text, message):
    """Clear the screen and print the whole game display."""
    clear_screen()
    print("=" * 36)
    print("          H A N G M A N")
    print("=" * 36)
    print(f"Category: {category}")
    print(HANGMAN_PICS[len(wrong_letters)])
    print()
    print("Word:  " + get_masked_word(word, guessed_letters))
    print()
    print(f"Wrong guesses ({len(wrong_letters)}/{MAX_WRONG}): "
          + (", ".join(sorted(wrong_letters)) if wrong_letters else "none"))
    if hint_text:
        print(f"Hint: {hint_text}")
    if message:
        print(f"\n{message}")
    print()


def get_valid_guess(guessed_letters, hint_used):
    """
    Ask for a guess until the player types something valid.
    Returns a single lowercase letter, or "?" if they want the hint.
    """
    while True:
        guess = input("Guess a letter (or ? for a hint): ").strip().lower()

        if guess == "?":
            if hint_used:
                print("You already used your hint this round.")
                continue
            return "?"
        if len(guess) != 1:
            print("Please enter exactly ONE letter.")
        elif not guess.isalpha() or not guess.isascii():
            print("Letters only (a-z). No numbers or symbols.")
        elif guess in guessed_letters:
            print(f"You already guessed '{guess}'. Try a different letter.")
        else:
            return guess


def play_round(category):
    """
    Play a single round of Hangman.
    Returns True if the player won, False if they lost.
    """
    word, hint = random.choice(WORDS[category])
    guessed_letters = set()  # every letter tried (right or wrong)
    wrong_letters = set()    # only the wrong ones
    hint_text = ""           # stays empty until the player asks
    hint_used = False
    message = f"The word has {len(word)} letters. Good luck!"

    # Keep going until the word is solved or the player runs out of lives.
    while len(wrong_letters) < MAX_WRONG:
        draw_board(category, word, guessed_letters, wrong_letters, hint_text, message)

        # Win check: every letter in the word has been guessed.
        if all(letter in guessed_letters for letter in word):
            break

        guess = get_valid_guess(guessed_letters, hint_used)

        if guess == "?":
            hint_text = hint
            hint_used = True
            message = "Hint revealed!"
            continue

        guessed_letters.add(guess)
        if guess in word:
            count = word.count(guess)
            message = f"Nice! '{guess}' appears {count} time(s)."
        else:
            wrong_letters.add(guess)
            message = f"Sorry, there is no '{guess}'."

    # The loop is over, so work out whether the player won or lost.
    won = all(letter in guessed_letters for letter in word)
    draw_board(category, word, guessed_letters, wrong_letters, hint_text, "")
    if won:
        print(f"*** YOU WIN! The word was '{word.upper()}'. ***")
    else:
        print(f"*** GAME OVER! The word was '{word.upper()}'. ***")
    return won


def ask_play_again():
    """Ask the player whether to play another round. Returns True or False."""
    while True:
        answer = input("\nPlay again? (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please type y or n.")


# ---------------------------------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------------------------------

def main():
    """Run the game loop and keep track of session statistics."""
    rounds_played = 0
    wins = 0

    clear_screen()
    print("Welcome to HANGMAN!")
    print(f"Guess the secret word before you make {MAX_WRONG} wrong guesses.\n")

    while True:
        category = choose_category()
        won = play_round(category)

        rounds_played += 1
        if won:
            wins += 1

        print(f"\nSession score: {wins} win(s) in {rounds_played} round(s) "
              f"({rounds_played - wins} loss(es)).")

        if not ask_play_again():
            break
        clear_screen()

    print(f"\nThanks for playing! Final score: {wins}/{rounds_played} won.")


# This makes the game start only when you run this file directly.
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C or closed input: exit politely instead of showing an error.
        print("\n\nGame ended. Goodbye!")
