from lxml import etree, html
from lib.gao import GAO
from lib.protest import Protest
import json
import re
import sqlite3

# Initialize the database
db = sqlite3.connect("protests.db")
cursor = db.cursor()

# Initialize the protest table
cursor.execute(
    '''CREATE TABLE IF NOT EXISTS protests (
        id INTEGER PRIMARY KEY,
        name TEXT,
        agency TEXT,
        solicitation_number TEXT,
        outcome TEXT,
        docket_url TEXT,
        filed_date TEXT,
        due_date TEXT,
        date_decided TEXT,
        case_type TEXT,
        gao_attorney TEXT,
        summary TEXT,
        decision TEXT
    )
''')

# Initialize the GAO scraper
gao = GAO(start_date="2015-01-01", end_date="2016-01-05")

# Paginate through the docket lists
for res in gao.get_docket_list():

    # Get the paginated docket list
    res_json = gao.get_protests_from_listing(res.text)

    # Take the protests and dump them into the database
    for protest in res_json:
        cursor.execute('''INSERT INTO protests (name, agency, solicitation_number, outcome, docket_url, filed_date, due_date, date_decided, case_type, gao_attorney, summary, decision)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?)''', (protest["name"], protest["agency"], protest.get("solicitation_number", ""), protest["outcome"], protest["docket_url"], protest["filed_date"], protest["due_date"], protest["date_decided"], protest["case_type"], protest["gao_attorney"], protest.get("opinion").summary if protest.get("opinion") else "", protest.get("opinion").decision if protest.get("opinion") else ""))
        db.commit()

# Close the database
db.close()
