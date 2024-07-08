from bot import Bot
from tools import math

import colorama
from colorama import Fore
colorama.init()



def main():
    # define bot
    tools = [math.multiply, math.add, math.exponentiate]
    bot = Bot(name='Soda', tools=tools, verbose=True)


    # chat
    while True:
        # question
        print(f"{Fore.CYAN}You:{Fore.RESET} ", end='')
        question = input()

        # answer
        answer = bot.chat(question)
        print(f"{Fore.MAGENTA}Bot:{Fore.RESET} {answer}")


if __name__ == "__main__":
    main()