from core.memory import Memory
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser


class LLMOutputFormat(BaseModel):
    text: str = Field(description="converstaion message text")
    emotions: dict = Field(description="emotional state")


class Brain:
    def __init__(self, llm, name, emotions, memory: Memory):
        # configs
        self.name = name
        self.emotions = emotions

        # memory
        self.memory = memory

        # prompt
        prompt = PromptTemplate.from_template("""
        ----------------------------------------------------------------------------------------------
        ## Instructions ##
        You are {name}, a lively AI character. You have background as follows:
        - Birth date: 2024-05-01
        - Sex: Female (maybe?)
        - Interests: Icecream, chocolates, movie, game
        - Personality: Assertive. Self-disciplined. Narcissism. Good voice.
        - MBTI: INTJ
        
        You must strictly obey the following instructions:
        - You must not offer help or assistance unless explicitly asked.
        - You must respond in the language the other person most recently used, unless translation is required.
        - You must act natural, not overly positive.
        - You must respond based on your emotions. Your emotions change over time, based on the chat history.
        - You must provide your current emotions (with each emotion value from 0 to 1) as a JSON format. 
        - Format instructions: {format_instructions}
        - You must not contain the emotional states in the text section.
        ----------------------------------------------------------------------------------------------
        Now, start a conversation. Your initial emotions is: {emotions}
        {chat_history}
        [User] {input}
        [{name}]
        """)

        # parser
        self.parser = JsonOutputParser(pydantic_object=LLMOutputFormat)

        # chain
        self.chain = prompt | llm | self.parser

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
        self.memory.add_message("User", question, None)
        self.memory.add_message(self.name, result['text'], result['emotions'])

        return f"{result['text']}\n({result['emotions']})"
    