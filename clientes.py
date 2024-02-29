import re

from PyQt6 import QtWidgets, QtCore, QtGui, QtSql
from PyQt6.QtWidgets import QComboBox

import conexion
import conexionClientes
import var


class Clientes():

    def validarArroba(self):

        try:
            arroba = var.ui.txtCorreo.text()

            arroba1 = "@"
            if not arroba1 in arroba:
                conexion.Conexion.show_warning("Debe estar el simbolo @ en el correo")


        except Exception as error:
            print('error al validar teléfono', error)



    @staticmethod
    def limpiarPanelCliente(self):
        """
            Limpia los campos del panel de cliente en la interfaz gráfica.

            Este método limpia los campos de texto y restablece la selección de los ComboBox en el panel de cliente en la interfaz
            gráfica.

            Args:
                self: Instancia de la clase.

            Returns:
                None

            """
        try:
            listawidgets = [var.ui.lblCodCliente, var.ui.txtDni2, var.ui.txt_razonSocial, var.ui.txtDireccionCliente,
                            var.ui.txtTelefono, var.ui.cmbProvinciaCliente, var.ui.cmbLocalidadCliente]
            for i in listawidgets:
                if hasattr(i, 'setText'):
                    i.setText(None)
                elif isinstance(i, QComboBox):  # borrar combobox
                    i.setCurrentIndex(-1)

        except Exception as error:
            print("error limpiando panel", error)

    def cargarFecha(qDate):
        """
            Carga la fecha seleccionada en el campo de texto correspondiente en la interfaz gráfica.

            Este método recibe una fecha en formato QDate y la formatea para luego asignarla al campo de texto de alta de cliente
            en la interfaz gráfica. Además, oculta el calendario después de cargar la fecha.

            Args:
                qDate (QDate): Fecha seleccionada.

            Returns:
                None

            """
        try:
            data = ('{:02d}/{:02d}/{:4d}'.format(qDate.day(), qDate.month(), qDate.year()))
            var.ui.txtAltaCliente.setText(str(data))
            var.calendar.hide()

        except Exception as error:
            print("error en cargar fecha", error)

    def validarTelefono(self=None):
        """
            Valida el formato del número de teléfono ingresado en la interfaz gráfica.

            Este método verifica que el número de teléfono ingresado contenga solo dígitos. En caso de no cumplir con el formato
            correcto, muestra un mensaje de aviso y limpia el campo de teléfono.

            Args:
                self: Parámetro opcional para permitir llamadas al método sin instancia específica.


            """
        try:
            telefono = var.ui.txtTelefono.text()

            if not telefono.isdigit():
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msg.setText('Escriba un número de teléfono correcto')
                msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                msg.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                msg.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                msg.exec()

                # Limpiar y enfocar el campo de teléfono
                var.ui.txtTelefono.clear()
                var.ui.txtTelefono.setFocus()

        except Exception as error:
            print('error al validar teléfono', error)

    def validarDni(dni):
        """
            Valida el formato del número de DNI ingresado en la interfaz gráfica.

            Este método verifica que el número de DNI ingresado cumpla con el formato y la letra de control correcta. Muestra un
            mensaje de aviso y limpia el campo de DNI en caso de no cumplir con las condiciones.

            Args:
                dni (str): Número de DNI a validar.

            Returns:
                bool: True si el DNI es válido, False si no lo es.

            """
        try:
            dni = str(dni).upper()
            var.ui.txtDni2.setText(str(dni))
            tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
            dig_ext = "XYZ"
            reemp_digito_extranjero = {'X': '0', 'Y': '1', 'Z': '2'}
            numeros = "1234567890"
            if len(dni) == 9:  # COMPRUEBO QUE SON 9
                dig_control = dni[8]  # TOMO LA LETRA DEL DNI QUE ESTÁ SITUADO EN LA POSICION 8
                dni = dni[:8]  # tomo los numeros del dni
                if dni[0] in dig_ext:
                    dni = dni.replace(dni[0], reemp_digito_extranjero[dni[0]])
                if len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni) % 23] == dig_control:
                    var.ui.lblValidarDni_2.setStyleSheet('color:green;')
                    var.ui.lblValidarDni_2.setText('V')
                    return True
                else:
                    var.ui.lblValidarDni_2.setStyleSheet('color:red;')
                    var.ui.lblValidarDni_2.setText('X')
                    var.ui.txtDni2.clear()  # Limpia el campo de texto
                    var.ui.txtDni2.setFocus()  # Mantiene el foco en el campo de texto

            else:
                var.ui.lblValidarDni_2.setStyleSheet('color:red;')
                var.ui.lblValidarDni_2.setText('X')
                var.ui.txtDni2.clear()  # Limpia el campo de texto
                var.ui.txtDni2.setFocus()  # Mantiene el foco en el campo de texto


        except Exception as error:
            print("Error en validar dni", error)

    def altaCliente(self):
        """
            Realiza el proceso de dar de alta a un cliente en la base de datos.

            Este método obtiene la información del cliente desde la interfaz gráfica, realiza algunas validaciones y luego llama al
            método correspondiente en la clase `ConexionCliente` para guardar el nuevo cliente en la base de datos.

            Args:
                self: Instancia de la clase.

            Returns:
                None

            """
        try:

            cliente = [var.ui.txtDni2, var.ui.txtAltaCliente, var.ui.txt_razonSocial, var.ui.txtDireccionCliente, var.ui.txtTelefono, var.ui.txtCorreo]
            newCliente = []

            for i in cliente:
                newCliente.append(i.text().title())

            ##AÑADIR PROVINCIAS AL CONDUCTOR
            prov = var.ui.cmbProvinciaCliente.currentText()
            newCliente.insert(5, prov)

            muni = var.ui.cmbLocalidadCliente.currentText()
            newCliente.insert(6, muni)
            print(newCliente)

            conexionClientes.ConexionCliente.guardarCliente(newCliente)
            Clientes.selEstadoCliente(1)

        except Exception as error:
            print("error alta cliente", error)

    def borrarCliente(self):
        """
            Realiza el proceso de dar de baja a un cliente en la base de datos.

            Este método obtiene el DNI del cliente desde la interfaz gráfica, llama al método correspondiente en la clase
            `ConexionCliente` para dar de baja al cliente en la base de datos y actualiza la lista de clientes en la interfaz.

            Args:
                self: Instancia de la clase.

            Returns:
                None

            """
        try:
            dni = var.ui.txtDni2.text()
            conexionClientes.ConexionCliente.borrarCliente(dni)
            conexionClientes.ConexionCliente.selectClientes(1)

        except Exception as error:
            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle('Aviso')
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            mensaje = ('          Cliente no existe o no se puede dar de baja          ')
            mbox.setText(mensaje)
            mbox.exec()

    def modificaCliente(self):
        """
            Realiza el proceso de modificar un cliente en la base de datos.

            Este método obtiene la información del cliente desde la interfaz gráfica, llama al método correspondiente en la clase
            `ConexionCliente` para modificar al cliente en la base de datos.

            Args:
                self: Instancia de la clase.

            Returns:
                None

            """
        try:
            cliente = [
                var.ui.lblCodCliente, var.ui.txtDni2, var.ui.txtAltaCliente, var.ui.txt_razonSocial, var.ui.txtDireccionCliente,
                var.ui.txtTelefono, var.ui.cmbProvinciaCliente, var.ui.cmbLocalidadCliente
            ]

            modificarNewCliente = []

            for i in cliente:
                if isinstance(i, QtWidgets.QComboBox):
                    modificarNewCliente.append(i.currentText())
                else:
                    modificarNewCliente.append(i.text().title())

            conexionClientes.ConexionCliente.modifCliente(modificarNewCliente)

        except Exception as error:
            print("Error al modificar el cliente", error)

    def cargarTablaClientes(registros):
        """
            Carga los registros de clientes en la tabla de clientes en la interfaz gráfica.

            Este método recibe una lista de registros de clientes y los muestra en la tabla de clientes en la interfaz gráfica.

            Args:
                registros (list): Lista de registros de clientes.

            Returns:
                None

            """
        try:

            index = 0
            for registro in registros:
                var.ui.tabClientes.setRowCount(index + 1)  # crea una fila
                var.ui.tabClientes.setItem(index, 0,QtWidgets.QTableWidgetItem(str(registro[0])))  # añadimos el new  en la tabla
                var.ui.tabClientes.setItem(index, 1, QtWidgets.QTableWidgetItem(str(registro[1])))
                var.ui.tabClientes.setItem(index, 2,QtWidgets.QTableWidgetItem(str(registro[2])))  # añadimos el new  en la tabla
                var.ui.tabClientes.setItem(index, 3, QtWidgets.QTableWidgetItem(str(registro[3])))  # añadimos el new  en la tabla
                var.ui.tabClientes.setItem(index, 4, QtWidgets.QTableWidgetItem(str(registro[4])))

                # Alineamos los items seleccionados
                var.ui.tabClientes.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabClientes.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                index += 1


        except Exception as error:
            print("Error mostrar tabla", error)

    def cargaCliente(self):
        """
            Carga los datos del cliente seleccionado en la interfaz gráfica.

            Este método obtiene la fila seleccionada en la tabla de clientes, llama al método `oneCliente` en la clase
            `ConexionCliente` para obtener los datos del cliente correspondiente y luego llama al método `cargarDatosCliente` para
            mostrar los datos en la interfaz.

            Args:
                self: Instancia de la clase.

            Returns:
                None

            """
        try:
            Clientes.limpiarPanelCliente(self)

            row = var.ui.tabClientes.selectedItems()
            fila = [dato.text() for dato in row]
            registro = conexionClientes.ConexionCliente.oneCliente(fila[0])

            # LLAMAMOS AL METODO CARGARDATOS PARA NO COPIAR CODIGO
            Clientes.cargarDatosCliente(registro)

        except Exception as error:
            print("Error al cargar los datos de un cliente ", error)

    def buscarClienteLupa(self):
        """
            Busca y resalta un cliente en la tabla de clientes según el DNI ingresado.

            Este método obtiene el DNI del cliente desde la interfaz gráfica, llama al método `codigoCliente` en la clase
            `ConexionCliente` para obtener el código del cliente correspondiente y luego llama al método `cargarDatosCliente` para
            mostrar los datos en la interfaz. Además, resalta la fila del cliente en la tabla.

            Args:
                self: Instancia de la clase.

            Returns:
                None

            """
        try:
            dni = var.ui.txtDni2.text()
            registro = conexionClientes.ConexionCliente.codigoCliente(dni)
            Clientes.cargarDatosCliente(registro)

            if var.ui.rbtTodosCliente.isChecked():
                estado = 0
                conexionClientes.ConexionCliente.selectClientes(estado)
            elif var.ui.rbtAltaCliente.isChecked():
                estado = 1
                conexionClientes.ConexionCliente.selectClientes(estado)
            elif var.ui.rbtBajaCliente.isChecked():
                estado = 2
                conexionClientes.ConexionCliente.selectClientes(estado)

            codigo = var.ui.lblCodCliente.text()
            for fila in range(var.ui.tabClientes.rowCount()):
                if var.ui.tabClientes.item(fila, 0).text() == str(codigo):
                    for columna in range(var.ui.tabClientes.columnCount()):
                        item = var.ui.tabClientes.item(fila, columna)
                        if item is not None:
                            item.setBackground(QtGui.QColor(255, 241, 150))
                    # Hacer scroll hasta la fila resaltada
                    var.ui.tabClientes.scrollToItem(var.ui.tabClientes.item(fila, 0))
                    break  # Salir del bucle una vez que se encuentra el driver

        except Exception as error:
            print("ERROR AL SELECCIONAR EL CLIENTE", error)

    def cargarDatosCliente(registro):
        """
            Carga los datos de un cliente en la interfaz gráfica.

            Este método recibe un registro de cliente y carga los datos en los campos correspondientes de la interfaz gráfica.

            Args:
                registro (list): Lista con los datos del cliente.


            """
        try:
            var.ui.lblCodCliente.setText(str(registro[0]))
            var.ui.txtDni2.setText(str(registro[1]))
            var.ui.txtAltaCliente.setText(registro[2])
            var.ui.txt_razonSocial.setText(str(registro[3]))
            var.ui.txtDireccionCliente.setText(str(registro[4]))
            var.ui.txtTelefono.setText(str(registro[5]))
            var.ui.cmbProvinciaCliente.setCurrentText(str(registro[6]))
            var.ui.cmbLocalidadCliente.setCurrentText(str(registro[7]))


            #AL CLICKEAR ENCIMA DEUN CLIENTE ME APARECE SU DNI EN CLIENTE DE LA TABLA FACTURACION
            var.ui.txtcifcliente.setText(str(registro[1]))

            print(registro)

        except Exception as error:
            print("Error al cargar los datos de un cliente ", error)

    def selEstadoCliente(self):
        """
            Selecciona y muestra los clientes según el estado elegido (todos, alta o baja).

            Este método verifica qué opción de estado de cliente (todos, alta o baja) está seleccionada y llama al método
            correspondiente en la clase `ConexionCliente` para seleccionar y mostrar los clientes en la interfaz gráfica.

            Args:
                self: Instancia de la clase.

            Returns:
                None

            """

        try:

            if var.ui.rbtTodosCliente.isChecked():  ##FUNCION PARA VERIFICAR QUE SE CLICKEO ENCIMA
                estado = 0
                conexionClientes.ConexionCliente.selectClientes(estado)

            elif var.ui.rbtAltaCliente.isChecked():

                estado = 1
                conexionClientes.ConexionCliente.selectClientes(estado)

            elif var.ui.rbtBajaCliente.isChecked():

                estado = 2
                conexionClientes.ConexionCliente.selectClientes(estado)


        except Exception as error:
            print("Error en selEstado:", error)

    def buscarClienteTabla(codigo):
        """
            Busca y selecciona un cliente en la tabla de clientes según su código.

            Este método recibe el código del cliente y busca la fila correspondiente en la tabla de clientes en la interfaz gráfica.
            Luego, selecciona la fila y realiza un scroll para que sea visible en la ventana.

            Args:
                codigo (int): Código del cliente a buscar.

            Returns:
                None

            """
        try:
            tabla = var.ui.tabClientes
            for fila in range(tabla.rowCount()):
                item = tabla.item(fila, 0)
                valorCelda = item.text()
                if valorCelda == int(codigo):
                    tabla.selectRow(fila)
                    tabla.scrollToItem(item)
                    print("Fila encontrada:", fila)
        except Exception as error:
            print('No se ha podido seleccionar al cliente en la tabla', error)
