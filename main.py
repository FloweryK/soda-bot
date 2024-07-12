# colorama init
import colorama
colorama.init()

# env init
from dotenv import load_dotenv
load_dotenv('.env')

# imports
import emoji
from colorama import Fore
from tools import math
from core.brain import Brain
from core.tts.azure_tts import AzureTTS
from core.stt.realtime_stt import RealtimeSTT


def main():
    # brain
    tools = [math.multiply, math.add, math.exponentiate]
    brain = Brain(name='Soda', tools=tools, short_term_limit=10, verbose=False)

    # stt
    stt = RealtimeSTT(language="en")

    # tts
    tts = AzureTTS(
        language="en-US",
        voice="en-US-AshleyNeural",
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
            answer = brain.chat(question)
            print(f"\n{Fore.MAGENTA}Bot:{Fore.RESET} {answer}")

            # speak
            answer_filtered = emoji.replace_emoji(answer, replace='')
            tts.synthesize(answer_filtered)
        

if __name__ == "__main__":
    main()