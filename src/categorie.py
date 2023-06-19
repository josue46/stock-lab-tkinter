import sqlite3 as s

class Categories:

    @classmethod
    def getCategories(cls):
                cts = cls.getAll()
                t = []
                for ct in cts:
                    t.append(ct[1])
                return t
    
    
    def getAll():
        """
        Cette fonction permet de recuperer toutes lignes de la table categories
        ensuite retourner le resultat sous form de dictionaire
        """        
        try:            
            with s.connect("stock.db") as connexion:
                cursor = connexion.cursor()
                # Enregistrer
                sql = "SELECT * FROM categories ORDER BY nom"
                cursor.execute(sql)
                categories = cursor.fetchall()

        except s.OperationalError as e:
            print('une erreur est survenue')
            print(e)
        
        finally:
            connexion.close()
        
        return categories       
    
    
    @staticmethod
    def getIdByName(name):
        """
        selectionner en fonction du nom de la categorie
        """
        categorie = None     
        try:           
            with s.connect("stock.db") as connexion:
                # Enregistrer
                cursor = connexion.cursor()
                q = "SELECT * FROM categories WHERE nom=?"
                cursor.execute(q, (name, ))
                categorie = cursor.fetchall()

        except s.OperationalError as e:
            print('une erreur est survenue')
            print(e)
        
        finally:
            connexion.close()
        
        return categorie
    
    
    @staticmethod
    def delete_cat_model(i: int): 
        try:
            with s.connect("stock.db") as connexion:                
                c = connexion.cursor()
                c.execute("DELETE FROM categories WHERE id=?", (i, ))
                c.execute("DELETE FROM products WHERE id_categorie=?", (i, ))
                connexion.commit()                                
        except s.OperationalError as e:
            print(e)
        finally:
            connexion.close()
    
    
    @staticmethod
    def update_cat_model(n: str, i: int):
        try:
            with s.connect("stock.db") as connexion:
                cur = connexion.cursor()
                cur.execute("UPDATE categories SET nom='{0}' WHERE id={1}".format(str(n).title(), i))
                connexion.commit()
        except s.OperationalError as e:
            print(e)
        finally:
            connexion.close()
    
    @staticmethod
    def create_cat_model(n: str):
        try:
            with s.connect("stock.db") as connexion:
                cur = connexion.cursor()
                insert_query = "INSERT INTO categories(nom) VALUES( ? )"
                cur.execute(insert_query, (str(n).title(), ))
                connexion.commit()
        except s.OperationalError as e:
            print(e)
        finally:
            connexion.close()


    @staticmethod
    def getNameById(idd):
        """
        selectionner en fonction de l'id de la categorie
        """
        categorie = None     
        try:           
            with s.connect("stock.db") as connexion:
                # Enregistrer
                cursor = connexion.cursor()
                q = "SELECT nom FROM categories WHERE id=?"
                cursor.execute(q, (idd, ))
                categorie = cursor.fetchall()                

        except s.OperationalError as e:
            print('une erreur est survenue')
            print(e)
        
        finally:
            connexion.close()
        
        return categorie[0][0]