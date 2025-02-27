from bs4 import BeautifulSoup
import httpx
from openai import OpenAI
from rizaio import Riza

openai_client = OpenAI()
riza_client = Riza()

# REQUIRED SETUP:
RUNTIME_REVISION_ID="<the ID of your runtime revision>"

WEBSITE = 'https://www2.brea.ca.gov/breasearch/faces/party/search.xhtml'

PROMPT = """
You are given the exact HTML of a website that contains a table of results.
Write Python code to extract the data from the table. Your code should print
out the extracted data in CSV format. Include the headings of the table.
Here are the rules for writing code:
- Use print() to write the output of your code to stdout.
- Use only the Python standard library and built-in modules. For example,
do not use `pandas`, but you can use `csv`. The one exception to this rule
is that you should use `beautifulsoup4` to parse HTML.
- In order to access the raw HTML, you must use a function called `get_html()`.
Include these exact lines in your code:
def get_html():
    stdin = sys.stdin.read()
    return stdin
Finally, here is the HTML string of the website. Remember, the goal is to extract
the rows from the table of results:
{}
"""

def extract_body_html(full_html):
    """Reduces a page of HTML to just the <body>, without any <scripts>"""
    soup = BeautifulSoup(full_html, "html.parser")
    body = soup.find("body")
    if body:
        for script in body.find_all("script"):
            script.decompose()
        return str(body)
    else:
        print("No <body> tag found in the HTML.")
        return None

def download_html_body(website_url):
    response = httpx.get(website_url)
    if response.status_code == 200:
        return extract_body_html(response.text)
    return None

def generate_code(site_html):
    completion = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
              "role": "system",
              "content": "You are an expert programmer. When given a programming task, " +
                  "you will only output the final code, without any explanation. " +
                  "Do NOT put quotes around the code."
            },
            {
                "role": "user",
                "content": PROMPT.format(site_html),
            }
        ]
    )
    code = completion.choices[0].message.content
    return code

def run_code(code, input_data):
    result = riza_client.command.exec(
        language="PYTHON",
        runtime_revision_id=RUNTIME_REVISION_ID,
        stdin=input_data,
        code=code,
    )
    if result.exit_code != 0:
        print("Code did not execute successfully. Error:")
        print(result.stderr)
    elif result.stdout == "":
        print("Code executed successfully but produced no output. "
            "Ensure your code includes print statements to get output.")
    return result.stdout

def main():
    html = download_html_body(WEBSITE)
    if html is None:
        print('Could not download HTML')
        return None

    code = generate_code(html)
    # print(code)

    result = run_code(code, html)
    print('Data from {}:\n\n{}'.format(WEBSITE, result))

if __name__ == "__main__":
    main()
