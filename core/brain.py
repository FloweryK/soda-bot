from core.memory import Memory
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables.base import RunnableSerializable


class LLMOutputFormat(BaseModel):
    text: str = Field(description="Conversation message text (emotional states must not be included in this field).")
    emotions: dict = Field(description="Current emotional state (each emotion value ranges from 0 to 1) in JSON format.")
    contexts: str = Field(description="A summary of chat history in one sentence.")


class Brain:
    def __init__(self, llm, name, prompt, emotions, memory: Memory):
        # configs
        self.name = name
        self.emotions = emotions

        # memory
        self.memory = memory

        # prompt
        prompt = PromptTemplate.from_template(prompt)

        # parser
        self.parser = JsonOutputParser(pydantic_object=LLMOutputFormat)

        # chain
        self.chain: RunnableSerializable = prompt | llm | self.parser

    def stream(self, question: str):
        for s in self.chain.stream({
                'name': self.name,
                'format_instructions': self.parser.get_format_instructions(),
                'emotions': self.emotions,
                'chat_history': self.memory.get_chat_history(),
                'contexts': self.memory.contexts,
                'input': question,
            }):
            yield(s)
    
    def add_chat_history(self, question, text, emotions, contexts):
        self.memory.add_message("User", question, None)
        self.memory.add_message(self.name, text, emotions)
        self.memory.contexts = contexts