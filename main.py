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
from core.memory import Memory
from core.tts.azure_tts import AzureTTS
from core.stt.realtime_stt import RealtimeSTT
import config


def main():
    # memory
    memory = Memory(
        short_term_limit=config.SHORT_TERM_LIMIT, 
    )

    # brain
    brain = Brain(
        llm=config.LLM,
        name=config.NAME, 
        emotions=config.EMOTIONS,
        memory=memory
    )

    # stt
    if config.STT_ON:
        stt = RealtimeSTT(
            language=config.STT_LANGUAGE
        )
    else:
        stt = None

    # tts
    if config.TTS_ON:
        tts = AzureTTS(
            language=config.TTS_LANGUAGE,
            voice=config.TTS_VOICE,
            rate=config.TTS_RATE,
            pitch=config.TTS_PITCH
        )
    else:
        tts = None


    while True:
        # listen
        if config.STT_ON:
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

            if config.TTS_ON:
                # speak
                answer_filtered = emoji.replace_emoji(answer, replace='')
                tts.synthesize(answer_filtered)


if __name__ == "__main__":
    main()