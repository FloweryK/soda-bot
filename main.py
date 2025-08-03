from dotenv import load_dotenv
load_dotenv(".env")

import os
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage

from common.state import State
from common.utils import save, load
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


STATE_PATH = "state.pickle"

while True:
    user_input = input("[User] ")

    # load state
    if os.path.exists(STATE_PATH):
        state = load(STATE_PATH)
        graph.update_state(config, values=state)
    
    graph.invoke(
        input={
            "messages": [HumanMessage(content=user_input)],
            "emotions": DEFAULT_EMOTIONS,
        }, 
        config=config
    )

    # save state
    state = graph.get_state(config).values
    save(state, STATE_PATH)