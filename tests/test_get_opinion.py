# test_get_opinion.py
import pytest
import vcr
import sqlite3
from lib.opinion import Opinion


@vcr.use_cassette('tests/cassettes/test_opinion/opinion.yml')
def test_get_working_opinion():
    o = Opinion("b-418029,b-418029.2,b-418029.3")
    assert o.summary is not None

@vcr.use_cassette('tests/cassettes/test_opinion/opinion.yml')
def test_get_working_opinion_summary():
    o = Opinion("b-418029,b-418029.2,b-418029.3")
    assert o.summary == ("""Highlights\n  \n    \n22nd Century Technologies, Inc., of McLean, Virginia, protests the establishment of a blanket purchase agreement (BPA) with Deloitte Consulting, LLP, of Arlington, Virginia under request for quotations (RFQ) No. 1605DC-19-Q-00006, issued by the Department of Labor (DOL), for enterprise-wide support services. 22nd Century argues that the agency's evaluation was unreasonable, the agency treated vendors disparately, and the best-value tradeoff was flawed.\n\n\n          \n        We deny the protest.""")

@vcr.use_cassette('tests/cassettes/test_opinion/opinion.yml')
def test_get_working_opinion_decision():
    o = Opinion("b-418029,b-418029.2,b-418029.3")
    # assert False
    assert "General Counsel" in o.decision
