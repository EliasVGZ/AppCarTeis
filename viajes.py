from PyQt6.QtWidgets import QComboBox

import conexion
import facturas
import tarifas
import viajes
from windowaux import *
from PyQt6 import QtWidgets, QtSql, QtGui, QtCore
from datetime import date, datetime
import drivers
import eventos
import var


class Viajes():


    @staticmethod
    def limpiarPanelViaje(self):
        """
        Limpia el texto de los diferentes widgets en el módulo.

        :param self: Instancia del módulo.
        :type self: Viajes

        """
        try:
            listawidgets = [var.ui.cmbOrigenProvFac, var.ui.cmbOrigenLocFac,
                          var.ui.cmbDestinoProvFac, var.ui.cmbDestinoLocFac, var.ui.txt_kms, var.ui.lbl_idViaje]
            for i in listawidgets:
                if hasattr(i, 'setText'):
                    i.setText(None)
                elif isinstance(i, QComboBox):  # borrar combobox
                    i.setCurrentIndex(-1)

        except Exception as error:
            print("error limpiando panel de viajes", error)



    """ZONA CONEXION"""

    def selMuniviajeorigen(self=None):
        """
        Actualiza la lista de municipios en el combo box de origen basándose en la provincia seleccionada.

        :param self: Instancia de la clase (puede ser None si se llama de manera estática).
        :type self: Viajes

        """
        try:
            var.ui.cmbOrigenLocFac.clear()
            id = 0
            prov = var.ui.cmbOrigenProvFac.currentText()  #
            query = QtSql.QSqlQuery()

            query.prepare('select idprov from provincias where provincia = :prov')
            query.bindValue(':prov', prov)
            if query.exec():
                while query.next():  # LLENAR LAS PROVINCIAS MIENTRAS HAYA
                    id = query.value(0)
            query1 = QtSql.QSqlQuery()
            query1.prepare('select municipio from municipios where idprov = :id')
            query1.bindValue(':id', int(id))
            if query1.exec():
                var.ui.cmbOrigenLocFac.addItem('')
                while query1.next():
                    var.ui.cmbOrigenLocFac.addItem(query1.value(0))

        except Exception as error:
            print("error seleccion municipios  en origen", error)

    def selMuniviajedestino(self=None):
        """
                Actualiza la lista de municipios en el combo box de origen basándose en la provincia seleccionada.

                :param self: Instancia de la clase
                :type self: Viajes

        """

        try:
            var.ui.cmbDestinoLocFac.clear()
            id = 0
            prov = var.ui.cmbDestinoProvFac.currentText()  #
            query = QtSql.QSqlQuery()

            query.prepare('select idprov from provincias where provincia = :prov')
            query.bindValue(':prov', prov)
            if query.exec():
                while query.next():  # LLENAR LAS PROVINCIAS MIENTRAS HAYA
                    id = query.value(0)
            query1 = QtSql.QSqlQuery()
            query1.prepare('select municipio from municipios where idprov = :id')
            query1.bindValue(':id', int(id))
            if query1.exec():
                var.ui.cmbDestinoLocFac.addItem('')
                while query1.next():
                    var.ui.cmbDestinoLocFac.addItem(query1.value(0))

        except Exception as error:
            print("error seleccion municipios en destino ", error)

    #FUNCION PARA CONTROLAR LOS COMBOX, OPCIONES NACIONAL, PROVINCIAL Y LOCAL
    @staticmethod
    def datosViaje(self):

        """

        :return: Módulo que devuelve registro de un viaje
        :rtype: bytearray

        Este módulo carga los datos de los widgets del panel de gestión,
        selecciona la tarifa en funcion del tipo de viaje y devuelve
        un array con los datos

        """
        try:


            #tarifas = [0.20, 0.40, 0.8]
            datosViaje = [
                var.ui.cmbOrigenProvFac.currentText(),
                var.ui.cmbOrigenLocFac.currentText(),
                var.ui.cmbDestinoProvFac.currentText(),
                var.ui.cmbDestinoLocFac.currentText(),
                var.ui.txt_kms.text()
            ]

            if str(datosViaje[0]) == str(datosViaje[2]) and str(datosViaje[1]) == str(datosViaje[3]):
                var.ui.rbtLocal.setChecked(True)
                var.ui.txt_kms.setText("10")
                estado = 2
                tarifa_valor = tarifas.Tarifas.selectTarifa(estado)
                datosViaje.append(str(tarifa_valor))


            elif str(datosViaje[0]) == str(datosViaje[2]):
                var.ui.txt_kms.setText("")
                var.ui.rbtProvincial.setChecked(True)
                estado = 1
                tarifa_valor = tarifas.Tarifas.selectTarifa(estado)
                datosViaje.append(str(tarifa_valor))

                #datosViaje.append(str(tarifas[1]))

            else:
                var.ui.txt_kms.setText("")
                var.ui.rbtNacional.setChecked(True)
                estado = 0
                tarifa_valor = tarifas.Tarifas.selectTarifa(estado)
                datosViaje.append(str(tarifa_valor))

            return datosViaje

        except Exception as error:
            print("error datos viajes", error)

    @staticmethod
    def cargarLineaVenta():
        """
        Método para cargar una línea de venta.

        Parámetros:
            - Ninguno directamente. Utiliza los datos del viaje y el número de factura desde la interfaz gráfica.

        Acciones:
            - Obtiene los datos del viaje utilizando el método datosViaje de la clase Viajes.
            - Obtiene el número de factura desde la interfaz gráfica.
            - Si el valor del índice 5 de los datos del viaje es igual a 0.8, establece la variable km a 10.
              En caso contrario, obtiene el valor de los kilómetros desde la interfaz gráfica.
            - Agrega el número de factura y la variable km a la lista de datos del viaje.
            - Llama al método cargarLineaViaje de la clase Viajes para realizar la conexión con la base de datos.

        """
        try:


            viaje = Viajes.datosViaje(viajes.Viajes)
            factura = var.ui.lblNumFac.text()
            viaje.append(factura)


            if viaje[5] == str(0.8):
                km = 10
                viaje.append(km)

            if Viajes.cargarLineaViaje(viaje):
                return True
            else:
                return False

        except Exception as error:
            print("Error en cargarLineaVenta:", error)
            return False


    @staticmethod
    def cargarLineaViaje(registro):
        """

        Método para cargar un registro de viaje en la base de datos.

        Parámetros:
            - registro: Lista que contiene los datos del viaje a ser almacenados en la base de datos.
                        Debe contener los siguientes elementos en este orden: factura, origen, destino, tarifa, km.

        Acciones:
            - Imprime por pantalla el registro recibido.
            - Verifica si algún elemento en el registro está vacío o compuesto solo por espacios en blanco.
              Si es así, muestra un mensaje de advertencia indicando que faltan datos del viaje o número de factura.
            - Si todos los elementos del registro tienen datos válidos, prepara una consulta SQL para insertar el viaje en la base de datos.
            - Ejecuta la consulta y muestra un mensaje de éxito o error según el resultado.
            - Si la inserción es exitosa, actualiza la tabla de viajes llamando al método cargarTablaViajes de la clase Viajes.

        """
        try:

            print("Registro en cargar linea viaje :" + str(registro))##IMPRIMIR POR PANTALLA EL REGISTRO QUE ME LLEGA


            if any(not elemento for elemento in registro):
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle('AVISO')
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setText('Faltan datos del viaje o numero factura')
                mbox.exec()

            else:

                query = QtSql.QSqlQuery()
                query.prepare('insert into viajes(factura, origen, destino, tarifa, km)'
                              'VALUES (:factura, :origen, :destino, :tarifa, :km)')
                query.bindValue(':factura', str(registro[6]))
                query.bindValue(':origen', str(registro[1]))
                query.bindValue(':destino', str(registro[3]))
                query.bindValue(':tarifa', str(registro[5]))
                query.bindValue(':km', str(registro[4]))

                if query.exec():
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle('GUARDADO')
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setText('Viaje grabado en la base de datos')
                    mbox.exec()
                    Viajes.cargarTablaViajes(self=None)
                    conexion.Conexion.cargarFacturas(self=None)
                    Viajes.limpiarPanelViaje(self=None)
                else:
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle(':(')
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    mbox.setText('Error al grabar el viaje en la base de datos')
                    mbox.exec()


        except Exception as error:
            print("error cargar linea viaje", error)


    def cargarTablaViajes(self):
        """

        Método para cargar los datos de viajes en la tabla de la interfaz gráfica.

        Parámetros:
            - Ninguno directamente. Utiliza el número de factura desde la interfaz gráfica.

        Acciones:
            - Obtiene los datos de viajes asociados al número de factura desde la clase Viajes.
            - Itera sobre los registros obtenidos y los muestra en la tabla de viajes de la interfaz gráfica.
            - Calcula el total para cada registro y lo muestra en la columna correspondiente.
            - Alinea el texto en las celdas de la tabla y agrega un botón de eliminación para cada registro.
            - Calcula el subtotal, el IVA y el total de los viajes y los muestra en etiquetas correspondientes.

        """
        try:
            var.ui.actionlimpiarPanel.triggered.connect(Viajes.limpiarPanelViaje)
            datos = Viajes.viajesFactura(var.ui.lblNumFac.text())
            print("print DATOS PARA VER QUE LLEGA A LA TABLA:-->> "+str(datos))
            index = 0
            subtotal = 0.0

            # Verificar si hay datos antes de realizar acciones en la tabla
            if datos:
                for registro in datos:
                    var.ui.tabViajes.setRowCount(index + 1)  # crea una fila
                    var.ui.tabViajes.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                    var.ui.tabViajes.setItem(index, 1, QtWidgets.QTableWidgetItem(str(registro[2])))
                    var.ui.tabViajes.setItem(index, 2, QtWidgets.QTableWidgetItem(str(registro[3])))
                    var.ui.tabViajes.setItem(index, 3, QtWidgets.QTableWidgetItem(str(registro[4])))
                    var.ui.tabViajes.setItem(index, 4, QtWidgets.QTableWidgetItem(str(registro[5])))

                    valor_pos4 = float(registro[4])
                    valor_pos5 = float(registro[5])
                    total = valor_pos4 * valor_pos5
                    total_str = "{:.2f}".format(total)
                    var.ui.tabViajes.setItem(index, 5, QtWidgets.QTableWidgetItem(str(total_str) + ' €'))

                    # Alinear el texto en las celdas de la tabla
                    for col in range(6):
                        var.ui.tabViajes.item(index, col).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                    btn_borrar = QtWidgets.QPushButton()
                    btn_borrar.setFixedSize(30, 28)
                    btn_borrar.setIcon(QtGui.QIcon('./img/basura.png'))
                    var.ui.tabViajes.horizontalHeader().setSectionResizeMode(6,QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

                    var.ui.tabViajes.setColumnWidth(6, 50)
                    var.ui.tabViajes.setCellWidget(index, 6, btn_borrar)
                    btn_borrar.clicked.connect(Viajes.borrarviaje)
                    # Sumar el subtotal
                    subtotal += total
                    index += 1

                iva_porc = 0.21

                descuento_text = var.ui.txt_descuento.text()

                # Verificar si hay descuento ingresado
                if descuento_text:
                    descuento = float(descuento_text)
                else:
                    descuento = 0.0

                # Calcular el subtotal después de aplicar el descuento
                descuento_str = (descuento * subtotal) / 100
                subtotal_descuento = subtotal - descuento_str

                iva = subtotal_descuento * iva_porc
                total_iva = subtotal_descuento + iva

                # Asignar los valores calculados a las etiquetas después del bucle
                var.ui.lbl_subTotal.setText("{:.2f}".format(subtotal_descuento) + " \u20AC")
                var.ui.lbl_iva.setText("{:.2f}".format(iva) + " \u20AC")
                var.ui.lbl_total.setText("{:.2f}".format(total_iva) + " \u20AC")
                var.ui.lbl_descuento.setText("{:.2f}".format(descuento_str) + " \u20AC")



            else:
                # Si no hay datos de viajes, limpiar la tabla y actualizar las etiquetas a cero
                var.ui.tabViajes.setRowCount(0)
                var.ui.lbl_subTotal.setText("0.00 \u20AC")
                var.ui.lbl_iva.setText("0.00 \u20AC")
                var.ui.lbl_total.setText("0.00 \u20AC")

        except Exception as error:
            print("error cargar TABLA VIAJES", error)

    def limpiarTablaViajes(self):
        """

        Método para limpiar la tabla de viajes en la interfaz gráfica.

        """
        var.ui.tabViajes.setRowCount(0)  # Elimina todas las filas de la tabla
        var.ui.lbl_subTotal.setText("0.00 \u20AC")
        var.ui.lbl_iva.setText("0.00 \u20AC")
        var.ui.lbl_total.setText("0.00 \u20AC")


    def viajesFactura(dato):
        """

        Método para obtener información sobre los viajes asociados a un número de factura.

        :return: - Una lista de listas, donde cada lista representa un registro de viaje.
                   Cada registro contiene los datos de un viaje almacenados en la base de datos.
        :rtype: - dato: Número de factura del cual se desea obtener información

        """
        try:
            valores = []
            query = QtSql.QSqlQuery()
            query.prepare("select * from viajes where factura = :dato")
            query.bindValue(':dato', int(dato))
            if query.exec():
                while query.next():
                    row = [query.value(i) for i in range(query.record().count())]  # funcion lambda
                    valores.append(row)
            #print("Valores de viajesfactura22222: "+str(valores))
            return valores

        except Exception as error:
            print("ERROR CARGAR viaje a la vista", error)




    def cargaViaje(self):
        """

        Método para cargar los datos de un viaje al hacer clic en una fila de la tabla de viajes.

        Acciones:
            - Limpia el panel de información de viaje llamando al método limpiarPanelViaje.
            - Obtiene la fila seleccionada en la tabla de viajes.
            - Llama al método cargarDatosViaje para mostrar los datos en los ComboBox correspondientes.

        """
        try:
            #Viajes.limpiarPanelViaje(self)

            row = var.ui.tabViajes.selectedItems()
            fila = [dato.text() for dato in row]


            Viajes.cargarDatosViaje(fila)

        except Exception as error:
            print("Error al cargar los datos DE UN VIAJE EN CARGAVIAJE ", error)

    ##METODO para recoger todos los datos de un viaje

    def oneViaje(codigo):
        """
        Método para obtener información de un viaje específico identificado por su código.

        :param codigo: Código del viaje del cual se desea obtener información.
        :return: Una lista que contiene los datos del viaje: [idviajes, factura, origen, destino, tarifa, km].
        :rtype: list

        Acciones:
            - Crea una lista vacía llamada 'registro' para almacenar los datos del viaje.
            - Prepara una consulta SQL para seleccionar los campos específicos de la tabla 'viajes'
              donde el ID del viaje sea igual al código proporcionado.
            - Ejecuta la consulta y, si tiene éxito, obtiene los datos del primer registro y los agrega a la lista 'registro'.
            - Retorna la lista 'registro' que contiene la información del viaje.

        """
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT idviajes, factura, origen, destino, tarifa, km  FROM viajes WHERE idviajes = :numfac")
            query.bindValue(":numfac", str(codigo))

            if query.exec():
                if query.next():
                    for i in range(5):
                        registro.append(str(query.value(i)))


            return registro

        except Exception as error:
            print("Error en fichero conexion datos de UN VIAJE: ", error)

    def cargarDatosViaje(fila):

        """
                Método para cargar los datos de un viaje en los widgets de la interfaz gráfica.

                :param fila: Lista que contiene los datos del viaje actual [origen, destino, tarifa, km].
                :type fila: list

                Acciones:
                    - Imprime por consola los datos del viaje actual.
                    - Obtiene las localidades y provincias asociadas a los datos del viaje.
                    - Itera sobre los ComboBox y asigna las provincias y localidades a cada uno.
                    - Asigna el valor de los kilómetros al campo de texto correspondiente.
                    - Itera sobre los RadioButton y selecciona el RadioButton correspondiente a la tarifa del viaje.

        """

        try:
            print("Datos del viaje actual:", fila)

            localidades = [str(fila[1]), str(fila[2])]
            provincias = [Viajes.obtenerNombreProvincia(Viajes.obtenerIdProvincia(localidad)) for localidad in
                          localidades]
            tarifa = float(fila[3])
            kms = str(fila[4])
            idViaje = str(fila[0])

            for cmbProv, cmbLoc, provincia, localidad in zip(
                    [var.ui.cmbOrigenProvFac, var.ui.cmbDestinoProvFac],
                    [var.ui.cmbOrigenLocFac, var.ui.cmbDestinoLocFac],
                    provincias,
                    localidades
            ):

                cmbProv.addItem(provincia)
                cmbProv.setCurrentText(provincia)


                cmbLoc.addItem(localidad)
                cmbLoc.setCurrentText(localidad)

            var.ui.txt_kms.setText(kms)
            var.ui.lbl_idViaje.setText(idViaje)

            for rbt, tarifa_valor in zip(
                    [var.ui.rbtNacional, var.ui.rbtProvincial, var.ui.rbtLocal],
                    [0.2, 0.4, 0.8]
            ):
                rbt.setChecked(tarifa == tarifa_valor)

        except Exception as error:
            print("Error al cargar los datos de un viaje en cargarDatosViaje ", error)



    #TODO METODO PARA CARGAR LOS DATOS DEL VIAJE PERO SIN FOR, ENTENDIBLE PERO MAS EXTENSO

    # def cargarDatosViaje(fila):
    #     try:
    #         print("Datos del viaje actual:", fila)
    #
    #         localidad_origen = str(fila[1])
    #         localidad_destino = str(fila[2])
    #
    #         id_provincia_origen = Viajes.obtenerIdProvincia(localidad_origen)
    #         id_provincia_destino = Viajes.obtenerIdProvincia(localidad_destino)
    #
    #         provincia_origen = Viajes.obtenerNombreProvincia(id_provincia_origen)
    #         provincia_destino = Viajes.obtenerNombreProvincia(id_provincia_destino)
    #
    #         var.ui.cmbOrigenProvFac.clear()
    #         var.ui.cmbOrigenProvFac.addItem(provincia_origen)
    #         var.ui.cmbOrigenProvFac.setCurrentText(provincia_origen)
    #
    #         var.ui.cmbDestinoProvFac.clear()
    #         var.ui.cmbDestinoProvFac.addItem(provincia_destino)
    #         var.ui.cmbDestinoProvFac.setCurrentText(provincia_destino)
    #
    #         var.ui.cmbOrigenLocFac.clear()
    #         var.ui.cmbOrigenLocFac.addItem(localidad_origen)
    #         var.ui.cmbOrigenLocFac.setCurrentText(localidad_origen)
    #
    #         var.ui.cmbDestinoLocFac.clear()
    #         var.ui.cmbDestinoLocFac.addItem(localidad_destino)
    #         var.ui.cmbDestinoLocFac.setCurrentText(localidad_destino)
    #
    #         kms = str(fila[4])
    #         var.ui.txt_kms.setText(kms)
    #
    #         tarifa = float(fila[3])
    #
    #         # Marcar el RadioButton según el valor de la tarifa
    #         if tarifa == 0.2:
    #             var.ui.rbtNacional.setChecked(True)
    #         elif tarifa == 0.4:
    #             var.ui.rbtProvincial.setChecked(True)
    #         elif tarifa == 0.8:
    #             var.ui.rbtLocal.setChecked(True)
    #
    #     except Exception as error:
    #         print("Error al cargar los datos de un viaje en cargarDatosViaje ", error)

    def obtenerIdProvincia(localidad):
        """
            Método para obtener el ID de la provincia asociado a una localidad.

            :param localidad: Nombre de la localidad para la cual se desea obtener el ID de la provincia.
            :type localidad: str
            :return: El ID de la provincia asociado a la localidad.
            :rtype: int or None

            Acciones:
                - Prepara una consulta SQL para seleccionar el ID de la provincia de la tabla 'municipios'
                  donde el nombre de la localidad sea igual al proporcionado.
                - Ejecuta la consulta y, si tiene éxito, obtiene el resultado y lo retorna como un entero.
                - Si no se encuentra un ID de provincia, imprime un mensaje indicando la falta de información y retorna None.

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT idprov FROM municipios WHERE municipio = :localidad")
            query.bindValue(":localidad", localidad)

            if query.exec() and query.next():
                resultado = query.value(0)

                return resultado
            else:
                print("No se encontró un ID de provincia para la localidad {}".format(localidad))
                return None

        except Exception as error:
            print("Error al obtener el ID de la provincia: ", error)
            return None

    def obtenerNombreProvincia(id_provincia):
        """
            Método para obtener el nombre de la provincia asociado a un ID de provincia.

            :param id_provincia: ID de la provincia para el cual se desea obtener el nombre.
            :type id_provincia: int
            :return: El nombre de la provincia asociado al ID proporcionado.
            :rtype: str or None

            Acciones:
                - Prepara una consulta SQL para seleccionar el nombre de la provincia de la tabla 'provincias'
                  donde el ID de la provincia sea igual al proporcionado.
                - Ejecuta la consulta y, si tiene éxito, obtiene el resultado y lo retorna como una cadena.
                - Si no se encuentra un nombre de provincia, retorna None.

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT provincia FROM provincias WHERE idprov = :id_provincia")
            query.bindValue(":id_provincia", id_provincia)

            if query.exec() and query.next():
                return query.value(0)
            else:
                return None

        except Exception as error:
            print("Error al obtener el nombre de la provincia: ", error)
            return None

    @staticmethod
    def borrarviaje(self):
        """

        Método estático para solicitar confirmación y borrar un viaje seleccionado.

        :param self: Referencia a la instancia de la clase.
        :type self: TuClase or None

        Acciones:
            - Muestra un cuadro de diálogo de advertencia preguntando al usuario si desea borrar el viaje.
            - Si el usuario elige 'Sí', obtiene la fila seleccionada en la tabla de viajes y prepara una consulta SQL para eliminar el viaje.
            - Ejecuta la consulta y actualiza la tabla de viajes llamando al método cargarTablaViajes de la clase Viajes.

        """
        try:
            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Borrar")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            mbox.setText("¿Desea Borrar el viaje?")
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)

            resultado = mbox.exec()

            if resultado == QtWidgets.QMessageBox.StandardButton.Yes:
                row = var.ui.tabViajes.selectedItems()

                query = QtSql.QSqlQuery()
                query.prepare('delete from viajes where idviajes = :id')

                query.bindValue(':id', int(row[0].text()))

                if query.exec():
                    query.next()
                Viajes.cargarTablaViajes(self=None)

            elif resultado == QtWidgets.QMessageBox.StandardButton.No:
                mbox.close()

        except Exception as error:
            print('error al borrar viaje', error)


    #TODO METODO PARA BUSCAR UN VIAJE AL SELECCIONARLO EN LA TABLA
    def buscarViajeTabla(codigo):
        """
            Método para buscar un viaje en la tabla de viajes al seleccionarlo.

            :param codigo: Código del viaje que se desea buscar en la tabla.
            :type codigo: int or str

            Acciones:
                - Itera sobre las filas de la tabla de viajes.
                - Compara el valor de la primera celda (columna de códigos) con el código proporcionado.
                - Si encuentra una coincidencia, selecciona la fila correspondiente y realiza un desplazamiento para mostrarla.
                - Imprime un mensaje indicando la fila encontrada.

        """
        try:
            tabla = var.ui.tabViajes
            for fila in range(tabla.rowCount()):
                item = tabla.item(fila, 0)
                valorCelda = item.text()
                if valorCelda == int(codigo):
                    tabla.selectRow(fila)
                    tabla.scrollToItem(item)
                    print("Fila encontrada:", fila)
        except Exception as error:
            print('No se ha podido seleccionar al cliente en la tabla', error)

    def modificarViaje(self):
        """
        Método para modificar un viaje con los datos proporcionados por el usuario.

        Acciones:
            - Obtiene los valores de origen, destino y kilómetros desde los ComboBox y el campo de texto correspondiente.
            - Llama al método modificarViajeConexion de la clase Viajes para realizar la modificación en la base de datos.

        """
        try:
            tarifas = [0.20, 0.40, 0.8]

            viajes = [var.ui.lbl_idViaje, var.ui.cmbOrigenProvFac, var.ui.cmbDestinoProvFac, var.ui.cmbOrigenLocFac,
                      var.ui.cmbDestinoLocFac, var.ui.txt_kms]
            modificarViaje = []

            for i in range(6):  # Ajusta el rango para incluir todos los elementos
                if isinstance(viajes[i], QtWidgets.QComboBox):
                    modificarViaje.append(viajes[i].currentText())
                else:
                    modificarViaje.append(viajes[i].text())

            # Verificar si hay algún campo en blanco
            if any(not campo.strip() for campo in modificarViaje):
                conexion.Conexion.show_warning("Todos los campos deben estar llenos.")
                return  # Salir del método si hay campos en blanco

            if str(modificarViaje[0] == str(modificarViaje[1])):
                if str(modificarViaje[2]) == str(modificarViaje[3]):
                    var.ui.rbtLocal.setChecked(True)
                    modificarViaje.append(str(tarifas[2]))
                else:
                    var.ui.rbtProvincial.setChecked(True)
                    modificarViaje.append(str(tarifas[1]))
            else:
                var.ui.rbtNacional.setChecked(True)

            Viajes.modificarViajeConexion(modificarViaje)

        except Exception as error:
            print("Error al modificar el viaje", error)

    def modificarViajeConexion(modificarViaje):
        """
            Función para modificar un viaje en la base de datos con los datos proporcionados.

            Parámetros:
                - modificarViaje: Lista que contiene los datos del viaje a modificar [idviajes, origen, destino, tarifa, km].
                  Se espera que idviajes sea una cadena y los demás elementos sean cadenas o flotantes convertidos a cadenas.

            Acciones:
                - Imprime por consola los datos del viaje a modificar.
                - Prepara una consulta SQL para actualizar la información del viaje en la tabla 'viajes' usando los valores proporcionados.
                - Ejecuta la consulta y muestra un mensaje de aviso o advertencia en función del resultado.

        """
        try:
            print("MODIFICAR VIAJE -> " + str(modificarViaje))

            query = QtSql.QSqlQuery()
            query.prepare(
                'UPDATE viajes SET origen = :origen, destino = :destino, tarifa = :tarifa, km = :km where idviajes = :idviajes')

            query.bindValue(':idviajes', modificarViaje[0])
            query.bindValue(':origen', modificarViaje[3])
            query.bindValue(':destino', modificarViaje[4])
            query.bindValue(':tarifa', modificarViaje[6])
            query.bindValue(':km', modificarViaje[5])

            if query.exec():  # Cambiado a exec_() para reflejar la ejecución de la consulta
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle('Aviso')
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText('Viaje modificado')
                mbox.exec()
                Viajes.cargarTablaViajes(modificarViaje)
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle('Aviso')
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setText(query.lastError().text())
                mbox.exec()

        except Exception as error:
            print("Error al modificar el viaje en conexion", error)



















