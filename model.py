from sqlite3 import Error
import conexao

#o modelo pra rodar os comandos sql
#simplifiquei pra ter só o select que retorna a string e uma função genérica pros comandos que modificam
#o banco pra eu não fazer outro script e testar meu conhecimento dos comandos sql
#em si
class Model:
    def __init__(self):
        self.con = conexao.Conexao()

    def select(self, sql):
        try:
            con = self.con.get_conexao()
            cursor = con.cursor()
            result = cursor.execute(sql).fetchall()
            con.close()
            return result
        except Error as er:
            print(er)

    def comando(self, sql):
        try:
            con = self.con.get_conexao()
            cursor = con.cursor()
            cursor.execute(sql)
            if cursor.rowcount == 1: #Quantidade de linhas afetadas
                con.commit()
            con.close()
            return cursor.rowcount
        except Error as er:
            print(er)