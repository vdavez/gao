from lxml import etree, html
import json
import re
import sqlite3


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

    db = sqlite3.connect("protests.db")
    cursor = db.cursor()

    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS protests (
            id INTEGER PRIMARY KEY,
            name TEXT,
            agency TEXT,
            solicitation_number TEXT,
            outcome TEXT,
            docket_url TEXT,
            filed_date TEXT,
            due_date TEXT,
            date_decided TEXT,
            case_type TEXT,
            gao_attorney TEXT
        )
    ''')

    with open('tests/data/sustained.html', 'r') as f:
        fullhtml = f.read()
        tree = html.fromstring(fullhtml)
        protests = tree.find_class('docketSearch')
        out = []
        for p in protests:
            protest = Protest(etree.tostring(p).decode('utf-8')).data
            cursor.execute('''INSERT INTO protests (name, agency, solicitation_number, outcome, docket_url, filed_date, due_date, date_decided, case_type, gao_attorney)
                  VALUES(?,?,?,?,?,?,?,?,?,?)''', (protest["name"], protest["agency"], protest.get("solicitation_number", ""), protest["outcome"], protest["docket_url"], protest["filed_date"], protest["due_date"], protest["date_decided"], protest["case_type"], protest["gao_attorney"]))
            out.append(protest)
        db.commit()
        # with open('gao.json', 'w') as outfile:
            # outfile.write(json.dumps(out, indent=2))
