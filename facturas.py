import time

from PyQt6 import QtWidgets, QtCore, QtGui, QtSql
from PyQt6.QtWidgets import QComboBox

import conexion
import conexionClientes
import var, re
import clientes
import viajes


class Facturas():


    @staticmethod
    def limpiarPanelFacturas():
        """

            Método estático para limpiar y restablecer los elementos del panel de facturas en la interfaz gráfica.

            Este método limpia y restablece los valores de varios widgets en el panel de facturas, incluyendo etiquetas, campos
            de texto y un ComboBox.

            Args:
                No recibe argumentos directos, pero utiliza widgets de la interfaz gráfica para realizar la limpieza.

            Returns:
                No devuelve ningún valor explícito, pero limpia y restablece los elementos del panel de facturas en la interfaz gráfica.

            """
        try:
            listawidgets = [var.ui.lblNumFac, var.ui.txtcifcliente, var.ui.txtAltaFac, var.ui.cmbFactura]
            for i in listawidgets:
                if hasattr(i, 'setText'):
                    i.setText(None)
                elif isinstance(i, QComboBox):  # borrar combobox
                    i.setCurrentIndex(-1)

            conexion.Conexion.cargarFacturas()

        except Exception as error:
            print("error limpiando panel de facturas", error)

    @staticmethod
    def abrirCalendarioFac(self):
        """
            Método estático para abrir el calendario de facturación en la interfaz gráfica.

            Este método muestra el calendario de facturación en la interfaz gráfica cuando se invoca.

            Args:
                No recibe argumentos directos.

            Returns:
                No devuelve ningún valor explícito, pero muestra el calendario de facturación en la interfaz gráfica.

            """
        try:
            var.calendar.show()
        except Exception as error:
            print("error en abrir calendario en facturacion", error)

    def dataFactura(qDate):
        """
            Método para cargar la fecha seleccionada en el calendario en el campo de texto de fecha de facturación.

            Este método toma la fecha seleccionada en el calendario y la formatea como una cadena con el formato 'dd/mm/yyyy',
            luego actualiza el campo de texto de fecha de facturación en la interfaz gráfica.

            Args:
                qDate (QDate): La fecha seleccionada en el calendario.

            Returns:
                No devuelve ningún valor explícito, pero actualiza el campo de texto de fecha de facturación en la interfaz gráfica.

            """
        try:
            data = ('{:02d}/{:02d}/{:4d}'.format(qDate.day(), qDate.month(), qDate.year()))
            var.ui.txtAltaFac.setText(str(data))
            var.calendar.hide()

        except Exception as error:
            print("error en cargar fecha en facturas", error)

    def altaFactura(self):

        """
            Método para realizar el alta de una factura utilizando la información ingresada en la interfaz gráfica.

            Este método obtiene la información del cliente, la fecha y el tipo de factura desde la interfaz gráfica,
            forma un registro y lo pasa al método 'altaFacturacion' de la clase 'Conexion' para realizar el alta.

            Args:
                No recibe argumentos directos, pero utiliza la información ingresada en la interfaz gráfica.

            Returns:
                No devuelve ningún valor explícito, pero realiza el alta de la factura utilizando la clase 'Conexion'.

            """
        try:

            registro = [var.ui.txtcifcliente.text(), var.ui.txtAltaFac.text(),var.ui.cmbFactura.currentText().split('-')[0], var.ui.txt_descuento.text()]

            conexion.Conexion.altaFacturacion(registro)

        except Exception as error:
            print("error alta factura", error)

    def cargarTablaFacturas(registros):
        """
            Método para cargar datos en la tabla de facturas en la interfaz gráfica.

            Este método recibe una lista de registros y los utiliza para llenar la tabla de facturas en la interfaz gráfica.
            Cada fila de la tabla representa un registro, y se incluye un botón para borrar la factura asociada.

            Args:
                registros (list): Lista de registros de facturas a cargar en la tabla.

            Returns:
                No devuelve ningún valor explícito, pero carga los datos en la tabla de facturas de la interfaz gráfica.

            """

        try:
            index = 0
            for registro in registros:
                var.ui.tabFacturas.setRowCount(index + 1)  # crea una fila
                var.ui.tabFacturas.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                var.ui.tabFacturas.setItem(index, 1, QtWidgets.QTableWidgetItem(str(registro[1])))

                # Alineamos los items seleccionados
                var.ui.tabFacturas.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabFacturas.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                btn_borrar = QtWidgets.QPushButton()
                btn_borrar.setFixedSize(30, 28)
                btn_borrar.setIcon(QtGui.QIcon('./img/basura.png'))
                var.ui.tabFacturas.horizontalHeader().setSectionResizeMode(2,QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

                var.ui.tabFacturas.setColumnWidth(2, 50)
                var.ui.tabFacturas.setCellWidget(index, 2, btn_borrar)
                btn_borrar.clicked.connect(Facturas.borrarFactura)

                index += 1

        except Exception as error:
            print("Error carga tabla facturar", error)

    """ZONA CONEXION FACTURAS"""

    def oneFactura(codigo):
        """
            Método para obtener los datos de una factura específica mediante su código.

            Este método realiza una consulta a la base de datos para obtener los detalles de una factura dado su código.
            Incluye el número de factura, el DNI del cliente, la fecha y el nombre del driver asociado.

            Args:
                codigo (int): El código de la factura que se desea obtener.

            Returns:
                list: Una lista que contiene los detalles de la factura, incluyendo el número de factura, el DNI del cliente,
                la fecha y el nombre del driver (o un mensaje si el driver no se encuentra).

            """
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT numfac, dnicliente, fecha, driver, descuento FROM facturas WHERE numfac = :numfac")
            query.bindValue(":numfac", int(codigo))

            if query.exec():
                if query.next():
                    for i in range(5):  # Cambiado a 4 para incluir el campo 'driver'
                        if i == 3:  # Si estamos en la posición del campo 'driver'
                            driver_id = query.value(i)
                            # Realizar una segunda consulta para obtener el nombre del driver
                            driver_query = QtSql.QSqlQuery()
                            driver_query.prepare("SELECT codigo, nombredriver FROM drivers WHERE codigo = :codigo")
                            driver_query.bindValue(":codigo", driver_id)
                            if driver_query.exec() and driver_query.next():
                                # Concatenar el ID y el nombre del driver con un guion medio
                                id_nombre_driver = f"{driver_query.value(0)}-{driver_query.value(1)}"
                                registro.append(str(id_nombre_driver))
                            else:
                                registro.append("Driver no encontrado")  # En caso de que no se encuentre el driver
                        else:
                            registro.append(str(query.value(i)))

            return registro

        except Exception as error:
            print("Error en fichero conexion datos de UNA FACTURA: ", error)

    #METODO PARA QUE CARGUE EN EL COMBOX DE FACTURA TODOS LOS DRIVERS
    @staticmethod
    def cargadrivers(self=None):
        """

        Método estático para cargar los conductores disponibles en un ComboBox de la interfaz gráfica.

        Este método realiza una consulta a la base de datos para obtener los conductores que están activos
        (sin fecha de baja) y carga sus códigos y apellidos en un ComboBox de la interfaz gráfica.

        Args:
            self: Parámetro opcional para permitir llamadas al método sin instancia específica.

        Returns:
            None

    """
        try:
            var.ui.cmbFactura.clear()  # LIMPIA Y VUELVE A RECARGAR

            query = QtSql.QSqlQuery()
            query.prepare('select codigo, apeldriver from drivers where bajadriver is null')
            var.ui.cmbFactura.addItem(' ')

            if query.exec():
                var.ui.cmbFactura.addItem(' ')
                while query.next():  # LLENAR LOS CONDUCTORES MIENTRAS HAYA
                    # Obtener el código y el nombre del driver y concatenarlos en una sola cadena
                    codigo = str(query.value(0))
                    apellido = str(query.value(1))
                    texto_completo = f"{codigo}-{apellido}"
                    var.ui.cmbFactura.addItem(texto_completo)
        except Exception as error:
            print("error al cargar drivers en facturación", error)

    def cargarDatosFactura(registro):
        """
        Método para cargar los datos de una factura en la interfaz gráfica.

        Este método recibe una lista de datos de una factura y los utiliza para actualizar los elementos correspondientes
        en la interfaz gráfica, incluyendo el número de factura, el DNI del cliente, la fecha y el driver asociado.

        Args:
            registro (list): Lista que contiene los datos de una factura.

        Returns:
            None

    """
        try:
            datos = [var.ui.lblNumFac, var.ui.txtcifcliente, var.ui.txtAltaFac, var.ui.cmbFactura, var.ui.txt_descuento]

            for j, dato in enumerate(datos):
                # Si el índice j es igual a 3, significa que dato se refiere a un elemento desplegable (cmbFactura).
                if j == 3:
                    # Eliminar espacios adicionales antes y después del valor antes de establecerlo en el ComboBox
                    valor_combo = str(registro[j]).strip()
                    var.ui.cmbFactura.addItem(valor_combo)  # Agregar el valor al ComboBox
                    var.ui.cmbFactura.setCurrentText(valor_combo)  # Establecer el valor seleccionado
                else:
                    dato.setText(str(registro[j]))

        except Exception as error:
            print("Error al cargar los datos de una factura ", error)

    @staticmethod
    def cargaFactura():
        """
            Método para cargar los datos de una factura seleccionada en la interfaz gráfica.

            Este método obtiene la fila seleccionada en la tabla de facturas, recupera el código de la factura asociada,
            utiliza el método 'oneFactura' para obtener los datos de la factura, y luego carga esos datos en la interfaz gráfica.

            Args:
                self: Instancia de la clase que invoca el método.

            Returns:
                None

            """
        try:

            row = var.ui.tabFacturas.selectedItems()
            fila = [dato.text() for dato in row] ## Informacion de factura + cif cliente
            # El metodo oneFactura retorn registro, aqui devuelve el registro completo de la factura la cual su identificador es fila[0], primer id de la columna
            registro = Facturas.oneFactura(fila[0])
            print("printeo registro carga factura"+str(registro))


            # LLAMAMOS AL METODO CARGARDATOS PARA NO COPIAR CODIGO
            Facturas.cargarDatosFactura(registro)
            viajes.Viajes.cargarTablaViajes(registro)

        except Exception as error:
            print("Error al cargar los datos DE UNA FACTURA EN CARGAFACTURA ", error)




    def codigoFactura(codigo):
        """
            Método para buscar y obtener los datos de una factura a partir de su número.

            Este método realiza una consulta a la base de datos para buscar la factura con el número proporcionado.
            Luego, utiliza el número de factura encontrado para buscar y devolver los datos del viaje asociado.

            Args:
                codigo (str): Número de la factura que se desea buscar.

            Returns:
                list or None: Lista con los datos del viaje asociado a la factura encontrada o None si no se encuentra ninguna factura.

            """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT numfac FROM facturas WHERE numfac = :cod")
            query.bindValue(":cod", str(codigo))

            if query.exec():
                codigofactura = None
                while query.next():
                    codigofactura = query.value(0)
                    viajes.Viajes.buscarViajeTabla(codigofactura)


                if codigofactura is not None:
                    registro = viajes.Viajes.oneViaje(codigofactura)
                    return registro
                else:
                    conexion.Conexion.show_info("Debes seleccionar un viaje")
                    return None

        except Exception as error:
            print("Error en búsqueda de código de un cliente: ", error)

            return None


    @staticmethod
    def borrarFactura(self):
        """
            Método estático para eliminar una factura seleccionada de la base de datos.

            Este método muestra un cuadro de diálogo de confirmación y, si el usuario elige eliminar la factura,
            procede a eliminarla de la base de datos y recarga la tabla de facturas.

            Args:
                self: Parámetro opcional para permitir llamadas al método sin instancia específica.

            Returns:
                None

            """

        try:
            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Borrar")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            mbox.setText("¿Desea Borrar la factura?")
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)

            resultado = mbox.exec()

            if resultado == QtWidgets.QMessageBox.StandardButton.Yes:
                row = var.ui.tabFacturas.selectedItems()

                query = QtSql.QSqlQuery()
                query.prepare('delete from facturas where numfac = :numfac')
                query.bindValue(':numfac', int(row[0].text()))

                if query.exec():
                    # Después de eliminar, obtenemos la lista actualizada de facturas
                    query = QtSql.QSqlQuery()
                    query.prepare("select numfac, dnicliente from facturas")
                    registros = []
                    if query.exec():
                        while query.next():
                            row = [query.value(i) for i in range(query.record().count())]
                            registros.append(row)

                    # Llamamos a cargarTablaFacturas con la lista actualizada
                    Facturas.cargarTablaFacturas(registros)
                    viajes.Viajes.limpiarTablaViajes(self)

            elif resultado == QtWidgets.QMessageBox.StandardButton.No:
                mbox.close()

        except Exception as error:
            print('ERROR AL BORRAR LA FACTURA', error)

    @staticmethod
    def buscarFacturasCliente():
        """
        Busca las facturas asociadas a un cliente mediante su DNI.

        :return: Una lista de listas con la información de las facturas encontradas.
                 Cada lista interna contiene [numfac, dnicliente].

        """
        try:
            dni = var.ui.txtcifcliente.text()
            registroFacturas = []

            query = QtSql.QSqlQuery()
            query.prepare('SELECT numfac, dnicliente FROM facturas WHERE dnicliente = :dni')
            query.bindValue(':dni', dni)
            if (dni == ""):
                conexion.Conexion.show_warning("Campo vacio")

            elif query.exec():
                if query.next():
                    # Se encontraron facturas
                    while query.isValid():
                        numfac = query.value(0)
                        dnicliente = query.value(1)

                        registroFacturas.append([numfac, dnicliente])

                        query.next()

                    Facturas.cargarTablaFacturas(registroFacturas)
                    return registroFacturas

                else:
                    # No se encontraron facturas
                    msg = QtWidgets.QMessageBox()
                    msg.setModal(True)
                    msg.setWindowTitle('Aviso')
                    msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    msg.setText('No se encontraron facturas asociadas al DNI proporcionado.')
                    msg.exec()
                    return []

            else:
                print('Error al ejecutar la consulta:', query.lastError().text())

        except Exception as error:
            print('Error al buscar las facturas del cliente', error)












