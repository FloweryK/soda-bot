# env
from dotenv import load_dotenv
load_dotenv('.env')

# colorma
import colorama
from colorama import Fore
colorama.init()

# imports
from bot import Bot
from tools import math
from utils.tts import TTS
from utils.stt import AudioToTextRecorder


def main():
    # define bot
    tools = [math.multiply, math.add, math.exponentiate]
    bot = Bot(name='Soda', tools=tools, short_term_limit=10, verbose=False)

    # stt & tts
    stt = AudioToTextRecorder(language="en")
    tts = TTS()

    # chat
    while True:
        # question
        print(f"{Fore.CYAN}You:{Fore.RESET} ", end='')
        question = stt.text()
        print(question)

        if question:
            # answer
            answer = bot.chat(question)
            print(f"{Fore.MAGENTA}Bot:{Fore.RESET} {answer}")

            # speak
            tts.synthesize(answer)
        


if __name__ == "__main__":
    main()