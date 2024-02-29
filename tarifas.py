import time

from PyQt6 import QtWidgets, QtCore, QtGui, QtSql
from PyQt6.QtWidgets import QComboBox

import conexion
import conexionClientes
import var, re
import clientes
import viajes

class Tarifas():

    def selectTarifa(estado):

        try:


            if estado == 0:
                query = QtSql.QSqlQuery()
                query.prepare(
                    "select nacional from tarifas")
                if query.exec():
                    while query.next():
                        return query.value(0)


            elif estado == 1:
                query = QtSql.QSqlQuery()
                query.prepare(
                    "select provincial from tarifas")
                if query.exec():
                    while query.next():
                        return query.value(0)

            elif estado == 2:
                query = QtSql.QSqlQuery()
                query.prepare(
                    "select local from tarifas")
                if query.exec():
                    while query.next():
                        return query.value(0)

        except Exception as error:
            print("Error al seleccionar las tarifas", error)


    def cargaTarifaInterfaz(self):

        try:

            row = var.ui.tabTarifas.selectedItems()
            fila = [dato.text() for dato in row]
            #registro = Viajes.oneTarifa(fila[0])


            Tarifas.cargarDatosTarifa(fila)

        except Exception as error:
            print("Error al cargar los datos de una tarifa!! ", error)


    def cargarDatosTarifa(registro):


        try:
            var.ui.txtNacionalTarifa.setText(str(registro[0]))
            var.ui.txtProvincialTarifa.setText(str(registro[1]))
            var.ui.txtLocalTarifa.setText(str(registro[2]))


        except Exception as error:
            print("Error al cargar los datos de  tarifa", error)



    def resizeTabTarifa(self):

        try:
            header = var.ui.tabTarifas.horizontalHeader()
            for i in range(4): ##PONER EL RANGO DEL REGISTRO QUE HAY
                if i == 0:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Interactive)
                elif i == 1:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)

        except Exception as error:
            print("error al dimensionar la tabla facturas", error)


    def mostrarTarifa(self):

        try:
            registros = []

            query1 = QtSql.QSqlQuery()
            query1.prepare("select nacional, provincial, local from tarifas")
            if query1.exec():
                while query1.next():
                    row = [query1.value(i) for i in range(query1.record().count())]  # funcion lambda
                    registros.append(row)
            Tarifas.cargarTablaTarifa(registros)

        except Exception as error:
            print("error mostrar resultados", error)

    def cargarTablaTarifa(registros):


        try:

            index = 0
            for registro in registros:
                var.ui.tabTarifas.setRowCount(index + 1)  # crea una fila
                var.ui.tabTarifas.setItem(index, 0,QtWidgets.QTableWidgetItem(str(registro[0])))  # añadimos el new  en la tabla
                var.ui.tabTarifas.setItem(index, 1, QtWidgets.QTableWidgetItem(str(registro[1])))
                var.ui.tabTarifas.setItem(index, 2,QtWidgets.QTableWidgetItem(str(registro[2])))

                # Alineamos los items seleccionados
                var.ui.tabTarifas.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabTarifas.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                index += 1


        except Exception as error:
            print("Error mostrar tabla tarifa", error)



    def modificarTarifas(self):

        try:

            tarifa = [var.ui.txtNacionalTarifa, var.ui.txtProvincialTarifa, var.ui.txtLocalTarifa]

            modificarTarifa = []

            for i in tarifa:
                if isinstance(i, QtWidgets.QComboBox):
                    modificarTarifa.append(i.currentText())
                else:
                    modificarTarifa.append(i.text().title())


            Tarifas.modificarTarifaConexion(modificarTarifa)

        except Exception as error:
            print("Error al modificar la tarifa", error)


    def modificarTarifaConexion(modificartarifa):

        try:


            query = QtSql.QSqlQuery()
            query.prepare('update tarifas set nacional = :nacional, provincial = :provincial, local = :local')

            query.bindValue(':nacional', str(modificartarifa[0]))
            query.bindValue(':provincial', str(modificartarifa[1]))
            query.bindValue(':local', str(modificartarifa[2]))

            if query.exec():
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle('Aviso')
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText('Datos tarifa modificado')
                Tarifas.cargarTarifasEnTabla()
                mbox.exec()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle('Aviso')
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setText(query.lastError().text())
                mbox.exec()


        except Exception as error:
            print("Error al modificar tarifa en conexion", error)

    @staticmethod
    def cargarTarifasEnTabla():  ##TODO Método importante, carga los datos una vez que doy de alta, modifico o borro

        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("select nacional, provincial, local from tarifas")
            if query.exec():
                while query.next():
                    row = [query.value(i) for i in range(query.record().count())]  # funcion lambda
                    registro.append(row)

            Tarifas.cargarTablaTarifa(registro)

        except Exception as error:
            print("ERROR CARGAR FACTURA", error)





