from lxml import etree, html
import json
import re


class Protest:
    def __init__(self, protestdata):
        self.html = protestdata
        self.elems = html.fromstring(self.html)
        self.text = self.elems.text_content()
        self.data = self.get_protest_data()

    def get_protest_data(self):
        data = {}
        data["name"] = self.elems.xpath('//a/text()[(following::br)]')[0].strip()
        data["docket_url"] = self.elems.find_class('release_info')[0]\
                         .text_content().strip()
        # This is currently pretty brittle because if there's no solicitation
        # number, all of this gets thrown off, so really we need to validate
        # the field that's identified, and then saving the attribute
        for key in self.elems.xpath('//following-sibling::b'):
            field = key.text_content().replace(' ', '_').lower()
            data[field] = re.sub(r'^:', '', key.xpath('following-sibling::text()')[0]).strip()

        # solicitation_number = self.elems.xpath('//following-sibling::b//following-sibling::text()')[0].replace(':','').strip()
        # agency = self.elems.xpath('//following-sibling::b//following-sibling::text()')[1].replace(':','').strip()
        # file_number = self.elems.xpath('//following-sibling::b//following-sibling::text()')[2].replace(':','').strip()
        # outcome = self.elems.xpath('//following-sibling::b//following-sibling::text()')[3].replace(':','').strip()

        # TODO: For all of these dates, convert them into dates,
        # not like in current form "Dec 10, 2015"
        # data["decided_date"] = self.elems.xpath('//following-sibling::b//following-sibling::text()')[4].replace(':','').strip()
        data["filed_date"] = self.elems.xpath('//tr/td[2]/text()')[0]
        data["due_date"] = self.elems.xpath('//tr/td[2]/text()')[1]

        data["case_type"] = self.elems.xpath('//tr/td[2]/text()')[2]
        data["gao_attorney"] = self.elems.xpath('//tr/td[2]/text()')[3]

        return data
        # return ({
        #     "name": name,
        #     "url": docket_url,
        #     "solicitation_number": solicitation_number,
        #     "agency": agency,
        #     "file_number": file_number,
        #     "outcome": outcome,
        #     "decided_date": decided_date,
        #     "filed_date": filed_date,
        #     "due_date": due_date,
        #     "case_type": case_type,
        #     "gao_attorney": gao_attorney
        # })


if __name__ == "__main__":

    with open('tests/data/test.html', 'r') as f:
        fullhtml = f.read()
        tree = html.fromstring(fullhtml)
        protests = tree.find_class('docketSearch')
        out = []
        for p in protests:
            protest = Protest(etree.tostring(p).decode('utf-8'))
            out.append(protest.data)
        with open('gao.json', 'w') as outfile:
            outfile.write(json.dumps(out, indent=2))
