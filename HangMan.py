
import tkinter as tk
import random

WORDS = [
    "python", "julgran", "teater", "mamma", "present", "snöflinga",
    "tomte", "ren", "pepparkaka", "lampor"
]

MAX_WRONG_GUESSES = 6

class HangmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman")

        self.secret_word = ""
        self.guessed_letters = set()
        self.wrong_guesses = 0

        # Top frame: word display
        self.word_label = tk.Label(root, text="", font=("Helvetica", 24))
        self.word_label.pack(pady=10)

        # Middle: hangman drawing (text style)
        self.hangman_label = tk.Label(root, text="", font=("Courier", 16), justify="left")
        self.hangman_label.pack(pady=5)

        # Info label
        self.info_label = tk.Label(root, text="", font=("Helvetica", 12))
        self.info_label.pack(pady=5)

        # Letters guessed
        self.guessed_label = tk.Label(root, text="", font=("Helvetica", 12))
        self.guessed_label.pack(pady=5)

        # Entry + button
        entry_frame = tk.Frame(root)
        entry_frame.pack(pady=10)

        tk.Label(entry_frame, text="Gissa en bokstav:").pack(side=tk.LEFT, padx=5)
        self.entry = tk.Entry(entry_frame, width=3, font=("Helvetica", 14))
        self.entry.pack(side=tk.LEFT)
        self.entry.bind("<Return>", lambda event: self.guess_letter())

        self.guess_button = tk.Button(entry_frame, text="Gissa", command=self.guess_letter)
        self.guess_button.pack(side=tk.LEFT, padx=5)

        # Restart button
        self.restart_button = tk.Button(root, text="Nytt spel", command=self.new_game)
        self.restart_button.pack(pady=10)

        self.new_game()

    def new_game(self):
        self.secret_word = random.choice(WORDS).lower()
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.update_word_display()
        self.update_hangman_display()
        self.info_label.config(text=f"Du har {MAX_WRONG_GUESSES} försök.")
        self.guessed_label.config(text="Gissade bokstäver: -")
        self.entry.delete(0, tk.END)
        self.entry.config(state=tk.NORMAL)
        self.guess_button.config(state=tk.NORMAL)

    def update_word_display(self):
        display = " ".join(
            letter if letter in self.guessed_letters else "_"
            for letter in self.secret_word
        )
        self.word_label.config(text=display)

    def update_hangman_display(self):
        stages = [
            "",
            "  O",
            "  O\n  |",
            "  O\n /|",
            "  O\n /|\\",
            "  O\n /|\\\n /",
            "  O\n /|\\\n / \\",
        ]
        self.hangman_label.config(text=stages[self.wrong_guesses])

    def guess_letter(self):
        guess = self.entry.get().lower().strip()
        self.entry.delete(0, tk.END)

        if len(guess) != 1 or not guess.isalpha():
            self.info_label.config(text="Skriv EN bokstav (a–z).")
            return

        if guess in self.guessed_letters:
            self.info_label.config(text="Den bokstaven har du redan gissat.")
            return

        self.guessed_letters.add(guess)

        if guess in self.secret_word:
            self.info_label.config(text=f"Rätt! '{guess}' finns i ordet.")
        else:
            self.wrong_guesses += 1
            self.info_label.config(
                text=f"Fel! Du har {MAX_WRONG_GUESSES - self.wrong_guesses} försök kvar."
            )

        self.update_word_display()
        self.update_hangman_display()
        self.guessed_label.config(
            text="Gissade bokstäver: " + " ".join(sorted(self.guessed_letters))
        )

        # Check win
        if all(letter in self.guessed_letters for letter in self.secret_word):
            self.info_label.config(text=f"Grattis! Du vann. Ordet var '{self.secret_word}'.")
            self.entry.config(state=tk.DISABLED)
            self.guess_button.config(state=tk.DISABLED)

        # Check lose
        if self.wrong_guesses >= MAX_WRONG_GUESSES:
            self.info_label.config(text=f"Du förlorade! Ordet var '{self.secret_word}'.")
            self.entry.config(state=tk.DISABLED)
            self.guess_button.config(state=tk.DISABLED)

