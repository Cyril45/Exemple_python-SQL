   ## CONTEXTE

Remplacer le Nutella par une pâte aux noisettes, oui, mais laquelle ? Une idée créer un programme qui interagirait avec la base Open Food Facts pour en récupérer les aliments, les comparer et proposer à l'utilisateur un substitut plus sain à l'aliment qui lui fait envie.

   ## FONCTIONNALITÉS UTILISATEUR
   Au lancement du programme le menu de démarrage s'affiche et l'utilisateur choisit entre :
   1. Créer et mettre à jour la base de données.
   2. Sélectionner un aliment a remplacé.
   3. Retrouver ses aliments substitués.
   4. Quitter le programme 

   ### 1. Créer et mettre à jour la base de données:
   1. La création de la base de données et l'insertion de données est lancé.
   2. Quand la création est terminée le programme revient sur le menu


   ###  2. Sélectionner un aliment a remplacé:
   1. L'utilisateur sélectionne une catégorie de produits.
   2. L'utilisateur sélectionne un produit de la catégorie.
   3. Le programme renvoie le résultat d'une recherche.
   4. L'utilisateur sélectionne le produit de remplacement.
   5. L'utilisateur choisit d'enregistrer le résultat ou non.
   6. Le programme revient au menu principal.

   ### 3. Retrouver ses aliments substitués:
   1. Le programme affiche la liste des produits sélectionnés et leur produit de remplacement.
   2. L'utilisateur sélectionne à l'aide de l'index proposé les détails de produit dont il souhaite avoir l'information.
   3. Le programme affiche le detail et retourne au menu principal.
    
   ### 4. Quitter le programme:
   1. Permets à l'utilisateur de quitter le programme

  ## PRÉ-REQUIS
   - Python3.6
   - MySql
  
  ## DEPENDANCE
   - prettytable
   - mysql-connector
   - requests

  ## INSTALLATION
  Après avoir installé les prérequis et les dépendances déplacez-vous dans le dossier du programme (vous pouvez créer un environnement virtuel avec la commande **pipenv install**)

  L'installation de la base de données vous offre 2 choix:


  - **Choix 1:**
  1. Créer un utilisateur Mysql qui a les droits de création de base de données.
  2. Renseigner les informations ci-dessous dans le fichier \config\constant.py.
      - host = Adresse_du_serveur_mysql
      - user = Nom_utilisateur_Mysql
      - password = Mot_De_Passe_Mysql
      - name_base = Nom_de_la_base_de_données
  3. Lancer le programme avec **start.py**
  4. Puis **Créer et mettre à jour la base de données**


  - **Choix 2:**
  1. Créer un utilisateur Mysql.
  2. Créer une base de données (nom de votre choix).
  3. Donner les droits à l'utilisateur précédemment créer sur la base de donnée.
  4. Renseigner les informations ci-dessous dans le fichier \config\constant.py
      - host = Adresse_du_serveur_mysql
      - user = Nom_utilisateur_Mysql
      - password = Mot_De_Passe_Mysql
      - name_base = Nom_de_la_base_de_données
  5. Lancer le programme avec **start.py**
  6. Puis **Créer et mettre à jour la base de données**


  ## UTILISATION
  Vous pouvez maintenant executer **start.py**
