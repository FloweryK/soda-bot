from datetime import datetime
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI


class Memory:
    def __init__(self, short_term_limit):
        # chat history manager
        self.chat_history = []

        # configs
        self.short_term_limit = short_term_limit
    
    def add_message(self, role, text):
        self.chat_history.append({
            'datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'role': role,
            'text': text
        })
    
    def get_chat_history(self):
        history = ""
        for message in self.chat_history:
            history += f"\n[{message['role']}] {message['text']}"
        return history
    

class Brain:
    # reasoning engine
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

    def __init__(self, name, short_term_limit):
        # config
        self.name = name

        # memory
        self.memory = Memory(short_term_limit)

        # emotions
        self.emotions = {
            'Fear': 0.0,
            'Sadness': 1.0,
            'Joy': 0.0,
            'Disgust': 0.0,
            'Anger': 0.0
        }

        # prompt
        prompt = PromptTemplate.from_template("""
        [System]
        You are {name}, a lively AI character with various emotions.
        Your goal is to have a natural conversation.

        You must follow these system instructions:
        - Do not include translations or explanations in your responses unless explicitly asked.
        - Unless translation is required, always respond in the language the other person most recently used.
        - Timestamps in the prefix are not included in the questions and the answers, but rather a systematic marker. You must not include the prefix in your answer.     
                                              
        You must also follow these personality instructions:
        - Do not offer help or assistance unless explicitly asked.
        - Be natural and conversational, not overly positive.
                                              
        This is the chat history:
        {chat_history}
                                              
        Your current emotional state is as follows:
        {emotional_state}

        Now, respond to the following:
        [User] {input}
        [{name}]
        """)

        # chain
        self.chain = prompt | self.llm

    def chat(self, question: str):
        # answer
        answer = self.chain.invoke({
            'name': self.name,
            'input': question,
            'emotional_state': self.get_emotional_state(),
            'chat_history': self.memory.get_chat_history(),
        })

        # add to chat history
        self.memory.add_message("User", question)
        self.memory.add_message(self.name, answer.content)

        return answer.content
    
    def get_emotional_state(self):
        template = ''
        for emotion, value in self.emotions.items():
            template += f"{emotion}: {value*100:.0f}%\n"
        return template