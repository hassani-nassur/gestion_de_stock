class Produit:
    
    def __init__(self,con):
        
        self.con = con
        self.cursor = con.cursor()
    
    # ajout des information à la base de donné  
    def insert(self,nom,description,prix,quantite,id_categorie):
        
        requete = "INSERT INTO `produits`(`nom`,`description`,`prix`,`quantite`,`id_categorie`) VALUES (%s,%s,%s,%s,%s)"
        
        data = (nom,description,prix,quantite,id_categorie)
        
        self.cursor.execute(requete,data)
        
        self.con.commit()
    
    # recuperation des donnée depuis la base de donné
    def select(self,id_produit = None):
        
        if id_produit != None :
            requete = "SELECT *FROM `PRODUITS` WHERE `id_produit` = %s"
            data = (id_produit,)
            
            self.cursor.execute(requete,data)
            resultat = self.cursor.fetchone()
        else:
            requete = "SELECT * FROM `PRODUITS`"
            self.cursor.execute(requete)
            
            resultat = self.cursor.fetchall()
        
        return resultat
    
    # supression d'un tuple depuis la base de donné
    def delete(self,id_produit):
        requete = "DELETE FROM `PRODUITS` WHERE `id_produit` =%s"
        data = (id_produit,)
        
        self.cursor.execute(requete,data)
        self.con.commit()
    
    # Mis à jour d'un tuple de la base de donné
    def update(self,id_produit,nom,description,prix,quantite,id_categorie):
        requete = "UPDATE `produits`SET `nom` = %s, `description` = %s, `prix` = %s, `quantite` = %s, `id_categorie` = %s WHERE `id_produit` = %s"
        
        data = (nom,description,quantite,prix,id_categorie,id_produit)
        
        self.cursor.execute(requete,data)
        
        self.con.commit()
    
    
     