# gestion_de_stock

Les dependance :
1 - le module mysql.connector 
    il nous a servie pour faire la connexion entre notre code python et notre base de donnée MYSQL
2 - le module csv:
    celle ci à servie pour mettre en place le dispositif d'exportation des donnée dans un fichier csv
3 - lee module Tkinter:
    celle ci fut le module qui nous a permis de faire l'interface graphique et de rendre le travail plus conviviale.
    nous avons utiliser des module qui se situe à l'interieur de celle ci notament ttk et messagebox.

description de certain fonctionalitée:
    pour ajouter un produits il faut que les champs nom,prix,quantité et categorie soit remplis.
    pour suprimer ou modifier un produits de la liste il faut d'abord le selectionner de la liste avant de le modifier ou de le suprimer.
    lorsqu'on click sur exporter un fichier nommer "les produits.csv" contennant la liste des produits s'il n'exite, est crée s'il existe ce dernier est remplacé par une nouvelle contenant une recente liste des produits si une changement à eu lieu.

    nous avons la possibilitée de trier les données par rapport à leur categorie.