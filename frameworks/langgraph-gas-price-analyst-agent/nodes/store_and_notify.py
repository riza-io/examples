from state import TrackerState
from utils.storage import save_current_csv


def store_notify_node(state: TrackerState) -> TrackerState:
    url = state["url"]
    save_current_csv(url, state["current_csv"], state["storage_folder_path"])

    # For now, just print the output. Later could send email or Slack.
    print(f"\n🔔 Change summary for {url}:")
    print(state["summary"])
    print(f"\n📈 View the accompanying chart: {state["chart_path"]}")
    return state
