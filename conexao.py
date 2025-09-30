import sqlite3
from sqlite3 import Error
import sys
import os

class Conexao:
    #Conecta o BD
    #Cria as tabelas caso o arquivo do BD não exista ainda
    def get_conexao(self):
        caminho = self.caminho('save.db')
        try:
            con = sqlite3.connect(caminho)
            cursor = con.cursor()
            
            # Cria a tabela de usuarios se não existir
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    nome VARCHAR NOT NULL UNIQUE,
                    senha VARCHAR NOT NULL
                );
            """)
            
            # Cria a tabela chao se não existir
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chao (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    nome VARCHAR NOT NULL,
                    carinho INTEGER NOT NULL,
                    higiene INTEGER NOT NULL,
                    diversao INTEGER NOT NULL,
                    sono INTEGER NOT NULL,
                    fome INTEGER NOT NULL,
                    jog_id INTEGER NOT NULL,
                    FOREIGN KEY (jog_id) REFERENCES usuarios (id)
                );
            """)
            return con
        except Error as er:
            print((er))
	
	#Pro PyInstaller encontrar o arquivo
    def caminho(self, relativo):
        try:
            base = sys._MEIPASS
        except Exception:
            base = os.path.abspath(".")
        
        return os.path.join(base, relativo)