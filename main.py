from Class.Connexion import *
from Class.Produit import *
from Class.categorie import *
import tkinter as tk
from tkinter import ttk,messagebox

class interface:
    
    def __init__(self,fenetre):
        
        db = Connexion()
        self.con = db.get_connexion()
        self.fenetre = fenetre
        
        self.categorie = Categorie(self.con)
        self.produit = Produit(self.con)
        self.configuration()
        self.affichage()
    
    def affichage(self):
        
        self.formulaire_produit()
        self.liste_produits()
        
        
        self.btn_options()
    def btn_options(self):
        
        btn_modify = tk.Button(self.fenetre,text="Modifier",command=self.modify_data)
        btn_modify.place(x=900,y=530,width=90)
        btn_suppression = tk.Button(self.fenetre,text="Supprimer",command=self.delete_data)
        btn_suppression.place(x=900,y=570,width=90)
    
    def delete_data(self):
        if(self.liste_articles.focus() != ""):
            try:
                id_produit = int(self.liste_articles.focus()) 
            except Exception as e:
                messagebox.showerror("Error","Une erreur est survenue")
            
            if messagebox.askyesno("Suppression","Action Irreversible \n\nêtes vous sûr de vouloir suprimer ce produits?"):
                
                
                self.produit.delete(id_produit)
                self.liste_articles.delete(id_produit)
    
    def modify_data(self):
        if(self.liste_articles.focus() != ""):
            try:
                id_produit = int(self.liste_articles.focus()) 
            except Exception as e:
                messagebox.showerror("Error","Une erreur est survenue")
            self.formulaire.destroy()
            self.formulaire_produit(id_produit)
            

    def liste_produits(self):
        
        self.liste_articles = ttk.Treeview(self.fenetre,columns=(0,1,2,3,4,5), show="headings")
        self.liste_articles.place(x=90,y=350,width=800,height=270)
        
        self.liste_articles.heading(0,text="ID")
        self.liste_articles.heading(1,text="Nom")
        self.liste_articles.heading(2,text="Description")
        self.liste_articles.heading(3,text="Prix")
        self.liste_articles.heading(4,text="Quantité")
        self.liste_articles.heading(5,text="Categorie")
        
        self.liste_articles.column(0,width=2)
        self.liste_articles.column(1,width=2)
        self.liste_articles.column(2,width=2)
        self.liste_articles.column(3,width=2)
        self.liste_articles.column(4,width=2)
        self.liste_articles.column(5,width=2)
        
        produits = self.produit.select()
        
        for row in produits :
            categorie = self.categorie.select(row[5])
            produits = [row[0],row[1],row[2],row[3],row[4],categorie[1]]
            
            self.liste_articles.insert('','end',iid=produits[0],values=tuple(produits))
        
    def formulaire_produit(self,id_produit = None):
        
        self.formulaire = tk.Canvas(self.fenetre,bg="#fbc3c7")
        self.formulaire.place(x=100,y=10,width=600,height=300)
        
        tk.Label(self.formulaire,text="Nom du produit",font=("Times new roman",14),bg="#fbc3c7").place(x=60,y=10)
        self.nom_produit = tk.Entry(self.formulaire, font=("Times new roman",14))
        self.nom_produit.place(x=60,y=40,width=200)
        
        # Prix 
        tk.Label(self.formulaire,text="Prix",font=("Times new roman",14),bg="#fbc3c7").place(x=360,y=10)
        self.prix_produit = tk.Entry(self.formulaire, font=("Times new roman",14))
        self.prix_produit.place(x=360,y=40,width=200)
        
        # Quantite 
        tk.Label(self.formulaire,text="Quantité",font=("Times new roman",14),bg="#fbc3c7").place(x=360,y=70)
        self.quantite_produit = tk.Entry(self.formulaire,font=("Times new roman",14))
        self.quantite_produit.place(x=360,y=100,width=200)
        name_cat = []
        for i in self.categorie.select():
            name_cat.append(i[1])
        # Categorie
        name_cat.sort(key=lambda e: e.lower())
        tk.Label(self.formulaire,text="Categorie",font=("Times new roman",14),bg="#fbc3c7").place(x=60,y=70)
        self.categorie_produit = ttk.Combobox(self.formulaire,font=("Times new roman",14))
        self.categorie_produit["values"] = tuple(name_cat)
        self.categorie_produit.place(x=60,y=100,width=200)
        
        # description 
        tk.Label(self.formulaire,text="Description",font=("Times new roman",14),bg="#fbc3c7").place(x=250,y=150)
        self.description_produit = tk.Text(self.formulaire, font=("Times new roman",14))
        self.description_produit.place(x=150,y=180,height=60,width=300)
        
        if(id_produit != None):
            article = self.produit.select(id_produit)
            self.nom_produit.insert(0,article[1])
            self.prix_produit.insert(0,article[3])
            self.description_produit.insert("1.0",article[2])
            self.quantite_produit.insert(0,article[4])
            # cata = self.categorie.select(article[5])[1]
            self.id_produit = id_produit
            self.categorie_produit.insert(0,self.categorie.select(article[5])[1])
            
            btn_enregistrer = tk.Button(self.formulaire,text="Modifer",command=self.modification_data)
            btn_enregistrer.place(x=120,y=260,width=150)
            
            btn_enregistrer = tk.Button(self.formulaire,text="Anuler",command=self.formulaire_produit)
            btn_enregistrer.place(x=290,y=260,width=150)
        else:
            btn_enregistrer = tk.Button(self.formulaire,text="Enregistrez",command=self.enregistre_data)
            btn_enregistrer.place(x=240,y=260,width=150)
            
    def modification_data(self):
        
        nom_produit = self.nom_produit.get()
        prix = self.prix_produit.get()
        quantite = self.quantite_produit.get()
        description = self.description_produit.get("1.0","end")
        cat = self.categorie_produit.get()
        
        enregistre = True
        if nom_produit =='' or prix == '' or quantite == '' or cat =='':
            enregistre = False
            messagebox.showerror("Erreur","Veuillez Renseignez toutes les champs")
        else:
            try:
                prix = int(prix)
                quantite = int(quantite)
            except Exception as e:
                messagebox.showerror("Error","la quantité et le prix doivent être des entiers")
                enregistre = False
        
        if(enregistre):
            
            id_categorie = None
            categories = self.categorie.select()
            for categorie in categories:
                if(cat == categorie[1]):
                    id_categorie = categorie[0]
            
            if(id_categorie == None ):
                self.categorie.insert(cat)
                id_categorie = len(self.categorie.select())
            
            self.produit.update(self.id_produit,nom_produit,description,prix,quantite,id_categorie)
            messagebox.showinfo("succes","Operation reussi")
            
            self.formulaire.destroy()
            self.formulaire_produit()
            self.liste_articles.destroy()
            self.liste_produits()
       
    def enregistre_data(self):
        nom_produit = self.nom_produit.get()
        prix = self.prix_produit.get()
        quantite = self.quantite_produit.get()
        description = self.description_produit.get("1.0","end")
        cat = self.categorie_produit.get()
        
        enregistre = True
        if nom_produit =='' or prix == '' or quantite == '' or cat =='':
            enregistre = False
            messagebox.showerror("Erreur","Veuillez Renseignez toutes les champs")
        else:
            try:
                prix = int(prix)
                quantite = int(quantite)
            except Exception as e:
                messagebox.showerror("Error","la quantité et le prix doivent être des entiers")
                enregistre = False
        
        if(enregistre):
            
            id_categorie = None
            categories = self.categorie.select()
            for categorie in categories:
                if(cat == categorie[1]):
                    id_categorie = categorie[0]
            
            if(id_categorie == None ):
                self.categorie.insert(cat)
                produits = self.categorie.select()
                taille = len(produits)
                id_categorie = produits[taille-1][0]
                print(id_categorie)
            self.produit.insert(nom_produit,description,prix,quantite,id_categorie)
            messagebox.showinfo("succes","Operation reussi")
            
            self.formulaire.destroy()
            self.formulaire_produit()
            self.liste_articles.destroy()
            self.liste_produits()
            
    def configuration(self):
        self.fenetre.geometry("1000x640")

fenetre = tk.Tk()

interface(fenetre)

fenetre.mainloop()

