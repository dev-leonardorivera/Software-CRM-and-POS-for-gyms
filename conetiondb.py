
import sqlite3 as sql
import time
from datetime import datetime, timedelta



"""
Autor: leonardo Rivera
fecha: 2022-04-05

"""


class formatos_validar():
    def __init__(self):
        self.formatoh= "%Y-%m-%d %H:%M:%S"  # formato con hora
        self.formatosh= "%Y-%m-%d"          # formato sin hora
        self.f_mes_actual = "%Y-%m-01"      # formato con el dia 1 
    def validar_cliente(self,ID_cliente):
        
        conn = sql.connect("databases/WS_GYMDB.db")
        cur = conn.cursor()
        cur.execute(f"SELECT COUNT(*) FROM CLIENTE WHERE ID_CLIENTE = '{ID_cliente}'")
        num = cur.fetchall()
        conn.close()
        
        i = num[0]
        j = i[0]

        return j
        


class inicio(formatos_validar):

    def login(self,us,ps):
        conn = sql.connect("databases/WS_GYMDB.db")
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM USER WHERE USER.NAME_USER ='{us}' AND USER.PASSWORD = '{ps}'")
        lg = cur.fetchall()
        conn.close()
        if len(lg) == 1:
            return True
        else:
            return False
    
    def total_registrados(self):
        conn = sql.connect("databases/WS_GYMDB.db")
        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM CLIENTE ")
        max_clientes = cur.fetchall()
        conn.close()
        
        i = max_clientes[0]
        j = i[0]
        return j
    
    def total_activos(self):
        fecha_Actual = time.strftime(self.formatosh)
       
        conn = sql.connect("databases/WS_GYMDB.db")
        cur = conn.cursor()
        cur.execute(f"SELECT count(*) FROM STATUS_MENBRESIA WHERE FECHA_FIN >= '{fecha_Actual}'")
        total = cur.fetchall()
        conn.close()
        i = total[0]
        j = i[0]
        return j

    def total_no_activos(self):
        fecha_Actual = time.strftime(self.formatosh)
        conn = sql.connect("databases/WS_GYMDB.db")
        cur = conn.cursor()
        cur.execute(f"SELECT count(*) FROM STATUS_MENBRESIA WHERE FECHA_FIN < '{fecha_Actual}'")
        total = cur.fetchall()
        conn.close()
        i = total[0]
        j = i[0]
        return j
        
    def news_customers(self):
        fecha = time.strftime(self.f_mes_actual)
        conn = sql.connect("databases/WS_GYMDB.db")
        cur = conn.cursor()
        cur.execute(f"SELECT count(*) FROM CLIENTE WHERE FECHA_CLIENTE >='{fecha}'")
        total = cur.fetchall()
        conn.close()
        i = total[0]
        j = i[0]
        return j
    
    def table_customer_main(self):
        fecha_Actual = time.strftime(self.formatosh)
        conn = sql.connect("databases/WS_GYMDB.db")
        cur = conn.cursor()
        cur.execute(f"SELECT CLIENTE.ID_CLIENTE, CLIENTE.NOMBRE, CLIENTE.APELLIDO, STATUS_MENBRESIA.FECHA_FIN FROM STATUS_MENBRESIA INNER JOIN CLIENTE ON STATUS_MENBRESIA.IDCLIENTE = CLIENTE.ID_CLIENTE WHERE STATUS_MENBRESIA.FECHA_FIN >= '{fecha_Actual}'")
        clientes = cur.fetchall()
        conn.close()
        
        return clientes
    
    def search_customer_table_main(self,ID_cliente): 
        
        conn = sql.connect("databases/WS_GYMDB.db")
        cur = conn.cursor()
        cur.execute(f"SELECT CLIENTE.ID_CLIENTE, CLIENTE.NOMBRE, CLIENTE.APELLIDO, STATUS_MENBRESIA.FECHA_FIN FROM STATUS_MENBRESIA INNER JOIN CLIENTE ON STATUS_MENBRESIA.IDCLIENTE = CLIENTE.ID_CLIENTE WHERE CLIENTE.ID_CLIENTE = '{ID_cliente}'")
        clientes = cur.fetchall()
        conn.close()
        
        return clientes

    def get_id_user(self,us,ps):
        conn = sql.connect("databases/WS_GYMDB.db")
        cur = conn.cursor()
        cur.execute(f"SELECT USER.ID_USER FROM USER WHERE NAME_USER = '{us}' and PASSWORD = '{ps}'")
        id_user = cur.fetchall()
        conn.close()
        i = id_user[0]

        return i[0]

