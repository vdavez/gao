from lxml import etree, html
from lib.gao import GAO
from lib.protest import Protest
import json
import re
import sqlite3

# Initialize the database
db = sqlite3.connect("protests_2023.db")
cursor = db.cursor()

# Initialize the protest table
cursor.execute(
    """CREATE TABLE IF NOT EXISTS protests (
        id INTEGER PRIMARY KEY,
        name TEXT,
        agency TEXT,
        solicitation_number TEXT,
        file_number TEXT,
        outcome TEXT,
        docket_url TEXT,
        filed_date TEXT,
        due_date TEXT,
        date_decided TEXT,
        case_type TEXT,
        gao_attorney TEXT,
        summary TEXT,
        opinion_url TEXT
    )
"""
)

# Initialize the GAO scraper
gao = GAO(start_date="2023-01-01", end_date="2023-09-30")

# Paginate through the docket lists
for docket in gao.generate_all_dockets():
    # We're getting 20 protests here in JSON form...
    # Take the protests and dump them into the database
    for protest in docket:
        try:
            cursor.execute(
                """INSERT INTO protests (
                name,
                agency,
                solicitation_number,
                file_number,
                outcome,
                docket_url,
                filed_date,
                due_date,
                date_decided,
                case_type,
                gao_attorney,
                opinion_url
            ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    protest["name"],
                    protest["agency"],
                    protest.get("solicitation_number", ""),
                    protest["file_number"],
                    protest["outcome"],
                    protest["docket_url"],
                    protest["filed_date"],
                    protest["due_date"],
                    protest["decision_date"],
                    protest["type"],
                    protest["attorney"],
                    protest.get("opinion_url"),
                ),
            )
            db.commit()
        except Exception as err:
            print(f"Protest {protest['name']} failed")
# Close the database
db.close()
