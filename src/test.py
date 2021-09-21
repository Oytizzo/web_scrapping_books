import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/"
response = requests.get(url)
content = response.text
soup = BeautifulSoup(content, "html.parser")

category_list = soup.select(".nav-list li ul li a")

print(type(category_list))
print(type(category_list[0]))
print()
print(category_list[0].get("href", ""))
print(category_list[0].getText())
print(len(category_list[0].getText()))
print(type(category_list[0].getText()))
print()
print("Done")

# output
# <class 'bs4.element.ResultSet'>
# <class 'bs4.element.Tag'>
# {'href': 'catalogue/category/books/travel_2/index.html'}
# Done
