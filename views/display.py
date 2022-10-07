#! /usr/bin/env python3
# coding: utf-8

"""This module contains the display class."""

from prettytable import PrettyTable
from api.off import Off
from bdd.bdd_off import Bdd_off
from bdd.bdd_user import Bdd_user

import config.constant as constant


class Display:
    """
    1.

    This class allows the display of the different
    elements of the program.
    """

    def __init__(self):
        """Initialize class that allows communication between user and DB."""
        self.bdduser = Bdd_user()

    def menu_start(self, choice):
        """Show the menu of starting up."""
        while isinstance(choice, int) is False:
            print(constant.message["menu_start"])
            try:
                choice = int(input(constant.message["choice_mes"]))
                if choice < 0 or choice > 4:
                    print(constant.message["error_inv_number"])
                    choice = None
                else:
                    return choice
            except ValueError:
                print(constant.message["error_number"])
                choice = None

    def display_maj_bdd(self):
        """Update the database and displays a message."""
        print(constant.message["maj_BDD"])
        db_off = Bdd_off()
        Off(db_off)

    def printer(self, field_name, data, cat=False, number_page=None):
        """Allow for display formatting."""
        view = PrettyTable()
        view.field_names = field_name

        if cat is True:
            for index, string in enumerate(data):
                view.add_row([index, string])
        else:
            if isinstance(data, tuple) is True:
                data = [data]

            list_view = []
            for index, line in enumerate(data):
                list_view.append(index)
                for column in line:
                    list_view.append(column)
                view.add_row(list_view)
                list_view = []
        print(view)
        if number_page is not None:
            print(constant.message["page_number"] + str(number_page))

    def categories(self):
        """Display the categories available in the constant.py file."""
        self.printer(
            constant.field_names["categorie"],
            constant.categories,
            cat=True)

    def select_cat(self):
        """Allow to select a category."""
        error = True
        while error:
            try:
                select_cat = int(input(constant.message["select_cat"]))
                print(constant.message["standard_mes"],
                      constant.categories[select_cat])
                error = False
                return select_cat
            except IndexError:
                print(constant.message["error_choice"])
            except ValueError:
                print(constant.message["error_number"])

    def search(self, select_cat, paging=False):
        """Allow for a product search."""
        if paging is False:
            text_entered = input(constant.message["search_mes"])
            search = self.bdduser.search_product(
                constant.categories[select_cat],
                text_entered)
            self.printer(constant.field_names["search"], search)
            return search
        else:
            number_page = 1
            choice_page = str()
            while isinstance(choice_page, str) is True:
                search, number_page = self.bdduser.search_product(
                                      constant.categories[select_cat],
                                      text_entered=None,
                                      number_page=number_page)
                self.printer(constant.field_names["search"],
                             search,
                             cat=False,
                             number_page=number_page)
                choice_page = input(constant.message["mes_choice_page"])
                if choice_page == "+" and number_page >= 1:
                    number_page += 1
                elif choice_page == "-"and number_page > 1:
                    number_page -= 1
                else:
                    try:
                        result = self.select_product(choice_page, search)
                        return result
                    except ValueError:
                        print(constant.message["error_number"])
                    except IndexError:
                        print(constant.message["error_index"])

    def select_product(self, product_select, *search):
        """Allow you to select a product in the search result."""
        product_select = int(product_select)
        print(constant.message["standard_mes"])
        self.printer(constant.field_names["search"], search[0][product_select])
        return search[0][product_select]

    def compare_product(self, select_compare):
        """Allow for a similar product search with the selected product."""
        number_page = 1
        choice_page = str()
        while isinstance(choice_page, str) is True:
            compare_response = self.bdduser.compare_product(
                select_compare,
                number_page)
            print(constant.message["standard_mes2"])
            self.printer(constant.field_names["search"], compare_response)
            print(constant.message["select_replace"])
            choice_page = input(constant.message["mes_choice_page"])
            if choice_page == "+"and number_page >= 1:
                number_page += 1
            elif choice_page == "-"and number_page > 1:
                number_page -= 1
            else:
                try:
                    select_product_new = compare_response[int(choice_page)]
                    return select_product_new
                except ValueError:
                    print(constant.message["error_number"])
                except IndexError:
                    print(constant.message["error_index"])

    def save_product(self, result_search, compare_response):
        """
        1.

        Allow the backup of the selected product and the selected
        replacement product.
        """
        self.bdduser.save_product(result_search, compare_response)

    def print_save_product(self, index=None):
        """Allow the display of the saved products."""
        recup = self.bdduser.recup_save_product()
        if index is None:
            list2 = []
            for x in recup:
                list2.append((x[2], x[3]))
            self.printer(constant.field_names["saved"], list2)

        else:
            try:
                index = int(index)
                index1 = recup[index][0]
                index2 = recup[index][1]
                search = self.bdduser.search_product_id(index1)
                search2 = self.bdduser.search_product_id(index2)
                self.printer(constant.field_names["search"], search)
                self.printer(constant.field_names["search"], search2)
                return False
            except IndexError:
                print(constant.message["error_index"])
                return True
            except ValueError:
                print(constant.message["error_number"])
                return True
