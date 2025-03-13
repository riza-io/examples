import json
from rizaio import Riza
from test_cases import ALL_TEST_CASES
from data_transform_codegen import ClaudeCsvToJsonCodeGenerator


# Get an API key from https://dashboard.riza.io and set it as the value of
# an environment variable named RIZA_API_KEY
riza_client = Riza()


def _run_code(code, input_data):
    print("Running code on Riza...")
    return riza_client.command.exec_func(
        language="python",
        input=input_data,
        code=code,
    )


def _validate_result(test_case, code_execution):
    # 1. Check code executed
    if code_execution.execution.exit_code != 0:
        return {
            "passed": False,
            "details": {"error": f"Code failed to execute: {code_execution.execution.stderr}"}
        }
    elif code_execution.output_status != "valid":
        return {
            "passed": False,
            "details": {"error": f"Unsuccessful output status: {code_execution.output_status}, stderr: {code_execution.execution.stderr}"}
        }

    execution_result =  code_execution.output

    # 2. Check result exists
    if "result" not in execution_result:
        return {
            "passed": False,
            "details": {"error": "Missing 'result' in output"}
        }

    # 3. Check result is valid stringified JSON
    actual_output = execution_result["result"]
    if isinstance(actual_output, str):
        try:
          json_output = json.loads(actual_output)
        except Exception as e:
          return {
              "passed": False,
              "details": {"error": f"Failed to return a valid JSON string. Got: {actual_output}"}
          }
    else:
        return {
            "passed": False,
            "details": {"error": f"Did not return a string. Got: {str(actual_output)}"}
        }

    # 4. Check data accuracy
    if json_output != test_case.expected_json_out:
        return {
            "passed": False,
            "details": {"error": f"Actual output did not match expected output. \nExpected: {json.dumps(test_case.expected_json_out)} \nGot: {actual_output}"}
        }

    return {
        "passed": True,
        "details": {},
    }


def evaluate_llm_code(generator_id, code_generator, test_cases):
    results = {
        "generator_id": generator_id,
        "summary": {
            "total": len(test_cases),
            "passed": 0,
            "failed": 0,
        },
        "test_case_details": [],
        "overall_score": None,
    }

    if len(test_cases) == 0:
        return

    for t in test_cases:
        generated_code = code_generator(t.desired_schema, t.csv_sample)
        input_data = {"data": t.csv_full}
        execution_result = _run_code(generated_code, input_data)

        validation_result = _validate_result(t, execution_result)

        case_result = {
            "id": t.id,
            "name": t.name,
            "passed": validation_result["passed"],
            "details": validation_result["details"],
            "generated_code": generated_code
        }
        results["test_case_details"].append(case_result)

        if validation_result["passed"]:
            results["summary"]["passed"] += 1
        else:
            results["summary"]["failed"] += 1


    # Overall score
    passed_count = results["summary"]["passed"]
    total_count = results["summary"]["total"]
    results["overall_score"] = round(1.0 * passed_count / total_count, 2)

    return results


def main():
    code_generator = ClaudeCsvToJsonCodeGenerator()

    results = evaluate_llm_code(
        generator_id=code_generator.generator_id,
        code_generator=code_generator.generate_code,
        test_cases=ALL_TEST_CASES
    )

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
