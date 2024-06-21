from colorama import Fore
from bot import Bot
from tools import math


def main():
    # define bot
    tools = [math.multiply, math.add, math.exponentiate]
    bot = Bot(name='Soda', tools=tools, verbose=True)


    # chat
    while True:
        # question
        question = input(f"{Fore.CYAN}You:{Fore.RESET} ")

        # answer
        answer = bot.chat(question)
        print(f"{Fore.MAGENTA}Bot:{Fore.RESET} {answer}")


if __name__ == "__main__":
    main()