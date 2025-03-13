# ------------------------------------------------
# WatchBase Caliber Scraper (Limited to 1,000 Entries)
# Scrapes up to 1,000 calibers and their specs from https://watchbase.com/calibers
# ------------------------------------------------

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import matplotlib.pyplot as plt


# -----------------------------------------------
# Setup
# -----------------------------------------------
BASE_URL = "https://watchbase.com"
CALIBERS_URL = f"{BASE_URL}/calibers"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

# List to store all scraped data
calibers_data = []


# -----------------------------------------------
# Step 1: Collect up to 1,000 caliber page links
# -----------------------------------------------
def get_caliber_links(max_links=1000):
    print("Collecting caliber links from main page...")
    links = set()  # Use a set to avoid duplicates

    response = requests.get(CALIBERS_URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all 'a' tags with class 'link-color' inside divs with class 'brand-box'
    brand_boxes = soup.find_all('div', class_='brand-box')
    for box in brand_boxes:
        a_tags = box.find_all('a', class_='link-color')
        for a in a_tags:
            href = a['href']

            # ✅ Fix: Only add BASE_URL if it's a relative link
            if href.startswith('/'):
                link = BASE_URL + href
            else:
                link = href  # If already absolute, use as-is

            links.add(link)

            if len(links) >= max_links:
                print(f"✅ Reached target of {len(links)} links. Stopping collection.")
                print(links)
                return list(links)  # Convert set to list

    print(f"Total caliber links found: {len(links)}")
    return list(links)


# -----------------------------------------------
# Step 2: Scrape each caliber page for details
# -----------------------------------------------
def scrape_caliber_details(url):
    print(f"Scraping: {url}")
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the main caliber detail section
    caliber_detail = soup.find('div', id='caliber-detail')

    # Extract Name
    name_tag = caliber_detail.find('h1')
    name = name_tag.text.strip() if name_tag else "N/A"

    # Extract info table rows
    info_table = caliber_detail.find('table', class_='info-table')
    rows = info_table.find_all('tr') if info_table else []

    # Placeholder fields
    brand = movement = display = reserve = frequency = "N/A"

    # Loop through rows to find specific fields
    for row in rows:
        th = row.find('th').text.strip() if row.find('th') else ""
        td = row.find('td').text.strip() if row.find('td') else ""

        if "Brand" in th:
            brand = td
        elif "Movement" in th:
            movement = td
        elif "Display" in th:
            display = td
        elif "Reserve" in th:
            reserve = td
        elif "Frequency" in th:
            frequency = td

    return {
        "Name": name,
        "Brand": brand,
        "Movement": movement,
        "Display": display,
        "Reserve": reserve,
        "Frequency": frequency,
        "URL": url
    }

# -----------------------------------------------
# Plotting function for visualizations
# -----------------------------------------------
def plot_data(csv_file, file_prefix="watchbase"):
    print("\n📊 Generating plots from scraped data...")

    # Load data
    df = pd.read_csv(csv_file)

    # Clean string columns (strip spaces)
    string_cols = ['Movement', 'Display', 'Complications']
    for col in string_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # Convert numeric columns properly
    df['Frequency'] = pd.to_numeric(df['Frequency'], errors='coerce')
    df['Reserve'] = pd.to_numeric(df['Reserve'], errors='coerce')

    # -----------------------------
    # Plot 1: Pie chart for Movement Type Distribution
    # -----------------------------
    plt.figure(figsize=(8, 8))
    df['Movement'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=140)
    plt.title(f'{file_prefix} Movement Type Distribution')
    plt.ylabel('')  # Hide y-axis label
    plt.tight_layout()
    plt.savefig(f'{file_prefix}_movement_pie_chart.png')
    plt.show()

    # -----------------------------
    # Plot 2: Bar chart for Complication Frequency
    # -----------------------------
    if 'Complications' in df.columns:
        plt.figure(figsize=(12, 6))
        df['Complications'].value_counts().head(10).plot(kind='bar', color='coral')
        plt.title(f'{file_prefix} Top 10 Complication Frequency')
        plt.xlabel('Complications')
        plt.ylabel('Count')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(f'{file_prefix}_complication_bar_chart.png')
        plt.show()
    else:
        print("⚠️ 'Complications' column not found. Skipping complication chart.")

    # -----------------------------
    # Plot 3: Histogram of Frequency (Beat Rate)
    # -----------------------------
    plt.figure(figsize=(8, 5))
    df['Frequency'].dropna().plot(kind='hist', bins=15, color='green', edgecolor='black')
    plt.title(f'{file_prefix} Frequency Distribution (vph)')
    plt.xlabel('Frequency (vph)')
    plt.ylabel('Number of Calibers')
    plt.tight_layout()
    plt.savefig(f'{file_prefix}_frequency_histogram.png')
    plt.show()

    # -----------------------------
    # Plot 4: Histogram of Power Reserve
    # -----------------------------
    plt.figure(figsize=(8, 5))
    df['Reserve'].dropna().plot(kind='hist', bins=15, color='purple', edgecolor='black')
    plt.title(f'{file_prefix} Power Reserve Distribution (hours)')
    plt.xlabel('Reserve (hours)')
    plt.ylabel('Number of Calibers')
    plt.tight_layout()
    plt.savefig(f'{file_prefix}_reserve_histogram.png')
    plt.show()

    # -----------------------------
    # Plot 5: Scatter Plot of Reserve vs. Frequency
    # -----------------------------
    plt.figure(figsize=(8, 6))
    plt.scatter(df['Frequency'], df['Reserve'], alpha=0.7, color='blue', edgecolors='black')
    plt.title(f'{file_prefix} Reserve vs. Frequency')
    plt.xlabel('Frequency (vph)')
    plt.ylabel('Power Reserve (hours)')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(f'{file_prefix}_scatter_reserve_vs_frequency.png')
    plt.show()

    print("\n✅ All visualizations generated and saved as PNG files.")

def clean_data():
    # Load dataset
    df = pd.read_csv("raw_data.csv")

    # 1. Strip leading/trailing spaces from all string fields
    string_cols = ['Name', 'Brand', 'Movement', 'Display', 'URL']
    df[string_cols] = df[string_cols].apply(lambda x: x.str.strip())

    # 2. Convert 'Reserve' and 'Frequency' to numeric, coerce errors to NaN
    df['Reserve'] = pd.to_numeric(df['Reserve'], errors='coerce')
    df['Frequency'] = pd.to_numeric(df['Frequency'], errors='coerce')

    # 3. Handle missing values:
    # Drop rows where 'Name' or 'Brand' is missing
    df.dropna(subset=['Name', 'Brand'], inplace=True)

    # Optional: Fill other missing fields (e.g., "Unknown" for movement/display if you prefer)
    df['Movement'] = df['Movement'].fillna('Unknown')
    df['Display'] = df['Display'].fillna('Unknown')

    # 4. Remove duplicates (based on all columns or subset if needed)
    df.drop_duplicates(inplace=True)

    # 5. Standardize text casing (e.g., capitalize brands)
    df['Brand'] = df['Brand'].str.title()  # Capitalize first letter of each word

    # 6. Replace inconsistent placeholders like 'n/a', 'unknown', 'N/A' with NaN
    df.replace(['n/a', 'N/A', 'unknown', 'Unknown'], pd.NA, inplace=True)

    # 7. Summary of cleaned data
    print("✅ Cleaned dataset shape:", df.shape)
    print("\nMissing values:\n", df.isnull().sum())
    print("\nSample data:\n", df.head())

    # 8. Save cleaned dataset
    df.to_csv('cleaned_data.csv', index=False)
    print("\n✅ Cleaned data saved to 'cleaned_data.csv'.")


# -----------------------------------------------
# Main function to coordinate scraping
# -----------------------------------------------
def main_scrape():
    links = get_caliber_links(max_links=1000)  # Limit to 1,000 links
    print("Starting to scrape individual caliber pages...")

    for idx, link in enumerate(links, 1):
        try:
            data = scrape_caliber_details(link)
            print(data)
            calibers_data.append(data)
            print(f"[{idx}/{len(links)}] Scraped: {data['Name']}")
        except Exception as e:
            print(f"Failed to scrape {link} due to error: {e}")

        time.sleep(1)  # Be polite to the server

    # Save data to CSV
    df = pd.DataFrame(calibers_data)
    df.to_csv("raw_data.csv", index=False)
    print("\n✅ Scraping completed. Data saved to 'raw_data.csv'.")


# -----------------------------------------------
# Run the script
# -----------------------------------------------
if __name__ == "__main__":
    main_scrape()  # Run this function to scrape the data
    plot_data("raw_data.csv", "Raw")  # Call plotting function for Raw Data
    clean_data()
    plot_data("cleaned_data.csv", "Cleaned")  # Call plotting function for Cleaned Data



