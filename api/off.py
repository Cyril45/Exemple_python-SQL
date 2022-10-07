#! /usr/bin/env python3
# coding: utf-8

"""Allow interaction between program and API."""

import config.constant as constant
import requests


class Off:
    """
    1.

    This Class allows to communicate with
    the OpenFoodFact API and insert data in BDD.
    """

    def __init__(self, my_db):
        """
        1.

        Recovers categories, login to database and
        launches API data reading.
        """
        self.categories = constant.categories
        self.database = my_db
        self.read_values_off()

    def read_values_off(self):
        """Read the API data."""
        params_get = {
                    "action": "process",
                    "tagtype_0": "categories",
                    "tag_contains_0": "contains",
                    "page_size": "1000",
                    "json": "1"
                }
        for values in constant.categories:
            params_get["tag_0"] = values
            read = requests.get(
                            'https://world.openfoodfacts.org/cgi/search.pl',
                            params=params_get
                            )
            data = read.json()
            self.push_values_in_bdd(data, values)

    def push_values_in_bdd(self, data, values):
        """Send API data to database."""
        columns = ("id",
                   "product_name_fr",
                   "generic_name_fr",
                   "ingredients_text_with_allergens_fr",
                   "nutrition_grade_fr",
                   "categories",
                   "last_edit_dates_tags",
                   "url")
        for d in data["products"]:
            map(str.strip, d)
            product_data = []
            not_ok = False
            for c in columns:
                if c in d.keys():
                    if not d.get(c):
                        not_ok = True
                        break
                    else:
                        product_data.append(d.get(c))
            product_data.insert(1, values)
            if not_ok is False and len(product_data) == 9:
                product_data[7] = product_data[7][0]
                self.database.insert_data(product_data)
