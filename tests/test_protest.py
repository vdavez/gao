import pytest
from lxml import html, etree
from lib.protest import Protest


@pytest.fixture
def protest():
    with open('tests/data/test.html', 'r') as f:
        fullhtml = f.read()
        tree = html.fromstring(fullhtml)

        # For each protest, there is a div with class name "docketSearch". Use
        # this to collect *all* of the protests and create Protest objects.
        protest = etree.tostring(
                    tree.find_class('docketSearch')[0]
                  ).decode('utf-8')
    return protest


def test_protest_text(protest):
    p = Protest(protest)
    assert "Gartner Inc" and "AG-3144-S-15-0086" in p.text


def test_protest_html(protest):
    assert (
        '<h3>Gartner Inc.</h3><table><tbody><tr><td><b>Filed Date</b>:</td>'
        '<td>Dec 22, 2015</td></tr><tr><td><b>Due Date</b>:</td><td>Mar 31,'
        ' 2016</td></tr><tr><td><b>Case Type</b>:</td><td>Bid Protest</td>'
        '</tr><tr><td><b>GAO Attorney</b>:</td><td id="gao-attorney">'
        'Robert T. Wu</td></tr></tbody></table></div>'
        ) in Protest(protest).html
