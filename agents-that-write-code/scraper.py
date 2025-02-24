import codegen
from bs4 import BeautifulSoup
import httpx


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
        html = extract_body_html(response.text)
        with open("html.html", "w") as f:
            f.write(html)
        return html
    return None


if __name__ == "__main__":
    URL = "https://www2.brea.ca.gov/breasearch/faces/party/search.xhtml"
    html = download_html_body(URL)
    requirements = """
in the file are a few HTML tables. 
we care about the second table in the file. 
convert the data in that table to json.
"""
    codegen.write_review_and_run_code(requirements, input_filename="html.html")
