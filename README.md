# Gapminder Historical Estimates

source: http://www.gapminder.org/data/documentation/

In this repo:

* Gapminder Documentation 010 – Maternal mortality

## Problems in year column

in the `year` column, the data type is mixed. There are:

1. a range of years (e.g. 1890-1900)
2. one year (e.g. 1905)

We change the range of years into the middle of the range. So that 
1961-70 becomes 1965

## Errors in source data (2016 version)

below errors should be fixed before running the script.

1. change Australia's 1871-1980, 1881-1990 to 1871-1881 and 1881-1890
2. change New Zealand's 1989-02 to 1898-02
