import pytest
import vcr
from lxml import html, etree
from lib.protest import Protest


@pytest.fixture
def protest():
    with open("tests/data/test.html", "r") as f:
        fullhtml = f.read()
        tree = html.fromstring(fullhtml)

        # For each protest, there is a div with class name "docketSearch". Use
        # this to collect *all* of the protests and create Protest objects.
        protest = etree.tostring(tree.find_class("docketSearch")[0]).decode("utf-8")
    return protest


@pytest.fixture
def protest_with_decision():
    with open("tests/data/test.html", "r") as f:
        fullhtml = f.read()
        tree = html.fromstring(fullhtml)

        # For each protest, there is a div with class name "docketSearch". Use
        # this to collect *all* of the protests and create Protest objects.
        protest = etree.tostring(tree.find_class("docketSearch")[49]).decode("utf-8")
    return protest


def test_protest_text(protest):
    p = Protest(protest)
    assert "Man-Machine Systems Assessment Inc" == p.data["name"]
    assert "W91CRB-13-R-0009" in p.data["solicitation_number"]


@vcr.use_cassette("tests/data/failing-protest-opinion.yml", record_mode="new_episodes")
def test_protest_get_opinion(protest_with_decision):
    p = Protest(protest_with_decision)
    assert "We deny the request" in p.data["opinion"].summary
    assert (
        "The RFP, issued on April 17, 2014, contemplated the award of a cost-plus-fixed-fee level-of-effort contract for a base year and four 1-year options."
        in p.data["opinion"].decision
    )
