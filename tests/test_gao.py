import pytest
import lxml
from lib.gao import GAO


class TestGAO:
    def test_initalization(self):
        gao = GAO("2021-01-01", "2021-01-08")
        assert gao.start_date == "2021-01-01"
        assert gao.end_date == "2021-01-08"

    @pytest.mark.vcr(record_mode="new_episodes")
    def test_get_dockets_page_list(self):
        gao = GAO("2021-01-01", "2021-01-08")
        protests_page = gao.get_dockets_page_list(0)
        assert len(protests_page) == 20
        assert type(protests_page[0]) == lxml.html.HtmlElement

    @pytest.mark.vcr(record_mode="new_episodes")
    def test_get_all_dockets(self):
        gao = GAO(start_date="2021-01-01", end_date="2021-01-08")
        docket_pages = [page for page in gao.generate_all_dockets()]
        assert len(docket_pages) == 2


"""
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
"""