class registro(formatos_validar):
    
    def buscar_cliente(self,ID_cliente):
        
        conn = sql.connect("databases/WS_GYMDB.db")
        cur = conn.cursor()
        cur.execute(f"SELECT ID_CLIENTE, NOMBRE, APELLIDO, N_TLF, DC_RECIDENCIAL  FROM CLIENTE WHERE ID_CLIENTE = '{ID_cliente}'")
        clientes = cur.fetchall()
        conn.close()
        #,nombre,apellido,n_tlf, dc_recidencial
        return clientes
        

    def guardar_cliente(self,ID_cliente,nombre,apellido,n_tfl,residencia):
        n = self.validar_cliente(ID_cliente) #si existe n = 1 si no n = 0
        
    
        if n == 1:
            #si existe hacemos un update
            #notificar que el cliente existe y que se le actualizaran los datos
            mensaje = self.update_cliente(ID_cliente,nombre,apellido,n_tfl,residencia,n)
            
        if n == 0:
            # no existe hacemos un insert
            mensaje = self.insert_cliente(ID_cliente,nombre,apellido,n_tfl,residencia,n)
        
        return mensaje
    

    def update_cliente(self,ID_cliente,nombre,apellido,n_tfl,residencia,n):
        mensaje = "Elc liente ya existe, se han actualizado sus datos."
        conn = sql.connect("databases/WS_GYMDB.db")
        cur = conn.cursor()
        cur.execute(f"UPDATE CLIENTE SET NOMBRE = '{nombre}', APELLIDO = '{apellido}', N_TLF ='{n_tfl}', DC_RECIDENCIAL = '{residencia}' WHERE ID_CLIENTE = {ID_cliente}")
        conn.commit()
        conn.close()
        return mensaje
        

    def insert_cliente(self,ID_cliente,nombre,apellido,n_tfl,residencia,n):
        fecha_Actual =  time.strftime(self.formatoh)
        conn = sql.connect("databases/WS_GYMDB.db")
        cur = conn.cursor()
        cur.execute(f"INSERT INTO CLIENTE VALUES ({ID_cliente}, '{nombre}', '{apellido}', '{n_tfl}','{residencia}', '{fecha_Actual}' )")
        conn.commit()
        conn.close()
        
        mensaje = "El cliente no existia, se ha guardado como nuevo."
        return mensaje

