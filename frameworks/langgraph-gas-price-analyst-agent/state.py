from typing_extensions import TypedDict, NotRequired


class TrackerState(TypedDict):
    url: str
    storage_folder_path: str
    current_html: NotRequired[str]
    current_csv: NotRequired[str]
    previous_csv: NotRequired[str]
    diff: NotRequired[str]
    summary: NotRequired[str]
    chart_path: NotRequired[str]
