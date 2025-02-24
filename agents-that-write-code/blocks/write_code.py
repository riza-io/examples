from openai import OpenAI

prompt = """
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


def write_code(requirements):
    msgs = [
        {
            "role": "developer",
            "content": prompt.format(requirements=requirements),
        },
    ]

    code = call_openai(msgs)
    return code


if __name__ == "__main__":
    requirements = "What is 52! (52 factorial)?"
    code = write_code(requirements)
    print(code)
