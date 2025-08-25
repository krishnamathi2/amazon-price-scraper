
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import sys
import os
import webbrowser
from datetime import datetime

# Use PySimpleGUI for a more reliable UI
try:
    import PySimpleGUI as sg
    HAS_GUI = True
except ImportError:
    HAS_GUI = False

def generate_html_page(data, search_query):
    """Generate an HTML page with product information"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Amazon Products: {search_query}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f7f7f7;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        header {{
            background-color: #232f3e;
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        h1 {{
            margin: 0;
            font-size: 24px;
        }}
        .info {{
            font-size: 14px;
            margin-top: 5px;
            color: #ddd;
        }}
        .products {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }}
        .product {{
            background-color: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
            display: flex;
            flex-direction: column;
        }}
        .product:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        .product-title {{
            padding: 15px;
            font-weight: bold;
            flex-grow: 1;
            border-bottom: 1px solid #eee;
        }}
        .product-price {{
            padding: 15px;
            color: #B12704;
            font-size: 20px;
            font-weight: bold;
        }}
        .product-link {{
            display: block;
            background-color: #ff9900;
            color: white;
            text-align: center;
            padding: 10px;
            text-decoration: none;
            font-weight: bold;
            transition: background-color 0.2s;
        }}
        .product-link:hover {{
            background-color: #e68a00;
        }}
        footer {{
            margin-top: 30px;
            text-align: center;
            font-size: 14px;
            color: #666;
            padding: 20px;
            border-top: 1px solid #ddd;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Amazon Product Search: {search_query}</h1>
            <p class="info">Found {len(data)} products • Generated on {now}</p>
        </header>
        
        <div class="products">
"""
    
    # Add each product
    for product in data:
        title = product.get('Title', 'No Title')
        price = product.get('Price (INR)', 'N/A')
        link = product.get('Product Link', '#')
        
        html += f"""
            <div class="product">
                <div class="product-title">{title}</div>
                <div class="product-price">${price}</div>
                <a href="{link}" target="_blank" class="product-link">View on Amazon</a>
            </div>
"""
    
    # Close HTML
    html += """
        </div>
        
        <footer>
            <p>Data scraped from Amazon.com • Prices and availability subject to change</p>
        </footer>
    </div>
</body>
</html>
"""
    return html

def scrape_amazon_prices(search_query=None):
    # Open amazon.com first
    options = FirefoxOptions()
    options.add_argument("--headless")
    
    # Use relative path or current directory for geckodriver
    import os
    if os.path.exists("geckodriver.exe"):
        # When running as packaged exe
        driver_path = "geckodriver.exe"
    else:
        # When running as script
        driver_path = "C:\\pc\\.venv\\geckodriver.exe"
        
    service = FirefoxService(executable_path=driver_path)
    driver = webdriver.Firefox(service=service, options=options)

    driver.get("https://www.amazon.com")
    time.sleep(2)

    # Prompt for product name
    if not search_query:
        search_query = input("Enter product to search on Amazon: ")
    url = f"https://www.amazon.com/s?k={search_query.replace(' ', '+')}"
    print(f"🔍 Opening {url}")
    driver.get(url)
    time.sleep(3)

    # Screenshot for debugging
    driver.save_screenshot("firefox_amazon_debug.png")
    print("📸 Screenshot saved: firefox_amazon_debug.png")

    wait = WebDriverWait(driver, 10)
    product_elements = driver.find_elements(By.XPATH, '//div[contains(@data-component-type, "s-search-result")]')
    print(f"📦 Found {len(product_elements)} potential product items")

    data = []
    for idx, product in enumerate(product_elements, start=1):
        title = None
        link = None
        # Try to get the product link from <h2><a>
        try:
            a_tag = product.find_element(By.XPATH, './/h2//a')
            link = a_tag.get_attribute('href')
        except:
            pass
        # If not found, try to get any <a> tag inside the product card
        if not link:
            try:
                a_tag = product.find_element(By.XPATH, './/a')
                link = a_tag.get_attribute('href')
            except:
                link = None
        # Ensure full URL
        if link and link.startswith('/'):
            link = f"https://www.amazon.com{link}"

        for xpath in [
            './/span[contains(@class, "a-size-base-plus")]',
            './/span[contains(@class, "a-size-medium")]',
            './/h2//a'
        ]:
            try:
                elem = product.find_element(By.XPATH, xpath)
                title = elem.text
                break
            except:
                continue
        if not title:
            print(f"❌ Skipped item {idx}: No title found")
            continue

        try:
            price_whole = product.find_element(By.XPATH, './/span[@class="a-price-whole"]').text
            price_fraction = product.find_element(By.XPATH, './/span[@class="a-price-fraction"]').text
            price = f"{price_whole}.{price_fraction}"
            data.append({"Title": title, "Price (INR)": price, "Product Link": link})
        except Exception as e:
            print(f"❌ Skipped item {idx}: {e}")
            continue

    driver.quit()

    if data:
        df = pd.DataFrame(data)
        excel_file = "amazon_firefox_prices.xlsx"
        html_file = "amazon_products.html"
        
        # Save to Excel
        df.to_excel(excel_file, index=False)
        print(f"✅ Saved to {excel_file} (with product links)")
        
        # Generate HTML page
        html_content = generate_html_page(data, search_query)
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"✅ Saved to {html_file}")
        
        # Open in browser
        abs_path = os.path.abspath(html_file)
        webbrowser.open('file://' + abs_path)
        
        return True
    else:
        print("⚠️ No valid products scraped — try adjusting CSS or reviewing screenshot.")
        return False


