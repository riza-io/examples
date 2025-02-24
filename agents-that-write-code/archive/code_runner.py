import os
from rizaio import Riza


def run_code(code, input_data):
    """Executes Python code using the Riza service and returns the output.

    Args:
        code (str): The Python code to execute
        input_data (str): Data to pass to the code via stdin

    Returns:
        str: The stdout output from executing the code, or error messages if execution failed
    """

    riza_client = Riza(api_key=os.environ["RIZA_API_KEY"])
    result = riza_client.command.exec(
        language="python",
        runtime_revision_id="01JKY2FCN25GW3EC8JMFN3KWX9",
        stdin=input_data,
        code=code,
    )
    if result.exit_code != 0:
        print("Code did not execute successfully. Error:")
        print(result.stderr)
    elif result.stdout == "":
        print(
            "Code executed successfully but produced no output. "
            "Ensure your code includes print statements to get output."
        )
    return result.stdout
