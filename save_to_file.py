import csv
import pandas as pd
from notion_client import Client
import json

import configs
from baseparser import Baseparser
from configs import notion_token,notion_database_id


def if_change_tipy(item):
    if isinstance(item, int):
        return str(item)
    return item

class SalesParser(Baseparser):
    def __init__(self):
        super(SalesParser, self).__init__()




    def save_data_to_json(self, data, file):
        with open(f"{file}.json", mode="w", encoding="UTF-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)




    def save_data_to_CSV(self, data, filename):
        fieldnames = data[0].keys()
        with open(f"{filename}.csv", "w", newline='', encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                cleaned_row = {}
                for key, value in row.items():
                    if isinstance(value, (list, dict)):
                        cleaned_row[key] = json.dumps(value, ensure_ascii=False)
                    else:
                        cleaned_row[key] = value
                writer.writerow(cleaned_row)




    def save_data_to_excel(self, data, filename):
        df = pd.DataFrame(data)
        for col in df.columns:
            df[col] = df[col].apply(
                lambda x: "; ".join([f"{k}: {v}" for k, v in x.items()]) if isinstance(x, dict)
                else "; ".join(map(str, x)) if isinstance(x, list)
                else x
            )
        df.to_excel(f"{filename}.xlsx", index=False)

    def save_data_to_notion_database(self, data):
        notion = Client(auth=configs.notion_token)
        database_id = configs.notion_database_id

        def add_pr(item):
            if isinstance(item, int) or isinstance(item, float):
                return f"{item}%"
            return item or ""

        def if_change_tipy(value):
            if isinstance(value, (int, float)):
                return str(value)
            if value is None:
                return ""
            return str(value)

        for product in data:
            try:
                children_blocks = []

                # harakteristiki
                if "characteristics" in product and isinstance(product["characteristics"], dict) and product[
                    "characteristics"]:
                    children_blocks.append({
                        "object": "block",
                        "type": "heading_2",
                        "heading_2": {
                            "rich_text": [{"type": "text", "text": {"content": "Характеристики"}}]
                        }
                    })
                    children_blocks.append({
                        "object": "block",
                        "type": "table",
                        "table": {
                            "table_width": 2,
                            "has_column_header": True,
                            "has_row_header": False,
                            "children": [
                                            {
                                                "object": "block",
                                                "type": "table_row",
                                                "table_row": {
                                                    "cells": [
                                                        [{"type": "text", "text": {"content": "Характеристика"}}],
                                                        [{"type": "text", "text": {"content": "Значение"}}]
                                                    ]
                                                }
                                            }
                                        ] + [
                                            {
                                                "object": "block",
                                                "type": "table_row",
                                                "table_row": {
                                                    "cells": [
                                                        [{"type": "text", "text": {"content": str(key)}}],
                                                        [{"type": "text", "text": {"content": str(value)}}]
                                                    ]
                                                }
                                            } for key, value in product["characteristics"].items()
                                        ]
                        }
                    })



                # otzivi
                if "reviews" in product and isinstance(product["reviews"], dict):
                    children_blocks.append({
                        "object": "block",
                        "type": "heading_2",
                        "heading_2": {
                            "rich_text": [{"type": "text", "text": {"content": "Отзывы"}}]
                        }
                    })
                    children_blocks.append({
                        "object": "block",
                        "type": "table",
                        "table": {
                            "table_width": 2,
                            "has_column_header": True,
                            "has_row_header": False,
                            "children": [
                                            {
                                                "object": "block",
                                                "type": "table_row",
                                                "table_row": {
                                                    "cells": [
                                                        [{"type": "text", "text": {"content": "Автор"}}],
                                                        [{"type": "text", "text": {"content": "Отзыв"}}]
                                                    ]
                                                }
                                            }
                                        ] + [
                                            {
                                                "object": "block",
                                                "type": "table_row",
                                                "table_row": {
                                                    "cells": [
                                                        [{"type": "text", "text": {"content": str(author)}}],
                                                        [{"type": "text", "text": {"content": str(text)}}]
                                                    ]
                                                }
                                            } for author, text in product["reviews"].items()
                                        ]
                        }
                    })




                notion.pages.create(
                    parent={"database_id": database_id},
                    properties={
                        "Name": {
                            "title": [{
                                "text": {
                                    "content": product.get("name", "no name")
                                }
                            }]
                        },
                        "image": {
                            "files": [{
                                "type": "external",
                                "name": "Product Image",
                                "external": {"url": product.get("image", "")}
                            }]
                        },
                        "attribute": {
                            "rich_text": [{
                                "text": {
                                    "content": product.get("attribute", "")
                                }
                            }]
                        },
                        "new price": {
                            "number": product.get("new_price", 0)
                        },
                        "old price": {
                            "rich_text": [{
                                "text": {
                                    "content": if_change_tipy(product.get("old_price"))
                                }
                            }]
                        },
                        "discount": {
                            "rich_text": [{
                                "text": {
                                    "content": add_pr(product.get("discount"))
                                }
                            }]
                        },
                        "installment": {
                            "rich_text": [{
                                "text": {
                                    "content": product.get("installment", "")
                                }
                            }]
                        },
                        "stars": {
                            "number": product.get("stars", 0)
                        },
                        "count": {
                            "rich_text": [{
                                "text": {
                                    "content": if_change_tipy(product.get("count"))
                                }
                            }]
                        },
                        "reviews count": {
                            "number": product.get("r_count", 0)
                        },
                        "link": {
                            "url": product.get("link", "")
                        }
                    },
                    children=children_blocks if children_blocks else None
                )

                print(f"✅ {product.get('name')} dobavlen")
            except Exception as e:
                print(f"❌|{product.get('name')}| ne dobavleno\n oshibka: {e}")
