class Categorie:
    
    def __init__(self,con) -> None:
        self.con = con
        self.cursor = con.cursor()
    
    def insert(self,nom):
        
        requete = "INSERT INTO `categories`(`nom`) VALUES (%s)"
        data = (nom,)
        
        self.cursor.execute(requete,data)
        self.con.commit()
    
    def delete(self,id_categorie):
        
        requete = "DELETE FROM `categories` WHERE `id_categorie` = %s"
        data = (id_categorie,)
        
        self.cursor.execute(requete,data)
        self.con.commit()
    
    # recuperation des donnée depuis la base de donné
    def select(self,id_categorie = None):
        if id_categorie != None:
            requete = "SELECT * FROM `CATEGORIES` WHERE `id_categorie` = %s"
            data = (id_categorie,)
            
            self.cursor.execute(requete,data)
            resultat = self.cursor.fetchone()
            
        else:
            requete = "SELECT * FROM `CATEGORIES`"
            self.cursor.execute(requete)
            resultat = self.cursor.fetchall()
        
        return resultat

    # mis à jours d'un tuple
    def update(self,id_categorie,nom):
        requet = "UPDATE `categories` SET `nom` = %s WHERE `id_categorie` = %s"
        
        data = (nom,id_categorie)
        
        self.cursor.execute(requet,data)
    