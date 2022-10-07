#! /usr/bin/env python3
# coding: utf-8

"""Start.py is the program launch file."""

from views.display import Display
import config.constant as constant

if __name__ == "__main__":
    display = Display()
    choice = None
    select_cat = None
    while choice != 4:
        choice = display.menu_start(choice)

        if choice == 1:
            display.display_maj_bdd()
            choice = None

        elif choice == 2:
            display.categories()
            select_cat = display.select_cat()

            result_search = display.search(select_cat, paging=True)
            select_compare = [result_search[0],
                              constant.categories[select_cat],
                              result_search[3]
                              ]
            compare_response = display.compare_product(select_compare)

            print(constant.message["standard_mes"])
            display.printer(constant.field_names["search"], result_search)
            print(constant.message["product_replace"])
            display.printer(constant.field_names["search"], compare_response)

            save = input(constant.message["save_mes"]).lower()
            save = save[0]
            if save == "o":
                display.save_product(result_search[0], compare_response[0])
            choice = None
            select_cat = None

        elif choice == 3:
            error = True
            while error:
                display.print_save_product()
                index = input(constant.message["select_index"])
                error = display.print_save_product(index)

        elif choice == 4:
            print(constant.message["exit_mes"])
