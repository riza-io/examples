from utils.storage import load_previous_content
from utils.diff import get_diff
from types.state import TrackerState


def check_if_changed_node(state: TrackerState) -> TrackerState:
    url = state["url"]
    current = state["current_content"]
    storage_folder_path = state["storage_folder_path"]
    previous = load_previous_content(url, storage_folder_path)
    diff = get_diff(previous, current)
    return {**state, "previous_content": previous, "diff": diff}
