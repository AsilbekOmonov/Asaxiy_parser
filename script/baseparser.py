from property import Product_property
from bs4 import BeautifulSoup
import requests
import json
from configs import *
import re
import csv
import pandas as pd



class Baseparser:
    def __init__(self):
        self.url = URL
        self.host = HOST
        self.url_end=url_end

    def get_html(self,link):
        return requests.get(link,headers=headers).text

    @staticmethod
    def save_data_to_json(data,file):
        with open(f"{file}.json",mode="w",encoding="UTF-8") as f:
            json.dump(data,f,ensure_ascii=False,indent=4)

    @staticmethod
    def save_data_to_CSV(data, filename):
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

    @staticmethod
    def save_data_to_excel(data, filename):
        df = pd.DataFrame(data)
        for col in df.columns:
            df[col] = df[col].apply(lambda x: "; ".join([f"{k}: {v}" for k, v in x.items()]) if isinstance(x, dict)
            else "; ".join(map(str, x)) if isinstance(x, list)
            else x)
        df.to_excel(f"{filename}.xlsx", index=False)


class SalesParser(Baseparser):
    def __init__(self):
        super(SalesParser,self).__init__()
        self.data=[]



    def get_data(self,html):
        soup=BeautifulSoup(html,"html.parser")
        products=soup.find_all(*products_link)
        for produkt in products:
            product=Product_property()
            print("--------------------------------------------------------------------------------")

            # Name
            try:
                product.name = produkt.find(*name_link).get_text(strip=True)
            except Exception as e:
                print(e)
                product.name = "Unknown"
            print("Name   :  " + product.name)


            # Attribut
            try:
                product.attribute = produkt.find(*attribute_link).get_text(strip=True)
            except Exception as e:
                print(e)
                product.attribute = "Standard"
            print("Attribute     :" + product.attribute)


            # Staraya cena
            try:
                product.old_price = int(produkt.find(*old_price_link).get_text().replace(" ", "").replace("сум", ""))
            except Exception as e:
                print(e)
                product.old_price = "Unavailable"
            print(f"Old price  : {product.old_price}")


            # Novaya Cena
            try:
                product.new_price = int(produkt.find(*new_price_link).get_text().replace(" ", "").replace("сум", ""))
            except Exception as e:
                print(e)
                product.new_price = "Unavailable"
            print(f"New price  : {product.new_price}")


            # Skidka
            try:
                product.discount = 100 - int(product.new_price * 100 / product.old_price)
            except Exception as e:
                print(e)
                product.discount = "No discount"
            print(f"Discount : {product.discount}%")


            # Rassrochka
            try:
                str_inst = produkt.find(installment_link).get_text(strip=True)
                match = re.search(r'(\d[\d\s]+сум)\s*x\s*\d+\s*мес', str_inst)
                product.installment = match.group()
            except Exception as e:
                print(e)
                product.installment = "Unavailable"
            print(f"Installment : {product.installment}")


            # Kolichestvo otzivov
            try:
                r_count_block = produkt.find(*r_count_link)
                span = r_count_block.find("span")
                product.r_count = int(span.get_text(strip=True).replace(" отзывов", ""))
            except Exception as e:
                print(e)
                product.r_count = "Unknown"
            print(f"Reviews count : {product.r_count}")


            # Kolichestvo zvyozdv
            try:
                rating_block = produkt.find(*stars_link)
                product.stars = 0
                if rating_block:
                    stars = rating_block.find_all("i")
                    for star in stars:
                        class_list = star.get("class", [])
                        if "fas" in class_list and "fa-star" in class_list:
                            product.stars += 1
            except Exception as e:
                print(e)
                product.stars = 0
            print(f"Stars : {product.stars}")


            # Ssilka
            try:
                if produkt.find("a", href=True):
                    product.link = self.host + produkt.find(*link_link)["href"]
            except Exception as e:
                print(e)
                product.link = "No link"
            print(product.link)


            # Product page
            try:
                html_ = requests.get(product.link,headers=headers).text
                inter_html = BeautifulSoup(html_, "html.parser")
            except Exception as e:
                print(e)
                print("-------------------------Product page error!!-------------------------")


            # Nalichiye
            try:
                elements = inter_html.find_all(*count_link)
                for el in elements:
                    text = el.get_text(strip=True)
                    if "В наличии" in text or "Нет в наличии" in text:
                        product.count = text.replace("● ", "")
                        break
            except Exception as e:
                print(e)
                product.count = "Unavailable"
            print(product.count)


            # Otzivi
            try:
                revs = inter_html.find_all(*reviews_link)
                product.reviews={}
                for review in revs:
                    key_txt= review.find(*review_name_link).get_text(strip=True)
                    value_txt = review.find(*review_link).get_text(strip=True)
                    product.reviews[key_txt]=value_txt
                print("Reviews: ", product.reviews)
            except Exception as e:
                print(e)
                product.reviews = "No reviews"


            # Xarakteristiki
            product.characteristics = {}
            try:
                ch_block = inter_html.find(*characteristics_link)
                ch_text = ch_block.find_all("tr")
                for text in ch_text:
                    key_tx = text.find("td", class_="text-left").get_text(strip=True)
                    value_tx = text.find("td", class_="text-right").get_text(strip=True)
                    product.characteristics[key_tx]=value_tx
            except Exception as e:
                print(e)
            print(f"Harakteristiki:  {product.characteristics}")


            # Sohraneniye
            self.data.append({
                "name": product.name,
                "attribute": product.attribute,
                "new_price": product.new_price,
                "old_price": product.old_price,
                "discount": product.discount,
                "installment": product.installment,
                "stars": product.stars,
                "count": product.count,
                "r_count": product.r_count,
                "reviews": product.reviews,
                "characteristics": product.characteristics,
                "link": product.link
            })