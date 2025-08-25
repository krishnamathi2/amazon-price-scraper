# Amazon Price Scraper

A powerful tool that scrapes Amazon product prices based on search queries and provides a clean, user-friendly interface to view and save results.

![Amazon Price Scraper](https://img.shields.io/badge/Amazon-Price%20Scraper-orange?style=for-the-badge&logo=amazon)

## Features

- 🔍 Search for products on Amazon
- 💰 Extract product prices automatically
- 🔗 Capture direct links to product pages
- 📊 Save results to Excel spreadsheet
- 🌐 Generate attractive web page with product listings
- 💻 Clean user interface with both GUI and command-line options

## Screenshots

(Add screenshots of your application here)

## Installation

### Option 1: Using the packaged application

1. Download the latest release ZIP file
2. Extract all files to a folder
3. Run `AmazonPriceScraper.bat` or create a shortcut using `CreateShortcut.vbs`

### Option 2: From source code

```bash
# Clone this repository
git clone https://github.com/yourusername/amazon-price-scraper.git

# Navigate to the project directory
cd amazon-price-scraper

# Install required packages
pip install -r requirements.txt

# Run the application
python aps.py
```

## Requirements

- Python 3.6+
- Firefox browser
- Required Python packages:
  - selenium
  - pandas
  - tkinter (standard library)

## Usage

1. Launch the application
2. Enter a product name in the search field
3. Click "Scrape Prices"
4. Wait for the scraping to complete
5. View the results in the automatically generated web page
6. Find the Excel file with all data in the same directory

## How It Works

The application uses Selenium WebDriver to:
1. Open Amazon's website
2. Input search query
3. Parse product information from search results
4. Extract titles, prices, and product links
5. Save data to Excel and generate HTML report

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This tool is for educational purposes only. Use responsibly and in accordance with Amazon's Terms of Service.
