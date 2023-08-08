from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo, showwarning, showerror, askyesno
import sqlite3 as sq

from src.categorie import Categories
import sys
import os

from src.product import delete_product, get_all, register_product, search_product_by_categorie, search_product_by_name, update_product
from xlsw import inventory_excel_file

class MainWindow:
    def __init__(self):
        self.root = Tk()        
        self.root.wm_state(newstate="zoomed")
        self.root.title("StockLab")
        self.root.iconbitmap("icon/icone.ico")
        self.menu = Menu(self.root)
        self.root.config(background="#23222e", menu=self.menu)

        # sous-menu fichier
        file = Menu(self.menu, tearoff=0)
        file.add_command(label="Nouvelle fenêtre", command=self.new, accelerator="Ctrl+N")
        file.add_command(label="Bureau de change", command=self.conversion, accelerator="Ctrl+B")
        file.add_separator()
        file.add_command(label="Quitter", command=quit)
        self.menu.add_cascade(label="Fichier", menu=file)
        self.root.bind_all("<Control-KeyPress-n>", self.new_bind)
        self.root.bind_all("<Control-KeyPress-N>", self.new_bind)
        self.root.bind_all("<Control-KeyPress-b>", self.conversion_bind)
        self.root.bind_all("<Control-KeyPress-B>", self.conversion_bind)

        # sous-menu thème
        theme = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Option", menu=theme)

        # sous-menu color
        color_menu = Menu(self.menu, tearoff=0)
        self.color = IntVar()
        self.color.set(1)
        color_menu.add_radiobutton(label="<Thème par defaut>", variable=self.color, value=1, command=self.change_theme)
        color_menu.add_separator()
        color_menu.add_radiobutton(label="gris", variable=self.color, value=2, command=self.change_theme)
        color_menu.add_radiobutton(label="violet", variable=self.color, value=3, command=self.change_theme)        
        
        theme.add_cascade(menu=color_menu, label="Thème")
        
        # sous-menu aide
        aide = Menu(self.menu, tearoff=0)
        aide.add_command(label="À propos de StockLab", command=self.about)
        self.menu.add_cascade(label="Aide", menu=aide)

        self.by = StringVar()
        self.nom_cat = StringVar()
        self.id_cat = StringVar()
        self.recherche = StringVar()
        self.id_prod = StringVar()
        self.name_prod = StringVar()
        self.state_prod = StringVar()
        self.quantity = StringVar()
        self.price = StringVar()
        self.categorie = StringVar()
        self.create_frame_for_product_list()
        self.create_frame_for_categorie_list()
        self.create_frame_for_adding_categorie()
    
    def show(self):
        for prod in self.tree.get_children():
            self.tree.delete(prod)
        for produit in get_all():
            self.tree.tag_configure('orow', font=('verdana', 10), background="#fff")
            self.tree.insert('', 'end', values=produit, tag='orow')            
    
    
    def create_frame_for_product_list(self):        
        self.colonnes = ("id", "nom", "quantite", "etat_stock", "prix", "id_categorie")     # les colonnes à afficher dans le tableau
        self.frame = Frame(self.root, bd=0, bg="#8080FF")
        self.frame.place(x=0, y=2, width=1278, height=400)
        self.lab_main = Label(self.frame, text="TABLEAU DES PRODUITS", font=("consolas", 16), bg="#8080FF", fg="white")
        self.lab_main.place(x=5, y=5)
                
        # champ de recherche        
        search_field = Entry(self.frame, textvariable=self.recherche, font=("verdana", 10))
        search_field.place(x=880, y=5, width=170, height=28)
        
        # label rechercher par
        self.lbl_search = Label(self.frame, text="RECHERCHER PAR:", background="#8080FF", fg="white", font=("ms reference sans serif", 10, "bold"))
        self.lbl_search.place(x=530, y=10)

        # bouton recherche
        btn_search = Button(self.frame, text='Rechercher', width=10, command=self.search)
        btn_search.place(x=1060, y=5, width=90, height=28)
        search_by= ttk.Combobox(self.frame, textvariable=self.by, font=("verdana", 10), state="readonly", values=("", "catégorie", "nom du produit"))
        search_by.place(x=670, y=5, width=200, height=28)
        search_by.current(0)

        # bouton pour afficher tous les informations
        btn_info = Button(self.frame, text=' Tout afficher', width=10, command=self.show)
        btn_info.place(x=1160, y=5, width=90, height=28)
        
        # Bouton d'ajout, de modification et de suppression d'un produit
        btn_del = Button(self.frame, text="Supprimer un produit",bg="#333", fg="#fff", command=self.delete_product_view)
        btn_del.place(x=775 , y=358, width=150, height=33)
        btn_update = Button(self.frame, text="Modifier un produit",  command=self.update_product_view)
        btn_update.place(x=935 , y=358, width=150, height=33)
        btn_add = Button(self.frame, text="Ajouter un produit", bg='yellow' ,command=self.register_product_view)
        btn_add.place(x=1095 , y=358, width=150, height=33)
        
        # bouton pour générer un fichier excel de l'inventaire des produits
        btn_excel = Button(self.frame, text='Télécharger un fichier excel des produits', bg='#333', fg='#fff',command=inventory_excel_file)
        btn_excel.place(x=15, y=358, height=33)        

        # scrollbar vertical et tableau
        self.tree = ttk.Treeview(self.frame, columns=self.colonnes, show='headings', selectmode='browse')
        self.scrollY = ttk.Scrollbar(self.frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollY.set)
        
        # configuration du tableau pour afficher la liste de tous les produits       
        self.scrollY.pack(side=RIGHT, fill=Y)
        self.tree.column("#0", width=0, stretch=NO)
        self.tree.column('id', width=20, anchor=S)
        self.tree.column("nom", width=100, anchor=S)
        self.tree.column("quantite", width=50, anchor=S)
        self.tree.column("etat_stock", width=100, anchor=S)
        self.tree.column("prix", width=50, anchor=S)
        self.tree.column("id_categorie", width=50, anchor=S)

        self.tree.heading('id', text='Identifiant', anchor=S)
        self.tree.heading('nom', text='Nom du produit', anchor=S)
        self.tree.heading('quantite', text='Quantité en stock', anchor=S)
        self.tree.heading('etat_stock', text='Etat du stock', anchor=S)
        self.tree.heading('prix', text='Prix', anchor=S)
        self.tree.heading('id_categorie', text='Catégorie', anchor=S)
        
        self.tree.place(x=8, y=40, height=310, width=1232)
        for e in self.tree.get_children():
            self.tree.delete(e)
        for product in get_all():
            self.tree.insert('', 'end', values=product, tag="orow")
    
        self.tree.tag_configure('orow', font=('verdana', 10), background="#fff")
        self.tree.bind("<ButtonRelease-1>", self.get_products_info)
    
    def delete_product_view(self):
        self.win_sup = Toplevel(self.root)
        self.win_sup.title("Suppression des produits")
        self.win_sup.geometry("500x430+380+160")
        self.win_sup.iconbitmap("icon/icone.ico")
        self.win_sup.resizable(False, False)
        self.win_sup.config(background="#0a0b38")
        
        lable_principal = Label(self.win_sup, text="Suppression des produits", fg="#fff", bg="#b60d2a", font=("consolas", 18))
        lable_principal.place(x=0, y=0, width=500, height=90)

        # LABEL POUR L'IDENTIFIANT DU PRODUIT
        label1 = Label(self.win_sup, text="N° Identifiant", font=("ms reference sans serif", 12), bg='#0a0b38', fg="#ffffff")
        label1.place(x=40, y=200)
        sup_entry = Entry(self.win_sup, textvariable=self.id_prod, bd=1, font=("verdana", 10))
        sup_entry.place(x=180, y=200, width=240, height=28)
        
        
        # Bouton supprimer
        btn_sup = Button(self.win_sup, text="Supprimer", bg="#b60d2a", fg="#fff", bd=0, command=self.delete, font=("ms reference sans serif", 11))
        btn_sup.place(x=140 , y=340, width=250, height=33)
    
    
    def delete(self):
        if str(self.id_prod.get()) == "" or str(self.id_prod.get()) == " ":
            showwarning('Attention', "Le champ n° identifiant est requis pour supprimer", parent=self.win_sup)
        else:
            res = askyesno("Notice", "Vous êtes entrain de supprimer ce produit. Voulez-vous continuer ?", parent=self.win_sup)
            if res:                
                delete_product(self.id_prod.get())
                self.rafraichir()              
                # vider les champs de saisi
                self.reinitialize()
                showinfo('succès', "Produit supprimé", parent=self.win_sup)
            else:
                pass
    
    def register_product_view(self):
        self.win_create = Toplevel(self.root)        
        self.win_create.title("Enrégistrement des produits")
        self.win_create.geometry("560x480+380+160")
        self.win_create.iconbitmap("icon/icone.ico")
        self.win_create.resizable(False, False)
        self.win_create.config(background="#0a0b38")

        #121246        
        lable_principal = Label(self.win_create, text="Enrégistrement des produits", fg="#fff", bg="#49ca74", font=("century gothic", 20))
        lable_principal.place(x=0, y=0, width=560, height=90)

        # LABEL POUR LES DONNEES DU PRODUIT
        label1 = Label(self.win_create, text="Nom:", font=("ms reference sans serif", 12), bg='#0a0b38', fg='#fff')
        label1.place(x=40, y=120)
        name_entry = Entry(self.win_create, textvariable=self.name_prod, bd=1, font=("verdana", 10))
        name_entry.place(x=180, y=120, width=240, height=28)
        
        label2 = Label(self.win_create, text="Quantité:", font=("ms reference sans serif", 12), bg='#0a0b38', fg='#fff')
        label2.place(x=40, y=170)
        quantity_entry = Entry(self.win_create, textvariable=self.quantity, bd=1, font=("verdana", 10))
        quantity_entry.place(x=180, y=170, width=240, height=28)
        
        label3 = Label(self.win_create, text="Prix:", font=("ms reference sans serif", 12), bg='#0a0b38', fg='#fff')
        label3.place(x=40, y=214)
        price_entry = Entry(self.win_create, textvariable=self.price, bd=0, font=("verdana", 10))
        price_entry.place(x=180, y=214, width=240, height=28)
        
        label4 = Label(self.win_create, text="Etat du produit:", font=("ms reference sans serif", 12), bg='#0a0b38', fg='#fff')
        label4.place(x=40, y=263)
        state_entry = ttk.Combobox(self.win_create, textvariable=self.state_prod, font=("verdana", 10))
        state_entry["values"] = ("en stock", "vide")
        state_entry["state"] = "readonly"
        state_entry.current(0)
        state_entry.place(x=180, y=263, width=240, height=28)
        
        label5 = Label(self.win_create, text="Catégorie:", font=("ms reference sans serif", 12), bg='#0a0b38', fg='#fff')
        label5.place(x=40, y=310)
        categorie_entry = ttk.Combobox(self.win_create, textvariable=self.categorie, font=("verdana", 10))
        categorie_entry["values"] = Categories.getCategories()
        categorie_entry["state"] = "readonly"        
        categorie_entry.place(x=180, y=310, width=240, height=28)
        
        
        # Bouton enrégistrer
        btn_create = Button(self.win_create, text="Enrégister", bg="#49ca74", fg="#fff", bd=0, command=self.register, font=("ms reference sans serif", 11))
        btn_create.place(x=160 , y=406, width=250, height=33)

    
    def register(self):
        if str(self.name_prod.get()) == "" or str(self.name_prod.get()) == " ":
            showwarning("Rappel", "Entrez un nom pour ce produit", parent=self.win_create)
        elif str(self.price.get()) == "" or str(self.price.get()) == " ":
            showwarning("Rappel", "Vous avez oublié de mettre un prix pour ce produit. Soit mettez un prix de 0 Fc pour indiquer l'absence du prix", parent=self.win_create)
        elif str(self.quantity.get()) == "" or str(self.quantity.get()) == " ":
            showinfo("Rappel", "Précisez une quantité pour ce produit. Vous pouvez mettre 0 pour une quantité vide", parent=self.win_create)
        elif str(self.quantity.get()) == '0' and str(self.state_prod.get()) == 'en stock':
            showerror("Erreur", "Le produit ne peut pas être en stock pendant que sa quantité est 0. Modifiez l'état du produit", parent=self.win_create)
        elif self.categorie.get() == "":
            showinfo("Rappel", "Attribuez une catégorie à ce produit en selectionnant une dans le champ catégorie", parent=self.win_create)
        else:
            categorie = Categories.getIdByName(self.categorie.get())     # recuperation de la categorie selectionnée
            values = self.name_prod.get().strip(), self.quantity.get().strip(), \
                    self.state_prod.get().strip(), categorie[0][1], self.price.get().strip()
            register_product(*values)
            self.rafraichir()
            # vider les champs de saisi
            self.reinitialize()
            showinfo("Succès", 'Enregistrement éffectué', parent=self.win_create)
    
    def update_product_view(self):
        self.win_update = Toplevel(self.root)
        self.win_update.title("Mise à jour des produits")
        self.win_update.geometry("560x480+380+160")
        self.win_update.iconbitmap("icon/icone.ico")
        self.win_update.resizable(False, False)
        self.win_update.config(background="#0a0b38")
        
        lable_principal = Label(self.win_update, text="Mise à jour des produits", fg="#fff", bg="#1c9be4", font=("consolas", 18))
        lable_principal.place(x=0, y=0, width=560, height=90)

        # LABEL POUR LES DONNEES DU PRODUIT
        label1 = Label(self.win_update, text="Nom:", font=("ms reference sans serif", 12), bg='#0a0b38', fg="#fff")
        label1.place(x=40, y=120)
        name_entry = Entry(self.win_update, textvariable=self.name_prod, bd=1, font=("verdana", 10))
        name_entry.place(x=180, y=120, width=240, height=28)
        
        label2 = Label(self.win_update, text="Quantité:", font=("ms reference sans serif", 12), bg='#0a0b38', fg="#fff")
        label2.place(x=40, y=170)
        quantity_entry = Entry(self.win_update, textvariable=self.quantity, bd=1, font=("verdana", 10))
        quantity_entry.place(x=180, y=170, width=240, height=28)
        
        label3 = Label(self.win_update, text="Prix:", font=("ms reference sans serif", 12), bg='#0a0b38', fg="#fff")
        label3.place(x=40, y=214)
        price_entry = Entry(self.win_update, textvariable=self.price, bd=0, font=("verdana", 10))
        price_entry.place(x=180, y=214, width=240, height=28)
        
        label4 = Label(self.win_update, text="Etat du produit:", font=("ms reference sans serif", 12), bg='#0a0b38', fg="#fff")
        label4.place(x=40, y=263)
        state_entry = ttk.Combobox(self.win_update, textvariable=self.state_prod, font=("verdana", 10))
        state_entry["values"] = ("en stock", "vide")
        state_entry["state"] = "readonly"
        state_entry.current(0)
        state_entry.place(x=180, y=263, width=240, height=28)
        
        label5 = Label(self.win_update, text="Catégorie:", font=("ms reference sans serif", 12), bg='#0a0b38', fg="#fff")
        label5.place(x=40, y=310)
        categorie_entry = ttk.Combobox(self.win_update, textvariable=self.categorie, font=("verdana", 10))
        categorie_entry["values"] = Categories.getCategories()
        categorie_entry["state"] = "readonly"
        categorie_entry.place(x=180, y=310, width=240, height=28)
        
        label6 = Label(self.win_update, text="N° identifiant:", font=("ms reference sans serif", 12), bg='#0a0b38', fg="#fff")
        label6.place(x=40, y=350)
        id_entry = Entry(self.win_update, textvariable=self.id_prod, font=("verdana", 10))
        id_entry.place(x=180, y=350, width=240, height=28)
        
        
        # Bouton modification
        btn_create = Button(self.win_update, text="Mettre à jour", bg="#1c9be4", fg="#fff", bd=0, command=self.update, font=("ms reference sans serif", 11))
        btn_create.place(x=160 , y=430, width=250, height=33)

    
    def update(self):        
        if str(self.id_prod.get()) == "":
            showwarning("Attention", "Précisez l'identifiant du produit que vous voulez mettre à jour", parent=self.win_update)
        elif str(self.price.get()) == "" or self.price.get() == '0':
            showinfo("Rappel", "Vous avez oublié de mettre le prix à ce produit ou mettez un prix différent de 0 Fc", parent=self.win_update)
        elif str(self.quantity.get()) == "" or str(self.quantity.get()) == " ":
            showinfo("Rappel", "Précisez une quantité pour ce produit. Vous pouvez mettre 0 pour une quantité vide", parent=self.win_update)
        elif str(self.quantity.get()) == '0' and str(self.state_prod.get()) == 'en stock':
            showerror("Erreur", "Le produit ne peut pas être en stock pendant que sa quantité est 0. Modifiez l'état du produit", parent=self.win_update)
        elif str(self.name_prod.get()) == "":
            showerror("Erreur", "Vous ne pouvez pas enlever le nom à ce produit", parent=self.win_update)
        elif self.categorie.get() == "":
            showinfo("Rappel", "Attribuez une catégorie à ce produit en selectionnant une dans le champ catégorie", parent=self.win_update)
        else:
            if str(self.state_prod.get()) != "":
                icategorie = Categories.getIdByName(self.categorie.get())         # recuperation du nom de la categorie selectionnee
                n_cat = Categories.getNameById(int(icategorie[0][0]))
                values = self.name_prod.get().strip(), self.quantity.get().strip(), \
                    self.state_prod.get(), str(n_cat), self.price.get().strip(), self.id_prod.get().strip()
                update_product(*values)
                self.rafraichir()
                # vider les champs de saisi
                self.reinitialize()
                showinfo("Succès", 'Mise à jour éffectuée', parent=self.win_update)                                
            else:
                showwarning("Attention", "Mettez à jour au moins un champ des données", parent=self.win_update)
    
    
    def reinitialize(self):
        self.name_prod.set('')
        self.price.set('')
        self.quantity.set('')
        self.state_prod.set('en stock')
        self.id_prod.set('')
        
                
    def create_frame_for_categorie_list(self):        
        self.frame2 = Frame(self.root, bd=2, background="#8080FF")
        self.frame2.place(x=0, y=404, width=705, height=320)
        self.lbl_cat = Label(self.frame2, text="TABLEAU DES CATEGORIES DES PRODUITS", font=("consolas", 16), bg="#8080FF", fg="white")
        self.lbl_cat.place(x=5, y=5)
        
        # cration du tableau
        self.tree2 = ttk.Treeview(self.frame2, columns=("id", "nom"), show="headings", selectmode='browse')
        scroll_y = ttk.Scrollbar(self.frame2, orient='vertical', command=self.tree2.yview)
        self.tree2.configure(yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT, fill=Y)
        self.tree2.column("#0", width=0, stretch=NO)
        self.tree2.column("id", width=20, anchor=S)
        self.tree2.column("nom", width=100, anchor=S)
        self.tree2.heading("id", text="Identifiant", anchor=S)
        self.tree2.heading("nom", text="Nom", anchor=S)
        self.tree2.place(x=8, y=45, width=650)
        self.tree2.tag_configure('orow', font=('verdana', 11), background="#fff")
        self.tree2.bind("<ButtonRelease-1>", self.get_categories_info)

        # BOUTON DELETE ET UPDATE
        self.btn_sup = Button(self.frame2, text="Supprimer la catégorie", bg='#333', fg='#fff',command=self.delete_cat)    
        self.btn_sup.place(x=160, y=275, width=150, height=30)
        self.btn_modif = Button(self.frame2, text="Modifier la catégorie", command=self.update_cat)
        self.btn_modif.place(x=330, y=275, width=150, height=30)        
        
        # affichage des catégories dans le tableau
        for c in self.tree2.get_children():
            self.tree2.delete(c)
            
        for categorie in Categories.getAll():
            self.tree2.insert('', END, values=categorie, tag="orow")            
            
    
    def get_categories_info(self, event):
            """cette fonction elle récupères tous les données d'une catégories dans le tableau 
            et le réaffecte
            dans leurs champs de saisi
            """
            ligne_focus = self.tree2.focus()
            contenus = self.tree2.item(ligne_focus)
            row = contenus["values"]
            self.id_cat.set(row[0])
            self.nom_cat.set(row[1])
    
    
    def get_products_info(self, event):
            """cette fonction elle récupères tous les données d'un produit dans le tableau 
            et le réaffecte
            dans leurs champs de saisi
            """
            focus_line = self.tree.focus()
            contents = self.tree.item(focus_line)
            rows = contents["values"]
            prix = str(rows[4]).split(" ")            
            self.id_prod.set(rows[0])
            self.name_prod.set(rows[1])
            self.quantity.set(rows[2])
            self.state_prod.set(rows[3])
            self.categorie.set(rows[5])
            self.price.set(prix[0])

        
    def create_frame_for_adding_categorie(self):
        self.frame3 = Frame(self.root, bd=2, background="#8080FF")
        self.frame3.place(x=708, y=404, width=571, height=320)
        Label(self.frame3, text="AJOUT DES CATEGORIES", font=("consolas", 16), bg="#000", fg="white").place(x=-1.5, y=-1.5, width=571, height=70)
        
        # CHAMP NOM DE LA CATEGORIE
        self.lb_name_cat = Label(self.frame3, text="Nom de la catégorie", font=("ms reference sans serif", 12), bg="#8080FF")
        self.lb_name_cat.place(x=200, y=100)
        self.lb_id_cat = Label(self.frame3, text="N° identifiant", font=("ms reference sans serif", 12), bg="#8080FF")
        self.lb_id_cat.place(x=229, y=184)
        nom = Entry(self.frame3, font=("arial", 11), textvariable=self.nom_cat)
        nom.place(x=150, y=140, width=290, height=32)
        idt = Entry(self.frame3, font=("arial", 11), textvariable=self.id_cat)
        idt.place(x=150, y=220, width=290, height=32)
        btn_add_cat = Button(self.frame3, text="Ajouter la catégorie", font=("ms reference sans serif", 11), command=self.create_cat)
        btn_add_cat.place(x=170, y=270, width=250, height=32)
    
                
    def delete_cat(self):
        if self.id_cat.get() != "":
            response = askyesno("Notice", "Cette opération est irréversible. Tous les produits appartennant à cette catégorie seront aussi supprimé !\nVoulez-vous quand-même supprimer cette catégorie ? ")
            if response:
                name_cat_from_prod = Categories.getNameById(self.id_cat.get())
                Categories.delete_cat_model(self.id_cat.get(), name_cat_from_prod)
                self.rafraichir()
                self.nom_cat.set("")
                self.id_cat.set("")
                showinfo("Succès", "Catégorie supprimée avec succès")          
            else:
                pass
        else:
            showwarning("Attention", "Vous devez préciser l'identifiant de la catégorie que vous voulez supprimer")


    def update_cat(self):
        if self.id_cat.get() == "" or self.id_cat.get() == " ":
            showwarning("Attention", "Précisez l'identifiant de la catégorie que vous voulez modifier")
        else:                                    
            if self.nom_cat.get() != "" and self.nom_cat.get() != " ":
                Categories.update_cat_model(self.nom_cat.get().strip(), self.id_cat.get())
                self.rafraichir()
                self.nom_cat.set("")
                self.id_cat.set("")
                showinfo("succès", "Catégorie modifiée succèes")
            else:
                showwarning("Attention", "Entrez les nouvelles coordonnées de la catégorie sélectionnée")
    
    
    def rafraichir(self):
        """
        Cette fonction rafraichi tous les tableaux après chaque ajout, modification ou suppression
        de la part de l'utilisateur
        """
        self.root.after(1, self.create_frame_for_categorie_list())
        self.root.after(1, self.create_frame_for_product_list()) 
    
    
    def create_cat(self):
        if self.nom_cat.get() == "" or self.nom_cat.get() == " ":
            showwarning("Attention", "Vous devez entrer un nom pour créer une catégorie")
        elif self.id_cat.get() != "":
            showerror("erreur", "L'identifiant est géneré automatiquement !")
        else:
            Categories.create_cat_model(self.nom_cat.get().strip())
            self.rafraichir()
            self.nom_cat.set("")
            showinfo("succès", "Catégorie créée avec succès")
    
    
    def search(self):
        if self.by.get() == "nom du produit":
            if self.recherche.get() == "" or self.recherche.get() == " ":
                showwarning("Notice", "Entrez le nom du produit que vous voulez rechercher", parent=self.root)
            else:
                if len(search_product_by_name(self.recherche.get().title())) != 0:
                    for el in self.tree.get_children():
                        self.tree.delete(el)

                    for row in search_product_by_name(self.recherche.get().title()):
                        self.tree.insert('', END, values=row, tag='orow')
                        self.tree.tag_configure('orow', font=('verdana', 10), background='#fff')
                        self.recherche.set("")
                else:
                    showinfo("Not found", "Produit non trouvé", parent=self.root)
        elif self.by.get() == "catégorie":
            if self.recherche.get() == "" or self.recherche.get() == " ":
                showwarning("Notice", "Entrez le nom de la catégorie des produits que vous voulez rechercher", parent=self.root)
            else:
                categorie_name = Categories.get_name_of_categorie(self.recherche.get().title())
                if categorie_name != []:                   
                    if len(search_product_by_categorie(categorie_name[0][0])) != 0:
                        for el in self.tree.get_children():
                            self.tree.delete(el)                        
                        for row in search_product_by_categorie(categorie_name[0][0]):
                            self.tree.insert('', END, values=row, tag='orow')
                            self.tree.tag_configure('orow', font=('verdana', 10), background='#fff')
                            self.recherche.set("")
                    else:
                        showinfo("Not found", "Aucun produit n'est associé à cette catégorie", parent=self.root)
                else: 
                    showinfo("Not found", "Catégorie non trouvée", parent=self.root)            
        else:
            showerror("Erreur", "Précisez votre recherche en selectionnant le type de recherche dans le champ <RECHERCHER PAR> ", parent=self.root)
    

    def conversion(self):
        self.c = Toplevel()
        self.c.title("Convertissez votre monnaie")
        self.c.geometry("340x410+380+160")
        self.c.iconbitmap("icon/icone.ico")        
        self.cframe = Frame(self.c, bg='#0a0b38')
        self.cframe.place(x=0, y=0, width=340, height=410)
        self.e2 = StringVar()

        Label(self.cframe, text="Devise", font=("verdana", 12), bg='#0a0b38', fg='#fff').place(x=0, y=10)
        self.devise = ttk.Combobox(self.cframe, values=("franc", "dollar"), state='readonly')
        self.devise.place(x=60, y=12, width=60)
        self.devise.current(1)

        Label(self.c, text='Montant', font=("ms reference sans serif", 11), bg='#0a0b38', fg='#fff').place(x=135, y=100)
        self.entree1 = Entry(self.cframe, font=("verdana", 11))
        self.entree1.place(x=50, y=130, width=240, height=25)

        Label(self.c, text='Resultat', font=("ms reference sans serif", 11), bg='#0a0b38', fg='#fff').place(x=135, y=210)
        self.entree2 = Entry(self.cframe, textvariable=self.e2, font=("verdana", 11))
        self.entree2.place(x=50, y=240, width=240, height=25)
        Label(self.cframe, text="Taux= 2465", font=("sans serif", 8), bg='#0a0b38', fg='#fff').place(x=50, y=280)

        def convert_b(event):
            e1 = self.entree1.get()
            taux = 2465
            r = None

            match(self.devise.get()):
                case('franc'):
                    if e1 != '':
                        r = int(float(e1)) / taux
                        self.e2.set(f'{r} $')
                    else:
                        showinfo('', 'Mettez un montant dans le premier champ de saisi', parent=self.c)
                case('dollar'):
                    if e1 != '':
                        r = int(float(e1)) * taux
                        self.e2.set(f'{r} fc')
                    else:
                        showinfo('', 'Mettez un montant dans le premier champ de saisi', parent=self.c)                    
                case _:
                    showinfo('', 'Choississez une devise', parent=self.c)

        def convert():
            e1 = self.entree1.get()
            r = None
            taux = 2465

            match(self.devise.get()):
                case('franc'):
                    if r is None:
                        if e1 != "":
                            r = int(float(e1)) / taux
                            self.e2.set(f'{r} $')
                        else:
                            showinfo('', 'Mettez un montant dans le premier champ de saisi', parent=self.c)
                case('dollar'):
                    if r is None:
                        if e1 != '':
                            r = int(float(e1)) * taux
                            self.e2.set(f'{r} fc')
                        else:
                            showinfo('', 'Mettez un montant dans le premier champ de saisi', parent=self.c)
                    # Label(self.c, text='Montant', font=("ms reference sans serif", 11), bg='#000', fg='#fff').place(x=100, y=100)
                    # Label(self.c, text='Resultat', font=("ms reference sans serif", 11), bg='#333', fg='#fff').place(x=100, y=210)
                case _:
                    showinfo('', 'Choississez une devise', parent=self.c)

        self.c.bind("<Return>", convert_b)
        Button(self.c, text="Convertir", font=("arial", 14), bg='#3af076', command=convert).place(x=50, y=340, width=240)
    
    
    def conversion_bind(self, event):
        self.c = Toplevel()
        self.c.title("Convertissez votre monnaie")
        self.c.geometry("340x410+380+160")
        self.c.iconbitmap("icon/icone.ico")        
        self.cframe = Frame(self.c, bg='#0a0b38')
        self.cframe.place(x=0, y=0, width=340, height=410)
        self.e2 = StringVar()

        Label(self.cframe, text="Devise", font=("verdana", 12), bg='#0a0b38', fg='#fff').place(x=0, y=10)
        self.devise = ttk.Combobox(self.cframe, values=("franc", "dollar"), state='readonly')
        self.devise.place(x=60, y=12, width=60)
        self.devise.current(1)

        Label(self.c, text='Montant', font=("ms reference sans serif", 11), bg='#0a0b38', fg='#fff').place(x=135, y=100)
        self.entree1 = Entry(self.cframe, font=("verdana", 11))
        self.entree1.place(x=50, y=130, width=240, height=25)

        Label(self.c, text='Resultat', font=("ms reference sans serif", 11), bg='#0a0b38', fg='#fff').place(x=135, y=210)
        self.entree2 = Entry(self.cframe, textvariable=self.e2, font=("verdana", 11))
        self.entree2.place(x=50, y=240, width=240, height=25)
        Label(self.cframe, text="Taux= 2465", font=("sans serif", 8), bg='#0a0b38', fg='#fff').place(x=50, y=280)

        def convert_b(event):
            e1 = self.entree1.get()
            taux = 2465
            r = None

            match(self.devise.get()):
                case('franc'):
                    if e1 != '':
                        r = int(float(e1)) / taux
                        self.e2.set(f'{r} $')
                    else:
                        showinfo('', 'Mettez un montant dans le premier champ de saisi', parent=self.c)
                case('dollar'):
                    if e1 != '':
                        r = int(float(e1)) * taux
                        self.e2.set(f'{r} fc')
                    else:
                        showinfo('', 'Mettez un montant dans le premier champ de saisi', parent=self.c)                    
                case _:
                    showinfo('', 'Choississez une devise', parent=self.c)

        def convert():
            e1 = self.entree1.get()
            r = None
            taux = 2465

            match(self.devise.get()):
                case('franc'):
                    if r is None:
                        if e1 != "":
                            r = int(float(e1)) / taux
                            self.e2.set(f'{r} $')
                        else:
                            showinfo('', 'Mettez un montant dans le premier champ de saisi', parent=self.c)
                case('dollar'):
                    if r is None:
                        if e1 != '':
                            r = int(float(e1)) * taux
                            self.e2.set(f'{r} fc')
                        else:
                            showinfo('', 'Mettez un montant dans le premier champ de saisi', parent=self.c)
                    # Label(self.c, text='Montant', font=("ms reference sans serif", 11), bg='#000', fg='#fff').place(x=100, y=100)
                    # Label(self.c, text='Resultat', font=("ms reference sans serif", 11), bg='#333', fg='#fff').place(x=100, y=210)
                case _:
                    showinfo('', 'Choississez une devise', parent=self.c)

        self.c.bind("<Return>", convert_b)
        Button(self.c, text="Convertir", font=("arial", 14), bg='#3af076', command=convert).place(x=50, y=340, width=240)
    
    
    def new(self):
        os.popen("main.py")
    
    def new_bind(self, event):
        os.popen("main.py")
    
    
    def change_theme(self):
        theme_value = self.color.get()
        match (theme_value):                            
            case(2):
                self.frame["bg"] = "grey"
                self.lab_main["bg"] = "grey"
                self.lbl_search["bg"] = "grey"
                self.frame2["background"] = "grey"
                self.lbl_cat["bg"] = "grey"
                self.frame3["background"] = "grey"
                self.lb_name_cat["bg"] = "grey"
                self.lb_id_cat["bg"] = "grey"
            case(3):
                self.frame["bg"] = "purple"
                self.lab_main["bg"] = "purple"
                self.lbl_search["bg"] = "purple"
                self.frame2["background"] = "purple"
                self.lbl_cat["bg"] = "purple"
                self.frame3["background"] = "purple"
                self.lb_name_cat["bg"] = "purple"
                self.lb_id_cat["bg"] = "purple"
            case _:
                self.frame["bg"] = "#8080FF"
                self.lab_main["bg"] = "#8080FF"
                self.lbl_search["bg"] = "#8080FF"
                self.frame2["background"] = "#8080FF"
                self.lbl_cat["bg"] = "#8080FF"
                self.frame3["background"] = "#8080FF"
                self.lb_name_cat["bg"] = "#8080FF"
                self.lb_id_cat["bg"] = "#8080FF"
    
    def about(self):        
        showinfo("À propos de StockLab", "StockLab", detail="\r\nVersion: 2.3.14\r\nAuteur: Josué Luis Panzu\r\nDescription: Stock Lab est une application de gestion de stockage\r\nSystème: Windows x64 Linux MacOS\r\n\nCopyright (C) 2023 Walborn Inc.")
        
        
if __name__ == "__main__":
    window = MainWindow()
    window.root.mainloop()