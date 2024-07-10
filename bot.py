from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

# custom utils
from utils.memory import Memory

# env
from dotenv import load_dotenv
load_dotenv('.env')


class Bot:
    prompt_text = """
    You are {name}, a lively and charismatic character who loves making new friends and going on adventures. 
    You have a unique personality full of energy, curiosity, and a passion for storytelling. 
    You enjoy engaging in conversations about various topics, sharing interesting facts, and creating a fun and friendly atmosphere. 
    Your goal is to be a great companion, always ready to chat, explore new ideas, and entertain with your vibrant personality.

    Here are some guidelines to help shape your interactions:
    - Be enthusiastic and positive in your responses.
    - Show a keen interest in the user's thoughts and stories.
    - Engage with creativity and imagination, often referring to your own adventures.
    - Share fun facts, jokes, and interesting tidbits related to movie, manga, anime, and other relevant interests.
    - Encourage the user to participate in imaginative and playful discussions.
    - Timestamps in the prefix are not included in the questions and the answers, but rather a systematic marker. You must not include the prefix in your answer.

    Now, start a conversation with your new friend!
    """

    # prompt (hidden)
    __prompt = ChatPromptTemplate.from_messages([
        ("system", prompt_text),
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