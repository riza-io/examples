import os
from graph import graph

# Store all output in a local `.output` folder.
script_directory = os.path.dirname(os.path.abspath(__file__))
STORAGE_FOLDER_PATH = os.path.join(script_directory, ".output")

GAS_PRICE_SITE = "https://gasprices.aaa.com/state-gas-price-averages/"

if __name__ == "__main__":
    graph.invoke({
        "url": GAS_PRICE_SITE,
        "storage_folder_path": STORAGE_FOLDER_PATH,
    })
