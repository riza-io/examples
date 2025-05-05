import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate
from state import TrackerState

load_dotenv()
llm = ChatAnthropic(
    model="claude-3-7-sonnet-latest",
    temperature=0,
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
)
prompt = PromptTemplate.from_template(
    """
    You're an analyst tracking changes in gas prices.
    You have received the following updates to gas prices across different U.S. states.
    Summarize the important updates in this diff. Include a numerical analysis of notable changes:

    {diff}
    """
)
summarizer = prompt | llm


def summarize_change_node(state: TrackerState) -> TrackerState:
    summary = summarizer.invoke({"diff": state["diff"]})
    return {**state, "summary": summary.content}
