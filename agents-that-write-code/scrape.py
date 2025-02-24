import codegen


requirements = """
in the file are a few HTML tables. 
we care about the second table in the file. 
convert the data in that table to json.
"""

codegen.write_review_and_run_code(requirements, input_filename="data.html")
