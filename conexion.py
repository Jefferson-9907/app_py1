import os
import pickle
import pyodbc

class ConnectDatabase:
    """this is the model class for ConnectDatabase class from module connect_database, it connects frontend and
    backend """

    def __init__(self, driver, server, database, autentication):
        self.__driver = driver
        self.__server = server
        self.__database = database
        self.__autentication = autentication

    def get_driver(self):
        return self.__driver

    def get_server(self):
        return self.__server

    def get_database(self):
        return self.__database

    def get_autentication(self):
        return self.__autentication

class DatabaseConnection:
    """
        Conectando el front-end a la base de datos, aquí se escribe todo el código del backend, como insertar,
        actualizar, borrar, seleccionar
    """

    def __init__(self):
        self.file()

        self.len = None
        self.dictcred = None  

    def file(self):
        """
            Extrayendo las credenciales para la conexión al servidor como:
            host, puerto, nombre de usuario, contraseña que luego se utilizan para conectarse a la base de datos
        """

        self.len = os.path.getsize("database_data.txt")
        if self.len > 0:
            f = open("database_data.txt", "rb")
            self.dictcred = pickle.load(f)

            for k, p in self.dictcred.items():
                a = p[0]
                po = p[1]
                u = p[2]
                pa = p[3]
                self.d_connection(a, po, u, pa)

    def d_connection(self, driv, serv, datab, trust_c):
        """
            Tomando 4 argumentos driver, server, database y trusted_connection 
        """
        self.connection = pyodbc.connect(driver=driv, server=serv, database=datab, trusted_connection=trust_c)
        self.cursor = self.connection.cursor()
        self.connection.setdecoding( pyodbc . SQL_CHAR , encoding = 'utf-8' )
        return self.cursor
    
    def __del__(self):
        """
            Si la conexión se encuentra sin uso, esto cerrará de todos modos esa conexión
        """
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()

        except BaseException as msg:
            pass

    def create(self, query):
        """
            Utilizado para crear la base de datos en el host
        """
        self.cursor.execute(query)
        self.connection.commit()

    def search(self, query, values):
        """
            Buscar los valores de la base de datos
        """
        self.cursor.execute(query, values)
        data = self.cursor.fetchall()
        self.connection.commit()
        return data

    def select(self, parametros, query):
        """
            :returns data
        """
        self.cursor.execute(query, parametros)
        data = self.cursor.fetchall()
        self.connection.commit()
        return data

    def update(self, query, values):
        """
            Actualiza los valores de la interfaz
        """
        self.cursor.execute(query, values)
        self.connection.commit()

