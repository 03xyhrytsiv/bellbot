from urllib.request import urlopen
import json


data = urlopen("http://95.46.45.206:8000/public/goods").read()
data = json.loads(data)
europeanKitchen = []
japaneseKitchen = []
desserts = []
drinks = []
pisneMenu = []
with open("jsonFile.json", "w") as file:
    json.dump(data, file, indent=4)

for dicts in data:
    if dicts['subCategoryResponse']['categoryResponse']['name']\
            == 'Європейська Кухня':
        europeanKitchen.append(dicts)
    if dicts['subCategoryResponse']['categoryResponse']['name'] \
            == 'Десерти':
        desserts.append(dicts)
    if dicts['subCategoryResponse']['categoryResponse']['name'] \
            == 'Напої':
        drinks.append(dicts)
    if dicts['subCategoryResponse']['categoryResponse']['name']\
            == 'Пісне Меню':
        pisneMenu.append(dicts)
    if dicts['subCategoryResponse']['categoryResponse']['name'] \
            == 'Японська Кухня':
        japaneseKitchen.append(dicts)
