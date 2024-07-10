from datetime import datetime
from langchain_community.chat_message_histories import ChatMessageHistory


class Memory:
    def __init__(self, short_term_limit):
        # chat history manager
        self.chat_history = ChatMessageHistory()

        # configs
        self.short_term_limit = short_term_limit

    def add_ai_message_with_time(self, message):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.chat_history.add_ai_message(f"[{now}] {message}")
    
    def add_user_message_with_time(self, message):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.chat_history.add_user_message(f"[{now}] {message}")
    
    def get_short_term_memory(self):
        return self.chat_history.messages[-self.short_term_limit:]
        
