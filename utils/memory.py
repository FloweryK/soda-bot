import datetime
from langchain_community.chat_message_histories import ChatMessageHistory


class ChatHistory(ChatMessageHistory):
    def add_ai_message_with_time(self, message):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S]")
        self.add_ai_message(f"[{now}] {message}")
    
    def add_user_message_with_time(self, message):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S]")
        self.add_user_message(f"[{now}] {message}")