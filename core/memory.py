from datetime import datetime


class Memory:
    def __init__(self, short_term_limit):
        # configs
        self.short_term_limit = short_term_limit

        # chat history manager
        self.chat_history = []

        # current context
        self.contexts = None
    
    def add_message(self, role, text, emotions):
        self.chat_history.append({
            'datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'role': role,
            'text': text,
            'emotions': emotions
        })
    
    def get_chat_history(self):
        history = "\n"
        for message in self.chat_history:
            history += f"\n[{message['datetime']}] [{message['role']}] {message['text']}"
            history += f" ({message['emotions']})" if message['emotions'] else ""
        return history
