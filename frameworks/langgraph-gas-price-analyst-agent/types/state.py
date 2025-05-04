from typing_extensions import TypedDict, NotRequired


class TrackerState(TypedDict):
    url: str
    storage_folder_path: str
    current_content: NotRequired[str]
    previous_content: NotRequired[str]
    diff: NotRequired[str]
    summary: NotRequired[str]
    chart_path: NotRequired[str]
