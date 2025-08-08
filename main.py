from save_to_file import SalesParser
import time

def parsing():
    parser = SalesParser()
    html = parser.get_html(parser.url + parser.url_end)

    start = time.time()
    parser.get_data(html)
    finish = time.time()

    print(f"time  : {finish - start:.2f} seconds")

    data = parser.data
    parser.save_data_to_json(data, "Asaxiy database")
    parser.save_data_to_notion_database(data)
    parser.save_data_to_CSV(data, "Asaxiy database")
    parser.save_data_to_excel(data, "Asaxiy database")

parsing()
