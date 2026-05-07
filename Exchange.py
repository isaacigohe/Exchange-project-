import requests
from bs4 import BeautifulSoup
import csv

# 1. Scrape 10 books from the website
def get_product_data():
    results = []
    page_num = 1
    
    # Continue until we hit our target of 10 items
    while len(results) < 10:
        url = f"https://books.toscrape.com/catalogue/page-{page_num}.html"
        response = requests.get(url)
        
        # Manual check for page load success
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.find_all('article', class_='product_pod')
            
            if items:
                for item in items:
                    if len(results) < 10:
                        name = item.h3.a['title']
                        # Extract price and clean the currency symbols
                        price_raw = item.find('p', class_='price_color').text
                        price_clean = price_raw.replace('£', '').replace('Â', '').strip()
                        
                        results.append({
                            'name': name,
                            'price_gbp': float(price_clean)
                        })
            else:
                break # No more items found
        else:
            break # Page failed to load
            
        page_num += 1
        
    return results

# 2. Get conversion rate using a simpler public API
def fetch_rate(currency_code):
    # Using the standard exchangerate-api v4 (often doesn't require keys for basic GBP calls)
    api_url = "https://api.exchangerate-api.com/v4/latest/GBP"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        rates = data.get('rates')
        if rates:
            return rates.get(currency_code)
    return None

# 3. Calculate the new prices
def apply_conversion(data_list, target_label, rate_value):
    if rate_value:
        for item in data_list:
            converted = item['price_gbp'] * rate_value
            item['converted_val'] = round(converted, 2)
            item['target_label'] = target_label
    return data_list

# 4. Save results to a CSV file
def export_to_csv(data_list, filename):
    if data_list:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Product Name', 'Price (GBP)', 'Converted Price', 'Currency'])
            for row in data_list:
                writer.writerow([row['name'], row['price_gbp'], row['converted_val'], row['target_label']])
        print(f"\n[File Created]: {filename}")

# 5. Display data in a neat terminal table
def display_results(data_list):
    print("\n" + "="*70)
    print(f"{'Product Title':<40} | {'GBP':<8} | {'Converted':<12}")
    print("-" * 70)
    for row in data_list:
        # Trim title for a clean table look
        short_name = (row['name'][:37] + '..') if len(row['name']) > 37 else row['name']
        print(f"{short_name:<40} | {row['price_gbp']:<8.2f} | {row['converted_val']:<8.2f} {row['target_label']}")
    print("="*70)

# Main Execution Flow
def main():
    print("--- Starting Price Scraper & Converter ---")
    
    # User Input
    choice = input("Enter target currency (e.g. KES, USD, EUR): ").upper().strip()
    if not choice:
        choice = "KES"

    # Step 1: Scrape
    print("Scraping product list...")
    scraped_data = get_product_data()
    
    if scraped_data:
        # Step 2: Get Rate
        print(f"Fetching exchange rate for {choice}...")
        current_rate = fetch_rate(choice)
        
        if current_rate:
            # Step 3: Convert
            final_data = apply_conversion(scraped_data, choice, current_rate)
            
            # Step 4: Save
            export_to_csv(final_data, f"scraped_{choice}.csv")
            
            # Step 5: Show
            display_results(final_data)
        else:
            print(f"Error: Could not find rate for '{choice}'.")
    else:
        print("Error: No data was scraped from the site.")

if __name__ == "__main__":
    main()