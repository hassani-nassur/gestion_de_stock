from Class.Connexion import *
from Class.Produit import *
from Class.categorie import *
import tkinter as tk
from tkinter import ttk,messagebox
import csv
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
                                               
class interface:
    
    def __init__(self,fenetre):
        
        db = Connexion()
        self.con = db.get_connexion()
        self.fenetre = fenetre
        
        self.categorie = Categorie(self.con)
        self.produit = Produit(self.con)
        self.configuration()
        self.affichage()
    
    # affichage des elements
    def affichage(self):
        self.formulaire_produit()
        self.Trie()
        self.btn_options()
        self.graphe_categorie()
        
    def graphe_categorie(self):
        
        # the figure that will contain the plot
        self.figure = Figure(figsize = (3, 3),dpi = 100)
        # list of squares
        x=[]
        y=[]
  
        categories = self.categorie.select()
        for row in categories:
            x.append(str(row[1])[0].upper())
            produits = self.produit.select_with_id_categorie(row[0])
            qtt = 0
            for line in produits:
                qtt +=line[4]
            y.append(qtt)  

        # adding the subplot
        self.plot1 = self.figure.add_subplot(111)
    
        # plotting the graph
        self.plot1.bar(x,y,color = "#37aceb")
        
        self.figure.suptitle("Quantité Produits par categories")
        canvas = FigureCanvasTkAgg(self.figure)  
        canvas.draw()
        
        # les parametre lier à la figure
        toolbar = NavigationToolbar2Tk(canvas,self.fenetre)
        toolbar.update()
        toolbar.place(x=690,y=305)
    
        # placement de la figure
        canvas.get_tk_widget().place(x=660,y=10,height=290,width=330)
        
    # trie des elements produits
    def Trie(self):
        name_cat = []
        for i in self.categorie.select():
            name_cat.append(i[1])
        # Categorie
        name_cat.sort(key=lambda e: e.lower())
        name_cat.insert(0,"Tout")
        
        contenu_search=tk.Frame(self.fenetre)
        contenu_search.place(x=30,y=315,width=390,height=40)
        
        tk.Label(contenu_search,text="Afficher par Categorie",font=("Times new roman",14)).place(x=3,y=5)
        self.categorie_search = ttk.Combobox(contenu_search,stat="readonly",font=("Times new roman",14))
        self.categorie_search["values"] = tuple(name_cat)
        self.categorie_search.current(0)
        self.categorie_search.place(x=180,y=5,width=200)
        
        self.categorie_search.bind("<<ComboboxSelected>>",self.get_produits)
        prods = self.produit.select()
        self.liste_produits(prods)
    
    # fonction permetant de faire le trie des produits selon leurs categorie
    def get_produits(self,event):    
        
        self.liste_articles.destroy()
        categories = self.categorie.select()
        categorie = self.categorie_search.get()
       
        if(categorie !="Tout"):
            for i in categories:
                if i[1] == categorie:
                    id_categorie = i[0]
            prods= self.produit.select_with_id_categorie(id_categorie)
        else:
            prods = self.produit.select()
        
        self.liste_produits(prods)
    
    # les button de modification et de supression d'un produits
    def btn_options(self):
        
        btn_exporter = tk.Button(self.fenetre,text="Exporter",command=self.export_data)
        btn_exporter.place(x=870,y=490,width=90)
        
        btn_modify = tk.Button(self.fenetre,text="Modifier",command=self.modify_data)
        btn_modify.place(x=870,y=530,width=90)
        
        btn_suppression = tk.Button(self.fenetre,text="Supprimer",command=self.delete_data)
        btn_suppression.place(x=870,y=570,width=90)
    
    # exportaion des donne sous le format csv
    def export_data(self):
        
        data = self.produit.select()
        # name_file = "les produits du {}.csv".format(time.strftime("%d/%m/%Y"))
        name_file ="les produits.csv"
        header = ["id","nom","description","prix","quantite","categorie"]
        produits = []
        
        for produit in data :
            cat = self.categorie.select(produit[5])
            produits.append(
                {
                    "id":produit[0],
                    "nom":produit[1],
                    "description":produit[2],
                    "prix":produit[3],
                    "quantite":produit[4],
                    "categorie":cat[1]
                }
            )
        try:    
            with open(name_file,"w",newline="") as fichier:
                file = csv.DictWriter(fichier,fieldnames=header,delimiter=",")
                file.writeheader()
                file.writerows(produits)
        except Exception as e:
            print("[ERROR]",e)  
        messagebox.showinfo("Exportation des donnée","l'exportaion des données à reussi.. \nUn fichier nommer \"{}\" a été crée".format(name_file))    
   
    # supression du produits selectionner
    def delete_data(self):
        if(self.liste_articles.focus() != ""):
            try:
                id_produit = int(self.liste_articles.focus()) 
            except Exception as e:
                messagebox.showerror("Error","Une erreur est survenue")
            
            if messagebox.askyesno("Suppression","Action Irreversible \n\nêtes vous sûr de vouloir suprimer ce produits?"):
                
                self.produit.delete(id_produit)
                self.liste_articles.delete(id_produit)
    
    # modification du prduits selectionner
    def modify_data(self):
        if(self.liste_articles.focus() != ""):
            try:
                id_produit = int(self.liste_articles.focus()) 
            except Exception as e:
                messagebox.showerror("Error","Une erreur est survenue")
            self.formulaire.destroy()
            self.formulaire_produit(id_produit)
            
    # affichage des produits dans un objet triview
    def liste_produits(self,produits):
        
        style = ttk.Style()
        
        style.configure("Treeview.Heading",font=('times new roman',14),rowheight=12)
        self.liste_articles = ttk.Treeview(self.fenetre,columns=(0,1,2,3,4,5), show="headings",selectmode='browse')
        self.liste_articles.place(x=30,y=350,width=800,height=270)
        
        vsb = ttk.Scrollbar(self.liste_articles, orient="vertical", command=self.liste_articles.yview)
        vsb.place(x=780, y=2, height=265)

        self.liste_articles.configure(yscrollcommand=vsb.set)
        
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
        
        for row in produits :
            categorie = self.categorie.select(row[5])
            produits = [row[0],row[1],row[2],row[3],row[4],categorie[1]]
            
            self.liste_articles.insert('','end',iid=produits[0],values=tuple(produits))
    
    # formulaire d'ajout et de modification d'un produits   
    def formulaire_produit(self,id_produit = None):
        
        self.formulaire = tk.Canvas(self.fenetre,bg="#f4cf92")
        self.formulaire.place(x=30,y=10,width=600,height=290)
        
        tk.Label(self.formulaire,text="Nom du produit",font=("Times new roman",14),bg="#f4cf92").place(x=60,y=10)
        self.nom_produit = tk.Entry(self.formulaire, font=("Times new roman",14))
        self.nom_produit.place(x=60,y=40,width=200)
        
        # Prix 
        tk.Label(self.formulaire,text="Prix",font=("Times new roman",14),bg="#f4cf92").place(x=360,y=10)
        self.prix_produit = tk.Entry(self.formulaire, font=("Times new roman",14))
        self.prix_produit.place(x=360,y=40,width=200)
        
        # Quantite 
        tk.Label(self.formulaire,text="Quantité",font=("Times new roman",14),bg="#f4cf92").place(x=360,y=70)
        self.quantite_produit = tk.Entry(self.formulaire,font=("Times new roman",14))
        self.quantite_produit.place(x=360,y=100,width=200)
        name_cat = []
       
        for i in self.categorie.select():
            name_cat.append(i[1])
       
        # Categorie
        name_cat.sort(key=lambda e: e.lower())
        tk.Label(self.formulaire,text="Categorie",font=("Times new roman",14),bg="#f4cf92").place(x=60,y=70)
        self.categorie_produit = ttk.Combobox(self.formulaire,font=("Times new roman",14))
        self.categorie_produit["values"] = tuple(name_cat)
        self.categorie_produit.place(x=60,y=100,width=200)
        
        # description 
        tk.Label(self.formulaire,text="Description",font=("Times new roman",14),bg="#f4cf92").place(x=250,y=150)
        self.description_produit = tk.Text(self.formulaire, font=("Times new roman",14))
        self.description_produit.place(x=150,y=180,height=60,width=300)
        
        # cas d'une modification 
        if(id_produit != None):
            article = self.produit.select(id_produit)
            self.nom_produit.insert(0,article[1])
            self.prix_produit.insert(0,article[3])
            self.description_produit.insert("1.0",article[2])
            self.quantite_produit.insert(0,article[4])
            
            self.id_produit = id_produit
            self.categorie_produit.insert(0,self.categorie.select(article[5])[1])
            
            btn_enregistrer = tk.Button(self.formulaire,text="Modifer",command=self.modification_data,bg="#f2be74")
            btn_enregistrer.place(x=120,y=255,width=150)
            
            btn_enregistrer = tk.Button(self.formulaire,text="Anuler",command=self.formulaire_produit,bg="#f2be74")
            btn_enregistrer.place(x=290,y=255,width=150)
        else:
            btn_enregistrer = tk.Button(self.formulaire,text="Enregistrer",command=self.enregistre_data,bg="#f2be74")
            btn_enregistrer.place(x=240,y=255,width=150)
   
    # enregistrement de la modification effectuer sur un produit    
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
            messagebox.showinfo("succes","Operation reussi! les modifcations sont bien enregistrez.")
            
            self.formulaire.destroy()
            self.formulaire_produit()
            self.liste_articles.destroy()
            self.Trie()
            self.plot1.remove()
            self.graphe_categorie()
    
    # enregistrement de l'ajouts d'un produits   
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
            messagebox.showinfo("succes","Operation reussi !,le produit a bien été ajouter.")
            
            self.formulaire.destroy()
            self.formulaire_produit()
            self.liste_articles.destroy()
            self.Trie()
            self.plot1.remove()
            self.graphe_categorie()
    
    # configuration de la fentre d'affichge
    def configuration(self):
        self.fenetre.geometry("1000x640")
        self.fenetre.config(bg="#f2be74")
        self.fenetre.title("Gestion de stock")
        self.fenetre.resizable(width=False,height=False)

fenetre = tk.Tk()

interface(fenetre)

fenetre.mainloop()

