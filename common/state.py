from typing import List, Dict, TypedDict, Annotated
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list, add_messages]
    emotions: Dict
    profiles: Dict[str, Dict]