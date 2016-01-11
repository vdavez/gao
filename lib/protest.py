from lxml import etree, html
from lib.opinion import Opinion
import json
import re


class Protest:
    def __init__(self, protestdata):
        self.elems = html.fromstring(protestdata)
        self.data = self.get_protest_data()

    def get_protest_data(self):
        data = {}
        data["name"] = self.elems.xpath('//a/text()[(following::br)]')[0].strip()
        data["docket_url"] = self.elems.find_class('release_info')[0]\
                         .text_content().strip()

        # Get the field that's identified, and then save the attribute
        # Responsible for solicitation_number, agency, file_number, and outcome
        for key in self.elems.xpath('//following-sibling::b'):
            field = key.text_content().replace(' ', '_').lower()
            data[field] = re.sub(r'^:', '', key.xpath('following-sibling::text()')[0]).strip()
            if len(key.xpath("following-sibling::a/@href")) > 0:
                data["opinion"] = Opinion(key.xpath("following-sibling::a/@href")[0].split('/')[-1])

        # TODO: For all of these dates, convert them into dates,
        # not like in current form "Dec 10, 2015"
        data["filed_date"] = self.elems.xpath('//tr/td[2]/text()')[0]
        data["due_date"] = self.elems.xpath('//tr/td[2]/text()')[1]

        data["case_type"] = self.elems.xpath('//tr/td[2]/text()')[2]
        data["gao_attorney"] = self.elems.xpath('//tr/td[2]/text()')[3]

        return data
