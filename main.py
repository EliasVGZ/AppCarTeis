
import clientes, informes
import conexion
import conexionClientes
import drivers
import eventos
import facturas
import informes
import viajes
import tarifas

from venta_principal import *
import sys, var
from calendario import *
from windowaux import Calendar, Salir, DlgAcerca, FileDialogAbrir
import locale
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
locale.setlocale(locale.LC_MONETARY, 'es_ES.UTF-8')

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_VentanaPrincipal()
        var.ui.setupUi(self) #encargado de la interfaz
        var.calendar=Calendar()
        var.salir=Salir()
        var.dlgacercade=DlgAcerca()
        var.dlgabrir = FileDialogAbrir()
        conexion.Conexion.conexion()
        conexionClientes.ConexionCliente.conexion()
        conexion.Conexion.cargarFacturas()

        #cargar provincias
        conexion.Conexion.cargar_provincias(var.ui.cmbProvincia)#Carga provincias en driver
        conexion.Conexion.cargar_provincias(var.ui.cmbProvinciaCliente)#carga provincias en clientes
        conexion.Conexion.cargar_provincias(var.ui.cmbOrigenProvFac)  # carga provincias en origen facturas
        conexion.Conexion.cargar_provincias(var.ui.cmbDestinoProvFac)  # carga provincias en destino facturas


        conexion.Conexion.mostrarDrivers(self)
        conexionClientes.ConexionCliente.mostrarClientes(self)

        facturas.Facturas.cargadrivers(self)
        viajes.Viajes.datosViaje(self)

        estado = 1
        conexion.Conexion.selectDrivers(estado)#PARA QUE AL COMENZAR EL PRO ME MUESTRE LOS DE ALTA
        conexionClientes.ConexionCliente.selectClientes(estado)

        """ZONA EXAMEN"""
        tarifas.Tarifas.mostrarTarifa(self)
        var.ui.btnModificarTarifa.clicked.connect(tarifas.Tarifas.modificarTarifas)
        var.ui.actionListado_Viaje_Clientes.triggered.connect(informes.Informes.mostrarViajesCliente)
        var.ui.txtCorreo.editingFinished.connect(lambda: clientes.Clientes.validarArroba(var.ui.txtCorreo.text()))#todo metodo para que valide que el corre tiene @
        tarifas.Tarifas.mostrarTarifa(self)#todo metodo para actualizar la tabla tarifafa
        tarifas.Tarifas.resizeTabTarifa(self)
        var.ui.tabTarifas.clicked.connect(tarifas.Tarifas.cargaTarifaInterfaz)




        """ZONA DE EVENTOS DEL BOTON"""

        var.ui.btnCalendario.clicked.connect(eventos.Eventos.abrirCalendario) #abrir calendario al clickearlo
        var.ui.btnCalendarioCliente.clicked.connect(eventos.Eventos.abrirCalendario)#ABRIR CALENDARIO EN CLIENTES
        var.ui.btnAltaDriver.clicked.connect(drivers.Drivers.altaDriver) #alta driver al darle click
        var.ui.btnBuscarDriver.clicked.connect(drivers.Drivers.buscarDriverLupa)
        var.ui.btnModifDriver.clicked.connect(drivers.Drivers.modificarDriver)
        var.ui.btnBajaDriver.clicked.connect(drivers.Drivers.borrarDriver)
        var.ui.btnBuscarCliente.clicked.connect(clientes.Clientes.buscarClienteLupa)

        """ZONA DE FACTURAS"""
        var.ui.btnBuscarClienteFac.clicked.connect(facturas.Facturas.buscarFacturasCliente)
        var.ui.btnCalendarioFac.clicked.connect(facturas.Facturas.abrirCalendarioFac)
        var.ui.btnFacturar.clicked.connect(facturas.Facturas.altaFactura)

        """ZONA VIAJES"""
        var.ui.btnGrabarViaje.clicked.connect(viajes.Viajes.cargarLineaVenta)
        var.ui.btnModificar.clicked.connect(viajes.Viajes.modificarViaje)


        """ZONA DE EVENTOS DEL BOTON DEL EXAMEN"""
        var.ui.btnAltaCliente.clicked.connect(clientes.Clientes.altaCliente)
        var.ui.btnBajaCliente.clicked.connect(clientes.Clientes.borrarCliente)
        var.ui.btnModifCliente.clicked.connect(clientes.Clientes.modificaCliente)



        """ ZONA DE EVENTOS DEL MENU BAR"""

        var.ui.actionSalir.triggered.connect(eventos.Eventos.salir)
        var.ui.actAcerca_de.triggered.connect(eventos.Eventos.acercade)
        var.ui.actionCrear_Copia_Seguridad.triggered.connect(eventos.Eventos.crearBackUp)#Herramienta
        var.ui.actionRestaurar_Copia_Seguridad.triggered.connect(eventos.Eventos.restaurarBackUp)#Herramienta
        var.ui.actionExportar_Datos_xls.triggered.connect(eventos.Eventos.exportarDatosXls)#Herramienta
        var.ui.actionImportar_Datos_XLS.triggered.connect(eventos.Eventos.importardatosxls)

        """ZONA INFORMES"""
        var.ui.actionImportar_Datos_Clientes_XLS.triggered.connect(eventos.Eventos.importardatosclientesxls)
        var.ui.actionExportar_Datos_Clientes_XLS.triggered.connect(eventos.Eventos.exportarDatosClientesXls)
        """LLAMADA A LOS INFORMES DE CLIENTES Y CONDUCTORES"""
        var.ui.actionListado_Clientes.triggered.connect(informes.Informes.reportclientes)
        var.ui.actionListado_Conductors.triggered.connect(informes.Informes.reportconductores)
        var.ui.actionInforme.triggered.connect(informes.Informes.elegirinforme)
        var.ui.actionFacturar.triggered.connect(informes.Informes.reportfacturas)


        """ZONA DE EVENTOS DE LA CAJAS DE TEXTO"""
        var.ui.txtDni.editingFinished.connect(lambda: drivers.Drivers.validarDni(var.ui.txtDni.text()))  #cuando estás escribiendo y salgas, ejecuta ese evento
        var.ui.txtMovil.editingFinished.connect(drivers.Drivers.validarMovil) #valida que el movil tiene 9 digitos
        var.ui.txtSalario.editingFinished.connect(drivers.Drivers.validarSalario)

        """ZONA DE EVENTOS DE LA CAJAS DE TEXTO del EXAMEN"""
        var.ui.txtTelefono.editingFinished.connect(clientes.Clientes.validarTelefono)
        var.ui.txtDni2.editingFinished.connect(lambda: clientes.Clientes.validarDni(var.ui.txtDni2.text()))

        var.ui.txtNombre.editingFinished.connect(eventos.Eventos.formatCajaTexto)
        var.ui.txtApellido.editingFinished.connect(eventos.Eventos.formatCajaTexto)
        var.ui.txtSalario.editingFinished.connect(eventos.Eventos.formatCajaTexto)

        var.ui.txtDni2.editingFinished.connect(eventos.Eventos.formatCajaTexto)
        var.ui.txt_razonSocial.editingFinished.connect(eventos.Eventos.formatCajaTexto)
        var.ui.txtDireccionCliente.editingFinished.connect(eventos.Eventos.formatCajaTexto)

        """EVENTOS DEl TOOL BAR"""
        var.ui.actionbarSalir.triggered.connect(eventos.Eventos.salir)
        var.ui.actionlimpiarPanel.triggered.connect(drivers.Drivers.limpiarPanel)
        var.ui.actioncrearCopia.triggered.connect(eventos.Eventos.crearBackUp)#llamada al icono
        var.ui.actionrestaurarCopia.triggered.connect(eventos.Eventos.restaurarBackUp)#llamada al icono


        """EXAMEN! EVENTOS DEl TOOL BAR"""
        var.ui.actionlimpiarPanel.triggered.connect(clientes.Clientes.limpiarPanelCliente)
        var.ui.actionlimpiarPanel.triggered.connect(facturas.Facturas.limpiarPanelFacturas)
        var.ui.btn_limpiar_viaje.clicked.connect(viajes.Viajes.limpiarPanelViaje)


        """EVENTOS DE TABLAS"""

        eventos.Eventos.resizeTabDrivers(self)
        eventos.Eventos.resizeTabFacturas(self) #TODO REDIMENSIONAR LA TABLA FACTURAS

        var.ui.tabClientes.clicked.connect(clientes.Clientes.cargaCliente)
        var.ui.tabDrivers.clicked.connect(drivers.Drivers.cargaDriver)
        var.ui.tabFacturas.clicked.connect(facturas.Facturas.cargaFactura)
        var.ui.tabViajes.clicked.connect(viajes.Viajes.cargaViaje)

        """EVENTOS DE TABLAS EXAMEN"""
        eventos.Eventos.resizeTabClientes(self)


        """EVENTOS COMBOBOX"""
        var.ui.cmbProvincia.currentIndexChanged.connect(conexion.Conexion.selMuni)
        var.ui.buttonGroup.buttonClicked.connect(drivers.Drivers.selEstado)

        var.ui.cmbOrigenProvFac.currentIndexChanged.connect(viajes.Viajes.selMuniviajeorigen)
        var.ui.cmbDestinoProvFac.currentIndexChanged.connect(viajes.Viajes.selMuniviajedestino)
        #SE CAMBIAR LA TARIFA SEGUN EL MUNCIPIO SELECCIONADO
        var.ui.cmbOrigenLocFac.currentIndexChanged.connect(viajes.Viajes.datosViaje)
        var.ui.cmbDestinoLocFac.currentIndexChanged.connect(viajes.Viajes.datosViaje)

        var.ui.buttonGroupCliente.buttonClicked.connect(clientes.Clientes.selEstadoCliente)
        var.ui.cmbProvinciaCliente.currentIndexChanged.connect(conexionClientes.ConexionCliente.selMuni)



        """DIFERENTES EVENTOS AL CARGAR EL PROGRAMA"""
        eventos.Eventos.cargarstatusbar(self)




    def closeEvent(self, event):
        mbox = QtWidgets.QMessageBox()
        mbox.setWindowTitle('Confirmar Salida')
        mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
        mbox.setText('¿Está seguro de que desea salir?')
        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        mbox.button(QtWidgets.QMessageBox.StandardButton.Yes).setText('Si')
        mbox.button(QtWidgets.QMessageBox.StandardButton.No).setText('No')
        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Yes)
        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)

        if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
            event.accept()
            #sys.exit()
        else:
            event.ignore()
            #mbox.hide()




if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())


