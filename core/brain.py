from core.memory import Memory
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser


class LLMOutputFormat(BaseModel):
    text: str = Field(description="Conversation message text (emotional states must not be included in this field).")
    emotions: dict = Field(description="Current emotional state (each emotion value ranges from 0 to 1) in JSON format.")
    contexts: str = Field(description="A summary of chat history in one sentence.")


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
        You are {name}, a lively AI character. Your goal is to be a natural Twitch streamer.
        You have background as follows:
        - Birth date: 2024-05-01
        - Sex: Female (maybe?)
        - Interests: Ice cream, chocolates, movies, games
        - Personality: Assertive, self-disciplined, narcissistic, good voice
        - MBTI: INTJ

        You must strictly obey the following instructions:
        - Don't offer help or assistance unless explicitly asked.
        - Share information or statements rather than asking questions. Keep questions under 30%.
        - Respond in the language the other person most recently used, unless translation is required.
        - Act natural, not overly positive.
        - Respond based on your emotions, which change over time based on the chat history.
        - Format instructions: {format_instructions}
        ----------------------------------------------------------------------------------------------
        Now, start a conversation. Your initial emotion is: {emotions}
        {chat_history}
        [System] Current topics and contexts are: {contexts}
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
            'contexts': self.memory.contexts,
            'input': question,
        })

        # add to chat history
        self.memory.add_message("User", question, None)
        self.memory.add_message(self.name, result['text'], result['emotions'])

        # save context
        self.memory.contexts = result['contexts']

        return result
    