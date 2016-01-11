import requests
from lxml import etree, html


class Opinion:
    def __init__(self, docket):
        self.docket = docket
        self.summary = None
        self.decision = None
        self.get_opinion()

    def get_opinion(self):
        r = requests.get("http://gao.gov/products/" + self.docket)
        tree = html.fromstring(r.text)
        if r.status_code == 404 or self.opinion_not_found(tree):
            return False
        else:
            self.summary = self.get_summary_from_opinion(tree)
            self.decision = self.get_decision_from_opinion(tree)
        return True

    @staticmethod
    def opinion_not_found(tree):
        return len(tree.xpath("//div[@id='summary']/div[@class='left_col']")) == 0

    @staticmethod
    def get_summary_from_opinion(tree):
        return tree.xpath("//div[@id='summary']/div[@class='left_col']")[0].text_content().strip()

    @staticmethod
    def get_decision_from_opinion(tree):
        return str(etree.tostring(tree.xpath("//div[@class='Xright_col']")[0]).strip())
