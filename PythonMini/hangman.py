class HangmanGame:
    def __init__(self,word):
        self._secret_word=word
        self._guesses_left=6
        self._guessed_letters=set([])
        print("New Hangman game started!")

    def display_word(self):
        ans=""
        length=len(self._secret_word)
        count=0
        for ch in self._secret_word:
            count+=1
            if ch in self._guessed_letters:
                ans+=ch
            else:
                ans+="_"
            if count!=length:
                ans+=" "
        
        return ans

    def make_guess(self,letter):
        if letter in self._guessed_letters:
            print("You already guessed that letter.")
            return
        else:
            self._guessed_letters.add(letter)
            if letter in self._secret_word:
                print("Good guess!")
            else:
                self._guesses_left-=1
                print(f"Wrong guess. {self._guesses_left} guesses left.")

    def display_game_status(self):
    
        guessed = ', '.join(sorted(self._guessed_letters)) if self._guessed_letters else "None"
        print(f"Guesses Left: {self._guesses_left} | Guessed Letters: {guessed}")


    def is_game_over(self):
        to_return=True
        if self._guesses_left==0:
            print("You've run out of guesses.Game Over!")
            return True
        for ch in self._secret_word:
            if ch not in self._guessed_letters:
                to_return=False
            else:
                continue
        if(to_return):
            print("Congratulations! You've guessed the word.")
        return to_return

    def reveal_word(self):
        return f"The word was: {self._secret_word}"

    def has_already_guessed(self,letter):
        if letter in self._guessed_letters:
            return True
        return False

    def play(self):
        while not self.is_game_over():
            print("\n"+self.display_word())
            guess=input("Enter a letter: ").lower()
            if len(guess)!=1 or not guess.isalpha():
                print("Invalid input. Please enter a single alphabet.")
                continue
            self.make_guess(guess)
            self.display_game_status()
        print(self.reveal_word())

    
