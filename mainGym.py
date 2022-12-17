import sys
import conetiondb as cdb
from Ui_gui import *
from PyQt5 import QtCore, QtGui, QtWidgets 
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QTableWidgetItem




class MiApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.validar_login)
        self.ui.btn_inicio.clicked.connect(self.inicio)
        self.ui.bnt_registro.clicked.connect(lambda: self.ui.page_option.setCurrentWidget(self.ui.page_registro))
        self.ui.btn_pos.clicked.connect(self.abrir_pos)
        self.ui.btn_pos_2.clicked.connect(lambda: self.ui.page_option.setCurrentWidget(self.ui.page_consulta))
        self.ui.bnt_config.clicked.connect(self.config)
        self.ui.btn_cliente_7.clicked.connect(self.buscar_datos_inicio)
        self.ui.btn_cliente_5.clicked.connect(self.buscar_datos_registro)
        self.ui.pushButton_6.clicked.connect(self.limpiar_registro)
        self.ui.btn_cliente_6.clicked.connect(self.registrar_cliente)
        self.ui.btn_cliente_4.clicked.connect(self.buscar_datos_pos)
        self.ui.btn_cliente_2.clicked.connect(self.guardar_datos_config)
        self.ui.lineEdit_15.returnPressed.connect(self.buscar_datos_inicio)
        self.ui.lineEdit_11.returnPressed.connect(self.buscar_datos_registro)
        self.ui.lineEdit_2.returnPressed.connect(self.validar_login)
        self.ui.lineEdit_12.returnPressed.connect(self.buscar_datos_pos)
        self.ui.lineEdit_13.returnPressed.connect(self.cargar_pago_pos)
        self.ui.lineEdit_14.returnPressed.connect(self.cargar_pago_pos)
        self.ui.btn_cliente_9.clicked.connect(self.btn_pagar_pos)
        self.ui.btn_cliente_3.clicked.connect(self.buscar_cliente_consulta)
        self.ui.lineEdit_10.returnPressed.connect(self.buscar_cliente_consulta)
        


    def validar_login(self):
        us = self.ui.lineEdit.text()
        ps = self.ui.lineEdit_2.text()
        db = cdb.inicio()
        user = db.login(us,ps)
        if user==True:
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_main)
            self.inicio()
            self.cargar_datos_inicio()

        else:
            self.ui.lineEdit.setStyleSheet("border: none;\n"
"border-bottom: 2px solid rgb(255, 0, 0);\n"
"color:rgb(255, 0, 0);\n"
"padding: 2px;\n"
"\n"
"")
            self.ui.lineEdit_2.setStyleSheet("border: none;\n"
"border-bottom: 2px solid rgb(255, 0, 0);\n"
"color:rgb(255, 0, 0);\n"
"padding: 2px;\n"
"\n"
"")
            self.alertbox("El usuario o clave introducido no es conrrecto")
           
    def alertbox(self,mensaje):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(mensaje)
        msgBox.setWindowTitle("Alerta")
        msgBox.setStandardButtons(QMessageBox.Ok)
        

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            pass
    
    def inicio(self):
        self.ui.page_option.setCurrentWidget(self.ui.page_inicio)
        
        self.cargar_datos_inicio()

    def config(self): 
        self.ui.page_option.setCurrentWidget(self.ui.page_config)
        self.cargar_datos_config()

    def cargar_datos_inicio(self):
        datos = cdb.inicio()
        n_total = str(datos.total_registrados())
        n_activos = str(datos.total_activos())
        n_no_activos = str(datos.total_no_activos())
        new_customers = str(datos.news_customers())
        tabla = datos.table_customer_main()
        self.ui.label_36.setText(n_total)
        self.ui.label_38.setText(n_activos)
        self.ui.label_40.setText(n_no_activos)
        self.ui.label_42.setText(new_customers)

        self.ui.tableWidget.clearContents()
        row = 0
        for item in tabla:
            self.ui.tableWidget.setRowCount(row +1)
            self.ui.tableWidget.setItem(row, 0,QTableWidgetItem(str(item[0])))
            self.ui.tableWidget.setItem(row, 1,QTableWidgetItem(item[1]))
            self.ui.tableWidget.setItem(row, 2,QTableWidgetItem(item[2]))
            self.ui.tableWidget.setItem(row, 3,QTableWidgetItem(str(item[3])))
            
            row  +=1 

    def buscar_datos_inicio(self):
        datos = cdb.inicio()
        ID_cliente = self.ui.lineEdit_15.text()
        if len(ID_cliente) ==0:
            self.cargar_datos_inicio()
        else:
            tabla = datos.search_customer_table_main(ID_cliente)
            self.ui.tableWidget.clearContents()
            row=0
            for item in tabla:
                self.ui.tableWidget.setRowCount(row +1)
                self.ui.tableWidget.setItem(row, 0,QTableWidgetItem(str(item[0])))
                self.ui.tableWidget.setItem(row, 1,QTableWidgetItem(item[1]))
                self.ui.tableWidget.setItem(row, 2,QTableWidgetItem(item[2]))
                self.ui.tableWidget.setItem(row, 3,QTableWidgetItem(str(item[3])))
                
                row  +=1 

        self.ui.lineEdit_15.setText('')

    def buscar_datos_registro(self):
        datos = cdb.registro()
        ID_cliente = self.ui.lineEdit_11.text()
        if len(ID_cliente) != 0:
            valido = datos.validar_cliente(ID_cliente)
            if valido == 1:
                cliente = datos.buscar_cliente(ID_cliente)
                items = cliente[0]
                self.ui.lineEdit_11.setText(str(items[0]))
                self.ui.lineEdit_4.setText(items[1])
                self.ui.lineEdit_8.setText(items[2])
                self.ui.lineEdit_6.setText(items[3])
                self.ui.textEdit_2.setText(items[4])
            else:
                self.alertbox("La cedula ingresada es incorrecta o no se encuentra registrada")
        else:
            self.ui.lineEdit_11.setText('')
            self.ui.lineEdit_4.setText('')
            self.ui.lineEdit_8.setText('')
            self.ui.lineEdit_6.setText('')
            self.ui.textEdit_2.setText('')

    def limpiar_registro(self):
        self.ui.lineEdit_11.setText('')
        self.ui.lineEdit_4.setText('')
        self.ui.lineEdit_8.setText('')
        self.ui.lineEdit_6.setText('')
        self.ui.textEdit_2.setText('')

    def registrar_cliente(self):
        datos = cdb.registro()
        ID_cliente = self.ui.lineEdit_11.text()
        nombre = self.ui.lineEdit_4.text()
        apellido = self.ui.lineEdit_8.text()
        n_tlf = self.ui.lineEdit_6.text()
        dc_recidencial = self.ui.textEdit_2.toPlainText()

        if len(ID_cliente) != 0:
            if ID_cliente.isdigit() and n_tlf.isdigit():
                if len(nombre) != 0 and len(apellido) != 0 and len(n_tlf) != 0 and len(dc_recidencial) != 0 : 
                    mensaje = datos.guardar_cliente(ID_cliente, nombre, apellido, n_tlf, dc_recidencial)
                    self.alertbox(mensaje)
                else:
                    self.alertbox("Falto algun campo por llenar")
            else:
                self.alertbox("La Identificacion ingresada o el telefono no es un digito numerico")

        else:
            self.alertbox("No hay ninguna identificacion para registrar")
        
    def  buscar_datos_pos(self):
        datos = cdb.pos()
        ID_cliente = self.ui.lineEdit_12.text()
        if len(ID_cliente) !=0:
            valido = datos.validar_cliente(ID_cliente)
            if valido == 1:
                cliente = datos.cliente(ID_cliente)
                
                if type(cliente) == str:
                    self.alertbox(cliente)
                else: 
                    item = cliente[0]
                    self.ui.lineEdit_12.setText(str(item[0]))
                    self.ui.label_27.setText(item[1]+' '+ item[2])
                    self.ui.label_28.setText(item[3])
                    try:
                        self.ui.label_31.setText(item[4])
                    except:
                        self.ui.label_31.setText('0-0-0')
                        
                        pass
            else:
                self.alertbox("La cedula ingresada es incorrecta o no se encuentra registrada")
            

        else:
            self.alertbox("No hay una identificacion del cliente pasa buscar.")
            self.ui.label_27.setText('')
            self.ui.label_28.setText('')
            self.ui.label_31.setText('')

    def cargar_datos_config(self):
        datos = cdb.config()
        config = datos.cargar()
        item = config[0]
        self.ui.lineEdit_9.setText(str(item[0]))
        self.ui.lineEdit_3.setText(str(item[1]))

    def guardar_datos_config(self):
        datos = cdb.config()
        try:
            precio = float(self.ui.lineEdit_9.text())
            porcentaje = float(self.ui.lineEdit_3.text())
            validar = datos.guardar(precio,porcentaje)
            if validar == True:
                self.alertbox("La configuracion se guardo con exito")
        except:
            self.alertbox("Los datos introducidos no son digitos numericos")

    def abrir_pos(self):
        datos = cdb.pos()
        self.ui.page_option.setCurrentWidget(self.ui.page_pos)
        descuento = str(datos.get_descuento())
        
        self.ui.lineEdit_14.setText(descuento)

    def cargar_pago_pos(self):
        datos = cdb.pos()
        dias = self.ui.lineEdit_13.text()
        precio =    datos.get_precio()
        porcentaje = float(self.ui.lineEdit_14.text())
        sub_total = float(dias)*float(precio)
        porcentaje = (porcentaje*sub_total)/100
        total = sub_total - porcentaje
        ID_cliente = self.ui.lineEdit_12.text()
        fecha_fin = datos.get_fecha_fin(int(dias),ID_cliente)
        self.ui.label_33.setText(str(fecha_fin))
        self.ui.label_48.setText(str(sub_total))
        self.ui.label_62.setText(str(total))

    def btn_pagar_pos(self):
        us = self.ui.lineEdit.text()
        ps = self.ui.lineEdit_2.text()
        datos = cdb.inicio()
        pagar = cdb.pos()
        #dias = self.ui.lineEdit_13.text()
        #precio =    pagar.get_precio()
        #sub_total = float(dias)*float(precio)
        
        #ID_cliente = self.ui.lineEdit_12.text()
        #descuento = float(self.ui.lineEdit_14.text())
        #descuento = (porcentaje*sub_total)/100
        #total = sub_total - porcentaje
        #fecha_fin = datos.get_fecha_fin(int(dias) )
        ID_cliente = self.ui.lineEdit_12.text()
        descuento  = self.ui.lineEdit_14.text()
        sub_total  = self.ui.label_48.text()
        total = self.ui.label_62.text()
        ID_user = datos.get_id_user(us, ps)
        n_dias = self.ui.lineEdit_13.text()

        if len(ID_cliente) !=0:
            mensaje = pagar.pagar(ID_cliente, descuento, sub_total, total, ID_user, n_dias)
        
            self.ui.label_27.setText('')
            self.ui.label_28.setText('')
            self.ui.label_31.setText('')
            self.ui.lineEdit_12.setText('')
            self.ui.lineEdit_13.setText('')
            self.ui.label_33.setText('')
            self.ui.lineEdit_14.setText('')
            self.ui.label_48.setText('0$')
            self.ui.label_62.setText('0$')
            self.alertbox(mensaje)
        else:
            self.alertbox("No hay cedula asignada para cobrar.")

    def buscar_cliente_consulta(self):
        datos = cdb.consulta()
        ID_cliente = self.ui.lineEdit_10.text()
        if len(ID_cliente) != 0:
            valido = datos.buscar(ID_cliente)
            if valido != False:
                
                items = valido[0]
                self.ui.label_18.setText(items[0])#nombre
                self.ui.label_20.setText(items[1])#apellid
                self.ui.label_15.setText(items[2])#numero de telefono
                self.ui.textBrowser.setText(items[3])#descripcion residencial
                self.ui.label_9.setText(items[4])#fecha registro
                self.ui.label_13.setText(items[5])# fin menbresia
                
                
            else:
                self.alertbox("La cedula ingresada es incorrecta o no se encuentra registrada")
        else:
            self.ui.label_18.setText('')
            self.ui.label_20.setText('')
            self.ui.label_9.setText('')
            self.ui.label_13.setText('')
            self.ui.label_15.setText('')
            





       
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mi_app = MiApp()
    mi_app.show()
    sys.exit(app.exec_())	


