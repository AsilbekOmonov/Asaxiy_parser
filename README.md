# 🛍️ Asaxiy.uz Online Market Parser

This Python project is a web scraper for the **asaxiy.uz** online marketplace.  
It collects detailed product information and saves the data into an Excel file.

## ✅ Extracted Data Fields:

Each product includes the following fields:
- `name` – product name  
- `attribute` – model or specification info  
- `new_price` – current price  
- `old_price` – previous price (if discounted)  
- `discount` – percentage discount  
- `installment` – monthly installment offer  
- `reviews` – text of top reviews  
- `r_count` – number of reviews  
- `characteristics` – full product description/specs  
- `stars` – rating (1–5 stars)  
- `count` – availability or stock status  
- `link` – direct URL to product

## 🧰 Used Libraries:

- `requests` – for sending HTTP requests  
- `BeautifulSoup` (`bs4`) – for HTML parsing  
- `openpyxl` – for saving data to Excel files  
- `time`, `random` – for delays (anti-bot measures)  
- `re` – regular expressions for text processing
- `json` – optional for structured data output

## 🗂️ Folder Structure (example):

+ Asaxiy_Parser/
+ │
+ ├── main.py # Entry point to run the parser
+ ├── baseparser.py # Core parsing logic
+ ├── configs/ # Configuration files (URLs, categories, etc.)
+ ├── property/ # Custom classes or data models
+ │
+ ├── data/ # Parsed data output (CSV, Excel, etc.)
+ ├── README.md # This file
+ ├── requirements.txt # Required dependencies
+ └── .gitignore # Ignored files and folders


## 🚀 How to Run:

Make sure all dependencies are installed. Then run:

```bash
python main.py