import sqlite3
from sqlite3 import Error

#Conecta com o BD
#Arrumar um jeito dele criar o BD caso não exista (NÃO ESQUECE) -- já arrumado
class Conexao:
    def get_conexao(self):
        caminho = 'banco.db'
        try:
            con = sqlite3.connect(caminho)
            cursor = con.cursor()
            
            #cria as tabelas caso o arrquivo não exista antes
            cursor.execute("""create table if not exists usuarios(
	id integer not null primary key autoincrement,
	nome varchar not null,
	senha varchar not null
);""")
            cursor.execute("""create table if not exists chao(
	id integer not null primary key autoincrement,
	nome varchar not null,
	carinho int not null,
	higiene int not null,
	diversao int not null,
	sono int not null,
	fome int not null,
	jog_id int not null,
	
	foreign key (jog_id) references usuarios (id)
);""")
            return con
        except Error as er:
            print(er)