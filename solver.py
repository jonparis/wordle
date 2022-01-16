from abc import ABC, abstractmethod
from random import choice as random_choice, sample
from wordle import Game, Guess, WordGuessCharPositionalResult, WORDS


class Solver(ABC):
    def __init__(self, game):
        self.game = game

    @abstractmethod
    def make_a_guess(self):
        """
        The game will ask the solver to make a guess (string) over and over until it wins or loses.
        """

        pass

    def on_guess_processed(self, guess):
        """
        The game will call a callback on the solver after a guess is processed with the Guess instance.
        """

        pass

    def on_end(self):
        """
        Upon the game ending, the solver will get a callback.
        """

        pass


class RandomSolver(Solver):
    def make_a_guess(self):
        return random_choice(WORDS)


class CLISolver(Solver):
    def make_a_guess(self):
        if self.game.god_mode:
            return input(f"THE SOLUTION IS {self.game._target_word}. You have as many guesses left as you want.").strip().lower()

        return input(f"{self.game.MAX_NUM_GUESSES - self.game.num_guesses_taken} guesses left. Please make a guess....").strip().lower()

    def on_end(self):
        if self.game.won:
            print(
                f"Congrats! You got the word in {self.game.num_guesses_taken} guesses.")
        else:
            print(
                f"Sorry, you are out of guesses. The correct word was '{self.game._target_word}'")


class AbeSolver(Solver):
    def __init__(self, game):
        super().__init__(game)
        self.characters_that_are_in_target_word = set([])
        self.characters_that_are_not_in_target_word = set([])
        self.positional_characters = [None for _ in range(len(WORDS[0]))]
        self.guessed_words = set([])

    def on_guess_processed(self, guess):
        self.guessed_words.add(guess.guess)

        for i in range(len(guess.guess)):
            guess_result = guess.guess_result[i]
            c = guess.guess[i]
            if guess_result == WordGuessCharPositionalResult.CORRECT:
                self.characters_that_are_in_target_word.add(guess.guess[i])
                self.positional_characters[i] = c
            elif guess_result == WordGuessCharPositionalResult.IN_WORD:
                self.characters_that_are_in_target_word.add(guess.guess[i])
            else:
                self.characters_that_are_not_in_target_word.add(guess.guess[i])

    def make_a_guess(self):
        # 1. First, we filter words since we might know about positional characters and also
        #    if certain characters are definitely not in the word.
        filtered_words = []
        filter_words_that_dont_have_known_chars = len(
            self.characters_that_are_in_target_word) > 0
        for word in WORDS:
            char_set = {c for c in word}
            if filter_words_that_dont_have_known_chars:
                # The word must have every known char in the target word.
                if len(self.characters_that_are_in_target_word - char_set) > 0:
                    continue

            # If the word has a wrong positional character, do not add it.
            # Also, if the word has a char that we know is not in the target word, do not add it.
            has_wrong_positional_char = False
            has_character_that_is_not_in_target_word = False
            for i in range(len(word)):
                c = word[i]

                if self.positional_characters[i] is not None and c != self.positional_characters[i]:
                    has_wrong_positional_char = True
                    break

                if c in self.characters_that_are_not_in_target_word:
                    has_character_that_is_not_in_target_word = True
                    break

            if has_wrong_positional_char or has_character_that_is_not_in_target_word:
                continue

            filtered_words.append(word)

        # 2. Calculate the adjusted frequency of every letter within filtered_words.
        denominator = 0.0

        for word in filtered_words:
            for c in word:
                denominator += 1.0

        count_map = {}
        for word in filtered_words:
            for c in word:
                if c not in count_map:
                    count_map[c] = 0.0
                count_map[c] += 1.0

        # A map of position to a map of character to frequency.
        frequency_map = {}
        for word in filtered_words:
            for c in word:
                if c not in frequency_map:
                    frequency_map[c] = 0.0

                frequency_map[c] = count_map[c] / \
                    denominator if denominator > 0.0 else 0.0

        # Now, go through every word and calculate the "coverage". Give back the word with the max.
        ret = None
        max_coverage = -1.0
        for word in filtered_words:
            if word in self.guessed_words:
                continue

            coverage = sum([frequency_map[c] for c in set([c for c in word])])
            if coverage > max_coverage:
                ret = word
                max_coverage = coverage

        return ret


def evaluate_solver(solver_klass, k):
    """
    Play the game k times. The overall score will simply be the mean score(i) for all k games,
    where score(i) = num_guesses_taken if won else MAX_NUM_GUESSES + 1 (so lower is better).
    """

    assert k > 0
    k = min(len(WORDS), k)
    shuffled_words = sample(WORDS, k)

    score_sum = 0
    for i in range(k):
        print(
            f"Evaluating solver iteration {i}, target word = {shuffled_words[i]}...")
        game = Game(target_word=shuffled_words[i])
        game.play(solver_klass(game))
        if game.won:
            print(
                f"Solver won in {game.num_guesses_taken} guesses. The word was {game._target_word}")
        else:
            print(f"Solver lost. The word was {game._target_word}")

        score_sum += game.num_guesses_taken if game.won else game.MAX_NUM_GUESSES + 1

    return float(score_sum) / float(k)
