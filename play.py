#!/usr/bin/python3

from solver import CLISolver
from wordle import Game

def play_game():
    game = Game()
    game.play(CLISolver(game))

    play_again = input("Play again (y/n)? ").strip().lower()
    if "y" == play_again:
        play_game()
    else:
        print("Bye!")


if __name__ == '__main__':
    play_game()