import json
import anthropic

# Get an API key from Anthropic and set it as the value of
# an environment variable named ANTHROPIC_API_KEY
anthropic_client = anthropic.Anthropic()


PROMPT = """
You are given raw CSV data of a list of people.

Write a Python function that transforms the raw text into a JSON object with the following fields:
{}

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

class ClaudeCsvToJsonCodeGenerator:
  id = "claude-3-7-sonnet-latest"

  @staticmethod
  def generate_code(desired_schema_obj, sample_data):
      message = anthropic_client.messages.create(
          model="claude-3-7-sonnet-latest",
          max_tokens=2048,
          system="You are an expert programmer. When given a programming task, " +
            "you will only output the final code, without any explanation. " +
            "Do NOT put the code in a codeblock.",
          messages=[
              {
                  "role": "user",
                  "content": PROMPT.format(json.dumps(desired_schema_obj), sample_data),
              }
          ]
      )
      code = message.content[0].text
      return code
