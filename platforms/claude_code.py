import anthropic
import rizaio

# Get an API key from Anthropic and set it as the value of an environment variable named ANTHROPIC_API_KEY
client = anthropic.Anthropic()

# Get an API key from https://dashboard.riza.io and set it as the value of an environment variable named RIZA_API_KEY
riza = rizaio.Riza()


def execute_function(language, code, function_input):
    print(f"Running the following {language} code on Riza:\n")
    print(code)
    print("\n\n... with the following input:\n")
    print(function_input)

    resp = riza.command.exec_func(
        language=language,
        code=code,
        input=function_input
    )

    print("\nResponse from Riza:\n")
    print(resp)

    if int(resp.execution.exit_code) > 0:
        print(f"Riza execution resulted in a non-zero exit code: {resp.execution.exit_code}")
    return resp


def main():
    CLAUDE_MODEL = "claude-3-7-sonnet-latest"
    EXECUTE_PYTHON_FUNCTION_TOOL = {
        "name": "execute_python_function",
        "description":
            "Execute a Python function that takes in one parameter, `input`. `input` is a Python object that can have any fields. The Python runtime includes the entire standard library. Write output by returning a Python object with any relevant fields.",
        "input_schema": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "The Python function to execute. The function signature must be: `def execute(input)`.",
                },
                "input": {
                    "type": "object",
                }
            },
            "required": ["code", "input"],
        }
    }

    messages = [{
        "role": "user",
        "content": "Please base32 encode this message: purple monkey dishwasher"
    }]
    tools = [EXECUTE_PYTHON_FUNCTION_TOOL]

    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=1024,
        tools=tools,
        messages=messages,
    )

    while True:
        tool_used = False
        messages.append({
            "role": "assistant",
            "content": response.content,
        })

        for block in response.content:
            if block.type == 'tool_use' and block.name == 'execute_python_function':
                tool_used = True

                riza_response = execute_function("python", block.input['code'], block.input['input'])

                messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": str(riza_response.output) if riza_response.execution.exit_code == 0 else f"Function execution resulted in an error: {riza_response.execution.stderr}",
                        }
                    ],
                })

        if not tool_used:
            print("\nNo tool used. Final response from Claude:\n")
            print(response)
            return

        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=1024,
            tools=tools,
            messages=messages,
        )


if __name__ == "__main__":
    main()
