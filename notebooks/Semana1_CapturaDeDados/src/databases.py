import psycopg2
import cx_Oracle
import pandas as pd
import numpy as np


class Postgresql:

    def create_table(self, query,user, password, host, port, database, connect = False):
        
        try:
            connection = psycopg2.connect(user = user ,
                                    password = password ,
                                    host = host ,
                                    port = port ,
                                    database = database )

            cursor = connection.cursor()
        
            create_query = query
        
            cursor.execute(create_query)
            connection.commit()
            print("Tabela criada no postgresql com sucesso ")

        except (Exception, psycopg2.DatabaseError) as error :
            print ("Erro durante a criação da tabela ", error)

        finally:
            #closing database connection.
                if connect:
                    cursor.close()
                    connection.close()
                    print("Conexão com Postgresql fechada")

    def retrieve_data(self,query, user, password, host, port, database, connect = True, objeto = 'pd'):
        
        try:
            connection = psycopg2.connect(user = user ,
                                    password = password ,
                                    host = host ,
                                    port = port ,
                                    database = database )

            cursor = connection.cursor()
        
            select_query = query
        
            cursor.execute(select_query)
            print("Buscando os dados!!!")

            resultado = cursor.fetchall()
            colunas = [desc[0] for desc in cursor.description]

            if objeto == 'pd':
                base = pd.DataFrame(resultado, columns=colunas)
            else:
                base = np.array(resultado)
            return base
        
        except (Exception, psycopg2.DatabaseError) as error :
            print ("Erro durante a criação da tabela ", error)

        finally:
            #closing database connection.
                if connect:
                    cursor.close()
                    connection.close()
                    print("Conexão com Postgresql fechada")


    def insert_data(self, df, tabela, user, password, host, port, database, connect = True):

        try:

            connection = psycopg2.connect(user = user ,
                                    password = password ,
                                    host = host ,
                                    port = port ,
                                    database = database )
            cursor = connection.cursor()


            cols=",".join([str(i) for i in df.columns.tolist()])

            for _,row in df.iterrows():
                sql = "INSERT INTO" + tabela + "(" +cols + ") VALUES (" + "%s,"*(len(row)-1) + "%s)"
                cursor.execute(sql, tuple(row))
                connection.commit()

        except (Exception, psycopg2.Error) as error :
            if connection:
                print("Erro durante a criação da tabela ", error)

        finally:
        #closing database connection.
            if connect:
                cursor.close()
                connection.close()
                print("Conexão com Postgresql fechada")


class Oracle:
    
    def retrieve_data(self,con,sql, connect=True):
    
        con = cx_Oracle.connect(con)
        try:
            cur = con.cursor()
            cur.execute(sql)
            dw = pd.DataFrame(cur.fetchall())
            cols = pd.DataFrame(cur.description).loc[:,0]
            dw = dw.rename(columns = cols)
            print(">Tabela Criada...")

        except cx_Oracle.IntegrityError as error:
            error_obj = error.args
            print('>Codigo do erro: ', error_obj.code)
            print('>Mensaem do erro: ', error_obj.message)
        else:
            print(">Dados obtidos com sucesso")

        if connect:
            con.close()
            print("Conexão com Oracle fechada")
        return dw
        
    
    def insert_data(self, df, tabela, con, sql, connect=True):
        con = cx_Oracle.connect(con)
        cols ="','".join([str(i) for i in df.columns.to_list()])

        try:
            cur = con.cursor()
            for _,row in df.iterrows():
                sql = "INSERT INTO" + tabela + "(" +cols + ") VALUES (" + "%s,"*(len(row)-1) + "%s)"
                cur.execute(sql,tuple(row))
                con.commit()
            print('>Commit realizaddo...')

        except cx_Oracle.IntegrityError as error:
            error_obj = error.args
            print('>Codigo do erro: ', error_obj.code)
            print('>Mensaem do erro: ', error_obj.message)
        else:
            print(">Dados obtidos com sucesso")

        if connect:
            con.close()
            print("Conexão com Oracle fechada")




