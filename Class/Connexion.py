import mysql.connector as MC
class Connexion:
    def __init__(self):
        
        try:
            self.con = MC.connect(host="localhost",user="root",passwd="",database="gestion_stock")
        except Exception as e:
            print("#[ERROR]",e)
    
    def get_connexion(self):
        return self.con