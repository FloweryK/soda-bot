# colorama init
import colorama
colorama.init()

# env init
from dotenv import load_dotenv
load_dotenv('.env')

# imports
import emoji
from colorama import Fore
from core.brain import Brain
from core.tts.azure_tts import AzureTTS
from core.stt.realtime_stt import RealtimeSTT

# CONFIGS
BOT_NAME = 'Soda'
MEMORY_SHORT_TERM_LIMIT = 10
USE_STT = False
USE_TTS = False


def main():
    # brain
    brain = Brain(name=BOT_NAME, short_term_limit=MEMORY_SHORT_TERM_LIMIT)

    # stt
    if USE_STT:
        stt = RealtimeSTT(language="en")
    else:
        stt = None

    # tts
    if USE_TTS:
        tts = AzureTTS(
            language="en-US",
            voice="en-US-AshleyNeural",
            rate="+10.00%",
            pitch="+25.00%"
        )
    else:
        tts = None


    while True:
        # listen
        if USE_STT:
            print(f"{Fore.CYAN}You:{Fore.RESET} ")
            question = stt.text()
            print(question, '\n')
        else:
            print(f"{Fore.CYAN}You:{Fore.RESET} ", end='')
            question = input()

        if question:
            # answer
            answer = brain.chat(question)
            print(f"{Fore.MAGENTA}Bot:{Fore.RESET} {answer}")

            if USE_TTS:
                # speak
                answer_filtered = emoji.replace_emoji(answer, replace='')
                tts.synthesize(answer_filtered)
        

if __name__ == "__main__":
    main()