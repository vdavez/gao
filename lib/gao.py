import requests
from lxml import etree, html
from .protest import Protest


class GAO:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def get_docket_list(self):
        """
        A method to get the docket listing.
        """

        ###
        # Planned method of attack
        ###
        # Get the list of 50
        # Process the 50 (get_protests_from_listing())
        # Dump each of the 50 into sqlite (within get_protests_from_listing())
        # Get next 50
        ###

        offset = 0
        url = ("http://gao.gov/legal/bid-protests/search?snumber=&filenum=&"
               "now_sort=docdate+desc%2Cissue_date_dt+desc&page_name="
               "bid_protest_docket&facets=a%3A3%3A%7Bs%3A4%3A%22site%22%3Bs%3A"
               "18%3A%22Bid+Protest+Docket%22%3Bs%3A8%3A%22closed_s%22%3Bs%3A1"
               "%3A%22Y%22%3Bs%3A7%3A%22docdate%22%3Bs%3A22%3A%22" +
               self.start_date + "to" + self.end_date +
               "%22%3B%7D&searched=1&rows=50"
               "&top_path=Legal%3ABid+Protest%3ABid+Protest+Docket&path="
               "Legal%3ABid+Protest%3ABid+Protest+Docket#bidProForm&o=" +
               str(offset)
               )
        self.res = requests.get(url)
        return self.res

    """
    get_protests_from_listing
    Take a listing of 50 (generally) protests in the docket data and create
    50 Protest objects, cleaned and ready for the database
    """
    def get_protests_from_listing(self, docketlist):
        tree = html.fromstring(docketlist)
        protests = tree.find_class('docketSearch')
        out = []
        for p in protests:
            protest = Protest(etree.tostring(p).decode('utf-8'))
            out.append(protest.data)
        return out

    """
    dump_json_into_db
    Take the protest objects and insert them into a sqlite database
    """
    def dump_json_into_db(self, project):
        pass
