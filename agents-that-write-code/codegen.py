import os
from rizaio import Riza
from openai import OpenAI
import helpers


def get_prompt(filename, **kwargs):
    path = "prompts/" + filename + ".txt"
    with open(path, "r") as f:
        prompt = f.read().strip()
    return prompt.format(**kwargs)


def get_requirements(filename):
    path = "requirements/" + filename + ".txt"
    with open(path, "r") as f:
        return f.read().strip()


def call_openai(messages):
    client = OpenAI()
    response = client.chat.completions.create(model="o3-mini", messages=messages)
    return response.choices[0].message.content.strip()


def write_code(requirements):
    msgs = [
        {
            "role": "developer",
            "content": get_prompt("write_code", requirements=requirements),
        },
    ]
    code = call_openai(msgs)
    helpers.write_code(code)
    return True


def revise_code(requirements, feedback=None, error=None):
    """
    Revise the existing code based on review feedback or an error message.
    One of review_feedback or error_message should be provided.
    """
    existing_code = helpers.read_code()
    if not existing_code:
        print("No existing code found to revise.")
        return False

    prompt = get_prompt("write_code", requirements=requirements)

    if feedback:
        prompt += get_prompt(
            "revise_code_feedback",
            feedback=feedback,
            code=existing_code,
        )
    elif error:
        prompt += get_prompt(
            "revise_code_error",
            error=error,
            code=existing_code,
        )
    else:
        print("No feedback provided for revision.")
        return False

    messages = [
        {"role": "developer", "content": prompt},
    ]

    updated_code = call_openai(messages)
    helpers.write_code(updated_code)
    return True


def review_code():
    code = helpers.read_code()
    prompt = get_prompt("review_code", code=code)
    msgs = [
        {"role": "developer", "content": prompt},
    ]
    review = call_openai(msgs)
    helpers.write_review_comments(review)
    return review


def run_code(input_filename=None):
    code = helpers.read_code()
    if not code:
        message = "Error: code_for_riza.py file not found"
        print(message)
        helpers.write_execution_output(message)
        return None, message
    riza_client = Riza(api_key=os.environ["RIZA_API_KEY"])
    try:
        opts = {
            "language": "python",
            "runtime_revision_id": "01JM3WYPGJE3YV2DC7PXB00D1T",
            "code": code,
            "http": {"allow": [{"host": "*"}]},
        }
        if input_filename:
            opts["stdin"] = open(input_filename, "r").read()

        result = riza_client.command.exec(**opts)

    except Exception as e:
        message = f"Exception during execution: {str(e)}"
        print(message)
        helpers.write_execution_output(message)
        return None, message
    if result.exit_code != 0:
        message = f"Code did not execute successfully. Error: {result.stderr}"
        print(message)
        helpers.write_execution_output(message)
        return None, message
    if not result.stdout:
        message = "Code executed successfully but produced no output."
        print(message)
        helpers.write_execution_output(message)
        return "", message
    helpers.write_execution_output(result.stdout)
    return result.stdout, None


def write_review_and_run_code(requirements, input_filename=None):
    """
    Execute the entire code generation, review, revision, and execution process.
    Uses provided instructions.
    """
    helpers.clear_files_directory()
    max_attempts = 10

    print("Requirements:")
    print(requirements)

    for attempt in range(1, max_attempts + 1):
        print(f"\nAttempt {attempt}:")

        if attempt == 1:
            print("Generating code...")
            write_code(requirements)
        else:
            print("Using revised code...")

        print("Reviewing code...")
        feedback = review_code()
        print("Code Review:")
        print(feedback)

        if feedback != "👍":
            print("Review feedback received. Revising code based on review feedback...")
            revise_code(requirements, feedback=feedback)
            continue

        print("Executing code...")
        output, runtime_error = run_code(input_filename)
        if runtime_error:
            print(
                "Runtime error encountered. Revising code based on runtime error feedback..."
            )
            revise_code(requirements, error=runtime_error)
            continue

        if output:
            print("Output:")
            print(output)
            helpers.write_execution_output(output)
        break
    else:
        print("Max attempts reached without successful code generation")


if __name__ == "__main__":
    requirements = get_requirements("fib")
    write_review_and_run_code(requirements)


__all__ = [
    "call_openai",
    "write_code",
    "revise_code",
    "review_code",
    "run_code",
    "write_review_and_run_code",
    "get_prompt",
    "get_requirements",
]
