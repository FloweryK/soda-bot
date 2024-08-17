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
        config.MEMORY_SAVE_DIR,
        config.MEMORY_SHORT_TERM_LIMIT, 
    )

    # brain
    brain = Brain(
        config.BRAIN_LLM,
        config.BRAIN_NAME, 
        config.BRAIN_PROMPT,
        config.BRAIN_EMOTIONS,
        memory
    )

    # stt
    stt = RealtimeSTT(
        language=config.STT_LANGUAGE
    ) if config.STT_ON else None

    # tts
    tts = AzureTTS(
        config.TTS_LANGUAGE,
        config.TTS_VOICE,
        config.TTS_RATE,
        config.TTS_PITCH
    ) if config.TTS_ON else None


    while True:
        # get user's input as question
        print(f"{Fore.CYAN}You:{Fore.RESET} ", end='')

        if config.STT_ON:
            print()
            question = stt.text()
            print(question, '\n')
        else:
            question = input()

        # get ai's response to the question
        buffer_key = None
        buffer_value = ""
        keys_seen = set()

        for s in brain.chat(question, is_stream=True):
            for key, value in s.items():
                if key not in keys_seen:
                    print(f"{Fore.MAGENTA}Bot:{Fore.RESET} " if key == "text" else f"\n\t{key} -> ", end="")
                    buffer_key = key
                    buffer_value = ""
                    keys_seen.add(key)

                if key == buffer_key:
                    # parse value
                    if isinstance(value, str):
                        pass
                    elif isinstance(value, dict):
                        value = str(value)[1:-1]
                    else:
                        raise TypeError("Unsupported input type:", value, type(value))
                
                    # print and update
                    print(value[len(buffer_value):], end='')
                    buffer_value = value
        print()

        # create tts from the response
        if config.TTS_ON:
            text = emoji.replace_emoji(text, replace='')
            tts.synthesize(text)


if __name__ == "__main__":
    main()