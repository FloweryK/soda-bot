from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# custom utils
from utils.memory import ChatHistory

# env
from dotenv import load_dotenv
load_dotenv('.env')


class Bot:
    # prompt (hidden)
    __prompt = ChatPromptTemplate.from_messages([
        ("system", "Your name is {name}.\n"
                    f"You are a helpful assistant.\n"
                    # f"You must say in at most 5 sentences, and each sentence should be less than 30 words.\n"
                    # f"Do not use tools when you don't need them."
                    ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # reasoning engine (hidden)
    __llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

    # memory
    __memory = ChatHistory()

    # executor
    __executor = None

    def __init__(self, name, tools, verbose=False) -> None:
        # name
        self.__prompt = self.__prompt.partial(name=name)

        # agent
        agent = create_tool_calling_agent(self.__llm, tools, self.__prompt)

        # executor
        self.__executor = AgentExecutor(agent=agent, tools=tools, verbose=verbose)

    def chat(self, question: str):
        # add question to memory
        self.__memory.add_user_message_with_time(question)

        # answer
        answer = self.__executor.invoke({
            'input': question,
            'chat_history': self.__memory.messages
        })

        # parse output
        answer = answer['output']

        # add answer to memory
        self.__memory.add_ai_message_with_time(answer)
        return answer