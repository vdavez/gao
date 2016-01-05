from lxml import etree, html


class Protest:
    def __init__(self, protestdata):
        self.html = protestdata
        self.elems = html.fromstring(self.html)
        self.text = self.elems.text_content()
        self.data = self.get_protest_data()

    def get_protest_data(self):
        self.name = self.elems.xpath('//a/text()[(following::br)]')[0].strip()
        self.docket_url = self.elems.find_class('release_info')[0].text_content().strip()
        self.solicitation_number = self.elems.xpath('//following-sibling::b//following-sibling::text()')[0].replace(':','').strip()
        self.agency = self.elems.xpath('//following-sibling::b//following-sibling::text()')[1].replace(':','').strip()
        self.file_number = self.elems.xpath('//following-sibling::b//following-sibling::text()')[2].replace(':','').strip()
        self.outcome = self.elems.xpath('//following-sibling::b//following-sibling::text()')[3].replace(':','').strip()
        self.decided_date = self.elems.xpath('//following-sibling::b//following-sibling::text()')[4].replace(':','').strip()
        self.filed_date = self.elems.xpath('//tr/td[2]/text()')[0]
        self.due_date = self.elems.xpath('//tr/td[2]/text()')[1]
        self.case_type = self.elems.xpath('//tr/td[2]/text()')[2]
        self.gao_attorney = self.elems.xpath('//tr/td[2]/text()')[3]

        return ({
            "name": self.name,
            "url": self.docket_url,
            "solicitation_number": self.solicitation_number,
            "agency": self.agency,
            "file_number": self.file_number,
            "outcome": self.outcome,
            "decided_date": self.decided_date,
            "filed_date": self.filed_date,
            "due_date": self.due_date,
            "case_type": self.case_type,
            "gao_attorney": self.gao_attorney
        })

# print(x.xpath('a//text()')[2].strip())

if __name__ == "__main__":

    with open('tests/data/test.html', 'r') as f:
        fullhtml = f.read()
        tree = html.fromstring(fullhtml)
        protests = tree.find_class('docketSearch')
        for p in protests:
            protest = Protest(etree.tostring(p).decode('utf-8'))
            print(protest.data)
