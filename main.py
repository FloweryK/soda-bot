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
    # text
    result = f"{Fore.MAGENTA}Bot:{Fore.RESET} {text}"

    # emotions
    emotions = {key: f"{value:.1f}" for key, value in emotions.items()}
    result += f"\n(emotions: {emotions})"

    # contexts
    result += f"\n(contexts: {contexts})"
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
        save_dir=config.MEMORY_SAVE_DIR,
        short_term_limit=config.MEMORY_SHORT_TERM_LIMIT, 
    )

    # brain
    brain = Brain(
        llm=config.BRAIN_LLM,
        name=config.BRAIN_NAME, 
        prompt=config.BRAIN_PROMPT,
        emotions=config.BRAIN_EMOTIONS,
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
        # STT
        if config.STT_ON:
            print(format_user_message())
            question = stt.text()
            print(question, '\n')
        else:
            print(format_user_message(), end='')
            question = input()

        # LLM
        if question:
            # create a room for ai's messages
            text = ''
            emotions = {}
            contexts = ''
            print(format_ai_message(text, emotions, contexts))

            for s in brain.stream(question):
                # clear the room
                clear_previous_lines(n=3)

                # print the result
                text = s['text'] if 'text' in s else text
                emotions = s['emotions'] if 'emotions' in s else emotions
                contexts = s['contexts'] if 'contexts' in s else contexts
                print(format_ai_message(text, emotions, contexts))

            # add to chat history
            brain.add_chat_history(question, text, emotions, contexts)

            # TTS
            if config.TTS_ON:
                # speak
                text = emoji.replace_emoji(text, replace='')
                tts.synthesize(text)


if __name__ == "__main__":
    main()