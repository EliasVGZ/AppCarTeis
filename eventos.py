import os.path
import shutil
from datetime import datetime

import xlrd
from PyQt6 import QtWidgets, QtCore, QtSql

import conexionClientes
import drivers, clientes
import var, sys, locale, zipfile, shutil, conexion, xlwt

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
locale.setlocale(locale.LC_MONETARY, 'es_ES.UTF-8')


class Eventos():

    @staticmethod
    def salir():
        """
           Muestra la ventana de confirmación para salir de la aplicación.

           Este método estático muestra la ventana de confirmación para salir de la aplicación cuando se activa la opción
           correspondiente en la interfaz gráfica.

           Retorna:
               None

           """
        try:
            var.salir.show()

        except Exception as error:
            print(error, "en modulos eventos")

    @staticmethod
    def abrirCalendario(self):
        """
            Abre la ventana del calendario.

            Este método estático abre la ventana del calendario cuando se activa la opción correspondiente en la interfaz gráfica.

            Parámetros:
                self: Parámetro opcional, generalmente utilizado en métodos de clases.

            Retorna:
                None

            """
        try:
            var.calendar.show()
        except Exception as error:
            print("error en abrir calendario", error)

    @staticmethod
    def acercade():
        """
            Abre la ventana de Acerca de.

            Este método estático abre la ventana de Acerca de cuando se activa la opción correspondiente en la interfaz gráfica.

            Retorna:
                None

            """
        try:
            var.dlgacercade.show()
        except Exception as error:
            print("error abrir ventana acerca de", error)

    @staticmethod
    def cerraracercade():
        """
            Cierra la ventana de Acerca de.

            Este método estático cierra la ventana de Acerca de cuando se activa la opción correspondiente en la interfaz gráfica.

            Retorna:
                None

            """
        try:
            var.dlgacercade.hide()

        except Exception as error:
            print('error abrir ventana acerca de', error)

    @staticmethod
    def cerrarsalir():
        """
            Cierra la ventana de confirmación para salir.

            Este método estático cierra la ventana de confirmación para salir cuando se activa la opción correspondiente en la
            interfaz gráfica.

            Retorna:
                None

            """
        try:
            var.dlgsalir.hide()
        except Exception as error:
            print('error abrir ventana acerca de', error)

    @staticmethod
    def mostrarsalir(self, event):
        """
        Muestra la ventana de confirmación para salir.

        Este método estático muestra la ventana de confirmación para salir cuando se activa la opción correspondiente en la
        interfaz gráfica.

        Parámetros:
            self: Parámetro opcional, generalmente utilizado en métodos de clases.
            event: Evento asociado a la acción que activa la ventana.

        Retorna:
            None
        """
        try:
            var.dlgsalir.show()
        except Exception as error:
            print('error abrir ventana acerca de', error)

    @staticmethod
    def aceptar(self):
        """
        Cierra la aplicación.

        Este método estático cierra la aplicación cuando se activa la opción correspondiente en la interfaz gráfica.

        Parámetros:
            self: Parámetro opcional, generalmente utilizado en métodos de clases.

        Retorna:
            None
        """
        sys.exit()

    @staticmethod
    def cancelar():
        """
        Oculta el cuadro de diálogo de salir.

        Este método estático oculta el cuadro de diálogo de salir cuando se activa la opción correspondiente en la interfaz
        gráfica.

        Retorna:
            None
        """
        var.salir.hide()

    @staticmethod
    def cargarstatusbar(self):
        """
           Carga los elementos en la barra de estado de la interfaz de usuario.

           Este método estático es responsable de agregar dos etiquetas a la barra de estado:
           1. Una etiqueta que muestra la fecha actual en formato "Día - DD/MM/AAAA".
           2. Otra etiqueta que muestra la versión de la aplicación.

           Parameters:
           - self: Referencia a la instancia actual de la clase.

           Note:
           - Este método utiliza la clase `QtWidgets.QLabel` para crear etiquetas de texto.
           - La fecha se formatea utilizando la fecha y hora actuales en formato "Día - DD/MM/AAAA".
           - La versión de la aplicación se obtiene de la variable global `var.version`.
           - Las etiquetas se agregan a la barra de estado con alineaciones específicas.

           """

        try:
            fecha = datetime.now().strftime("%A  -  " + "%d/%m/%Y")
            fecha = fecha.capitalize()
            self.labelstatus = QtWidgets.QLabel(fecha, self)
            self.labelstatus.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
            var.ui.statusbar.addPermanentWidget(self.labelstatus, 1)

            self.labelstatusversion = QtWidgets.QLabel("Version: " + var.version, self)
            self.labelstatusversion.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
            var.ui.statusbar.addPermanentWidget(self.labelstatusversion, 0)
        except Exception as error:
            print('Error cargar el statusbar: ', error)

    def resizeTabDrivers(self):
        """
            Ajusta el tamaño de las columnas en la tabla de la interfaz de usuario.

            Este método ajusta el tamaño de las columnas en la tabla de controladores (tabDrivers) de la interfaz de usuario.
            Las columnas se ajustan de acuerdo con las siguientes reglas:
            - La primera, cuarta y quinta columna se ajustan al contenido.
            - La segunda y tercera columna se ajustan para ocupar todo el espacio disponible.

            Parameters:
            - self: Referencia a la instancia actual de la clase.

            Note:
            - Este método utiliza la clase `QtWidgets.QHeaderView` para ajustar el tamaño de las columnas.
            - Las columnas se ajustan según la sección de la cabecera de la tabla.

            """
        try:
            header = var.ui.tabDrivers.horizontalHeader()
            for i in range(5):
                if i == 0 or i == 4 or i == 3:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                elif i == 1 or i == 2:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)

        except Exception as error:
            print("error al dimensionar la tabla", error)

    def resizeTabFacturas(self):
        """
            Ajusta el tamaño de las columnas en la tabla de facturas de la interfaz de usuario.

            Este método ajusta el tamaño de las columnas en la tabla de facturas (tabFacturas) de la interfaz de usuario.
            Las columnas se ajustan de acuerdo con las siguientes reglas:
            - La primera columna se ajusta al contenido.
            - La segunda columna se ajusta para ocupar todo el espacio disponible.

            Parameters:
            - self: Referencia a la instancia actual de la clase.

            """
        try:
            header = var.ui.tabFacturas.horizontalHeader()
            for i in range(2):
                if i == 0:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                elif i == 1:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)

        except Exception as error:
            print("error al dimensionar la tabla facturas", error)

    def resizeTabClientes(self):
        """
            Ajusta el tamaño de las columnas en la tabla de clientes de la interfaz de usuario.

            Este método ajusta el tamaño de las columnas en la tabla de clientes (tabClientes) de la interfaz de usuario.
            Las columnas se ajustan de acuerdo con las siguientes reglas:
            - La primera y cuarta columna se ajustan al contenido.
            - La segunda y tercera columna se ajustan para ocupar todo el espacio disponible.

            Parameters:
            - self: Referencia a la instancia actual de la clase.

            Returns:
            - None

            """
        try:
            header = var.ui.tabClientes.horizontalHeader()
            for i in range(4):
                if i == 0 or i == 3:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                elif i == 1 or i == 2:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)

        except Exception as error:
            print("error al dimensionar la tabla", error)

    def formatCajaTexto(self=None):
        """
            Formatea el texto en varias cajas de texto de la interfaz de usuario.

            Este método realiza operaciones de formateo en diferentes cajas de texto de la interfaz de usuario:
            - La caja de texto 'txtApellido' convierte el texto a título (primera letra de cada palabra en mayúscula).
            - La caja de texto 'txtNombre' convierte el texto a título.
            - La caja de texto 'txtSalario' formatea el número como una cadena de texto en formato de moneda, según la configuración regional actual.
            - La caja de texto 'txtDni2' convierte el texto a título.
            - La caja de texto 'txt_razonSocial' convierte el texto a título.
            - La caja de texto 'txtDireccionCliente' convierte el texto a título.

            Parameters:
            - self: Referencia a la instancia actual de la clase. Puede ser nulo.

            Returns:
            - None

            """
        try:

            var.ui.txtApellido.setText(
                var.ui.txtApellido.text().title())  # Toma el texto del widget txtApellido, lo convierte a título (es decir, la primera letra de cada palabra en mayúscula)
            var.ui.txtNombre.setText(var.ui.txtNombre.text().title())
            var.ui.txtSalario.setText(str(locale.currency(float(
                var.ui.txtSalario.text()))))  # Formatea el número como una cadena de texto en formato de moneda según la configuración regional actual

            var.ui.txtDni2.setText(var.ui.txtDni2.text().title())
            var.ui.txt_razonSocial.setText(var.ui.txt_razonSocial.text().title())
            var.ui.txtDireccionCliente.setText(var.ui.txtDireccionCliente.text().title())

        except Exception as error:
            print("error poner letra capital en caja de texto", error)

    def crearBackUp(self):
        """
            Crea una copia de seguridad del archivo de la base de datos.

            Este método genera una copia de seguridad del archivo de la base de datos en formato ZIP.
            La copia de seguridad se guarda con un nombre que incluye la fecha y hora actual en el formato 'YYYY_MM_DD_HH_MM_SS'.
            Se utiliza un cuadro de diálogo para que el usuario seleccione la ubicación y el nombre del archivo de la copia de seguridad.

            Parameters:
            - self: Referencia a la instancia actual de la clase.

            Returns:
            - None

            """
        try:
            fecha = datetime.today()
            fecha = fecha.strftime('%Y_%m_%d_%H_%M_%S')  # formato año, mes, dia, hora, minuto, segundos
            copia = str(fecha + '_backup.zip')  # nombre del fichero
            directorio, filename = var.dlgabrir.getSaveFileName(None, 'Guardar Copia Seguridad', copia, '.zip')

            if var.dlgabrir.accept and filename:
                fichzip = zipfile.ZipFile(copia, 'w')
                fichzip.write(var.bbdd, os.path.basename(var.bbdd), zipfile.ZIP_DEFLATED)
                fichzip.close()
                shutil.move(str(copia), str(directorio))
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle('Aviso')
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText('Copia de Seguridad creada ')
                mbox.exec()
        except Exception as error:
            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle('Aviso')
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            mbox.setText('Error en Copia de Seguridad: ')
            mbox.exec()

    def restaurarBackUp(self):
        """
            Restaura una copia de seguridad previamente creada.

            Este método permite al usuario seleccionar un archivo ZIP que contiene una copia de seguridad de la base de datos.
            Luego, restaura la base de datos desde el archivo ZIP seleccionado.
            Después de la restauración, se actualiza la vista de controladores en la interfaz de usuario.

            Parameters:
            - self: Referencia a la instancia actual de la clase.

            Returns:
            - None

            """
        try:
            filename = var.dlgabrir.getOpenFileName(None, 'Restaurar Copia de Seguridad',
                                                    '', '*.zip;;All Files(*)')
            file = filename[0]
            if var.dlgabrir.accept and file:
                with zipfile.ZipFile(str(file), 'r') as bbdd:
                    bbdd.extractall(pwd=None)

                bbdd.close()
                conexion.Conexion.mostrarDrivers()

                msg = QtWidgets.QMessageBox()
                msg.setModal(True)
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText('Copia de Seguridad Restaurada ')
                msg.exec()

        except Exception as error:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle('Aviso')
            msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            msg.setText('Error en Restauracion Copia Seguridad ')
            msg.exec()

    def exportarDatosXls(self):
        """
            Exporta datos de conductores a un archivo XLS.

            Este método genera un archivo de hoja de cálculo XLS que contiene información sobre los conductores.
            Utiliza la biblioteca xlwt para crear el archivo y escribir los datos.
            La hoja de cálculo tiene columnas que representan diferentes atributos de los conductores.

            Parameters:
            - self: Referencia a la instancia actual de la clase.

            Returns:
            - None

            """
        try:
            fecha = datetime.today()
            fecha = fecha.strftime('%Y_%m_%d_%H_%M_%S')  # formato año, mes, dia, hora, minuto, segundos
            file = (str(fecha) + ' _Datos.xls')
            directorio, filename = var.dlgabrir.getSaveFileName(None, 'Exportar Datos en Fichero XLS', file, '.xls')

            if var.dlgabrir.accept and filename:
                wb = xlwt.Workbook()
                sheet1 = wb.add_sheet('Conductores')
                sheet1.write(0, 0, 'Codigo')  # el 0,0 es fila y columna
                sheet1.write(0, 1, 'DNI')
                sheet1.write(0, 2, 'Fecha Alta')
                sheet1.write(0, 3, 'Apellidos')
                sheet1.write(0, 4, 'Nombre')
                sheet1.write(0, 5, 'Dirección')
                sheet1.write(0, 6, 'Provincia')
                sheet1.write(0, 7, 'Municipio')
                sheet1.write(0, 8, 'Móvil')
                sheet1.write(0, 9, 'Salario')
                sheet1.write(0, 10, 'Carnet')
                sheet1.write(0, 11, 'Fecha baja')

                registros = conexion.Conexion.selectDriversTodos(self)

                for fila, registro in enumerate(registros, 1):
                    for i, valor in enumerate(
                            registro[:-1]):  # el :-1 es para que no te muestre el ultimo dato, en este caso fecha baja
                        sheet1.write(fila, i, str(valor))
                wb.save(directorio)
        except Exception as error:
            msg = QtWidgets.QMessageBox()
            msg.setModal(True)  # para que la ventana sea modal, que nadie pueda acceder a la ventana de atras
            msg.setWindowTitle('Aviso')
            msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            msg.setText('Exportacion datos correcta ')
            msg.exec()

    def exportarDatosClientesXls(self):
        """
            Exporta datos de clientes a un archivo XLS.

            Este método genera un archivo de hoja de cálculo XLS que contiene información sobre los clientes.
            Utiliza la biblioteca xlwt para crear el archivo y escribir los datos.
            La hoja de cálculo tiene columnas que representan diferentes atributos de los clientes.

            Parameters:
            - self: Referencia a la instancia actual de la clase.

            Returns:
            - None

            """
        try:
            fecha = datetime.today()
            fecha = fecha.strftime('%Y_%m_%d_%H_%M_%S')  # formato año, mes, dia, hora, minuto, segundos
            file = (str(fecha) + ' _DatosClientes.xls')
            directorio, filename = var.dlgabrir.getSaveFileName(None, 'Exportar Datos en Fichero XLS', file, '.xls')

            if var.dlgabrir.accept and filename:
                wb = xlwt.Workbook()
                sheet1 = wb.add_sheet('Clientes')
                sheet1.write(0, 0, 'Codigo')  # el 0,0 es fila y columna
                sheet1.write(0, 1, 'DNI')
                sheet1.write(0, 2, 'Fecha Alta')
                sheet1.write(0, 3, 'Razón Social')
                sheet1.write(0, 4, 'Dirección')
                sheet1.write(0, 5, 'Teléfono')
                sheet1.write(0, 6, 'Municipio')
                sheet1.write(0, 7, 'Localidad')

                registros = conexionClientes.ConexionCliente.selectClientesTodos(self)
                print("registro de exportar clientes: "+str(registros))

                for fila, registro in enumerate(registros, 1):
                    for i, valor in enumerate(registro[:-1]):  # el :-1 es para que no te muestre el ultimo dato, en este caso fecha baja
                        sheet1.write(fila, i, str(valor))
                wb.save(directorio)

                msg = QtWidgets.QMessageBox()
                msg.setModal(True)  # para que la ventana sea modal, que nadie pueda acceder a la ventana de atras
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText('Exportacion datos correcta ')
                msg.exec()

        except Exception as error:
            msg = QtWidgets.QMessageBox()
            msg.setModal(True)  # para que la ventana sea modal, que nadie pueda acceder a la ventana de atras
            msg.setWindowTitle('Aviso')
            msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            msg.setText('Error Exportar Datos en Hoja de Cálculos ' + str(error))
            msg.exec()


    def importardatosxls(self):
        """
            Importa datos desde un archivo XLS y guarda la información en la base de datos.

            Este método permite al usuario seleccionar un archivo XLS para importar datos.
            Luego, recorre las filas y columnas del archivo y realiza las siguientes acciones:
            - Convierte las fechas del formato interno de Excel a formato 'DD/MM/YYYY'.
            - Guarda los datos en la base de datos utilizando el método 'guardarClick' de la clase 'Conexion'.
            - Muestra mensajes de advertencia si hay DNIs incorrectos.

            Parameters:
            - self: Referencia a la instancia actual de la clase.

            Returns:
            - None

            """
        try:
            estado = 0
            filename, _ = var.dlgabrir.getOpenFileName(None, 'Importar datos',
                                                       '', '*.xls;;All Files (*)')
            if filename:
                file = filename
                documento = xlrd.open_workbook(file)
                datos = documento.sheet_by_index(0)
                filas = datos.nrows
                columnas = datos.ncols
                for i in range(filas):
                    if i == 0:
                        pass
                    else:
                        new = []
                        for j in range(columnas):
                            if j == 1:
                                dato = xlrd.xldate_as_datetime(datos.cell_value(i, j), documento.datemode)
                                dato = dato.strftime('%d/%m/%Y')
                                new.append(str(dato))
                            else:
                                new.append(str(datos.cell_value(i, j)))

                        if drivers.Drivers.validarDni(str(new[0])):
                            conexion.Conexion.guardarClick(new)
                            drivers.Drivers.limpiarPanel(self)
                        elif estado == 0:
                            estado = 1
                            msg = QtWidgets.QMessageBox()
                            msg.setModal(True)
                            msg.setWindowTitle('Aviso')
                            msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                            msg.setText('Hay DNI incorrectos')
                            msg.exec()
                var.ui.lblValidarDni.setText('')

                msg = QtWidgets.QMessageBox()
                msg.setModal(True)
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText('Importación de Datos Realizada')
                var.ui.lblValidarDni.setText('')
                msg.exec()

            conexion.Conexion.selectDrivers(1)

        except Exception as error:
            msg = QtWidgets.QMessageBox()
            msg.setModal(True)
            msg.setWindowTitle('Aviso')
            msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            msg.setText('Error', error)
            msg.exec()

    def importardatosclientesxls(self):
        """
            Importa datos de clientes desde un archivo XLS y guarda la información en la base de datos.

            Este método permite al usuario seleccionar un archivo XLS para importar datos de clientes.
            Luego, recorre las filas y columnas del archivo y realiza las siguientes acciones:
            - Convierte los valores numéricos a cadenas y evita la notación científica.
            - Guarda los datos en la base de datos utilizando el método 'guardarCliente' de la clase 'ConexionCliente'.
            - Muestra mensajes de advertencia si hay DNIs incorrectos.

            Parameters:
            - self: Referencia a la instancia actual de la clase.

            Returns:
            - None

            """
        try:
            estado = 0
            filename, _ = var.dlgabrir.getOpenFileName(None, 'Importar datos', '', '*.xls;;All Files (*)')
            if filename:
                file = filename
                documento = xlrd.open_workbook(file)
                datos = documento.sheet_by_index(0)
                filas = datos.nrows
                columnas = datos.ncols

                for i in range(1, filas):
                    new = []
                    for j in range(columnas):
                        cell_value = datos.cell_value(i, j)

                        if datos.cell_type(i, j) == xlrd.XL_CELL_DATE:
                            # Convertir fecha numérica a objeto de fecha y hora
                            date_value = xlrd.xldate_as_datetime(cell_value, documento.datemode)
                            new.append(date_value.strftime('%d/%m/%Y'))
                        elif isinstance(cell_value, float):
                            new.append(str("{:.0f}".format(cell_value)))
                        else:
                            new.append(str(cell_value))
                    print("New Data:", new)  # Agrega esta línea

                    if clientes.Clientes.validarDni(str(new[0])):
                        conexionClientes.ConexionCliente.guardarCliente(new)
                        clientes.Clientes.limpiarPanelCliente(self)

                var.ui.lblValidarDni_2.setText('')

                msg = QtWidgets.QMessageBox()
                msg.setModal(True)
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText('Importación de Datos Realizada')
                var.ui.lblValidarDni_2.setText('')
                msg.exec()

            conexionClientes.ConexionCliente.selectClientes(1)

        except Exception as error:
            msg = QtWidgets.QMessageBox()
            msg.setModal(True)
            msg.setWindowTitle('Aviso')
            msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            msg.setText(f'Error: {str(error)}')
            msg.exec()
