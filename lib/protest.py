from lxml import etree, html
from lib.opinion import Opinion
import json
import re
import requests


class Protest:
    def __init__(self, protestdata):
        self.elems = html.fromstring(protestdata)
        self.get_protest_data()

    def get_protest_data(self):
        self.data = {}
        url = "https://www.gao.gov" + self.elems.xpath("//h4/a/@href")[0].strip()
        self.data["docket_url"] = url
        self.get_data_from_url(url)
        return True

    def get_data_from_url(self, url):
        res = requests.get(url)
        elems = html.fromstring(res.text)

        try:
            self.data["name"] = (
                elems.find_class("field--name-field-protestor")[0]
                .cssselect(".field__item")[0]
                .text_content()
            )

            solicitation = elems.find_class("field--name-field-solicitation-number")
            self.data["solicitation_number"] = ""
            if solicitation != []:
                self.data["solicitation_number"] = (
                    solicitation[0].cssselect(".field__item")[0].text_content()
                )
            # Need to adjust for the SBA, which only has one span
            agency_div = (
                elems.find_class("field--type-entity-reference")[0]
                .cssselect(".field__item")[0]
                .cssselect("span")
            )
            if len(agency_div) == 2:
                self.data["agency"] = (
                    agency_div[0].text_content() + ";" + agency_div[1].text_content()
                )
            else:
                self.data["agency"] = agency_div[0].text_content()
            self.data["file_number"] = (
                elems.find_class("field--type-entity-reference")[1]
                .cssselect(".field__item")[0]
                .text_content()
                .strip()
            )
            self.data["outcome"] = ""
            outcome = elems.find_class("field--name-field-outcome")
            if outcome != []:
                self.data["outcome"] = (
                    outcome[0].find_class("field__item")[0].text_content().strip()
                )

            decision = elems.find_class("field--name-field-decision-date")
            if decision != []:
                self.data["decision_date"] = (
                    decision[0].cssselect("time")[0].get("datetime")
                )
            else:
                self.data["decision_date"] = ""
            self.data["filed_date"] = (
                elems.find_class("field--name-field-filed-date")[0]
                .cssselect("time")[0]
                .get("datetime")
            )
            self.data["due_date"] = (
                elems.find_class("field--name-field-due-date")[0]
                .cssselect("time")[0]
                .get("datetime")
            )
            self.data["type"] = (
                elems.find_class("field--name-field-case-type")[0]
                .cssselect(".field__item")[0]
                .text_content()
            )

            attorney = elems.find_class("field--name-field-gao-attorney")
            self.data["attorney"] = ""
            if attorney != []:
                self.data["attorney"] = (
                    attorney[0].cssselect(".field__item")[0].text_content()
                )

            opinion = elems.find_class("field--name-field-decision-summary")
            self.data["opinion_url"] = ""
            if opinion != []:
                url = "https://www.gao.gov" + opinion[0].cssselect("a")[0].get("href")
                if url != "https://www.gao.gov/legal/bid-protests/faqs":
                    self.data["opinion_url"] = url
        except Exception as error:
            print(error)
            import pdb

            pdb.set_trace()

        return True
