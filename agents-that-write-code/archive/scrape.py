import os
import json
from bs4 import BeautifulSoup
import httpx
from rizaio import Riza

from openai import OpenAI

openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
riza_client = Riza(api_key=os.environ["RIZA_API_KEY"])


def extract_body_html(full_html):
    """Returns just the <body> of an HTML page, without any <scripts>"""
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


def run_code(code, input_data):
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


def generate_code(site_html):
    full_prompt = open("generate_code_prompt.txt").read() + "\n\n" + site_html
    completion = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": full_prompt,
            }
        ],
    )
    code = completion.choices[0].message.content
    return code


def save_data(data, filename):
    with open(filename, "w") as f:
        f.write(data)


def main():
    url = "https://www.pro-football-reference.com/players/A/AndeKe00.htm"
    html = download_html_body(url)
    if html is None:
        print("Could not download HTML")
        return None

    code = generate_code(html)
    result = run_code(code, html)

    print("Extracted data:\n\n{}".format(result))
    save_data(result, "data.json")


if __name__ == "__main__":
    main()
