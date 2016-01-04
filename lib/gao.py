import requests


class GAO:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def get_docket_list(self):
        """
        A method to get the docket listing.
        """
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