# --- Tkinter UI ---
def run_ui():
    # Define the window layout
    layout = [
        [sg.Text('Enter product to search on Amazon:', font=('Helvetica', 12))],
        [sg.Input(key='QUERY', size=(40, 1))],
        [sg.Button('Scrape Prices', key='SCRAPE'), sg.Button('Cancel')]
    ]
    
    # Create the Window
    window = sg.Window('Amazon Price Scraper', layout, size=(400, 150))
    
    # Event Loop to process events
    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
            
        if event == 'SCRAPE':
            query = values['QUERY']
            if not query.strip():
                sg.popup_error('Please enter a product name.')
                continue
                
            # Disable button during scraping
            window['SCRAPE'].update(disabled=True)
            window.refresh()
            
            # Run scraping
            success = scrape_amazon_prices(query)
            
            # Re-enable button
            window['SCRAPE'].update(disabled=False)
            
            # Show result
            if success:
                sg.popup('Done', 'Prices saved to amazon_firefox_prices.xlsx!')
            else:
                sg.popup_error('No valid products scraped. Check screenshot and try again.')
    
    # Close the window
    window.close()

def run_command_line():
    print("Amazon Price Scraper - Command Line Interface")
    print("--------------------------------------------")
    search_query = input("Enter product to search on Amazon: ")
    if search_query.strip():
        print(f"Searching for: {search_query}")
        success = scrape_amazon_prices(search_query)
        if success:
            print("\n✅ Prices saved to amazon_firefox_prices.xlsx!")
        else:
            print("\n❌ No valid products scraped. Check the screenshot and try again.")
    else:
        print("No product specified. Exiting.")
        
def run_simple_ui():
    """Fallback ultra-simple UI using only standard library"""
    import tkinter as tk
    from tkinter import messagebox
    
    # Create a simple window
    window = tk.Tk()
    window.title("Amazon Price Scraper")
    window.geometry("400x150")
    
    # Add widgets
    tk.Label(window, text="Enter product to search on Amazon:").pack(pady=10)
    entry = tk.Entry(window, width=40)
    entry.pack(pady=5)
    
    def on_scrape():
        query = entry.get()
        if not query.strip():
            messagebox.showwarning("Input Required", "Please enter a product name.")
            return
        
        btn["state"] = "disabled"
        window.update()
        
        success = scrape_amazon_prices(query)
        
        btn["state"] = "normal"
        
        if success:
            messagebox.showinfo("Done", "Prices saved to amazon_firefox_prices.xlsx!")
        else:
            messagebox.showerror("Error", "No valid products scraped. Check screenshot and try again.")
    
    btn = tk.Button(window, text="Scrape Prices", command=on_scrape)
    btn.pack(pady=10)
    
    # Start the main loop
    window.mainloop()

if __name__ == "__main__":
    print("Starting Amazon Price Scraper...")
    
    # Try various UI methods in order of preference
    try_ui = True
    
    if try_ui:
        # First try PySimpleGUI
        if HAS_GUI:
            try:
                print("Launching PySimpleGUI interface...")
                run_ui()
                sys.exit(0)  # Exit if successful
            except Exception as e:
                print(f"PySimpleGUI failed: {e}")
                
        # Then try standard Tkinter
        try:
            print("Trying standard Tkinter UI...")
            run_simple_ui()
            sys.exit(0)  # Exit if successful
        except Exception as e:
            print(f"Tkinter UI failed: {e}")
            
        # Fallback to command line
        print("Falling back to command-line interface...")
    
    # Default to command line interface
    run_command_line()

