import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate
from rizaio import Riza
from state import TrackerState

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
    You are given HTML table of gas prices in different US states. Write a python function that extracts the data, and returns it as a CSV with the following headings:
    - state
    - regular_price
    - midgrade_price
    - premium_price
    - diesel_price

    IMPORTANT: Only output the final code, without any explanation. Do NOT put the code in a codeblock.

    Here are the rules for writing the Python function:
    - The function should return an object that has 1 field: "csv". The "csv" data should the CSV content as a string.
    - Use only the Python standard library and built-in modules. In addition, you can use `beautifulsoup4`.
    - The function signature must be:

    ```
    def execute(input):
    ```

    `input` is a Python object.
    The HTML table is available as text at `input["html_table"]`.

    Here is the html_table:

    {html_table}

    """
)

extractor = prompt | llm


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


def extract_price_data_node(state: TrackerState) -> TrackerState:
    response = extractor.invoke({
        "html_table": state["current_html"],
    })

    python_code = response.content
    print("Python code: ")
    print(python_code)

    input_data = {
        "html_table": state["current_html"],
    }
    output = _run_code(python_code, input_data)
    print("Output of running the code:")
    print(output)

    return {**state, "current_csv": output["csv"]}
