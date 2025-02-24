import codegen

requirements = """
use the open notify api to tell me the current location of the ISS. 
http://api.open-notify.org/iss-now.json
please convert the lat long into language that I would understand. 
"""

codegen.write_review_and_run_code(requirements)
