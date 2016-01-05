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

        # Get the field that's identified, and then save the attribute
        # Responsible for solicitation_number, agency, file_number, and outcome
        for key in self.elems.xpath('//following-sibling::b'):
            field = key.text_content().replace(' ', '_').lower()
            data[field] = re.sub(r'^:', '', key.xpath('following-sibling::text()')[0]).strip()

        # TODO: For all of these dates, convert them into dates,
        # not like in current form "Dec 10, 2015"
        data["filed_date"] = self.elems.xpath('//tr/td[2]/text()')[0]
        data["due_date"] = self.elems.xpath('//tr/td[2]/text()')[1]

        data["case_type"] = self.elems.xpath('//tr/td[2]/text()')[2]
        data["gao_attorney"] = self.elems.xpath('//tr/td[2]/text()')[3]

        return data


if __name__ == "__main__":

    with open('tests/data/sustain.html', 'r') as f:
        fullhtml = f.read()
        tree = html.fromstring(fullhtml)
        protests = tree.find_class('docketSearch')
        out = []
        for p in protests:
            protest = Protest(etree.tostring(p).decode('utf-8'))
            out.append(protest.data)
        with open('gao.json', 'w') as outfile:
            outfile.write(json.dumps(out, indent=2))
