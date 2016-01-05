from lxml import html


class Protest:
    def __init__(self, protestdata):
        self.html = protestdata
        self.elems = html.fromstring(self.html)
        self.text = self.elems.text_content()

    def get_protest_data(self):
        pass

# print(x.xpath('a//text()')[2].strip())
