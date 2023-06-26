from .entities.User import User
import requests
from bs4 import BeautifulSoup
import urllib.parse

class ModelUser():
    @classmethod
    def login(cls, db, user, table):
        try:
            cursor = db.connection.cursor()
            if table == 'users':
                sql = """SELECT idUser, username, password, Nombres, Apellidos, rango FROM {} 
                        WHERE username = '{}'""".format(table, user.username)
                cursor.execute(sql)
                row = cursor.fetchone()
                if row is not None:
                    rango = int(row[5])  # Convertir rango a entero
                    return User(row[0], row[1], User.check_password(row[2], user.password), row[3], row[4], 'Administrador', rango)
        
            elif table == 'maestros':
                sql = """SELECT idMaestro, Nombres, password, Apellidos FROM {} 
                        WHERE username = '{}'""".format(table, user.username)
                cursor.execute(sql)
                row = cursor.fetchone()
                if row is not None:
                   
                    return User(row[0], row[1], User.check_password(row[2], user.password), row[3], "Maestro")
            return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(cls, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT idUser, username, Nombres, Apellidos, rango FROM users WHERE idUser = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row is not None:
                rango = int(row[4])  # Convertir rango a entero
                return User(row[0], row[1], None, row[2], row[3], 'Administrador', rango)
            else:
                sql = "SELECT idMaestro, Nombres, Apellidos FROM maestros WHERE idMaestro = {}".format(id)
                cursor.execute(sql)
                row = cursor.fetchone()
                if row is not None:
                    return User(row[0], row[1], None, row[2], "Maestro")
                else:
                    return None
        except Exception as ex:
            raise Exception(ex)
        
def get_image_url(name):
    API_KEY = 'AIzaSyBsO-8A8qtM41tOKuZ07iTXimtq5AeQpJs'
    SEARCH_ENGINE_ID = '21a2bf56b1ed44b37'
    encoded_query = urllib.parse.quote(name)
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={encoded_query}&searchType=image"
    response = requests.get(url)
    data = response.json()

    if 'items' in data and len(data['items']) > 0:
        image_url = data['items'][0]['link']
    else:
        # Si no se encuentra ninguna imagen, puedes proporcionar una URL de imagen alternativa
        image_url = "URL_DE_IMAGEN_ALTERNATIVA"

    return image_url

