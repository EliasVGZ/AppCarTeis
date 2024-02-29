
from calendar import Calendar

import facturas
import viajes
from windowaux import *
from PyQt6 import QtWidgets, QtSql, QtGui, QtCore
from datetime import date, datetime
import drivers
import eventos
import var


class Conexion():

    

    def conexion(self=None):
        """
    Método para establecer la conexión con la base de datos SQLite.

    Este método utiliza la clase QSqlDatabase para establecer la conexión con una base de datos SQLite
    que se encuentra en el archivo 'bbdd.sqlite'. Si la conexión es exitosa, imprime un mensaje indicando
    que la base de datos está conectada.

    Args:
        self: Parámetro opcional para permitir llamadas al método sin instancia específica.

    Returns:
        bool: True si la conexión se estableció correctamente, False si hubo un error en la conexión.

    """
        var.bbdd = 'bbdd.sqlite'
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(var.bbdd)
        if not db.open():
            print("error de conexión")
            return False
        else:
            print("base de datos conectada")
            return True

    # @staticmethod
    # def cargaprov(self=None):
    #     try:
    #         var.ui.cmbProvincia.clear()  # LIMPIA Y VUELVE A RECARGAR
    #
    #         query = QtSql.QSqlQuery()
    #         query.prepare('select provincia from provincias')
    #         var.ui.cmbProvincia.addItem(' ')
    #
    #         if query.exec():
    #             var.ui.cmbProvincia.addItem(' ')
    #             while query.next():  # LLENAR LAS PROVINCIAS MIENTRAS HAYA
    #                 var.ui.cmbProvincia.addItem(query.value(0))
    #     except Exception as error:
    #         print("error al carga provincias", error)

    def cargar_provincias(combo_box):
        """
            Método para cargar las provincias desde la base de datos en un ComboBox.

            Este método recibe un objeto ComboBox como argumento, limpia su contenido y luego carga las provincias
            obtenidas de la base de datos en el ComboBox.

            Args:
                combo_box: Objeto ComboBox en el cual se cargarán las provincias.

            Returns:
                None

            """
        try:
            # Limpiar y volver a cargar
            combo_box.clear()

            query = QtSql.QSqlQuery()
            query.prepare('SELECT provincia FROM provincias')

            if query.exec():
                combo_box.addItem(' ')
                while query.next():
                    combo_box.addItem(query.value(0))
        except Exception as error:
            print("Error al cargar provincias:", error)

    def selMuni(self=None):
        """

            Método para seleccionar y cargar los municipios correspondientes a una provincia en un ComboBox.

            Este método obtiene la provincia seleccionada desde un ComboBox, busca el identificador (id) asociado a esa provincia
            en la base de datos y luego utiliza ese id para cargar los municipios correspondientes en otro ComboBox.

            Args:
                self: Parámetro opcional para permitir llamadas al método sin instancia específica.

            Returns:
                None

            """
        try:
            var.ui.cmbLocalidad.clear()
            id = 0
            prov = var.ui.cmbProvincia.currentText()  #
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
                var.ui.cmbLocalidad.addItem('')
                while query1.next():
                    var.ui.cmbLocalidad.addItem(query1.value(0))

        except Exception as error:
            print("error seleccion municipios ", error)

    @staticmethod
    def guardarClick(newDriver):
        """
            Método estático para guardar un nuevo registro de driver en la base de datos.

            Este método recibe una lista con los datos del nuevo driver, valida que los campos esenciales no estén vacíos,
            y luego realiza una inserción en la tabla 'drivers' de la base de datos.

            Args:
                newDriver (list): Lista con los datos del nuevo driver, en el siguiente orden:
                    [DNI, Fecha de alta, Apellido, Nombre, Dirección, Provincia, Municipio, Móvil, Salario, Carnet]

            Returns:
                bool: True si la inserción fue exitosa, False si hubo algún error.

            """
        try:
            dni = str(newDriver[0])
            if (dni.strip() == "" or newDriver[2].strip() == "" or newDriver[3].strip() == "" or newDriver[
                7].strip() == ""):
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle('Aviso')
                mbox.setWindowIcon(QtGui.QIcon('./IMG/aviso.jpg'))
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mensaje = ('Faltan datos:\n Dni, Apellido, Nombre, Fecha de alta o Movil no pueden estar vacíos')
                mbox.setText(mensaje)
                mbox.exec()

            else:
                query = QtSql.QSqlQuery()
                query.prepare(
                    'insert into drivers (dnidriver, altadriver, apeldriver, nombredriver, '
                    'direcciondriver, provdriver, munidriver, movildriver, salario, carnet) '
                    'VALUES (:dni, :alta, :apel, :nombre, :direccion, :provincia, :municipio, '
                    ':movil, :salario, :carnet)')

                query.bindValue(':dni', dni)
                query.bindValue(':alta', str(newDriver[1]))
                query.bindValue(':apel', str(newDriver[2]))
                query.bindValue(':nombre', str(newDriver[3]))
                query.bindValue(':direccion', str(newDriver[4]))
                query.bindValue(':provincia', str(newDriver[5]))
                query.bindValue(':municipio', str(newDriver[6]))
                query.bindValue(':movil', str(newDriver[7]))
                query.bindValue(':salario', str(newDriver[8]))
                query.bindValue(':carnet', str(newDriver[9]))

            if query.exec():
                return True
            else:
                return False
            Conexion.mostrarDrivers(self=None)

        except Exception as error:
            print("Error guardando los drivers", error)

    def mostrarDrivers(self):
        """
            Método para mostrar los drivers en la interfaz gráfica, según el estado seleccionado.

            Este método verifica si el botón de radio para mostrar solo drivers de alta está seleccionado.
            En ese caso, llama a la función 'selectDrivers' de la clase 'Conexion' para obtener los drivers de alta.
            De lo contrario, realiza una consulta para obtener todos los drivers de la base de datos y los muestra en la tabla.

            Args:
                self: Parámetro opcional para permitir llamadas al método sin instancia específica.

            """
        try:
            registros = []
            if var.ui.rbtAlta.isChecked():
                estado = 1
                Conexion.selectDrivers(estado)
            else:
                query1 = QtSql.QSqlQuery()
                query1.prepare("select codigo, apeldriver, nombredriver, movildriver, "
                               "carnet, bajadriver from drivers")
                if query1.exec():
                    while query1.next():
                        row = [query1.value(i) for i in range(query1.record().count())]  # funcion lambda
                        registros.append(row)
            # SI ESTAN TODOS DE BAJA DEBE MOSTRAR LA TABLA DE ALTA VACIA
            if registros:
                drivers.Drivers.cargarTablaDriver(registros)
            else:
                var.ui.tabDrivers.setRowCount(0)

        except Exception as error:
            print("error mostrar resultados", error)

    def oneDriver(codigo):
        """
            Método para obtener los datos de un driver específico mediante su código.

            Este método realiza una consulta a la base de datos para obtener todos los datos asociados a un driver
            identificado por su código.

            Args:
                codigo (int): Código único del driver que se desea obtener.

            Returns:
                list: Lista con los datos del driver obtenidos de la base de datos.
                      El orden de los elementos en la lista es: [DNI, Fecha de alta, Apellido, Nombre, Dirección,
                      Provincia, Municipio, Móvil, Salario, Carnet, Fecha de baja, Estado]

            """
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM drivers WHERE codigo = :codigo")
            query.bindValue(":codigo", int(codigo))
            if query.exec():
                while query.next():
                    for i in range(12):
                        registro.append(str(query.value(i)))
            return registro
        except Exception as error:
            print("Error en fichero conexion datos de 1 driver: ", error)

    def codigoDriver(dni):
        """
            Método para obtener el código de un driver a partir de su DNI y realizar acciones adicionales.

            Este método realiza una consulta a la base de datos para obtener el código de un driver dado su DNI.
            Si encuentra el código, llama a la función 'buscarDriverTabla' de la clase 'Drivers' para resaltar la fila
            correspondiente en la tabla de drivers y, a continuación, utiliza el código para obtener y devolver el registro
            completo del driver mediante la función 'oneDriver' de la clase 'Conexion'. Si no se encuentra el conductor,
            se muestra un aviso en la interfaz gráfica y se devuelve None.

            Args:
                dni (str): DNI del driver que se desea buscar.

            Returns:
                list or None: Lista con los datos del driver si se encuentra, o None si no se encuentra.

            """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT codigo FROM drivers WHERE dnidriver = :dnidri")
            query.bindValue(":dnidri", str(dni))

            if query.exec():
                codigo = None
                while query.next():
                    codigo = query.value(0)
                    drivers.Drivers.buscarDriverTabla(codigo)

                if codigo is not None:
                    registro = Conexion.oneDriver(codigo)
                    return registro
                else:
                    # Si no se encuentra el conductor, mostrar un aviso
                    var.ui.lblValidarDni.setStyleSheet('color:red;')
                    var.ui.lblValidarDni.setText('X')
                    var.ui.txtDni.clear()  # Limpia el campo de texto
                    var.ui.txtDni.setFocus()  # Mantiene el foco en el campo de texto
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle('Aviso')
                    mbox.setWindowIcon(QtGui.QIcon('./IMG/aviso.jpg'))  # Ruta del archivo del icono
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    mensaje = ('          DNI no existe          ')
                    mbox.setText(mensaje)
                    mbox.exec()
                    return None

        except Exception as error:
            print("Error en búsqueda de código de un conductor: ", error)
            return None

    def modifDriver(modificarNewDriver):
        """
            Método para modificar los datos de un conductor en la base de datos.

            Este método compara los nuevos datos del conductor con los existentes y ofrece opciones para cambiar la fecha
            de baja o eliminarla. Si no hay cambios, permite cambiar la fecha de baja o cancelar la operación. Si hay cambios,
            actualiza los datos del conductor en la base de datos.

            """
        try:
            registro = Conexion.oneDriver(int(modificarNewDriver[0]))
            if modificarNewDriver == registro[:-1]:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText('No hay datos que modificar. Desea cambiar la fecha o eliminar fecha de baja?')
                msg.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No |
                    QtWidgets.QMessageBox.StandardButton.Cancel)
                msg.button(QtWidgets.QMessageBox.StandardButton.Yes).setText("Alta")
                msg.button(QtWidgets.QMessageBox.StandardButton.No).setText("Modificar")
                msg.button(QtWidgets.QMessageBox.StandardButton.Cancel).setText('Cancelar')
                opcion = msg.exec()
                if opcion == QtWidgets.QMessageBox.StandardButton.Yes:
                    if registro[11] != '':
                        query1 = QtSql.QSqlQuery()
                        query1.prepare('update drivers set bajadriver = NULL where '
                                       ' dnidriver = :dni')
                        query1.bindValue(':dni', str(modificarNewDriver[1]))
                        if query1.exec():
                            msg = QtWidgets.QMessageBox()
                            msg.setWindowTitle('Aviso')
                            msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                            msg.setText('Datos Conductor Modificados')
                            msg.exec()
                            Conexion.selectDrivers(2)
                    else:
                        msg = QtWidgets.QMessageBox()
                        msg.setWindowTitle('Aviso')
                        msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                        msg.setText('El conductor está en alta. Nada que modificar')
                        msg.exec()
                        Conexion.selectDrivers(1)
                elif opcion == QtWidgets.QMessageBox.StandardButton.No:
                    var.calendar2 = Calendar()
                    var.calendar2.show()
                    var.calendar2.selectionChanged.connect(Conexion.showSelectedDate)

                    data = Conexion.showSelectedDate()
                    data = data.toString("dd/MM/yyyy")


                    if registro[11] != '':
                        query1 = QtSql.QSqlQuery()
                        query1.prepare('update drivers set bajadriver = :data where '
                                       ' dnidriver = :dni')
                        query1.bindValue(':data', str(data))
                        query1.bindValue(':dni', str(modificarNewDriver[1]))
                        if query1.exec():
                            msg = QtWidgets.QMessageBox()
                            msg.setWindowTitle('Aviso')
                            msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                            msg.setText('Baja Modificada. Nueva Fecha Baja')
                            msg.exec()
                        Conexion.selectDrivers(0)
                    else:
                        msg = QtWidgets.QMessageBox()
                        msg.setWindowTitle('Aviso')
                        msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                        msg.setText('El conductor está en alta. Nada que modificar')
                        msg.exec()
                        Conexion.selectDrivers(1)
                elif opcion == QtWidgets.QMessageBox.StandardButton.Cancel:
                    pass
            else:

                query = QtSql.QSqlQuery()
                query.prepare(
                    'update drivers set dnidriver = :dni, altadriver = :alta, apeldriver = :apel, nombredriver = :nombre, direcciondriver = :direccion, '
                    'provdriver = :provincia, munidriver = :municipio, movildriver = :movil, salario = :salario, carnet = :carnet where codigo = :codigo')

                query.bindValue(':codigo', int(modificarNewDriver[0]))
                query.bindValue(':dni', str(modificarNewDriver[1]))
                query.bindValue(':alta', str(modificarNewDriver[2]))
                query.bindValue(':apel', str(modificarNewDriver[3]))
                query.bindValue(':nombre', str(modificarNewDriver[4]))
                query.bindValue(':direccion', str(modificarNewDriver[5]))
                query.bindValue(':provincia', str(modificarNewDriver[6]))
                query.bindValue(':municipio', str(modificarNewDriver[7]))
                query.bindValue(':movil', str(modificarNewDriver[8]))
                query.bindValue(':salario', str(modificarNewDriver[9]))
                query.bindValue(':carnet', str(modificarNewDriver[10]))
                if query.exec():
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle('Aviso')
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setText('Datos conductor modificado')
                    mbox.exec()
                    Conexion.mostrarDrivers(1)
                else:
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle('Aviso')
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    mbox.setText(query.lastError().text())
                    mbox.exec()

        except Exception as error:
            print("Error al modificar driver en conexion", error)

    def showSelectedDate(self=None):
        """
    Método para obtener la fecha seleccionada en un calendario y devolverla en formato de cadena.

    Este método utiliza el calendario almacenado en la variable global 'var.calendar2' para obtener la fecha seleccionada.
    Luego, convierte la fecha al formato de cadena "dd/MM/yyyy" y la devuelve.

    Returns:
        str: Fecha seleccionada en formato de cadena "dd/MM/yyyy".

    """
        selected_date = var.calendar2.selectedDate()
        return selected_date.toString("dd/MM/yyyy")

    def borraDriv(dni):
        """
            Método para dar de baja a un conductor en la base de datos.

            Este método verifica si el conductor ya está dado de baja consultando la fecha de baja en la base de datos.
            Si el conductor no está dado de baja, obtiene la fecha actual y actualiza la base de datos con la fecha de baja.
            Muestra mensajes de aviso en la interfaz gráfica según el resultado.

            Args:
                dni (str): DNI del conductor que se desea dar de baja.

            """

        global valor
        try:
            query1 = QtSql.QSqlQuery()
            query1.prepare('select bajadriver from drivers where  '
                           'dnidriver = :dni')
            query1.bindValue(':dni', str(dni))

            if query1.exec():
                while query1.next():
                    valor = query1.value(0)
                    print(valor)
            if valor == '':
                fecha = datetime.today()
                fecha = fecha.strftime("%d/%m/%Y")

                query = QtSql.QSqlQuery()
                query.prepare('update drivers set bajadriver = :fechabaja where '
                              'dnidriver = :dni')
                query.bindValue(':fechabaja', str(fecha))
                query.bindValue(':dni', str(dni))

                if query.exec():
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle('Aviso')
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setText('Conductor dado de baja')
                    mbox.exec()

                else:
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle('Aviso')
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    mbox.setText('Error al dar de baja al conductor: ' + query.lastError().text())
                    mbox.exec()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle('Aviso')
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setText('Conductor ya está dado de baja')
                mbox.exec()
        except Exception as error:
            print("Error al dar de baja al driver", error)

    def selectDrivers(estado):
        """
            Método para seleccionar y cargar datos de conductores según su estado en la base de datos.

            Este método ejecuta diferentes consultas SQL según el estado proporcionado y carga los datos de los conductores
            en la tabla correspondiente en la interfaz gráfica.

            Args:
                estado (int): Estado de los conductores a seleccionar. Puede ser 0 (todos), 1 (en alta), o 2 (dado de baja).

            """
        try:
            registros = []
            if estado == 0:
                query = QtSql.QSqlQuery()
                query.prepare("select codigo, apeldriver, nombredriver, movildriver, "
                              "carnet, bajadriver from drivers")
                if query.exec():
                    while query.next():
                        row = [query.value(i) for i in range(query.record().count())]
                        registros.append(row)

                if registros:
                    drivers.Drivers.cargarTablaDriver(registros)
                else:
                    var.ui.tabDrivers.setRowCount(0)

            elif estado == 1:
                query = QtSql.QSqlQuery()
                query.prepare("select codigo, apeldriver, nombredriver, movildriver, "
                              "carnet, bajadriver from drivers where bajadriver is null")
                if query.exec():
                    while query.next():
                        row = [query.value(i) for i in range(query.record().count())]
                        registros.append(row)

                if registros:
                    drivers.Drivers.cargarTablaDriver(registros)
                else:
                    var.ui.tabDrivers.setRowCount(0)


            elif estado == 2:
                query = QtSql.QSqlQuery()
                query.prepare("select codigo, apeldriver, nombredriver, movildriver, "
                              "carnet, bajadriver from drivers where bajadriver is not null")
                if query.exec():
                    while query.next():
                        row = [query.value(i) for i in range(query.record().count())]
                        registros.append(row)

                drivers.Drivers.cargarTablaDriver(registros)
        except Exception as error:
            print("Error al seleccionar los drivers", error)

    def selectDriversTodos(self):
        """
            Método para seleccionar y devolver todos los datos de conductores en la base de datos.

            Este método ejecuta una consulta SQL para seleccionar todos los conductores y devuelve los datos como una lista.

            Returns:
                list: Lista de listas, donde cada lista representa los datos de un conductor.


            """
        try:
            registros = []
            query = QtSql.QSqlQuery()
            query.prepare("select * from drivers order by codigo")

            if query.exec():
                while query.next():
                    row = [query.value(i) for i in range(query.record().count())]
                    registros.append(row)
            return registros

        except Exception as error:
            print("error devolver todos los drivers", error)

    def volverDarAlta(dni):
        """
            Método para dar de alta a un conductor que estaba dado de baja.

            Este método muestra un cuadro de diálogo de confirmación para dar de alta a un conductor que estaba previamente
            dado de baja. Si el usuario elige dar de alta, se actualiza la base de datos y se recarga la tabla de conductores.

            Args:
                dni (str): DNI del conductor que se dará de alta.

            """
        try:
            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Dar Alta")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
            mbox.setText("El conductor está dado de baja.\n¿Desea darlo de alta de nuevo?")
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            mbox.button(QtWidgets.QMessageBox.StandardButton.Yes).setText('Si')
            mbox.button(QtWidgets.QMessageBox.StandardButton.No).setText('No')
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Yes)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)

            if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
                query = QtSql.QSqlQuery()
                query.prepare("update drivers set bajadriver = :baja where dnidriver = :dni")
                query.bindValue(":dni", dni)
                # query.bindValue(":baja", None)
                if query.exec():
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Aviso")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setText("Conductor dado de alta")
                    mbox.exec()
                    drivers.Drivers.cargarTablaDriver()
                else:
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Aviso")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    mbox.setText("El conductor no se pudo dar de alta")
                    mbox.exec()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Aviso")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setText("Conductor no dado de alta")
                mbox.exec()

        except Exception as error:
            print("Error al dar alta de nuevo conductor en BD", error)

    def conductorEstaDadoDeBaja(self, dni):
        """
            Verifica si un conductor está dado de baja en la base de datos.

            Este método ejecuta una consulta SQL para obtener la fecha de baja de un conductor
            y verifica si está dado de baja.

            Args:
                dni (str): DNI del conductor.

            Returns:
                bool: True si el conductor está dado de baja, False en caso contrario.

            """
        query = QtSql.QSqlQuery()
        query.prepare("SELECT bajadriver FROM drivers WHERE dnidriver = :dni")
        query.bindValue(":dni", dni)

        if query.exec() and query.next():
            bajadriver_value = query.value(0)
            return bajadriver_value is not None and bajadriver_value != 0

        return False

    def driversEstadoAlta(self):
        """
            Obtiene la lista de conductores que están actualmente dados de alta.

            Este método ejecuta una consulta SQL para obtener la información de los conductores
            que están en estado de alta (sin fecha de baja).

            Returns:
                list: Lista de conductores en estado de alta. Cada elemento de la lista es una lista
                      que representa la información de un conductor.

            """
        try:
            conductores_alta = []
            query = QtSql.QSqlQuery()
            query.prepare("select codigo, apeldriver, nombredriver, movildriver, "
                          "carnet, bajadriver from drivers where bajadriver is null")

            if query.exec():
                while query.next():
                    conductor = [str(query.value(i)) for i in range(12)]
                    conductores_alta.append(conductor)

            return conductores_alta

        except Exception as error:
            print("Error al obtener conductores de alta:", error)
            return []

    def driversEstadoBaja(self):
        """
                    Obtiene la lista de conductores que están actualmente dados de baja.

                    Este método ejecuta una consulta SQL para obtener la información de los conductores
                    que están en estado de baja (fecha no esta a null).

                    Returns:
                        list: Lista de conductores en estado de baja. Cada elemento de la lista es una lista
                              que representa la información de un conductor.

                    """
        try:
            conductores_baja = []
            query = QtSql.QSqlQuery()
            query.prepare("select codigo, apeldriver, nombredriver, movildriver, "
                          "carnet, bajadriver from drivers where bajadriver is not null")

            if query.exec():
                while query.next():
                    conductor = [str(query.value(i)) for i in range(12)]
                    conductores_baja.append(conductor)

            return conductores_baja

        except Exception as error:
            print("Error al obtener conductores de baja:", error)
            return []

    def conductorExiste(self, dni):
        """
            Verifica si un conductor existe en la base de datos.

            Este método ejecuta una consulta SQL para contar la cantidad de registros en la tabla
            de conductores que tienen el DNI especificado.

            Args:
                dni (str): DNI del conductor.

            Returns:
                bool: True si el conductor existe, False en caso contrario.

            """
        query = QtSql.QSqlQuery()
        query.prepare("SELECT COUNT(*) FROM drivers WHERE bajadriver = :dni")
        query.bindValue(":dni", dni)

        if query.exec() and query.next():
            count = query.value(0)
            return count > 0

        return False

    """ZONA DE FACTURACION"""


    def altaFacturacion(nuevaFactura):
        """
            Registra una nueva factura en la base de datos.

            Este método verifica que los campos necesarios no estén vacíos y que el cliente asociado a la factura
            exista y esté dado de alta. Luego, comprueba si la factura ya existe antes de insertarla en la base de datos.

            Args:
                nuevaFactura (list): Lista que contiene los datos de la nueva factura [DNI Cliente, Fecha, Conductor].

            Returns:
                None

            """

        try:
            if not all(field.strip() for field in nuevaFactura[:3]):
                Conexion.show_warning("Faltan datos:\n Cliente, Alta Factura, Conductor no pueden estar vacíos")

            elif Conexion.comprobarCliente(nuevaFactura[0]):
                Conexion.show_warning("Cliente dado de baja. No se puede dar de alta la factura.")

            elif not Conexion.existeCliente(nuevaFactura[0]):
                Conexion.show_warning("Cliente no registrado en la base de datos")

            else:
                # Verificar si la factura ya existe
                if Conexion.existeFactura(nuevaFactura[0], nuevaFactura[1], nuevaFactura[2]):
                    Conexion.show_warning("La factura ya existe en la base de datos")
                else:
                    query = QtSql.QSqlQuery()
                    query.prepare('INSERT INTO facturas (dnicliente, fecha, driver, descuento) VALUES (:dni, :fecha, :driver, :descuento)')
                    query.bindValue(':dni', nuevaFactura[0])
                    query.bindValue(':fecha', nuevaFactura[1])
                    query.bindValue(':driver', nuevaFactura[2])
                    query.bindValue(':descuento', nuevaFactura[3])


                    if query.exec():
                        Conexion.show_info("Factura guardada. \n Se recomienda añadir un viaje")

                        Conexion.cargarFacturas()

                        factura_id = query.lastInsertId()
                        print(factura_id)
                        return factura_id
                    else:
                        Conexion.show_warning("ERROR AL GRABAR LA FACTURA")

        except Exception as error:
            print("Error al dar de alta la factura", error)



    @staticmethod
    def existeFactura(dni_cliente, fecha, driver):
        """
            Verifica si una factura ya existe en la base de datos.

            Este método comprueba si hay una factura con los mismos valores de DNI Cliente, Fecha y Conductor en la base de datos.

            Args:
                dni_cliente (str): DNI del cliente asociado a la factura.
                fecha (str): Fecha de la factura.
                driver (str): Conductor asociado a la factura.

            Returns:
                bool: True si la factura existe, False en caso contrario.

            """
        query = QtSql.QSqlQuery()
        query.prepare('SELECT COUNT(*) FROM facturas WHERE dnicliente = :dni AND fecha = :fecha AND driver = :driver')
        query.bindValue(':dni', dni_cliente)
        query.bindValue(':fecha', fecha)
        query.bindValue(':driver', driver)

        if query.exec() and query.next():
            return query.value(0) > 0

        return False

    #VERIFICA QUE EL CLIENT ESTA DADO DE BAJKA
    def comprobarCliente(dato):
        """
            Comprueba si un cliente existe en la base de datos y está dado de baja.

            Este método verifica si el DNI del cliente existe en la tabla de clientes y si está dado de baja.

            Args:
                dato (str): DNI del cliente a comprobar.

            Returns:
                bool: True si el cliente existe y está dado de baja, False en caso contrario.

            """
        try:
            # Verificar si el DNI existe en la tabla clientes y no está dado de baja
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM clientes WHERE dnicliente = :dni and bajacliente is not null")
            query.bindValue(":dni", str(dato))

            if query.exec():
                if query.next():
                    return True
                else:
                    return False

        except Exception as error:
            print("Error al comprobar cliente baja", error)

    # VERIFICA QUE EL DNI DEL CLIENTE EXISTE
    def existeCliente(dato):
        """
            Comprueba si un cliente existe en la base de datos y no está dado de baja.

            Este método verifica si el DNI del cliente existe en la tabla de clientes y si no está dado de baja.

            Args:
                dato (str): DNI del cliente a comprobar.

            Returns:
                bool: True si el cliente existe y no está dado de baja, False en caso contrario.

            """
        try:
            # Verificar si el DNI existe en la tabla clientes
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM clientes WHERE dnicliente = :dni and bajacliente is null")
            query.bindValue(":dni", str(dato))

            if query.exec():
                if query.next():
                    return True
                else:
                    return False

        except Exception as error:
            print("Error al comprobar si existe el cliente", error)


    @staticmethod
    def cargarFacturas():
        """
            Carga las facturas desde la base de datos y actualiza la tabla de facturas en la interfaz gráfica.

            Este método realiza una consulta a la base de datos para obtener las facturas y luego llama al método
            cargarTablaFacturas de la clase Facturas para actualizar la interfaz gráfica con los nuevos datos.

            Args:
                self: Parámetro opcional para permitir llamadas al método sin instancia específica.

            Returns:
                None

            """
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("select numfac, dnicliente from facturas")
            if query.exec():
                while query.next():
                    row = [query.value(i) for i in range(query.record().count())]  # funcion lambda
                    registro.append(row)

            facturas.Facturas.cargarTablaFacturas(registro)

        except Exception as error:
            print("ERROR CARGAR FACTURA", error)

    def cargarViaje(self):
        """
            Carga los datos de viajes desde la base de datos y actualiza la tabla de viajes en la interfaz gráfica.

            Este método realiza una consulta a la base de datos para obtener los datos de viajes y luego llama al método
            cargarTablaViajes de la clase Viajes para actualizar la interfaz gráfica con los nuevos datos.

            Args:
                self: Parámetro opcional para permitir llamadas al método sin instancia específica.

            """
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("select factura, origen, destino, tarifa, km from viajes")
            if query.exec():
                while query.next():
                    row = [query.value(i) for i in range(query.record().count())]  # funcion lambda
                    registro.append(row)
            viajes.Viajes.cargarTablaViajes(registro)

        except Exception as error:
            print("ERROR CARGAR FACTURA", error)






    """ZONA FUNCIONES WARNING Y AVISOS"""

    def show_warning(message):
        """
            Muestra un cuadro de diálogo de advertencia con el mensaje proporcionado.

            Este método crea y muestra un cuadro de diálogo de advertencia con un ícono de advertencia y el mensaje proporcionado.

            """
        mbox = QtWidgets.QMessageBox()
        mbox.setWindowTitle('Aviso')
        mbox.setWindowIcon(QtGui.QIcon('./IMG/aviso.jpg'))
        mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        mbox.setText(message)
        mbox.exec()

    def show_info(message):
        """
            Muestra un cuadro de diálogo informativo con el mensaje proporcionado.

            Este método crea y muestra un cuadro de diálogo informativo con un ícono de información y el mensaje proporcionado.

            Args:
                message (str): El mensaje a mostrar en el cuadro de diálogo.

            """
        mbox = QtWidgets.QMessageBox()
        mbox.setWindowTitle("Aviso")
        mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
        mbox.setText(message)
        mbox.exec()







