import os, var, shutil
from PyQt6 import QtSql, QtWidgets
from reportlab.pdfgen import canvas
from datetime import datetime
import conexion
import svglib.svglib

import conexionClientes
import facturas
import viajes


class Informes:
    @staticmethod
    def mostrarViajesCliente(self):

        try:
            fecha = datetime.today()
            nombre = fecha.strftime('%d-%m-%Y_%H-%M-%S') + '_listadoviajes.pdf'
            var.report = canvas.Canvas(os.path.join('informes', nombre))
            titulo = "Listado Viajes a clientes"
            Informes.topInforme(titulo)
            Informes.footInforme(titulo)

            items = ['VIAJE', 'ORIGEN', 'DESTINO', 'KM']
            var.report.setFont('Helvetica-Bold', size=10)
            var.report.drawString(55, 675, str(items[0]))
            var.report.drawString(200, 675, str(items[1]))
            var.report.drawString(300, 675, str(items[2]))
            var.report.drawString(450, 675, str(items[3]))
            var.report.line(50, 670, 525, 670)  # Ajusta la longitud de la línea

            # OBTENEMOS DATOS DE LA BASE DE DATOS
            query = QtSql.QSqlQuery()
            query.prepare('select idviajes, origen, destino, km from viajes')
            var.report.setFont('Helvetica', size=9)

            if query.exec():
                i = 55
                j = 655
                while query.next():
                    if j <= 80:
                        #var.report.drawString(450, 75, 'Página siguiente...')
                        var.report.showPage()  # Crea una nueva página
                        Informes.topInforme(titulo)
                        Informes.footInforme(titulo)
                        var.report.setFont('Helvetica-Bold', size=10)
                        var.report.drawString(55, 675, str(items[0]))
                        var.report.drawString(200, 675, str(items[1]))
                        var.report.drawString(300, 675, str(items[2]))
                        var.report.drawString(450, 675, str(items[3]))
                        var.report.line(50, 670, 525, 670)  # Ajusta la longitud de la línea

                        i = 55
                        j = 655
                    var.report.setFont('Helvetica', size=9)


                    var.report.drawString(i + 8, j, str(query.value(0)))
                    var.report.drawString(i + 150, j, str(query.value(1)))
                    var.report.drawString(i + 250, j, str(query.value(2)))
                    var.report.drawString(i + 400, j, str(query.value(3)))
                    j = j - 25


                    # total_km =0
                    # total_km += total_km+query.value(3)
                    # total_str = "{:.2f}".format(total_km)
                    # #var.report.drawString(i + 405, j, str(total_str))
                    # j = j - 25
                    #
                    # var.report.setFont('Helvetica-Bold', size=10)
                    # var.report.drawRightString(450, 75, 'TOTAL KILOMETROS: ' + str('{:.2f}'.format(total_km)))

            var.report.save()
            rootPath = '.\\informes'

            for file in os.listdir(rootPath):
                if file.endswith(nombre):
                    os.startfile(os.path.join(rootPath, file))

        except Exception as error:
            print('Error en informe Clientes', error)

    def elegirinforme(self):
        """
            Permite al usuario elegir qué informes desea generar.

            Este método muestra un cuadro de diálogo con opciones para generar informes de conductores y/o clientes.
            Si el usuario elige generar informes, se ejecutan los informes correspondientes y se muestra un mensaje de aviso.

            Parameters:
            - self: Referencia a la instancia actual de la clase.

            Returns:
            - None

            """
        try:
            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Realizar Informe")
            mbox.setText("Seleccione informe/es")

            conductorcheck = QtWidgets.QCheckBox("Informe de conductores")
            clientecheck = QtWidgets.QCheckBox("Informe de clientes")

            layout = QtWidgets.QVBoxLayout()
            layout.addWidget(conductorcheck)
            layout.addWidget(clientecheck)

            container = QtWidgets.QWidget()
            container.setLayout(layout)

            mbox.layout().addWidget(container, 1, 1, 1, mbox.layout().columnCount())

            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            mbox.button(QtWidgets.QMessageBox.StandardButton.Yes).setText('Aceptar')
            mbox.button(QtWidgets.QMessageBox.StandardButton.No).setText('Cancelar')

            resultado = mbox.exec()

            if resultado == QtWidgets.QMessageBox.StandardButton.Yes:
                if conductorcheck.isChecked():
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle('Aviso ')
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setText('Informe de conductores creado')
                    mbox.exec()
                    Informes.reportconductores(self)
                if clientecheck.isChecked():
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle('Aviso ')
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setText('Informe de Clientes creado')
                    mbox.exec()
                    Informes.reportclientes(self)

                if not (conductorcheck.isChecked() or clientecheck.isChecked()):
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle('Aviso", "No se ha seleccionado ningún informe')
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    mbox.setText('Cliente ya está dado de baja')
                    mbox.exec()

        except Exception as error:
            print("Error al elegir informes", error)

    @staticmethod
    def reportclientes(self):
        """
            Genera un informe en formato PDF con un listado de clientes.

            Este método utiliza la biblioteca ReportLab para crear un informe PDF que contiene un listado de clientes.
            Los datos se obtienen de la base de datos y se presentan en forma tabular en el informe.

            Parameters:
            - self: Referencia a la instancia actual de la clase.

            Returns:
            - None

            """
        try:
            fecha = datetime.today()
            nombre = fecha.strftime('%d-%m-%Y_%H-%M-%S') + '_listadoclientes.pdf'
            var.report = canvas.Canvas(os.path.join('informes', nombre))
            titulo = "Listado Clientes"
            Informes.topInforme(titulo)
            Informes.footInforme(titulo)

            items = ['CODIGO', 'DNI', 'RAZON SOCIAL', 'MUNICIPIO', 'TELEFONO', 'FECHA BAJA']
            var.report.setFont('Helvetica-Bold', size=10)
            var.report.drawString(55, 675, str(items[0]))
            var.report.drawString(120, 675, str(items[1]))
            var.report.drawString(160, 675, str(items[2]))
            var.report.drawString(285, 675, str(items[3]))
            var.report.drawString(370, 675, str(items[4]))
            var.report.drawString(460, 675, str(items[5]))  # Nueva coordenada para "FECHA BAJA"
            var.report.line(50, 670, 525, 670)  # Ajusta la longitud de la línea

            # OBTENEMOS DATOS DE LA BASE DE DATOS
            query = QtSql.QSqlQuery()
            query.prepare('select codigocliente, dnicliente, razonSocial, municipiocliente, telefono, bajacliente '
                          'from clientes order by razonSocial')
            var.report.setFont('Helvetica', size=9)

            if query.exec():
                i = 55
                j = 655
                while query.next():
                    if j <= 80:
                        var.report.drawString(450, 75, 'Página siguiente...')
                        var.report.showPage()  # Crea una nueva página
                        Informes.topInforme(titulo)
                        Informes.footInforme(titulo)
                        var.report.setFont('Helvetica-Bold', size=10)
                        var.report.drawString(55, 675, str(items[0]))
                        var.report.drawString(120, 675, str(items[1]))
                        var.report.drawString(160, 675, str(items[2]))
                        var.report.drawString(285, 675, str(items[3]))
                        var.report.drawString(370, 675, str(items[4]))
                        var.report.drawString(460, 675, str(items[5]))  # Nueva coordenada para "FECHA BAJA"
                        var.report.line(50, 670, 525, 670)  # Ajusta la longitud de la línea

                        i = 55
                        j = 655
                    var.report.setFont('Helvetica', size=9)

                    # Obtén el DNI completo
                    dni_completo = str(query.value(1))

                    # Oculta todos los dígitos del DNI excepto los últimos dos antes de la letra
                    dni_oculto = '*' * (len(dni_completo) - 2) + dni_completo[-2:]

                    var.report.drawString(i + 8, j, str(query.value(0)))
                    var.report.drawString(i + 50, j, dni_oculto)
                    var.report.drawString(i + 100, j, str(query.value(2)))
                    var.report.drawString(i + 230, j, str(query.value(3)))
                    var.report.drawString(i + 320, j, str(query.value(4)))
                    var.report.drawString(i + 410, j, str(query.value(5)))  # Nueva coordenada para "FECHA BAJA"
                    j = j - 25

            var.report.save()
            rootPath = '.\\informes'

            for file in os.listdir(rootPath):
                if file.endswith(nombre):
                    os.startfile(os.path.join(rootPath, file))

        except Exception as error:
            print('Error en informe Clientes', error)



    @staticmethod
    def reportconductores(self):
        """
            Genera un informe en formato PDF con un listado de conductores.

            Este método utiliza la biblioteca ReportLab para crear un informe PDF que contiene un listado de conductores.
            Los datos se obtienen de la base de datos y se presentan en forma tabular en el informe.

            Parameters:
            - self: Referencia a la instancia actual de la clase.

            Returns:
            - None

            """
        try:
            fecha = datetime.today()
            nombre = fecha.strftime('%d-%m-%Y_%H-%M-%S') + '_listadoconductores.pdf'
            var.report = canvas.Canvas(os.path.join('informes', nombre))
            titulo = "Listado Conductores"
            Informes.topInforme(titulo)
            Informes.footInforme(titulo)

            items = ['CODIGO', 'APELLIDOS', 'NOMBRE', 'MOVIL', 'LICENCIA', 'FECHA BAJA']
            var.report.setFont('Helvetica-Bold', size=10)
            var.report.drawString(50, 675, str(items[0]))
            var.report.drawString(100, 675, str(items[1]))
            var.report.drawString(180, 675, str(items[2]))
            var.report.drawString(285, 675, str(items[3]))
            var.report.drawString(370, 675, str(items[4]))
            var.report.drawString(460, 675, str(items[5]))  # Nueva coordenada para "FECHA BAJA"
            var.report.line(50, 670, 525, 670)  # Ajusta la longitud de la línea

            # OBTENEMOS DATOS DE LA BASE DE DATOS
            query = QtSql.QSqlQuery()
            query.prepare('select codigo, apeldriver, nombredriver, movildriver, carnet, bajadriver '
                          'from drivers order by codigo')
            var.report.setFont('Helvetica', size=9)

            if query.exec():
                i = 55
                j = 655
                while query.next():
                    if j <= 80:
                        var.report.drawString(450, 75, 'Página siguiente...')
                        var.report.showPage()  # Crea una nueva página
                        Informes.topInforme(titulo)
                        Informes.footInforme(titulo)
                        var.report.setFont('Helvetica-Bold', size=10)
                        var.report.drawString(50, 675, str(items[0]))
                        var.report.drawString(100, 675, str(items[1]))
                        var.report.drawString(180, 675, str(items[2]))
                        var.report.drawString(285, 675, str(items[3]))
                        var.report.drawString(370, 675, str(items[4]))
                        var.report.drawString(460, 675, str(items[5]))  # Nueva coordenada para "FECHA BAJA"
                        var.report.line(50, 670, 525, 670)  # Ajusta la longitud de la línea

                        i = 55
                        j = 655
                    var.report.setFont('Helvetica', size=9)

                    var.report.drawString(i + 8, j, str(query.value(0)))
                    var.report.drawString(i + 45, j, str(query.value(1)))
                    var.report.drawString(i + 130, j, str(query.value(2)))
                    var.report.drawString(i + 225, j, str(query.value(3)))
                    var.report.drawString(i + 320, j, str(query.value(4)))
                    var.report.drawString(i + 410, j, str(query.value(5)))  # Nueva coordenada para "FECHA BAJA"
                    j = j - 25

            var.report.save()
            rootPath = '.\\informes'

            for file in os.listdir(rootPath):
                if file.endswith(nombre):
                    os.startfile(os.path.join(rootPath, file))

        except Exception as error:
            print('Error en informe Drivers', error)

    def topInforme(titulo):
        """
            Crea la cabecera del informe en formato PDF.

            Este método configura la cabecera del informe PDF, incluyendo el nombre de la empresa, el título del informe,
            la línea de separación y la información de contacto.

            Parameters:
            - titulo: Título del informe.

            Returns:
            - None

            """
        try:
            logo = '.\IMG\icono.png'
            var.report.line(50, 800, 525, 800)
            var.report.setFont('Helvetica-Bold', size=14)
            var.report.drawString(55, 785, 'Transportes Teis')
            var.report.drawString(240, 695, titulo)
            var.report.line(50, 690, 525, 690)
            var.report.drawImage(logo, 440, 725, width=40, height=35)#Dibuja la imagen en el informe
            var.report.setFont('Helvetica', size=9)
            var.report.drawString(55, 770, 'CIF:A12345678')
            var.report.drawString(55, 755, 'Avda Galicia - 101')
            var.report.drawString(55, 740, 'Vigo - 36216 - España')
            var.report.drawString(55, 710, 'Telefono: 986123 456')
            var.report.drawString(55, 725, 'e-mail: cartesteis@gmail.com')



        except Exception as error:
            print('Error en cabecera de informe ', error)

    @staticmethod
    def reportfacturas(self):
        """
            Genera un informe en formato PDF con detalles de las facturas.

            Este método utiliza la biblioteca ReportLab para crear un informe PDF que contiene detalles de las facturas,
            incluyendo información sobre los viajes asociados a la factura y los totales.

            Parameters:
            - self: Referencia a la instancia actual de la clase.

            Returns:
            - None

            """
        try:
            global continuar_generacion  # Acceder a la variable global
            codigo_factura = var.ui.lblNumFac.text()

            fecha = datetime.today()
            nombre = codigo_factura + '_facturas.pdf'
            var.report = canvas.Canvas(os.path.join('informes', nombre))
            titulo = "FACTURAS"
            Informes.topInformeFactura(titulo)
            Informes.footInforme(titulo)


            codigo_factura = var.ui.lblNumFac.text()

            # OBTENEMOS DATOS DE LA BASE DE DATOS
            query = QtSql.QSqlQuery()
            query.prepare('SELECT idviajes, origen, destino, tarifa, km '
                          'FROM viajes '
                          'WHERE factura = :codigo_factura '  
                          'ORDER BY idviajes')
            query.bindValue(':codigo_factura', codigo_factura)

            var.report.setFont('Helvetica', size=9)


            items = ['Codigo', 'Origen', 'Destino', 'Tarifa', 'KM', 'Total']
            var.report.setFont('Helvetica-Bold', size=10)
            var.report.drawString(50, 640, str(items[0]))
            var.report.drawString(100, 640, str(items[1]))
            var.report.drawString(200, 640, str(items[2]))
            var.report.drawString(300, 640, str(items[3]))
            var.report.drawString(370, 640, str(items[4]))
            var.report.drawString(460, 640, str(items[5]))
            var.report.line(50, 660, 525, 660)  # Ajusta la longitud de la línea

            if query.exec():
                i = 55
                j = 620
                while query.next():
                    if j <= 80:
                        var.report.drawString(450, 75, 'Página siguiente...')
                        var.report.showPage()  # Crea una nueva página
                        Informes.topInforme(titulo)
                        Informes.footInforme(titulo)
                        var.report.setFont('Helvetica-Bold', size=10)
                        var.report.drawString(50, 600, str(items[0]))
                        var.report.drawString(100, 635, str(items[1]))
                        var.report.drawString(220, 635, str(items[2]))
                        var.report.drawString(355, 635, str(items[3]))
                        var.report.drawString(370, 635, str(items[4]))
                        var.report.drawString(460, 635, str(items[5]))
                        var.report.line(50, 670, 525, 630)  # Ajusta la longitud de la línea

                        i = 55
                        j = 620
                    var.report.setFont('Helvetica', size=9)

                    var.report.drawString(i + 8, j, str(query.value(0)))
                    var.report.drawString(i + 45, j, str(query.value(1)))
                    var.report.drawString(i + 150, j, str(query.value(2)))
                    var.report.drawString(i + 250, j, str(query.value(3)))
                    var.report.drawString(i + 315, j, str(query.value(4)))


                    #calculo del total
                    total_viaje = query.value(3) * query.value(4)
                    total_str = "{:.2f}".format(total_viaje)
                    var.report.drawString(i + 405, j, str(total_str))
                    j = j - 25

                    subtotal = Informes.limpiar_cadena_para_conversion(var.ui.lbl_subTotal.text())
                    iva = Informes.limpiar_cadena_para_conversion(var.ui.lbl_iva.text())
                    total = Informes.limpiar_cadena_para_conversion(var.ui.lbl_total.text())
                    descuento = Informes.limpiar_cadena_para_conversion(var.ui.lbl_descuento.text())

                    var.report.setFont('Helvetica-Bold', size=10)
                    var.report.drawRightString(i + 450, 130, 'Subtotal: ' + str('{:.2f}'.format(subtotal)) + ' €')
                    var.report.drawRightString(i + 450, 115, 'IVA: ' + str('{:.2f}'.format(iva)) + ' €')
                    var.report.drawRightString(i + 450, 100, 'DESCUENTO: ' + str('{:.2f}'.format(descuento)) + ' €')
                    var.report.drawRightString(i + 450, 85, 'Total: ' + str('{:.2f}'.format(total)) + ' €')

            var.report.save()
            rootPath = '.\\informes'

            if continuar_generacion:
                for file in os.listdir(rootPath):
                    if file.endswith(nombre):
                        os.startfile(os.path.join(rootPath, file))

        except Exception as error:
            print('Error en informe facturas', error)

    def topInformeFactura(titulo):
        """
            Crea la cabecera específica para un informe de factura en formato PDF.

            Este método configura la cabecera específica para un informe de factura en formato PDF, incluyendo el nombre de la empresa,
            el título del informe, la línea de separación, el logo y la información del cliente asociado a la factura.

            Parameters:
            - titulo: Título del informe.

            Returns:
            - None

            """
        try:
            global continuar_generacion

            cif_cliente = var.ui.txtcifcliente.text()

            # Variable booleana para indicar si continuar con la generación del informe
            continuar_generacion = True

            # Validar si el campo CIF del cliente está vacío
            if not cif_cliente:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle('Aviso ')
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText('Debes seleccionar alguna factura.')
                mbox.exec()

                # Establecer la variable para evitar la generación del PDF
                continuar_generacion = False

            if continuar_generacion:
                registro = conexionClientes.ConexionCliente.codigoCliente(cif_cliente)

                fecha = datetime.today()
                fecha = fecha.strftime('%d/%m/%Y')

                # Resto del código...
                logo = '.\IMG\icono.png'
                var.report.line(50, 800, 525, 800)
                var.report.setFont('Helvetica-Bold', size=14)
                var.report.drawString(55, 785, 'Transportes Teis')
                var.report.drawString(240, 670, titulo)
                var.report.line(50, 660, 525, 660)
                var.report.drawImage(logo, 480, 740, width=40, height=35)
                var.report.setFont('Helvetica', size=9)
                var.report.drawString(55, 770, 'CIF:A12345678')
                var.report.drawString(55, 755, 'Avda Galicia - 101')
                var.report.drawString(55, 740, 'Vigo - 36216 - España')
                var.report.drawString(55, 710, 'Telefono: 986123 456')
                var.report.drawString(55, 725, 'e-mail: cartesteis@gmail.com')

                var.report.setFont('Helvetica-Bold', size=9)
                var.report.drawString(290, 785,
                                      f'NÚMERO FACTURA: ' + var.ui.lblNumFac.text() + '        Fecha: ' + fecha)

                var.report.drawString(290, 770, f'CLIENTE')
                var.report.setFont('Helvetica', size=9)
                var.report.drawString(290, 755, f'CIF: ' + str(registro[1]))
                var.report.drawString(290, 740, f'Razón Social: ' + str(registro[3]))
                var.report.drawString(290, 710, f'Dirección: ' + str(registro[4]))
                var.report.drawString(290, 725,
                                      f'Provincia: ' + str(registro[6]) + ' - ' + 'Localidad: ' + str(registro[7]))
                var.report.drawString(290, 695, f'Teléfono: ' + str(registro[5]))

                if not Informes.existeViajeEnFactura(var.ui.lblNumFac.text()):
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle('Aviso ')
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setText('La factura no tiene viajes asociados y no se puede imprimir.')
                    mbox.exec()

                    # Establecer la variable para evitar la generación del PDF
                    continuar_generacion = False


        except Exception as error:
            print('Error en cabecera de informe topinformefactura', error)

    @staticmethod
    def existeViajeEnFactura(numero_factura):
        """
            Comprueba si existe algun viaje en la tabla factura

            Parameters:
            - numero_factura
            Retorna true si encuentra algun viaje y False si no encuentra

            """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('SELECT COUNT(*) FROM viajes WHERE factura = :numero_factura')
            query.bindValue(':numero_factura', numero_factura)

            if query.exec():
                query.next()
                cantidad_viajes = query.value(0)
                return cantidad_viajes > 0
            else:
                return False

        except Exception as error:
            print('Error al verificar viajes asociados:', error)
            return False

    def footInforme(titulo):
        """
            Crea el pie de página para un informe en formato PDF.

            Este método configura el pie de página para un informe en formato PDF, incluyendo una línea de separación,
            la fecha actual, el título del informe y el número de página.

            Parameters:
            - titulo: Título del informe.

            Returns:
            - None

            """
        try:
            var.report.line(50, 50, 525, 50)
            fecha = datetime.today()
            fecha = fecha.strftime('%d-%m-%Y %H:%M:%S')
            var.report.setFont('Helvetica', size=7)
            var.report.drawString(50, 40, str(fecha))
            var.report.drawString(250, 40, str(titulo))
            var.report.drawString(490, 40, str('Página %s' % var.report.getPageNumber()))


        except Exception as error:
            print('Error en pie de informe', error)

    @staticmethod
    def limpiar_cadena_para_conversion(cadena):
        """
        Elimina caracteres no numéricos y convierte la cadena a float.

        Este método toma una cadena como entrada, elimina todos los caracteres no numéricos y convierte la cadena resultante a float.

        Parameters:
        - cadena: Cadena de entrada.

        Returns:
        - float: Valor numérico resultante después de limpiar la cadena.

    """
        solo_digitos = ''.join(caracter for caracter in cadena if caracter.isdigit() or caracter == '.')
        return float(solo_digitos) if solo_digitos else 0.0  # Devolver 0.0 si la cadena está vacía

