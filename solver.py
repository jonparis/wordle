from abc import ABC, abstractmethod
from random import choice as random_choice, sample
from wordle import Game, WORDS


class Solver(ABC):
    def __init__(self, game):
        self.game = game

    @abstractmethod
    def make_a_guess(self):
        """
        The game will ask the solver to make a guess (string) over and over until it wins or loses.
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


class LarsSolver(Solver):
    """
    Lars came up with an analysis on a table strategy cf. https://www.facebook.com/lars/posts/10159740204907566
    """

    def make_a_guess(self):
        if len(self.game.guesses) == 0:
            # First guess will always be REAST
            return "reast"


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
