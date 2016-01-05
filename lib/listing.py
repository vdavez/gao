from lxml import html

with open('tests/test.html', 'r') as f:
    tree = html.fromstring(f.read())

    listings = tree.find_class('docketSearch')
    [print(x.xpath('a//text()')[2].strip()) for x in listings]
