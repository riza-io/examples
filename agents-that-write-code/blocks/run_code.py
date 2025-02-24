import os
from rizaio import Riza


def run_code(code):
    riza_client = Riza(api_key=os.environ["RIZA_API_KEY"])
    try:
        opts = {
            "language": "python",
            "runtime_revision_id": "01JM3WYPGJE3YV2DC7PXB00D1T",
            "code": code,
            "http": {"allow": [{"host": "*"}]},
        }

        result = riza_client.command.exec(**opts)

    except Exception as e:
        message = f"Exception during execution: {str(e)}"
        print(message)
        return None, message
    if result.exit_code != 0:
        message = f"Code did not execute successfully. Error: {result.stderr}"
        print(message)
        return None, message
    if not result.stdout:
        message = "Code executed successfully but produced no output."
        print(message)
        return "", message
    print(result.stdout)
    return result.stdout, None


if __name__ == "__main__":
    code = "print(10 * 9 * 8 * 7 * 6 * 5 * 4 * 3 * 2 * 1"
    run_code(code)
