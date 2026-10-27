
from html.parser import HTMLParser
import re
import json
import os


class ProductParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.products = []
        self.current = {}
        self.capture = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        if "product" in attrs.get("class", "").lower():
            self.current = {}
        if "name" in attrs.get("class", "").lower():
            self.capture = "name"
        elif "price" in attrs.get("class", "").lower():
            self.capture = "price"
        elif "rating" in attrs.get("class", "").lower():
            self.capture = "rating"

    def handle_data(self, data):
        if self.capture:
            value = data.strip()
            if value:
                self.current[self.capture] = value

    def handle_endtag(self, tag):
        if self.capture == "rating":
            if all(key in self.current for key in ("name", "price", "rating")):
                self.products.append(self.current.copy())
                self.current = {}
        self.capture = None


def parse_products(path):
    parser = ProductParser()
    with open(path, "r", encoding="utf-8", errors="ignore") as file:
        parser.feed(file.read())

    return parser.products


def main():
    try:
        p, k = map(int, input().split())

        if not 1 <= p <= 5000 or not 1 <= k <= 1000:
            print("Invalid input")
            return

        products = {}

        for _ in range(p):
            path = input().strip()

            if not os.path.isfile(path):
                print("File not found:", path)
                return

            for item in parse_products(path):
                name = item["name"].strip()
                price_text = re.sub(r"[^\d.]", "", item["price"])
                price = float(price_text)
                rating = float(item["rating"])

                if not 0 <= rating <= 5 or price < 0:
                    continue

                product = {
                    "name": name,
                    "price": price,
                    "rating": rating
                }

                if name not in products or rating > products[name]["rating"]:
                    products[name] = product
                elif rating == products[name]["rating"] and price < products[name]["price"]:
                    products[name] = product

        ranked = sorted(
            products.values(),
            key=lambda x: (-x["rating"], x["price"], x["name"])
        )

        for item in ranked[:k]:
            price = item["price"]
            price = int(price) if price.is_integer() else price
            print(item["name"], price, item["rating"])

    except (ValueError, OSError) as error:
        print("Error:", error)


if __name__ == "__main__":
    main()
