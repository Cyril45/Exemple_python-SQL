#! /usr/bin/env python3
# coding: utf-8

"""
1.

This file contains the constants necessary for the operation of the program.
"""

conn = {
    'host': 'Adresse_du_serveur_mysql',
    'user': 'Nom_utilisateur_Mysql',
    'password': 'Mot_De_Passe_Mysql',
    }

name_base = "Nom_de_la_base_de_données"

categories = [
    "boissons",
    "fruits-et-produits-derives",
    "legumes-et-derives",
    "viandes",
    "poissons",
    "sauces",
    "produits-laitiers"
    ]

message = {
    "menu_start": "\
Saisir 1 pour créer et mettre à jour la base de données \n\
Saisir 2 sélectionner les aliments que vous souhaitez remplacer.\n\
Saisir 3 retrouver mes aliments substitués.\n\
Saisir 4 pour quitter",
    "choice_mes": "Merci d'entrer votre choix: ",
    "select_cat": "Merci de sélectionner une catégorie: ",
    "standard_mes": "Vous avez sélectionné: ",
    "product_replace": "Le produit de remplacement que vous avez choisi est le \
suivant: ",
    "search_mes": "Merci d'insérer le nom du produit que vous rechercher: ",
    "select_pro": "Merci de sélectionner le produit a l'aide de son index: ",
    "standard_mes2": "Voici les produits de remplacement proposé: ",
    "select_replace": "Liste de produit de remplacement ",
    "save_mes": "Voulez-vous sauvegarder Oui ou Non: ",
    "select_index": "Merci de sélectionner le détail des produits qui vous \
intéresse à l'aide des index:  ",
    "exit_mes": "Merci d'avoir utilisé notre programme <3",
    "error_index": "Cet index n'existe pas.",
    "error_inv_number": "Le nombre n'est pas valide.",
    "error_number": "Cet entrée n'est pas valide",
    "error_choice": "Ce choix n'existe pas",
    "maj_BDD": "Mise à jour de la BDD en cours",
    "page_number": "Vous êtes sur la page: ",
    "mes_choice_page": "Choisissez\n\
[+] pour aller à la page suivante,\n\
[-] pour la page précédente,\n\
[index] pour sélectionner un produit: ",
    "BDD_no_exist": "La base de données n'existe pas celle-ci va être créée",
}

field_names = {
    "categorie": ["index", "catégories"],
    "search": ["index", "Code barre", "Nom du produit", " Desciption ",
               "NutriScore", "Derniere mise a jour", "URL"],
    "saved": ["index", "produit de base", "produit de remplacemment"]
}
