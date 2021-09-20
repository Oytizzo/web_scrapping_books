import re

with open('players.html') as f_html:
    content = f_html.read()
    # print(type(content))

    new_content = re.sub(r'\s*(.*?)\s*<ol>\s*<li>(.*?)</li>\s*<li>(.*?)</li>', r'\1 - \2, \3', content)
    # print(type(new_content))
    # print(new_content)

    pat = re.compile(r'<li>\s*(.*?)\s*</ol>')

    player_list = pat.findall(new_content)
    # print(player_list)

    for item in player_list:
        print(item)
