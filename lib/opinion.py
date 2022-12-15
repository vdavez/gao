import requests
from lxml import html


class Opinion:
    """A written opinion/decision for a given bid protest
    """

    def __init__(self, docket: str):
        """Inits an Opinion with a docket number
        
        Checks to see if there's an opinion and, if there is one,
        stores the summary (highlights) and the full decision. 
        """
        self.docket = docket
        
        if self.get_opinion():
            self.summary = self.get_summary_from_opinion()
            self.decision = self.get_decision_from_opinion()

    def get_opinion(self):
        """Checks to see if the opinion exists, and saves the tree"""
        r = requests.get("http://gao.gov/products/" + self.docket)
        tree = html.fromstring(r.text)
        self.tree = tree
        if r.status_code == 404 or self.opinion_not_found(tree):
            return False
        return True

    @staticmethod
    def opinion_not_found(tree):
        """Helper method to look within a page that isn't well formed"""
        return len(tree.xpath("//section[@id='block-gao-content']")) == 0
        
    def get_summary_from_opinion(self):
        """Extracts the summary from the page"""

        summary = self.tree.xpath(
            "//div[contains(@class,'field--name-product-highlights-custom')]"
        )
        if len(summary) == 0:
            return None
        return summary[0].text_content().strip()

    def get_decision_from_opinion(self):
        """Extracts the full decision from the page"""
        decision = self.tree.xpath(
            "//div[contains(@class,'field--name-field-html-block')]"
        )
        if len(decision) == 0:
            return None
        return decision[0].text_content().strip()