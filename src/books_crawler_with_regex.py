import logging
import re
import sys
import csv
from html import unescape

import requests


def get_page_content(url):
    """
    getting content of the url page
    """
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        logging.error(e)
    if response.ok:
        return response.text
    logging.error("Can not get content from URL:" + url)


def get_next_page(category_url, category_page_content):
    result = next_page_pat.findall(category_page_content)
    if len(result) == 0:
        return None
    i = category_url.rfind("/")
    return category_url[0:i+1] + result[0]


def crawl_category(content):
    pass


def crawl_website():
    """
    crawl_website is the main function for crawling the website
    """
    base_url = "https://books.toscrape.com"
    content = get_page_content(base_url)

    if content == "":
        logging.critical(f"Empty content from {base_url}")
        sys.exit(1)
    category_list = category_pat.findall(content)

    # for category in category_list
    for category in category_list:
        category_url, category_name = category
        category_url = base_url + "/" + category_url

        while True:
            category_page_content = get_page_content(category_url)
            book_list = book_list_pat.findall(category_page_content)

            # for book in book_list:
            for book in book_list:
                book_url, book_title = book
                book_url = base_url + "/catalogue/" + book_url

                # category and bookname name to csv
                book_dict = {"Category": category_name, "BookName": unescape(book_title)}
                print(f"Scraping category: {category_name} ---- book: {unescape(book_title)}")
                logging.info(f"Scraping from book_list: {book_url}")

                # book URL to csv
                book_dict["BookURL"] = book_url

                book_detail_page_content = get_page_content(book_url)
                # imageurl to csv
                img = img_pat.findall(book_detail_page_content)
                if len(img) == 0:
                    logging.warn(f'ImageUrl not found')
                    img_url = ""
                else:
                    img_url = img[0]
                    img_url = base_url + "/" + img_url

                book_dict['ImageURL'] = img_url

                # UPC to csv
                upc = upc_pat.findall(book_detail_page_content)
                if len(upc) == 0:
                    logging.warn(f'UPC not found')
                    upc = ""
                else:
                    upc = upc[0]

                book_dict['UPC'] = upc

                # price to csv
                price = price_pat.findall(book_detail_page_content)
                if len(price) == 0:
                    logging.warn(f"Price not found")
                    price = ""
                else:
                    price = price[0]

                book_dict['Price'] = price

                # availability to csv
                availability = availability_pat.findall(book_detail_page_content)
                if len(availability) == 0:
                    logging.warn(f"Availability not found")
                    availability = ""
                else:
                    availability = availability[0]

                book_dict['Availability'] = availability

                # description to csv
                desc = description_pat.findall(book_detail_page_content)
                if len(desc) == 0:
                    logging.warn(f'Description not found')
                    desc = ""
                else:
                    desc = unescape(desc[0])

                book_dict['Description'] = desc

                csv_writer.writerow(book_dict)

            next_page = get_next_page(category_url, category_page_content)
            if next_page is None:
                break

            category_url = next_page


if __name__ == "__main__":
    print("###########################start#######################")
    # compile patterns
    category_pat = re.compile(r'<li>\s*<a href="(catalogue/category/books/.*?)">\s*([\s\w]+\w)\s*?<',
                              re.M | re.DOTALL)

    book_list_pat = re.compile(r'<h3>\s*<a href="../../../(.*?)".*?>(.*?)</a>')

    img_pat = re.compile(r'<div class="item active">\s*<img src="../../(.*?)"', re.M | re.DOTALL)

    upc_pat = re.compile(r'<th>UPC</th>\s*<td>(.*?)</td>', re.M | re.DOTALL)

    price_pat = re.compile(r'<th>Price \(incl. tax\)</th>\s*<td>\D+([\d.]+?)</td>')

    availability_pat = re.compile(r'<th>Availability</th>\s*<td>(.*?)</td>')

    description_pat = re.compile(r'<div id="product_description" class="sub-header">.*?<p>(.*?)</p>', re.M | re.DOTALL)

    next_page_pat = re.compile(r'<li class="next">\s*<a href="(.*?)">next</a>')

    # logging
    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%d-%m-%Y %I:%M:%S %p',
                        filename='books.log',
                        level=logging.DEBUG)

    # csv writting
    with open('book_list.csv', 'w', newline='', encoding="ISO-8859-1") as csvf:
        csv_writer = csv.DictWriter(csvf, fieldnames=[
            "Category", "BookName", "BookURL", "UPC", "ImageURL", "Price", "Availability", "Description"])
        csv_writer.writeheader()

        crawl_website()
        print('###########################end#########################')
