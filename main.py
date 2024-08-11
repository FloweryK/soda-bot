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


def format_user_message():
    return f"{Fore.CYAN}You:{Fore.RESET} "


def format_ai_message(text, emotions, contexts):
    emotions = {key: f"{value:.1f}" for key, value in emotions.items()}
    result = (
        f"{Fore.MAGENTA}Bot:{Fore.RESET} {text}\n"
        f"(emotions: {emotions})\n"
        f"(contexts: {contexts})"
    )
    return result


def clear_previous_lines(n=3):
    # Move the cursor up by 'n' lines
    print(f"\033[{n}A", end='')

    # Clear each line
    for _ in range(n):
        print("\033[K", end='')


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
        print(format_user_message(), end='')
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
            print(format_ai_message(text, emotions, contexts))

            for s in brain.stream(question):
                clear_previous_lines(n=3)
                text = s['text'] if 'text' in s else text
                emotions = s['emotions'] if 'emotions' in s else emotions
                contexts = s['contexts'] if 'contexts' in s else contexts
                print(format_ai_message(text, emotions, contexts))

            # add to chat history
            brain.add_chat_history(question, text, emotions, contexts)

            # create tts from the response
            if config.TTS_ON:
                text = emoji.replace_emoji(text, replace='')
                tts.synthesize(text)


if __name__ == "__main__":
    main()