from state import TrackerState
from utils.storage import save_current_version


def store_notify_node(state: TrackerState) -> TrackerState:
    url = state["url"]
    save_current_version(url, state["current_content"])

    # For now, just print the output. Later could send email or Slack.
    print(f"\n🔔 Change summary for {url}:")
    print(state["summary"])
    print(f"\n📈 View the accompanying chart: {state["chart_path"]}")
    return state