class pos(formatos_validar):
    def cliente(self,ID_cliente):
        conn = sql.connect("databases/WS_GYMDB.db")
        cur = conn.cursor()

        cur.execute(f"SELECT COUNT (*) FROM STATUS_MENBRESIA WHERE STATUS_MENBRESIA.IDCLIENTE = {ID_cliente}")
        validar_menbresia = cur.fetchall()
        cantidad = validar_menbresia[0]
        j = cantidad[0]
        n = self.validar_cliente(ID_cliente) #si existe n = 1 si no n = 0
        if j == 1:
            #si j igual a 1 consultamos la tabla status_menbresia de la base de datos  
           
            cur.execute(f"SELECT CLIENTE.ID_CLIENTE, CLIENTE.NOMBRE, CLIENTE.APELLIDO,CLIENTE.N_TLF, STATUS_MENBRESIA.FECHA_FIN FROM STATUS_MENBRESIA INNER JOIN CLIENTE ON STATUS_MENBRESIA.IDCLIENTE = CLIENTE.ID_CLIENTE WHERE CLIENTE.ID_CLIENTE = {ID_cliente}")
            
            cliente = cur.fetchall()
            conn.close()
            return cliente
        else:
            n = self.validar_cliente(ID_cliente) #si existe n = 1 si no n = 0   
        
            if n == 1:
                
                
                cur.execute(f"SELECT CLIENTE.ID_CLIENTE , CLIENTE.NOMBRE, CLIENTE.APELLIDO, CLIENTE.N_TLF FROM CLIENTE WHERE ID_CLIENTE = {ID_cliente}")
                
                cliente = cur.fetchall()
                conn.close()
                return cliente
            if n == 0 :
                return "NO SE ENCONTRO AL CLIENTE"


    def validar_menbresia(self,ID_cliente):
    
        conn = sql.connect("databases/WS_GYMDB.db")
        cur = conn.cursor()
        cur.execute(f"SELECT COUNT(*) FROM STATUS_MENBRESIA WHERE STATUS_MENBRESIA.IDCLIENTE = {ID_cliente}")
        num = cur.fetchall()
        conn.close()
        
        i = num[0]
        j = i[0]

        return j

    def pagar(self,ID_cliente,descuento,sub_total,total,ID_user,n_dias ):
        fecha_Actual = time.strftime(self.formatosh)
        fecha = datetime.strptime(fecha_Actual,self.formatosh) +timedelta(int(n_dias))
        fecha_final = datetime.strftime(fecha,self.formatosh)
        
        n = self.validar_cliente(ID_cliente) #si existe n = 1 si no n = 0
        if n == 1:
            if int(n_dias) >0:
                
                conn = sql.connect("databases/WS_GYMDB.db")
                cur = conn.cursor()
                cur.execute(f"INSERT INTO REGISTRO_PAGOS(FECHA, DESCUENTO, SUB_TOTAL,TOTAL, IDCLIENTE, IDUSER,CANTIDAD_DIAS) VALUES ('{time.strftime(self.formatoh)}', {descuento}, {sub_total},{total}, {ID_cliente},'{ID_user}', {n_dias})")
                v_menbresia = self.validar_menbresia(ID_cliente) # VALIDAR MENBRESIA
                if v_menbresia ==1:
                    conn = sql.connect("databases/WS_GYMDB.db")
                    cur = conn.cursor()
                    cur.execute(f"SELECT FECHA_FIN FROM STATUS_MENBRESIA WHERE IDCLIENTE = '{ID_cliente}'")
                    fecha_DB = cur.fetchall()
                    i = fecha_DB[0]
                    j = i[0]
                    fecha = datetime.strptime(j,self.formatosh) +timedelta(int(n_dias))
                    fecha_final = datetime.strftime(fecha,self.formatosh)
                    

                    cur.execute(f"UPDATE STATUS_MENBRESIA SET FECHA_INICIAL = '{fecha_Actual}',FECHA_FIN = '{fecha_final}', N_DIAS = {n_dias} WHERE IDCLIENTE = {ID_cliente}")
                else:
                    cur.execute(f"INSERT INTO STATUS_MENBRESIA (FECHA_INICIAL, FECHA_FIN, N_DIAS, IDCLIENTE) VALUES ('{fecha_Actual}','{fecha_final}',{n_dias},{ID_cliente})  ")

                conn.commit()
                conn.close()
                return "Pago realizado y menbresia actualizada"
            else:
                
                return "No hay cantidad de dias  para guardar"
        if n == 0 :
            
            return "NO SE ENCONTRO AL CLIENTE"

    def get_descuento(self):
        conn = sql.connect("databases/WS_CONFIGDB.db")
        cur = conn.cursor()
        cur.execute("SELECT PORCENTAJE FROM CONFIG WHERE ID = 1")
        descuento = cur.fetchall()
        conn.close()
        d = descuento[0]
        return d[0] 

    def get_precio(self):
        conn = sql.connect("databases/WS_CONFIGDB.db")
        cur = conn.cursor()
        cur.execute("SELECT PRECIO_DIA FROM CONFIG WHERE ID = 1")
        precio = cur.fetchall()
        conn.close()
        p = precio[0]
        return p[0]   

    def get_fecha_fin(self, n_dias, ID_cliente):


        fecha_Actual = time.strftime(self.formatosh)
        fecha = datetime.strptime(fecha_Actual,self.formatosh) +timedelta(int(n_dias))
        fecha_final = datetime.strftime(fecha,self.formatosh)
        
        n = self.validar_cliente(ID_cliente) #si existe n = 1 si no n = 0
        if n == 1:
            if int(n_dias) >0:
                
                
                
                v_menbresia = self.validar_menbresia(ID_cliente) # VALIDAR MENBRESIA
                if v_menbresia ==1:
                    conn = sql.connect("databases/WS_GYMDB.db")
                    cur = conn.cursor()
                    
                    cur.execute(f"SELECT FECHA_FIN FROM STATUS_MENBRESIA WHERE IDCLIENTE = '{ID_cliente}'")
                    fecha_DB = cur.fetchall()
                    i = fecha_DB[0]
                    j = i[0]
                    fecha = datetime.strptime(j,self.formatosh) +timedelta(int(n_dias))
                    fecha_final = datetime.strftime(fecha,self.formatosh)
                    conn.commit()
                    conn.close()
                    return fecha_final
                else:
                    return fecha_final
            else:
                pass
                
        if n == 0 :
            
            return fecha_final
        """fecha_Actual = time.strftime(self.formatosh)
        fecha = datetime.strptime(fecha_Actual,self.formatosh) +timedelta(n_dias)
        fecha_final = datetime.strftime(fecha,self.formatosh)

        return fecha_final"""


