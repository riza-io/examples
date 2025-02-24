from openai import OpenAI


REVISE_PROMPT = """
You previously wrote this code: 

```
{code}
```

A code review resulted in the following feedback: 

<feedback>
{feedback}
</feedback>

Update the code based on the feedback. 

Again, only return valid code. 

"""


WRITE_PROMPT = """
You are an expert Python developer. 
Follow best practices and generate code accordingly. 
Only return working python. 
You are an expert programmer. 
When given a programming task, you will only output the final code, without any explanation. 
Do NOT put quotes or backticks around the code. 
Do NOT provide any commentary before or after the valid code. 

Your task is to generate code based on these instructions: 

<requirements>
{requirements}
</requirements>
"""


def call_openai(messages):
    client = OpenAI()
    response = client.chat.completions.create(model="o3-mini", messages=messages)
    return response.choices[0].message.content.strip()


def revise_code(code, requirements, feedback=None):
    prompt = WRITE_PROMPT.format(requirements=requirements)
    prompt += REVISE_PROMPT.format(code=code, feedback=feedback)

    messages = [
        {"role": "developer", "content": prompt},
    ]

    updated_code = call_openai(messages)
    return updated_code


if __name__ == "__main__":
    requirements = "write a hello world program in python"
    code = "print('Hello, world!)"
    feedback = "The code is not valid."
    updated_code = revise_code(code, requirements, feedback)
    print(updated_code)
