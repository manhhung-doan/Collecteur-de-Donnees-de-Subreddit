# Collecteur de Données de Subreddit

Ce script qui vous permet de récupérer les données d'un subreddit de votre choix et de les enregistrer dans une base de données SQLite. Vous pouvez également exporter les données dans un fichier Excel, XML ou JSON en utilisant des arguments de ligne de commande.

Le script utilise la bibliothèque PRAW pour se connecter à l'API Reddit et récupérer les données de subreddit. Il utilise également la bibliothèque pandas pour exporter les données vers un fichier Excel, et les bibliothèques json et xml.etree.ElementTree pour exporter les données vers un fichier JSON ou XML, respectivement.

Pour utiliser le script, il suffit de spécifier le nom du subreddit que vous voulez gratter et le nombre de messages à récupérer en utilisant les arguments de ligne de commande. Vous pouvez également spécifier le type de fichier dans lequel vous voulez exporter les données.

Disclaimer: Ce script est uniquement à des fins académiques, convient pour les analystes de données, les chercheurs, les journalistes et toute personne qui s'intéresse à l'analyse des données de Reddit. Il est facile à utiliser et mais il y a de nombreuses limitations, veuillez considérer attentivement avant d'utiliser.