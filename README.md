# Kevlarsjal

Kevlarsjal queries get_daily_adjusted data from alpha Vantage and stores data in an pre-installed mysql db

## Getting Started

It now uses only TSX_Composite_Index that is listed on WIKI link(https://en.wikipedia.org/wiki/S%26P/TSX_Composite_Index)

usage: main.py [-h] [-a | -i] index ic type

Kevlarsjal reads index and store data

positional arguments:
  index           index, ej: tsxci
  ic              None if update all. Industry Code sigle word(first 3cha),
                  multi-word(1st cha)
  type            query type, full or compact

optional arguments:
  -h, --help      show this help message and exit
  -a, --all       Update all
  -i, --industry  Update by Industry Code

  example:
  to query bank industry, use:
  python main.py -i tsxci ban compact

to query all securities:
python main.py -i tsxci bs compact

Terms:
tsxci : TSX_Composite_Index
full : full quote, for years data
compact: only today quote

### Prerequisites

a mysql db and alphaVantage framework

## Versioning

We use 1.2.3.0 which is updated with logging and many fixes

## Authors

Colin Zhong


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
