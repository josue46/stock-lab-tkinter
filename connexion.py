import sqlite3 as s

with s.connect("stock.db") as connexion:
	cursor = connexion.cursor()

	# activation de la clé étrangère
	cursor.execute("PRAGMA foreign_keys = ON")
	    
	cursor.execute(""" CREATE TABLE IF NOT EXISTS categories (
		"id"	INTEGER,
		"nom"	TEXT NOT NULL,
		PRIMARY KEY("id" AUTOINCREMENT)
		); """)
	
	cursor.execute(""" CREATE TABLE IF NOT EXISTS products ("id" INTEGER, "nom" TEXT NOT NULL, "quantite" INTEGER, "etat_stock"	TEXT NOT NULL, "prix" INTEGER, "id_categorie" TEXT NOT NULL,
		PRIMARY KEY("id" AUTOINCREMENT), FOREIGN KEY("id_categorie") REFERENCES categories("nom") ); """)