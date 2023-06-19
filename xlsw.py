import locale
import xlsxwriter as xls
from src.product import get_all
from src.categorie import Categories
from datetime import datetime
from tkinter.messagebox import showinfo, showwarning


def inventory_excel_file():
    locale.setlocale(locale.LC_ALL, 'fr-FR')
    date = datetime.now().strftime("%B %Y")
    with xls.Workbook(f"inventaire {date}.xlsx") as w:
        # création de la feuille de travaille
        worksheet = w.add_worksheet('Inventaire des produits')
        
        # rédimensionnement des colonnes
        worksheet.set_column("A:A", 10)
        worksheet.set_column("B:B", 20)
        worksheet.set_column("C:C", 15)
        worksheet.set_column("D:D", 20)
        worksheet.set_column("E:E", 30)
        worksheet.set_column("F:F", 30)

		# définition d'un style pour les colonnes de l'en-tête
        style = w.add_format({
			"bg_color": "gray",
			"font_color": "white",
			"bold":True
			})

		# colonnes d'en-tête
        worksheet.write("A1", 'ID', style)
        worksheet.write("B1", 'Nom du produit', style)
        worksheet.write("C1", 'Quantité', style)
        worksheet.write("D1", 'Etat du stock', style)
        worksheet.write("E1", 'Prix', style)
        worksheet.write("F1", 'Catégorie', style)
        
        pos = 2	        
        prods = get_all()
        if not prods == []:
            for prod in prods:
                categorie_name = Categories.getNameById(prod[4])
                worksheet.write(f"A{pos}", prod[0])
                worksheet.write(f"B{pos}", prod[1])
                worksheet.write(f"C{pos}", prod[2])
                worksheet.write(f"D{pos}", prod[3])
                worksheet.write(f"E{pos}", prod[5])
                worksheet.write(f"F{pos}", categorie_name)
                
                pos +=1
                
            # si téléchargement réussi, envoyer ce message
            showinfo("Téléchargement réussi", "Le fichier excel a été téléchargé dans le dossier actuel")
        else:
            # si téléchargement échoué, envoyer ce message
            showwarning("Téléchargement échoué", "Aucune donnée n'a été téléchargé car le tableau des produits est vide")