import emoji
import colorama
from colorama import Fore
from core.brain import Brain
from core.tts.azure_tts import AzureTTS
from core.stt.realtime_stt import RealtimeSTT
colorama.init()


class InterfaceCLI:
    def __init__(self, config):
        self.brain = Brain(
            config.BRAIN_LLM,
            config.BRAIN_NAME, 
            config.BRAIN_PROMPT,
            config.BRAIN_EMOTIONS,
            config.MEMORY_SAVE_DIR,
            config.MEMORY_SHORT_TERM_LIMIT
        )
    
        # stt
        self.stt = RealtimeSTT(
            language=config.STT_LANGUAGE
        ) if config.STT_ON else None

        # tts
        self.tts = AzureTTS(
            config.TTS_LANGUAGE,
            config.TTS_VOICE,
            config.TTS_RATE,
            config.TTS_PITCH
        ) if config.TTS_ON else None


    def run(self):
        def get_input():
            if self.stt:
                print()
                question = self.stt.text()
                print(question, '\n')
            else:
                question = input()
            return question
    
        def create_answer(question):
            # get ai's response to the question
            buffer = {}
            buffer_key = None
            keys_seen = set()

            for s in self.brain.chat(question, is_stream=True):
                for key, value in s.items():
                    if key not in keys_seen:
                        print(f"{Fore.MAGENTA}Bot:{Fore.RESET} " if key == "text" else f"\n\t{key} -> ", end="")
                        
                        # initialize buffer
                        buffer_key = key
                        buffer[key] = ""
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
                        print(value[len(buffer[key]):], end='')
                        buffer[key] = value
            print()
            return buffer['text']
        
        def create_tts(text):
            if self.tts:
                text = emoji.replace_emoji(text, replace='')
                self.tts.synthesize(text)

        while True:
            print(f"{Fore.CYAN}You:{Fore.RESET} ", end='')
            question = get_input()
            answer = create_answer(question)
            create_tts(answer)