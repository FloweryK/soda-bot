from core.memory import Memory
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser


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
    