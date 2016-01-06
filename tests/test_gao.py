import pytest
import vcr
import sqlite3
from lib.gao import GAO


class TestGAO():

    def test_initalization(self):
        gao = GAO('2015-01-01', '2015-01-08')
        assert gao.start_date == '2015-01-01'
        assert gao.end_date == '2015-01-08'

    @vcr.use_cassette('tests/data/test-initial-request.yml')
    def test_get_docket_list(self):
        gao = GAO(start_date='2015-01-01', end_date='2015-01-08')
        res = gao.get_docket_list()
        assert res.status_code == 200
        assert "National Veterans Service Bureau" in res.text

    @vcr.use_cassette('tests/data/test-multiple-request.yml')
    def test_get_docket_list_multiple(self):
        gao = GAO(start_date='2015-01-01', end_date='2015-12-31')
        res = gao.get_docket_list()
        assert res.status_code == 200
        assert "National Veterans Service Bureau" not in res.text

    @vcr.use_cassette('tests/data/test-multiple-request.yml')
    def test_get_protests_from_listing(self):
        gao = GAO(start_date='2015-01-01', end_date='2015-12-31')
        res_html = gao.get_docket_list()
        res_json = gao.get_protests_from_listing(res_html.text)
        assert len(res_json) == 50

    @vcr.use_cassette('tests/data/test-multiple-request.yml')
    def test_insert_protests_into_database(self):
        db = sqlite3.connect(':memory:')
        gao = GAO(start_date='2015-01-01', end_date='2015-12-31')
        res_html = gao.get_docket_list()
        res_json = gao.get_protests_from_listing(res_html.text)
