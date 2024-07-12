import emoji
import colorama
from colorama import Fore
from dotenv import load_dotenv
from bot import Bot
from tools import math
from utils.tts import AzureTTS
from utils.stt import RealtimeSTT


# intializations
load_dotenv('.env')
colorama.init()


def main():
    # bot
    tools = [math.multiply, math.add, math.exponentiate]
    bot = Bot(name='Soda', tools=tools, short_term_limit=10, verbose=False)

    # stt
    stt = RealtimeSTT(language="en")

    # tts
    tts = AzureTTS(
        language="en-US",
        voice_name="en-US-AshleyNeural",
        rate="+10.00%",
        pitch="+25.00%"
    )

    while True:
        # listen
        print(f"{Fore.CYAN}You:{Fore.RESET} ")
        question = stt.text()
        print(question)

        if question:
            # answer
            answer = bot.chat(question)
            print(f"\n{Fore.MAGENTA}Bot:{Fore.RESET} {answer}")

            # speak
            answer_filtered = emoji.replace_emoji(answer, replace='')
            tts.synthesize(answer_filtered)
        

if __name__ == "__main__":
    main()