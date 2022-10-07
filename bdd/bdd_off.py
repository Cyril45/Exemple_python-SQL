#! /usr/bin/env python3
# coding: utf-8

"""
1.

This module contains the classes that allow communication between the API
and the database.
"""

import mysql.connector
import config.constant as constant
import unicodedata


class Bdd_off:
    """
    1.

    This class creates the database and inserts the data received from the API.
    """

    def __init__(self):
        """
        1.

        Initialize the connection to the database and
        launches the creation of the table.
        """
        self.config_DB = constant.conn.copy()
        self.config_DB_and_base = constant.conn.copy()
        self.config_DB_and_base["database"] = constant.name_base

        self.connect_db = self.db_connect(self.config_DB_and_base,
                                          self.config_DB)
        self.cursor = self.connect_db.cursor(buffered=True)
        self.create_table()

    def db_connect(self, config_DB_and_base, config_DB):
        """Allow connection to database."""
        try:
            return mysql.connector.connect(**config_DB_and_base)

        except mysql.connector.Error as e:
            if e.errno == 1049:
                print(constant.message["BDD_no_exist"])
                connect = mysql.connector.connect(**config_DB)
                self.create_database(connect)
                return mysql.connector.connect(**config_DB_and_base)

    def create_database(self, connect):
        """Allow the creation of the base."""
        cursor = connect.cursor()
        cursor.execute("CREATE DATABASE " +
                       self.config_DB_and_base["database"] +
                       " CHARACTER SET 'utf8mb4'")

    def create_table(self):
        """Allow the creation of tables."""
        self.cursor.execute("CREATE TABLE IF NOT EXISTS products(id BIGINT PRIMARY KEY,\
            categorie VARCHAR(40), nom VARCHAR(200), description TEXT,\
            indice CHAR(10), date_update DATE, url TEXT) ENGINE=InnoDB;")

        self.cursor.execute("CREATE TABLE IF NOT EXISTS ingredients(\
            id BIGINT AUTO_INCREMENT PRIMARY KEY, ingredient TEXT)\
            ENGINE=InnoDB;")

        self.cursor.execute("CREATE TABLE IF NOT EXISTS categories(\
            id BIGINT AUTO_INCREMENT PRIMARY KEY,categorie TEXT)\
            ENGINE=InnoDB;")

        self.cursor.execute("CREATE TABLE IF NOT EXISTS products_save(\
            id INT AUTO_INCREMENT, id_product BIGINT,\
            id_save_product BIGINT, PRIMARY KEY (id),\
            CONSTRAINT products_save_id_idProduct\
            FOREIGN KEY (id_product)\
            REFERENCES products(id),\
            CONSTRAINT products_save_id_idProductSave\
            FOREIGN KEY (id_save_product)\
            REFERENCES products(id))\
            ENGINE=InnoDB;")

        self.cursor.execute("CREATE TABLE IF NOT EXISTS ing_product(\
            id INT AUTO_INCREMENT, id_product BIGINT, id_ing BIGINT,\
            PRIMARY KEY (id),\
            CONSTRAINT ing_product_idProduct\
            FOREIGN KEY (id_product)\
            REFERENCES products(id),\
            CONSTRAINT ing_product_idIng\
            FOREIGN KEY (id_ing)\
            REFERENCES ingredients(id))\
            ENGINE=InnoDB;")

        self.cursor.execute("CREATE TABLE IF NOT EXISTS cat_product(\
            id INT AUTO_INCREMENT, id_product BIGINT, id_cat BIGINT,\
            PRIMARY KEY (id),\
            CONSTRAINT cat_product_idProduct\
            FOREIGN KEY (id_product)\
            REFERENCES products(id),\
            CONSTRAINT cat_product_idCat\
            FOREIGN KEY (id_cat)\
            REFERENCES categories(id))\
            ENGINE=InnoDB;")

    def insert_data(self, product_data):
        """Adding data to tables."""
        # insert catégorie in table categories
        list_cat = product_data.pop(6)
        list_cat = self.formating_data(list_cat)
        list_id_cat = []
        for word_cat in list_cat:
            self.cursor.execute("SELECT * FROM categories WHERE categorie\
                LIKE '{}'".format(word_cat))
            id_cat = self.cursor.fetchone()

            if id_cat is not None:
                list_id_cat.append(id_cat[0])

            if id_cat is None:
                self.cursor.execute("INSERT INTO categories\
                    VALUES(NULL, '{}');".format(word_cat))
                id_cat = self.cursor.lastrowid
                list_id_cat.append(id_cat)
                self.connect_db.commit()

        # insert ingredient in table ingredients
        list_ing = product_data.pop(4)
        list_ing = self.formating_data(list_ing)
        list_id_ing = []
        for word_ing in list_ing:
            self.cursor.execute("SELECT * FROM ingredients\
                WHERE ingredient LIKE '{}'".format(word_ing))
            id_ing = self.cursor.fetchone()

            if id_ing is not None:
                list_id_ing.append(id_ing[0])

            if id_ing is None:
                self.cursor.execute("INSERT INTO ingredients\
                    VALUES(NULL, '{}');".format(word_ing))
                id_ing = self.cursor.lastrowid
                list_id_ing.append(id_ing)
                self.connect_db.commit()

        # insert product in table products
        product_data = tuple(product_data)

        self.cursor.execute("INSERT IGNORE INTO products(id, categorie, nom,\
            description,indice, date_update, url)\
            VALUES(%s, %s, %s, %s,%s,%s,%s);", product_data)
        self.connect_db.commit()

        # insert DATA in association table
        for x in list_id_cat:
            data_for_query = [product_data[0], x]
            self.cursor.execute("SELECT id_product, id_cat FROM cat_product\
                WHERE id_product LIKE '{}'\
                AND id_cat LIKE '{}';".format(*data_for_query))
            result = self.cursor.fetchone()
            if result is None:
                self.cursor.execute("INSERT INTO cat_product\
                    VALUES(NULL, '{}', '{}');".format(*data_for_query))
                self.connect_db.commit()

        for y in list_id_ing:
            data_for_query = [product_data[0], y]
            self.cursor.execute("SELECT id_product, id_ing FROM ing_product\
                WHERE id_product LIKE '{}'\
                AND id_ing LIKE '{}';".format(*data_for_query))
            result = self.cursor.fetchone()
            if result is None:
                self.cursor.execute("INSERT INTO ing_product\
                    VALUES(NULL, '{}',' {}');".format(*data_for_query))
                self.connect_db.commit()

    def formating_data(self, data):
        """Allow the formatting of the data."""
        data = unicodedata.normalize('NFKD', data)\
            .encode('ASCII', 'ignore').decode()
        data = data.lower()
        data = data.replace("<span class=\"allergen\">", "")
        data = data.replace("</span>", "")
        data = data.replace("&quot", "")
        data = data.replace("&lt", "")
        data = ''.join([x if x.isalpha() else " " for x in data]).split()
        data_list = []
        for word in data:
            if len(word) >= 3:
                data_list.append(word)
        return data_list
