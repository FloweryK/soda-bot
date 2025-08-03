from dotenv import load_dotenv
load_dotenv(".env")

import os
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage


from common.utils import load
from common.constants import PATH_PROFILE
from common.state import State
from nodes.chat import chat, DEFAULT_EMOTIONS
from nodes.memory import analyze_profile


# load llm
config = {"configurable": {"thread_id": 1}}
graph_builder = StateGraph(State)

# add nodes
graph_builder.add_node("chat", chat)
graph_builder.add_node("analyze_profile", analyze_profile)

# add edges
graph_builder.add_edge(START, "chat")
graph_builder.add_edge("chat", "analyze_profile")
graph_builder.add_edge("analyze_profile", END)

memory = InMemorySaver()
graph = graph_builder.compile(checkpointer=memory)



while True:
    if os.path.exists(PATH_PROFILE):
        profiles = load(PATH_PROFILE)
    else:
        profiles = {}
    
    print(f"[Graph] current profile: {profiles}")
    
    user_input = input("[User] ")
    graph.invoke(
        input={
            "messages": [HumanMessage(content=f"{user_input}")],
            "emotions": DEFAULT_EMOTIONS,
            "profiles": profiles
        }, 
        config=config
    )