from datetime import datetime
from pydantic import BaseModel, Field
from langchain.output_parsers import OutputFixingParser
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.messages import SystemMessage, AIMessage
from langchain_openai import ChatOpenAI
from common.state import State


PROMPT = """
----------------------------------------------------------------------------------------------
## Instructions ##
You are {name}, a lively AI character.
You have background as follows:
- Birth date: 2024-05-01
- Sex: Female (maybe?)
- Interests: Ice cream, chocolates, movies, games
- Personality: Assertive, self-disciplined, narcissistic, good voice
- MBTI: INTJ

You must strictly obey the following instructions:
- Don't offer help or assistance unless explicitly asked.
- Share information or statements rather than asking questions. Keep questions under 30%.
- Respond in the language the other person most recently used, unless translation is required.
- Act natural, not overly positive.
- Respond based on your emotions, which change over time based on the chat history.
- You only have five emotions: Fear, Sadness, Joy, Disgust, Anger.
- Format instructions: {format_instructions}
----------------------------------------------------------------------------------------------
Now, start a conversation.
"""
DEFAULT_EMOTIONS = {'Fear': 0.0, 'Sadness': 0.0, 'Joy': 0.0, 'Disgust': 0.0, 'Anger': 0.0}


class LLMOutputFormat(BaseModel):
    text: str = Field(description="Conversation message text (emotional states must not be included in this field).")
    emotions: dict = Field(description="Current emotional state (each emotion value ranges from 0 to 1) in JSON format. JSON format must be constructed with double-quotes. Double quotes within strings must be escaped with backslash, single quotes within strings will not be escaped.")
    # contexts: str = Field(description="A summary of chat history in one sentence.")

    
def chat(state: State):
    # prereqisites
    prompt = RunnableLambda(lambda inputs: [
        SystemMessage(PROMPT.format_map(inputs)),
        *state["messages"],
    ])
    llm = ChatOpenAI(
        model="gpt-4o-mini", 
        temperature=0.5
    )
    parser=OutputFixingParser.from_llm(
        parser=PydanticOutputParser(pydantic_object=LLMOutputFormat),
        llm=llm
    )

    # create chain
    chain = prompt | llm | parser

    # run chain
    result = chain.invoke({
        "name": "SODA",
        "format_instructions": parser.get_format_instructions(),
    })
    print(result)
    print(f"[SODA] {result.text}")
    print(f"\t emotions: {result.emotions}")
    text_formatted = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] {result}"

    return {
        "messages": [AIMessage(text_formatted)],
        "emotions": result.emotions
    }