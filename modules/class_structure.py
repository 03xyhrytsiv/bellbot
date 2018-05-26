import json
from urllib.request import urlopen


class Opening:
    MENU = {}

    def __init__(self, data):
        self.data = data

    def wholeMenu(self):
        """
        Creating file with the whole menu
        :return: menu
        """
        for position in self.data:
            self.MENU[position['subCategoryResponse']['categoryResponse']['name']] \
                = dict()

        # Adding subcategories as values of appropriate categories
        for position in self.data:
            category = position['subCategoryResponse']['categoryResponse']['name']
            self.MENU[category].update({position['subCategoryResponse']['name']: []})

        # Adding dishes to an appropriate subcategory
        for position in self.data:
            category = position['subCategoryResponse']['categoryResponse']['name']
            subcategory = position['subCategoryResponse']['name']
            self.MENU[category][subcategory].append(position['name'])

        return self.MENU

    def __str__(self):
        deData = Opening.wholeMenu(self)
        # print(deData)
        return str(deData)


# Reading URL
data = json.loads(urlopen("http://95.46.45.206:8000/public/goods").read())

deluxe = Opening(data)
menu = deluxe.wholeMenu()
