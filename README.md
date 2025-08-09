# 🛍️ Asaxiy.uz Online Market Parser

This Python project is a **web scraper** for the [asaxiy.uz](https://asaxiy.uz) online marketplace.  
It collects detailed product information and saves the data into an **Excel, Notion** file for analysis.

---

## ✅ Extracted Data Fields

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

---
## 📤 Output Formats

The parsed data can be saved in multiple formats:
- **Excel (.xlsx)** – for spreadsheets
- **CSV (.csv)** – for universal data exchange
- **JSON (.json)** – structured format, compatible with Notion and other tools
- **Database (notion)** -  send parsed data directly to a Notion database via API for real-time, shareable, and easily filterable product tracking.
---

## 🧰 Used Libraries

- [`requests`](https://pypi.org/project/requests/) – HTTP requests  
- [`BeautifulSoup`](https://pypi.org/project/beautifulsoup4/) (`bs4`) – HTML parsing  
- [`openpyxl`](https://pypi.org/project/openpyxl/) – Excel export  
- `time`, `random` – delays (anti-bot protection)  
- `re` – regex text processing  
- `json` – optional structured data output

---

## 🗂️ Folder Structure



+ Asaxiy_parser/
+ ├── main.py               # Entry point to run the parser
+ ├── baseparser.py          # Core parsing logic
+ ├── save_to_file.py        # File saving functions (JSON, CSV, Excel)
+ ├── configs.py             # Configurations (URLs, categories, settings)
+ ├── property.py            # Custom classes and data models
+ ├── data/                  # Output data
+ │   ├── Asaxiy database.json
+ │   ├── Asaxiy database.csv
+ │   └── Asaxiy database.xlsx



---

## 📦 Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/username/asaxiy-parser.git
cd asaxiy-parser
pip install -r requirements.txt

## 🚀 How to Run:

Make sure all dependencies are installed. Then run:

```bash
python main.py
