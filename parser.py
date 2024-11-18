import internal_logger
import re
from bs4 import BeautifulSoup

compulsory_fields = ["results_selector", "description_selector", "title_selector", "url_selector"]

class ResultParser: 
    def __init__(self):
        self.logger = internal_logger.get_logger(self)
        self.soup = None

    def search_pagination(self, source):
        """Checks if pagination is available on the search results page.
        Args:
            source (str): The HTML source of the search results page.
        Returns:
            bool: True if pagination is available, False otherwise.
        """
        self.soup = BeautifulSoup(source, features="lxml")
        return bool(self.soup.find("span", class_=["SJajHc", "NVbCr"]))
    
    def remove_duplicate_results(results):
        """Removes duplicate search results based on the URL.
        Args:
            search_results (list): List of search results to deduplicate.
        Returns:
            list: List of search results with duplicates removed.
        """
        seen_urls = set()
        unique_results = []

        # Append only unique results
        for result in results:
            url = result[2]
            if url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(result)

        return unique_results
    
    def get_all_results(self):
        """Retrieves all result elements from a valid SERP
        """
        pass

    def extract_result_description(self, result):
        """Given a valid result elements, obtains the title

        Args:
            result (BS Obj): A single results element.
        """
        pass

    def extract_result_title(self, result):
        """Given a valid result elements, obtains the title

        Args:
            result (BS Obj): A single results element.
        """
        pass

    def extract_result_url(self, result):
        """Given a valid result elements, obtains the title

        Args:
            result (BS Obj): A single results element.
        """
        pass

    def remove_unwanted_elements(self):
        """Removes unwanted result elements from a set of results.
        """
        pass

    def update_soup(self, source):
        """Takes HTML source code and updates the parser's soup property. 
        Intended to be executed before result parsing to get latest page HTML.

        Args:
            source (str (HTML)): HTML code.
        """
        self.soup = BeautifulSoup(source, 'lxml')

   


class GoogleParser(ResultParser):
    def get_all_results(self):
        return self.soup.find_all("div", class_=["tF2Cxc", "dURPMd"])
    
    def remove_unwanted_elements(self):
        undesired_classes = ["d4rhi", "Wt5Tfe", "UDZeY fAgajc OTFaAf"]
        for cls in undesired_classes:
            for s in self.soup.find_all("div", class_=cls):
                s.decompose()  # Extract elements from the DOM

    def extract_result_title(self, result):
        try:
            title = result.find("h3", class_=["LC20lb", "MBeuO", "DKV0Md"]).text.strip()
        except:
            title = "N/A"
        return title

    def extract_result_description(self, result):
        try:
            description = result.find("div", class_=re.compile("VwiC3b", re.I)).text.strip()
        except:
            description = "N/A"
        return description
    
    def extract_result_url(self, result):
        # Extract URL
        try:
            urls = result.find_all("a")
            if urls:
                url = urls[0].attrs.get('href', "N/A")
        except Exception:
            url = "N/A"
        return url


class BingParser(ResultParser):
    def get_all_results(self):
        return self.soup.find_all("li", class_=["b_algo", "b_algo_group"])

    def extract_result_title(self, result):
        try:
            title = result.find("a").text.strip() if result.find("a") else "N/A"
        except:
            title = "N/A"
        return title

    def remove_unwanted_elements(self):
        for tag in self.soup.find_all("span", class_=["algoSlug_icon"]):
            tag.extract()
        for tag in self.soup.find_all("li", class_=["b_algoBigWiki"]):
            tag.extract()

    def extract_result_url(self, result):
        try:
            url = result.find("a")["href"] if result.find("a") else "N/A"
        except:
            url = "N/A"
        return url

    def extract_result_description(self, result):
        try:
            description = (
                result.find("p", class_=["b_lineclamp2 b_algoSlug", "b_lineclamp4 b_algoSlug", "b_paractl", "b_lineclamp3 b_algoSlug", "b_lineclamp1 b_algoSlug", "b_dList"]).text.strip()
                if result.find("p") else
                result.find("ol", class_=["b_dList"]).text.strip() if result.find("ol") else "N/A"
            )
        except:
            description = "N/A"
        return description


class DDGParser(ResultParser):
    def get_all_results(self):
        return self.soup.find_all("li", class_="wLL07_0Xnd1QZpzpfR4W")
    
    def remove_unwanted_elements(self):
        pass

    def extract_result_title(self, result):
        try:
            title = result.find("span", class_="EKtkFWMYpwzMKOYr0GYm LQVY1Jpkk8nyJ6HBWKAk").text.strip()
        except:
            title = "N/A"
        return title

    def extract_result_description(self, result):
        try:
            description = " ".join([desc.text.strip() for desc in result.find_all("div", class_="E2eLOJr8HctVnDOTM8fs")])
        except:
            description = "N/A"
        return description
    
    def extract_result_url(self, result):
        try:
            url = result.find("a", class_="Rn_JXVtoPVAFyGkcaXyK")['href']
        except:
            url = "N/A"
        return url


class EcosiaParser(ResultParser):        
    def get_all_results(self):
        return self.soup.find_all("div", class_=["result__body"])
    
    def remove_unwanted_elements(self):
        pass

    def extract_result_title(self, result):
        try:
            title = result.find("div", class_=["result__title"]).text.strip()
        except:
            title = "N/A"
        return title

    def extract_result_description(self, result):
        try:
            description_elem = result.find("div", class_=["result__description"])
            if description_elem:
                description = description_elem.text.strip()
        except:
            description = "N/A"
        return description
    
    def extract_result_url(self, result):
        try:
            url_elem = result.find("a")
            if url_elem:
                url = url_elem.attrs['href']
                result_url = url
        except:
            pass
        return result_url