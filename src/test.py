import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/"
response = requests.get(url)
content = response.text
soup = BeautifulSoup(content, "html.parser")

category_list = soup.select(".nav-list li ul li a")

print("Inside loop")
print(len(category_list))
# loop for getting category_link and category_name
for category in category_list:
    category_name = category.getText().strip()
    category_link = category.get("href", "")
    category_link = url + category_link
    print(category_name)
    print(len(category_name))
    print(category_link)

print("Done")

# print(type(category_list))
# print(type(category_list[0]))
# print()
# print(category_list[0].get("href", ""))
# print(category_list[0].getText())
# print(len(category_list[0].getText()))
# print(category_list[0].getText().strip())
# print(len(category_list[0].getText().strip()))
# print(type(category_list[0].getText()))
# print()
# print("Done")
# output
# <class 'bs4.element.ResultSet'>
# <class 'bs4.element.Tag'>
#
# catalogue/category/books/travel_2/index.html
#
#
#                                 Travel
#
#
# 122
# Travel
# 6
# <class 'str'>
#
# Done



