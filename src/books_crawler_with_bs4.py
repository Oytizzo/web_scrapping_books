import csv
import logging

import requests
from bs4 import BeautifulSoup


def crawl_website():
    url = "https://books.toscrape.com/"
    response = requests.get(url)
    content = response.text
    if content == "":
        logging.critical("Got empty content from " + url)
    soup = BeautifulSoup(content, "html.parser")

    category_list = soup.select(".nav-list li ul li a")
    # print("Inside loop")
    # print(len(category_list))

    # loop for getting category_link and category_name
    for category in category_list:
        category_name = category.getText().strip()
        category_link = category.get("href", "")
        category_link = url + category_link
        # print("Category_Name: ", category_name)
        # print(len(category_name))
        # print("Category_Link: ", category_link)

        # csv
        book_dict = {"Category": category_name}
        while True:
            category_page_response = requests.get(category_link)
            category_page_content = category_page_response.text

            category_soup = BeautifulSoup(category_page_content, "html.parser")

            book_list = category_soup.select(".row li h3 a")

            for book in book_list:
                book_name = book.get("title", "")
                book_link = book.get("href", "")
                book_link = "https://books.toscrape.com/catalogue/" + book_link[9:]
                # print("    Book_Name: ", book_name)
                # print("    Book_Link: ", book_link)
                print("Scrapping-- Category: " + category_name + " BookName: " + book_name)
                print("    Book_Link: ", book_link)

                # csv
                book_dict["BookName"] = book_name
                book_dict["BookLink"] = book_link

                book_detail_page_response = requests.get(book_link)
                book_detail_page_content = book_detail_page_response.text

                book_detail_page_soup = BeautifulSoup(book_detail_page_content, "html.parser")

                book_img = book_detail_page_soup.select_one(".item.active img")
                book_img_link = book_img.get("src", "")
                book_img_link = url + book_img_link[6:]
                # print("          book_image_link: ", book_img_link)
                # csv
                book_dict["ImageLink"] = book_img_link

                book_desc = book_detail_page_soup.select_one("article.product_page > p")
                if book_desc is None:
                    book_desc = ""
                else:
                    book_desc = book_desc.getText()
                # print("          book_desc: ", book_desc)
                # csv
                book_dict["BookDescription"] = book_desc
                # upc
                book_upc = book_detail_page_soup.select_one(".table-striped > tr > td")
                if book_upc is None:
                    book_upc = ""
                else:
                    book_upc = book_upc.getText()
                # print("          book_upc: ", book_upc)
                # csv
                book_dict["UPC"] = book_upc
                # price
                book_price = book_detail_page_soup.select_one(".table-striped > tr:nth-of-type(4) > td")
                if book_price is None:
                    book_price = ""
                else:
                    book_price = book_price.getText()
                # print("          book_price: ", book_price)
                # csv
                book_dict["Price"] = book_price
                # availability
                book_availability = book_detail_page_soup.select_one(".table-striped > tr:nth-of-type(6) > td")
                if book_availability is None:
                    book_availability = ""
                else:
                    book_availability = book_availability.getText()
                # print("          book_availability: ", book_availability)
                # csv
                book_dict["Availability"] = book_availability
                csv_writer.writerow(book_dict)

            print("##################################################################")
            next_page = category_soup.select_one(".next a")
            if next_page is None:
                break
            next_page_link = next_page.get("href", None)

            i = category_link.rfind("/")
            category_link = category_link[0:i+1] + next_page_link
            print("Next_page_link: ", category_link)
        print("------------------------------------Next Category--------------------------------")


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%d-%m-%Y %I:%M:%S %p',
                        filename="books_bs4.log",
                        level=logging.DEBUG)

    with open("books_crawler_list_with_bs4.csv", "w", newline='', encoding="ISO-8859-1") as csvf:
        csv_writer = csv.DictWriter(csvf, fieldnames=["Category",
                                                      "BookName",
                                                      "BookLink",
                                                      "ImageLink",
                                                      "BookDescription",
                                                      "UPC",
                                                      "Price",
                                                      "Availability"])
        csv_writer.writeheader()
        # crawl website
        crawl_website()
        print("Done")
