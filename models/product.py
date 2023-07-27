import sqlite3 as sq

def delete_product(i):
    try:
        with sq.connect("stock.db") as connexion:                
            c = connexion.cursor()
            c.execute("DELETE FROM products WHERE id=?", (i, ))            
    except sq.OperationalError as error:
        print("Une erreur est survenu lors de la suppression du produit")
        print(error)
        connexion.rollback()
    else:
        connexion.commit()
    finally:
        connexion.close()


def update_product(name: str, quantity: int, state: str, id_cat: int, prix: int, idd: int):
    try:
        with sq.connect("stock.db") as connexion:            
            c = connexion.cursor()
            query = """ UPDATE products SET nom='{}', quantite={}, etat_stock='{}', prix='{}', id_categorie='{}' WHERE id={} """
            c.execute(query.format(str(name).title(), quantity, str(state), int(prix), str(id_cat), idd ))
    except sq.OperationalError as error:
        print("Une erreur est survenu lors de la modification du produit")
        print(error)
        connexion.rollback()
    else:
        connexion.commit()
    finally:
        connexion.close()


def register_product(n: str, q: int, e: str, i: int, p: int):
    """cette fonction prend toutes les données nécessaire pour l'ajout
        d'un produit dans la base des données

    Args:
        n (str): le nom du produit
        q (int): la quantité du produit en stock
        e (str): l'état du produit (soit en stock soit vide ou en rupture de stock)
        i (int): indentifiant de la catégorie à laquelle appartient le produit
        p (int): prix du produit
    """
    try:
        with sq.connect("stock.db") as connexion:
            cur = connexion.cursor()
            insert_query = "INSERT INTO products(nom, quantite, etat_stock, id_categorie, prix) VALUES( ?, ?, ?, ?, ? )"
            cur.execute(insert_query, (str(n).title(), int(q), str(e), i, int(p)))
    except sq.OperationalError as e:
        print(e)
        connexion.rollback()
    else:
        connexion.commit()
    finally:
        connexion.close()


def get_all() -> list:
    """
    Cette fonction récupère tous les produits dans la base des données
    et les retourne sous forme d'une liste
    Returns:
        list: la liste de tous les produits
    """
    products = None
    try:
        with sq.connect("stock.db") as connexion:
            cursor = connexion.cursor()
            cursor.execute("SELECT * FROM products ORDER BY nom")
    except sq.OperationalError as e:
        print(e)
    else:
        products = cursor.fetchall()
    finally:
        connexion.close()
    
    return products


def search_product_by_name(name: str):
    rows = None
    try:
        with sq.connect("stock.db") as connexion:
            cur = connexion.cursor()
            cur.execute("SELECT * FROM products WHERE nom LIKE'%" + str(name) + "%' ")            
    except Exception as e:
        print(e)
    else:
        rows = cur.fetchall()
    finally:
        connexion.close()
                    
    return rows
        
        
def search_product_by_categorie(cat: str):
    try:
        with sq.connect("stock.db") as connexion:
            cur = connexion.cursor()
            cur.execute("SELECT * FROM products WHERE id_categorie=? ", (cat, ))            
    except Exception as e:
        print(e)
    else:
        rows = cur.fetchall()
    finally:
        connexion.close()
    
    return rows