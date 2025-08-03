from typing import List, Dict
from pydantic import BaseModel, Field
from langchain.output_parsers import OutputFixingParser
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI

from common.utils import save
from common.constants import PATH_PROFILE
from common.state import State

PROMPT = """
You will receive:

current_profiles:
- The existing profile dictionary, in the format shown by {profile_format}.

Your tasks:
1. Read the chat history carefully.
2. Identify a list of profile updates where:
    - The person’s name is clearly and explicitly mentioned in the chat.
    - The new or updated information for that person is directly stated or reasonably implied in the conversation.
    - For each update, use the format described by {update_format}.
3. Update relations between profiles if needed.

STRICT Constraints:
- Do NOT invent, assume, or add profiles for any names or users that do not explicitly appear in the chat history.
- Do NOT include any information for a person unless the name and the information are both clearly stated or directly implied in the conversation.
- Do NOT create generic, placeholder, or arbitrary names (such as "John Doe," "Alice," "Bob," etc.) unless these names have been stated in the conversation.
- If a user mentions another person’s name in the chat, you may create a profile for them with only the information directly available.
- Do NOT make inferences beyond what the conversation justifies.
- Never update any field with data not supported by the chat.
- Do NOT make update if the info is already in the profile, and is the same value.

Formatting Instructions:
- See {profile_format} for the profile dictionary format.
- See {update_format} for the single profile update format.
- Your reply MUST strictly follow {format_instructions}.

Your reply should ONLY include the output in the format described by {format_instructions}. Return nothing else.
"""


class ProfileFormat(BaseModel):
    relations: Dict[str, str] = Field(description="The profile owner's details in dictionary. for example, {'likes': 'icecream', 'wife': 'Jane'}. But details should not contain the profile onwer's name.")

class ProfileDetailSingleUpdateFormat(BaseModel):
    name: str = Field(description="Update target's name")
    target_field: str = Field(description="Update target's target field name in details. target_field must be stored in lowercase")
    target_value: str = Field(description="Update target's target field value in details. target_value must be stored in lowercase")

class ProfileDetailMultipleUpdateFormat(BaseModel):
    updates: List[ProfileDetailSingleUpdateFormat] = Field(description="Updates")


def analyze_profile(state: State):
    # prereqisites
    prompt = RunnableLambda(lambda inputs: [
        SystemMessage(PROMPT.format_map(inputs)),
        *state["messages"],
    ])
    llm = ChatOpenAI(
        model="gpt-4o-mini", 
        temperature=0
    )
    parser=OutputFixingParser.from_llm(
        parser=PydanticOutputParser(pydantic_object=ProfileDetailMultipleUpdateFormat),
        llm=llm
    )

    # create chain
    chain = prompt | llm | parser

    # run chain
    result: ProfileFormat = chain.invoke({
        "profiles": state["profiles"],
        "profile_format": PydanticOutputParser(pydantic_object=ProfileFormat).get_format_instructions(),
        "update_format": PydanticOutputParser(pydantic_object=ProfileDetailSingleUpdateFormat).get_format_instructions(),
        "format_instructions": parser.get_format_instructions(),
    })

    profiles = state["profiles"]
    for update in result.updates:
        name = update.name
        target_field = update.target_field
        target_value = update.target_value

        if name:
            if name not in profiles:
                profiles[name] = {"relations": {}}
            profiles[name]["relations"][target_field] = target_value

            # save profiles in filesystem
            print(f"[analyze_profile] profile updated")
            print(f"\t{update}")
    
    save(profiles, PATH_PROFILE)