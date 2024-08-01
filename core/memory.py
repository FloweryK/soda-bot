import os
import pickle
from datetime import datetime


def format_message(message):
    return f"[{message['datetime']}] [{message['role']}] {message['text']}" + f" ({message['emotions']})" if message['emotions'] else ""


class Memory:
    def __init__(self, save_dir, short_term_limit):
        # configs
        self.short_term_limit = short_term_limit

        # chat history manager
        self.path_today = None
        self.previous_messages = []
        self.current_messages = []
        self.initialize_messages(save_dir)

        # current context
        self.contexts = None
    
    def initialize_messages(self, save_dir):
        # set today's save path
        self.path_today = os.path.join(save_dir, datetime.now().strftime("%Y%m%d")) + '.pickle'

        # load previous messages
        for file_name in sorted(os.listdir(save_dir)):
            if file_name.endswith('.pickle'):
                file_path = os.path.join(save_dir, file_name)
                if file_path != self.path_today:
                    with open(file_path, 'rb') as f:
                        self.previous_messages.extend(pickle.load(f))
        
        # load current messages
        if os.path.exists(self.path_today):
            with open(self.path_today, 'rb') as f:
                self.current_messages += pickle.load(f)
        
        # add a system message for a new conversation
        self.add_message('SYSTEM', 'A NEW CHAT STARTED', None, is_save=False)

    def get_chat_history(self):
        chat_history = self.previous_messages + self.current_messages
        return '\n'.join(format_message(message) for message in chat_history)
    
    def add_message(self, role, text, emotions, is_save=True):
        self.current_messages.append({
            'datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'role': role,
            'text': text,
            'emotions': emotions
        })

        # save
        if is_save:
            with open(self.path_today, 'wb') as f:
                pickle.dump(self.current_messages, f)
