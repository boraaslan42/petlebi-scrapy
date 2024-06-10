import scrapy
import json
from bs4 import BeautifulSoup

#Bora Aslan

class PetlebiSpider(scrapy.Spider):
    name = "petlebi"
    allowed_domains = ["www.petlebi.com"]
    headers = {
        "authority": "www.petlebi.com",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        "cookie": "_gcl_au=1.1.411432945.1711450844; personaclick_session_code=NiGTbrA1FX; personaclick_device_id=RkX51iBvWr; personaclick_lazy_recommenders=true; _gid=GA1.2.254193501.1711450845; _clck=fj1n24^%^7C2^%^7Cfke^%^7C0^%^7C1546; _ym_uid=1711450845675037289; _ym_d=1711450845; __storejs_infosetChatWidget__iVisitorId=^%^22e6a06e7f-398c-4764-b2bb-11c034b061da^%^22; _ym_isad=1; personaclick_session_last_act=1711450905819; personaclick-popup-264=showed; _ga=GA1.2.1378935571.1711450845; _dc_gtm_UA-52763134-1=1; acceptCookies=true; _clsk=1481fo1^%^7C1711450910245^%^7C3^%^7C1^%^7Cm.clarity.ms^%^2Fcollect; XSRF-TOKEN=eyJpdiI6IkpUdWYzTE80T0NNZDNOV2N6VEdDVWc9PSIsInZhbHVlIjoiZ3ZLVVZ5NnlZN2VYS0hlMDdlQi9LeWdsK1k5RFRjZXNXaUZrMzRoaWdrYy8yU0M4RGZKV2FScG9XY1EzRnVhUmlCeVNJaDRHaUZkbkUzME9JazVrMmlwTC9SWndJS2F6djh0bERReDhtZVFHc1V1YXgwVXZldFQyRzFBei9wczUiLCJtYWMiOiI5YTMyYWNhNTUzMGU5MzAyNjg2Y2RjYTVjZmI2ODU4MDlkNjg1MzNmM2Q3OGI5NmI0Y2YwMTY2MDVjNTE4ZWNlIiwidGFnIjoiIn0^%^3D; psession=eyJpdiI6Im84dlpmR0J1YXRHb3dnUmROazJaWlE9PSIsInZhbHVlIjoiQTNRc3VDVmlycDByMm5IaE9tNmhyR0toT2NtaURTR3FlZ05Wc05KUEttR25ZUU1jSnJZeHlwTWlGK2Q3NXA3UXFjbEgyQVpRT3lETkJsVGxoRWVmQVA5VzdHSzFON3gyRWV0cVVIaWhWK0xHeFU0Q2pBT3dRVGhVS0hPUXJlYnoiLCJtYWMiOiJjYTg4MGRmYWM1MTA3Nzg4MjNjZGE4ZDU3NTUwZjAwNmEzZjM3ZTc0MzYxNGQ5NGU4ZTg1MWVjNjA4ZTAwZDhhIiwidGFnIjoiIn0^%^3D; _ga_9YMCTF3FJH=GS1.2.1711450844.1.1.1711450921.45.0.0; _ga_PKY713P156=GS1.1.1711450844.1.1.1711450921.44.0.0",
        "referer": "https://www.petlebi.com/alisveris/ara?page=1",
        "sec-ch-ua": '^"Not A(Brand^";v=^"99^", ^"Opera GX^";v=^"107^", ^"Chromium^";v=^"121^"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '^"Windows^"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0",
        "x-requested-with": "XMLHttpRequest",
    }
    num_of_pages = 0
    
    #Spider checks for the number of pages in the website and then extracts the product links and their json data
    def start_requests(self):
        url = "https://www.petlebi.com/alisveris/ara?page=0&op=json"
        yield scrapy.Request(
            url=url, headers=self.headers, callback=self.extract_num_of_pages
        )
    
    def extract_num_of_pages(self, response):
        json_data = json.loads(response.text)
        soup = BeautifulSoup(json_data["response"], "html.parser")
        links = BeautifulSoup(soup.div["data-pagination"], "html.parser").find_all("li")
        self.num_of_pages = int(links[-2].text)
        for i in range(1, self.num_of_pages + 1):
            # for i in range(1, 2):
            url = f"https://www.petlebi.com/alisveris/ara?page={i}&op=json"
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse)
            
    #With the scraped number of pages, spider extracts the product links from each page with pagination and also data for every product 
    # which is not reachable or more costful to reach in products own page
    def parse(self, response):
        json_data = json.loads(response.text)
        soup = BeautifulSoup(json_data["response"], "html.parser")
        soup.find_all("a", class_="p-link")[2]["data-gtm-product"]
        products = soup.find_all("a", class_="p-link")
        product_urls = [product["href"] for product in products]
        productJsons = soup.find_all("a", class_="p-link")

        json_meta_list = []
        for product in productJsons:
            product_json = json.loads(product["data-gtm-product"])
            json_meta = {
                "id": product_json["id"],
                "name": product_json["name"],
                "category": product_json["category"],
                "brand": product_json["brand"],
                "price": product_json["price"],
            }
            json_meta_list.append(json_meta)

        for productZip in zip(product_urls, json_meta_list):

            yield scrapy.Request(
                url=productZip[0], callback=self.parse_product, meta=productZip[1]
            )
    #Spider extracts the product data from the product page and merges it with the data extracted from the product list page
    def parse_product(self, response):

        product_json = response.meta
        soup = BeautifulSoup(response.text, "html.parser")

        productName = product_json["name"]
        description = (
            soup.find("div", id="hakkinda")
            .find("span", id="productDescription")
            .text.replace("\n", " ")
            .strip()
        )

        productURL = soup.find("link", rel="canonical")["href"]
        try:
            productStock = soup.find_all("option")[-1].text.split(" ")[0]
        except:
            productStock = "Out of Stock"

        category = product_json["category"]

        productID = product_json["id"]

        brand = product_json["brand"]
        productImages = tuple()
        for link in soup.find(
            "div", class_=lambda x: x and "MagicScroll" in x
        ).find_all("img"):
            image_link = "https:" + link["src"].replace("xs", "lg")
            productImages += (image_link,)

        productPrice = product_json["price"]
        for i in soup.find("div", id="hakkinda").find_all("div", class_="row mb-2"):
            if i.find("div", class_="col-2 pd-d-t").text == "BARKOD":
                sku = i.find("div", class_="col-10 pd-d-v").text

        productDict = {
            "Product URL": productURL,
            "Product Name": productName,
            "Product Barcode": sku,
            "Product Price": productPrice,
            "Product Stock": productStock,
            "Description": description,
            "SKU": sku,
            "Category": category,
            "Product ID": productID,
            "Brand": brand,
            "Product Images": productImages,
        }

        yield productDict
