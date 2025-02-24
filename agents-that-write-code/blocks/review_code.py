from openai import OpenAI

prompt = """
You are a Python code reviewer. 
Analyze the code for errors, bugs, and potential issues. 
Ensure that this is valid, runable python code. 
If you find issues, provide specific feedback with line numbers. 
If the code looks good, respond with only '👍'. 
Format issues as 'Line X: description of issue'. 

Code: 
{code}
"""


def call_openai(messages):
    client = OpenAI()
    response = client.chat.completions.create(model="o3-mini", messages=messages)
    return response.choices[0].message.content.strip()


def review_code(code):
    msgs = [
        {"role": "developer", "content": prompt.format(code=code)},
    ]
    review = call_openai(msgs)
    return review


if __name__ == "__main__":
    code = "print('Hello, world!)"
    review = review_code(code)
    print(review)
