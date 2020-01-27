# Seeing Alpha Earnings Call Assignment

This is a crawler for seekingalpha.com Earning Calls.

## Requirements


1. **User inputs:**

    Company name
    Product name

2. **Website:** [seekingalpha.com](seekingalpha.com)

3. **Function(s):**

    Scrape the latest company earnings call transcript and save it as a file on the computer
    Extract sentences containing the Product name and save them in a separate file.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install crawler.

```bash
pip3 install -r requirements.txt
```

## Usage

```bash
python3 extract_seeking_alpha.py
```

## Crawled Earning Calls
You will find the crawled Earning Calls in the `articles` folder with the name of `<company>.txt` file

## Output
You will find the output in the `output` folder with the name of `<company>_<product>.txt` file
