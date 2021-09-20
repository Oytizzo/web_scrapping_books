import re
import requests

url = "https://books.toscrape.com/"
content = requests.get(url).text
# print
# print(content)
# print(len(content))

ul_pat = re.compile(r'<div class="side_categories">(.*?)</div>', re.M | re.DOTALL)
ul_list = ul_pat.findall(content)
ul = ul_list[0]
# print
# print(ul_list)
# print(len(ul_list))
# write to file
# with open('books.html', 'w') as fp:
#     fp.write(ul[0])

category_pat = re.compile(r'<li>\s*<a href="(.*?)">\s*(.*?)\s*</a>', re.M | re.DOTALL)
categories = category_pat.findall(ul)
print(len(categories))
for category in categories:
    print(category[0])
