import sys
from datetime import datetime

from PyQt6 import QtWidgets, QtCore

import clientes
import drivers
import eventos
import facturas
import var
from calendario import Ui_Calendario
from ventana_acercade import Ui_dlgAbout
from ventana_salir import Ui_dlgSalir


class Calendar(QtWidgets.QDialog):
    def __init__(self):
        super(Calendar, self). __init__()
        var.calendar = Ui_Calendario()
        var.calendar.setupUi(self)
        dia= datetime.now().day
        mes = datetime.now().month
        ano = datetime.now().year
        var.calendar.ventanaCalendario.setSelectedDate((QtCore.QDate(ano,mes,dia)))
        var.calendar.ventanaCalendario.clicked.connect(drivers.Drivers.cargarFecha)
        var.calendar.ventanaCalendario.clicked.connect(clientes.Clientes.cargarFecha)
        var.calendar.ventanaCalendario.clicked.connect(facturas.Facturas.dataFactura)


class Salir(QtWidgets.QDialog):
    def __init__(self):
        super(Salir, self). __init__()
        var.salir = Ui_dlgSalir()
        var.salir.setupUi(self)
        var.salir.btnAceptar.clicked.connect(eventos.Eventos.aceptar)
        var.salir.btnCancelar.clicked.connect(eventos.Eventos.cancelar)


class DlgAcerca(QtWidgets.QDialog):
    def __init__(self):
        super(DlgAcerca, self).__init__()
        var.dlgacerca = Ui_dlgAbout()
        var.dlgacerca.setupUi(self)
        var.dlgacerca.btnAceptar.clicked.connect(eventos.Eventos.cerraracercade)
        var.dlgacerca.lblVersion.setText("Version: " + var.version)

class FileDialogAbrir(QtWidgets.QFileDialog):
    def __init__(self):
        super(FileDialogAbrir, self).__init__()



