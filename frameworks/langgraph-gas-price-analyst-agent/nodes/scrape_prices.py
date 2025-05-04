import os
from dotenv import load_dotenv
from browserbase import Browserbase
from playwright.sync_api import sync_playwright, Playwright
from types.state import TrackerState

load_dotenv()
bb = Browserbase(api_key=os.environ["BROWSERBASE_API_KEY"])


def _run(playwright: Playwright, url: str) -> str:
    session = bb.sessions.create(project_id=os.environ["BROWSERBASE_PROJECT_ID"])

    chromium = playwright.chromium
    browser = chromium.connect_over_cdp(session.connect_url)
    context = browser.contexts[0]
    page = context.pages[0]

    table_html = ""

    try:
        page.goto(url)
        print(page.title())

        # Wait for the table to be visible
        page.wait_for_selector("table")

        # Get the table element
        table_element = page.query_selector("table")

        # Extract the HTML content of the table
        table_html = table_element.inner_html()

    finally:
        page.close()
        browser.close()
        print(f"Session complete! View replay at https://browserbase.com/sessions/{session.id}")

    return table_html


def scrape_prices_node(state: TrackerState) -> TrackerState:
    url = state["url"]
    table_html = ""
    with sync_playwright() as playwright:
      table_html = _run(playwright, url)
    return {**state, "current_content": table_html}
