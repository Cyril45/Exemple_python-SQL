#! /usr/bin/env python3
# coding: utf-8

"""
1.

This module contains the communication classes
between the BDD and the user.
"""

import mysql.connector
import config.constant as constant


class Bdd_user:
    """This class allows the user to communicate with the database."""

    def __init__(self):
        """Initialize the connection to the database."""
        self.config_DB_and_base = constant.conn.copy()
        self.config_DB_and_base["database"] = constant.name_base
        self.connect_db = mysql.connector.connect(
                            **self.config_DB_and_base)
        self.cursor = self.connect_db.cursor(buffered=True)

    def search_product(self,
                       cat,
                       text_entered=None,
                       number_page=1,
                       search_save=False):
        """Allow product search by pagination or text."""
        limit = 10
        offset = (number_page * limit) - limit
        if text_entered is not None:
            self.cursor.execute("SELECT id, nom, description, indice,\
                                date_update, url FROM products WHERE nom\
                                LIKE '%{}%' AND categorie LIKE '{}' LIMIT {}\
                                OFFSET {};".format(
                                            text_entered,
                                            cat,
                                            limit,
                                            offset))
            result = self.cursor.fetchall()
            return result

        else:
            self.cursor.execute("SELECT id, nom, description, indice,\
                                date_update, url FROM products WHERE categorie\
                                LIKE '{}' LIMIT {} OFFSET {};".format(
                                                                      cat,
                                                                      limit,
                                                                      offset))
            result = self.cursor.fetchall()
            return result, number_page

    def search_product_id(self, id):
        """Allow product search by ID."""
        self.cursor.execute("SELECT id, nom, description, indice, date_update,\
                             url FROM products WHERE id LIKE '{}';".format(id))
        result = self.cursor.fetchall()
        return result

    def compare_product(self, receive, number_page):
        """Allow product search by comparison."""
        limit = 10
        offset = (number_page * limit) - limit
        if len(receive) <= 3:
            receive.append(limit)
            receive.append(offset)
        else:
            receive[3] = limit
            receive[4] = offset

        self.cursor.execute("SELECT DISTINCT id_cat FROM cat_product\
                             WHERE id_product = '{}';".format(receive[0]))
        result_id_cat = self.cursor.fetchall()
        list_id_cat = [str(i[0]) for i in result_id_cat]

        self.cursor.execute("SELECT DISTINCT id_ing FROM ing_product WHERE\
                            id_product = '{}';".format(receive[0]))
        result_id_ing = self.cursor.fetchall()
        list_id_ing = [str(i[0]) for i in result_id_ing]

        query = "SELECT DISTINCT products.id, products.nom, products.description,\
        products.indice, products.date_update, products.url \
        FROM products \
        INNER JOIN cat_product \
        ON cat_product.id_product = products.id \
        INNER JOIN ing_product \
        ON ing_product.id_product = products.id WHERE cat_product.id_cat IN ("
        query += ",".join(list_id_cat)
        query += ") AND ing_product.id_ing IN("
        query += ",".join(list_id_ing)
        query += ") AND products.id != %s AND products.categorie = %s\
        AND products.indice <= %s ORDER BY products.indice LIMIT %s OFFSET %s;"
        self.cursor.execute(query, receive)
        return self.cursor.fetchall()

    def save_product(self, select_product, select_product_new):
        """Allow product backup."""
        self.cursor.execute("INSERT INTO products_save VALUES (NULL, {}, {});"
                            .format(select_product, select_product_new))
        self.connect_db.commit()

    def recup_save_product(self):
        """Allow the recovery of products backup."""
        self.cursor.execute("""SELECT products_save.id_product, products_save.id_save_product, a.nom, b.nom
        FROM products_save

        INNER JOIN products as a
        ON products_save.id_product = a.id

        INNER JOIN products as b
        ON products_save.id_save_product = b.id;""")
        return self.cursor.fetchall()
