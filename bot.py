from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# custom utils
from utils.memory import Memory

# env
from dotenv import load_dotenv
load_dotenv('.env')


class Bot:
    # prompt (hidden)
    __prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant named {name}."),
        MessagesPlaceholder(variable_name="short_term_memory"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # reasoning engine (hidden)
    __llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

    def __init__(self, name, tools, short_term_limit, verbose=False) -> None:
        # name
        self.__prompt = self.__prompt.partial(name=name)

        # agent
        agent = create_tool_calling_agent(self.__llm, tools, self.__prompt)

        # executor
        self.__executor = AgentExecutor(agent=agent, tools=tools, verbose=verbose)
        
        # memory
        self.__memory = Memory(short_term_limit=short_term_limit)


    def chat(self, question: str):
        # answer
        answer = self.__executor.invoke({
            'input': question,
            'short_term_memory': self.__memory.get_short_term_memory()
        })

        # parse output
        answer = answer['output']

        # add the question and the answer to memory
        self.__memory.add_user_message_with_time(question)
        self.__memory.add_ai_message_with_time(answer)
        return answer