from graph import graph

# TODO: Provide the path to a folder that will be used to store previous
# scraped gas prices for comparison.
STORAGE_FOLDER_PATH = ""

GAS_PRICE_SITE = "https://gasprices.aaa.com/state-gas-price-averages/"

if __name__ == "__main__":
    graph.invoke({
        "url": GAS_PRICE_SITE,
        "storage_folder_path": STORAGE_FOLDER_PATH,
    })
