import os
import pickle
from datetime import datetime


def format_message(message):
    text = f"[{message['datetime']}] [{message['role']}] {message['text']}"
    if message['emotions']:
        text += f" ({message['emotions']})"
    return text


class Memory:
    def __init__(self, save_dir, short_term_limit):
        # configs
        self.short_term_limit = short_term_limit

        # chat history fs
        path_prefix = os.path.join(save_dir, datetime.now().strftime("%Y%m%d"))
        self.path_pickle = path_prefix + '.pickle'
        self.path_txt = path_prefix + '.txt'

        # chat history manager
        self.previous_messages = []
        self.current_messages = []
        self.initialize_messages(save_dir)

        # current context
        self.contexts = None
    
    def initialize_messages(self, save_dir):
        # create save_dir
        os.makedirs(save_dir, exist_ok=True)

        # load previous messages
        for file_name in sorted(os.listdir(save_dir)):
            file_path = os.path.join(save_dir, file_name)

            if file_name.endswith('.pickle') and (file_path != self.path_pickle):
                with open(file_path, 'rb') as f:
                    self.previous_messages.extend(pickle.load(f))
        
        # load current messages
        if os.path.exists(self.path_pickle):
            with open(self.path_pickle, 'rb') as f:
                self.current_messages += pickle.load(f)

    def get_chat_history(self):
        chat_history = self.previous_messages + self.current_messages
        return '\n'.join(format_message(message) for message in chat_history)
    
    def add_message(self, role, text, emotions):
        self.current_messages.append({
            'datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'role': role,
            'text': text,
            'emotions': emotions
        })

        # save
        with open(self.path_pickle, 'wb') as f:
            pickle.dump(self.current_messages, f)
        with open(self.path_txt, 'w') as f:
            f.write(self.get_chat_history())
