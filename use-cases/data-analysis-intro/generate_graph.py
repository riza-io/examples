import anthropic
from rizaio import Riza
import itertools
import base64


# Get an API key from Anthropic and set it as the value of
# an environment variable named ANTHROPIC_API_KEY
anthropic_client = anthropic.Anthropic()

# Get an API key from https://dashboard.riza.io and set it as the value of
# an environment variable named RIZA_API_KEY
riza_client = Riza()

# OTHER REQUIRED SETUP:
RUNTIME_REVISION_ID=""
INPUT_CSV_FILEPATH = ""
OUTPUT_GRAPH_FILEPATH = ""


PROMPT = """
You are given a dataset of the yearly salary of SF city employees (who work in Fire Services) over many years.

Write a Python function that calculates the minimum, maximum, mean, median, and mode of the salaries per year, and plots them. The function should generate a chart and return the chart as a base64-encoded PNG image.

The function signature is:

```
def execute(input):
```

`input` is a Python object. The full data is available as text at `input["data"]`. The data is in CSV format.

Here are the rules for writing code:
- The function should return an object that has 1 field: "image". The "image" data should be the chart as a base64-encoded PNG image.
- Use only the Python standard library and built-in modules. In addition, you can use `pandas`, `matplotlib`, and `seaborn`.

Finally, here is an excerpt of the CSV data:

{}
"""


def generate_code(csv_sample):
    message = anthropic_client.messages.create(
        model="claude-3-7-sonnet-latest",
        max_tokens=2048,
        system="You are an expert programmer. When given a programming task, " +
           "you will only output the final code, without any explanation. " +
           "Do NOT put the code in a codeblock.",
        messages=[
            {
                "role": "user",
                "content": PROMPT.format(csv_sample),
            }
        ]
    )
    code = message.content[0].text
    # print("GENERATED CODE: ")
    # print(code)
    return code


def run_code(code, input_data):
    print("Running code on Riza...")
    result = riza_client.command.exec_func(
        language="python",
        runtime_revision_id=RUNTIME_REVISION_ID,
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


def read_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()
    return content


def first_n_lines(text, n):
    return "\n".join(itertools.islice(text.splitlines(), n))


def save_image_to_file(base64_encoded_image, filepath):
    with open(filepath, "wb") as image_file:
        image_file.write(base64.b64decode(base64_encoded_image))


def main():
    full_rows = read_file(INPUT_CSV_FILEPATH)

    first_rows = first_n_lines(full_rows, 10)
    python_code = generate_code(first_rows)

    input_data = {
        "data": full_rows,
    }
    output = run_code(python_code, input_data)
    save_image_to_file(output["image"], OUTPUT_GRAPH_FILEPATH)


if __name__ == "__main__":
    main()
