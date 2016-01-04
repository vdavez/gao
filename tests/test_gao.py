import pytest
import vcr
from lib.gao import GAO


class TestGAO():

    def test_initalization(self):
        gao = GAO('2015-01-01', '2015-01-08')
        assert gao.start_date == '2015-01-01'
        assert gao.end_date == '2015-01-08'

    @vcr.use_cassette('tests/test-initial-request.yml')
    def test_get_docket_list(self):
        gao = GAO(start_date='2015-01-01', end_date='2015-01-08')
        res = gao.get_docket_list()
        assert res.status_code == 200
        assert "National Veterans Service Bureau" in res.text
