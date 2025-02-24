import httpx
from bs4 import BeautifulSoup
from icecream import ic


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
    """Downloads and returns the <body> content of a webpage, with scripts removed"""
    response = httpx.get(website_url)
    if response.status_code == 200:
        return extract_body_html(response.text)
    print(f"Failed to download page. Status code: {response.status_code}")
    return None


def extract_webpage_body(url):
    try:
        response = httpx.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        body = soup.find("body")

        return body.get_text(strip=True) if body else None

    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    url = input("Enter website URL: ")
    html_body = download_html_body(url)
    if html_body:
        ic(html_body)
