# Exchange-project-

# Books Price Scraper & Converter

A simple Python tool that scrapes book data from a demo site, grabs live exchange rates, and spits out a converted price list in your terminal and a CSV file.

## What it does
1.  **Scrapes:** Pulls the first 10 book titles and prices from `books.toscrape.com`.
2.  **Cleans:** Fixes weird encoding characters and converts price strings to floats.
3.  **Converts:** Hits the `exchangerate-api` to get real-time rates (GBP to KES, USD, etc.).
4.  **Exports:** Saves everything to a CSV so you actually have the data.

## Setup
Make sure you're in your virtual environment, then grab the dependencies:
```bash
pip install requests beautifulsoup4

 ** older Structure
Exchange.py: The main logic.

scraped_XXX.csv: Created after the script runs (contains the final data).

README.md: This file.

Code Logic
get_product_data: Uses a while loop to paginate through the site until 10 books are found.

fetch_rate: Uses the v4 public API to get the latest GBP pairs.

 display_results: Uses f-string padding to make the terminal output look like an actual table.

