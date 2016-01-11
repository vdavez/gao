# test_get_opinion.py
import pytest
import vcr
import sqlite3
from lib.opinion import Opinion


@vcr.use_cassette('tests/data/working-opinion.yml')
def test_get_working_opinion():
    o = Opinion("B-411916.2")
    assert o.summary is not None


@vcr.use_cassette('tests/data/failing-opinion.yml')
def test_get_failing_opinion():
    o = Opinion("B-412093.2")
    assert o.summary is None


@vcr.use_cassette('tests/data/working-opinion.yml')
def test_get_working_opinion_summary():
    o = Opinion("B-411916.2")
    assert o.summary == ("""West Coast General Corporation (West Coast), of Poway, California, protests the evaluation and selection decision under request for proposals (RFP) No. GS-09P-15-KS-D-00015, issued by the General Services Administration's (GSA), Public Building Service, for repair and alteration services with design-build effort for four designated geographic zones. The protester argues that the agency's evaluation of price proposals and its source selection decision were flawed.\n\n\tWe sustain the protest.""")


@vcr.use_cassette('tests/data/working-opinion.yml')
def test_get_working_opinion_decision():
    o = Opinion("B-411916.2")
    assert "DOCUMENT FOR PUBLIC RELEASE" in o.decision
