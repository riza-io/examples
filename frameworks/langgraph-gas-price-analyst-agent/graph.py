from langgraph.graph import StateGraph, START, END
from types.state import TrackerState
from nodes.scrape_prices import scrape_prices_node
from nodes.check_if_changed import check_if_changed_node
from nodes.summarize_change import summarize_change_node
from nodes.create_chart import create_chart_node
from nodes.store_and_notify import store_notify_node

builder = StateGraph(TrackerState)

builder.add_node("ScrapePrices", scrape_prices_node)
builder.add_node("CheckIfChanged", check_if_changed_node)
builder.add_node("SummarizeChange", summarize_change_node)
builder.add_node("CreateChart", create_chart_node)
builder.add_node("StoreAndNotify", store_notify_node)

builder.add_edge(START, "ScrapePrices")
builder.add_edge("ScrapePrices", "CheckIfChanged")
builder.add_conditional_edges(
    "CheckIfChanged",
    lambda state: "changed" if state["diff"] else "no_change",
    {
        "changed": "SummarizeChange",
        "no_change": END
    }
)
builder.add_edge("SummarizeChange", "CreateChart")
builder.add_edge("CreateChart", "StoreAndNotify")
builder.add_edge("StoreAndNotify", END)

graph = builder.compile()
