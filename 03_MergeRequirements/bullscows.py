import argparse
import pathlib
from typing import Tuple
import urllib.request
import cowsay
import random


def bullscows(guess: str, secret: str) -> Tuple[int, int]:
    bulls, cows = 0, 0
    for guess_c, secret_c in zip(guess, secret):
        if guess_c == secret_c:
            bulls += 1
        elif guess_c in secret:
            cows += 1
    return (bulls, cows)


def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    secret = random.choice(words)
    bulls = 0
    tries = 0
    cowfile = cowsay.get_cow("flying", f"{pathlib.Path(__name__).parent}")
    while bulls != len(secret):
        guess = ask(
            cowsay.cowsay("Введите слово: ", cowfile=cowfile)
            + "\n",
            words,
        )
        tries += 1
        bulls, cows = bullscows(guess, secret)
        inform("Быки: {}, Коровы: {}", bulls, cows)
    print(tries)


def _ask_impl(prompt: str, valid: list[str] = None) -> str:
    valid_guess = False
    while not valid_guess:
        print(prompt, end="")
        guess = input().strip()
        valid_guess = not valid or guess in valid
    return guess


def _inform_impl(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))


if __name__ == "__main__":
    parser = argparse.ArgumentParser("bullscows")
    parser.add_argument("dictionary", type=str)
    parser.add_argument("length", type=int, nargs="?", default=5)
    args = parser.parse_args()
    dictionary_file = pathlib.Path(args.dictionary)
    if dictionary_file.exists() and dictionary_file.is_file():
        with open(args.dictionary, "r") as file:
            words = [word.strip() for word in file.readlines()]
    else:
        # Try to download dictionary
        with urllib.request.urlopen(args.dictionary) as file:
            words = [word.decode().strip() for word in file.readlines()]
    words = [word for word in filter(lambda word: len(word) == args.length, words)]
    if len(words):
        gameplay(_ask_impl, _inform_impl, words)
