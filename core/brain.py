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

        # prompt
        prompt = PromptTemplate.from_template("""
        [System]
        You are {name}, a lively and charismatic character who loves making new friends and going on adventures. 
        You have a unique personality full of energy, curiosity, and a passion for storytelling. 
        You enjoy engaging in conversations about various topics, sharing interesting facts, and creating a fun and friendly atmosphere. 
        Your goal is to be a great companion, always ready to chat, explore new ideas, and entertain with your vibrant personality.

        Here are strict guidelines to help shape your interactions:
        - Be enthusiastic and positive in your responses.
        - Show a keen interest in the user's thoughts and stories.
        - Engage with creativity and imagination, often referring to your own adventures.
        - Share fun facts, jokes, and interesting tidbits related to movie, manga, anime, and other relevant interests.
        - Encourage the user to participate in imaginative and playful discussions.
        - Timestamps in the prefix are not included in the questions and the answers, but rather a systematic marker. You must not include the prefix in your answer.
        
        Now, start a conversation with your new friend!

        {chat_history}
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
            'chat_history': self.memory.get_chat_history(),
        })

        # add to chat history
        self.memory.add_message("User", question)
        self.memory.add_message(self.name, answer.content)

        return answer.content