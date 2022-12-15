# GAO dockets

A client/scraper for GAO bid protests.

## What's the point?

[GAO](http://gao.gov)'s [bid protest decisions](http://gao.gov/legal/bid-protests/search) are awesome. I want to *know* them through data science. But first, I must access all of them and I must build a wrapper/scraper to get them all.

## Data

Although GAO publishes both *dockets* and *decisions* separately, but decision is always part of a docket. So, we will use the search for dockets and then, when there *is* a decision, we'll pull that too.

## Getting set up 

I am now using [Poetry](https://python-poetry.org/) to handle python dependencies. Please make sure you have Poetry installed and then, after getting the repository, run `poetry install`.

## Running tests

We're going to use [pytest](https://docs.pytest.org/en/7.2.x/contents.html), [vcrpy](https://vcrpy.readthedocs.io/en/latest/index.html) and [pytest-vcr](https://pytest-vcr.readthedocs.io/en/latest/) to handle tests.

``` sh
pytest tests/test_gao.py
```