from .memory import Memory
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables.base import RunnableSerializable


class LLMOutputFormat(BaseModel):
    text: str = Field(description="Conversation message text (emotional states must not be included in this field).")
    emotions: dict = Field(description="Current emotional state (each emotion value ranges from 0 to 1) in JSON format. JSON format must be constructed with double-quotes. Double quotes within strings must be escaped with backslash, single quotes within strings will not be escaped.")
    contexts: str = Field(description="A summary of chat history in one sentence.")


class Brain:
    def __init__(self, llm, name, prompt, emotions, memory_save_dir, memory_short_term_limit):
        # configs
        self.name = name
        self.emotions = emotions
        self.retry_limit = 5

        # prompt
        prompt = PromptTemplate.from_template(prompt)

        # parser
        self.parser = JsonOutputParser(pydantic_object=LLMOutputFormat)

        # chain
        self.chain: RunnableSerializable = prompt | llm | self.parser

        # memory
        self.memory = Memory(memory_save_dir, memory_short_term_limit)

    def chat(self, question, is_stream):
        # add user message
        self.add_user_message(question)

        chain_input = {
            'name': self.name,
            'format_instructions': self.parser.get_format_instructions(),
            'emotions': self.emotions,
            'chat_history': self.memory.get_chat_history(),
            'contexts': self.memory.contexts,
            'input': question,
        }
        
        # response buffer
        res = None

        n_retry = 0
        while n_retry <= self.retry_limit:
            try:
                # get response
                if is_stream:
                    for s in self.chain.stream(chain_input):
                        yield(s)
                        res = s
                else:
                    res = self.chain.invoke(chain_input)
                    yield(res)
                
                # add response message
                self.add_ai_message(res)
                break
            except:
                print(f"llm crashed. n_retry: {n_retry}")
                self.memory.add_message("SYSTEM", f"LLM CRASHED: n_retry={n_retry}", None, is_save=True)
                n_retry += 1
    
    def add_user_message(self, text):
        self.memory.add_message("User", text, None)
    
    def add_ai_message(self, res):
        if isinstance(res, dict) and res.keys() == {"text", "emotions", "contexts"}:
            self.memory.add_message(self.name, res['text'], res['emotions'])
            self.memory.contexts = res['contexts']
        else:
            raise KeyError("invalid resposne:", res)