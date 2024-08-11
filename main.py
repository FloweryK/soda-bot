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


def update_and_print(new_value, old_value, label):
    if new_value:
        if isinstance(new_value, dict):
            print(str(new_value)[len(str(old_value))-1:-1], end='')
        elif isinstance(new_value, str):
            print(new_value[len(old_value):], end='')
        else:
            raise TypeError("Unimplemented input type:", new_value, type(new_value))
    else:
        print(f"{label}", end='')

    return new_value


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
        if question:
            text = ''
            emotions = {}
            contexts = ''

            for s in brain.stream(question):
                if 'text' in s:
                    text = update_and_print(s['text'], text, f"{Fore.MAGENTA}Bot:{Fore.RESET} ")
                if 'emotions' in s:
                    emotions = update_and_print(s['emotions'], emotions, '\n\temotions -> ')
                if 'contexts' in s:
                    contexts = update_and_print(s['contexts'], contexts, '\n\tcontexts -> ')
            print()

            # add to chat history
            brain.add_chat_history(question, text, emotions, contexts)

            # create tts from the response
            if config.TTS_ON:
                text = emoji.replace_emoji(text, replace='')
                tts.synthesize(text)


if __name__ == "__main__":
    main()