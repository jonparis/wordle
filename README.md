# wordle

A python framework for evaluating automatic wordle solvers.

# Why?

There's a ton of people out there saying they have the optimal strategy. Prove it!

## How to use

Subclass the `Solver` class and implement the `make_a_guess()` method. The `Game` instance in the solver will have a list of guesses made so far. Each `Guess` instance has the guess raw string and also a "result" array telling you the evaluation of each character per the wordle gameplay rules/dynamic.

In main(), you can change the `Solver` instance to your solver and optionally change the number of times the solver is evaluated. Or you can call `evaluate_solver()` yourself with your `Solver` subclass. That function will basically just play the game `k` times with your `Solver` and tell you the score which will be the mean number of guesses your solver took (7 if it failed to guess the target word).
