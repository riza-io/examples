import os
import rizaio
import google.generativeai as genai

# Get an API key for Gemini from Google and set it as the value of an environment variable named GEMINI_API_KEY
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Get an API key from https://dashboard.riza.io and set it as the value of an environment variable named RIZA_API_KEY
riza_client = rizaio.Riza()


def execute_python(code:str):
    """ Executes a Python script and returns whatever was printed to stdout.

    The Python runtime does not have filesystem access, but does include the entire standard library. Read input from stdin and write output to stdout.
    """
    resp = riza_client.command.exec(
        language="python",
        code=code
    )
    return resp.stdout


def main():
    GEMINI_MODEL = "gemini-2.0-flash"

    model = genai.GenerativeModel(
        GEMINI_MODEL,
        tools=[execute_python]
    )
    chat = model.start_chat(enable_automatic_function_calling=True)
    response = chat.send_message('Please base32 encode this message (use a tool if needed): purple monkey dishwasher')
    print(response.text)

    for content in chat.history:
        print(content.role, "->", [type(part).to_dict(part) for part in content.parts])
        print('-'*80)


if __name__ == "__main__":
    main()
