#Task 4

def make_hangman(secret_word):
    guesses = []

    def hangman_closure(letter):
        guesses.append(letter.lower())

        display = ""
        for char in secret_word:
            if char.lower() in guesses:
                display += char
            else:
                display += "_ "
        print(display)

        return all(char.lower() in guesses for char in secret_word)
    return hangman_closure

if __name__ == "__main__":
    secret = input("Enter the secret word: ")
    game = make_hangman(secret)

    print("\nLet's start the Hangman game!\n")

    finished = False
    while not finished:
        guess = input("Guess a letter: ").strip().lower()
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter.")
            continue
        finished = game(guess)

    print("\nCongratulations! You've guessed the word!")
    