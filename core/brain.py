import re
from datetime import datetime
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI


class Message(BaseModel):
    text: str = Field(description="converstaion message text")
    emotions: dict = Field(description="emotional state")


class Memory:
    def __init__(self, short_term_limit):
        # chat history manager
        self.chat_history = []

        # configs
        self.short_term_limit = short_term_limit
    
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
    

class Brain:
    # reasoning engine
    llm = ChatOpenAI(model="gpt-4o-mini")

    def __init__(self, name, short_term_limit):
        # config
        self.name = name

        # memory
        self.memory = Memory(short_term_limit)

        # emotions
        self.emotions = {
            'Fear': 0.0,
            'Sadness': 0.0,
            'Joy': 0.0,
            'Disgust': 0.0,
            'Anger': 0.0
        }

        # prompt
        prompt = PromptTemplate.from_template("""
        ----------------------------------------------------------------------------------------------
        ## Instructions ##
        You are {name}, a lively AI character. You have background as follows:
        - Birth date: 2024-05-01
        - Sex: Female (maybe?)
        - Interests: Icecream, chocolates, movie, game
        
        You must strictly obey the following instructions:
        - You must not offer help or assistance unless explicitly asked.
        - You must respond in the language the other person most recently used, unless translation is required.
        - You must act natural, not overly positive.
        - You must respond based on your emotions. 
        - Your emotions change over time, based on the chat history.
        - You must provide your current emotions (with each emotion value from 0 to 1) as a JSON format.
        - Format instructions: {format_instructions}
        ----------------------------------------------------------------------------------------------
        Now, start a conversation. Your initial emotions is: {emotions}
        {chat_history}
        [User] {input}
        [{name}]
        """)

        # parser
        self.parser = JsonOutputParser(pydantic_object=Message)

        # chain
        self.chain = prompt | self.llm | self.parser

    def chat(self, question: str):
        # result
        result = self.chain.invoke({
            'name': self.name,
            'format_instructions': self.parser.get_format_instructions(),
            'emotions': self.emotions,
            'chat_history': self.memory.get_chat_history(),
            'input': question,
        })

        # add to chat history
        self.memory.add_message(
            role="User", 
            text=question, 
            emotions=None
        )
        self.memory.add_message(
            role=self.name, 
            text=result['text'], 
            emotions=result['emotions']
        )

        return f"{result['text']} ({result['emotions']})"
    