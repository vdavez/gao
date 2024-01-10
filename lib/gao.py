import requests
from lxml import etree, html
from .protest import Protest


class GAO:
    def __init__(self, start_date: str, end_date: str):
        """Inits a GAO search period

        Args:
            start_date: A string in the form "2022-01-01"
            end_date: A string in the form "2022-01-08"
        """
        self.start_date = start_date
        self.end_date = end_date

    def get_dockets_page_list(self, page: int) -> []:
        """Gets a list of html results representing dockets, given a page
        Args:
            page: An integer >= 0

        Returns:
            A list of HTML elements representing dockets
        """
        url = f"https://www.gao.gov/search?f%5B0%5D=content_type_1%3ABid%20Protest%20Docket&search_mode=adv&f%5B1%5D=date%3Astart%2B{self.start_date}%2Bend%2B{self.end_date}&page={page}"
        res = requests.get(url)

        # Look for the docket results in the page
        tree = html.fromstring(res.text)
        dockets = tree.find_class("c-search-result")
        protests = []
        for docket in dockets:
            protest = Protest(etree.tostring(docket).decode("utf-8"))
            protests.append(protest.data)
        return protests

    def generate_all_dockets(self):
        """A generator that yields docket listing pages for the search period."""

        # Offset for pagination...
        page = 0
        while True:
            dockets = self.get_dockets_page_list(page)

            # If there are no protests, stop iterating
            if len(dockets) == 0:
                break
            # Otherwise, iterate
            else:
                yield dockets
            page += 1

        return True
