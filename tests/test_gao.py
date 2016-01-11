import pytest
import vcr
import sqlite3
from lib.gao import GAO


class TestGAO():

    def test_initalization(self):
        gao = GAO('2015-01-01', '2015-01-08')
        assert gao.start_date == '2015-01-01'
        assert gao.end_date == '2015-01-08'

    @vcr.use_cassette('tests/data/test-initial-request.yml', record_mode="new_episodes")
    def test_get_docket_list(self):
        gao = GAO(start_date='2015-01-01', end_date='2015-01-08')
        for res in gao.get_docket_list():
            assert res.status_code == 200
            assert "National Veterans Service Bureau" in res.text

    @vcr.use_cassette('tests/data/test-multiple-request.yml', record_mode="new_episodes")
    def test_get_docket_list_multiple(self):
        gao = GAO(start_date='2015-01-01', end_date='2015-01-15')
        res = gao.get_docket_list()
        for res in gao.get_docket_list():
            assert res.status_code == 200
            assert "Science Applications International Corporation" or "Man-Machine Systems Assessment Inc" in res.text

    @vcr.use_cassette('tests/data/test-multiple-request.yml', record_mode="new_episodes")
    def test_get_protests_from_listing(self):
        gao = GAO(start_date='2015-01-01', end_date='2015-01-15')
        res_json = []
        for res in gao.get_docket_list():
            res_json.append(gao.get_protests_from_listing(res.text))
        results = [protest for dockets in res_json for protest in dockets]
        assert results[8]["opinion"].summary is not None
        assert len(results) == 73
