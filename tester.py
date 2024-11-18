import controller
import controller_config
import json
import os
from selenium.webdriver.chrome.options import Options

# Configure and initialize controller
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--start-maximized")
options.add_argument('--disable-search-engine-choice-screen')

with open("default_config.json", 'r') as file:
    default_config = json.load(file)

config = controller_config.ControllerConfig(default_config)
cc = controller.Controller(engine="duckduckgo", default_config=config, driver_options=options)

# Create an output folder
folder_path = "scraping_output"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

try:
    # Values
    ecosia_de = "https://duckduckgo.com/"
    search_box = "q"
    query = "Roberto Carlos"

    # Visit Ecosia
    cc.get(ecosia_de)
    cc.random_wait(2, 5)

    # Find the search input field and send a query
    cc.search_by_searchbox(query, search_box)
    results = cc.extract_search_results()

    # Save screenshots
    cc.save_screenshot(f"{folder_path}/output_top.png")
    cc.scroll_down()
    cc.save_screenshot(f"{folder_path}/output_bottom.png")
    cc.random_wait(2, 4)

    # Save results as JSON
    with open(f"{folder_path}/output.json", 'w') as file:
        json.dump(results, file, indent=4)
finally:
    cc.quit