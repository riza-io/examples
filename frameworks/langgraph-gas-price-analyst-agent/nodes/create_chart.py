import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate
from rizaio import Riza
from types.state import TrackerState
from utils.storage import save_image

load_dotenv()

riza_client = Riza(api_key=os.getenv("RIZA_API_KEY"))

# Create a Riza Python custom runtime that has the `plotly` and `beautifulsoup4`
# Python packages, and set the runtime revision ID in your .env file.
RIZA_RUNTIME_REVISION_ID = os.getenv("RIZA_RUNTIME_REVISION_ID")

llm = ChatAnthropic(
    model="claude-3-7-sonnet-latest",
    temperature=0,
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
)
prompt = PromptTemplate.from_template(
    """
    You're an analyst tracking changes in gas prices across different U.S. states.

    I want to create a chart / graph / infographic that illustrates the changes described in the "Summary" below. I've also provided the raw HTML tables that contain the gas price data from yesterday, and gas price data from today. The "Summary" was written based on this data.

    Please figure out what chart / graph / infographic to create, then write a Python function to create this graph. Keep it simple.

    IMPORTANT: Only output the final code, without any explanation. Do NOT put the code in a codeblock.

    Here are the rules for writing the Python function:
    - The function should return an object that has 1 field: "image". The "image" data should be the chart as a base64-encoded PNG image.
    - Use only the Python standard library and built-in modules. In addition, you can use `plotly` and `beautifulsoup4`.
    - The function should generate a chart and return the chart as a base64-encoded PNG image.
    - The function signature must be:

    ```
    def execute(input):
    ```

    `input` is a Python object.
    Yesterday's HTML data is available as text at `input["yesterday"]`.
    Today's HTML data is available as text at `input["today"]`.


    Here is the gas price summary, and raw data of gas prices yesterday and today:


    == Summary ==
    {summary}


    == Previous data (yesterday) ==
    {previous_data}


    == New data (today) ==

    {current_data}

    """
)

grapher = prompt | llm


def _run_code(code, input_data):
    print("Running code on Riza...")
    result = riza_client.command.exec_func(
        language="python",
        runtime_revision_id=RIZA_RUNTIME_REVISION_ID,
        input=input_data,
        code=code,
    )
    if result.execution.exit_code != 0:
        print("Code did not execute successfully. Error:")
        print(result.execution.stderr)
    elif result.output_status != "valid":
        print("Unsuccessful output status:")
        print(result.output_status)
    return result.output


def create_chart_node(state: TrackerState) -> TrackerState:
    response = grapher.invoke({
        "summary": state["summary"],
        "previous_data": state["previous_content"],
        "current_data": state["current_content"],
    })

    python_code = response.content
    # print("Python code: ")
    # print(python_code)

    input_data = {
        "yesterday": state["previous_content"],
        "today": state["current_content"],
    }
    output = _run_code(python_code, input_data)
    # print("Output of running the code:")
    # print(output)

    image_path = save_image(state["url"], output["image"], state["storage_folder_path"])

    return {**state, "chart_path": image_path}
