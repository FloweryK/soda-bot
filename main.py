from dotenv import load_dotenv
load_dotenv(".env")

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage

from common.state import State
from nodes.chat import chat, DEFAULT_EMOTIONS


# load llm
config = {"configurable": {"thread_id": 1}}
graph_builder = StateGraph(State)

# add nodes
graph_builder.add_node("chat", chat)

# add edges
graph_builder.add_edge(START, "chat")
graph_builder.add_edge("chat", END)

memory = InMemorySaver()
graph = graph_builder.compile(checkpointer=memory)


while True:
    user_input = input("[User] ")
    
    graph.invoke(
        input={
            "messages": [HumanMessage(content=user_input)],
            "emotions": DEFAULT_EMOTIONS,
        }, 
        config=config
    )