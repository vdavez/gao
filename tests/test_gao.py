import json
import pytest
import lxml
from lib.gao import GAO


class TestGAO:
    def test_initalization(self):
        gao = GAO("2021-01-07", "2021-01-08")
        assert gao.start_date == "2021-01-07"
        assert gao.end_date == "2021-01-08"

    @pytest.mark.vcr(record_mode="once")
    def test_get_dockets_page_list(self):
        gao = GAO("2021-01-07", "2021-01-08")
        protests_page = gao.get_dockets_page_list(0)
        with open ("tests/data/test.json","r") as fp:
            data = json.load(fp)
            assert protests_page == data

    @pytest.mark.vcr(record_mode="none")
    def test_get_all_dockets(self):
        gao = GAO(start_date="2021-01-01", end_date="2021-01-08")
        docket_pages = [page for page in gao.generate_all_dockets()]
        assert len(docket_pages) == 2
