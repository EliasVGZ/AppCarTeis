from datetime import datetime

from PyQt6 import QtWidgets, QtSql, QtGui

import clientes
import var


class ConexionCliente():

    def conexion(self=None):
        """
            Establece una conexión a una base de datos SQLite utilizando PyQt.

            Parámetros:
                self: Parámetro opcional, generalmente utilizado en métodos de clases.

            Retorna:
                bool: True si la conexión fue exitosa, False en caso contrario.

            """
        var.bbdd = 'bbdd.sqlite'
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(var.bbdd)
        if not db.open():
            print("error de conexión")
            return False
        else:
            print("base de datos conectada")

    def selMuni(self=None):
        """
            Llena el combo box de localidades del cliente en función de la provincia seleccionada.

            Parámetros:
                self: Parámetro opcional, generalmente utilizado en métodos de clases.

            """
        try:
            var.ui.cmbLocalidadCliente.clear()
            id = 0
            provcliente = var.ui.cmbProvinciaCliente.currentText()  #
            query = QtSql.QSqlQuery()

            query.prepare('select idprov from provincias where provincia = :prov')
            query.bindValue(':prov', provcliente)
            if query.exec():
                while query.next():  # LLENAR LAS PROVINCIAS MIENTRAS HAYA
                    id = query.value(0)
            query1 = QtSql.QSqlQuery()
            query1.prepare('select municipio from municipios where idprov = :id')
            query1.bindValue(':id', int(id))
            if query1.exec():
                var.ui.cmbLocalidadCliente.addItem('')
                while query1.next():
                    var.ui.cmbLocalidadCliente.addItem(query1.value(0))

        except Exception as error:
            print("error seleccion municipios ", error)

    @staticmethod
    def guardarCliente(cliente):
        """
            Guarda la información de un cliente en la base de datos.

            Parámetros:
                cliente (list): Lista que contiene la información del cliente.

            Retorna:
                bool: True si la operación de guardado fue exitosa, False en caso contrario.
            """
        try:
            if (cliente[0].strip() == "" or cliente[1].strip() == "" or cliente[2].strip() == "" or
                    cliente[3].strip() == "" or cliente[4].strip() == "" or cliente[5].strip() == "" or cliente[
                        6].strip() == ""):
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Aviso")
                mbox.setWindowIcon(QtGui.QIcon("./img/warning.png"))
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mensaje = "Faltan DATOS. Debe llenar todos los campos."
                mbox.setText(mensaje)
                mbox.exec()
            else:
                query = QtSql.QSqlQuery()
                query.prepare(
                    'INSERT INTO clientes (dnicliente, altacliente, razonSocial, direccioncliente, telefono,'
                    ' provinciacliente, municipiocliente, correo) '
                    'VALUES (:dni, :altacliente, :razonsocial, :direccioncliente, :telefono, :provcliente,'
                    ':municliente, :correo)')

                query.bindValue(':dni', str(cliente[0]))
                query.bindValue(':altacliente', str(cliente[1]))
                query.bindValue(':razonsocial', str(cliente[2]))
                query.bindValue(':direccioncliente', str(cliente[3]))
                query.bindValue(':telefono', str(cliente[4]))
                query.bindValue(':provcliente', str(cliente[5]))
                query.bindValue(':municliente', str(cliente[6]))
                query.bindValue(':correo', str(cliente[7]))

                if query.exec():  # Usar exec_() en lugar de exec
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle('Aviso')
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setText("Cliente dado de alta.")
                    mbox.exec()
                    return True
                else:
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle('Aviso')
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    mbox.setText("Asegúrese de que el cliente no existe.")
                    mbox.exec()
                    return False
                # Seleccionar datos de clientes de la base de datos
            ConexionCliente.mostrarClientes(1)

        except Exception as error:
            print("Error guardando los clientes", error)
            return False  # Agregar un retorno False en caso de excepción

    def borrarCliente(dni):
        """
    Da de baja a un cliente en la base de datos.

    Parámetros:
        dni (str): DNI del cliente a dar de baja.

    Descripción:
        Este método verifica si un cliente ya ha sido dado de baja consultando la fecha de baja en la base de datos.
        Si el cliente no está dado de baja, actualiza la fecha de baja con la fecha actual.
        Muestra mensajes informativos o de advertencia según el resultado de la operación.

    Retorna:
        None

    """
        global valor
        try:
            query1 = QtSql.QSqlQuery()
            query1.prepare('select bajacliente from clientes where  '
                           'dnicliente = :dni')
            query1.bindValue(':dni', str(dni))

            if query1.exec():
                while query1.next():
                    valor = query1.value(0)

            if valor == '':
                fecha = datetime.today()
                fecha = fecha.strftime("%d/%m/%Y")

                query = QtSql.QSqlQuery()
                query.prepare('update clientes set bajacliente = :fechabaja where '
                              'dnicliente = :dni')
                query.bindValue(':fechabaja', str(fecha))
                query.bindValue(':dni', str(dni))

                if query.exec():
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle('Aviso')
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setText('Cliente dado de baja')
                    mbox.exec()
                else:
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle('Aviso')
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    mbox.setText('Error al dar de baja al Cliente: ' + query.lastError().text())
                    mbox.exec()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle('Aviso')
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setText('Cliente ya está dado de baja')
                mbox.exec()
        except Exception as error:
            print("Error al dar de baja al Cliente", error)

    def mostrarClientes(self):
        """
            Muestra la información de los clientes en la interfaz gráfica.

            Este método recupera la información de los clientes desde la base de datos y la presenta en la interfaz gráfica.
            Dependiendo de la opción seleccionada (alta o todos), se muestra la información de los clientes dados de alta o todos
            los clientes. Si no hay clientes, se establece el número de filas en la tabla de clientes a 0.

            Parámetros:
                self: Parámetro opcional, generalmente utilizado en métodos de clases.

            Retorna:
                None

            """
        try:
            registros = []
            if var.ui.rbtAlta.isChecked():
                estado = 1
                ConexionCliente.selectClientes(estado)
            else:
                query1 = QtSql.QSqlQuery()
                query1.prepare("select codigocliente, razonSocial, telefono, provinciacliente from clientes")
                if query1.exec():
                    while query1.next():
                        row = [query1.value(i) for i in range(query1.record().count())]  # funcion lambda
                        registros.append(row)
            # SI ESTAN TODOS DE BAJA DEBE MOSTRAR LA TABLA DE ALTA VACIA
            if registros:
                clientes.Clientes.cargarTablaClientes(registros)
            else:
                var.ui.tabClientes.setRowCount(0)

        except Exception as error:
            print("error mostrar resultados", error)

    def oneCliente(codigo):
        """
            Recupera la información de un cliente específico de la base de datos.

            Este método busca en la base de datos la información del cliente correspondiente al código proporcionado
            como parámetro. Retorna una lista con la información del cliente si se encuentra en la base de datos.

            Parámetros:
                codigo (str): Código del cliente a buscar.

            Retorna:
                list: Lista con la información del cliente encontrado, o una lista vacía si no se encuentra.

            """
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM clientes WHERE codigocliente = :codigo")
            query.bindValue(":codigo", str(codigo))
            if query.exec():
                while query.next():
                    for i in range(8):
                        registro.append(str(query.value(i)))
            return registro

        except Exception as error:
            print("Error en fichero conexion datos de 1 cliente: ", error)

    def codigoCliente(dni):
        """

            Busca el código de un cliente en la base de datos a partir de su DNI.

            Este método busca el código del cliente correspondiente al DNI proporcionado como parámetro en la base de datos.
            Si encuentra el cliente, actualiza la interfaz gráfica con la información del cliente y retorna una lista con
            la información del cliente. Si el DNI no existe, muestra un mensaje de aviso en la interfaz gráfica.

            Parámetros:
                dni (str): DNI del cliente a buscar.

            Retorna:
                list or None: Lista con la información del cliente encontrado, o None si el DNI no existe.

            """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT codigocliente FROM clientes WHERE dnicliente = :dni")
            query.bindValue(":dni", str(dni))

            if query.exec():
                codigocliente = None
                while query.next():
                    codigocliente = query.value(0)
                    clientes.Clientes.buscarClienteTabla(codigocliente)

                if codigocliente is not None:
                    registro = ConexionCliente.oneCliente(codigocliente)
                    return registro
                else:
                    # Si no se encuentra el cliente, mostrar un aviso
                    var.ui.lblValidarDni_2.setStyleSheet('color:red;')
                    var.ui.lblValidarDni_2.setText('X')
                    var.ui.txtDni2.clear()  # Limpia el campo de texto
                    var.ui.txtDni2.setFocus()  # Mantiene el foco en el campo de texto
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle('Aviso')
                    mbox.setWindowIcon(QtGui.QIcon('./IMG/aviso.jpg'))  # Ruta del archivo del icono
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    mensaje = ('          DNI no existe          ')
                    mbox.setText(mensaje)
                    var.ui.txtcifcliente.setText('')
                    mbox.exec()
                    return None

        except Exception as error:
            print("Error en búsqueda de código de un cliente: ", error)

            return None

    def modifCliente(modificarNewCliente):
        """

            Modifica la información de un cliente en la base de datos.

            Este método busca la información del cliente a modificar en la base de datos a partir del código proporcionado.
            Si encuentra el cliente, actualiza la información con los nuevos datos proporcionados en la lista
            `modificarNewCliente`. Muestra mensajes informativos o de advertencia según el resultado de la operación.

            Parámetros:
                modificarNewCliente (list): Lista con la nueva información del cliente.

            """
        try:
            registro = ConexionCliente.oneCliente(modificarNewCliente[0])
            print("printeo el registro que llega a modifcar cliente "+str(registro))


            if registro and modificarNewCliente[0] == registro[0]:

                query = QtSql.QSqlQuery()
                query.prepare(
                    'update clientes set dnicliente = :dni, altacliente = :altacliente, razonSocial = :razonsocial, direccioncliente = :dire, telefono = :tel, provinciacliente = :prov, '
                    'municipiocliente = :muni where codigocliente = :codigo')

                query.bindValue(':codigo', int(modificarNewCliente[0]))
                query.bindValue(':altacliente', str(modificarNewCliente[2]))
                query.bindValue(':dni', str(modificarNewCliente[1]))
                query.bindValue(':razonsocial', str(modificarNewCliente[3]))
                query.bindValue(':dire', str(modificarNewCliente[4]))
                query.bindValue(':tel', str(modificarNewCliente[5]))
                query.bindValue(':prov', str(modificarNewCliente[6]))
                query.bindValue(':muni', str(modificarNewCliente[7]))

                if query.exec():
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle('Aviso')
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setText('Datos cliente modificado')
                    mbox.exec()
                    estado = 1
                    ConexionCliente.selectClientes(estado)
                    #ConexionCliente.mostrarClientes(self=None)
                else:
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle('Aviso')
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    mbox.setText(query.lastError().text())
                    mbox.exec()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Aviso")
                msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msg.setText("No existe el cliente a modificar.")
                msg.exec()

        except Exception as error:
            print("Error al modificar cliente en conexion", error)

    def selectClientes(estado):
        """
            Selecciona y muestra los clientes en la interfaz gráfica según su estado.

            Este método selecciona y recupera los clientes de la base de datos dependiendo del estado proporcionado como
            parámetro. Los estados posibles son:
            - estado 0: Todos los clientes (alta y baja)
            - estado 1: Clientes dados de alta (sin fecha de baja)
            - estado 2: Clientes dados de baja (con fecha de baja)
            Luego, carga la información en la tabla de clientes de la interfaz gráfica.

            Parámetros:
                estado (int): Estado de los clientes a seleccionar.

        """
        try:
            registros = []

            if estado == 0:
                query = QtSql.QSqlQuery()
                query.prepare(
                    "select codigocliente, razonSocial, telefono, provinciacliente, bajacliente from clientes")
                if query.exec():
                    while query.next():
                        row = [query.value(i) for i in range(query.record().count())]
                        registros.append(row)

                if registros:
                    clientes.Clientes.cargarTablaClientes(registros)
                else:
                    var.ui.tabClientes.setRowCount(0)

            elif estado == 1:
                # TODO ZONA ALTA
                query = QtSql.QSqlQuery()
                query.prepare(
                    "select codigocliente, razonSocial, telefono, provinciacliente, bajacliente from clientes where bajacliente is null")
                if query.exec():
                    while query.next():
                        row = [query.value(i) for i in range(query.record().count())]
                        registros.append(row)

                if registros:
                    clientes.Clientes.cargarTablaClientes(registros)
                else:
                    var.ui.tabClientes.setRowCount(0)

            elif estado == 2:  # TODO ZONA DE BAJA
                query = QtSql.QSqlQuery()
                query.prepare(
                    "select codigocliente, razonSocial, telefono, provinciacliente, bajacliente from clientes where bajacliente is not null")
                if query.exec():
                    while query.next():
                        row = [query.value(i) for i in range(query.record().count())]
                        registros.append(row)

                clientes.Clientes.cargarTablaClientes(registros)

        except Exception as error:
            print("Error al seleccionar los clientes", error)

    def selectClientesTodos(self):
        """

            Selecciona y devuelve todos los clientes de la base de datos.

            Este método realiza una consulta para obtener la información de todos los clientes presentes en la base de datos.
            La información se devuelve en forma de una lista de registros.

            Parámetros:
                self: Parámetro opcional, generalmente utilizado en métodos de clases.

            Retorna:
                list: Lista de registros que contienen la información de todos los clientes.

            """
        try:
            registros = []
            query = QtSql.QSqlQuery()
            query.prepare("select * from clientes order by codigocliente")

            if query.exec():
                while query.next():
                    row = [query.value(i) for i in range(query.record().count())]
                    registros.append(row)
            return registros

        except Exception as error:
            print("error devolver todos los drivers", error)
