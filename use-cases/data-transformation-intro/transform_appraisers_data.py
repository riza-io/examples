import itertools
from rizaio import Riza
import anthropic

# Get an API key from Anthropic and set it as the value of
# an environment variable named ANTHROPIC_API_KEY
anthropic_client = anthropic.Anthropic()

# Get an API key from https://dashboard.riza.io and set it as the value of
# an environment variable named RIZA_API_KEY
riza_client = Riza()


# OTHER REQUIRED SETUP:
INPUT_CSV_FILEPATH = ""

PROMPT = """
You are given raw CSV data of a list of people.

Write a Python function that transforms the raw text into a JSON object with the following fields:
{{
  "type": "object",
  "properties": {{
    "appraisers": {{
      "type": "array",
      "items": {{
          "type": "object",
          "properties": {{
            "name": {{
              "type: "string"
            }},
            "phone": {{
              "type": "string"
            }},
            "license": {{
              "type": "string"
            }}
          }}
      }}
    }}
  }}
}}

The function signature of the Python function must be:

```
def execute(input):
```

`input` is a Python object. The full data is available as text at `input["data"]`. The data is text.

Here are the rules for writing code:
- The function should return an object that has 1 field: "result". The "result" data should a stringified JSON object.
- Use only the Python standard library and built-in modules.

Finally, here are a few lines of the raw text of the CSV:

{}
"""

def run_code(code, input_data):
    print("Running code on Riza...")
    result = riza_client.command.exec_func(
        language="python",
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


def generate_code(sample_data):
    message = anthropic_client.messages.create(
        model="claude-3-7-sonnet-latest",
        max_tokens=2048,
        system="You are an expert programmer. When given a programming task, " +
           "you will only output the final code, without any explanation. " +
           "Do NOT put the code in a codeblock.",
        messages=[
            {
                "role": "user",
                "content": PROMPT.format(sample_data),
            }
        ]
    )
    code = message.content[0].text
    return code


def read_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()
    return content


def first_n_lines(text, n):
    return "\n".join(itertools.islice(text.splitlines(), n))


def main():
    full_rows = read_file(INPUT_CSV_FILEPATH)

    first_rows = first_n_lines(full_rows, 10)
    python_code = generate_code(first_rows)
    # print(python_code)

    input_data = {
        "data": full_rows,
    }
    output = run_code(python_code, input_data)
    print(output)


if __name__ == "__main__":
    main()
