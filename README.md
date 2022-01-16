# wordle

A python framework for evaluating automatic wordle solvers.

## Why?

There's a ton of people out there saying they have the optimal strategy. Prove it!

## How to use

Subclass the `Solver` class and implement the `make_a_guess()` method. The `Game` instance in the solver will have a list of guesses made so far. Each `Guess` instance has the guess raw string and also a "result" array telling you the evaluation of each character per the wordle gameplay rules/dynamic. There are also a couple of callbacks that you can override (see `Solver` class for explanations).

If you want to just play via CLI, just run:

```
python3 play.py
```

If you want to evaluate your solver, do something like this in the python cli:

```
from solver import evaluate_solver, AbeSolver
evaluate_solver(AbeSolver, k=10000)
```

The result will be `k` games played using your Solver, and the result of the function is the average number of guesses your solver took to win. Example screenshot:

![evaluate_solver() example screenshot](/images/evaluate_solver_example.png "evalute_solver() example")