class consulta(formatos_validar):
    def buscar(self,ID_cliente):
        n = self.validar_cliente(ID_cliente) #si existe n = 1 si no n = 0
        if n == 1:
            
            
            conn = sql.connect("databases/WS_GYMDB.db")
            cur = conn.cursor()
            cur.execute(f"SELECT CLIENTE.NOMBRE, CLIENTE.APELLIDO, CLIENTE.N_TLF, CLIENTE.DC_RECIDENCIAL, STATUS_MENBRESIA.FECHA_INICIAL, STATUS_MENBRESIA.FECHA_FIN FROM STATUS_MENBRESIA INNER JOIN CLIENTE ON STATUS_MENBRESIA.IDCLIENTE = CLIENTE.ID_CLIENTE WHERE CLIENTE.ID_CLIENTE = {ID_cliente}")
            cliente = cur.fetchall()
            conn.close()
            return cliente
            
        if n == 0 :
            
            return False

class config():
    def cargar(self):
        conn = sql.connect("databases/WS_CONFIGDB.db")
        cur = conn.cursor()
        cur.execute("SELECT CONFIG.PRECIO_DIA , CONFIG.PORCENTAJE FROM CONFIG WHERE CONFIG.ID = 1")
        configuracion = cur.fetchall()
        conn.close()
        return configuracion

    def guardar(self, precio, porcentaje):
        conn = sql.connect("databases/WS_CONFIGDB.db")
        cur = conn.cursor()
        cur.execute(f"UPDATE CONFIG SET PRECIO_DIA = {precio}, PORCENTAJE = {porcentaje} WHERE ID = 1 ")
        conn.commit()
        conn.close()
        return True

"""def update():
    conn = sql.connect("databases/WS_GYMDB.db")
    cur = conn.cursor()
    cur.execute(f"SELECT FECHA_FIN FROM STATUS_MENBRESIA WHERE IDCLIENTE = 28316441")
    fecha_DB = cur.fetchall()
    conn.close()
    i = fecha_DB[0]
    j = i[0]
    fecha = datetime.strptime(j,"%Y-%m-%d") +timedelta(int('10'))
    fecha_final = datetime.strftime(fecha,"%Y-%m-%d")"""

if __name__ == "__main__":
   
    db = registro()
    db2 = inicio()
    db3 = pos()
    db4 = consulta()
    db5 = config()
    
   