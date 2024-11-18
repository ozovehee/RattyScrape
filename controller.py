import controller_config
import internal_logger
import parser
import proxy_manager
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class InvalidEngineError(Exception):
    def __init__(self, message="Only Bing, Google, DuckDuckGo and Ecosia are supported by the parser"):
        super().__init__(message)

class Controller:

    available_drivers = []

    def __init__(self, driver_options=None, engine=None, default_config=None):
        if default_config:
            self.config = default_config
        else:
            self.config = controller_config.ControllerConfig()
        logging_file = self.config.get_config_value("logging_file")
        if logging_file: 
            internal_logger.set_logging_file(logging_file)
        self.logger = internal_logger.get_logger(self)
        self.parser = self.select_engine_parser(engine)
        self.active_driver = webdriver.Chrome(options=driver_options)

    def check_captcha(self, captcha_marker):
        return captcha_marker in self.page_source()
    
    def driver(self):
        return self.active_driver
    
    def extract_search_results(self, remove_duplicates=False):
        if not self.parser:
            raise InvalidEngineError
        valid_results = []
        
        try:
            self.parser.update_soup(self.page_source())
            results = self.parser.get_all_results()
            for result in results:
                title = self.parser.extract_result_title(result)
                description = self.parser.extract_result_description(result)
                url = self.parser.extract_result_url(result)
                valid_results.append([title, description, url])
        except:
            pass

        if remove_duplicates:
            return self.parser.remove_duplicate_results(valid_results)

        return valid_results
    
    def get(self, url):
        self.logger.debug(f"Executing action: get on url {url}")
        return self.active_driver.get(url)
    
    def page_source(self):
        return self.active_driver.page_source
        
    def random_wait(self, min, max):
        time.sleep(random.randint(min, max))
        return
    
    def save_screenshot(self, file=None):
        """Takes a screenshot of the current browser window and saves it.

        Args:
            file (string, optional): The name to use in saving the screenshot. Defaults to None.
        """
        self.logger.debug("Executing action: save_screenshot")
        if file:
            screenshot_file = file
        else:
            current_time = datetime.now()
            time_string = current_time.strftime("%Y-%m-%d %H:%M:%S")

            # Replace spaces with underscores
            screenshot_file = "screenshot_"+time_string.replace(" ", "_").replace(":", "_")+".png"

        time.sleep(2)

        self.active_driver.maximize_window() #maximize browser window for screenshot
        self.active_driver.save_screenshot(screenshot_file)
        self.logger.debug("Executed action: save_screenshot")
        return
    
    
    def scroll_down(self):
        self.active_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def search_by_searchbox(self, query, search_box):
        """Executes a search via a search box. Results in a SERP

        Args:
            query (string): The searchbox input
            search_box (string): _description_
        """
        self.logger.debug(f"Executing action: search_by_searchbox with query: {query}")
        search = self.active_driver.find_element(By.NAME, search_box)
        search.send_keys(query)
        search.send_keys(Keys.RETURN)
        self.random_wait(2, 5)
        # TO DO: generate the parser here
        return

    def search_by_url(self, search_url):
        self.logger.debug(f"Executing action: search_by_url with url {search_url}")
        self.active_driver.get(search_url)

    
    def search_for_pagination(self):
        self.logger.debug(f"Executing action: search_for_pagination")
        return self.parser.search_pagination(self.page_source)
    
    def select_engine_parser(self, engine):
        """Selects an engine parser from a collection of available options.

        Args:
            engine (string): Search engine name e.g "Google", "Ecosia" et.c.

        Returns:
            parser.ResultParser(): a suitable parser for provided search engine.
        """
        # selects parser based on engine input.
        engine = str(engine).lower()
        if engine == "bing":
            return parser.BingParser()
        elif engine == "duckduckgo":
            return parser.DDGParser()
        elif engine == "ecosia":
            return parser.EcosiaParser()
        elif engine == "google":
            return parser.GoogleParser()
        else:
            warning_str = f"Invalid search engine passed: {engine}. Supported engines are Bing, Ecosia, and Google with unverified support for DuckDuckGo."
            self.logger.warning(warning_str)
            raise InvalidEngineError()
    
    def quit(self):
        # Quit and kill driver.
        self.logger.debug(f"Executing action: quit")
        self.active_driver.quit()
        return

    def change_proxy(self, new_proxy):
        """
        Change the proxy for the active driver

        Args:
            new_proxy (str): The new proxy to be used.

        Returns:
            webdriver: A new WebDriver instance with the new proxy settings.
        """

        # Test proxy against most popular SE: Google US
        if not proxy_manager.validate_proxy(new_proxy, "https://www.google.com/webhp?hl=en"):
            return

        # Save current driver options
        current_options = self.active_driver.options

        # Quit the existing driver to release resources
        self.quit()

        # Initialize new Chrome options
        options = webdriver.ChromeOptions()

        # Add the existing options (e.g., headless) back
        for option in current_options.arguments:
            if not "proxy-server" in str(option):
                options.add_argument(option)

        # Reinitialize the WebDriver with the new proxy and previous options
        options.add_argument(f'--proxy-server={new_proxy}')
        self.active_driver = webdriver.Chrome(options=options)