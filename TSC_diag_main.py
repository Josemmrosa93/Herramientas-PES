from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QProgressBar,
    QHeaderView,
    QLabel,
    QFileDialog,
    QMessageBox,
    QScrollArea,
    QFormLayout,
    QPushButton,
    QDialog,
    QTextEdit,
    QMenu,
    QStyleFactory,
    QSplitter,
    QListWidget, 
    QStackedWidget,
    QDialogButtonBox,
    QLineEdit,
    QCheckBox,
    QSpinBox,
    QHeaderView,
    QGridLayout,
    QPlainTextEdit,
    QFrame,
    QSlider,
)
from PySide6.QtGui import (
    QAction,
    QPixmap,
    QPainter,
    QColor,
    QImage,
    QBrush,
)
from PySide6.QtCore import (
    Qt,
    QThread,
    Signal,
    QTimer,
    QObject,
    QRectF,
    QEvent,
)
from xml.etree.ElementTree import ( 
    Element,
    SubElement,
    tostring
)
from PySide6.QtSvgWidgets import QSvgWidget
from pathlib import Path
import urllib.request
import json
import datetime
import webbrowser
import subprocess
import platform
import re
import sys
import os
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Event, RLock
from numpy import array_split, concatenate
import time
import xlsxwriter
import pandas as pd
import math
import copy
from isagrafInterface import isagrafInterface
from weasyprint import HTML as WPHtml


APP_VERSION = "1.0.3"
DEV_MODE = True  # True → lazo de puertas con datos simulados, sin conexión al tren
GITHUB_OWNER = "Josemmrosa93"
GITHUB_REPO = "Herramientas-PES"

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "general":{
        "ping_timeout": 200,
    },  
    "massive_ping":{
        "ping_count": "1",
        "max_threads": "21",
        "auto_export": True,        
    }
}

class TCMS_vars:
    def __init__(self):
        
        #TIPOS DE COCHE EN FUNCIÓN DEL PROYECTO
        self.COACH_TYPES_DB={1: "L9215", 2: "C4340", 3: "C4301", 4: "C4306", 5: "C4314", 6: "C4315", 7: "C4322", 8: "C4302S", 9: "C4302P", 10: "C4302C", 11: "C4328"}
        self.COACH_TYPES_DSB={2: "C4740", 3: "C4701", 5: "C4714", 8: "C4702S", 9: "C4702P", 11: "C4728"}
        #VARIABLE DE TCMS QUE INDICA EL TIPO DE COCHE
        self.COACH_TYPE = ['oVCUCH_TRDP_DS_A000.COM_Vehicle_Type']
        #VARIABLES DEL LAZO DE SEGURIDAD, INCLUYENDO LAS DEL PMR
        self.TSC_COACH_VARS_DSB = [
        'iVCUCH_IO_DS_A602_S45_X1.DIu_RiomS1isOK',
        'iVCUCH_IO_DS_A602_S45_X1.DIu_SafCon1Loop',
        'iVCUCH_IO_DS_A602_S45_X1.DIu_SafCon2Loop',
        'iVCUCH_IO_DS_A602_S42_X1.DIu_RiomS1isOKB1',
        'iVCUCH_IO_DS_A602_S43_X1.DIu_SafCon1LoopB1',
        'iVCUCH_IO_DS_A602_S43_X1.DIu_SafCon2LoopB1',
        'iVCUCH_IO_DS_A602_S46_X1.DIu_STCMSBypass',
        'iVCUCH_IO_DS_A602_S42_X1.DIu_EmBrakValvsOpen',
        'iVCUCH_IO_DS_A602_S46_X1.DIu_SIFA1Cond',
        'iVCUCH_IO_DS_A602_S46_X1.DIu_SIFA2Cond',
        'iVCUCH_IO_DS_A602_S45_X1.DIu_BypCoachActiv',
        'iVCUCH_IO_DS_A602_S45_X1.DIu_BypPRMActiv',
        'iVCUCH_IO_DS_A602_S46_X1.DIu_SafBypasLoopOff',
        'RIOMSC1_MVB1_DS_2EA.DigitalInput10', #S60 PRINCIPAL
        'RIOMSC1r_MVB2_DS_2EA.DigitalInput10', #S60 REDUNDANTE
        'RIOMSC1_MVB1_DS_2EA.DigitalInput11', #S62 PRINCIPAL
        'RIOMSC1r_MVB2_DS_2EA.DigitalInput11', #S62 REDUNDANTE
        'RIOMSC1_MVB1_DS_2EA.DigitalInput4', #S256 PRINCIPAL
        'RIOMSC1r_MVB2_DS_2EA.DigitalInput4', #S256 REDUNDANTE
        'RIOMSC1_MVB1_DS_2EA.DigitalInput3', #S255 PRINCIPAL
        'RIOMSC1r_MVB2_DS_2EA.DigitalInput3', #S255 REDUNDANTE
        'RIOMSC1_MVB1_DS_2E7_Failure_Rate', #Tasa de fallos RIOM 1 Principal
        'RIOMSC1r_MVB2_DS_2E7_Failure_Rate', #Tasa de fallos RIOM 1 Redundante
        'RIOMSC2_MVB1_DS_2FB_Failure_Rate', #Tasa de fallos RIOM 2 Principal (sólo PMR)
        'RIOMSC2r_MVB2_DS_2FB_Failure_Rate', #Tasa de fallos RIOM 2 Redundante (sólo PMR)
        'RIOMSC2_MVB1_DS_2FE.DigitalInput10', #S60 PRINCIPAL
        'RIOMSC2r_MVB2_DS_2FE.DigitalInput10', #S60 REDUNDANTE
        'RIOMSC2_MVB1_DS_2FE.DigitalInput11', #S62 PRINCIPAL
        'RIOMSC2r_MVB2_DS_2FE.DigitalInput11', #S62 REDUNDANTE
        'RIOMSC2_MVB1_DS_2FE.DigitalInput4', #S256 PRINCIPAL
        'RIOMSC2r_MVB2_DS_2FE.DigitalInput4', #S256 REDUNDANTE
        ]
        self.TSC_COACH_VARS_DB = [
        'iVCUCH_IO_DS_A602_S45_X1.DIu_RiomS1isOK',
        'iVCUCH_IO_DS_A602_S45_X1.DIu_SafCon1Loop',
        'iVCUCH_IO_DS_A602_S45_X1.DIu_SafCon2Loop',
        'iVCUCH_IO_DS_A602_S42_X1.DIu_RiomS1isOKB1',
        'iVCUCH_IO_DS_A602_S43_X1.DIu_SafCon1LoopB1',
        '_INPUT_LAYER.BRK_TST_F_Emg_Brk.iIO_DS_A602_S43_X1_DIu_SafCon2Loop_B1',
        'iVCUCH_IO_DS_A602_S45_X1.DIu_BypCoachActiv',
        'iVCUCH_IO_DS_A602_S45_X1.DIu_BypPRMActiv',
        'RIOMSC1_MVB1_DS_2EA.DigitalInput10', #S60 PRINCIPAL
        'RIOMSC1r_MVB2_DS_2EA.DigitalInput10', #S60 REDUNDANTE
        'RIOMSC1_MVB1_DS_2EA.DigitalInput11', #S62 PRINCIPAL
        'RIOMSC1r_MVB2_DS_2EA.DigitalInput11', #S62 REDUNDANTE
        'RIOMSC1_MVB1_DS_2EA.DigitalInput4', #S256 PRINCIPAL
        'RIOMSC1r_MVB2_DS_2EA.DigitalInput4', #S256 REDUNDANTE
        'RIOMSC1_MVB1_DS_2EA.DigitalInput3', #S255 PRINCIPAL
        'RIOMSC1r_MVB2_DS_2EA.DigitalInput3', #S255 REDUNDANTE
        'RIOMSC1_MVB1_DS_2E7_Failure_Rate', #Tasa de fallos RIOM 1 Principal
        'RIOMSC1r_MVB2_DS_2E7_Failure_Rate', #Tasa de fallos RIOM 1 Redundante
        'RIOMSC2_MVB1_DS_2FB_Failure_Rate', #Tasa de fallos RIOM 2 Principal (sólo PMR)
        'RIOMSC2r_MVB2_DS_2FB_Failure_Rate', #Tasa de fallos RIOM 2 Redundante (sólo PMR)
        'RIOMSC2_MVB1_DS_2FE.DigitalInput10', #S60 PRINCIPAL (sólo PMR)
        'RIOMSC2r_MVB2_DS_2FE.DigitalInput10', #S60 REDUNDANTE (sólo PMR)
        'RIOMSC2_MVB1_DS_2FE.DigitalInput11', #S62 PRINCIPAL (sólo PMR)
        'RIOMSC2r_MVB2_DS_2FE.DigitalInput11', #S62 REDUNDANTE (sólo PMR)
        'RIOMSC2_MVB1_DS_2FE.DigitalInput4', #S256 PRINCIPAL (sólo PMR)
        'RIOMSC2r_MVB2_DS_2FE.DigitalInput4', #S256 REDUNDANTE (sólo PMR)
        ]
        self.TSC_CC_VARS_DB = [
        'RIOMPUP1_MVB1_DS_17D.DIp_BrakeHandlEmer1', #S8
        'RIOMPUP1r_MVB2_DS_17D.DIs_BrakeHandlEmer1', #S8
        'RIOMPUP1_MVB1_DS_17D.DIp_PushEmerg1', #S6
        'RIOMPUP1r_MVB2_DS_17D.DIs_PushEmerg1', #S6
        'RIOMPUP1r_MVB2_DS_17D.DIu_LatHandEmBrkRq1', #S10
        'VCUS_MVB1_DS_CB.OccupiedCab1', #K1
        'RIOMCAB1_MVB1_DS_193.DIu_ActiveCabin1', #K80
        'RIOMCAB1r_MVB2_DS_193.DIu_ActiveCabin2', #K81
        'VCUS_MVB1_DS_CB.EmBrakValve1Opened', #K82
        'VCUS_MVB1_DS_CB.EmBrakValve2Opened', #K83
        'RIOMCAB1_MVB1_DS_193.DIu_SIFA1Cond', #SIFA 1 COND
        'RIOMCAB1r_MVB2_DS_193.DIu_SIFA2Cond', #SIFA 1 COND
        'RIOMCAB1_MVB1_DS_193.DIu_ETCSIsolated', #S700
        'RIOMCAB1r_MVB2_DS_193.DIu_ATBIsolated', #S701
        'RIOMCAB1r_MVB2_DS_193.DIu_CMDIsolated', #S702
        'RIOMCAB1_MVB1_DS_193.DIu_TELOCHMOFF', #S703
        'RIOMCAB1_MVB1_DS_193.DIu_PZBLZBIsolated', #S704
        'RIOMCAB1_MVB1_DS_192.DIu_ETCSRelay1Open', #K700
        'RIOMCAB1_MVB1_DS_191.DIu_ETCSRelay2Open', #K701
        'RIOMAT_MVB1_DS_12F.DIu_ATBRelay1Open', #K710
        'RIOMAT_MVB1_DS_12F.DIu_ATBRelay2Open', #K711
        'EVC_MVB1_DS_7D5.ATB_EB_INH', #K708/K709
        'RIOMAT_MVB1_DS_12F.DIu_HMRelay1Open', #K731
        'RIOMAT_MVB1_DS_12F.DIu_HMRelay2Open', #K732
        'RIOMCAB1_MVB1_DS_193.DIu_LZBRelay1Open', #K740
        'RIOMCAB2_MVB1_DS_1A7.DIu_LZBRelay2Open', #K741
        'RIOMCAB1_MVB1_DS_193.DIp_STCMSBypass', #S25
        'RIOMCAB1r_MVB2_DS_193.DIs_STCMSBypass', #S25
        'RIOMCAB1_MVB1_DS_191.DIu_SafBypasLoopOff', #K753
                            ]
                
        #DESCRIPCIONES FILTRADAS DE ERRORES DE TAR, VELOCIDAD Y TEMPERATURAS DE RODAMIENTOS
        self.filtered_TSC_DIAG_NAMES=[
        "TAR 1 indisponible",
        "TAR 2 indisponible", 
        "TAR 3 indisponible",
        "TAR 4 indisponible",
        "Sensor de rueda 1 indisponible",
        "Sensor de rueda 2 indisponible",
        "Sensor de rueda 3 indisponible",
        "Sensor de rueda 4 indisponible",  
        "Temperatura rodamiento interior izquierdo (SC1 MVB1) no disponible",
        "Temperatura rodamiento interior izquierdo (SC1r MVB2) no disponible",
        "Temperatura rodamiento exterior izquierdo (SC1 MVB1) no disponible",
        "Temperatura rodamiento exterior izquierdo (SC1r MVB2) no disponible",
        "Temperatura rodamiento interior derecho (SC1 MVB1) no disponible",
        "Temperatura rodamiento interior derecho (SC1r MVB2) no disponible",
        "Temperatura rodamiento exterior derecho (SC1 MVB1) no disponible",
        "Temperatura rodamiento exterior derecho (SC1r MVB2) no disponible",
        "Temperatura rodamiento interior izquierdo eje B1 (SC2 MVB1) no disponible",
        "Temperatura rodamiento interior izquierdo eje B1 (SC2r MVB2) no disponible",
        "Temperatura rodamiento exterior izquierdo eje B1 (SC2 MVB1) no disponible",
        "Temperatura rodamiento exterior izquierdo eje B1 (SC2r MVB2) no disponible",
        "Temperatura rodamiento interior derecho eje B1 (SC2 MVB1) no disponible",
        "Temperatura rodamiento interior derecho eje B1 (SC2r MVB2) no disponible",
        "Temperatura rodamiento exterior derecho eje B1 (SC2 MVB1) no disponible",
        "Temperatura rodamiento exterior derecho eje B1 (SC2r MVB2) no disponible",  
        "Fallo tarjeta HSA RIOM 1",
        "Fallo tarjeta HSA RIOM 1r",
        "Fallo tarjeta HSA RIOM 2",
        "Fallo tarjeta HSA RIOM 2r",
        "Fallo tarjetas DIO RIOM 1",
        "Fallo tarjetas DIO RIOM 1r",
        "Fallo tarjetas DIO RIOM 2",
        "Fallo tarjetas DIO RIOM 2r",
        ]
        #VARIABLES PARA LA DIAGNÓSIS DE APERTURA (TEMPERATURA DE RODAMIENTOS, TAR Y DIAGNÓSIS DE FRENO)
        self.TSC_DIAG_VARS = [
        'RIOMSC1_MVB1_DS_2E8.InstabUnavail', #INDISPONIBILIDAD DE TAR
        'RIOMSC1r_MVB2_DS_2E8.InstabUnavail',
        'RIOMSC2_MVB1_DS_2FC.InstabUnavail',
        'RIOMSC2r_MVB2_DS_2FC.InstabUnavail',
        'RIOMSC1_MVB1_DS_2E8.SpeedUnav', #INDISPONIBILIDAD DE SENSORES DE RUEDA
        'RIOMSC1r_MVB2_DS_2E8.SpeedUnav',
        'RIOMSC2_MVB1_DS_2FC.SpeedUnav',
        'RIOMSC2r_MVB2_DS_2FC.SpeedUnav',
        'RIOMSC1_MVB1_DS_2E8.TempUnavailBear1', #INDISPONIBILIDAD DE TEMPERATURA DE RODAMIENTOS
        'RIOMSC1r_MVB2_DS_2E8.TempUnavailBear1',
        'RIOMSC1_MVB1_DS_2E8.TempUnavailBear2',
        'RIOMSC1r_MVB2_DS_2E8.TempUnavailBear2',
        'RIOMSC1_MVB1_DS_2E8.TempUnavailBear3',
        'RIOMSC1r_MVB2_DS_2E8.TempUnavailBear3',
        'RIOMSC1_MVB1_DS_2E8.TempUnavailBear4',
        'RIOMSC1r_MVB2_DS_2E8.TempUnavailBear4',
        'RIOMSC2_MVB1_DS_2FC.TempUnavailBear1',
        'RIOMSC2r_MVB2_DS_2FC.TempUnavailBear1',
        'RIOMSC2_MVB1_DS_2FC.TempUnavailBear2',
        'RIOMSC2r_MVB2_DS_2FC.TempUnavailBear2',
        'RIOMSC2_MVB1_DS_2FC.TempUnavailBear3',
        'RIOMSC2r_MVB2_DS_2FC.TempUnavailBear3',
        'RIOMSC2_MVB1_DS_2FC.TempUnavailBear4',
        'RIOMSC2r_MVB2_DS_2FC.TempUnavailBear4',
        'RIOMSC1_MVB1_DS_2E8.RiomFailureHSA1', #FALLA TARJETA HSA RIOM 1
        'RIOMSC1r_MVB2_DS_2E8.RiomFailureHSA1', #FALLA TARJETA HSA RIOM 1r
        'RIOMSC2_MVB1_DS_2FC.RiomFailureHSA1', #FALLA TARJETA HSA RIOM 2
        'RIOMSC2r_MVB2_DS_2FC.RiomFailureHSA1', #FALLA TARJETA HSA RIOM 2r
        'RIOMSC1_MVB1_DS_2E9.RiomFailureDIO', #FALLA TARJETA DIO RIOM 1
        'RIOMSC1r_MVB2_DS_2E9.RiomFailureDIO', #FALLA TARJETA DIO RIOM 1r
        'RIOMSC2_MVB1_DS_2FD.RiomFailureDIO', #FALLA TARJETA DIO RIOM 2
        'RIOMSC2r_MVB2_DS_2FD.RiomFailureDIO', #FALLA TARJETA DIO RIOM 2r
        ]
        self.TSC_DIAG_VARS_OLD = [
        'RIOMSC1_MVB1_DS_2E8.AvTempBear1', #TEMPERATURA 1
        'RIOMSC1r_MVB2_DS_2E8.AvTempBear1',
        'RIOMSC1_MVB1_DS_2E8.AvTempBear2',
        'RIOMSC1r_MVB2_DS_2E8.AvTempBear2',
        'RIOMSC1_MVB1_DS_2E8.AvTempBear3',
        'RIOMSC1r_MVB2_DS_2E8.AvTempBear3',
        'RIOMSC1_MVB1_DS_2E8.AvTempBear4',
        'RIOMSC1r_MVB2_DS_2E8.AvTempBear4', #TEMPERATURA 8
        'RIOMSC2_MVB1_DS_2FC.AvTempBear1',
        'RIOMSC2r_MVB2_DS_2FC.AvTempBear1',
        'RIOMSC2_MVB1_DS_2FC.AvTempBear2',
        'RIOMSC2r_MVB2_DS_2FC.AvTempBear2',
        'RIOMSC2_MVB1_DS_2FC.AvTempBear3',
        'RIOMSC2r_MVB2_DS_2FC.AvTempBear3',
        'RIOMSC2_MVB1_DS_2FC.AvTempBear4',
        'RIOMSC2r_MVB2_DS_2FC.AvTempBear4', #TEMPERATURA 16 (SÓLO EN COCHE DE DOBLE EJE)
        'RIOMSC1_MVB1_DS_2E8.AccelerationRms', #TAR 1
        'RIOMSC1r_MVB2_DS_2E8.AccelerationRms',
        'RIOMSC2_MVB1_DS_2FC.AccelerationRms',
        'RIOMSC2r_MVB2_DS_2FC.AccelerationRms', #TAR 4 (SÓLO EN COCHE DE DOBLE EJE)
        'RIOMSC1_MVB1_DS_2E8.InstabUnavail', #INDISPONIBILIDAD DE TAR
        'RIOMSC1r_MVB2_DS_2E8.InstabUnavail',
        'RIOMSC2_MVB1_DS_2FC.InstabUnavail',
        'RIOMSC2r_MVB2_DS_2FC.InstabUnavail',
        'VCUCH_MVB2_DS_6E.uSpeedRef', #VELOCIDAD DE REFERENCIA
        'RIOMSC1_MVB1_DS_2E8.SpeedUnav', #INDISPONIBILIDAD DE SENSORES DE RUEDA
        'RIOMSC1r_MVB2_DS_2E8.SpeedUnav',
        'RIOMSC2_MVB1_DS_2FC.SpeedUnav',
        'RIOMSC2r_MVB2_DS_2FC.SpeedUnav',
        'VCUCH_MVB1_DS_30D.bPBA_Speed', #FRENO DE ESTACIONAMIENTO APLICADO CON VELOCIDAD
        'BCUCH1_MVB2_DS_30F.bPB_Status', #ESTADO DEL FRENO DE ESTACIONAMIENTO
        'RIOMSC1_MVB1_DS_2E8.TempUnavailBear1', #INDISPONIBILIDAD DE TEMPERATURA DE RODAMIENTOS
        'RIOMSC1r_MVB2_DS_2E8.TempUnavailBear1',
        'RIOMSC1_MVB1_DS_2E8.TempUnavailBear2',
        'RIOMSC1r_MVB2_DS_2E8.TempUnavailBear2',
        'RIOMSC1_MVB1_DS_2E8.TempUnavailBear3',
        'RIOMSC1r_MVB2_DS_2E8.TempUnavailBear3',
        'RIOMSC1_MVB1_DS_2E8.TempUnavailBear4',
        'RIOMSC1r_MVB2_DS_2E8.TempUnavailBear4',
        'RIOMSC2_MVB1_DS_2FC.TempUnavailBear1',
        'RIOMSC2r_MVB2_DS_2FC.TempUnavailBear1',
        'RIOMSC2_MVB1_DS_2FC.TempUnavailBear2',
        'RIOMSC2r_MVB2_DS_2FC.TempUnavailBear2',
        'RIOMSC2_MVB1_DS_2FC.TempUnavailBear3',
        'RIOMSC2r_MVB2_DS_2FC.TempUnavailBear3',
        'RIOMSC2_MVB1_DS_2FC.TempUnavailBear4',
        'RIOMSC2r_MVB2_DS_2FC.TempUnavailBear4',
        'RIOMSC1_MVB1_DS_2E8.RiomFailureHSA1', #FALLA TARJETA HSA RIOM 1
        'RIOMSC1r_MVB2_DS_2E8.RiomFailureHSA1', #FALLA TARJETA HSA RIOM 1r
        'RIOMSC2_MVB1_DS_2FC.RiomFailureHSA1', #FALLA TARJETA HSA RIOM 2
        'RIOMSC2r_MVB2_DS_2FC.RiomFailureHSA1', #FALLA TARJETA HSA RIOM 2r
        'RIOMSC1_MVB1_DS_2E9.RiomFailureDIO', #FALLA TARJETA DIO RIOM 1
        'RIOMSC1r_MVB2_DS_2E9.RiomFailureDIO', #FALLA TARJETA DIO RIOM 1r
        'RIOMSC2_MVB1_DS_2FD.RiomFailureDIO', #FALLA TARJETA DIO RIOM 2
        'RIOMSC2r_MVB2_DS_2FD.RiomFailureDIO', #FALLA TARJETA DIO RIOM 2r
        ]
        #NOMBRES DE LAS TEMPERATURAS DE RODAMIENTO DE RODAL Y BOGIE
        self.BEARING_NAMES = [
        "Rodamiento interior rueda izquierda RIOM SC (B100)",
        "Rodamiento interior rueda izquierda RIOM SCr (B101)",
        "Rodamiento exterior rueda izquierda RIOM SC (B102)",
        "Rodamiento exterior rueda izquierda RIOM SCr (B103)",
        "Rodamiento interior rueda derecha RIOM SC (B110)",
        "Rodamiento interior rueda derecha RIOM SCr (B111)",
        "Rodamiento exterior rueda derecha RIOM SC (B112)",
        "Rodamiento exterior rueda derecha RIOM SCr (B113)",
        "Rodamiento interior rueda izquierda RIOM SC B1 (B100)",
        "Rodamiento interior rueda izquierda RIOM SCr B1 (B101)",
        "Rodamiento exterior rueda izquierda RIOM SC B1 (B102)",
        "Rodamiento exterior rueda izquierda RIOM SCr B1 (B103)",
        "Rodamiento interior rueda derecha RIOM SC B1 (B110)",
        "Rodamiento interior rueda derecha RIOM SCr B1 (B111)",
        "Rodamiento exterior rueda derecha RIOM SC B1 (B112)",
        "Rodamiento exterior rueda derecha RIOM SCr B1 (B113)"
        ]
        #NOMBRES DE LAS INDISPONIBILIDADES DE TEMPERATURAS DE RODAMIENTO
        self.TEMP_UNAV_NAMES = [
        "Temperatura rodamiento interior izquierdo (SC1 MVB1) no disponible",
        "Temperatura rodamiento interior izquierdo (SC1r MVB2) no disponible",
        "Temperatura rodamiento exterior izquierdo (SC1 MVB1) no disponible",
        "Temperatura rodamiento exterior izquierdo (SC1r MVB2) no disponible",
        "Temperatura rodamiento interior derecho (SC1 MVB1) no disponible",
        "Temperatura rodamiento interior derecho (SC1r MVB2) no disponible",
        "Temperatura rodamiento exterior derecho (SC1 MVB1) no disponible",
        "Temperatura rodamiento exterior derecho (SC1r MVB2) no disponible",
        "Temperatura rodamiento interior izquierdo eje B1 (SC2 MVB1) no disponible",
        "Temperatura rodamiento interior izquierdo eje B1 (SC2r MVB2) no disponible",
        "Temperatura rodamiento exterior izquierdo eje B1 (SC2 MVB1) no disponible",
        "Temperatura rodamiento exterior izquierdo eje B1 (SC2r MVB2) no disponible",
        "Temperatura rodamiento interior derecho eje B1 (SC2 MVB1) no disponible",
        "Temperatura rodamiento interior derecho eje B1 (SC2r MVB2) no disponible",
        "Temperatura rodamiento exterior derecho eje B1 (SC2 MVB1) no disponible",
        "Temperatura rodamiento exterior derecho eje B1 (SC2r MVB2) no disponible",
        ]
        #NOMBRES DE LOS TAR
        self.TAR_NAMES = [
        "TAR 1 Eje 1",
        "TAR 2 Eje 1",
        "TAR 1 Eje 2",
        "TAR 2 Eje 2"] 
        #NOMBRES DE LAS INDISPONIBILIDADES DE TAR
        self.TAR_UNAV_NAMES = [
        "Indisponibilidad de inestabilidad 1 (TAR indisponible)",
        "Indisponibilidad de inestabilidad 2 (TAR indisponible)", 
        "Indisponibilidad de inestabilidad 3 (TAR indisponible)", 
        "Indisponibilidad de inestabilidad 4 (TAR indisponible)"
        ]
        #VARIABLES PARA LA DIAGNÓSIS DE BCU
        self.BCU_DIAGNOSIS = [
        'BCUCH1_MVB2_DS_311.sDiagnosis01_b1',
        'BCUCH1_MVB2_DS_311.sDiagnosis01_b2', 
        'BCUCH1_MVB2_DS_311.sDiagnosis01_b3', 
        'BCUCH1_MVB2_DS_311.sDiagnosis01_b4', 
        'BCUCH1_MVB2_DS_311.sDiagnosis01_b5', 
        'BCUCH1_MVB2_DS_311.sDiagnosis01_b6', 
        'BCUCH1_MVB2_DS_311.sDiagnosis01_b7', 
        'BCUCH1_MVB2_DS_311.sDiagnosis02_b0', 
        'BCUCH1_MVB2_DS_311.sDiagnosis02_b1', 
        'BCUCH1_MVB2_DS_311.sDiagnosis02_b2', 
        'BCUCH1_MVB2_DS_311.sDiagnosis02_b3', 
        'BCUCH1_MVB2_DS_311.sDiagnosis02_b4', 
        'BCUCH1_MVB2_DS_311.sDiagnosis02_b5', 
        'BCUCH1_MVB2_DS_311.sDiagnosis02_b6', 
        'BCUCH1_MVB2_DS_311.sDiagnosis02_b7', 
        'BCUCH1_MVB2_DS_311.sDiagnosis03_b0', 
        'BCUCH1_MVB2_DS_311.sDiagnosis03_b1', 
        'BCUCH1_MVB2_DS_311.sDiagnosis03_b2', 
        'BCUCH1_MVB2_DS_311.sDiagnosis03_b3', 
        'BCUCH1_MVB2_DS_311.sDiagnosis03_b4', 
        'BCUCH1_MVB2_DS_311.sDiagnosis03_b6', 
        'BCUCH1_MVB2_DS_311.sDiagnosis03_b7', 
        'BCUCH1_MVB2_DS_311.sDiagnosis04_b0', 
        'BCUCH1_MVB2_DS_311.sDiagnosis04_b1', 
        'BCUCH1_MVB2_DS_311.sDiagnosis04_b2', 
        'BCUCH1_MVB2_DS_311.sDiagnosis04_b3', 
        'BCUCH1_MVB2_DS_311.sDiagnosis04_b4', 
        'BCUCH1_MVB2_DS_311.sDiagnosis04_b5', 
        'BCUCH1_MVB2_DS_311.sDiagnosis04_b6', 
        'BCUCH1_MVB2_DS_311.sDiagnosis04_b7', 
        'BCUCH1_MVB2_DS_311.sDiagnosis05_b0', 
        'BCUCH1_MVB2_DS_311.sDiagnosis05_b1', 
        'BCUCH1_MVB2_DS_311.sDiagnosis05_b2', 
        'BCUCH1_MVB2_DS_311.sDiagnosis05_b3', 
        'BCUCH1_MVB2_DS_311.sDiagnosis05_b4', 
        'BCUCH1_MVB2_DS_311.sDiagnosis05_b5', 
        'BCUCH1_MVB2_DS_311.sDiagnosis05_b6', 
        'BCUCH1_MVB2_DS_311.sDiagnosis05_b7', 
        'BCUCH1_MVB2_DS_311.sDiagnosis06_b0', 
        'BCUCH1_MVB2_DS_311.sDiagnosis06_b1', 
        'BCUCH1_MVB2_DS_311.sDiagnosis06_b2', 
        'BCUCH1_MVB2_DS_311.sDiagnosis06_b3', 
        'BCUCH1_MVB2_DS_311.sDiagnosis06_b4', 
        'BCUCH1_MVB2_DS_311.sDiagnosis06_b5', 
        'BCUCH1_MVB2_DS_311.sDiagnosis06_b6', 
        'BCUCH1_MVB2_DS_311.sDiagnosis06_b7', 
        'BCUCH1_MVB2_DS_311.sDiagnosis07_b0', 
        'BCUCH1_MVB2_DS_311.sDiagnosis07_b1', 
        'BCUCH1_MVB2_DS_311.sDiagnosis07_b2', 
        'BCUCH1_MVB2_DS_311.sDiagnosis07_b3', 
        'BCUCH1_MVB2_DS_311.sDiagnosis07_b4', 
        'BCUCH1_MVB2_DS_311.sDiagnosis07_b5', 
        'BCUCH1_MVB2_DS_311.sDiagnosis07_b6', 
        'BCUCH1_MVB2_DS_311.sDiagnosis07_b7', 
        'BCUCH1_MVB2_DS_311.sDiagnosis08_b0', 
        'BCUCH1_MVB2_DS_311.sDiagnosis08_b1', 
        'BCUCH1_MVB2_DS_311.sDiagnosis08_b2', 
        'BCUCH1_MVB2_DS_311.sDiagnosis08_b3', 
        'BCUCH1_MVB2_DS_311.sDiagnosis08_b4', 
        'BCUCH1_MVB2_DS_311.sDiagnosis08_b5', 
        'BCUCH1_MVB2_DS_311.sDiagnosis08_b6', 
        'BCUCH1_MVB2_DS_311.sDiagnosis08_b7', 
        'BCUCH1_MVB2_DS_311.sDiagnosis09_b0', 
        'BCUCH1_MVB2_DS_311.sDiagnosis09_b1', 
        'BCUCH1_MVB2_DS_311.sDiagnosis09_b2', 
        'BCUCH1_MVB2_DS_311.sDiagnosis09_b3', 
        'BCUCH1_MVB2_DS_311.sDiagnosis09_b4', 
        'BCUCH1_MVB2_DS_311.sDiagnosis09_b5', 
        'BCUCH1_MVB2_DS_311.sDiagnosis09_b6', 
        'BCUCH1_MVB2_DS_311.sDiagnosis09_b7', 
        'BCUCH1_MVB2_DS_311.sDiagnosis10_b0', 
        'BCUCH1_MVB2_DS_311.sDiagnosis10_b1', 
        'BCUCH1_MVB2_DS_311.sDiagnosis10_b2', 
        'BCUCH1_MVB2_DS_311.sDiagnosis10_b3', 
        'BCUCH1_MVB2_DS_311.sDiagnosis10_b4', 
        'BCUCH1_MVB2_DS_311.sDiagnosis10_b5', 
        'BCUCH1_MVB2_DS_311.sDiagnosis10_b6', 
        'BCUCH1_MVB2_DS_311.sDiagnosis10_b7', 
        'BCUCH1_MVB2_DS_311.sDiagnosis11_b0', 
        'BCUCH1_MVB2_DS_311.sDiagnosis11_b1', 
        'BCUCH1_MVB2_DS_311.sDiagnosis11_b2', 
        'BCUCH1_MVB2_DS_311.sDiagnosis11_b3', 
        'BCUCH1_MVB2_DS_311.sDiagnosis11_b4', 
        'BCUCH1_MVB2_DS_311.sDiagnosis11_b5', 
        'BCUCH1_MVB2_DS_311.sDiagnosis11_b6', 
        'BCUCH1_MVB2_DS_311.sDiagnosis11_b7', 
        'BCUCH1_MVB2_DS_311.sDiagnosis12_b0', 
        'BCUCH1_MVB2_DS_311.sDiagnosis12_b1', 
        'BCUCH1_MVB2_DS_311.sDiagnosis12_b2', 
        'BCUCH1_MVB2_DS_311.sDiagnosis12_b3', 
        'BCUCH1_MVB2_DS_311.sDiagnosis12_b4', 
        'BCUCH1_MVB2_DS_311.sDiagnosis12_b5', 
        'BCUCH1_MVB2_DS_311.sDiagnosis12_b6', 
        'BCUCH1_MVB2_DS_311.sDiagnosis12_b7', 
        'BCUCH1_MVB2_DS_311.sDiagnosis13_b0', 
        'BCUCH1_MVB2_DS_311.sDiagnosis13_b1', 
        'BCUCH1_MVB2_DS_311.sDiagnosis13_b2', 
        'BCUCH1_MVB2_DS_311.sDiagnosis13_b3', 
        'BCUCH1_MVB2_DS_311.sDiagnosis13_b4', 
        'BCUCH1_MVB2_DS_311.sDiagnosis13_b5', 
        'BCUCH1_MVB2_DS_311.sDiagnosis13_b6', 
        'BCUCH1_MVB2_DS_311.sDiagnosis13_b7', 
        'BCUCH1_MVB2_DS_311.sDiagnosis14_b0', 
        'BCUCH1_MVB2_DS_311.sDiagnosis14_b1', 
        'BCUCH1_MVB2_DS_311.sDiagnosis14_b2', 
        'BCUCH1_MVB2_DS_311.sDiagnosis14_b3', 
        'BCUCH1_MVB2_DS_311.sDiagnosis14_b4', 
        'BCUCH1_MVB2_DS_311.sDiagnosis14_b5', 
        'BCUCH1_MVB2_DS_311.sDiagnosis14_b6', 
        'BCUCH1_MVB2_DS_311.sDiagnosis14_b7', 
        'BCUCH1_MVB2_DS_311.sDiagnosis15_b0', 
        'BCUCH1_MVB2_DS_311.sDiagnosis15_b1', 
        'BCUCH1_MVB2_DS_311.sDiagnosis15_b2', 
        'BCUCH1_MVB2_DS_311.sDiagnosis15_b3', 
        'BCUCH1_MVB2_DS_311.sDiagnosis15_b4', 
        'BCUCH1_MVB2_DS_311.sDiagnosis15_b5', 
        'BCUCH1_MVB2_DS_311.sDiagnosis15_b6', 
        'BCUCH1_MVB2_DS_311.sDiagnosis15_b7', 
        'BCUCH1_MVB2_DS_311.sDiagnosis16_b0', 
        'BCUCH1_MVB2_DS_311.sDiagnosis16_b1', 
        'BCUCH1_MVB2_DS_311.sDiagnosis16_b2', 
        'BCUCH1_MVB2_DS_311.sDiagnosis16_b3', 
        'BCUCH1_MVB2_DS_311.sDiagnosis16_b4', 
        'BCUCH1_MVB2_DS_311.sDiagnosis16_b5', 
        'BCUCH1_MVB2_DS_311.sDiagnosis16_b6', 
        'BCUCH1_MVB2_DS_311.sDiagnosis16_b7', 
        'BCUCH1_MVB2_DS_311.sDiagnosis17_b0', 
        'BCUCH1_MVB2_DS_311.sDiagnosis17_b1', 
        'BCUCH1_MVB2_DS_311.sDiagnosis17_b2', 
        'BCUCH1_MVB2_DS_311.sDiagnosis17_b3', 
        'BCUCH1_MVB2_DS_311.sDiagnosis17_b4', 
        'BCUCH1_MVB2_DS_311.sDiagnosis17_b5', 
        'BCUCH1_MVB2_DS_311.sDiagnosis17_b6', 
        'BCUCH1_MVB2_DS_311.sDiagnosis17_b7', 
        'BCUCH1_MVB2_DS_311.sDiagnosis18_b0', 
        'BCUCH1_MVB2_DS_311.sDiagnosis18_b1', 
        'BCUCH1_MVB2_DS_311.sDiagnosis18_b2', 
        'BCUCH1_MVB2_DS_311.sDiagnosis18_b3', 
        'BCUCH1_MVB2_DS_311.sDiagnosis18_b4', 
        'BCUCH1_MVB2_DS_311.sDiagnosis18_b5', 
        'BCUCH1_MVB2_DS_311.sDiagnosis18_b6', 
        'BCUCH1_MVB2_DS_311.sDiagnosis18_b7', 
        'BCUCH1_MVB2_DS_311.sDiagnosis19_b0', 
        'BCUCH1_MVB2_DS_311.sDiagnosis19_b1', 
        'BCUCH1_MVB2_DS_311.sDiagnosis19_b2', 
        'BCUCH1_MVB2_DS_311.sDiagnosis19_b3', 
        'BCUCH1_MVB2_DS_311.sDiagnosis19_b4', 
        'BCUCH1_MVB2_DS_311.sDiagnosis19_b5', 
        'BCUCH1_MVB2_DS_311.sDiagnosis19_b6', 
        'BCUCH1_MVB2_DS_311.sDiagnosis19_b7', 
        'BCUCH1_MVB2_DS_311.sDiagnosis20_b0', 
        'BCUCH1_MVB2_DS_311.sDiagnosis20_b1', 
        'BCUCH1_MVB2_DS_311.sDiagnosis20_b2', 
        'BCUCH1_MVB2_DS_311.sDiagnosis20_b3', 
        'BCUCH1_MVB2_DS_311.sDiagnosis20_b4', 
        'BCUCH1_MVB2_DS_311.sDiagnosis20_b5', 
        'BCUCH1_MVB2_DS_311.sDiagnosis20_b6', 
        'BCUCH1_MVB2_DS_311.sDiagnosis20_b7', 
        'BCUCH1_MVB2_DS_311.sDiagnosis21_b0', 
        'BCUCH1_MVB2_DS_311.sDiagnosis21_b1', 
        'BCUCH1_MVB2_DS_311.sDiagnosis21_b2', 
        'BCUCH1_MVB2_DS_311.sDiagnosis21_b3', 
        'BCUCH1_MVB2_DS_311.sDiagnosis21_b4', 
        'BCUCH1_MVB2_DS_311.sDiagnosis21_b5', 
        'BCUCH1_MVB2_DS_311.sDiagnosis21_b6', 
        'BCUCH1_MVB2_DS_311.sDiagnosis21_b7', 
        'BCUCH1_MVB2_DS_311.sDiagnosis22_b0', 
        'BCUCH1_MVB2_DS_311.sDiagnosis22_b1', 
        'BCUCH1_MVB2_DS_311.sDiagnosis22_b2', 
        'BCUCH1_MVB2_DS_311.sDiagnosis22_b3', 
        'BCUCH1_MVB2_DS_311.sDiagnosis22_b4', 
        'BCUCH1_MVB2_DS_311.sDiagnosis22_b5', 
        'BCUCH1_MVB2_DS_311.sDiagnosis22_b6', 
        'BCUCH1_MVB2_DS_311.sDiagnosis22_b7', 
        'BCUCH1_MVB2_DS_311.sDiagnosis23_b0', 
        'BCUCH1_MVB2_DS_311.sDiagnosis23_b1', 
        'BCUCH1_MVB2_DS_311.sDiagnosis23_b2',
        'BCUCH2_MVB1_DS_311.sDiagnosis01_b1',
        'BCUCH2_MVB1_DS_311.sDiagnosis01_b2', 
        'BCUCH2_MVB1_DS_311.sDiagnosis01_b3', 
        'BCUCH2_MVB1_DS_311.sDiagnosis01_b4', 
        'BCUCH2_MVB1_DS_311.sDiagnosis01_b5', 
        'BCUCH2_MVB1_DS_311.sDiagnosis01_b6', 
        'BCUCH2_MVB1_DS_311.sDiagnosis01_b7', 
        'BCUCH2_MVB1_DS_311.sDiagnosis02_b0', 
        'BCUCH2_MVB1_DS_311.sDiagnosis02_b1', 
        'BCUCH2_MVB1_DS_311.sDiagnosis02_b2', 
        'BCUCH2_MVB1_DS_311.sDiagnosis02_b3', 
        'BCUCH2_MVB1_DS_311.sDiagnosis02_b4', 
        'BCUCH2_MVB1_DS_311.sDiagnosis02_b5', 
        'BCUCH2_MVB1_DS_311.sDiagnosis02_b6', 
        'BCUCH2_MVB1_DS_311.sDiagnosis02_b7', 
        'BCUCH2_MVB1_DS_311.sDiagnosis03_b0', 
        'BCUCH2_MVB1_DS_311.sDiagnosis03_b1', 
        'BCUCH2_MVB1_DS_311.sDiagnosis03_b2', 
        'BCUCH2_MVB1_DS_311.sDiagnosis03_b3', 
        'BCUCH2_MVB1_DS_311.sDiagnosis03_b4', 
        'BCUCH2_MVB1_DS_311.sDiagnosis03_b6', 
        'BCUCH2_MVB1_DS_311.sDiagnosis03_b7', 
        'BCUCH2_MVB1_DS_311.sDiagnosis04_b0', 
        'BCUCH2_MVB1_DS_311.sDiagnosis04_b1', 
        'BCUCH2_MVB1_DS_311.sDiagnosis04_b2', 
        'BCUCH2_MVB1_DS_311.sDiagnosis04_b3', 
        'BCUCH2_MVB1_DS_311.sDiagnosis04_b4', 
        'BCUCH2_MVB1_DS_311.sDiagnosis04_b5', 
        'BCUCH2_MVB1_DS_311.sDiagnosis04_b6', 
        'BCUCH2_MVB1_DS_311.sDiagnosis04_b7', 
        'BCUCH2_MVB1_DS_311.sDiagnosis05_b0', 
        'BCUCH2_MVB1_DS_311.sDiagnosis05_b1', 
        'BCUCH2_MVB1_DS_311.sDiagnosis05_b2', 
        'BCUCH2_MVB1_DS_311.sDiagnosis05_b3', 
        'BCUCH2_MVB1_DS_311.sDiagnosis05_b4', 
        'BCUCH2_MVB1_DS_311.sDiagnosis05_b5', 
        'BCUCH2_MVB1_DS_311.sDiagnosis05_b6', 
        'BCUCH2_MVB1_DS_311.sDiagnosis05_b7', 
        'BCUCH2_MVB1_DS_311.sDiagnosis06_b0', 
        'BCUCH2_MVB1_DS_311.sDiagnosis06_b1', 
        'BCUCH2_MVB1_DS_311.sDiagnosis06_b2', 
        'BCUCH2_MVB1_DS_311.sDiagnosis06_b3', 
        'BCUCH2_MVB1_DS_311.sDiagnosis06_b4', 
        'BCUCH2_MVB1_DS_311.sDiagnosis06_b5', 
        'BCUCH2_MVB1_DS_311.sDiagnosis06_b6', 
        'BCUCH2_MVB1_DS_311.sDiagnosis06_b7', 
        'BCUCH2_MVB1_DS_311.sDiagnosis07_b0', 
        'BCUCH2_MVB1_DS_311.sDiagnosis07_b1', 
        'BCUCH2_MVB1_DS_311.sDiagnosis07_b2', 
        'BCUCH2_MVB1_DS_311.sDiagnosis07_b3', 
        'BCUCH2_MVB1_DS_311.sDiagnosis07_b4', 
        'BCUCH2_MVB1_DS_311.sDiagnosis07_b5', 
        'BCUCH2_MVB1_DS_311.sDiagnosis07_b6', 
        'BCUCH2_MVB1_DS_311.sDiagnosis07_b7', 
        'BCUCH2_MVB1_DS_311.sDiagnosis08_b0', 
        'BCUCH2_MVB1_DS_311.sDiagnosis08_b1', 
        'BCUCH2_MVB1_DS_311.sDiagnosis08_b2', 
        'BCUCH2_MVB1_DS_311.sDiagnosis08_b3', 
        'BCUCH2_MVB1_DS_311.sDiagnosis08_b4', 
        'BCUCH2_MVB1_DS_311.sDiagnosis08_b5', 
        'BCUCH2_MVB1_DS_311.sDiagnosis08_b6', 
        'BCUCH2_MVB1_DS_311.sDiagnosis08_b7', 
        'BCUCH2_MVB1_DS_311.sDiagnosis09_b0', 
        'BCUCH2_MVB1_DS_311.sDiagnosis09_b1', 
        'BCUCH2_MVB1_DS_311.sDiagnosis09_b2', 
        'BCUCH2_MVB1_DS_311.sDiagnosis09_b3', 
        'BCUCH2_MVB1_DS_311.sDiagnosis09_b4', 
        'BCUCH2_MVB1_DS_311.sDiagnosis09_b5', 
        'BCUCH2_MVB1_DS_311.sDiagnosis09_b6', 
        'BCUCH2_MVB1_DS_311.sDiagnosis09_b7', 
        'BCUCH2_MVB1_DS_311.sDiagnosis10_b0', 
        'BCUCH2_MVB1_DS_311.sDiagnosis10_b1', 
        'BCUCH2_MVB1_DS_311.sDiagnosis10_b2', 
        'BCUCH2_MVB1_DS_311.sDiagnosis10_b3', 
        'BCUCH2_MVB1_DS_311.sDiagnosis10_b4', 
        'BCUCH2_MVB1_DS_311.sDiagnosis10_b5', 
        'BCUCH2_MVB1_DS_311.sDiagnosis10_b6', 
        'BCUCH2_MVB1_DS_311.sDiagnosis10_b7', 
        'BCUCH2_MVB1_DS_311.sDiagnosis11_b0', 
        'BCUCH2_MVB1_DS_311.sDiagnosis11_b1', 
        'BCUCH2_MVB1_DS_311.sDiagnosis11_b2', 
        'BCUCH2_MVB1_DS_311.sDiagnosis11_b3', 
        'BCUCH2_MVB1_DS_311.sDiagnosis11_b4', 
        'BCUCH2_MVB1_DS_311.sDiagnosis11_b5', 
        'BCUCH2_MVB1_DS_311.sDiagnosis11_b6', 
        'BCUCH2_MVB1_DS_311.sDiagnosis11_b7', 
        'BCUCH2_MVB1_DS_311.sDiagnosis12_b0', 
        'BCUCH2_MVB1_DS_311.sDiagnosis12_b1', 
        'BCUCH2_MVB1_DS_311.sDiagnosis12_b2', 
        'BCUCH2_MVB1_DS_311.sDiagnosis12_b3', 
        'BCUCH2_MVB1_DS_311.sDiagnosis12_b4', 
        'BCUCH2_MVB1_DS_311.sDiagnosis12_b5', 
        'BCUCH2_MVB1_DS_311.sDiagnosis12_b6', 
        'BCUCH2_MVB1_DS_311.sDiagnosis12_b7', 
        'BCUCH2_MVB1_DS_311.sDiagnosis13_b0', 
        'BCUCH2_MVB1_DS_311.sDiagnosis13_b1', 
        'BCUCH2_MVB1_DS_311.sDiagnosis13_b2', 
        'BCUCH2_MVB1_DS_311.sDiagnosis13_b3', 
        'BCUCH2_MVB1_DS_311.sDiagnosis13_b4', 
        'BCUCH2_MVB1_DS_311.sDiagnosis13_b5', 
        'BCUCH2_MVB1_DS_311.sDiagnosis13_b6', 
        'BCUCH2_MVB1_DS_311.sDiagnosis13_b7', 
        'BCUCH2_MVB1_DS_311.sDiagnosis14_b0', 
        'BCUCH2_MVB1_DS_311.sDiagnosis14_b1', 
        'BCUCH2_MVB1_DS_311.sDiagnosis14_b2', 
        'BCUCH2_MVB1_DS_311.sDiagnosis14_b3', 
        'BCUCH2_MVB1_DS_311.sDiagnosis14_b4', 
        'BCUCH2_MVB1_DS_311.sDiagnosis14_b5', 
        'BCUCH2_MVB1_DS_311.sDiagnosis14_b6', 
        'BCUCH2_MVB1_DS_311.sDiagnosis14_b7', 
        'BCUCH2_MVB1_DS_311.sDiagnosis15_b0', 
        'BCUCH2_MVB1_DS_311.sDiagnosis15_b1', 
        'BCUCH2_MVB1_DS_311.sDiagnosis15_b2', 
        'BCUCH2_MVB1_DS_311.sDiagnosis15_b3', 
        'BCUCH2_MVB1_DS_311.sDiagnosis15_b4', 
        'BCUCH2_MVB1_DS_311.sDiagnosis15_b5', 
        'BCUCH2_MVB1_DS_311.sDiagnosis15_b6', 
        'BCUCH2_MVB1_DS_311.sDiagnosis15_b7', 
        'BCUCH2_MVB1_DS_311.sDiagnosis16_b0', 
        'BCUCH2_MVB1_DS_311.sDiagnosis16_b1', 
        'BCUCH2_MVB1_DS_311.sDiagnosis16_b2', 
        'BCUCH2_MVB1_DS_311.sDiagnosis16_b3', 
        'BCUCH2_MVB1_DS_311.sDiagnosis16_b4', 
        'BCUCH2_MVB1_DS_311.sDiagnosis16_b5', 
        'BCUCH2_MVB1_DS_311.sDiagnosis16_b6', 
        'BCUCH2_MVB1_DS_311.sDiagnosis16_b7', 
        'BCUCH2_MVB1_DS_311.sDiagnosis17_b0', 
        'BCUCH2_MVB1_DS_311.sDiagnosis17_b1', 
        'BCUCH2_MVB1_DS_311.sDiagnosis17_b2', 
        'BCUCH2_MVB1_DS_311.sDiagnosis17_b3', 
        'BCUCH2_MVB1_DS_311.sDiagnosis17_b4', 
        'BCUCH2_MVB1_DS_311.sDiagnosis17_b5', 
        'BCUCH2_MVB1_DS_311.sDiagnosis17_b6', 
        'BCUCH2_MVB1_DS_311.sDiagnosis17_b7', 
        'BCUCH2_MVB1_DS_311.sDiagnosis18_b0', 
        'BCUCH2_MVB1_DS_311.sDiagnosis18_b1', 
        'BCUCH2_MVB1_DS_311.sDiagnosis18_b2', 
        'BCUCH2_MVB1_DS_311.sDiagnosis18_b3', 
        'BCUCH2_MVB1_DS_311.sDiagnosis18_b4', 
        'BCUCH2_MVB1_DS_311.sDiagnosis18_b5', 
        'BCUCH2_MVB1_DS_311.sDiagnosis18_b6', 
        'BCUCH2_MVB1_DS_311.sDiagnosis18_b7', 
        'BCUCH2_MVB1_DS_311.sDiagnosis19_b0', 
        'BCUCH2_MVB1_DS_311.sDiagnosis19_b1', 
        'BCUCH2_MVB1_DS_311.sDiagnosis19_b2', 
        'BCUCH2_MVB1_DS_311.sDiagnosis19_b3', 
        'BCUCH2_MVB1_DS_311.sDiagnosis19_b4', 
        'BCUCH2_MVB1_DS_311.sDiagnosis19_b5', 
        'BCUCH2_MVB1_DS_311.sDiagnosis19_b6', 
        'BCUCH2_MVB1_DS_311.sDiagnosis19_b7', 
        'BCUCH2_MVB1_DS_311.sDiagnosis20_b0', 
        'BCUCH2_MVB1_DS_311.sDiagnosis20_b1', 
        'BCUCH2_MVB1_DS_311.sDiagnosis20_b2', 
        'BCUCH2_MVB1_DS_311.sDiagnosis20_b3', 
        'BCUCH2_MVB1_DS_311.sDiagnosis20_b4', 
        'BCUCH2_MVB1_DS_311.sDiagnosis20_b5', 
        'BCUCH2_MVB1_DS_311.sDiagnosis20_b6', 
        'BCUCH2_MVB1_DS_311.sDiagnosis20_b7', 
        'BCUCH2_MVB1_DS_311.sDiagnosis21_b0', 
        'BCUCH2_MVB1_DS_311.sDiagnosis21_b1', 
        'BCUCH2_MVB1_DS_311.sDiagnosis21_b2', 
        'BCUCH2_MVB1_DS_311.sDiagnosis21_b3', 
        'BCUCH2_MVB1_DS_311.sDiagnosis21_b4', 
        'BCUCH2_MVB1_DS_311.sDiagnosis21_b5', 
        'BCUCH2_MVB1_DS_311.sDiagnosis21_b6', 
        'BCUCH2_MVB1_DS_311.sDiagnosis21_b7', 
        'BCUCH2_MVB1_DS_311.sDiagnosis22_b0', 
        'BCUCH2_MVB1_DS_311.sDiagnosis22_b1', 
        'BCUCH2_MVB1_DS_311.sDiagnosis22_b2', 
        'BCUCH2_MVB1_DS_311.sDiagnosis22_b3', 
        'BCUCH2_MVB1_DS_311.sDiagnosis22_b4', 
        'BCUCH2_MVB1_DS_311.sDiagnosis22_b5', 
        'BCUCH2_MVB1_DS_311.sDiagnosis22_b6', 
        'BCUCH2_MVB1_DS_311.sDiagnosis22_b7', 
        'BCUCH2_MVB1_DS_311.sDiagnosis23_b0', 
        'BCUCH2_MVB1_DS_311.sDiagnosis23_b1', 
        'BCUCH2_MVB1_DS_311.sDiagnosis23_b2',
        'BCU_MVB1_DS_06E.bDIBA_Train_S2',
        'BCU_MVB2_DS_30D.bDIBA_Train_S2',
        'BCU_MVB1_DS_06E.bDIMGA_Train_S2',
        'BCU_MVB2_DS_30D.bDIMGA_Train_S2',
        'BCU_MVB1_DS_06E.bDIMGA',
        'BCU_MVB2_DS_30D.bDIMGA',
        'BCU_MVB2_DS_30D.bPBA_Speed',
        'BCU_MVB1_DS_06E.bPBA_Speed',
        'BCUCH1_MVB2_DS_310.bDNRA_OK',
        'BCUCH2_MVB1_DS_310.bDNRA_OK',
        "BCU_MVB1_DS_06E.bDNRA_Notlocked",
        "BCU_MVB2_DS_30D.bDNRA_Notlocked"
        ]
        self.BCU_DIAGNOSIS_CC = [
        'BCUB90_MVB1_DS_614.sDiagnosis01_b1',
        'BCUB95_MVB2_DS_614.sDiagnosis01_b1',
        'BCUB90_MVB1_DS_614.sDiagnosis01_b2',
        'BCUB95_MVB2_DS_614.sDiagnosis01_b2',
        'BCUB90_MVB1_DS_614.sDiagnosis01_b3',
        'BCUB95_MVB2_DS_614.sDiagnosis01_b3',
        'BCUB90_MVB1_DS_614.sDiagnosis01_b4',
        'BCUB95_MVB2_DS_614.sDiagnosis01_b4',
        'BCUB90_MVB1_DS_614.sDiagnosis01_b5',
        'BCUB95_MVB2_DS_614.sDiagnosis01_b5',
        'BCUB90_MVB1_DS_614.sDiagnosis01_b6',
        'BCUB95_MVB2_DS_614.sDiagnosis01_b6',
        'BCUB90_MVB1_DS_614.sDiagnosis01_b7',
        'BCUB95_MVB2_DS_614.sDiagnosis01_b7',
        'BCUB90_MVB1_DS_614.sDiagnosis02_b0',
        'BCUB95_MVB2_DS_614.sDiagnosis02_b0',
        'BCUB90_MVB1_DS_614.sDiagnosis02_b1',
        'BCUB95_MVB2_DS_614.sDiagnosis02_b1',
        'BCUB90_MVB1_DS_614.sDiagnosis02_b2',
        'BCUB95_MVB2_DS_614.sDiagnosis02_b2',
        'BCUB90_MVB1_DS_614.sDiagnosis02_b3',
        'BCUB95_MVB2_DS_614.sDiagnosis02_b3',
        'BCUB90_MVB1_DS_614.sDiagnosis02_b4',
        'BCUB95_MVB2_DS_614.sDiagnosis02_b4',
        'BCUB90_MVB1_DS_614.sDiagnosis02_b5',
        'BCUB95_MVB2_DS_614.sDiagnosis02_b5',
        'BCUB90_MVB1_DS_614.sDiagnosis02_b6',
        'BCUB95_MVB2_DS_614.sDiagnosis02_b6',
        'BCUB90_MVB1_DS_614.sDiagnosis02_b7',
        'BCUB95_MVB2_DS_614.sDiagnosis02_b7',
        'BCUB90_MVB1_DS_614.sDiagnosis03_b0',
        'BCUB95_MVB2_DS_614.sDiagnosis03_b0',
        'BCUB90_MVB1_DS_614.sDiagnosis03_b1',
        'BCUB95_MVB2_DS_614.sDiagnosis03_b1',
        'BCUB90_MVB1_DS_614.sDiagnosis03_b2',
        'BCUB95_MVB2_DS_614.sDiagnosis03_b2',
        'BCUB90_MVB1_DS_614.sDiagnosis03_b3',
        'BCUB95_MVB2_DS_614.sDiagnosis03_b3',
        'BCUB90_MVB1_DS_614.sDiagnosis03_b4',
        'BCUB95_MVB2_DS_614.sDiagnosis03_b4',
        'BCUB90_MVB1_DS_614.sDiagnosis03_b6',
        'BCUB95_MVB2_DS_614.sDiagnosis03_b6',
        'BCUB90_MVB1_DS_614.sDiagnosis03_b7',
        'BCUB95_MVB2_DS_614.sDiagnosis03_b7',
        'BCUB90_MVB1_DS_614.sDiagnosis04_b0',
        'BCUB95_MVB2_DS_614.sDiagnosis04_b0',
        'BCUB90_MVB1_DS_614.sDiagnosis04_b1',
        'BCUB95_MVB2_DS_614.sDiagnosis04_b1',
        'BCUB90_MVB1_DS_614.sDiagnosis04_b2',
        'BCUB95_MVB2_DS_614.sDiagnosis04_b2',
        'BCUB90_MVB1_DS_614.sDiagnosis04_b3',
        'BCUB95_MVB2_DS_614.sDiagnosis04_b3',
        'BCUB90_MVB1_DS_614.sDiagnosis04_b4',
        'BCUB95_MVB2_DS_614.sDiagnosis04_b4',
        'BCUB90_MVB1_DS_614.sDiagnosis04_b5',
        'BCUB95_MVB2_DS_614.sDiagnosis04_b5',
        'BCUB90_MVB1_DS_614.sDiagnosis04_b6',
        'BCUB95_MVB2_DS_614.sDiagnosis04_b6',
        'BCUB90_MVB1_DS_614.sDiagnosis04_b7',
        'BCUB95_MVB2_DS_614.sDiagnosis04_b7',
        'BCUB90_MVB1_DS_614.sDiagnosis05_b0',
        'BCUB95_MVB2_DS_614.sDiagnosis05_b0',
        'BCUB90_MVB1_DS_614.sDiagnosis05_b1',
        'BCUB95_MVB2_DS_614.sDiagnosis05_b1',
        'BCUB90_MVB1_DS_614.sDiagnosis05_b2',
        'BCUB95_MVB2_DS_614.sDiagnosis05_b2',
        'BCUB90_MVB1_DS_614.sDiagnosis05_b3',
        'BCUB95_MVB2_DS_614.sDiagnosis05_b3',
        'BCUB90_MVB1_DS_614.sDiagnosis05_b4',
        'BCUB95_MVB2_DS_614.sDiagnosis05_b4',
        'BCUB90_MVB1_DS_614.sDiagnosis05_b5',
        'BCUB95_MVB2_DS_614.sDiagnosis05_b5',
        'BCUB90_MVB1_DS_614.sDiagnosis05_b6',
        'BCUB95_MVB2_DS_614.sDiagnosis05_b6',
        'BCUB90_MVB1_DS_614.sDiagnosis05_b7',
        'BCUB95_MVB2_DS_614.sDiagnosis05_b7',
        'BCUB90_MVB1_DS_614.sDiagnosis06_b0',
        'BCUB95_MVB2_DS_614.sDiagnosis06_b0',
        'BCUB90_MVB1_DS_614.sDiagnosis06_b1',
        'BCUB95_MVB2_DS_614.sDiagnosis06_b1',
        'BCUB90_MVB1_DS_614.sDiagnosis06_b2',
        'BCUB95_MVB2_DS_614.sDiagnosis06_b2',
        'BCUB90_MVB1_DS_614.sDiagnosis06_b3',
        'BCUB95_MVB2_DS_614.sDiagnosis06_b3',
        'BCUB90_MVB1_DS_614.sDiagnosis06_b4',
        'BCUB95_MVB2_DS_614.sDiagnosis06_b4',
        'BCUB90_MVB1_DS_614.sDiagnosis06_b5',
        'BCUB95_MVB2_DS_614.sDiagnosis06_b5',
        'BCUB90_MVB1_DS_614.sDiagnosis06_b6',
        'BCUB95_MVB2_DS_614.sDiagnosis06_b6',
        'BCUB90_MVB1_DS_614.sDiagnosis06_b7',
        'BCUB95_MVB2_DS_614.sDiagnosis06_b7',
        'BCUB90_MVB1_DS_614.sDiagnosis07_b0',
        'BCUB95_MVB2_DS_614.sDiagnosis07_b0',
        'BCUB90_MVB1_DS_614.sDiagnosis07_b1',
        'BCUB95_MVB2_DS_614.sDiagnosis07_b1',
        'BCUB90_MVB1_DS_614.sDiagnosis07_b2',
        'BCUB95_MVB2_DS_614.sDiagnosis07_b2',
        'BCUB90_MVB1_DS_614.sDiagnosis07_b3',
        'BCUB95_MVB2_DS_614.sDiagnosis07_b3',
        'BCUB90_MVB1_DS_614.sDiagnosis07_b4',
        'BCUB95_MVB2_DS_614.sDiagnosis07_b4',
        'BCUB90_MVB1_DS_614.sDiagnosis07_b5',
        'BCUB95_MVB2_DS_614.sDiagnosis07_b5',
        'BCUB90_MVB1_DS_614.sDiagnosis07_b6',
        'BCUB95_MVB2_DS_614.sDiagnosis07_b6',
        'BCUB90_MVB1_DS_614.sDiagnosis07_b7',
        'BCUB95_MVB2_DS_614.sDiagnosis07_b7',
        'BCUB90_MVB1_DS_614.sDiagnosis08_b0',
        'BCUB95_MVB2_DS_614.sDiagnosis08_b0',
        'BCUB90_MVB1_DS_614.sDiagnosis08_b1',
        'BCUB95_MVB2_DS_614.sDiagnosis08_b1',
        'BCUB90_MVB1_DS_614.sDiagnosis08_b2',
        'BCUB95_MVB2_DS_614.sDiagnosis08_b2',
        'BCUB90_MVB1_DS_614.sDiagnosis08_b3',
        'BCUB95_MVB2_DS_614.sDiagnosis08_b3',
        'BCUB90_MVB1_DS_614.sDiagnosis08_b4',
        'BCUB95_MVB2_DS_614.sDiagnosis08_b4',
        'BCUB90_MVB1_DS_614.sDiagnosis08_b5',
        'BCUB95_MVB2_DS_614.sDiagnosis08_b5',
        'BCUB90_MVB1_DS_614.sDiagnosis08_b6',
        'BCUB95_MVB2_DS_614.sDiagnosis08_b6',
        'BCUB90_MVB1_DS_614.sDiagnosis08_b7',
        'BCUB95_MVB2_DS_614.sDiagnosis08_b7',
        'BCUB90_MVB1_DS_614.sDiagnosis09_b0',
        'BCUB95_MVB2_DS_614.sDiagnosis09_b0',
        'BCUB90_MVB1_DS_614.sDiagnosis09_b1',
        'BCUB95_MVB2_DS_614.sDiagnosis09_b1',
        'BCUB90_MVB1_DS_614.sDiagnosis09_b2',
        'BCUB95_MVB2_DS_614.sDiagnosis09_b2',
        'BCUB90_MVB1_DS_614.sDiagnosis09_b3',
        'BCUB95_MVB2_DS_614.sDiagnosis09_b3',
        'BCUB90_MVB1_DS_614.sDiagnosis09_b4',
        'BCUB95_MVB2_DS_614.sDiagnosis09_b4',
        'BCUB90_MVB1_DS_614.sDiagnosis09_b5',
        'BCUB95_MVB2_DS_614.sDiagnosis09_b5',
        'BCUB90_MVB1_DS_614.sDiagnosis19_b6',
        'BCUB95_MVB2_DS_614.sDiagnosis19_b6',
        'BCUB90_MVB1_DS_614.sDiagnosis19_b7',
        'BCUB95_MVB2_DS_614.sDiagnosis19_b7',
        'BCUB90_MVB1_DS_614.sDiagnosis20_b0',
        'BCUB95_MVB2_DS_614.sDiagnosis20_b0',
        'BCUB90_MVB1_DS_614.sDiagnosis20_b1',
        'BCUB95_MVB2_DS_614.sDiagnosis20_b1',
        'BCUB90_MVB1_DS_614.sDiagnosis20_b2',
        'BCUB95_MVB2_DS_614.sDiagnosis20_b2',
        'BCUB90_MVB1_DS_614.sDiagnosis20_b3',
        'BCUB95_MVB2_DS_614.sDiagnosis20_b3',
        'BCUB90_MVB1_DS_614.sDiagnosis20_b4',
        'BCUB95_MVB2_DS_614.sDiagnosis20_b4',
        'BCUB90_MVB1_DS_614.sDiagnosis20_b5',
        'BCUB95_MVB2_DS_614.sDiagnosis20_b5',
        'BCUB90_MVB1_DS_614.sDiagnosis20_b6',
        'BCUB95_MVB2_DS_614.sDiagnosis20_b6',
        'BCUB90_MVB1_DS_614.sDiagnosis20_b7',
        'BCUB95_MVB2_DS_614.sDiagnosis20_b7',
        'BCUB90_MVB1_DS_614.sDiagnosis21_b0',
        'BCUB95_MVB2_DS_614.sDiagnosis21_b0',
        'BCUB90_MVB1_DS_614.sDiagnosis21_b1',
        'BCUB95_MVB2_DS_614.sDiagnosis21_b1',
        'BCUB90_MVB1_DS_614.sDiagnosis21_b2',
        'BCUB95_MVB2_DS_614.sDiagnosis21_b2',
        'BCUB90_MVB1_DS_614.sDiagnosis21_b3',
        'BCUB95_MVB2_DS_614.sDiagnosis21_b3',
        'BCUB90_MVB1_DS_614.sDiagnosis21_b4',
        'BCUB95_MVB2_DS_614.sDiagnosis21_b4',
        'BCUB90_MVB1_DS_614.sDiagnosis21_b5',
        'BCUB95_MVB2_DS_614.sDiagnosis21_b5',
        'BCUB90_MVB1_DS_614.sDiagnosis21_b6',
        'BCUB95_MVB2_DS_614.sDiagnosis21_b6',
        'BCUB90_MVB1_DS_614.sDiagnosis21_b7',
        'BCUB95_MVB2_DS_614.sDiagnosis21_b7',
        'BCUB90_MVB1_DS_614.sDiagnosis22_b0',
        'BCUB95_MVB2_DS_614.sDiagnosis22_b0',
        'BCUB90_MVB1_DS_614.sDiagnosis22_b1',
        'BCUB95_MVB2_DS_614.sDiagnosis22_b1',
        'BCUB90_MVB1_DS_614.sDiagnosis22_b2',
        'BCUB95_MVB2_DS_614.sDiagnosis22_b2',
        'BCUB90_MVB1_DS_614.sDiagnosis22_b3',
        'BCUB95_MVB2_DS_614.sDiagnosis22_b3',
        'BCUB90_MVB1_DS_614.sDiagnosis22_b4',
        'BCUB95_MVB2_DS_614.sDiagnosis22_b4',
        'BCUB90_MVB1_DS_614.sDiagnosis22_b5',
        'BCUB95_MVB2_DS_614.sDiagnosis22_b5',
        'BCUB90_MVB1_DS_614.sDiagnosis22_b6',
        'BCUB95_MVB2_DS_614.sDiagnosis22_b6',
        'BCUB90_MVB1_DS_614.sDiagnosis22_b7',
        'BCUB95_MVB2_DS_614.sDiagnosis22_b7',
        'BCUB90_MVB1_DS_614.sDiagnosis23_b0',
        'BCUB95_MVB2_DS_614.sDiagnosis23_b0',
        'BCUB90_MVB1_DS_614.sDiagnosis23_b1',
        'BCUB95_MVB2_DS_614.sDiagnosis23_b1',
        'BCUB90_MVB1_DS_614.sDiagnosis23_b2',
        'BCUB95_MVB2_DS_614.sDiagnosis23_b2',
        'BCUB90_MVB1_DS_612.bDIMGA_NOK',
        'BCUB95_MVB2_DS_612.bDIMGA_NOK',
        'BCUB90_MVB1_DS_612.bPBA_Speed_NOK',
        'BCUB95_MVB2_DS_612.bPBA_Speed_NOK',
        'BCUB90_MVB1_DS_612.bDIBA_Train_S2_NOK',
        'BCUB95_MVB2_DS_612.bDIBA_Train_S2_NOK'

    ]
        #DICCIONARIO PARA INTERPRETAR LA DIAGNÓSIS DE FRENO
        self.BCU_DIAGNOSIS_DICT = {
        'bDIBA_S2_NOK': {'Error Code': 'bDIBA_S2_NOK', 'Description': 'Function DIBA_Train not available'},
        'bDIMGA_S0': {'Error Code': 'bDIMGA_S0', 'Description': 'Improperly MTB applied'},    
        'sDiagnosis01_b0': {'Error Code': 'DIA_BOARD_EB02B_07', 'Description': 'Malfunction Board EB02B Node 07 in BCU B9x '},
        'sDiagnosis01_b1': {'Error Code': 'DIA_BOARDCODING_EB02B_07', 'Description': 'The board coding is not correct: either the mode or the node information coded does not comply with the expected codification for the board'},
        'sDiagnosis01_b2': {'Error Code': 'DIA_CAN_COMM_EB02B_07', 'Description': 'Internal CAN Communications error'},
        'sDiagnosis01_b3': {'Error Code': 'DIA_BOARD_EB01B_08', 'Description': 'Malfunction Board EB01B Node 08 in BCU B9x '},
        'sDiagnosis01_b4': {'Error Code': 'DIA_BOARDCODING_EB01B_08', 'Description': 'The board coding is not correct: either the mode or the node information coded does not comply with the expected codification for the board'},
        'sDiagnosis01_b5': {'Error Code': 'DIA_CAN_COMM_EB01B_08', 'Description': 'Internal CAN Communications error'}, 'sDiagnosis01_b6': {'Error Code': 'DIA_BOARD_EB01B_09', 'Description': 'Malfunction Board EB01B Node 09 in BCU B90 '},
        'sDiagnosis01_b7': {'Error Code': 'DIA_BOARDCODING_EB01B_09', 'Description': 'The board coding is not correct: either the mode or the node information coded does not comply with the expected codification for the board'},
        'sDiagnosis02_b0': {'Error Code': 'DIA_CAN_COMM_EB01B_09', 'Description': 'Internal CAN Communications error'}, 'sDiagnosis02_b1': {'Error Code': 'DIA_BOARD_MB03B_04', 'Description': 'Malfunction Board MB03B Node 04 in BCU B9x '},
        'sDiagnosis02_b2': {'Error Code': 'DIA_BOARDCODING_MB03B_04', 'Description': 'The board coding is not correct: either the mode or the node information coded does not comply with the expected codification for the board'},
        'sDiagnosis02_b3': {'Error Code': 'DIA_CAN_COMM_MB03B_04', 'Description': 'Internal CAN Communications error'}, 'sDiagnosis02_b4': {'Error Code': 'DIA_BOARD_MB03B_06', 'Description': 'Malfunction Board MB03B Node 06 in BCU B9x '},
        'sDiagnosis02_b5': {'Error Code': 'DIA_BOARDCODING_MB03B_06', 'Description': 'The board coding is not correct: either the mode or the node information coded does not comply with the expected codification for the board'},
        'sDiagnosis02_b6': {'Error Code': 'DIA_CAN_COMM_MB03B_06', 'Description': 'Internal CAN Communications error'}, 'sDiagnosis02_b7': {'Error Code': 'DIA_BOARD_MB03B_05', 'Description': 'Malfunction Board MB03B Node 05 in BCU B95 '},
        'sDiagnosis03_b0': {'Error Code': 'DIA_BOARDCODING_MB03B_05', 'Description': 'The board coding is not correct: either the mode or the node information coded does not comply with the expected codification for the board'},
        'sDiagnosis03_b1': {'Error Code': 'DIA_CAN_COMM_MB03B_05', 'Description': 'Internal CAN Communications error'},
        'sDiagnosis03_b2': {'Error Code': 'DIA_BOARD_CB09F_02', 'Description': 'Malfunction Board CB09F Node 02 in BCU B9x '},
        'sDiagnosis03_b3': {'Error Code': 'DIA_BOARDCODING_CB09F_02', 'Description': 'The board coding is not correct: either the mode or the node information coded does not comply with the expected codification for the board'},
        'sDiagnosis03_b4': {'Error Code': 'DIA_CAN_COMM_CB09F_02', 'Description': 'Internal CAN Communications error'},
        'sDiagnosis03_b6': {'Error Code': 'DIA_BOARDCODING_CB05A_03', 'Description': 'The board coding is not correct: either the mode or the node information coded does not comply with the expected codification for the board'},
        'sDiagnosis03_b7': {'Error Code': 'DIA_CAN_COMM_CB05A_03', 'Description': 'Internal CAN Communications error'},
        'sDiagnosis04_b0': {'Error Code': 'DIA_EB01B_08_RELAY0', 'Description': 'Relay failure: relay output does not operate correctly'},
        'sDiagnosis04_b1': {'Error Code': 'DIA_EB01B_08_RELAY1', 'Description': 'Relay failure: relay output does not operate correctly'},
        'sDiagnosis04_b2': {'Error Code': 'DIA_EB01B_08_RELAY2', 'Description': 'Relay failure: relay output does not operate correctly'},
        'sDiagnosis04_b3': {'Error Code': 'DIA_EB01B_08_RELAY3', 'Description': 'Relay failure: relay output does not operate correctly'},
        'sDiagnosis04_b4': {'Error Code': 'DIA_EB01B_08_RELAY4', 'Description': 'Relay failure: relay output does not operate correctly'},
        'sDiagnosis04_b5': {'Error Code': 'DIA_EB01B_08_RELAY5', 'Description': 'Relay failure: relay output does not operate correctly'},
        'sDiagnosis04_b6': {'Error Code': 'DIA_EB01B_08_RELAY6', 'Description': 'Relay failure: relay output does not operate correctly'},
        'sDiagnosis04_b7': {'Error Code': 'DIA_EB01B_08_RELAY7', 'Description': 'Relay failure: relay output does not operate correctly'},
        'sDiagnosis05_b0': {'Error Code': 'DIA_EB01B_09_RELAY0', 'Description': 'Relay failure: relay output does not operate correctly'},
        'sDiagnosis05_b1': {'Error Code': 'DIA_EB01B_09_RELAY1', 'Description': 'Relay failure: relay output does not operate correctly'},
        'sDiagnosis05_b2': {'Error Code': 'DIA_EB01B_09_RELAY2', 'Description': 'Relay failure: relay output does not operate correctly'},
        'sDiagnosis05_b3': {'Error Code': 'DIA_EB01B_09_RELAY3', 'Description': 'Relay failure: relay output does not operate correctly'},
        'sDiagnosis05_b4': {'Error Code': 'DIA_EB01B_09_RELAY4', 'Description': 'Relay failure: relay output does not operate correctly'},
        'sDiagnosis05_b5': {'Error Code': 'DIA_EB01B_09_RELAY5', 'Description': 'Relay failure: relay output does not operate correctly'},
        'sDiagnosis05_b6': {'Error Code': 'DIA_EB01B_09_RELAY6', 'Description': 'Relay failure: relay output does not operate correctly'},
        'sDiagnosis05_b7': {'Error Code': 'DIA_EB01B_09_RELAY7', 'Description': 'Relay failure: relay output does not operate correctly'},
        'sDiagnosis06_b0': {'Error Code': 'DIA_70_WSP', 'Description': 'Cumulative error: all the speed sensors of car are in fault.'},
        'sDiagnosis06_b1': {'Error Code': 'DIA_72_WSP', 'Description': 'Cumulative error: WSP errors in one axle (bogie) or wheel (rodal)'},
        'sDiagnosis06_b2': {'Error Code': 'DIA_73_WSP', 'Description': 'Cumulative error: WSP errors in one axle (bogie) or wheel (rodal)'},
        'sDiagnosis06_b3': {'Error Code': 'DIA_TIMEOUT_1_WSP', 'Description': '- Mechanical failure in anti-skid valve (WSP is not able to correct a slide)_x000D_\n- Failure in speed signal_x000D_\n- Very low adhesion'},
        'sDiagnosis06_b4': {'Error Code': 'DIA_TIMEOUT_2_WSP', 'Description': '- Mechanical failure in anti-skid valve (WSP is not able to correct a slide)_x000D_\n- Failure in speed signal_x000D_\n- Very low adhesion'},
        'sDiagnosis06_b5': {'Error Code': 'DIA_TIMEOUT_3_WSP', 'Description': '- Mechanical failure in anti-skid valve (WSP is not able to correct a slide)\n- Failure in speed signal\n- Very low adhesion'},
        'sDiagnosis06_b6': {'Error Code': 'DIA_FSI_1_WSP', 'Description': '“Short circuit/Open circuit” also called mean-voltage error. Detected by checking that the mean voltage/current value of the speed sensor signal is out of range.'},
        'sDiagnosis06_b7': {'Error Code': 'DIA_FSI_2_WSP', 'Description': '“Short circuit/Open circuit” also called mean-voltage error. Detected by checking that the mean voltage/current value of the speed sensor signal is out of range.'},
        'sDiagnosis07_b0': {'Error Code': 'DIA_FSI_3_WSP', 'Description': '“Short circuit/Open circuit” also called mean-voltage error. Detected by checking that the mean voltage/current value of the speed sensor signal is out of range.'},
        'sDiagnosis07_b1': {'Error Code': 'DIA_FSI_4_WSP', 'Description': '“Short circuit/Open circuit” also called mean-voltage error. Detected by checking that the mean voltage/current value of the speed sensor signal is out of range.'},
        'sDiagnosis07_b2': {'Error Code': 'DIA_DV_1_WSP', 'Description': 'Failure in plausibility of speed signal. This means that the speed signal is giving values that are not phisically acceptable.'},
        'sDiagnosis07_b3': {'Error Code': 'DIA_DV_2_WSP', 'Description': 'Failure in plausibility of speed signal. This means that the speed signal is giving values that are not phisically acceptable.'},
        'sDiagnosis07_b4': {'Error Code': 'DIA_DV_3_WSP', 'Description': 'Failure in plausibility of speed signal. This means that the speed signal is giving values that are not phisically acceptable.'},
        'sDiagnosis07_b5': {'Error Code': 'DIA_DV_4_WSP', 'Description': 'Failure in plausibility of speed signal. This means that the speed signal is giving values that are not phisically acceptable.'},
        'sDiagnosis07_b6': {'Error Code': 'DIA_SHORT_VALVE1_WSP', 'Description': 'ShortCut detected in the anti-skid valve circuits'},
        'sDiagnosis07_b7': {'Error Code': 'DIA_SHORT_VALVE2_WSP', 'Description': 'ShortCut detected in the anti-skid valve circuits'},
        'sDiagnosis08_b0': {'Error Code': 'DIA_SHORT_VALVE3_WSP', 'Description': 'ShortCut detected in the anti-skid valve circuits'},
        'sDiagnosis08_b1': {'Error Code': 'DIA_OPEN_VALVE1_WSP', 'Description': 'Open Circuit detected in the anti-skid valve circuits'},
        'sDiagnosis08_b2': {'Error Code': 'DIA_OPEN_VALVE2_WSP', 'Description': 'Open Circuit detected in the anti-skid valve circuits'},
        'sDiagnosis08_b3': {'Error Code': 'DIA_OPEN_VALVE3_WSP', 'Description': 'Open Circuit detected in the anti-skid valve circuits'},
        'sDiagnosis08_b4': {'Error Code': 'DIA_UWR_TIMEOUT_1_WSP', 'Description': 'Failure in the safety monitoring circuit (whatchdog) detected with a WSP complete test in POP1/2'},
        'sDiagnosis08_b5': {'Error Code': 'DIA_UWR_TIMEOUT_2_WSP', 'Description': 'Failure in the safety monitoring circuit (whatchdog) detected with a WSP complete test in POP3/4'},
        'sDiagnosis08_b6': {'Error Code': 'DIA_UWR_TIMEOUT_3_WSP', 'Description': 'Failure in the safety monitoring circuit (whatchdog) detected with a WSP complete test in POP5/6'},
        'sDiagnosis08_b7': {'Error Code': 'DIA_LOCKED_1_DIAG_WSP', 'Description': '- Very low adhesion value between wheel and rail_x000D_\n- Very high slide between wheel and rail over long period of time_x000D_\n- Anti-skid valve defect_x000D_\n- Speed sensor defect_x000D_\n- Main board MB03B defect'},
        'sDiagnosis09_b0': {'Error Code': 'DIA_LOCKED_2_DIAG_WSP', 'Description': '- Very low adhesion value between wheel and rail_x000D_\n- Very high slide between wheel and rail over long period of time_x000D_\n- Anti-skid valve defect_x000D_\n- Speed sensor defect_x000D_\n- Main board MB03B defect'},
        'sDiagnosis09_b1': {'Error Code': 'DIA_LOGIC_TIMEOUT_1_WSP', 'Description': '- Maximum admissible actuation time reached:_x000D_\n- Very low adhesion value between wheel and rail_x000D_\n- Anti-skid valve defect_x000D_\n- Speed sensor defect_x000D_\n- Main board MB03B defect'},
        'sDiagnosis09_b2': {'Error Code': 'DIA_LOGIC_TIMEOUT_2_WSP', 'Description': '- Maximum admissible actuation time reached:_x000D_\n- Very low adhesion value between wheel and rail_x000D_\n- Anti-skid valve defect_x000D_\n- Speed sensor defect_x000D_\n- Main board MB03B defect'},
        'sDiagnosis09_b3': {'Error Code': 'DIA_LOGIC_TIMEOUT_3_WSP', 'Description': '- Maximum admissible actuation time reached:_x000D_\n- Very low adhesion value between wheel and rail_x000D_\n- Anti-skid valve defect_x000D_\n- Speed sensor defect_x000D_\n- Main board MB03B defect'},
        'sDiagnosis09_b4': {'Error Code': 'DIA_WHEELSET_1_WSP', 'Description': 'The „Wheelset error“ is an accumulated error which regards the following single WSP errors: 10_E, 11_E, 21_E, 31_E, 41_E, 12_E, 22_E, 32_E, 42_E, 13_E, 14_E, 15_E, 17_E'},
        'sDiagnosis09_b5': {'Error Code': 'DIA_WHEELSET_2_WSP', 'Description': 'The „Wheelset error“ is an accumulated error which regards the following single WSP errors: 20_E, 11_E, 21_E, 31_E, 41_E, 12_E, 22_E, 32_E, 42_E, 23_E, 24_E, 25_E, 27_E'},
        'sDiagnosis09_b6': {'Error Code': 'DIA_WHEELSET_3_WSP', 'Description': 'The „Wheelset error“ is an accumulated error which regards the following single WSP errors: 30_E, 11_E, 21_E, 31_E, 41_E, 12_E, 22_E, 32_E, 42_E, 33_E, 34_E, 35_E, 37_E'},
        'sDiagnosis09_b7': {'Error Code': 'DIA_WHEELSET_4_WSP', 'Description': 'The „Wheelset error“ is an accumulated error which regards the following single WSP errors: 40_E, 11_E, 21_E, 31_E, 41_E, 12_E, 22_E, 32_E, 42_E, 33_E, 34_E, 35_E, 37_E'},
        'sDiagnosis10_b0': {'Error Code': 'DIA_MVB', 'Description': 'Malfunction of MVB bus'},
        'sDiagnosis10_b1': {'Error Code': 'DIA_C_PRESS_SENSOR', 'Description': 'Cylinder pressure transducer error'},
        'sDiagnosis10_b2': {'Error Code': 'DIA_C_PRESS1_SENSOR', 'Description': 'Cylinder pressure transducer error'},
        'sDiagnosis10_b3': {'Error Code': 'DIA_C_PRESS2_SENSOR', 'Description': 'Cylinder pressure transducer error'},
        'sDiagnosis10_b4': {'Error Code': 'DIA_T_PRESS_SENSOR', 'Description': 'Load (suspension) pressure transducer error'},
        'sDiagnosis10_b5': {'Error Code': 'DIA_R_PRESS_SENSOR', 'Description': 'Reservoir pressure transducer error'},
        'sDiagnosis10_b6': {'Error Code': 'DIA_HC_PRESS1_SENSOR', 'Description': 'Parking brake hydraulic pressure transducer error'},
        'sDiagnosis10_b7': {'Error Code': 'DIA_HC_PRESS2_SENSOR', 'Description': 'Parking brake hydraulic pressure transducer error'},
        'sDiagnosis11_b0': {'Error Code': 'DIA_ER_PRESS_SENSOR', 'Description': 'ER pressure transducer error'},
        'sDiagnosis11_b1': {'Error Code': 'DIA_BP_PRESS_SENSOR', 'Description': 'BP pressure transducer error'},
        'sDiagnosis11_b2': {'Error Code': 'DIA_MRP_PRESS_SENSOR', 'Description': 'MRP pressure transducer error'},
        'sDiagnosis11_b3': {'Error Code': 'DIA_FL_PRESS_SENSOR', 'Description': 'MRP pressure transducer error'},
        'sDiagnosis11_b4': {'Error Code': 'DIA_DIR_BRK_PRESS_SENSOR', 'Description': 'Direct brake C pressure transducer error'},
        'sDiagnosis11_b5': {'Error Code': 'DIA_SANDING_PRESS_SENSOR', 'Description': 'Sanding pressure transducer error'},
        'sDiagnosis11_b6': {'Error Code': 'DIA_DIBA', 'Description': 'Brake should be released but brake is applied according to brake pressure monitored.'},
        'sDiagnosis11_b7': {'Error Code': 'DIA_NBA', 'Description': 'Brake should not be released but brake is released according to brake pressure monitored.'},
        'sDiagnosis12_b0': {'Error Code': 'DIA_DIMGA', 'Description': 'MTB should be released but MTB is applied (low position and energized) according to MTB monitoring.'},
        'sDiagnosis12_b1': {'Error Code': 'DIA_DCL_DEVIATION_BP_NORMAL', 'Description': '- ER pressure sensor defect_x000D_\n- ER charge valve defect_x000D_\n- ER vent valve defect_x000D_\n- ER electronic mode valve defect_x000D_\n- Main board MB03B defect'},
        'sDiagnosis12_b2': {'Error Code': 'DIA_DCL_OFFSET_BP_NORMAL', 'Description': 'ER pressure sensor defect:\n- Pressure below -0.2bar OR\n- At least expired since pressure dropped below 0.6bar with measured pressure above 0.4bar'},
        'sDiagnosis12_b3': {'Error Code': 'DIA_POP1_DCL_CHARGE_BP_NORMAL', 'Description': '- Plugs from main board MB03B to ER charge magnet valve unfastened_x000D_\n- Wiring failure between main board MB03B and ER charge magnet valve_x000D_\n- ER charge valve defect_x000D_\n- Main board MB03 defect'},
        'sDiagnosis12_b4': {'Error Code': 'DIA_POP2_DCL_VENT_BP_NORMAL', 'Description': '- Plugs from main board MB03B to ER vent magnet valve unfastened_x000D_\n- Wiring failure between main board MB03B and ER vent magnet valve_x000D_\n- ER vent valve defect_x000D_\n- Main board MB03 defect'},
        'sDiagnosis12_b5': {'Error Code': 'DIA_POP3_BP_NORMAL_MODE', 'Description': '- Plugs from main board MB03B to ER electronic mode magnet valve unfastened_x000D_\n- Wiring failure between main board MB03B and ER electronic mode magnet valve_x000D_\n- ER electronic mode valve defect_x000D_\n- Main board MB03 defect'},
        'sDiagnosis12_b6': {'Error Code': 'DIA_DCL_DEVIATION_BP_BACKUP', 'Description': '- ER pressure sensor defect_x000D_\n- ER charge valve defect_x000D_\n- ER vent valve defect_x000D_\n- ER electronic mode valve defect_x000D_\n- Main board MB03B defect'},
        'sDiagnosis12_b7': {'Error Code': 'DIA_DCL_OFFSET_BP_BACKUP', 'Description': 'ER pressure sensor defect:_x000D_\n- Pressure below -0.2bar OR_x000D_\n- At least expired since pressure dropped below 0.6bar with measured pressure above 0.4bar'},
        'sDiagnosis13_b0': {'Error Code': 'DIA_POP1_DCL_CHARGE_BP_BACKUP', 'Description': '- Plugs from main board MB03B to ER charge magnet valve unfastened_x000D_\n- Wiring failure between main board MB03B and ER charge magnet valve_x000D_\n- ER charge valve defect_x000D_\n- Main board MB03 defect'},
        'sDiagnosis13_b1': {'Error Code': 'DIA_POP2_DCL_VENT_BP_BACKUP', 'Description': '- Plugs from main board MB03B to ER vent magnet valve unfastened_x000D_\n- Wiring failure between main board MB03B and ER vent magnet valve_x000D_\n- ER vent valve defect_x000D_\n- Main board MB03 defect'},
        'sDiagnosis13_b2': {'Error Code': 'DIA_POP3_BP_BACKUP_MODE', 'Description': '- Plugs from main board MB03B to ER electronic mode magnet valve unfastened_x000D_\n- Wiring failure between main board MB03B and ER electronic mode magnet valve_x000D_\n- ER electronic mode valve defect_x000D_\n- Main board MB03 defect'},
        'sDiagnosis13_b3': {'Error Code': 'DIA_POP5_BP_CUT_OUT', 'Description': '- Plugs from main board MB03B to BP cut-out magnet valve unfastened_x000D_\n- Wiring failure between main board MB03B and BP cut-out magnet valve_x000D_\n- BP cut-out valve defect_x000D_\n- Main board MB03 defect'},
        'sDiagnosis13_b4': {'Error Code': 'DIA_POP6_MR_CUT_OUT', 'Description': '- Plugs from main board MB03B to MR cut-out magnet valve unfastened_x000D_\n- Wiring failure between main board MB03B and MR cut-out magnet valve_x000D_\n- MR cut-out valve defect_x000D_\n- Main board MB03 defect'},
        'sDiagnosis13_b5': {'Error Code': 'DIA_POP7_LARGE_CROSS_SEC', 'Description': '- Plugs from main board MB03B to large cross section magnet valve unfastened_x000D_\n- Wiring failure between main board MB03B and large cross section magnet valve_x000D_\n- Large cross section valve defect_x000D_\n- Main board MB03 defect'},
        'sDiagnosis13_b6': {'Error Code': 'DIA_PRC_CONFIG', 'Description': 'The ER pressure controller has detected a configuration fault.'}, 'sDiagnosis13_b7': {'Error Code': 'DIA_PRC_DEVIATION', 'Description': '- Stationary system deviation is greater than 0.5bar_x000D_\n- There are dynamic deviations from the reference model'},
        'sDiagnosis14_b0': {'Error Code': 'DIA_BP_NOT_CUTIN', 'Description': 'The BP cut-out magnet valve is deactivated but the end position switch reports a cut-out BP'}, 'sDiagnosis14_b1': {'Error Code': 'DIA_BP_NOT_CUTOUT', 'Description': 'The BP cut-out magnet valve is activated but the end position switch reports a cut-in BP'},
        'sDiagnosis14_b2': {'Error Code': 'DIA_MR_NOT_CUTIN', 'Description': 'The MR cut-out magnet valve is deactivated but the end position switch reports a cut-out MR'}, 'sDiagnosis14_b3': {'Error Code': 'DIA_MR_NOT_CUTOUT', 'Description': 'The MR cut-out magnet valve is activated but the end position switch reports a cut-in MR'},
        'sDiagnosis14_b4': {'Error Code': 'DIA_LARGE_CS_NOT_OPEN', 'Description': 'The large cross section magnet valve is activated but the end position switch reports a normal cross section'},
        'sDiagnosis14_b5': {'Error Code': 'DIA_LARGE_CS_NOT_CLOSED', 'Description': 'The large cross section magnet valve is deactivated but the end position switch reports a large cross section'},
        'sDiagnosis14_b6': {'Error Code': 'DIA_BP_NormalModeDisturbed', 'Description': 'The BP is generated by the normal mode but this mode is been disturbed'},
        'sDiagnosis14_b7': {'Error Code': 'DIA_BP_BackupModeDisturbed', 'Description': 'The BP is generated by the backup mode but this mode is been disturbed'},
        'sDiagnosis15_b0': {'Error Code': 'DIA_PB_FAULTAPPLIED1', 'Description': 'Parking Brake not applied despite parking brake command.'},
        'sDiagnosis15_b1': {'Error Code': 'DIA_PB_ISOINCOHERENCE1', 'Description': 'Parking brake Not Isolated_x000D_\nPossible problems in the electric system._x000D_\n'},
        'sDiagnosis15_b2': {'Error Code': 'DIA_SAND_FAIL', 'Description': 'There is no sanding pressure despite sanding request.'},
        'sDiagnosis15_b3': {'Error Code': 'DIA_SAND_REQ_UNDUE', 'Description': 'Sanding request in not sanding allowed conditions '},
        'sDiagnosis15_b4': {'Error Code': 'DIA_IC_NORMALBACKUP_DISCREP', 'Description': 'Hardwired signals read different position of Normal / Backup control'},
        'sDiagnosis15_b5': {'Error Code': 'DIA_ACTIVECAB_HW_DISCREP', 'Description': 'Discrepancy between Active Cab hardwired signals'},
        'sDiagnosis15_b6': {'Error Code': 'DIA_ACTIVECAB_SW_DISCREP', 'Description': 'Discrepancy between Active Cab signals. Two or more cabins active.'},
        'sDiagnosis15_b7': {'Error Code': 'DIA_DBH_DISCREP', 'Description': 'Hardwired signals read different positions of the DBH manipulator'},
        'sDiagnosis16_b0': {'Error Code': 'DIA_BP_PRESS_DISCREP', 'Description': 'BP pressure sensors read different pressure values'},
        'sDiagnosis16_b1': {'Error Code': 'DIA_MR_PRESS_DISCREP', 'Description': 'MR pressure sensors read different pressure values'},
        'sDiagnosis16_b2': {'Error Code': 'DIA_TL_EM_DISCREP', 'Description': 'Hardwired signals read different emergency indications between both BCUs in car.'},
        'sDiagnosis16_b3': {'Error Code': 'DIA_PRMG_POS_IMPLAUS', 'Description': 'Hardwired signals read an implausible combination of P-R-R+Mg position lever'},
        'sDiagnosis16_b4': {'Error Code': 'DIA_PR_VALVE', 'Description': '- P-R-R+Mg lever in P position and P-R magnet valve in R position_x000D_\n- P-R-R+Mg lever in R or R+Mg position and P-R magnet valve in P position'},
        'sDiagnosis16_b5': {'Error Code': 'DIA_POST_EX', 'Description': '696 hous have been elapsed since the last power on of the BCU.'},
        'sDiagnosis16_b6': {'Error Code': 'DIA_DBVFULLBRAKE', 'Description': 'No pressure is been applied under manipulator D11 direct brake demand.'},
        'sDiagnosis16_b7': {'Error Code': 'DIA_LOW_MRP', 'Description': 'MRP pressure is below the defined range.'},
        'sDiagnosis17_b0': {'Error Code': 'DIA_PB_FAULTAPPLIED2', 'Description': 'Parking Brake not applied despite parking brake command.'},
        'sDiagnosis17_b1': {'Error Code': 'DIA_PB_ISOINCOHERENCE2', 'Description': 'Parking brake Not Isolated_x000D_\nPossible problems in the electric system._x000D_\n'},
        'sDiagnosis17_b2': {'Error Code': 'Reserved', 'Description': None}, 'sDiagnosis17_b3': {'Error Code': 'Reserved', 'Description': None},
        'sDiagnosis17_b4': {'Error Code': 'DIA_LOW_R_PRESS', 'Description': 'Brake R pressure is below the defined range.'},
        'sDiagnosis17_b5': {'Error Code': 'DIA_LOGIC_TIMEOUT_4_WSP', 'Description': '- Maximum admissible actuation time reached:_x000D_\n- Very low adhesion value between wheel and rail_x000D_\n- Anti-skid valve defect_x000D_\n- Speed sensor defect_x000D_\n- Main board MB03B defect'},
        'sDiagnosis17_b6': {'Error Code': 'DIA_LOCKED_3_DIAG_WSP', 'Description': '- Very low adhesion value between wheel and rail_x000D_\n- Very high slide between wheel and rail over long period of time_x000D_\n- Anti-skid valve defect_x000D_\n- Speed sensor defect_x000D_\n- Main board MB03B defect'},
        'sDiagnosis17_b7': {'Error Code': 'DIA_LOCKED_4_DIAG_WSP', 'Description': '- Very low adhesion value between wheel and rail_x000D_\n- Very high slide between wheel and rail over long period of time_x000D_\n- Anti-skid valve defect_x000D_\n- Speed sensor defect_x000D_\n- Main board MB03B defect'},
        'sDiagnosis18_b0': {'Error Code': 'DIA_SPEED_SENSOR_1_WARNING_WSP', 'Description': 'Warning (possible malfunction) of the speed sensor 1: after a deep and continous analysis (values vs time) of the signal of the speed sensor 1, a suspicious behavior has been detected.'},
        'sDiagnosis18_b1': {'Error Code': 'DIA_SPEED_SENSOR_2_WARNING_WSP', 'Description': 'Warning (possible malfunction) of the speed sensor 2: after a deep and continous analysis (values vs time) of the signal of the speed sensor 2, a suspicious behavior has been detected.'},
        'sDiagnosis18_b2': {'Error Code': 'DIA_SPEED_SENSOR_3_WARNING_WSP', 'Description': 'Warning (possible malfunction) of the speed sensor 3: after a deep and continous analysis (values vs time) of the signal of the speed sensor 3, a suspicious behavior has been detected.'},
        'sDiagnosis18_b3': {'Error Code': 'DIA_SPEED_SENSOR_4_WARNING_WSP', 'Description': 'Warning (possible malfunction) of the speed sensor 4: after a deep and continous analysis (values vs time) of the signal of the speed sensor 4, a suspicious behavior has been detected.'},
        'sDiagnosis18_b4': {'Error Code': 'DIA_CAN_COMM_MB03B_X6_NO_TX', 'Description': 'Communication Board CB09F no longer receives data from the Main Board MB03B.'},
        'sDiagnosis18_b5': {'Error Code': 'DIA_CAN_COMM_MB03B_X5_NO_TX', 'Description': 'Communication Board CB09F no longer receives data from the Main Board MB03B.'},
        'sDiagnosis18_b6': {'Error Code': 'DIA_CAN_COMM_MB03B_X4_NO_TX', 'Description': 'Communication Board CB09F no longer receives data from the Main Board MB03B.'},
        'sDiagnosis18_b7': {'Error Code': 'DIA_CAN_COMM_EB01B_X8_NO_TX', 'Description': 'Main Board MB03B no longer receives data from the Extension Board EB01B.'},
        'sDiagnosis19_b0': {'Error Code': 'DIA_CAN_COMM_EB01B_X9_NO_TX', 'Description': 'Main Board MB03B no longer receives data from the Extension Board EB01B.'},
        'sDiagnosis19_b1': {'Error Code': 'DIA_CAN_COMM_EB02B_X7_NO_TX', 'Description': 'Main Board MB03B no longer receives data from the Extension Board EB02B.'},
        'sDiagnosis19_b2': {'Error Code': 'DIA_HYDRAULIC_LOWER_C_1', 'Description': 'Low cylinder hydraulic pressure. Brake may not be applied'},
        'sDiagnosis19_b3': {'Error Code': 'DIA_HYDRAULIC_LOWER_C_2', 'Description': 'Low cylinder hydraulic pressure. Brake may not be applied'},
        'sDiagnosis19_b4': {'Error Code': 'DIA_HYDRAULIC_HIGHER_C_1', 'Description': 'High cylinder hydraulic pressure. Brake may not be released'},
        'sDiagnosis19_b5': {'Error Code': 'DIA_HYDRAULIC_HIGHER_C_2', 'Description': 'High cylinder hydraulic pressure. Brake may not be released'},
        'sDiagnosis19_b6': {'Error Code': 'DIA_CAN_COMM_MB03B_Y6_NO_TX', 'Description': 'Communication Board CB09F no longer receives data from the Main Board MB03B in other BCU.'},
        'sDiagnosis19_b7': {'Error Code': 'DIA_CAN_COMM_MB03B_Y4_NO_TX', 'Description': 'Communication Board CB09F no longer receives data from the Main Board MB03B in other BCU.'},
        'sDiagnosis20_b0': {'Error Code': 'DIA_DBH_POS', 'Description': 'DBH Failure'},
        'sDiagnosis20_b1': {'Error Code': 'DIA_CAN_COMM_MB03B_Y5_NO_TX', 'Description': 'Communication Board CB09F no longer receives data from the Main Board MB03B in other BCU.'},
        'sDiagnosis20_b2': {'Error Code': 'Reserved', 'Description': None},
        'sDiagnosis20_b3': {'Error Code': 'Reserved', 'Description': None},
        'sDiagnosis20_b4': {'Error Code': 'DIA_VALVE1_WSP', 'Description': 'Antislide valve 1 cannot control correctly the output pressure.'},
        'sDiagnosis20_b5': {'Error Code': 'DIA_VALVE2_WSP', 'Description': 'Antislide valve 2 cannot control correctly the output pressure.'},
        'sDiagnosis20_b6': {'Error Code': 'DIA_VALVE3_WSP', 'Description': 'Antislide valve 3 cannot control correctly the output pressure.'},
        'sDiagnosis20_b7': {'Error Code': 'DIA_VALVE4_WSP', 'Description': 'Antislide valve 4 cannot control correctly the output pressure.'},
        'sDiagnosis21_b0': {'Error Code': 'DIA_BrakeEP_SigON_UIC', 'Description': 'Error while activating the ep brake signal'},
        'sDiagnosis21_b1': {'Error Code': 'DIA_BrakeEP_SigOFF_UIC', 'Description': 'Error while deactivating the ep brake signal'},
        'sDiagnosis21_b2': {'Error Code': 'DIA_ReleaseEP_SigON_UIC', 'Description': 'Error while activating the ep release signal'},
        'sDiagnosis21_b3': {'Error Code': 'DIA_ReleaseEP_SigOFF_UIC', 'Description': 'Error while deactivating the ep release signal'},
        'sDiagnosis21_b4': {'Error Code': 'DIA_EPLoop_R_open', 'Description': 'Meassurement of the ep loop detected a resistor value bigger than the upper limit of the "normal condition" (SEP1)'},
        'sDiagnosis21_b5': {'Error Code': 'DIA_EPLoop_R_short', 'Description': 'Meassurement of the ep loop detected a resistor value smaller than the lower limit of the "normal condition" (SEP1)'},
        'sDiagnosis21_b6': {'Error Code': 'DIA_EPBrake_Train_SigOFF', 'Description': 'ep brake disabled but a signal as been detected on the ep brake train line.'},
        'sDiagnosis21_b7': {'Error Code': 'DIA_EPRelease_Train_SigOFF', 'Description': 'ep brake disabled but a signal as been detected on the ep release train line.'},
        'sDiagnosis22_b0': {'Error Code': 'DIA_EBOLoop_R_open', 'Description': 'Meassurement of the EBO loop detected a resistor value bigger than the upper limit of the "normal condition" (SSA1)'},
        'sDiagnosis22_b1': {'Error Code': 'DIA_EBOLoop_R_short', 'Description': 'Meassurement of the EBO loop detected that the EBO loop is disturbed (SSA5)'},
        'sDiagnosis22_b2': {'Error Code': 'DIA_EBO_Train_OFF', 'Description': 'EBO according UIC 541-5 disabled but a signal has been detected on the EBO train line'},
        'sDiagnosis22_b3': {'Error Code': 'DIA_EBO_SigON', 'Description': 'Error while activating the EBO signal'},
        'sDiagnosis22_b4': {'Error Code': 'DIA_EBO_SigOFF', 'Description': 'Error while deactivating the EBO signal'},
        'sDiagnosis22_b5': {'Error Code': 'DIA_Ubatt', 'Description': 'Battery voltage in one coach fell off'},
        'sDiagnosis22_b6': {'Error Code': 'DIA_ContEBO_SSAON', 'Description': 'Error while activating the continous EBO signal (SSA)'},
        'sDiagnosis22_b7': {'Error Code': 'DIA_ContEBO_SSAOFF', 'Description': 'Error while deactivating the continous EBO signal (SSA)'},
        'sDiagnosis23_b0': {'Error Code': 'DIA_ContEBO_SigON', 'Description': 'Error while activating the continous EBO signal'},
        'sDiagnosis23_b1': {'Error Code': 'DIA_ContEBO_SigOFF', 'Description': 'Error while deactivating the continous EBO signal'},
        'sDiagnosis23_b2': {'Error Code': 'DIA_ContEBO_Train_OFF', 'Description': 'EBO according UIC 541-6 disabled but a signal has been detected on the EBO train line'},
        'bDIBA_Train_S2': {'Error Code': 'DIBA_Train_S2', 'Description': 'Improperly Brake Applied detected in any train wheelsets (only in Loco and extreme cars)'},
        'bDIMGA_Train_S2': {'Error Code': 'DIMGA_Train_S2', 'Description': 'Improperly MG brake Applied detected in any train car (only Loco and extreme cars)'},
        'bDNRA_Notlocked': {'Error Code': 'DNRA_Notlocked1', 'Description': 'Wheelset 1 not locked'},
        'bDNRA_Notlocked2': {'Error Code': 'DNRA_Notlocked2', 'Description': 'Wheelset 2 not locked'},
        'bDNRA_Notlocked': {'Error Code': 'NRA detected (locked) in any wheelset loco/car (all cars except pmr)'},
        'bDIMGA': {'Error Code': 'DIMGA', 'Description': 'Improperly MTB applied'},
        'bPBA_Speed': {'Error Code': 'PBA_Speed', 'Description': 'Parking Applied with Speed > 5 kmh'},
        'bDIMGA_NOK': {'Error Code': 'DIMGA_NOK', 'Description': 'Function DIMGA not available'},
        'bPBA_Speed_NOK': {'Error Code': 'PBA_Speed_NOK', 'Description': 'Function PBA_Speed not available'},
        'bDIBA_Train_S2_NOK': {'Error Code': 'DIBA_Train_S2_NOK', 'Description': 'Function DIBA_Train not available'},
        'bDNRA_OK': {'Error Code': 'DNRA_OK', 'Description': 'Function DNRA available'},
        'DIA_BOARD_EB02B_07': {'Variable': 'sDiagnosis01_b0', 'Description': 'Malfunction Board EB02B Node 07 in BCU B9x '},
        'DIA_BOARDCODING_EB02B_07': {'Variable': 'sDiagnosis01_b1', 'Description': 'The board coding is not correct: either the mode or the node information coded does not comply with the expected codification for the board'},
        'DIA_CAN_COMM_EB02B_07': {'Variable': 'sDiagnosis01_b2', 'Description': 'Internal CAN Communications error'},
        'DIA_BOARD_EB01B_08': {'Variable': 'sDiagnosis01_b3', 'Description': 'Malfunction Board EB01B Node 08 in BCU B9x '},
        'DIA_BOARDCODING_EB01B_08': {'Variable': 'sDiagnosis01_b4', 'Description': 'The board coding is not correct: either the mode or the node information coded does not comply with the expected codification for the board'},
        'DIA_CAN_COMM_EB01B_08': {'Variable': 'sDiagnosis01_b5', 'Description': 'Internal CAN Communications error'},
        'DIA_BOARD_EB01B_09': {'Variable': 'sDiagnosis01_b6', 'Description': 'Malfunction Board EB01B Node 09 in BCU B90 '},
        'DIA_BOARDCODING_EB01B_09': {'Variable': 'sDiagnosis01_b7', 'Description': 'The board coding is not correct: either the mode or the node information coded does not comply with the expected codification for the board'},
        'DIA_CAN_COMM_EB01B_09': {'Variable': 'sDiagnosis02_b0', 'Description': 'Internal CAN Communications error'},
        'DIA_BOARD_MB03B_04': {'Variable': 'sDiagnosis02_b1', 'Description': 'Malfunction Board MB03B Node 04 in BCU B9x '},
        'DIA_BOARDCODING_MB03B_04': {'Variable': 'sDiagnosis02_b2', 'Description': 'The board coding is not correct: either the mode or the node information coded does not comply with the expected codification for the board'},
        'DIA_CAN_COMM_MB03B_04': {'Variable': 'sDiagnosis02_b3', 'Description': 'Internal CAN Communications error'},
        'DIA_BOARD_MB03B_06': {'Variable': 'sDiagnosis02_b4', 'Description': 'Malfunction Board MB03B Node 06 in BCU B9x '},
        'DIA_BOARDCODING_MB03B_06': {'Variable': 'sDiagnosis02_b5', 'Description': 'The board coding is not correct: either the mode or the node information coded does not comply with the expected codification for the board'},
        'DIA_CAN_COMM_MB03B_06': {'Variable': 'sDiagnosis02_b6', 'Description': 'Internal CAN Communications error'},
        'DIA_BOARD_MB03B_05': {'Variable': 'sDiagnosis02_b7', 'Description': 'Malfunction Board MB03B Node 05 in BCU B95 '},
        'DIA_BOARDCODING_MB03B_05': {'Variable': 'sDiagnosis03_b0', 'Description': 'The board coding is not correct: either the mode or the node information coded does not comply with the expected codification for the board'},
        'DIA_CAN_COMM_MB03B_05': {'Variable': 'sDiagnosis03_b1', 'Description': 'Internal CAN Communications error'},
        'DIA_BOARD_CB09F_02': {'Variable': 'sDiagnosis03_b2', 'Description': 'Malfunction Board CB09F Node 02 in BCU B9x '},
        'DIA_BOARDCODING_CB09F_02': {'Variable': 'sDiagnosis03_b3', 'Description': 'The board coding is not correct: either the mode or the node information coded does not comply with the expected codification for the board'},
        'DIA_CAN_COMM_CB09F_02': {'Variable': 'sDiagnosis03_b4', 'Description': 'Internal CAN Communications error'},
        'DIA_BOARDCODING_CB05A_03': {'Variable': 'sDiagnosis03_b6', 'Description': 'The board coding is not correct: either the mode or the node information coded does not comply with the expected codification for the board'},
        'DIA_CAN_COMM_CB05A_03': {'Variable': 'sDiagnosis03_b7', 'Description': 'Internal CAN Communications error'}, 'DIA_EB01B_08_RELAY0': {'Variable': 'sDiagnosis04_b0', 'Description': 'Relay failure: relay output does not operate correctly'},
        'DIA_EB01B_08_RELAY1': {'Variable': 'sDiagnosis04_b1', 'Description': 'Relay failure: relay output does not operate correctly'},
        'DIA_EB01B_08_RELAY2': {'Variable': 'sDiagnosis04_b2', 'Description': 'Relay failure: relay output does not operate correctly'},
        'DIA_EB01B_08_RELAY3': {'Variable': 'sDiagnosis04_b3', 'Description': 'Relay failure: relay output does not operate correctly'},
        'DIA_EB01B_08_RELAY4': {'Variable': 'sDiagnosis04_b4', 'Description': 'Relay failure: relay output does not operate correctly'},
        'DIA_EB01B_08_RELAY5': {'Variable': 'sDiagnosis04_b5', 'Description': 'Relay failure: relay output does not operate correctly'},
        'DIA_EB01B_08_RELAY6': {'Variable': 'sDiagnosis04_b6', 'Description': 'Relay failure: relay output does not operate correctly'},
        'DIA_EB01B_08_RELAY7': {'Variable': 'sDiagnosis04_b7', 'Description': 'Relay failure: relay output does not operate correctly'},
        'DIA_EB01B_09_RELAY0': {'Variable': 'sDiagnosis05_b0', 'Description': 'Relay failure: relay output does not operate correctly'},
        'DIA_EB01B_09_RELAY1': {'Variable': 'sDiagnosis05_b1', 'Description': 'Relay failure: relay output does not operate correctly'},
        'DIA_EB01B_09_RELAY2': {'Variable': 'sDiagnosis05_b2', 'Description': 'Relay failure: relay output does not operate correctly'},
        'DIA_EB01B_09_RELAY3': {'Variable': 'sDiagnosis05_b3', 'Description': 'Relay failure: relay output does not operate correctly'},
        'DIA_EB01B_09_RELAY4': {'Variable': 'sDiagnosis05_b4', 'Description': 'Relay failure: relay output does not operate correctly'},
        'DIA_EB01B_09_RELAY5': {'Variable': 'sDiagnosis05_b5', 'Description': 'Relay failure: relay output does not operate correctly'},
        'DIA_EB01B_09_RELAY6': {'Variable': 'sDiagnosis05_b6', 'Description': 'Relay failure: relay output does not operate correctly'},
        'DIA_EB01B_09_RELAY7': {'Variable': 'sDiagnosis05_b7', 'Description': 'Relay failure: relay output does not operate correctly'},
        'DIA_70_WSP': {'Variable': 'sDiagnosis06_b0', 'Description': 'Cumulative error: all the speed sensors of car are in fault.'},
        'DIA_72_WSP': {'Variable': 'sDiagnosis06_b1', 'Description': 'Cumulative error: WSP errors in one axle (bogie) or wheel (rodal)'},
        'DIA_73_WSP': {'Variable': 'sDiagnosis06_b2', 'Description': 'Cumulative error: WSP errors in one axle (bogie) or wheel (rodal)'},
        'DIA_TIMEOUT_1_WSP': {'Variable': 'sDiagnosis06_b3', 'Description': '- Mechanical failure in anti-skid valve (WSP is not able to correct a slide)_x000D_\n- Failure in speed signal_x000D_\n- Very low adhesion'},
        'DIA_TIMEOUT_2_WSP': {'Variable': 'sDiagnosis06_b4', 'Description': '- Mechanical failure in anti-skid valve (WSP is not able to correct a slide)_x000D_\n- Failure in speed signal_x000D_\n- Very low adhesion'},
        'DIA_TIMEOUT_3_WSP': {'Variable': 'sDiagnosis06_b5', 'Description': '- Mechanical failure in anti-skid valve (WSP is not able to correct a slide)\n- Failure in speed signal\n- Very low adhesion'},
        'DIA_FSI_1_WSP': {'Variable': 'sDiagnosis06_b6', 'Description': '“Short circuit/Open circuit” also called mean-voltage error. Detected by checking that the mean voltage/current value of the speed sensor signal is out of range.'},
        'DIA_FSI_2_WSP': {'Variable': 'sDiagnosis06_b7', 'Description': '“Short circuit/Open circuit” also called mean-voltage error. Detected by checking that the mean voltage/current value of the speed sensor signal is out of range.'},
        'DIA_FSI_3_WSP': {'Variable': 'sDiagnosis07_b0', 'Description': '“Short circuit/Open circuit” also called mean-voltage error. Detected by checking that the mean voltage/current value of the speed sensor signal is out of range.'},
        'DIA_FSI_4_WSP': {'Variable': 'sDiagnosis07_b1', 'Description': '“Short circuit/Open circuit” also called mean-voltage error. Detected by checking that the mean voltage/current value of the speed sensor signal is out of range.'},
        'DIA_DV_1_WSP': {'Variable': 'sDiagnosis07_b2', 'Description': 'Failure in plausibility of speed signal. This means that the speed signal is giving values that are not phisically acceptable.'},
        'DIA_DV_2_WSP': {'Variable': 'sDiagnosis07_b3', 'Description': 'Failure in plausibility of speed signal. This means that the speed signal is giving values that are not phisically acceptable.'},
        'DIA_DV_3_WSP': {'Variable': 'sDiagnosis07_b4', 'Description': 'Failure in plausibility of speed signal. This means that the speed signal is giving values that are not phisically acceptable.'},
        'DIA_DV_4_WSP': {'Variable': 'sDiagnosis07_b5', 'Description': 'Failure in plausibility of speed signal. This means that the speed signal is giving values that are not phisically acceptable.'},
        'DIA_SHORT_VALVE1_WSP': {'Variable': 'sDiagnosis07_b6', 'Description': 'ShortCut detected in the anti-skid valve circuits'},
        'DIA_SHORT_VALVE2_WSP': {'Variable': 'sDiagnosis07_b7', 'Description': 'ShortCut detected in the anti-skid valve circuits'},
        'DIA_SHORT_VALVE3_WSP': {'Variable': 'sDiagnosis08_b0', 'Description': 'ShortCut detected in the anti-skid valve circuits'},
        'DIA_OPEN_VALVE1_WSP': {'Variable': 'sDiagnosis08_b1', 'Description': 'Open Circuit detected in the anti-skid valve circuits'},
        'DIA_OPEN_VALVE2_WSP': {'Variable': 'sDiagnosis08_b2', 'Description': 'Open Circuit detected in the anti-skid valve circuits'},
        'DIA_OPEN_VALVE3_WSP': {'Variable': 'sDiagnosis08_b3', 'Description': 'Open Circuit detected in the anti-skid valve circuits'},
        'DIA_UWR_TIMEOUT_1_WSP': {'Variable': 'sDiagnosis08_b4', 'Description': 'Failure in the safety monitoring circuit (whatchdog) detected with a WSP complete test in POP1/2'},
        'DIA_UWR_TIMEOUT_2_WSP': {'Variable': 'sDiagnosis08_b5', 'Description': 'Failure in the safety monitoring circuit (whatchdog) detected with a WSP complete test in POP3/4'},
        'DIA_UWR_TIMEOUT_3_WSP': {'Variable': 'sDiagnosis08_b6', 'Description': 'Failure in the safety monitoring circuit (whatchdog) detected with a WSP complete test in POP5/6'},
        'DIA_LOCKED_1_DIAG_WSP': {'Variable': 'sDiagnosis08_b7', 'Description': '- Very low adhesion value between wheel and rail_x000D_\n- Very high slide between wheel and rail over long period of time_x000D_\n- Anti-skid valve defect_x000D_\n- Speed sensor defect_x000D_\n- Main board MB03B defect'},
        'DIA_LOCKED_2_DIAG_WSP': {'Variable': 'sDiagnosis09_b0', 'Description': '- Very low adhesion value between wheel and rail_x000D_\n- Very high slide between wheel and rail over long period of time_x000D_\n- Anti-skid valve defect_x000D_\n- Speed sensor defect_x000D_\n- Main board MB03B defect'},
        'DIA_LOGIC_TIMEOUT_1_WSP': {'Variable': 'sDiagnosis09_b1', 'Description': '- Maximum admissible actuation time reached:_x000D_\n- Very low adhesion value between wheel and rail_x000D_\n- Anti-skid valve defect_x000D_\n- Speed sensor defect_x000D_\n- Main board MB03B defect'},
        'DIA_LOGIC_TIMEOUT_2_WSP': {'Variable': 'sDiagnosis09_b2', 'Description': '- Maximum admissible actuation time reached:_x000D_\n- Very low adhesion value between wheel and rail_x000D_\n- Anti-skid valve defect_x000D_\n- Speed sensor defect_x000D_\n- Main board MB03B defect'},
        'DIA_LOGIC_TIMEOUT_3_WSP': {'Variable': 'sDiagnosis09_b3', 'Description': '- Maximum admissible actuation time reached:_x000D_\n- Very low adhesion value between wheel and rail_x000D_\n- Anti-skid valve defect_x000D_\n- Speed sensor defect_x000D_\n- Main board MB03B defect'},
        'DIA_WHEELSET_1_WSP': {'Variable': 'sDiagnosis09_b4', 'Description': 'The „Wheelset error“ is an accumulated error which regards the following single WSP errors: 10_E, 11_E, 21_E, 31_E, 41_E, 12_E, 22_E, 32_E, 42_E, 13_E, 14_E, 15_E, 17_E'},
        'DIA_WHEELSET_2_WSP': {'Variable': 'sDiagnosis09_b5', 'Description': 'The „Wheelset error“ is an accumulated error which regards the following single WSP errors: 20_E, 11_E, 21_E, 31_E, 41_E, 12_E, 22_E, 32_E, 42_E, 23_E, 24_E, 25_E, 27_E'},
        'DIA_WHEELSET_3_WSP': {'Variable': 'sDiagnosis09_b6', 'Description': 'The „Wheelset error“ is an accumulated error which regards the following single WSP errors: 30_E, 11_E, 21_E, 31_E, 41_E, 12_E, 22_E, 32_E, 42_E, 33_E, 34_E, 35_E, 37_E'},
        'DIA_WHEELSET_4_WSP': {'Variable': 'sDiagnosis09_b7', 'Description': 'The „Wheelset error“ is an accumulated error which regards the following single WSP errors: 40_E, 11_E, 21_E, 31_E, 41_E, 12_E, 22_E, 32_E, 42_E, 33_E, 34_E, 35_E, 37_E'},
        'DIA_MVB': {'Variable': 'sDiagnosis10_b0', 'Description': 'Malfunction of MVB bus'},
        'DIA_C_PRESS_SENSOR': {'Variable': 'sDiagnosis10_b1', 'Description': 'Cylinder pressure transducer error'},
        'DIA_C_PRESS1_SENSOR': {'Variable': 'sDiagnosis10_b2', 'Description': 'Cylinder pressure transducer error'},
        'DIA_C_PRESS2_SENSOR': {'Variable': 'sDiagnosis10_b3', 'Description': 'Cylinder pressure transducer error'},
        'DIA_T_PRESS_SENSOR': {'Variable': 'sDiagnosis10_b4', 'Description': 'Load (suspension) pressure transducer error'},
        'DIA_R_PRESS_SENSOR': {'Variable': 'sDiagnosis10_b5', 'Description': 'Reservoir pressure transducer error'},
        'DIA_HC_PRESS1_SENSOR': {'Variable': 'sDiagnosis10_b6', 'Description': 'Parking brake hydraulic pressure transducer error'},
        'DIA_HC_PRESS2_SENSOR': {'Variable': 'sDiagnosis10_b7', 'Description': 'Parking brake hydraulic pressure transducer error'},
        'DIA_ER_PRESS_SENSOR': {'Variable': 'sDiagnosis11_b0', 'Description': 'ER pressure transducer error'},
        'DIA_BP_PRESS_SENSOR': {'Variable': 'sDiagnosis11_b1', 'Description': 'BP pressure transducer error'},
        'DIA_MRP_PRESS_SENSOR': {'Variable': 'sDiagnosis11_b2', 'Description': 'MRP pressure transducer error'},
        'DIA_FL_PRESS_SENSOR': {'Variable': 'sDiagnosis11_b3', 'Description': 'MRP pressure transducer error'},
        'DIA_DIR_BRK_PRESS_SENSOR': {'Variable': 'sDiagnosis11_b4', 'Description': 'Direct brake C pressure transducer error'},
        'DIA_SANDING_PRESS_SENSOR': {'Variable': 'sDiagnosis11_b5', 'Description': 'Sanding pressure transducer error'},
        'DIA_DIBA': {'Variable': 'sDiagnosis11_b6', 'Description': 'Brake should be released but brake is applied according to brake pressure monitored.'},
        'DIA_NBA': {'Variable': 'sDiagnosis11_b7', 'Description': 'Brake should not be released but brake is released according to brake pressure monitored.'},
        'DIA_DIMGA': {'Variable': 'sDiagnosis12_b0', 'Description': 'MTB should be released but MTB is applied (low position and energized) according to MTB monitoring.'},
        'DIA_DCL_DEVIATION_BP_NORMAL': {'Variable': 'sDiagnosis12_b1', 'Description': '- ER pressure sensor defect_x000D_\n- ER charge valve defect_x000D_\n- ER vent valve defect_x000D_\n- ER electronic mode valve defect_x000D_\n- Main board MB03B defect'},
        'DIA_DCL_OFFSET_BP_NORMAL': {'Variable': 'sDiagnosis12_b2', 'Description': 'ER pressure sensor defect:\n- Pressure below -0.2bar OR\n- At least expired since pressure dropped below 0.6bar with measured pressure above 0.4bar'},
        'DIA_POP1_DCL_CHARGE_BP_NORMAL': {'Variable': 'sDiagnosis12_b3', 'Description': '- Plugs from main board MB03B to ER charge magnet valve unfastened_x000D_\n- Wiring failure between main board MB03B and ER charge magnet valve_x000D_\n- ER charge valve defect_x000D_\n- Main board MB03 defect'},
        'DIA_POP2_DCL_VENT_BP_NORMAL': {'Variable': 'sDiagnosis12_b4', 'Description': '- Plugs from main board MB03B to ER vent magnet valve unfastened_x000D_\n- Wiring failure between main board MB03B and ER vent magnet valve_x000D_\n- ER vent valve defect_x000D_\n- Main board MB03 defect'},
        'DIA_POP3_BP_NORMAL_MODE': {'Variable': 'sDiagnosis12_b5', 'Description': '- Plugs from main board MB03B to ER electronic mode magnet valve unfastened_x000D_\n- Wiring failure between main board MB03B and ER electronic mode magnet valve_x000D_\n- ER electronic mode valve defect_x000D_\n- Main board MB03 defect'},
        'DIA_DCL_DEVIATION_BP_BACKUP': {'Variable': 'sDiagnosis12_b6', 'Description': '- ER pressure sensor defect_x000D_\n- ER charge valve defect_x000D_\n- ER vent valve defect_x000D_\n- ER electronic mode valve defect_x000D_\n- Main board MB03B defect'},
        'DIA_DCL_OFFSET_BP_BACKUP': {'Variable': 'sDiagnosis12_b7', 'Description': 'ER pressure sensor defect:_x000D_\n- Pressure below -0.2bar OR_x000D_\n- At least expired since pressure dropped below 0.6bar with measured pressure above 0.4bar'},
        'DIA_POP1_DCL_CHARGE_BP_BACKUP': {'Variable': 'sDiagnosis13_b0', 'Description': '- Plugs from main board MB03B to ER charge magnet valve unfastened_x000D_\n- Wiring failure between main board MB03B and ER charge magnet valve_x000D_\n- ER charge valve defect_x000D_\n- Main board MB03 defect'},
        'DIA_POP2_DCL_VENT_BP_BACKUP': {'Variable': 'sDiagnosis13_b1', 'Description': '- Plugs from main board MB03B to ER vent magnet valve unfastened_x000D_\n- Wiring failure between main board MB03B and ER vent magnet valve_x000D_\n- ER vent valve defect_x000D_\n- Main board MB03 defect'},
        'DIA_POP3_BP_BACKUP_MODE': {'Variable': 'sDiagnosis13_b2', 'Description': '- Plugs from main board MB03B to ER electronic mode magnet valve unfastened_x000D_\n- Wiring failure between main board MB03B and ER electronic mode magnet valve_x000D_\n- ER electronic mode valve defect_x000D_\n- Main board MB03 defect'},
        'DIA_POP5_BP_CUT_OUT': {'Variable': 'sDiagnosis13_b3', 'Description': '- Plugs from main board MB03B to BP cut-out magnet valve unfastened_x000D_\n- Wiring failure between main board MB03B and BP cut-out magnet valve_x000D_\n- BP cut-out valve defect_x000D_\n- Main board MB03 defect'},
        'DIA_POP6_MR_CUT_OUT': {'Variable': 'sDiagnosis13_b4', 'Description': '- Plugs from main board MB03B to MR cut-out magnet valve unfastened_x000D_\n- Wiring failure between main board MB03B and MR cut-out magnet valve_x000D_\n- MR cut-out valve defect_x000D_\n- Main board MB03 defect'},
        'DIA_POP7_LARGE_CROSS_SEC': {'Variable': 'sDiagnosis13_b5', 'Description': '- Plugs from main board MB03B to large cross section magnet valve unfastened_x000D_\n- Wiring failure between main board MB03B and large cross section magnet valve_x000D_\n- Large cross section valve defect_x000D_\n- Main board MB03 defect'},
        'DIA_PRC_CONFIG': {'Variable': 'sDiagnosis13_b6', 'Description': 'The ER pressure controller has detected a configuration fault.'}, 'DIA_PRC_DEVIATION': {'Variable': 'sDiagnosis13_b7', 'Description': '- Stationary system deviation is greater than 0.5bar_x000D_\n- There are dynamic deviations from the reference model'},
        'DIA_BP_NOT_CUTIN': {'Variable': 'sDiagnosis14_b0', 'Description': 'The BP cut-out magnet valve is deactivated but the end position switch reports a cut-out BP'}, 'DIA_BP_NOT_CUTOUT': {'Variable': 'sDiagnosis14_b1', 'Description': 'The BP cut-out magnet valve is activated but the end position switch reports a cut-in BP'},
        'DIA_MR_NOT_CUTIN': {'Variable': 'sDiagnosis14_b2', 'Description': 'The MR cut-out magnet valve is deactivated but the end position switch reports a cut-out MR'}, 'DIA_MR_NOT_CUTOUT': {'Variable': 'sDiagnosis14_b3', 'Description': 'The MR cut-out magnet valve is activated but the end position switch reports a cut-in MR'},
        'DIA_LARGE_CS_NOT_OPEN': {'Variable': 'sDiagnosis14_b4', 'Description': 'The large cross section magnet valve is activated but the end position switch reports a normal cross section'}, 'DIA_LARGE_CS_NOT_CLOSED': {'Variable': 'sDiagnosis14_b5', 'Description': 'The large cross section magnet valve is deactivated but the end position switch reports a large cross section'},
        'DIA_BP_NormalModeDisturbed': {'Variable': 'sDiagnosis14_b6', 'Description': 'The BP is generated by the normal mode but this mode is been disturbed'}, 'DIA_BP_BackupModeDisturbed': {'Variable': 'sDiagnosis14_b7', 'Description': 'The BP is generated by the backup mode but this mode is been disturbed'},
        'DIA_PB_FAULTAPPLIED1': {'Variable': 'sDiagnosis15_b0', 'Description': 'Parking Brake not applied despite parking brake command.'},
        'DIA_PB_ISOINCOHERENCE1': {'Variable': 'sDiagnosis15_b1', 'Description': 'Parking brake Not Isolated_x000D_\nPossible problems in the electric system._x000D_\n'},
        'DIA_SAND_FAIL': {'Variable': 'sDiagnosis15_b2', 'Description': 'There is no sanding pressure despite sanding request.'},
        'DIA_SAND_REQ_UNDUE': {'Variable': 'sDiagnosis15_b3', 'Description': 'Sanding request in not sanding allowed conditions '},
        'DIA_IC_NORMALBACKUP_DISCREP': {'Variable': 'sDiagnosis15_b4', 'Description': 'Hardwired signals read different position of Normal / Backup control'},
        'DIA_ACTIVECAB_HW_DISCREP': {'Variable': 'sDiagnosis15_b5', 'Description': 'Discrepancy between Active Cab hardwired signals'},
        'DIA_ACTIVECAB_SW_DISCREP': {'Variable': 'sDiagnosis15_b6', 'Description': 'Discrepancy between Active Cab signals. Two or more cabins active.'},
        'DIA_DBH_DISCREP': {'Variable': 'sDiagnosis15_b7', 'Description': 'Hardwired signals read different positions of the DBH manipulator'},
        'DIA_BP_PRESS_DISCREP': {'Variable': 'sDiagnosis16_b0', 'Description': 'BP pressure sensors read different pressure values'},
        'DIA_MR_PRESS_DISCREP': {'Variable': 'sDiagnosis16_b1', 'Description': 'MR pressure sensors read different pressure values'},
        'DIA_TL_EM_DISCREP': {'Variable': 'sDiagnosis16_b2', 'Description': 'Hardwired signals read different emergency indications between both BCUs in car.'},
        'DIA_PRMG_POS_IMPLAUS': {'Variable': 'sDiagnosis16_b3', 'Description': 'Hardwired signals read an implausible combination of P-R-R+Mg position lever'},
        'DIA_PR_VALVE': {'Variable': 'sDiagnosis16_b4', 'Description': '- P-R-R+Mg lever in P position and P-R magnet valve in R position_x000D_\n- P-R-R+Mg lever in R or R+Mg position and P-R magnet valve in P position'},
        'DIA_POST_EX': {'Variable': 'sDiagnosis16_b5', 'Description': '696 hous have been elapsed since the last power on of the BCU.'},
        'DIA_DBVFULLBRAKE': {'Variable': 'sDiagnosis16_b6', 'Description': 'No pressure is been applied under manipulator D11 direct brake demand.'},
        'DIA_LOW_MRP': {'Variable': 'sDiagnosis16_b7', 'Description': 'MRP pressure is below the defined range.'},
        'DIA_PB_FAULTAPPLIED2': {'Variable': 'sDiagnosis17_b0', 'Description': 'Parking Brake not applied despite parking brake command.'},
        'DIA_PB_ISOINCOHERENCE2': {'Variable': 'sDiagnosis17_b1', 'Description': 'Parking brake Not Isolated_x000D_\nPossible problems in the electric system._x000D_\n'},
        'Reserved': {'Variable': 'sDiagnosis20_b3', 'Description': None},
        'DIA_LOW_R_PRESS': {'Variable': 'sDiagnosis17_b4', 'Description': 'Brake R pressure is below the defined range.'},
        'DIA_LOGIC_TIMEOUT_4_WSP': {'Variable': 'sDiagnosis17_b5', 'Description': '- Maximum admissible actuation time reached:_x000D_\n- Very low adhesion value between wheel and rail_x000D_\n- Anti-skid valve defect_x000D_\n- Speed sensor defect_x000D_\n- Main board MB03B defect'},
        'DIA_LOCKED_3_DIAG_WSP': {'Variable': 'sDiagnosis17_b6', 'Description': '- Very low adhesion value between wheel and rail_x000D_\n- Very high slide between wheel and rail over long period of time_x000D_\n- Anti-skid valve defect_x000D_\n- Speed sensor defect_x000D_\n- Main board MB03B defect'},
        'DIA_LOCKED_4_DIAG_WSP': {'Variable': 'sDiagnosis17_b7', 'Description': '- Very low adhesion value between wheel and rail_x000D_\n- Very high slide between wheel and rail over long period of time_x000D_\n- Anti-skid valve defect_x000D_\n- Speed sensor defect_x000D_\n- Main board MB03B defect'},
        'DIA_SPEED_SENSOR_1_WARNING_WSP': {'Variable': 'sDiagnosis18_b0', 'Description': 'Warning (possible malfunction) of the speed sensor 1: after a deep and continous analysis (values vs time) of the signal of the speed sensor 1, a suspicious behavior has been detected.'},
        'DIA_SPEED_SENSOR_2_WARNING_WSP': {'Variable': 'sDiagnosis18_b1', 'Description': 'Warning (possible malfunction) of the speed sensor 2: after a deep and continous analysis (values vs time) of the signal of the speed sensor 2, a suspicious behavior has been detected.'},
        'DIA_SPEED_SENSOR_3_WARNING_WSP': {'Variable': 'sDiagnosis18_b2', 'Description': 'Warning (possible malfunction) of the speed sensor 3: after a deep and continous analysis (values vs time) of the signal of the speed sensor 3, a suspicious behavior has been detected.'},
        'DIA_SPEED_SENSOR_4_WARNING_WSP': {'Variable': 'sDiagnosis18_b3', 'Description': 'Warning (possible malfunction) of the speed sensor 4: after a deep and continous analysis (values vs time) of the signal of the speed sensor 4, a suspicious behavior has been detected.'},
        'DIA_CAN_COMM_MB03B_X6_NO_TX': {'Variable': 'sDiagnosis18_b4', 'Description': 'Communication Board CB09F no longer receives data from the Main Board MB03B.'}, 'DIA_CAN_COMM_MB03B_X5_NO_TX': {'Variable': 'sDiagnosis18_b5', 'Description': 'Communication Board CB09F no longer receives data from the Main Board MB03B.'},
        'DIA_CAN_COMM_MB03B_X4_NO_TX': {'Variable': 'sDiagnosis18_b6', 'Description': 'Communication Board CB09F no longer receives data from the Main Board MB03B.'}, 'DIA_CAN_COMM_EB01B_X8_NO_TX': {'Variable': 'sDiagnosis18_b7', 'Description': 'Main Board MB03B no longer receives data from the Extension Board EB01B.'},
        'DIA_CAN_COMM_EB01B_X9_NO_TX': {'Variable': 'sDiagnosis19_b0', 'Description': 'Main Board MB03B no longer receives data from the Extension Board EB01B.'}, 'DIA_CAN_COMM_EB02B_X7_NO_TX': {'Variable': 'sDiagnosis19_b1', 'Description': 'Main Board MB03B no longer receives data from the Extension Board EB02B.'},
        'DIA_HYDRAULIC_LOWER_C_1': {'Variable': 'sDiagnosis19_b2', 'Description': 'Low cylinder hydraulic pressure. Brake may not be applied'}, 'DIA_HYDRAULIC_LOWER_C_2': {'Variable': 'sDiagnosis19_b3', 'Description': 'Low cylinder hydraulic pressure. Brake may not be applied'},
        'DIA_HYDRAULIC_HIGHER_C_1': {'Variable': 'sDiagnosis19_b4', 'Description': 'High cylinder hydraulic pressure. Brake may not be released'}, 'DIA_HYDRAULIC_HIGHER_C_2': {'Variable': 'sDiagnosis19_b5', 'Description': 'High cylinder hydraulic pressure. Brake may not be released'},
        'DIA_CAN_COMM_MB03B_Y6_NO_TX': {'Variable': 'sDiagnosis19_b6', 'Description': 'Communication Board CB09F no longer receives data from the Main Board MB03B in other BCU.'},
        'DIA_CAN_COMM_MB03B_Y4_NO_TX': {'Variable': 'sDiagnosis19_b7', 'Description': 'Communication Board CB09F no longer receives data from the Main Board MB03B in other BCU.'},
        'DIA_DBH_POS': {'Variable': 'sDiagnosis20_b0', 'Description': 'DBH Failure'},
        'DIA_CAN_COMM_MB03B_Y5_NO_TX': {'Variable': 'sDiagnosis20_b1', 'Description': 'Communication Board CB09F no longer receives data from the Main Board MB03B in other BCU.'},
        'DIA_VALVE1_WSP': {'Variable': 'sDiagnosis20_b4', 'Description': 'Antislide valve 1 cannot control correctly the output pressure.'},
        'DIA_VALVE2_WSP': {'Variable': 'sDiagnosis20_b5', 'Description': 'Antislide valve 2 cannot control correctly the output pressure.'},
        'DIA_VALVE3_WSP': {'Variable': 'sDiagnosis20_b6', 'Description': 'Antislide valve 3 cannot control correctly the output pressure.'},
        'DIA_VALVE4_WSP': {'Variable': 'sDiagnosis20_b7', 'Description': 'Antislide valve 4 cannot control correctly the output pressure.'},
        'DIA_BrakeEP_SigON_UIC': {'Variable': 'sDiagnosis21_b0', 'Description': 'Error while activating the ep brake signal'},
        'DIA_BrakeEP_SigOFF_UIC': {'Variable': 'sDiagnosis21_b1', 'Description': 'Error while deactivating the ep brake signal'},
        'DIA_ReleaseEP_SigON_UIC': {'Variable': 'sDiagnosis21_b2', 'Description': 'Error while activating the ep release signal'},
        'DIA_ReleaseEP_SigOFF_UIC': {'Variable': 'sDiagnosis21_b3', 'Description': 'Error while deactivating the ep release signal'},
        'DIA_EPLoop_R_open': {'Variable': 'sDiagnosis21_b4', 'Description': 'Meassurement of the ep loop detected a resistor value bigger than the upper limit of the "normal condition" (SEP1)'},
        'DIA_EPLoop_R_short': {'Variable': 'sDiagnosis21_b5', 'Description': 'Meassurement of the ep loop detected a resistor value smaller than the lower limit of the "normal condition" (SEP1)'},
        'DIA_EPBrake_Train_SigOFF': {'Variable': 'sDiagnosis21_b6', 'Description': 'ep brake disabled but a signal as been detected on the ep brake train line.'},
        'DIA_EPRelease_Train_SigOFF': {'Variable': 'sDiagnosis21_b7', 'Description': 'ep brake disabled but a signal as been detected on the ep release train line.'},
        'DIA_EBOLoop_R_open': {'Variable': 'sDiagnosis22_b0', 'Description': 'Meassurement of the EBO loop detected a resistor value bigger than the upper limit of the "normal condition" (SSA1)'},
        'DIA_EBOLoop_R_short': {'Variable': 'sDiagnosis22_b1', 'Description': 'Meassurement of the EBO loop detected that the EBO loop is disturbed (SSA5)'},
        'DIA_EBO_Train_OFF': {'Variable': 'sDiagnosis22_b2', 'Description': 'EBO according UIC 541-5 disabled but a signal has been detected on the EBO train line'},
        'DIA_EBO_SigON': {'Variable': 'sDiagnosis22_b3', 'Description': 'Error while activating the EBO signal'},
        'DIA_EBO_SigOFF': {'Variable': 'sDiagnosis22_b4', 'Description': 'Error while deactivating the EBO signal'},
        'DIA_Ubatt': {'Variable': 'sDiagnosis22_b5', 'Description': 'Battery voltage in one coach fell off'},
        'DIA_ContEBO_SSAON': {'Variable': 'sDiagnosis22_b6', 'Description': 'Error while activating the continous EBO signal (SSA)'},
        'DIA_ContEBO_SSAOFF': {'Variable': 'sDiagnosis22_b7', 'Description': 'Error while deactivating the continous EBO signal (SSA)'},
        'DIA_ContEBO_SigON': {'Variable': 'sDiagnosis23_b0', 'Description': 'Error while activating the continous EBO signal'},
        'DIA_ContEBO_SigOFF': {'Variable': 'sDiagnosis23_b1', 'Description': 'Error while deactivating the continous EBO signal'},
        'DIA_ContEBO_Train_OFF': {'Variable': 'sDiagnosis23_b2', 'Description': 'EBO according UIC 541-6 disabled but a signal has been detected on the EBO train line'}
        }
        #VARIABLES PARA COMANDAR EN DCU
        self.DCU_COMMANDS_VARS = ['VCUCH_CAN_DS_21A.bSW_CenClosing',
                                  'VCUCH_CAN_DS_21A.bSW_BurnInOn',
                                'VCUCH_CAN_DS_21A.bSW_EnergySav',
                                'VCUCH_CAN_DS_21A.bSW_CleanMode',
                                'VCUCH_CAN_DS_21A.bSW_MaintMode',
                                'VCUCH_CAN_DS_21A.bSW_StandByMode',
                                'VCUCH_CAN_DS_21A.bSW_ReducedStep',
                                'VCUCH_CAN_DS_21A.bSW_CenOpening',
                                'VCUCH_CAN_DS_21C.bSW_CenClosing',
                                'VCUCH_CAN_DS_21C.bSW_BurnInOn',
                                'VCUCH_CAN_DS_21C.bSW_EnergySav',
                                'VCUCH_CAN_DS_21C.bSW_CleanMode',
                                'VCUCH_CAN_DS_21C.bSW_MaintMode',
                                'VCUCH_CAN_DS_21C.bSW_StandByMode',
                                'VCUCH_CAN_DS_21C.bSW_ReducedStep',
                                'VCUCH_CAN_DS_21C.bSW_CenOpening',
        ]
        #VARIABLES DEL LAZO DE PUERTAS / BURNING TEST
        self.DOORS_LOOP_VARS = [
            'DCU_CAN_DS_19A.bStepClosed',
            'DCU_CAN_DS_19C.bStepClosed',
            'DCU_CAN_DS_19A.bClosedLocked',
            'DCU_CAN_DS_19C.bClosedLocked',
            'DCU_CAN_DS_19A.b2RemoteCloseON',
            'DCU_CAN_DS_19C.b2RemoteCloseON',
            'DCU_CAN_DS_19A.bRemoteCloseON',
            'DCU_CAN_DS_19C.bRemoteCloseON',
            'DCU_CAN_DS_19A.bStepOpen',
            'DCU_CAN_DS_19C.bStepOpen',
            'DCU_CAN_DS_19A.bDoorOpen',
            'DCU_CAN_DS_19C.bDoorOpen',
            'DCU_CAN_DS_19A.bEEDoperated',
            'DCU_CAN_DS_19C.bEEDoperated',
            'DCU_CAN_DS_19A.bEADoperated',
            'DCU_CAN_DS_19C.bEADoperated',
            'DCU_CAN_DS_19A.bEmSwOperated',
            'DCU_CAN_DS_19C.bEmSwOperated',
            'DCU_CAN_DS_19A.bDoorOutService',
            'DCU_CAN_DS_19C.bDoorOutService',
            'DCU_CAN_DS_19A.bStepOutService',
            'DCU_CAN_DS_19C.bStepOutService',
            'DCU_CAN_DS_19A.bStepManRelease',
            'DCU_CAN_DS_19C.bStepManRelease',
            'DCU_CAN_DS_19A.bBurninActive',
            'DCU_CAN_DS_19C.bBurninActive',
            'DCU_CAN_DS_19A.bLastBurninNOK',
            'DCU_CAN_DS_19C.bLastBurninNOK',
            'DCU_CAN_DS_19A.bLastBurninOK',
            'DCU_CAN_DS_19C.bLastBurninOK',
            'DCU_CAN_DS_19A.bBurninReady',
            'DCU_CAN_DS_19C.bBurninReady',
            'DCU_CAN_DS_19A.bDiagnostiCodeB',
            'DCU_CAN_DS_19C.bDiagnostiCodeB',
            'DCU_CAN_DS_19A.bDiagnostiCodeA',
            'DCU_CAN_DS_19C.bDiagnostiCodeA',
            'DCU_CAN_DS_19A.bPRMoutside',
            'DCU_CAN_DS_19C.bPRMoutside',
            'DCU_CAN_DS_19A.bPRMinside',
            'DCU_CAN_DS_19C.bPRMinside',
            'DCU_CAN_DS_19A.bEchoOH',
            'DCU_CAN_DS_19C.bEchoOH',
            'DCU_CAN_DS_19A.bEchoV10',
            'DCU_CAN_DS_19C.bEchoV10',
            'DCU_CAN_DS_19A.bEchoV3',
            'DCU_CAN_DS_19C.bEchoV3',
            'DCU_CAN_DS_19A.bEchoStepIn',
            'DCU_CAN_DS_19C.bEchoStepIn',
            'DCU_CAN_DS_19A.bEchoRedStk',
            'DCU_CAN_DS_19C.bEchoRedStk',
            'DCU_CAN_DS_19A.MajorSWrev',
            'DCU_CAN_DS_19C.MajorSWrev',
            'DCU_CAN_DS_19A.MinorSWrev',
            'DCU_CAN_DS_19C.MinorSWrev',
            'DCU_CAN_DS_19A.HWrevision',
            'DCU_CAN_DS_19C.HWrevision',
            'DCU_CAN_DS_19B.bHomogTestFail',
            'DCU_CAN_DS_19D.bHomogTestFail',
            'DCU_CAN_DS_19B.bHomogTestFinhishOk',
            'DCU_CAN_DS_19D.bHomogTestFinhishOk',
            'DCU_CAN_DS_19B.bHomogTestAct',
            'DCU_CAN_DS_19D.bHomogTestAct',
            'DCU_CAN_DS_19B.bStUIC15',
            'DCU_CAN_DS_19D.bStUIC15',
            'DCU_CAN_DS_19B.bStUIC14',
            'DCU_CAN_DS_19D.bStUIC14',
            'DCU_CAN_DS_19B.bStUIC9',
            'DCU_CAN_DS_19D.bStUIC9',
            'DCU_CAN_DS_19B.bStUICLATMode',
            'DCU_CAN_DS_19D.bStUICLATMode',
            'DCU_CAN_DS_19B.bStSafeSt',
            'DCU_CAN_DS_19D.bStSafeSt',
            'DCU_CAN_DS_19B.bStTB0Mode',
            'DCU_CAN_DS_19D.bStTB0Mode',
            'DCU_CAN_DS_19B.bStOBBTBSMode',
            'DCU_CAN_DS_19D.bStOBBTBSMode',
            'DCU_CAN_DS_19B.bActiveRelease',
            'DCU_CAN_DS_19D.bActiveRelease',
            'DCU_CAN_DS_19B.bEnergySaving_Release',
            'DCU_CAN_DS_19D.bEnergySaving_Release',
            'DCU_CAN_DS_29B.CycleCountDoor',
            'DCU_CAN_DS_29D.CycleCountDoor',
            'DCU_CAN_DS_29B.CycleCountStep',
            'DCU_CAN_DS_29D.CycleCountStep',
            'DCU_CAN_DS_19A_Failure_Rate',
            'DCU_CAN_DS_19C_Failure_Rate',
            'VCUCH_CAN_DS_21A.N3_par',
            'VCUCH_CAN_DS_21C.N3_par',
            'DCU_CAN_DS_2D4.N3_feedback',
            'DCU_CAN_DS_2D6.N3_feedback'
        ]
        #VARIABLES PARA LA DIAGNOSIS DE DCU
        self.DCU_DIAGNOSIS = [
                'DCU_CAN_DS_49A.bCdiagCode1','DCU_CAN_DS_49C.bCdiagCode1',
                'DCU_CAN_DS_49A.bCdiagCode2','DCU_CAN_DS_49C.bCdiagCode2',
                'DCU_CAN_DS_49A.bCdiagCode3','DCU_CAN_DS_49C.bCdiagCode3',
                'DCU_CAN_DS_49A.bCdiagCode4','DCU_CAN_DS_49C.bCdiagCode4',
                'DCU_CAN_DS_49A.bCdiagCode5','DCU_CAN_DS_49C.bCdiagCode5',
                'DCU_CAN_DS_49A.bCdiagCode6','DCU_CAN_DS_49C.bCdiagCode6',
                'DCU_CAN_DS_49A.bCdiagCode7','DCU_CAN_DS_49C.bCdiagCode7',
                'DCU_CAN_DS_49A.bCdiagCode8','DCU_CAN_DS_49C.bCdiagCode8',
                'DCU_CAN_DS_49A.bCdiagCode9','DCU_CAN_DS_49C.bCdiagCode9',
                'DCU_CAN_DS_49A.bCdiagCode10','DCU_CAN_DS_49C.bCdiagCode10',
                'DCU_CAN_DS_49A.bCdiagCode12','DCU_CAN_DS_49C.bCdiagCode12',
                'DCU_CAN_DS_49A.bCdiagCode13','DCU_CAN_DS_49C.bCdiagCode13',
                'DCU_CAN_DS_49A.bCdiagCode14','DCU_CAN_DS_49C.bCdiagCode14',
                'DCU_CAN_DS_49A.bCdiagCode15','DCU_CAN_DS_49C.bCdiagCode15',
                'DCU_CAN_DS_49A.bCdiagCode16','DCU_CAN_DS_49C.bCdiagCode16',
                'DCU_CAN_DS_49A.bCdiagCode17','DCU_CAN_DS_49C.bCdiagCode17',
                'DCU_CAN_DS_49A.bCdiagCode18','DCU_CAN_DS_49C.bCdiagCode18',
                'DCU_CAN_DS_49A.bCdiagCode19','DCU_CAN_DS_49C.bCdiagCode19',
                'DCU_CAN_DS_49A.bCdiagCode20','DCU_CAN_DS_49C.bCdiagCode20',
                'DCU_CAN_DS_49A.bCdiagCode21','DCU_CAN_DS_49C.bCdiagCode21',
                'DCU_CAN_DS_49A.bCdiagCode22','DCU_CAN_DS_49C.bCdiagCode22',
                'DCU_CAN_DS_49A.bCdiagCode23','DCU_CAN_DS_49C.bCdiagCode23',
                'DCU_CAN_DS_49A.bCdiagCode24','DCU_CAN_DS_49C.bCdiagCode24',
                'DCU_CAN_DS_49A.bCdiagCode25','DCU_CAN_DS_49C.bCdiagCode25',
                'DCU_CAN_DS_49A.bCdiagCode26','DCU_CAN_DS_49C.bCdiagCode26',
                'DCU_CAN_DS_49A.bCdiagCode28','DCU_CAN_DS_49C.bCdiagCode28',
                'DCU_CAN_DS_49A.bCdiagCode29','DCU_CAN_DS_49C.bCdiagCode29',
                'DCU_CAN_DS_49A.bCdiagCode30','DCU_CAN_DS_49C.bCdiagCode30',
                'DCU_CAN_DS_49A.bCdiagCode31','DCU_CAN_DS_49C.bCdiagCode31',
                'DCU_CAN_DS_49A.bCdiagCode32','DCU_CAN_DS_49C.bCdiagCode32',
                'DCU_CAN_DS_49A.bCdiagCode33','DCU_CAN_DS_49C.bCdiagCode33',
                'DCU_CAN_DS_49A.bCdiagCode34','DCU_CAN_DS_49C.bCdiagCode34',
                'DCU_CAN_DS_49A.bCdiagCode35','DCU_CAN_DS_49C.bCdiagCode35',
                'DCU_CAN_DS_49A.bCdiagCode36','DCU_CAN_DS_49C.bCdiagCode36',
                'DCU_CAN_DS_49A.bCdiagCode37','DCU_CAN_DS_49C.bCdiagCode37',
                'DCU_CAN_DS_49A.bCdiagCode38','DCU_CAN_DS_49C.bCdiagCode38',
                'DCU_CAN_DS_49A.bCdiagCode39','DCU_CAN_DS_49C.bCdiagCode39',
                'DCU_CAN_DS_49A.bCdiagCode40','DCU_CAN_DS_49C.bCdiagCode40',
                'DCU_CAN_DS_49A.bCdiagCode41','DCU_CAN_DS_49C.bCdiagCode41',
                'DCU_CAN_DS_49A.bCdiagCode42','DCU_CAN_DS_49C.bCdiagCode42',
                'DCU_CAN_DS_49A.bCdiagCode43','DCU_CAN_DS_49C.bCdiagCode43',
                'DCU_CAN_DS_49A.bCdiagCode44','DCU_CAN_DS_49C.bCdiagCode44',
                'DCU_CAN_DS_49A.bCdiagCode45','DCU_CAN_DS_49C.bCdiagCode45',
                'DCU_CAN_DS_49A.bCdiagCode46','DCU_CAN_DS_49C.bCdiagCode46',
                'DCU_CAN_DS_49A.bCdiagCode47','DCU_CAN_DS_49C.bCdiagCode47',
                'DCU_CAN_DS_49A.bCdiagCode48','DCU_CAN_DS_49C.bCdiagCode48',
                'DCU_CAN_DS_49A.bCdiagCode49','DCU_CAN_DS_49C.bCdiagCode49',
                'DCU_CAN_DS_49A.bCdiagCode50','DCU_CAN_DS_49C.bCdiagCode50',
                'DCU_CAN_DS_49A.bCdiagCode51','DCU_CAN_DS_49C.bCdiagCode51',
                'DCU_CAN_DS_49A.bCdiagCode52','DCU_CAN_DS_49C.bCdiagCode52',
                'DCU_CAN_DS_49A.bCdiagCode53','DCU_CAN_DS_49C.bCdiagCode53',
                'DCU_CAN_DS_49A.bCdiagCode55','DCU_CAN_DS_49C.bCdiagCode55',
                'DCU_CAN_DS_49A.bCdiagCode56','DCU_CAN_DS_49C.bCdiagCode56',
                'DCU_CAN_DS_49A.bCdiagCode57','DCU_CAN_DS_49C.bCdiagCode57',
                'DCU_CAN_DS_49A.bCdiagCode61','DCU_CAN_DS_49C.bCdiagCode61',
                'DCU_CAN_DS_49A.bCdiagCode62','DCU_CAN_DS_49C.bCdiagCode62',
                'DCU_CAN_DS_49A.bCdiagCode66','DCU_CAN_DS_49C.bCdiagCode66',
                'DCU_CAN_DS_49A.bCdiagCode67','DCU_CAN_DS_49C.bCdiagCode67',
                'DCU_CAN_DS_49A.bCdiagCode70','DCU_CAN_DS_49C.bCdiagCode70',
                'DCU_CAN_DS_49A.bCdiagCode71','DCU_CAN_DS_49C.bCdiagCode71',
                'DCU_CAN_DS_49A.bCdiagCode72','DCU_CAN_DS_49C.bCdiagCode72',
                'DCU_CAN_DS_49A.bCdiagCode73','DCU_CAN_DS_49C.bCdiagCode73',
                'DCU_CAN_DS_49A.bCdiagCode74','DCU_CAN_DS_49C.bCdiagCode74',
                'DCU_CAN_DS_49A.bCdiagCode75','DCU_CAN_DS_49C.bCdiagCode75',
                'DCU_CAN_DS_19B.bCdiagCode63','DCU_CAN_DS_19D.bCdiagCode63',
                'DCU_CAN_DS_19B.bCdiagCode81','DCU_CAN_DS_19D.bCdiagCode81',
                'DCU_CAN_DS_19B.bCdiagCode82','DCU_CAN_DS_19D.bCdiagCode82',
                'DCU_CAN_DS_19B.bCdiagCode83','DCU_CAN_DS_19D.bCdiagCode83',
                'DCU_CAN_DS_19B.bCdiagCode84','DCU_CAN_DS_19D.bCdiagCode84',
                'DCU_CAN_DS_19B.bCdiagCode85','DCU_CAN_DS_19D.bCdiagCode85',
                'DCU_CAN_DS_19B.bCdiagCode86','DCU_CAN_DS_19D.bCdiagCode86',
                'DCU_CAN_DS_19B.bCdiagCode87','DCU_CAN_DS_19D.bCdiagCode87',
                'DCU_CAN_DS_19B.bCdiagCode88','DCU_CAN_DS_19D.bCdiagCode88',
                'DCU_CAN_DS_19B.bCdiagCode89','DCU_CAN_DS_19D.bCdiagCode89',
                'DCU_CAN_DS_19B.bCdiagCode90','DCU_CAN_DS_19D.bCdiagCode90',
                'DCU_CAN_DS_19B.bCdiagCode92','DCU_CAN_DS_19D.bCdiagCode92',
                'DCU_CAN_DS_19B.bCdiagCode93','DCU_CAN_DS_19D.bCdiagCode93',
                'DCU_CAN_DS_19B.bCdiagCode94','DCU_CAN_DS_19D.bCdiagCode94',
                'DCU_CAN_DS_19B.bCdiagCode95','DCU_CAN_DS_19D.bCdiagCode95',
                'DCU_CAN_DS_19B.bCdiagCode96','DCU_CAN_DS_19D.bCdiagCode96',
                'DCU_CAN_DS_19B.bCdiagCode97','DCU_CAN_DS_19D.bCdiagCode97',
                'DCU_CAN_DS_19B.bCdiagCode98','DCU_CAN_DS_19D.bCdiagCode98',
                'DCU_CAN_DS_19B.bCdiagCode99','DCU_CAN_DS_19D.bCdiagCode99',
                'DCU_CAN_DS_19B.bCdiagCode106','DCU_CAN_DS_19D.bCdiagCode106',
                'DCU_CAN_DS_19B.bCdiagCode107','DCU_CAN_DS_19D.bCdiagCode107',
                'DCU_CAN_DS_19B.bCdiagCode108','DCU_CAN_DS_19D.bCdiagCode108',
                'DCU_CAN_DS_19B.bCdiagCode110','DCU_CAN_DS_19D.bCdiagCode110',
                'DCU_CAN_DS_19B.bCdiagCode111','DCU_CAN_DS_19D.bCdiagCode111',
                'DCU_CAN_DS_19B.bCdiagCode112','DCU_CAN_DS_19D.bCdiagCode112',
                'DCU_CAN_DS_19B.bCdiagCode113','DCU_CAN_DS_19D.bCdiagCode113',
                'DCU_CAN_DS_19B.bCdiagCode114','DCU_CAN_DS_19D.bCdiagCode114',
                'DCU_CAN_DS_19B.bCdiagCode115','DCU_CAN_DS_19D.bCdiagCode115',
                'DCU_CAN_DS_19B.bCdiagCode116','DCU_CAN_DS_19D.bCdiagCode116',
                'DCU_CAN_DS_19B.bCdiagCode117','DCU_CAN_DS_19D.bCdiagCode117',
                'DCU_CAN_DS_19B.bCdiagCode118','DCU_CAN_DS_19D.bCdiagCode118',
                'DCU_CAN_DS_19B.bCdiagCode119','DCU_CAN_DS_19D.bCdiagCode119'
                ]
        #DICCIONARIO PARA INTERPRETAR LA DIAGNOSIS DE PUERTAS
        self.DCU_DIAGNOSIS_DICT = {
        'bCdiagCode1':  {'Error Code': 'bCdiagCode1',  'Description': 'Broken wire in door drive M1 motor'},
        'bCdiagCode2':  {'Error Code': 'bCdiagCode2',  'Description': 'Fault in door closed and locked micro [S1]'},
        'bCdiagCode3':  {'Error Code': 'bCdiagCode3',  'Description': 'Fault in door closed and locked micro [S2]'},
        'bCdiagCode4':  {'Error Code': 'bCdiagCode4',  'Description': 'Door does not unlock within 3 s'},
        'bCdiagCode5':  {'Error Code': 'bCdiagCode5',  'Description': 'Door motor encoder failure [M1]'},
        'bCdiagCode6':  {'Error Code': 'bCdiagCode6',  'Description': 'Repeated obstacle detection in door closing'},
        'bCdiagCode7':  {'Error Code': 'bCdiagCode7',  'Description': 'Repeated obstacle detection at door opening'},
        'bCdiagCode8':  {'Error Code': 'bCdiagCode8',  'Description': 'DCU internal security channel failure [Board A]'},
        'bCdiagCode9':  {'Error Code': 'bCdiagCode9',  'Description': 'Door leaf detection switch fails'},
        'bCdiagCode10': {'Error Code': 'bCdiagCode10', 'Description': 'Internal safety channel on board “B” of the DCU fails'},
        # No hay bCdiagCode11 en la tabla original
        'bCdiagCode12': {'Error Code': 'bCdiagCode12', 'Description': 'Short circuit on 5 VDC power supply of the DCU'},
        'bCdiagCode13': {'Error Code': 'bCdiagCode13', 'Description': 'Spare'},
        'bCdiagCode14': {'Error Code': 'bCdiagCode14', 'Description': 'Malfunction at DCU output O002: crew switch: position I “central close”'},
        'bCdiagCode15': {'Error Code': 'bCdiagCode15', 'Description': 'Malfunction at DCU output O003: power supply: elements entrance area {H1, H2, S11, S12, S21, S22, S47, S61}'},
        'bCdiagCode16': {'Error Code': 'bCdiagCode16', 'Description': 'Malfunction at DCU output O004: Decoupling emergency egress device Y4'},
        'bCdiagCode17': {'Error Code': 'bCdiagCode17', 'Description': 'Malfunction at DCU output O005: Warning lamp portal inside H11'},
        'bCdiagCode18': {'Error Code': 'bCdiagCode18', 'Description': 'Malfunction at DCU output O006: Illumination emergency switch S62'},
        'bCdiagCode19': {'Error Code': 'bCdiagCode19', 'Description': 'Malfunction at DCU output O007: illumination push button open portal inside + outside: LEDs green {S21, S22}'},
        'bCdiagCode20': {'Error Code': 'bCdiagCode20', 'Description': 'Malfunction at DCU output O008: illumination push button open portal inside + outside: LEDs red {S21, S22}'},
        'bCdiagCode21': {'Error Code': 'bCdiagCode21', 'Description': 'Malfunction at DCU output O009: Warning buzzer portal inside + outside: BIT 1 {H1, H2}'},
        'bCdiagCode22': {'Error Code': 'bCdiagCode22', 'Description': 'Malfunction at DCU output O010: Warning buzzer portal inside + outside: BIT 2 {H1, H2}'},
        'bCdiagCode23': {'Error Code': 'bCdiagCode23', 'Description': 'Malfunction at DCU output O011: Warning buzzer portal inside + outside: BIT 3 {H1, H2}'},
        'bCdiagCode24': {'Error Code': 'bCdiagCode24', 'Description': 'Malfunction at DCU output O012: power supply: limit switches door {S1, S2, S3, S4, S5.1, S5.2, S8, S16.1, S16.2, S17.1, S17.2}'},
        'bCdiagCode25': {'Error Code': 'bCdiagCode25', 'Description': 'Malfunction at DCU output O103: Power supply: push buttons PRM + close, elements step {S14, S26, S27}'},
        'bCdiagCode26': {'Error Code': 'bCdiagCode26', 'Description': 'Malfunction at DCU output O104: Armature stop brake step Y3'},
        # No hay bCdiagCode27 en la tabla original
        'bCdiagCode28': {'Error Code': 'bCdiagCode28', 'Description': 'Malfunction at DCU output O106: power supply: crew switch S47'},
        'bCdiagCode29': {'Error Code': 'bCdiagCode29', 'Description': 'Malfunction at DCU output O107: illumination push button PRM portal inside + outside: LEDs green {-} {S52.1, S55, S56.1}'},
        'bCdiagCode30': {'Error Code': 'bCdiagCode30', 'Description': 'Malfunction at DCU output O108: illumination push button PRM portal inside + outside: LEDs red {-} {S14, S26, S27, S31, S32}'},
        'bCdiagCode31': {'Error Code': 'bCdiagCode31', 'Description': 'Push button open portal inside S22 fails'},
        'bCdiagCode32': {'Error Code': 'bCdiagCode32', 'Description': 'Push button open portal outside S21 fails'},
        'bCdiagCode33': {'Error Code': 'bCdiagCode33', 'Description': 'PRM push button inside S32 fails'},
        'bCdiagCode34': {'Error Code': 'bCdiagCode34', 'Description': 'PRM push button outside S31 fails'},
        'bCdiagCode35': {'Error Code': 'bCdiagCode35', 'Description': 'Service push button on DCU fails'},
        'bCdiagCode36': {'Error Code': 'bCdiagCode36', 'Description': 'Sensitive edge door - front side, outer edge S11 steady activated'},
        'bCdiagCode37': {'Error Code': 'bCdiagCode37', 'Description': 'Sensitive edge door - front side, inner edge S12 steady activated'},
        'bCdiagCode38': {'Error Code': 'bCdiagCode38', 'Description': 'Sensitive edge door - front side, outer edge S11 fails'},
        'bCdiagCode39': {'Error Code': 'bCdiagCode39', 'Description': 'Sensitive edge door - front side, inner edge S12 fails'},
        'bCdiagCode40': {'Error Code': 'bCdiagCode40', 'Description': 'Sensitive edge step front side S14 fails'},
        'bCdiagCode41': {'Error Code': 'bCdiagCode41', 'Description': 'Sensitive edge step front side S14 steady activated'},
        'bCdiagCode42': {'Error Code': 'bCdiagCode42', 'Description': 'Ethernet Bus communication fails'},
        'bCdiagCode43': {'Error Code': 'bCdiagCode43', 'Description': 'Can Bus communication fails'},
        'bCdiagCode44': {'Error Code': 'bCdiagCode44', 'Description': 'Door leaves the closed&locked position without permission'},
        'bCdiagCode45': {'Error Code': 'bCdiagCode45', 'Description': 'Signals of the limit switches are different'},
        'bCdiagCode46': {'Error Code': 'bCdiagCode46', 'Description': 'Relay function fails (TIL001/002 board A)'},
        'bCdiagCode47': {'Error Code': 'bCdiagCode47', 'Description': 'Relay function fails (TIL101/102 board B)'},
        'bCdiagCode48': {'Error Code': 'bCdiagCode48', 'Description': 'Door coding faulty'},
        'bCdiagCode49': {'Error Code': 'bCdiagCode49', 'Description': 'Door coding faulty'},
        'bCdiagCode50': {'Error Code': 'bCdiagCode50', 'Description': 'Push button close inside S27 fails'},
        'bCdiagCode51': {'Error Code': 'bCdiagCode51', 'Description': 'Push button close outside S27 fails'},
        'bCdiagCode52': {'Error Code': 'bCdiagCode52', 'Description': 'Decoupling (solenoid) device on the EED fails'},
        'bCdiagCode53': {'Error Code': 'bCdiagCode53', 'Description': 'Short circuit on 5 VDC power supply of the DCU'},
        # No hay bCdiagCode54 en la tabla original
        'bCdiagCode55': {'Error Code': 'bCdiagCode55', 'Description': 'Malfunction at DCU output O110: illumination push button close portal inside + outside: LEDs green {S26, S27}'},
        'bCdiagCode56': {'Error Code': 'bCdiagCode56', 'Description': 'Malfunction at DCU output O111: illumination push button close portal inside + outside: LEDs red {S26, S27}'},
        'bCdiagCode57': {'Error Code': 'bCdiagCode57', 'Description': 'Malfunction at DCU output O112: power supply: limit switches step {S52.1, S55, S56.1}'},
        # No hay bCdiagCode58, bCdiagCode59, bCdiagCode60 en la tabla original
        'bCdiagCode61': {'Error Code': 'bCdiagCode61', 'Description': 'Crew switch fails'},
        'bCdiagCode62': {'Error Code': 'bCdiagCode62', 'Description': 'Crew switch inside “ramp mode” S48 fails'},
        'bCdiagCode63': {'Error Code': 'bCdiagCode63', 'Description': 'Crew switch for ready for departure fails'},
        # bCdiagCode64-65 no presentes
        'bCdiagCode66': {'Error Code': 'bCdiagCode66', 'Description': 'Door out of service device fails'},
        'bCdiagCode67': {'Error Code': 'bCdiagCode67', 'Description': 'Step out of service device fails'},
        # bCdiagCode68-69 no presentes
        'bCdiagCode70': {'Error Code': 'bCdiagCode70', 'Description': 'Limit switch “door locked left 1” {S16.1} fails'},
        'bCdiagCode71': {'Error Code': 'bCdiagCode71', 'Description': 'Limit switch “door locked left 2” {S16.2} fails'},
        'bCdiagCode72': {'Error Code': 'bCdiagCode72', 'Description': 'Limit switch “door locked right 1” {S17.1} fails'},
        'bCdiagCode73': {'Error Code': 'bCdiagCode73', 'Description': 'Limit switch “door locked right 2” {S17.2} fails'},
        'bCdiagCode74': {'Error Code': 'bCdiagCode74', 'Description': 'Door locking unit left fails'},
        'bCdiagCode75': {'Error Code': 'bCdiagCode75', 'Description': 'Door locking unit right fails'},
        'bCdiagCode81': {'Error Code': 'bCdiagCode81',  'Description': 'Broken cable in M2 motor, bridge-plate actuation'},
        'bCdiagCode82': {'Error Code': 'bCdiagCode82',  'Description': 'Limit switch “step closed” {S52.1} fails'},
        'bCdiagCode83': {'Error Code': 'bCdiagCode83',  'Description': 'Step leaves the closed position without permission'},
        'bCdiagCode84': {'Error Code': 'bCdiagCode84',  'Description': 'Step does not unlock within 3 s'},
        'bCdiagCode85': {'Error Code': 'bCdiagCode85',  'Description': 'Fault in step position sensors'},
        'bCdiagCode86': {'Error Code': 'bCdiagCode86',  'Description': 'Step movement monitoring at closing sequence was activated on a fixed number of successive closing attempts'},
        'bCdiagCode87': {'Error Code': 'bCdiagCode87',  'Description': 'Step obstacle detection at opening sequence was activated on a fixed number of successive opening attempts'},
        'bCdiagCode88': {'Error Code': 'bCdiagCode88',  'Description': 'Armature stop brake step fails'},
        'bCdiagCode89': {'Error Code': 'bCdiagCode89',  'Description': 'Burn In test fails'},
        'bCdiagCode90': {'Error Code': 'bCdiagCode90',  'Description': 'Status of input signals is different'},
        'bCdiagCode92': {'Error Code': 'bCdiagCode92',  'Description': 'Status of input speed signals is equal'},
        'bCdiagCode93': {'Error Code': 'bCdiagCode93',  'Description': 'System does not detect fully opened position at defined time'},
        'bCdiagCode94': {'Error Code': 'bCdiagCode94',  'Description': 'System does not detect closed (&locked) position at defined time'},
        'bCdiagCode95': {'Error Code': 'bCdiagCode95',  'Description': 'System does not detect fully opened position at defined time'},
        'bCdiagCode96': {'Error Code': 'bCdiagCode96',  'Description': 'Major internal DCU failure'},
        'bCdiagCode97': {'Error Code': 'bCdiagCode97',  'Description': 'System does not detect closed (&locked) position at defined time'},
        'bCdiagCode98': {'Error Code': 'bCdiagCode98',  'Description': 'UIC14 data bus signal and hardwired signal are different'},
        'bCdiagCode99': {'Error Code': 'bCdiagCode99',  'Description': 'UIC15 data bus signal and hardwired signal are different'},
        'bCdiagCode106': {'Error Code': 'bCdiagCode106', 'Description': 'Door leaf speed of manual movement is too high'},
        'bCdiagCode107': {'Error Code': 'bCdiagCode107', 'Description': 'Step plate speed of manual movement is too high'},
        'bCdiagCode108': {'Error Code': 'bCdiagCode108', 'Description': 'Faulty emergency state evaluated'},
        'bCdiagCode110': {'Error Code': 'bCdiagCode110', 'Description': 'Malfunction on UIC-trainline 14(+)/12(-)'},
        'bCdiagCode111': {'Error Code': 'bCdiagCode111', 'Description': 'Malfunction on UIC-trainline 15(+)/12(-)'},
        'bCdiagCode112': {'Error Code': 'bCdiagCode112', 'Description': 'Relay function fails on UIC16 bypass contact'},
        'bCdiagCode113': {'Error Code': 'bCdiagCode113', 'Description': 'Homogeneity test error'},
        'bCdiagCode114': {'Error Code': 'bCdiagCode114', 'Description': 'Malfunction at DCU output O101: UIC16 bypass relay'},
        'bCdiagCode115': {'Error Code': 'bCdiagCode115', 'Description': 'Malfunction at DCU output O102: Release opposite entrance'},
        'bCdiagCode116': {'Error Code': 'bCdiagCode116', 'Description': 'Malfunction at DCU output O105: Power supply: UIC14&15&16'},
        'bCdiagCode117': {'Error Code': 'bCdiagCode117', 'Description': 'Malfunction on output UIC 09(+)/12(-) of Door Control Unit'},
        'bCdiagCode118': {'Error Code': 'bCdiagCode118', 'Description': 'Incongruency in UIC14 vs UIC12 inputs'},
        'bCdiagCode119': {'Error Code': 'bCdiagCode119', 'Description': 'Incongruency in UIC15 vs UIC12 inputs'},
    }
    
class CoachClient:
    """
    Cliente por coche/coach basado en isagrafInterface (Ethernet).
    - 1 instancia por coach (reutilizable)
    - read_vars para lecturas (con timestamp)
    """

    def __init__(self, coach_id: str, ip: str, health_vars: list[str] | None = None):
        self.coach_id = coach_id
        self.ip = ip

        # Instancia reutilizable (mantiene socket mientras funcione)
        self.iface = isagrafInterface(ip)


        # Último timestamp “bueno” (no Error!)
        self.last_ok_ts_ms: int = 0

    def _flatten_ts_map(self, ts_map: dict) -> tuple[int, dict]:
        if not ts_map:
            return 0, {}

        ts_ms = max(ts_map.keys())
        merged = {}
        for t in sorted(ts_map.keys()):
            merged.update(ts_map[t] or {})

        return ts_ms, merged

    def _all_read_error(self, values: dict) -> bool: #El guion bajo en el nombre del método es para indicar que es “privado” (convención, no restricción real), es decir, que se usa sólo dentro del método, no es público
        """
        True si TODAS las variables leídas son Error! (no accesible / sin conexión / timeout).
        """
        if not values:
            return True
        return all(v == isagrafInterface.READ_ERROR for v in values.values())

    def _all_write_fail(self, results: dict) -> bool:
        """
        True si TODAS las escrituras han fallado (False).
        """
        if not results:
            return True
        return all(v is False for v in results.values())

    def read_vars(self, vars_list: list[str], wait_time: float = 1.0) -> tuple[bool, int, dict]:
        """
        Lectura genérica (para TSC, diagnósticos, etc.)

        Devuelve:
          (online, ts_ms, values)

        - online False si todo es Error!
        - ts_ms = timestamp ms del batch (del driver)
        - values = dict {var: value}
        """
        if not vars_list:
            return True, 0, {}

        ts_map = self.iface.readValues(vars_list, wait_time=wait_time)
        ts_ms, values = self._flatten_ts_map(ts_map)

        online = not self._all_read_error(values)
        if online:
            self.last_ok_ts_ms = ts_ms

        return online, ts_ms, values

    def write_vars(self, var_map: dict, lock: bool = False, wait_time: float = 1.0) -> tuple[bool, int, dict]:
        """
        Escritura genérica (para TSC, diagnósticos, etc.)

        Devuelve:
        (online, ts_ms, results)

        - online False si todo falla (todo False)
        - ts_ms = timestamp ms del batch (del driver)
        - results = dict {var: True/False}
        """
        if not var_map:
            return True, 0, {}

        ts_map = self.iface.writeValues(var_map, lock=lock, wait_time=wait_time)
        ts_ms, results = self._flatten_ts_map(ts_map)

        online = not self._all_write_fail(results)
        if online:
            self.last_ok_ts_ms = ts_ms

        return online, ts_ms, results

    def ssh_cmd(self, commands: str | list[str], wait_time: int = 5):
        return self.iface.executeCommand(commands, wait_time=wait_time) 

class Worker(QObject):

    on_tsc_data = Signal(str, object, dict)    # endpoint_id, ts_ms, values
    on_tsc_diag_data = Signal(str, object, dict)    # endpoint_id, ts_ms, values
    on_door_data = Signal(str, object, dict)    # endpoint_id, ts_ms, values
    on_door_diag_data = Signal(str, object, dict)    # endpoint_id, ts_ms, values
    status = Signal(str, bool, str, object)    # endpoint_id, online, msg, ts_ms

    def __init__(self, is_cc: bool, project: str, endpoint_client: CoachClient, vars_to_read: dict, diag_enabled: dict, period_s: float = 0.5, wait_time: float = 1.0):
        super().__init__()
        self.is_cc = is_cc
        self.project = project
        self.client = endpoint_client
        self.endpoint_id = endpoint_client.coach_id

        self.period_s = float(period_s)
        self.wait_time = float(wait_time)

        self._running = True
        self._at_least_one_read = False
        self._last_ts = -1

        self._timer = None
        self._busy = False
        
        self._pending_config = None

        # Desempaquetamos las variables a leer (para TSC, diagnósticos, etc.) según la configuración
        self.coach_type_var = vars_to_read.get("COACH_TYPE")
        self.tsc_coach_vars_db = vars_to_read.get("TSC_DB")
        self.tsc_coach_vars_dsb = vars_to_read.get("TSC_DSB")
        self.tsc_cc_vars = vars_to_read.get("TSC_CC_DB")
        self.tsc_diag_vars = vars_to_read.get("TSC_DIAG_VARS")
        self.bcu_diag_vars = vars_to_read.get("BCU_DIAG_VARS")
        self.bcu_diag_vars_cc = vars_to_read.get("BCU_DIAG_VARS_CC")
        self.doors_vars = vars_to_read.get("DOORS")
        self.doors_diag_vars = vars_to_read.get("DOORS_DIAG_VARS")

        # Desempaquetamos las opciones de diagnóstico habilitados según la configuración. Esto se modificará en función de lo que se quiera mostrar en la UI (checkboxes).
        self.tsc_enabled = diag_enabled.get("TSC")
        self.doors_enabled = diag_enabled.get("DOORS")

        if self.project == "DSB":
            self.tsc_normal_vars = list(self.tsc_coach_vars_dsb)
            self.tsc_cc_vars = []
            
        elif self.project == "DB":
            self.tsc_normal_vars = list(self.tsc_coach_vars_db)
            self.tsc_cc_vars = list(self.tsc_cc_vars)

        # Añadimos la variable de tipo de coche al final de la lista.
        if isinstance(self.coach_type_var, list):
            self.coach_type_var = self.coach_type_var[0] if self.coach_type_var else None
        if self.coach_type_var:
            self.tsc_normal_vars = [v for v in self.tsc_normal_vars if v != self.coach_type_var] + [self.coach_type_var] 
            self.doors_vars = [v for v in self.doors_vars if v != self.coach_type_var] + [self.coach_type_var]

    def start(self):
        if self._timer is None:
            self._timer = QTimer(self)
            self._timer.setInterval(max(1, int(self.period_s * 1000)))
            self._timer.timeout.connect(self._tick)

        self._running = True
        self._timer.start()

    def stop(self):
        self._running = False
        if self._timer is not None:
            self._timer.stop()

    def _tick(self):
            if not self._running:
                if self._timer:
                    self._timer.stop()
                return

            # evita reentrancia si un tick tarda mucho
            if self._busy:
                return
            self._busy = True

            _t_0 = time.perf_counter()

            try:
                # aplicar config pendiente al inicio del tick
                if self._pending_config is not None:
                    cfg = self._pending_config
                    self._pending_config = None

                    self.tsc_enabled = cfg.get("TSC")
                    self.doors_enabled = cfg.get("DOORS")
                    
                    # print(f"Updated Worker config: TSC_enabled={self.tsc_enabled}, Doors_enabled={self.doors_enabled}")

                # ################################# METEMOS UN DIAGNÓSTICO MÍNIMO PARA MANTENER VIVA LA TABLA ###############################

                if self.tsc_enabled or self.doors_enabled:
                    self._at_least_one_read = True
                else:
                    self._at_least_one_read = False

                ts_ms = 0

                # ################################ LECTURA DE TSC O NINGUNO ACTIVO #######################################

                if self.tsc_enabled or not self._at_least_one_read:
                    # print(f"TSC activo: {self.tsc_enabled}, al menos una lectura: {self._at_least_one_read} -> leyendo TSC y diag aunque no estén activos para mantener alive la tabla")
                    if not self.is_cc:
                        # print("Reading normal TSC vars:", self.tsc_normal_vars)
                        online, ts_ms, tsc_values = self.client.read_vars(self.tsc_normal_vars, wait_time=self.wait_time)
                        online, ts_ms, tsc_diag_values = self.client.read_vars(self.tsc_diag_vars + self.bcu_diag_vars, wait_time=self.wait_time) 
                                                
                    else:
                        # print("Reading CC TSC vars:", self.tsc_cc_vars)                        
                        online, ts_ms, tsc_values = self.client.read_vars(self.tsc_cc_vars, wait_time=self.wait_time)
                        online, ts_ms, tsc_diag_values = self.client.read_vars(self.bcu_diag_vars_cc, wait_time=self.wait_time) 


                    if not online:
                        self.status.emit(self.endpoint_id, False, "offline (READ_ERROR)", ts_ms)
                    else:
                        self.status.emit(self.endpoint_id, True, "ok", ts_ms)

                        if ts_ms >= self._last_ts:
                            self._last_ts = ts_ms
                            reformat_tsc_values = {k: self._to_str_value(v) for k, v in (tsc_values or {}).items()}
                            self.on_tsc_data.emit(self.endpoint_id, ts_ms, reformat_tsc_values)
                            reformat_diag_values = {k: self._to_str_value(v) for k, v in (tsc_diag_values or {}).items()}
                            self.on_tsc_diag_data.emit(self.endpoint_id, ts_ms, reformat_diag_values)

                ############################################################################################################

                #################################### LECTURA DE PUERTAS ####################################################

                if self.doors_enabled:
                    
                    # print(f"Doors diag activo: {self.doors_enabled} -> leyendo puertas y diag")
                    online, ts_ms, door_values = self.client.read_vars(self.doors_vars, wait_time=self.wait_time)
                    online, ts_ms, door_diag_values = self.client.read_vars(self.doors_diag_vars, wait_time=self.wait_time)

                    if not online:
                        self.status.emit(self.endpoint_id, False, "offline (READ_ERROR)", ts_ms)
                        
                    else:
                        self.status.emit(self.endpoint_id, True, "ok", ts_ms)

                        if ts_ms >= self._last_ts:
                            self._last_ts = ts_ms
                            reformat_door_values = {k: self._to_str_value(v) for k, v in (door_values or {}).items()}
                            self.on_door_data.emit(self.endpoint_id, ts_ms, reformat_door_values)
                            reformat_door_diag_values = {k: self._to_str_value(v) for k, v in (door_diag_values or {}).items()}
                            self.on_door_diag_data.emit(self.endpoint_id, ts_ms, reformat_door_diag_values)

                ############################################################################################################

            except Exception as e:
                print(f"Error: {e}")
                self.status.emit(self.endpoint_id, False, f"excepción: {e}", 0)

            finally:
                _elapsed_ms = (time.perf_counter() - _t_0) * 1000
                # print(f"Worker {self.client.coach_id} is CC ({self.is_cc}) -> tick elapsed time: {_elapsed_ms:.2f} ms")
                self._busy = False
    
    def _to_str_value(self, v):
        
        try:
            if v == isagrafInterface.READ_ERROR:
                return isagrafInterface.READ_ERROR
        except Exception:
            pass

        if v is None:
            return isagrafInterface.READ_ERROR
    
        if isinstance(v, bool):
            return "1" if v else "0"
        
        if isinstance(v, (int,float)):
            try: 
                return str(int(v))
            except Exception:
                return isagrafInterface.READ_ERROR
            
        if isinstance(v, str):
            s = v.strip().lower()
            if s in ("true", "t", "yes", "y", "on"):
                return "1"
            if s in ("false", "f", "no", "n", "off"):
                return "0"
            
            try:
                return str(int(float(s)))
            except Exception:
                return isagrafInterface.READ_ERROR

        try:
            return str(int(v))
        except Exception:
            return isagrafInterface.READ_ERROR

    def _update_config(self, config):

        # Guardamos y aplicamos en el siguiente tick (evita mezclar un ciclo a mitad)
        self._pending_config = dict(config or {})

class Vars_Warehouse(QObject):
    snapshotUpdated = Signal(dict)

    def __init__(self, endpoint_ids, render_hz=1):
        super().__init__()
        self.tsc_state = {eid: {"online": False, "values": {}} for eid in endpoint_ids}
        self.tsc_diag_state = {eid: {"online": False, "values": {}} for eid in endpoint_ids}
        self.doors_state = {eid: {"online": False, "values": {}} for eid in endpoint_ids}
        self.door_diag_state = {eid: {"online": False, "values": {}} for eid in endpoint_ids}
        self._dirty = True

        hz = max(1.0, float(render_hz))
        interval_ms = max(20, int(1000 / hz))
        self._timer = QTimer(self)
        self._timer.setInterval(interval_ms)
        self._timer.timeout.connect(self._tick)

    def start(self):
        self._timer.start()

    def stop(self):
        self._timer.stop()

    def on_tsc_data(self, endpoint_id, ts_ms, values):
        st = self.tsc_state.get(endpoint_id)
        if st is None:
            return
        
        values = values or {}

        # Si ya estaba online y los valores son iguales -> no hay cambio real
        if st["online"] and st["values"] == values:
            return

        st["online"] = True
        st["values"] = values
        self._dirty = True

    def on_doors_data(self, endpoint_id, ts_ms, values):
        st = self.doors_state.get(endpoint_id)
        if st is None:
            return
        
        values = values or {}

        # Si ya estaba online y los valores son iguales -> no hay cambio real
        if st["online"] and st["values"] == values:
            return

        st["online"] = True
        st["values"] = values
        self._dirty = True

    def on_status(self, endpoint_id, online, msg, ts_ms):
        online = bool(online)
        for state_dict in [self.tsc_state, self.doors_state]:
            st = state_dict.get(endpoint_id)
            if st is None:
                continue
            if st["online"] != online:
                st["online"] = online
                if not online:
                    st["values"] = {}
                self._dirty = True

    def on_tsc_diag_data(self, endpoint_id, ts_ms, values):
        st = self.tsc_diag_state.get(endpoint_id)
        if st is None:
            return
        
        if st["online"] and st["values"] == values:
            return
        
        st["online"] = True
        st["values"] = values
        self._dirty = True

    def on_door_diag_data(self, endpoint_id, ts_ms, values):
        st = self.door_diag_state.get(endpoint_id)
        if st is None:
            return
        
        if st["online"] and st["values"] == values:
            return
        
        st["online"] = True
        st["values"] = values
        self._dirty = True

    def _tick(self):
        if not self._dirty:
            return

        snapshot = {
            "tsc": {
                eid: {"online": bool(st["online"]), "values": dict(st["values"])}
                for eid, st in self.tsc_state.items()
            },
            "tsc_diag": {
                eid: {"online": bool(st["online"]), "values": dict(st["values"])}
                for eid, st in self.tsc_diag_state.items()
            },
            "doors": {
                eid: {"online": bool(st["online"]), "values": dict(st["values"])}
                for eid, st in self.doors_state.items()
            },
            "doors_diag": {
                eid: {"online": bool(st["online"]), "values": dict(st["values"])}
                for eid, st in self.door_diag_state.items()
            }
                }
        self._dirty = False
        self.snapshotUpdated.emit(snapshot)

class ScanThread(QThread):
    
    scan_progress = Signal(int, int)
    scan_completed = Signal(list)

    def __init__(self, ip_list, max_initial_ips, project, cabcar_VCUCH_ips, cabcar_VCUPH_ips, config):
        super().__init__()
        self.ip_list = ip_list
        self.max_initial_ips = max_initial_ips
        self.project = project
        self.cabcar_VCUCH_ips = cabcar_VCUCH_ips
        self.cabcar_VCUPH_ips = cabcar_VCUPH_ips
        self.config = config

    def run(self):

        def ping(ip: str) -> bool:
            
            host = ip.split(":")[0].strip()
            if not host:
                return False
            try:
                if platform.system().lower().startswith("win"):
                    cmd = ["ping", "-n", "1", "-w", "100", host]
                else:
                    cmd = ["ping", "-c", "1", "-W", "1", host]
                r = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                # print(ip, r.returncode == 0)
                return r.returncode == 0
            except Exception:
                return False

        valid_ips = self.ip_list[:self.max_initial_ips]
        scan_list = self.ip_list[self.max_initial_ips:]
        scan_list_vcuch_cc = self.cabcar_VCUCH_ips[self.max_initial_ips:]
        total = max(1, len(scan_list))

        for i, ip in enumerate(scan_list):
            vcu_norm_ping = ping(ip)
            vcu_cc_ping = ping(scan_list_vcuch_cc[i])
            if vcu_cc_ping:
                valid_ips.append(scan_list_vcuch_cc[i])
            elif vcu_norm_ping:
                valid_ips.append(ip)

            progress = ((i + 1) * 100) // total
            coach_number = len(valid_ips)
            self.scan_progress.emit(progress, coach_number)

        if self.project == "DB":
            # valid_ips.append(self.cabcar_VCUCH_ips[len(valid_ips)-1])
            valid_ips.insert(len(valid_ips) - 1, self.cabcar_VCUCH_ips[len(valid_ips) - 1])
            valid_ips[-1] = self.cabcar_VCUPH_ips[len(valid_ips) - 2]

        self.scan_completed.emit(valid_ips)

class TSCGenerator(QSvgWidget):
    """
    NUEVA versión:
    - NO hace lecturas (ni SSH ni isagraf).
    - SOLO dibuja usando snapshot.
    - Mantiene los mismos dibujos reutilizando tus helpers actuales.
    """

    def __init__(self, project, endpoint_ids, tsc_vars, project_coach_types, tsc_cc_vars, scale_factor = 1.25):
        super().__init__()

        self.project = project
        self.endpoint_ids = list(endpoint_ids)

        # Listas de variables (mismo orden que usabas antes)
        self.tsc_vars = list(tsc_vars)
        self.tsc_cc_vars = list(tsc_cc_vars) if tsc_cc_vars else []

        # Map de tipos (ya lo tienes en TCMS_vars)
        self.project_coach_types = project_coach_types

        # La var de tipo de coche (la usas para mostrar y para decidir dibujo)
        # OJO: en tu nuevo flujo dijiste que COACH_TYPE está al final de tsc_vars
        self.coach_type_var = self.tsc_vars[-1] if self.tsc_vars else None
        # print(f"Coach type variable: {self.coach_type_var}")

        # snapshot actual (lo alimenta vars_warehouse -> build_svg_snapshot)
        self.snapshot = {"tsc": {}}

        self.scale_factor = float(scale_factor)
        self.scaled_tsc_width = int(800 * self.scale_factor)
        self.scaled_tsc_height = int(300 * self.scale_factor)
      
    def set_snapshot(self, snapshot: dict):
        self.snapshot = snapshot or {"tsc": {}}
        self.render_from_snapshot()

    def render_from_snapshot(self):
        svg = self.generate_svg_from_snapshot()
        self.load(bytearray(svg, encoding="utf-8"))
  
    def generate_svg_from_snapshot(self) -> str:

        coaches_dict = (self.snapshot or {}).get("tsc", {}) or {}

        # Orden estable: el orden de endpoint_ids, pero solo los que existan en snapshot
        coach_ids = [eid for eid in self.endpoint_ids if eid in coaches_dict]
        self.num_coaches = len(coach_ids)

        # Si no hay nada, dibuja un SVG vacío mínimo (alto antiguo)
        if self.num_coaches == 0:
            root = Element("svg", xmlns="http://www.w3.org/2000/svg", width="800", height="305")
            return tostring(root, encoding="unicode")

        # Tipos y online por coach (para offsets como el antiguo)
        coach_type_codes = []
        coach_online = []
        for eid in coach_ids:
            st = coaches_dict.get(eid, {}) or {}
            values = st.get("values", {}) or {}
            ct = values.get(self.coach_type_var, "")
            coach_type_codes.append(str(ct))
            coach_online.append(bool(st.get("online", False)))

        # print(coach_type_codes)

        base_width = self.num_coaches * 100

        # Offsets “antiguos”
        pmr_extra = 250 if self.project == "DSB" else 100 if self.project == "DB" else 0
        cab_extra = 645 if self.project == "DB" else 0

        self.pmr_pos = coach_type_codes.index("5") if "5" in coach_type_codes else None
        self.cab_pos = coach_type_codes.index("2") if (self.project == "DB" and "2" in coach_type_codes) else None

        pmr_online = bool(coach_online[self.pmr_pos]) if self.pmr_pos is not None else False
        cab_online = bool(coach_online[self.cab_pos]) if self.cab_pos is not None else False

        corrected_svg_width = base_width
        if self.pmr_pos is not None and pmr_online:
            corrected_svg_width += pmr_extra
        if self.cab_pos is not None and cab_online:
            corrected_svg_width += cab_extra

        svg_root = Element(
            "svg",
            xmlns="http://www.w3.org/2000/svg",
            width=str(corrected_svg_width),
            height="305",
            viewBox = f"0 0 {corrected_svg_width} 305"
        )

        self.setFixedSize(int(corrected_svg_width * self.scale_factor), int(300 * self.scale_factor))
        self.scaled_tsc_width = int(corrected_svg_width * self.scale_factor)
        self.scaled_tsc_height = int(300 * self.scale_factor)
        # print(f"Adjusted SVG width: {corrected_svg_width}, scaled size: {self.scaled_tsc_width}x{self.scaled_tsc_height}")

        # Genera cada coche (grupo <g>) y lo traslada en X
        for idx, eid in enumerate(coach_ids):
            st = coaches_dict.get(eid, {}) or {}
            values = st.get("values", {}) or {}
            coach_type = str(values.get(self.coach_type_var, ""))
            online = bool(st.get("online", False))

            coach_g, _flag = self.process_coach_from_values(
                coach_id=eid,
                index=idx,
                coach_type=coach_type,
                values=values,
                online=online,
            )

            x_pos = idx * 100

            # “Hueco PMR” como el comportamiento antiguo: solo si PMR online y estás a la derecha
            if self.pmr_pos is not None and pmr_online and idx > self.pmr_pos:
                x_pos += pmr_extra

            coach_g.set("transform", f"translate({x_pos}, 0)")
            svg_root.append(coach_g)

        return tostring(svg_root, encoding="unicode")

    def process_coach_from_values(self, coach_id, index, coach_type, values, online=True):

        READ_ERR = isagrafInterface.READ_ERROR

        if not online:
            return self.offline_coach(coach_id, index), False

        def build_list(vars_list):
            return [values.get(v, READ_ERR) for v in (vars_list or [])]

        def g(lst, i, default=READ_ERR):
            return lst[i] if (i is not None and i < len(lst)) else default

        tsc_data = build_list(self.tsc_vars)
        tsc_data_cc = build_list(self.tsc_cc_vars) if self.tsc_cc_vars else []

        label = ""
        if isinstance(coach_type, str) and coach_type.isdigit():
            label = self.project_coach_types.get(int(coach_type), str(coach_type))

        if self.project == "DB":
            k800   = g(tsc_data, 0)
            k801   = g(tsc_data, 1)
            k802   = g(tsc_data, 2)
            k810   = g(tsc_data, 3)
            k811   = g(tsc_data, 4)
            k812   = g(tsc_data, 5)
            k804   = g(tsc_data, 6)
            k814   = g(tsc_data, 7)

            s60    = g(tsc_data, 8)
            s60_r  = g(tsc_data, 9)
            s62    = g(tsc_data, 10)
            s62_r  = g(tsc_data, 11)
            s256   = g(tsc_data, 12)
            s256_r = g(tsc_data, 13)
            s255   = g(tsc_data, 14)
            s255_r = g(tsc_data, 15)

            fr_riom_sc1  = g(tsc_data, 16)
            fr_riom_sc1r = g(tsc_data, 17)
            fr_riom_sc2  = g(tsc_data, 18)
            fr_riom_sc2r = g(tsc_data, 19)

            s60_b1    = g(tsc_data, 20)
            s60_r_b1  = g(tsc_data, 21)
            s62_b1    = g(tsc_data, 22)
            s62_r_b1  = g(tsc_data, 23)
            s256_b1   = g(tsc_data, 24)
            s256_r_b1 = g(tsc_data, 25)

            if coach_type == '11':
                coach = self.end_coach(label, index, k801, k800, k802, k804,
                                    s60, s60_r, s62, s62_r, s256, s256_r,
                                    s255, s255_r, fr_riom_sc1, fr_riom_sc1r)

            elif coach_type in ['3','4','6','7','8','9','10']:
                coach = self.normal_coach(label, index, k801, k800, k802, k804,
                                        s60, s60_r, s62, s62_r, s256, s256_r,
                                        self.pmr_pos, fr_riom_sc1, fr_riom_sc1r)

            elif coach_type == '5':
                coach = self.pmr_db_dsb2(label, index, k801, k800, k802, k810, k811, k812,
                                        k804, k814, s60, s60_r, s62, s62_r, s256, s256_r,
                                        fr_riom_sc1, fr_riom_sc1r, fr_riom_sc2, fr_riom_sc2r,
                                        s60_b1, s60_r_b1, s62_b1, s62_r_b1, s256_b1, s256_r_b1)

            elif coach_type == '2':
                s8    = g(tsc_data_cc, 0)
                s8_r  = g(tsc_data_cc, 1)
                s6    = g(tsc_data_cc, 2)
                s6_r  = g(tsc_data_cc, 3)
                s10   = g(tsc_data_cc, 4)

                k1    = g(tsc_data_cc, 5)
                k80   = g(tsc_data_cc, 6)
                k81   = g(tsc_data_cc, 7)
                k82   = g(tsc_data_cc, 8)
                k83   = g(tsc_data_cc, 9)

                sifa1_cond = g(tsc_data_cc, 10)
                sifa2_cond = g(tsc_data_cc, 11)

                s700  = g(tsc_data_cc, 12)
                s701  = g(tsc_data_cc, 13)
                s702  = g(tsc_data_cc, 14)
                s703  = g(tsc_data_cc, 15)
                s704  = g(tsc_data_cc, 16)

                k700  = g(tsc_data_cc, 17)
                k701  = g(tsc_data_cc, 18)
                k710  = g(tsc_data_cc, 19)
                k711  = g(tsc_data_cc, 20)
                k708  = g(tsc_data_cc, 21)
                k709  = g(tsc_data_cc, 21)
                k731  = g(tsc_data_cc, 22)
                k732  = g(tsc_data_cc, 23)
                k740  = g(tsc_data_cc, 24)
                k741  = g(tsc_data_cc, 25)

                s25   = g(tsc_data_cc, 26)
                s25_r = g(tsc_data_cc, 27)
                k753  = g(tsc_data_cc, 28)

                coach = self.cabcar(label, index, k801, k800, k802, k804,
                                    s60, s60_r, s62, s62_r, s255, s255_r, s256, s256_r,
                                    s8, s8_r, s6, s6_r, s10, k1, k80, k81, k82, k83,
                                    sifa1_cond, sifa2_cond,
                                    s700, s701, s702, s703, s704,
                                    k700, k701, k710, k711, k708, k709, k731, k732, k740, k741,
                                    s25, s25_r, k753, fr_riom_sc1, fr_riom_sc1r) 
            
            else:
                return self.offline_coach(coach_id, index), False

            return coach, True

    def save_as_png(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Guardar como PNG", "", "Archivos PNG (*.png)"
        )
        if not filename:
            return
        if not filename.lower().endswith(".png"):
            filename += ".png"

        renderer = self.renderer()

        # 1) Usa viewBox si está disponible (más fiable para no cortar)
        vb = renderer.viewBoxF()
        if vb.isValid() and vb.width() > 0 and vb.height() > 0:
            logical_w = vb.width()
            logical_h = vb.height()
        else:
            size = renderer.defaultSize()
            if not size.isValid() or size.width() <= 0 or size.height() <= 0:
                size = self.size()
            logical_w = float(size.width())
            logical_h = float(size.height())

        # 2) Opción A: ancho objetivo en píxeles
        target_width_px = 4000
        scale = target_width_px / max(1.0, logical_w)
        img_w = max(1, int(round(logical_w * scale)))
        img_h = max(1, int(round(logical_h * scale)))

        image = QImage(img_w, img_h, QImage.Format_ARGB32_Premultiplied)
        image.fill(Qt.transparent)

        painter = QPainter(image)
        try:
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setRenderHint(QPainter.TextAntialiasing, True)
            painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

            # 3) Renderiza al rect destino: evita recortes por tamaños lógicos raros
            renderer.render(painter, QRectF(0, 0, img_w, img_h))
        finally:
            painter.end()

        if image.save(filename, "PNG"):
            QMessageBox.information(self, "Éxito", f"Imagen guardada correctamente en:\n{filename}")
        else:
            QMessageBox.critical(self, "Error", f"No se pudo guardar el PNG:\n{filename}")
            
    def create_contact_svg(self, closed, x_offset=0, label=""):
        """
        Representa el estado de un contacto con una etiqueta.
        - opened=True para contacto abierto, False para cerrado.
        - x_offset para desplazar horizontalmente el contacto.
        - label es el texto que se mostrará debajo del contacto.
        """
        contact = Element("g", transform=f"translate({x_offset}, 0)")
        SubElement(contact, "circle", cx="0", cy="0", r="2", fill="black")
        SubElement(contact, "circle", cx="20", cy="0", r="2", fill="black")

        if closed:
            SubElement(contact, "line", x1="0", y1="0", x2="20", y2="0", stroke="green", stroke_width="1")
        else:
            SubElement(contact, "line", x1="0", y1="0", x2="18", y2="-7", stroke="red", stroke_width="1")
        
        # Etiqueta debajo del contacto
        SubElement(contact, "text", x="0", y="12", text_anchor="middle", font_style="italic", font_size="8").text = label

        return contact
    
    def create_led(self, energized, x_offset=0, tail_length=0, label=""):
        
        led=Element("g", transform=f"translate({x_offset}, 0)")
        
        upper_tail=-10-tail_length
        lower_tail=10+tail_length
        
        SubElement(led, "text", x="-28", y="2.5", text_anchor="middle", font_style="italic", font_size="6").text = label
        
        SubElement(led, "line", x1="0", y1=f"{upper_tail}", x2="0", y2="-7.5", stroke="black", stroke_width="1")
        SubElement(led, "line", x1="-7.5", y1="5.25", x2="7.5", y2="5.25", stroke="black", stroke_width="1")
        SubElement(led, "line", x1="0", y1="7.5", x2="0", y2=f"{lower_tail}", stroke="black", stroke_width="1")
        
        if int(energized)==1:
            SubElement(led, "polygon", points="-7.5,-7.5 7.5,-7.5 0,7.5", stroke="black", stroke_width="1",fill="red")
            SubElement(led, "line", x1="10", y1="0", x2="17.5", y2="-6", stroke="red", stroke_width="1")
            SubElement(led, "line", x1="10", y1="6", x2="17.5", y2="0", stroke="red", stroke_width="1")
            
            SubElement(led, "line", x1="17.5", y1="-6", x2="12.5", y2="-5.5", stroke="red", stroke_width="1")
            SubElement(led, "line", x1="17.5", y1="-6", x2="15.5", y2="-1", stroke="red", stroke_width="1")
            
            SubElement(led, "line", x1="17.5", y1="0", x2="12.5", y2="0.5", stroke="red", stroke_width="1")
            SubElement(led, "line", x1="17.5", y1="0", x2="15.5", y2="5", stroke="red", stroke_width="1")
            
        elif int(energized)==0:
            SubElement(led, "polygon", points="-7.5,-7.5 7.5,-7.5 0,7.5", stroke="black", stroke_width="1",fill="white")
            
            # SubElement(led, "line", x1="10", y1="0", x2="17.5", y2="-6", stroke="white", stroke_width="1")
            # SubElement(led, "line", x1="10", y1="6", x2="17.5", y2="0", stroke="white", stroke_width="1")
            
            # SubElement(led, "line", x1="17.5", y1="-6", x2="12.5", y2="-5.5", stroke="white", stroke_width="1")
            # SubElement(led, "line", x1="17.5", y1="-6", x2="15.5", y2="-1", stroke="white", stroke_width="1")
            
            # SubElement(led, "line", x1="17.5", y1="0", x2="12.5", y2="0.5", stroke="white", stroke_width="1")
            # SubElement(led, "line", x1="17.5", y1="0", x2="15.5", y2="5", stroke="white", stroke_width="1") #**{"stroke-width":"8"}

        else:
            SubElement(led, "polygon", points="-7.5,-7.5 7.5,-7.5 0,7.5", stroke="black", stroke_width="1",fill="yellow")

            SubElement(led, "line", x1="10", y1="0", x2="17.5", y2="-6", stroke="yellow", stroke_width="1")
            SubElement(led, "line", x1="10", y1="6", x2="17.5", y2="0", stroke="yellow", stroke_width="1")
            
            SubElement(led, "line", x1="17.5", y1="-6", x2="12.5", y2="-5.5", stroke="yellow", stroke_width="1")
            SubElement(led, "line", x1="17.5", y1="-6", x2="15.5", y2="-1", stroke="yellow", stroke_width="1")
            
            SubElement(led, "line", x1="17.5", y1="0", x2="12.5", y2="0.5", stroke="yellow", stroke_width="1")
            SubElement(led, "line", x1="17.5", y1="0", x2="15.5", y2="5", stroke="yellow", stroke_width="1") #**{"stroke-width":"8"}           

        return led
            
    def create_sifa(self, energized, forzed, x_offset=0, label=""):
        
        
        sifa=Element("g", transform=f"translate({x_offset}, 0)")
        
        SubElement(sifa, "line", x1="10", y1="5", x2="10", y2="20", stroke="black", stroke_width="1")
        SubElement(sifa, "line", x1="10", y1="0", x2="10", y2="-10", stroke="black", stroke_width="1")
        SubElement(sifa, "circle", cx="10", cy="-10", r="2", fill="black")
        SubElement(sifa, "circle", cx="10", cy="20", r="2", fill="black")
        
        
        SubElement(sifa, "line", x1="20", y1="5", x2="27.5", y2="5", stroke="black", stroke_width="1")
        SubElement(sifa, "line", x1="27.5", y1="5", x2="22.5", y2="-2.5", stroke="black", stroke_width="1")
        SubElement(sifa, "line", x1="22.5", y1="-2.5", x2="32.5", y2="-2.5", stroke="black", stroke_width="1")
        SubElement(sifa, "line", x1="32.5", y1="-2.5", x2="27.5", y2="5", stroke="black", stroke_width="1")
        SubElement(sifa, "line", x1="27.5", y1="5", x2="32.5", y2="12.5", stroke="black", stroke_width="1")
        SubElement(sifa, "line", x1="22.5", y1="12.5", x2="32.5", y2="12.5", stroke="black", stroke_width="1")
        SubElement(sifa, "line", x1="22.5", y1="12.5", x2="27.5", y2="5", stroke="black", stroke_width="1")
        
        SubElement(sifa, "text", x="0", y="-16", text_anchor="middle", font_style="italic", font_size="6").text = label
        
        
        
        if not int(forzed):
            SubElement(sifa, "rect", cx="0", cy="0", height="10", width="20",fill="yellow",stroke="black",stroke_width="1")
        elif not int(energized):
            SubElement(sifa, "rect", cx="0", cy="0", height="10", width="20",fill="green",stroke="black",stroke_width="1")
        else:
            SubElement(sifa, "rect", cx="0", cy="0", height="10", width="20",fill="red",stroke="black",stroke_width="1")
            
        return sifa
    
    def create_electovalve(self, energized, x_offset=0, label=""):
         
        valve=Element("g", transform=f"translate({x_offset}, 0)")
        
        SubElement(valve, "line", x1="10", y1="5", x2="10", y2="20", stroke="black", stroke_width="1")
        SubElement(valve, "line", x1="10", y1="0", x2="10", y2="-10", stroke="black", stroke_width="1")
        SubElement(valve, "circle", cx="10", cy="-10", r="2", fill="black")
        SubElement(valve, "circle", cx="10", cy="20", r="2", fill="black")
        
        
        # SubElement(valve, "line", x1="20", y1="5", x2="27.5", y2="5", stroke="black", stroke_width="1")
        # SubElement(valve, "line", x1="27.5", y1="5", x2="22.5", y2="-2.5", stroke="black", stroke_width="1")
        # SubElement(valve, "line", x1="22.5", y1="-2.5", x2="32.5", y2="-2.5", stroke="black", stroke_width="1")
        # SubElement(valve, "line", x1="32.5", y1="-2.5", x2="27.5", y2="5", stroke="black", stroke_width="1")
        # SubElement(valve, "line", x1="27.5", y1="5", x2="32.5", y2="12.5", stroke="black", stroke_width="1")
        # SubElement(valve, "line", x1="22.5", y1="12.5", x2="32.5", y2="12.5", stroke="black", stroke_width="1")
        # SubElement(valve, "line", x1="22.5", y1="12.5", x2="27.5", y2="5", stroke="black", stroke_width="1")
        
        SubElement(valve, "text", x="0", y="-16", text_anchor="middle", font_style="italic", font_size="6").text = label
        
        
        if int(energized):
            SubElement(valve, "rect", cx="0", cy="0", height="10", width="20",fill="green",stroke="black",stroke_width="1")
        else:
            SubElement(valve, "rect", cx="0", cy="0", height="10", width="20",fill="red",stroke="black",stroke_width="1")
            
        return valve
    
    def normal_coach(self, coach_name, coach_pos, k801_state, k800_state, k802_state, k804_state, s60, s60_r, s62, s62_r, s256, s256_r, pmr_index, fr_riom_sc1, fr_riom_sc1r):
        """
        Crea el SVG para un coche del tren con contactos k801, k800, k802 y una línea de separación.
        """
        coach = Element("g")

        # print(f"Coach Name: {coach_name}, Position: {coach_pos}, "
        # f"K801 State: {k801_state}, K800 State: {k800_state}, "
        # f"K802 State: {k802_state}, K804 State: {k804_state}, "
        # f"S60: {s60}, S60_R: {s60_r}, "
        # f"S62: {s62}, S62_R: {s62_r}, "
        # f"S256: {s256}, S256_R: {s256_r}")
        
        SubElement(coach, "line", x1="100", y1="0", x2="100", y2="315", stroke="black", **{"stroke-width": "1", "stroke-dasharray": "5, 5"},opacity="0.35")
        SubElement(coach, "text", x="50", y="292",**{"text-anchor": "middle","font-style": "italic","font-size": "10"}).text = f"Coche {coach_pos+1}: {coach_name}"


        if int(k800_state)==1:
            
            k800_state=0
        else:
            k800_state=1
        
        if int(k801_state)==1:
            k801_state=0
        else:
            k801_state=1
        
        if int(k802_state)==1:
            k802_state=0
        else:
            k802_state=1

            
        # Línea de entrada al coche (ajustada para ser de igual longitud)
        SubElement(coach, "line", x1="0", y1="30", x2="10", y2="30", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="10", y1="30", x2="10", y2="10", stroke="black", stroke_width="1")  # Bifurcación arriba
        SubElement(coach, "line", x1="10", y1="30", x2="10", y2="50", stroke="black", stroke_width="1")  # Bifurcación abajo
        SubElement(coach, "line", x1="10", y1="10", x2="40", y2="10", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="10", y1="50", x2="20", y2="50", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="60", y1="10", x2="90", y2="10", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="90", y1="10", x2="90", y2="30", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="40", y1="50", x2="60", y2="50", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="80", y1="50", x2="90", y2="50", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="90", y1="50", x2="90", y2="30", stroke="black", stroke_width="1")
        
        SubElement(coach, "line", x1="0", y1="90", x2="100", y2="90", stroke="black", stroke_width="1")
        
            
        # Camino superior (relé K801)
        upper_path = SubElement(coach, "g", transform="translate(40, 10)")
        upper_path.append(self.create_contact_svg(k801_state, x_offset=0, label="K801"))

        # Camino inferior (serie de K800 y K802)
        lower_path = SubElement(coach, "g", transform="translate(20, 50)")
        lower_path.append(self.create_contact_svg(k800_state, x_offset=0, label="K800"))
        lower_path.append(self.create_contact_svg(k802_state, x_offset=40, label="K802"))  # Desplazado 40 unidades a la derecha

        #Determina si el comportamiento de las RIOMS es correcto
        if int(fr_riom_sc1)>240:
            SubElement(coach, "text", x="50", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "red"}).text = "RIOM SC APAGADA"
        elif int(fr_riom_sc1r)>240:
            SubElement(coach, "text", x="50", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "red"}).text = "RIOM SCr APAGADA"
        elif k800_state and k802_state and not k801_state:
            SubElement(coach, "text", x="50", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "green"}).text = "CERRADO POR REDUNDANTE"
        elif k801_state and not k800_state:
            SubElement(coach, "text", x="50", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "green"}).text = "CERRADO POR PRINCIPAL"
        elif k800_state and not k801_state and not k802_state:
            SubElement(coach, "text", x="50", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "red"}).text = "ABIERTO"
        else:
            SubElement(coach, "text", x="50", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "red"}).text = "ERROR DE CABLEADO"

        # Conexión horizontal después de bifurcación y contacto (ajustada)
        SubElement(coach, "line", x1="90", y1="30", x2="100", y2="30", stroke="black", stroke_width="1")  # Salida

            
        # Determinar el color de fondo del coche
        if k801_state or (k800_state and k802_state):
            background_color = "green"
        else:
            background_color = "red"
            
        SubElement(coach, "rect", x="0", y="0", width="100", height="95", fill=background_color, opacity="0.15") 
            
        SubElement(coach, "circle", cx="100",cy="30",r="2",fill="black")
        SubElement(coach, "circle", cx="100",cy="90",r="2",fill="black")
        
        if pmr_index is not None and coach_pos<pmr_index:
            SubElement(coach, "text", x="60", y="37.5", transform="rotate(270 90 30)", **{"text-anchor": "right","font-style": "italic","font-size": "7"}).text = "XM06:24"
            SubElement(coach, "text", x="60", y="-52.5", transform="rotate(270 90 30)", **{"text-anchor": "right","font-style": "italic","font-size": "7"}).text = "XH06:24"
            SubElement(coach, "text", x="67.5", y="85",**{"text-anchor": "right","font-style": "italic","font-size": "7"}).text = "XM06:25"
            SubElement(coach, "text", x="5", y="85",**{"text-anchor": "left","font-style": "italic","font-size": "7"}).text = "XH06:25"
            
            SubElement(coach, "text", x="5", y="235", **{"text-anchor": "left","font-style": "italic","font-size": "7"}).text = "XH06:17"
            SubElement(coach, "text", x="5", y="270", **{"text-anchor": "left","font-style": "italic","font-size": "7"}).text = "XH06:18"    
            SubElement(coach, "text", x="67.5", y="235", **{"text-anchor": "right","font-style": "italic","font-size": "7"}).text = "XM06:17"
            SubElement(coach, "text", x="67.5", y="270", **{"text-anchor": "right","font-style": "italic","font-size": "7"}).text = "XM06:18"
            
            SubElement(coach, "text", x="5", y="125", **{"text-anchor": "left","font-style": "italic","font-size": "7"}).text = "XH06:7"
            SubElement(coach, "text", x="5", y="160", **{"text-anchor": "left","font-style": "italic","font-size": "7"}).text = "XH06:8"    
            SubElement(coach, "text", x="70", y="125", **{"text-anchor": "right","font-style": "italic","font-size": "7"}).text = "XM06:7"
            SubElement(coach, "text", x="70", y="160", **{"text-anchor": "right","font-style": "italic","font-size": "7"}).text = "XM06:8"
            
        elif pmr_index is not None and coach_pos>pmr_index:
            SubElement(coach, "text", x="60", y="37.5", transform="rotate(270 90 30)", **{"text-anchor": "right","font-style": "italic","font-size": "7"}).text = "XH06:24"
            SubElement(coach, "text", x="60", y="-52.5", transform="rotate(270 90 30)", **{"text-anchor": "right","font-style": "italic","font-size": "7"}).text = "XM06:24"
            SubElement(coach, "text", x="67.5", y="85",**{"text-anchor": "right","font-style": "italic","font-size": "7"}).text = "XH06:25"
            SubElement(coach, "text", x="5", y="85",**{"text-anchor": "left","font-style": "italic","font-size": "7"}).text = "XM06:25"
            
            SubElement(coach, "text", x="67.5", y="235", **{"text-anchor": "right","font-style": "italic","font-size": "7"}).text = "XH06:17"
            SubElement(coach, "text", x="67.5", y="270", **{"text-anchor": "right","font-style": "italic","font-size": "7"}).text = "XH06:18"    
            SubElement(coach, "text", x="5", y="235", **{"text-anchor": "left","font-style": "italic","font-size": "7"}).text = "XM06:17"
            SubElement(coach, "text", x="5", y="270", **{"text-anchor": "left","font-style": "italic","font-size": "7"}).text = "XM06:18"
            
            SubElement(coach, "text", x="70", y="125", **{"text-anchor": "right","font-style": "italic","font-size": "7"}).text = "XH06:7"
            SubElement(coach, "text", x="70", y="160", **{"text-anchor": "right","font-style": "italic","font-size": "7"}).text = "XH06:8"    
            SubElement(coach, "text", x="5", y="125", **{"text-anchor": "left","font-style": "italic","font-size": "7"}).text = "XM06:7"
            SubElement(coach, "text", x="5", y="160", **{"text-anchor": "left","font-style": "italic","font-size": "7"}).text = "XM06:8"
        
        SubElement(coach, "line", x1="0", y1="115", x2="40", y2="115", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="60", y1="115", x2="100", y2="115", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="0", y1="165", x2="100", y2="165", stroke="black", stroke_width="1") 
        
        if int(k804_state)==1:
            k804_state=0
        else:
            k804_state=1
        
        bypass = SubElement(coach, "g", transform="translate(40, 115)")
        bypass.append(self.create_contact_svg(k804_state, x_offset=0, label="K804"))
        
        if k804_state:
            background_color = "green"
        else:
            background_color = "red"
            
        SubElement(coach, "rect", x="0", y="95", width="100", height="100", fill=background_color, opacity="0.15")
        SubElement(coach, "line", x1="0", y1="95", x2="100", y2="95", stroke="black", **{"stroke-width": "4"}, opacity="0.35")

        SubElement(coach, "line", x1="0", y1="225", x2="100", y2="225", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="0", y1="275", x2="100", y2="275", stroke="black", stroke_width="1")

        
        SubElement(coach, "circle", cx="100",cy="225",r="2",fill="black")
        SubElement(coach, "circle", cx="100",cy="275",r="2",fill="black")
        
        SubElement(coach, "circle", cx="100",cy="115",r="2",fill="black")
        SubElement(coach, "circle", cx="100",cy="165",r="2",fill="black")

        SubElement(coach, "text", x="5", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9"}).text = "S60:"
        SubElement(coach, "text", x="5", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9"}).text = "S62:"
        # SubElement(coach, "text", x="50", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9"}).text = "S255:"
        SubElement(coach, "text", x="50", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9"}).text = "S256:"

        if s60 != s60_r:
            SubElement(coach, "text", x="22", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "yellow"}).text = "Error"
        elif s60 == "0":
            SubElement(coach, "text", x="22", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9",  "fill": "green"}).text = "Off"
        else:
            SubElement(coach, "text", x="22", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "red"}).text = "Activo"

        if s62 != s62_r:
            SubElement(coach, "text", x="22", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "yellow"}).text = "Error"
        elif s62 == "0":
            SubElement(coach, "text", x="22", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "green"}).text = "Off"
        else:
            SubElement(coach, "text", x="22", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "red"}).text = "Activo"

        # if s255 != s255_r:
        #     SubElement(coach, "text", x="72", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "yellow"}).text = "Error"
        # elif s255 == "0":
        #     SubElement(coach, "text", x="72", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "green"}).text = "Off"
        # else:
            # SubElement(coach, "text", x="72", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "red"}).text = "Activo"

        if s256 != s256_r:
            SubElement(coach, "text", x="72", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "yellow"}).text = "Error"
        elif s256 == "0":
            SubElement(coach, "text", x="72", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "green"}).text = "Off"
        else:
            SubElement(coach, "text", x="72", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "red"}).text = "Activo"
        
        return coach
   
    def end_coach(self, coach_name, coach_pos, k801_state, k800_state, k802_state, k804_state, s60, s60_r, s62, s62_r, s256, s256_r, s255, s255_r, fr_riom_sc1, fr_riom_sc1r):
        
        coach = Element("g")

        if coach_pos == 0:
            position = "left"
        else:
            position = "right"
        
        SubElement(coach, "text", x="50", y="292",**{"text-anchor": "middle","font-style": "italic","font-size": "10"}).text = f"Coche {coach_pos+1}: {coach_name}"
        
        if position == "left":
            
            SubElement(coach, "line", x1="100", y1="0", x2="100", y2="315", stroke="black", **{"stroke-width": "1", "stroke-dasharray": "5, 5"}, opacity="0.35")
            

        if int(k800_state)==1:
            
            k800_state=0
        else:
            k800_state=1
        
        if int(k801_state)==1:
            k801_state=0
        else:
            k801_state=1
        
        if int(k802_state)==1:
            k802_state=0
        else:
            k802_state=1
        
        #Determina si el comportamiento de las RIOMS es correcto
        if int(fr_riom_sc1)>240:
            SubElement(coach, "text", x="50", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "red"}).text = "RIOM SC APAGADA"
        elif int(fr_riom_sc1r)>240:
            SubElement(coach, "text", x="50", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "red"}).text = "RIOM SCr APAGADA"
        elif k800_state and k802_state and not k801_state:
            SubElement(coach, "text", x="50", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "green"}).text = "CERRADO POR REDUNDANTE"
        elif k801_state and not k800_state and k802_state:
            SubElement(coach, "text", x="50", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "green"}).text = "CERRADO POR PRINCIPAL"
        elif k800_state and not k801_state and not k802_state:
            SubElement(coach, "text", x="50", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "red"}).text = "ABIERTO"
        else:
            SubElement(coach, "text", x="50", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "red"}).text = "ERROR DE CABLEADO"

        # Línea de entrada al coche (ajustada para ser de igual longitud)
        SubElement(coach, "line", x1="10", y1="30", x2="10", y2="10", stroke="black", stroke_width="1")  # Bifurcación arriba
        SubElement(coach, "line", x1="10", y1="30", x2="10", y2="50", stroke="black", stroke_width="1")  # Bifurcación abajo
        SubElement(coach, "line", x1="10", y1="10", x2="40", y2="10", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="10", y1="50", x2="20", y2="50", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="60", y1="10", x2="90", y2="10", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="90", y1="10", x2="90", y2="30", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="40", y1="50", x2="60", y2="50", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="80", y1="50", x2="90", y2="50", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="90", y1="50", x2="90", y2="30", stroke="black", stroke_width="1")
        
        # Camino superior (relé K801)
        upper_path = SubElement(coach, "g", transform="translate(40, 10)")
        upper_path.append(self.create_contact_svg(k801_state, label="K801"))
    
        # Camino inferior (serie de K800 y K802)
        lower_path = SubElement(coach, "g", transform="translate(20, 50)")
        lower_path.append(self.create_contact_svg(k800_state, x_offset=0, label="K800"))
        lower_path.append(self.create_contact_svg(k802_state, x_offset=40, label="K802"))  # Desplazado 40 unidades a la derecha
        
        # if int(k753_state)==1 and int(s25_state)==0:
        #     bypass_backcolor = "green"
        #     bypass_state=2
        # else:
        #     bypass_backcolor = "red"
        #     bypass_state=2  

        
        # Líneas de entrada y salida y bifurcación entre coches en función de si es primer endcoach o último
        
        if position=="left":
            SubElement(coach, "line", x1="5", y1="30", x2="10", y2="30", stroke="black", stroke_width="1")
            SubElement(coach, "line", x1="5", y1="30", x2="5", y2="90", stroke="black", stroke_width="1")
            SubElement(coach, "line", x1="5", y1="90", x2="100", y2="90", stroke="black", stroke_width="1")
            SubElement(coach, "line", x1="90", y1="30", x2="100", y2="30", stroke="black", stroke_width="1")  # Salida
            
            SubElement(coach, "text", x="60", y="37.5", transform="rotate(270 90 30)", **{"text-anchor": "right","font-style": "italic","font-size": "7"}).text = "XM06:24"
            SubElement(coach, "text", x="67.5", y="85",**{"text-anchor": "right","font-style": "italic","font-size": "7"}).text = "XM06:25"
            SubElement(coach, "circle", cx="100",cy="30",r="2",fill="black")
            SubElement(coach, "circle", cx="100",cy="90",r="2",fill="black")
            
            SubElement(coach, "line", x1="5", y1="115", x2="40", y2="115", stroke="black", stroke_width="1")
            SubElement(coach, "line", x1="60", y1="115", x2="100", y2="115", stroke="black", stroke_width="1")
            SubElement(coach, "line", x1="5", y1="165", x2="100", y2="165", stroke="black", stroke_width="1") 
            SubElement(coach, "line", x1="5", y1="165", x2="5", y2="115", stroke="black", stroke_width="1")
            
            SubElement(coach, "line", x1="35", y1="225", x2="100", y2="225", stroke="black", stroke_width="1")  
            SubElement(coach, "line", x1="35", y1="275", x2="100", y2="275", stroke="black", stroke_width="1")
            
            SubElement(coach, "text", x="67.5", y="235", **{"text-anchor": "right","font-style": "italic","font-size": "7"}).text = "XM06:17"
            SubElement(coach, "text", x="67.5", y="270", **{"text-anchor": "right","font-style": "italic","font-size": "7"}).text = "XM06:18"
            
            SubElement(coach, "circle", cx="100",cy="225",r="2",fill="black")
            SubElement(coach, "circle", cx="100",cy="275",r="2",fill="black")
            
            SubElement(coach, "circle", cx="100",cy="115",r="2",fill="black")
            SubElement(coach, "circle", cx="100",cy="165",r="2",fill="black")
            
            SubElement(coach, "text", x="70", y="125", **{"text-anchor": "right","font-style": "italic","font-size": "7"}).text = "XM06:7"
            SubElement(coach, "text", x="70", y="160", **{"text-anchor": "right","font-style": "italic","font-size": "7"}).text = "XM06:8"
                        
        if position=="right":
            SubElement(coach, "line", x1="0", y1="30", x2="10", y2="30", stroke="black", stroke_width="1")
            SubElement(coach, "line", x1="95", y1="30", x2="95", y2="90", stroke="black", stroke_width="1")
            SubElement(coach, "line", x1="0", y1="90", x2="95", y2="90", stroke="black", stroke_width="1")
            SubElement(coach, "line", x1="90", y1="30", x2="95", y2="30", stroke="black", stroke_width="1")  # Salida
            SubElement(coach, "text", x="60", y="-52.5", transform="rotate(270 90 30)", **{"text-anchor": "right","font-style": "italic","font-size": "7"}).text = "XM06:24"
            SubElement(coach, "text", x="5", y="85",**{"text-anchor": "right","font-style": "italic","font-size": "7"}).text = "XM06:25"
    
            SubElement(coach, "line", x1="0", y1="115", x2="40", y2="115", stroke="black", stroke_width="1")
            SubElement(coach, "line", x1="60", y1="115", x2="95", y2="115", stroke="black", stroke_width="1")
            SubElement(coach, "line", x1="0", y1="165", x2="95", y2="165", stroke="black", stroke_width="1") 
            SubElement(coach, "line", x1="95", y1="165", x2="95", y2="115", stroke="black", stroke_width="1")
            
            SubElement(coach, "line", x1="0", y1="225", x2="65", y2="225", stroke="black", stroke_width="1")  
            SubElement(coach, "line", x1="0", y1="275", x2="65", y2="275", stroke="black", stroke_width="1")
            
            SubElement(coach, "text", x="5", y="235", **{"text-anchor": "left","font-style": "italic","font-size": "7"}).text = "XM06:17"
            SubElement(coach, "text", x="5", y="270", **{"text-anchor": "left","font-style": "italic","font-size": "7"}).text = "XM06:18"
            
            SubElement(coach, "text", x="5", y="125", **{"text-anchor": "right","font-style": "italic","font-size": "7"}).text = "XM06:7"
            SubElement(coach, "text", x="5", y="160", **{"text-anchor": "right","font-style": "italic","font-size": "7"}).text = "XM06:8"
                
        if int(k804_state)==1:
            k804_state=0
        else:
            k804_state=1

        # Determinar el color de fondo del coche
        if k801_state or (k800_state and k802_state):
            background_color = "green"
        else:
            background_color = "red"
            
    
        SubElement(coach, "rect", x="0", y="0", width="100", height="95", fill=background_color, opacity="0.15") 
        
        bypass = SubElement(coach, "g", transform="translate(40, 115)")
        bypass.append(self.create_contact_svg(k804_state, label="K804"))
        
        if k804_state:
            background_color = "green"
        else:
            background_color = "red"
            
        SubElement(coach, "rect", x="0", y="95", width="100", height="100", fill=background_color, opacity="0.15") 
        SubElement(coach, "line", x1="0", y1="95", x2="100", y2="95", stroke="black", **{"stroke-width": "4"}, opacity="0.35")

        SubElement(coach, "text", x="5", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9"}).text = "S60:"
        SubElement(coach, "text", x="5", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9"}).text = "S62:"
        SubElement(coach, "text", x="50", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9"}).text = "S255:"
        SubElement(coach, "text", x="50", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9"}).text = "S256:"

        

        if s60 != s60_r:
            SubElement(coach, "text", x="22", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "yellow"}).text = "Error"
        elif s60 == "0":
            SubElement(coach, "text", x="22", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9",  "fill": "green"}).text = "Off"
        else:
            SubElement(coach, "text", x="22", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "red"}).text = "Activo"

        if s62 != s62_r:
            SubElement(coach, "text", x="22", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "yellow"}).text = "Error"
        elif s62 == "0":
            SubElement(coach, "text", x="22", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "green"}).text = "Off"
        else:
            SubElement(coach, "text", x="22", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "red"}).text = "Activo"

        if s255 != s255_r:
            SubElement(coach, "text", x="72", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "yellow"}).text = "Error"
        elif s255 == "0":
            SubElement(coach, "text", x="72", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "green"}).text = "Off"
        else:
            SubElement(coach, "text", x="72", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "red"}).text = "Activo"

        if s256 != s256_r:
            SubElement(coach, "text", x="72", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "yellow"}).text = "Error"
        elif s256 == "0":
            SubElement(coach, "text", x="72", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "green"}).text = "Off"
        else:
            SubElement(coach, "text", x="72", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "red"}).text = "Activo"
        
        
        return coach

    def pmr_dsb1(self, coach_name, coach_pos, k801_state, k800_state, k802_state, k810_state, k811_state, k812_state, sifa1_state, sifa2_state, sifa1_forzed, sifa2_forzed, k804_state, k814_state, k753_state, s25_state, s60, s60_r, s62, s62_r, s256, s256_r, s255, s255_r, fr_riom_sc1, fr_riom_sc1r, fr_riom_sc2, fr_riom_sc2r, s60_b1, s60_r_b1, s62_b1, s62_r_b1, s256_b1, s256_r_b1):
        
        coach = Element("g")
        
        if int(k800_state)==1:
            
            k800_state=0
        else:
            k800_state=1
        
        if int(k801_state)==1:
            k801_state=0
        else:
            k801_state=1
        
        if int(k802_state)==1:
            k802_state=0
        else:
            k802_state=1


        if int(k810_state)==1:
            
            k810_state=0
        else:
            k810_state=1
        
        if int(k811_state)==1:
            k811_state=0
        else:
            k811_state=1
        
        if int(k812_state)==1:
            k812_state=0
        else:
            k812_state=1

            
        # Línea de entrada al coche (ajustada para ser de igual longitud)
        SubElement(coach, "line", x1="150", y1="30", x2="160", y2="30", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="160", y1="50", x2="160", y2="10", stroke="black", stroke_width="1")  # Bifurcación arriba
        SubElement(coach, "line", x1="160", y1="10", x2="190", y2="10", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="160", y1="50", x2="170", y2="50", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="210", y1="10", x2="240", y2="10", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="240", y1="10", x2="240", y2="30", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="190", y1="50", x2="210", y2="50", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="230", y1="50", x2="240", y2="50", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="240", y1="50", x2="240", y2="30", stroke="black", stroke_width="1")

        SubElement(coach, "line", x1="250", y1="30", x2="260", y2="30", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="260", y1="30", x2="260", y2="10", stroke="black", stroke_width="1")  # Bifurcación arriba
        SubElement(coach, "line", x1="260", y1="30", x2="260", y2="50", stroke="black", stroke_width="1")  # Bifurcación abajo
        SubElement(coach, "line", x1="260", y1="10", x2="290", y2="10", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="260", y1="50", x2="270", y2="50", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="310", y1="10", x2="340", y2="10", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="340", y1="10", x2="340", y2="30", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="290", y1="50", x2="310", y2="50", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="330", y1="50", x2="340", y2="50", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="340", y1="50", x2="340", y2="30", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="340", y1="30", x2="350", y2="30", stroke="black", stroke_width="1")
        
        SubElement(coach, "line", x1="0", y1="30", x2="5", y2="30", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="5", y1="30", x2="10", y2="90", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="10", y1="90", x2="350", y2="90", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="0", y1="90", x2="5", y2="90", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="5", y1="90", x2="10", y2="30", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="10", y1="30", x2="100", y2="30", stroke="black", stroke_width="1")
            
        # Camino superior (relé K801)
        upper_path = SubElement(coach, "g", transform="translate(190, 10)")
        upper_path.append(self.create_contact_svg(k801_state, label="K801"))

        # Camino inferior (serie de K800 y K802)
        lower_path = SubElement(coach, "g", transform="translate(170, 50)")
        lower_path.append(self.create_contact_svg(k800_state, x_offset=0, label="K800"))
        lower_path.append(self.create_contact_svg(k802_state, x_offset=40, label="K802"))  # Desplazado 40 unidades a la derecha

        #Determina si el comportamiento de las RIOMS es correcto
        if int(fr_riom_sc1)>240:
            SubElement(coach, "text", x="200", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "red"}).text = "RIOM SC APAGADA"     
        elif int(fr_riom_sc1r)>240:
            SubElement(coach, "text", x="200", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "red"}).text = "RIOM SCr APAGADA"
        elif k800_state and k802_state and not k801_state:
            SubElement(coach, "text", x="200", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "green"}).text = "CERRADO POR REDUNDANTE"
        elif k801_state and not k800_state and k802_state:
            SubElement(coach, "text", x="200", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "green"}).text = "CERRADO POR PRINCIPAL"
        elif k800_state and not k801_state and not k802_state:
            SubElement(coach, "text", x="200", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "red"}).text = "ABIERTO"
        else:
            SubElement(coach, "text", x="200", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "red"}).text = "ERROR DE CABLEADO"
        
        #Contacto S25
        s25_contact=SubElement(coach, "g", transform="translate(100, 30)")
        s25_contact.append(self.create_contact_svg(int(s25_state), label="S25"))
        #Línea tras contacto
        SubElement(coach, "line", x1="120", y1="30", x2="150", y2="30", stroke="black", stroke_width="1")  
        
        
        # Conexión horizontal después de bifurcación y contacto (ajustada)
        SubElement(coach, "line", x1="240", y1="30", x2="250", y2="30", stroke="black", stroke_width="1")  # Salida
        
        # Determinar el color de fondo del coche
        if (k801_state or (k800_state and k802_state)) and (k811_state or (k810_state and k812_state)):
            background_color = "green"
        else:
            background_color = "red"
            
        SubElement(coach, "rect", x="0", y="0", width="350", height="95", fill=background_color, opacity="0.15")
        SubElement(coach, "line", x1="350", y1="0", x2="350", y2="315", stroke="black", **{"stroke-width": "1", "stroke-dasharray": "5, 5"}, opacity="0.35")
        upper_path = SubElement(coach, "g", transform="translate(290, 10)")
        upper_path.append(self.create_contact_svg(k811_state, label="K811"))
        lower_path = SubElement(coach, "g", transform="translate(270, 50)")
        lower_path.append(self.create_contact_svg(k810_state, x_offset=0, label="K810"))
        lower_path.append(self.create_contact_svg(k812_state, x_offset=40, label="K812")) 

        #Determina si el comportamiento de las RIOMS es correcto
        if int(fr_riom_sc2)>199:
            SubElement(coach, "text", x="300", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "red"}).text = "RIOM SC2 APAGADA"
        elif int(fr_riom_sc2r)>199:
            SubElement(coach, "text", x="300", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "red"}).text = "RIOM SC2r APAGADA"
        elif k810_state and k812_state and not k811_state:
            SubElement(coach, "text", x="300", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "green"}).text = "CERRADO POR REDUNDANTE"
        elif k811_state and not k810_state and k812_state:
            SubElement(coach, "text", x="300", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "green"}).text = "CERRADO POR PRINCIPAL"
        elif k810_state and not k811_state and not k812_state:
            SubElement(coach, "text", x="300", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "red"}).text = "ABIERTO"
        else:
            SubElement(coach, "text", x="300", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "red"}).text = "ERROR DE CABLEADO"
        
        sifa_1=SubElement(coach, "g", transform="translate(20, 40)")
        sifa_1.append(self.create_sifa(int(sifa1_state), int(sifa1_forzed),0, "SIFA 1"))
        
        sifa_2=SubElement(coach, "g", transform="translate(60, 40)")
        sifa_2.append(self.create_sifa(int(sifa2_state), int(sifa2_forzed),0,"SIFA 2"))
        
        #Líneas de 110V desde SIFA
        SubElement(coach, "line", x1="30", y1="60", x2="128", y2="60", stroke="purple", stroke_width="1")
        SubElement(coach, "line", x1="128", y1="60", x2="128", y2="0", stroke="purple", stroke_width="1")
        SubElement(coach, "text", x="115", y="10", text_anchor="middle", font_style="italic", font_size="8").text = "0V"
       
        
        SubElement(coach, "line", x1="135", y1="30", x2="135", y2="0", stroke="blue", stroke_width="1")
        SubElement(coach, "circle", cx="135",cy="30",r="2",fill="black")
        SubElement(coach, "text", x="137", y="10", text_anchor="middle", font_style="italic", font_size="8").text = "110V"
        
        SubElement(coach, "text", x="175", y="292",**{"text-anchor": "middle","font-style": "italic","font-size": "10"}).text = f"Coche {coach_pos+1}: {coach_name}"
        
        SubElement(coach, "text", x="12.5", y="85",**{"text-anchor": "left","font-style": "italic","font-size": "7"}).text = "XH06:25"
        SubElement(coach, "text", x="320", y="85",**{"text-anchor": "right","font-style": "italic","font-size": "7"}).text = "XH06:25"
        
        SubElement(coach, "circle", cx="350",cy="90",r="2",fill="black")
        SubElement(coach, "circle", cx="350",cy="30",r="2",fill="black")
        
        SubElement(coach, "text", x="60", y="287.5", transform="rotate(270 90 30)", **{"text-anchor": "right","font-style": "italic","font-size": "7"}).text = "XH06:24"
        SubElement(coach, "text", x="92.5", y="-51.5", transform="rotate(270 90 30)", **{"text-anchor": "right","font-style": "italic","font-size": "7"}).text = "XH06:24"
        
        SubElement(coach, "line", x1="0", y1="115", x2="30", y2="115", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="50", y1="115", x2="80", y2="115", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="100", y1="115", x2="130", y2="115", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="0", y1="165", x2="340", y2="165", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="340", y1="115", x2="345", y2="165", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="345", y1="165", x2="350", y2="165", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="200", y1="115", x2="340", y2="115", stroke="black", stroke_width="1")
        
        SubElement(coach, "line", x1="340", y1="165", x2="345", y2="115", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="345", y1="115", x2="350", y2="115", stroke="black", stroke_width="1")
        
        if int(k804_state)==1:
            
            k804_state=0
        else:
            k804_state=1
            
        if int(k814_state)==1:
            
            k814_state=0
        else:
            k814_state=1
        
        
        bypass = SubElement(coach, "g", transform="translate(30, 115)")
        bypass.append(self.create_contact_svg(k804_state, label="K804"))
        bypassb1 = SubElement(coach, "g", transform="translate(80, 115)")
        bypassb1.append(self.create_contact_svg(k814_state, label="K814"))
        
        k753=SubElement(coach, "g", transform="translate(190, 125)")
        k753.append(self.create_electovalve(k753_state,0, "K753"))
        

        
        if k804_state and k814_state:
            background_color = "green"
        else:
            background_color = "red"
                        
        if int(k753_state)==1 and int(s25_state)==0:
            bypass_backcolor = "green"
            bypass_state = 0
        else:
            bypass_backcolor = "red"
            bypass_state = 1
            
        SubElement(coach, "rect", x="0", y="95", width="125", height="100", fill=background_color, opacity="0.15")
        SubElement(coach, "rect", x="125", y="95", width="17", height="100", fill=background_color, opacity="0.15")
        SubElement(coach, "rect", x="142", y="95", width="75", height="75", fill=background_color, opacity="0.15")
        SubElement(coach, "rect", x="217", y="95", width="133", height="100", fill=background_color, opacity="0.15")
        SubElement(coach, "rect", x="142", y="170", width="75", height="60", fill=bypass_backcolor, opacity="0.15")
        SubElement(coach, "line", x1="0", y1="95", x2="350", y2="95", stroke="black", **{"stroke-width": "4"}, opacity="0.35")

        SubElement(coach, "line", x1="130", y1="192", x2="130", y2="97.5", stroke="blue", stroke_width="1")
        SubElement(coach, "line", x1="137", y1="145", x2="137", y2="97.5", stroke="purple", stroke_width="1")
        SubElement(coach, "line", x1="137", y1="145", x2="200", y2="145", stroke="purple", stroke_width="1")
        SubElement(coach, "line", x1="137", y1="145", x2="137", y2="275", stroke="purple", stroke_width="1")
        SubElement(coach, "circle", cx="137",cy="145",r="2",fill="black")
        SubElement(coach, "circle", cx="137",cy="275",r="2",fill="black")
        SubElement(coach, "text", x="105", y="110", text_anchor="middle", font_style="italic", font_size="8").text = "110V"
        SubElement(coach, "text", x="142", y="110", text_anchor="middle", font_style="italic", font_size="8").text = "0V"
        SubElement(coach, "circle", cx="130",cy="115",r="2",fill="black")
        
        SubElement(coach, "circle", cx="135",cy="30",r="2",fill="black")
        
        SubElement(coach, "circle", cx="150",cy="192",r="2",fill="black")
        
        SubElement(coach, "circle", cx="130",cy="192",r="2",fill="black")
        
        SubElement(coach, "line", x1="130", y1="192", x2="150", y2="192", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="150", y1="192", x2="150", y2="177", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="150", y1="192", x2="150", y2="207", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="150", y1="177", x2="160", y2="177", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="150", y1="207", x2="160", y2="207", stroke="black", stroke_width="1")
        
        if int(k753_state):
            k753_NC=0
        else:
            k753_NC=1
        
        c753 = SubElement(coach, "g", transform="translate(160, 207)")
        c753.append(self.create_contact_svg(k753_NC, label="K753"))
        
        s25 = SubElement(coach, "g", transform="translate(160, 177)")
        s25.append(self.create_contact_svg(int(s25_state), label="S25"))
        
        SubElement(coach, "line", x1="180", y1="177", x2="190", y2="177", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="180", y1="207", x2="190", y2="207", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="190", y1="177", x2="190", y2="207", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="190", y1="192", x2="210", y2="192", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="210", y1="192", x2="210", y2="225", stroke="black", stroke_width="1")
        
        SubElement(coach, "circle", cx="210",cy="225",r="2",fill="black")
        
        SubElement(coach, "line", x1="0", y1="225", x2="350", y2="225", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="0", y1="275", x2="350", y2="275", stroke="black", stroke_width="1")
        
        SubElement(coach, "text", x="5", y="235", **{"text-anchor": "left","font-style": "italic","font-size": "7"}).text = "XH06:17"
        SubElement(coach, "text", x="5", y="270", **{"text-anchor": "left","font-style": "italic","font-size": "7"}).text = "XH06:18"    
        SubElement(coach, "text", x="315.5", y="235", **{"text-anchor": "right","font-style": "italic","font-size": "7"}).text = "XH06:17"
        SubElement(coach, "text", x="315.5", y="270", **{"text-anchor": "right","font-style": "italic","font-size": "7"}).text = "XH06:18"
        
        SubElement(coach, "circle", cx="350",cy="225",r="2",fill="black")
        SubElement(coach, "circle", cx="350",cy="275",r="2",fill="black")
        
        SubElement(coach, "circle", cx="350",cy="115",r="2",fill="black")
        SubElement(coach, "circle", cx="350",cy="165",r="2",fill="black")
        
        SubElement(coach, "text", x="5", y="160", **{"text-anchor": "left","font-style": "italic","font-size": "7"}).text = "XH06:8"
        SubElement(coach, "text", x="-10", y="130", transform="rotate(270 5 125)", **{"text-anchor": "right","font-style": "italic","font-size": "7"}).text = "XH06:7"
        
        SubElement(coach, "text", x="317.5", y="175", **{"text-anchor": "right","font-style": "italic","font-size": "7"}).text = "XH06:8"
        SubElement(coach, "text", x="315.5", y="107.5", **{"text-anchor": "right","font-style": "italic","font-size": "7"}).text = "XH06:7"

        SubElement(coach, "text", x="5", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9"}).text = "S60:"
        SubElement(coach, "text", x="5", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9"}).text = "S62:"
        # SubElement(coach, "text", x="50", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9"}).text = "S255:"
        SubElement(coach, "text", x="50", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9"}).text = "S256:"

        SubElement(coach, "text", x="220", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9"}).text = "S60_B1:"
        SubElement(coach, "text", x="220", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9"}).text = "S62_B1:"
        # SubElement(coach, "text", x="50", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9"}).text = "S255:"
        SubElement(coach, "text", x="278", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9"}).text = "S256_B1:"

        if s60 != s60_r:
            SubElement(coach, "text", x="22", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "yellow"}).text = "Error"
        elif s60 == "0":
            SubElement(coach, "text", x="22", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9",  "fill": "green"}).text = "Off"
        else:
            SubElement(coach, "text", x="22", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "red"}).text = "Activo"

        if s62 != s62_r:
            SubElement(coach, "text", x="22", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "yellow"}).text = "Error"
        elif s62 == "0":
            SubElement(coach, "text", x="22", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "green"}).text = "Off"
        else:
            SubElement(coach, "text", x="22", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "red"}).text = "Activo"

        if s256 != s256_r:
            SubElement(coach, "text", x="72", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "yellow"}).text = "Error"
        elif s256 == "0":
            SubElement(coach, "text", x="72", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "green"}).text = "Off"
        else:
            SubElement(coach, "text", x="72", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "red"}).text = "Activo"

        if s60_b1 != s60_r_b1:
            SubElement(coach, "text", x="252", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "yellow"}).text = "Error"
        elif s60_b1 == "0":
            SubElement(coach, "text", x="252", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9",  "fill": "green"}).text = "Off"
        else:
            SubElement(coach, "text", x="252", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "red"}).text = "Activo"

        if s62_b1 != s62_r_b1:
            SubElement(coach, "text", x="252", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "yellow"}).text = "Error"
        elif s62_b1 == "0":
            SubElement(coach, "text", x="252", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "green"}).text = "Off"
        else:
            SubElement(coach, "text", x="252", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "red"}).text = "Activo"

        if s256_b1 != s256_r_b1:
            SubElement(coach, "text", x="315", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "yellow"}).text = "Error"
        elif s256_b1 == "0":
            SubElement(coach, "text", x="315", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "green"}).text = "Off"
        else:
            SubElement(coach, "text", x="315", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "red"}).text = "Activo"
        
        SubElement(coach, "rect", attrib={
            "x": "-300", "y": "195", "width": "442", "height": "120",
            "fill": bypass_backcolor, "opacity": "0.15",
            "data-role": "pmr-bypass-band"
        })

        SubElement(coach, "rect", attrib={
            "x": "142", "y": "230", "width": "75", "height": "100",
            "fill": bypass_backcolor, "opacity": "0.15",
            "data-role": "pmr-bypass-band"
        })

        SubElement(coach, "rect", attrib={
            "x": "217", "y": "195", "width": "2000", "height": "120",
            "fill": bypass_backcolor, "opacity": "0.15",
            "data-role": "pmr-bypass-band"
        })

        
        p810=SubElement(coach, "g", transform="translate(-265, 250)")
        p810.append(self.create_led(bypass_state,0, 15, "P810"))

        p810=SubElement(coach, "g", transform="translate(1415, 250)")
        p810.append(self.create_led(bypass_state,0, 15, "P810"))
        
        return coach

    def pmr_db_dsb2(self, coach_name, coach_pos, k801_state, k800_state, k802_state, k810_state, k811_state, k812_state, k804_state, k814_state, s60, s60_r, s62, s62_r, s256, s256_r, fr_riom_sc1, fr_riom_sc1r, fr_riom_sc2, fr_riom_sc2r, s60_b1, s60_r_b1, s62_b1, s62_r_b1, s256_b1, s256_r_b1):
        
        coach = Element("g")
        
        if int(k800_state)==1:
            
            k800_state=0
        else:
            k800_state=1
        
        if int(k801_state)==1:
            k801_state=0
        else:
            k801_state=1
        
        if int(k802_state)==1:
            k802_state=0
        else:
            k802_state=1


        if int(k810_state)==1:
            
            k810_state=0
        else:
            k810_state=1
        
        if int(k811_state)==1:
            k811_state=0
        else:
            k811_state=1
        
        if int(k812_state)==1:
            k812_state=0
        else:
            k812_state=1

            
        # Línea de entrada al coche (ajustada para ser de igual longitud)
        SubElement(coach, "line", x1="10", y1="30", x2="15", y2="30", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="15", y1="50", x2="15", y2="10", stroke="black", stroke_width="1")  # Bifurcación arriba
        SubElement(coach, "line", x1="15", y1="10", x2="45", y2="10", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="15", y1="50", x2="25", y2="50", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="65", y1="10", x2="95", y2="10", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="95", y1="10", x2="95", y2="30", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="45", y1="50", x2="65", y2="50", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="55", y1="50", x2="65", y2="50", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="85", y1="50", x2="95", y2="50", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="95", y1="50", x2="95", y2="30", stroke="black", stroke_width="1")

        SubElement(coach, "line", x1="95", y1="30", x2="110", y2="30", stroke="black", stroke_width="1") #250 260
        SubElement(coach, "line", x1="110", y1="30", x2="110", y2="10", stroke="black", stroke_width="1")  # Bifurcación arriba
        SubElement(coach, "line", x1="110", y1="30", x2="110", y2="50", stroke="black", stroke_width="1")  # Bifurcación abajo
        SubElement(coach, "line", x1="110", y1="10", x2="140", y2="10", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="110", y1="50", x2="120", y2="50", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="160", y1="10", x2="190", y2="10", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="190", y1="10", x2="190", y2="30", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="140", y1="50", x2="160", y2="50", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="180", y1="50", x2="190", y2="50", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="190", y1="50", x2="190", y2="30", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="190", y1="30", x2="200", y2="30", stroke="black", stroke_width="1")
        
        SubElement(coach, "line", x1="0", y1="30", x2="5", y2="30", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="5", y1="30", x2="10", y2="30", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="10", y1="90", x2="200", y2="90", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="0", y1="90", x2="5", y2="90", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="5", y1="90", x2="10", y2="90", stroke="black", stroke_width="1")
        
            
        # Camino superior (relé K801)
        upper_path = SubElement(coach, "g", transform="translate(45, 10)")
        upper_path.append(self.create_contact_svg(k801_state, label="K801"))

        # Camino inferior (serie de K800 y K802)
        lower_path = SubElement(coach, "g", transform="translate(25, 50)")
        lower_path.append(self.create_contact_svg(k800_state, x_offset=0, label="K800"))
        lower_path.append(self.create_contact_svg(k802_state, x_offset=40, label="K802"))  # Desplazado 40 unidades a la derecha

        #Determina si el comportamiento de las RIOMS es correcto
        if int(fr_riom_sc1)>240:
            SubElement(coach, "text", x="50", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "red"}).text = "RIOM SC APAGADA"     
        elif int(fr_riom_sc1r)>240:
            SubElement(coach, "text", x="50", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "red"}).text = "RIOM SCr APAGADA"
        elif k800_state and k802_state and not k801_state:
            SubElement(coach, "text", x="50", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "green"}).text = "CERRADO POR REDUNDANTE"
        elif k801_state and not k800_state and k802_state:
            SubElement(coach, "text", x="50", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "green"}).text = "CERRADO POR PRINCIPAL"
        elif k800_state and not k801_state and not k802_state:
            SubElement(coach, "text", x="50", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "red"}).text = "ABIERTO"
        else:
            SubElement(coach, "text", x="50", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "red"}).text = "ERROR DE CABLEADO"
        
        # Determinar el color de fondo del coche
        if (k801_state or (k800_state and k802_state)) and (k811_state or (k810_state and k812_state)):
            background_color = "green"
        else:
            background_color = "red"
            
        SubElement(coach, "rect", x="0", y="0", width="200", height="95", fill=background_color, opacity="0.15")
        SubElement(coach, "line", x1="200", y1="0", x2="200", y2="315", stroke="black", **{"stroke-width": "1", "stroke-dasharray": "5, 5"}, opacity="0.35")
        upper_path = SubElement(coach, "g", transform="translate(140, 10)")
        upper_path.append(self.create_contact_svg(k811_state, label="K811"))
        lower_path = SubElement(coach, "g", transform="translate(120, 50)")
        lower_path.append(self.create_contact_svg(k810_state, x_offset=0, label="K810"))
        lower_path.append(self.create_contact_svg(k812_state, x_offset=40, label="K812")) 

        #Determina si el comportamiento de las RIOMS es correcto
        if int(fr_riom_sc2)>199:
            SubElement(coach, "text", x="150", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "red"}).text = "RIOM SC2 APAGADA"
        elif int(fr_riom_sc2r)>199:
            SubElement(coach, "text", x="150", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "red"}).text = "RIOM SC2r APAGADA"
        elif k810_state and k812_state and not k811_state:
            SubElement(coach, "text", x="150", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "green"}).text = "CERRADO POR REDUNDANTE"
        elif k811_state and not k810_state and k812_state:
            SubElement(coach, "text", x="150", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "green"}).text = "CERRADO POR PRINCIPAL"
        elif k810_state and not k811_state and not k812_state:
            SubElement(coach, "text", x="150", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "red"}).text = "ABIERTO"
        else:
            SubElement(coach, "text", x="150", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "red"}).text = "ERROR DE CABLEADO"
        

        if int(k804_state)==1:
            
            k804_state=0
        else:
            k804_state=1
            
        if int(k814_state)==1:
            
            k814_state=0
        else:
            k814_state=1
        
        
        bypass = SubElement(coach, "g", transform="translate(50, 115)")
        bypass.append(self.create_contact_svg(k804_state, label="K804"))
        bypassb1 = SubElement(coach, "g", transform="translate(130, 115)")
        bypassb1.append(self.create_contact_svg(k814_state, label="K814"))

        SubElement(coach, "line", x1="0", y1="115", x2="50", y2="115", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="70", y1="115", x2="130", y2="115", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="150", y1="115", x2="200", y2="115", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="0", y1="165", x2="200", y2="165", stroke="black", stroke_width="1")
         
        if k804_state and k814_state:
            background_color = "green"
        else:
            background_color = "red"

        
        SubElement(coach, "rect", x="0", y="95", width="200", height="100", fill=background_color, opacity="0.15")
                        

        SubElement(coach, "text", x="5", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9"}).text = "S60:"
        SubElement(coach, "text", x="5", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9"}).text = "S62:"
        # SubElement(coach, "text", x="100", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9"}).text = "S255:"
        SubElement(coach, "text", x="45", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9"}).text = "S256:"

        SubElement(coach, "text", x="65", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9"}).text = "S60_B1:"
        SubElement(coach, "text", x="95", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9"}).text = "S62_B1:"
        # SubElement(coach, "text", x="50", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9"}).text = "S255:"
        SubElement(coach, "text", x="128", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9"}).text = "S256_B1:"

        if s60 != s60_r:
            SubElement(coach, "text", x="22", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "yellow"}).text = "Error"
        elif s60 == "0":
            SubElement(coach, "text", x="22", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9",  "fill": "green"}).text = "Off"
        else:
            SubElement(coach, "text", x="22", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "red"}).text = "Activo"

        if s62 != s62_r:
            SubElement(coach, "text", x="22", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "yellow"}).text = "Error"
        elif s62 == "0":
            SubElement(coach, "text", x="22", y="188",**{"text-anchor": "right","font-sTtyle": "italic","font-size": "9", "fill": "green"}).text = "Off"
        else:
            SubElement(coach, "text", x="22", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "red"}).text = "Activo"

        if s256 != s256_r:
            SubElement(coach, "text", x="67", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "yellow"}).text = "Error"
        elif s256 == "0":
            SubElement(coach, "text", x="67", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "green"}).text = "Off"
        else:
            SubElement(coach, "text", x="67", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "red"}).text = "Activo"

        if s60_b1 != s60_r_b1:
            SubElement(coach, "text", x="97", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "yellow"}).text = "Error"
        elif s60_b1 == "0":
            SubElement(coach, "text", x="97", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9",  "fill": "green"}).text = "Off"
        else:
            SubElement(coach, "text", x="97", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "red"}).text = "Activo"

        if s62_b1 != s62_r_b1:
            SubElement(coach, "text", x="127", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "yellow"}).text = "Error"
        elif s62_b1 == "0":
            SubElement(coach, "text", x="127", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "green"}).text = "Off"
        else:
            SubElement(coach, "text", x="127", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "red"}).text = "Activo"

        if s256_b1 != s256_r_b1:
            SubElement(coach, "text", x="165", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "yellow"}).text = "Error"
        elif s256_b1 == "0":
            SubElement(coach, "text", x="165", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "green"}).text = "Off"
        else:
            SubElement(coach, "text", x="165", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "red"}).text = "Activo"


        SubElement(coach, "text", x="100", y="292",**{"text-anchor": "middle","font-style": "italic","font-size": "10"}).text = f"Coche {coach_pos+1}: {coach_name}"
        
        SubElement(coach, "text", x="5", y="85",**{"text-anchor": "left","font-style": "italic","font-size": "7"}).text = "XH06:25"
        SubElement(coach, "text", x="170", y="85",**{"text-anchor": "right","font-style": "italic","font-size": "7"}).text = "XH06:25"
        SubElement(coach, "text", x="60", y="137.5", transform="rotate(270 90 30)", **{"text-anchor": "right","font-style": "italic","font-size": "7"}).text = "XH06:24"
        SubElement(coach, "text", x="60", y="-52.5", transform="rotate(270 90 30)", **{"text-anchor": "right","font-style": "italic","font-size": "7"}).text = "XH06:24"

        SubElement(coach, "text", x="5", y="235", **{"text-anchor": "left","font-style": "italic","font-size": "7"}).text = "XH06:17"
        SubElement(coach, "text", x="5", y="270", **{"text-anchor": "left","font-style": "italic","font-size": "7"}).text = "XH06:18"    
        SubElement(coach, "text", x="167.5", y="235", **{"text-anchor": "right","font-style": "italic","font-size": "7"}).text = "XH06:17"
        SubElement(coach, "text", x="167.5", y="270", **{"text-anchor": "right","font-style": "italic","font-size": "7"}).text = "XH06:18"
        
        SubElement(coach, "text", x="5", y="125", **{"text-anchor": "left","font-style": "italic","font-size": "7"}).text = "XH06:7"
        SubElement(coach, "text", x="5", y="160", **{"text-anchor": "left","font-style": "italic","font-size": "7"}).text = "XH06:8"    
        SubElement(coach, "text", x="170", y="125", **{"text-anchor": "right","font-style": "italic","font-size": "7"}).text = "XH06:7"
        SubElement(coach, "text", x="170", y="160", **{"text-anchor": "right","font-style": "italic","font-size": "7"}).text = "XH06:8"
          
        
        SubElement(coach, "circle", cx="200",cy="90",r="2",fill="black")
        SubElement(coach, "circle", cx="200",cy="30",r="2",fill="black")
        SubElement(coach, "circle", cx="200",cy="115",r="2",fill="black")
        SubElement(coach, "circle", cx="200",cy="165",r="2",fill="black")
        SubElement(coach, "circle", cx="200",cy="225",r="2",fill="black")
        SubElement(coach, "circle", cx="200",cy="275",r="2",fill="black")

        SubElement(coach, "line", x1="0", y1="225", x2="200", y2="225", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="0", y1="275", x2="200", y2="275", stroke="black", stroke_width="1")


        SubElement(coach, "line", x1="0", y1="95", x2="200", y2="95", stroke="black", **{"stroke-width": "4"}, opacity="0.35")
            
        return coach

    def cabcar(self, coach_name, coach_pos, k801_state, k800_state, k802_state, k804_state, s60, s60_r, s62, s62_r, s255, s255_r, s256, s256_r, s8, s8_r, s6, s6_r, s10, k1, k80, k81, k82, k83, sifa1_cond, sifa2_cond, s700, s701, s702, s703, s704, k700, k701, k710, k711, k708, k709, k731, k732, k740, k741, s25, s25_r, k753, fr_riom_sc1, fr_riom_sc1r):

        coach = Element("g")

        # print(sifa1_cond, sifa2_cond)

        if int(k800_state)==1:
            
            k800_state=0
        else:
            k800_state=1
        
        if int(k801_state)==1:
            k801_state=0
        else:
            k801_state=1
        
        if int(k802_state)==1:
            k802_state=0
        else:
            k802_state=1
            
        if int(s6)==1:            
            s6=0
        else:
            s6=1
        
        if int(s8)==1:
            s8=0
        else:
            s8=1
        
        if int(s10)==1:
            s10=0
        else:
            s10=1

        if int(k82)==1:
            k82=0
        else:
            k82=1
        
        if int(k83)==1:
            k83=0
        else:
            k83=1


        # Línea de entrada al coche (ajustada para ser de igual longitud)
        SubElement(coach, "line", x1="0", y1="30", x2="10", y2="30", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="10", y1="30", x2="10", y2="10", stroke="black", stroke_width="1")  # Bifurcación arriba
        SubElement(coach, "line", x1="10", y1="30", x2="10", y2="50", stroke="black", stroke_width="1")  # Bifurcación abajo
        SubElement(coach, "line", x1="10", y1="10", x2="40", y2="10", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="10", y1="50", x2="20", y2="50", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="60", y1="10", x2="90", y2="10", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="90", y1="10", x2="90", y2="30", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="40", y1="50", x2="60", y2="50", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="80", y1="50", x2="90", y2="50", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="90", y1="50", x2="90", y2="30", stroke="black", stroke_width="1")
        
        SubElement(coach, "line", x1="0", y1="90", x2="140", y2="90", stroke="black", stroke_width="1")
        
            
        # Camino superior (relé K801)
        upper_path = SubElement(coach, "g", transform="translate(40, 10)")
        upper_path.append(self.create_contact_svg(k801_state, x_offset=0, label="K801"))

        # Camino inferior (serie de K800 y K802)
        lower_path = SubElement(coach, "g", transform="translate(20, 50)")
        lower_path.append(self.create_contact_svg(k800_state, x_offset=0, label="K800"))
        lower_path.append(self.create_contact_svg(k802_state, x_offset=40, label="K802"))  # Desplazado 40 unidades a la derecha

        #Determina si el comportamiento de las RIOMS es correcto
        if int(fr_riom_sc1)>240:
            SubElement(coach, "text", x="50", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "red"}).text = "RIOM SC APAGADA"
        elif int(fr_riom_sc1r)>240:
            SubElement(coach, "text", x="50", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "red"}).text = "RIOM SCr APAGADA"
        elif k800_state and k802_state and not k801_state:
            SubElement(coach, "text", x="50", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "green"}).text = "CERRADO POR REDUNDANTE"
        elif k801_state and not k800_state:
            SubElement(coach, "text", x="50", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "green"}).text = "CERRADO POR PRINCIPAL"
        elif k800_state and not k801_state and not k802_state:
            SubElement(coach, "text", x="50", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "red"}).text = "ABIERTO"
        else:
            SubElement(coach, "text", x="50", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "red"}).text = "ERROR DE CABLEADO"

        # Conexión horizontal después de bifurcación y contacto (ajustada)
        SubElement(coach, "line", x1="90", y1="30", x2="100", y2="30", stroke="black", stroke_width="1")  # Salida

        #Líneas de 110V desde SIFA
        # SubElement(coach, "line", x1="100", y1="60", x2="100", y2="0", stroke="purple", stroke_width="1")
        # SubElement(coach, "text", x="87", y="10", text_anchor="middle", font_style="italic", font_size="8").text = "0V"
       
        
        SubElement(coach, "line", x1="100", y1="30", x2="100", y2="0", stroke="blue", stroke_width="1")
        SubElement(coach, "circle", cx="100",cy="30",r="2",fill="black")
        SubElement(coach, "text", x="102", y="10", text_anchor="middle", font_style="italic", font_size="8").text = "110V"
        
        SubElement(coach, "text", x="367.5", y="292",**{"text-anchor": "middle","font-style": "italic","font-size": "10"}).text = f"Coche {coach_pos+1}: {coach_name}"

        SubElement(coach, "line", x1="100", y1="30", x2="100", y2="60", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="100", y1="60", x2="105", y2="60", stroke="black", stroke_width="1")

        s25_contact=SubElement(coach, "g", transform="translate(105, 60)")
        s25_contact.append(self.create_contact_svg(int(s25), label="S25"))

        SubElement(coach, "line", x1="125", y1="60", x2="130", y2="60", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="130", y1="60", x2="130", y2="90", stroke="black", stroke_width="1")
        SubElement(coach, "circle", cx="130",cy="90",r="2",fill="black")

        SubElement(coach, "line", x1="140", y1="90", x2="140", y2="50", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="140", y1="50", x2="150", y2="50", stroke="black", stroke_width="1")

        s6_contact=SubElement(coach, "g", transform="translate(150, 50)")
        s6_contact.append(self.create_contact_svg(int(s6), label="S6"))
        SubElement(coach, "line", x1="170", y1="50", x2="180", y2="50", stroke="black", stroke_width="1")
        s8_contact=SubElement(coach, "g", transform="translate(180, 50)")
        s8_contact.append(self.create_contact_svg(int(s8), label="S8"))
        SubElement(coach, "line", x1="200", y1="50", x2="210", y2="50", stroke="black", stroke_width="1")
        s10_contact=SubElement(coach, "g", transform="translate(210, 50)")
        s10_contact.append(self.create_contact_svg(int(s10), label="S10"))

        SubElement(coach, "line", x1="230", y1="50", x2="237.5", y2="50", stroke="black", stroke_width="1")

        SubElement(coach, "circle", cx="237.5",cy="50",r="2",fill="black")

        SubElement(coach, "line", x1="237.5", y1="30", x2="237.5", y2="50", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="237.5", y1="75", x2="237.5", y2="50", stroke="black", stroke_width="1")

        SubElement(coach, "line", x1="237.5", y1="30", x2="245", y2="30", stroke="black", stroke_width="1")

        k1_contact=SubElement(coach, "g", transform="translate(245, 30)")
        k1_contact.append(self.create_contact_svg(int(k1), label="K1"))

        SubElement(coach, "line", x1="265", y1="30", x2="275", y2="30", stroke="black", stroke_width="1")

        SubElement(coach, "line", x1="275", y1="10", x2="275", y2="50", stroke="black", stroke_width="1")

        # SubElement(coach, "line", x1="275", y1="10", x2="285", y2="10", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="275", y1="50", x2="285", y2="50", stroke="black", stroke_width="1")

        s700_contact1=SubElement(coach, "g", transform="translate(300, 10)")
        s700_contact1.append(self.create_contact_svg(int(s700), label="S700"))

        k700_contact1=SubElement(coach, "g", transform="translate(285, 50)")
        k700_contact1.append(self.create_contact_svg(int(k700), label="K700"))

        k701_contact1=SubElement(coach, "g", transform="translate(315, 50)")
        k701_contact1.append(self.create_contact_svg(int(k701), label="K701"))

        SubElement(coach, "line", x1="275", y1="10", x2="300", y2="10", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="320", y1="10", x2="345", y2="10", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="305", y1="50", x2="315", y2="50", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="335", y1="50", x2="345", y2="50", stroke="black", stroke_width="1")

        SubElement(coach, "line", x1="345", y1="10", x2="345", y2="50", stroke="black", stroke_width="1")

        SubElement(coach, "line", x1="345", y1="30", x2="355", y2="30", stroke="black", stroke_width="1")

        #################################################################################################

        SubElement(coach, "line", x1="355", y1="10", x2="355", y2="50", stroke="black", stroke_width="1")

        SubElement(coach, "line", x1="355", y1="50", x2="365", y2="50", stroke="black", stroke_width="1")

        s701_contact1=SubElement(coach, "g", transform="translate(380, 10)")
        s701_contact1.append(self.create_contact_svg(int(s701), label="S701"))

        k711_contact1=SubElement(coach, "g", transform="translate(365, 50)")
        k711_contact1.append(self.create_contact_svg(int(k711), label="K711"))

        k710_contact1=SubElement(coach, "g", transform="translate(395, 50)")
        k710_contact1.append(self.create_contact_svg(int(k710), label="K710"))

        SubElement(coach, "line", x1="355", y1="10", x2="380", y2="10", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="400", y1="10", x2="425", y2="10", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="385", y1="50", x2="395", y2="50", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="415", y1="50", x2="425", y2="50", stroke="black", stroke_width="1")

        SubElement(coach, "line", x1="425", y1="10", x2="425", y2="50", stroke="black", stroke_width="1")

        SubElement(coach, "line", x1="425", y1="30", x2="435", y2="30", stroke="black", stroke_width="1")

        #######################################################################################################

        SubElement(coach, "line", x1="435", y1="10", x2="435", y2="50", stroke="black", stroke_width="1")

        SubElement(coach, "line", x1="435", y1="50", x2="445", y2="50", stroke="black", stroke_width="1")

        s703_contact1=SubElement(coach, "g", transform="translate(460, 10)")
        s703_contact1.append(self.create_contact_svg(int(s703), label="S703"))

        k732_contact1=SubElement(coach, "g", transform="translate(445, 50)")
        k732_contact1.append(self.create_contact_svg(int(k732), label="K732"))

        k731_contact1=SubElement(coach, "g", transform="translate(475, 50)")
        k731_contact1.append(self.create_contact_svg(int(k731), label="K731"))

        SubElement(coach, "line", x1="435", y1="10", x2="460", y2="10", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="480", y1="10", x2="505", y2="10", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="465", y1="50", x2="475", y2="50", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="495", y1="50", x2="505", y2="50", stroke="black", stroke_width="1")

        SubElement(coach, "line", x1="505", y1="10", x2="505", y2="50", stroke="black", stroke_width="1")

        SubElement(coach, "line", x1="505", y1="30", x2="515", y2="30", stroke="black", stroke_width="1")

        #######################################################################################################

        SubElement(coach, "line", x1="515", y1="10", x2="515", y2="50", stroke="black", stroke_width="1")

        SubElement(coach, "line", x1="515", y1="50", x2="525", y2="50", stroke="black", stroke_width="1")

        s704_contact1=SubElement(coach, "g", transform="translate(540, 10)")
        s704_contact1.append(self.create_contact_svg(int(s704), label="S704"))

        k741_contact1=SubElement(coach, "g", transform="translate(525, 50)")
        k741_contact1.append(self.create_contact_svg(int(k741), label="K741"))

        k740_contact1=SubElement(coach, "g", transform="translate(555, 50)")
        k740_contact1.append(self.create_contact_svg(int(k740), label="K740"))

        SubElement(coach, "line", x1="515", y1="10", x2="540", y2="10", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="560", y1="10", x2="585", y2="10", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="545", y1="50", x2="555", y2="50", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="575", y1="50", x2="585", y2="50", stroke="black", stroke_width="1")

        SubElement(coach, "line", x1="585", y1="10", x2="585", y2="50", stroke="black", stroke_width="1")

        SubElement(coach, "line", x1="585", y1="30", x2="600", y2="30", stroke="black", stroke_width="1")

        #######################################################################################################

        SubElement(coach, "line", x1="237.5", y1="75", x2="300", y2="75", stroke="black", stroke_width="1")

        k80_contact=SubElement(coach, "g", transform="translate(300, 75)")
        k80_contact.append(self.create_contact_svg(not int(k80), label="K80"))

        SubElement(coach, "line", x1="320", y1="75", x2="350", y2="75", stroke="black", stroke_width="1")

        k81_contact=SubElement(coach, "g", transform="translate(350, 75)")
        k81_contact.append(self.create_contact_svg(not int(k81), label="K81"))

        SubElement(coach, "line", x1="370", y1="75", x2="600", y2="75", stroke="black", stroke_width="1")

        SubElement(coach, "circle", cx="600",cy="30",r="2",fill="black")

        SubElement(coach, "line", x1="600", y1="75", x2="600", y2="30", stroke="black", stroke_width="1")

        SubElement(coach, "line", x1="600", y1="30", x2="720", y2="30", stroke="black", stroke_width="1")

        k82_coil=SubElement(coach, "g", transform="translate(607, 40)")
        k82_coil.append(self.create_electovalve(int(k82),0, "K82"))
        
        sifa_1=SubElement(coach, "g", transform="translate(635, 40)")
        sifa_1.append(self.create_sifa(not int(k82), not int(sifa1_cond),0,"SIFA 1"))

        sifa_2=SubElement(coach, "g", transform="translate(675, 40)")
        sifa_2.append(self.create_sifa(not int(k83), not int(sifa2_cond),0, "SIFA 2"))
        
        k83_coil=SubElement(coach, "g", transform="translate(712.5, 40)")
        k83_coil.append(self.create_electovalve(int(k83),0,"K83"))

        SubElement(coach, "line", x1="617", y1="60", x2="722.5", y2="60", stroke="purple", stroke_width="1")
        SubElement(coach, "line", x1="722.5", y1="60", x2="722.5", y2="90", stroke="purple", stroke_width="1")
        SubElement(coach, "text", x="707.5", y="90", text_anchor="middle", font_style="italic", font_size="8").text = "0V"

        SubElement(coach, "line", x1="0", y1="95", x2="735", y2="95", stroke="black", **{"stroke-width": "4"}, opacity="0.35")

        # Determinar el color de fondo del coche
        if (k801_state or (k800_state and k802_state)) and int(s6) and int(s8) and int(s10) and (int(k1) and (int(s700) or (int(k700) and int(k701))) and (int(s701) or (int(k711) and int(k710))) and (int(s703) or (int(k732) and int(k731))) and (int(s704) or (int(k741) and int(k740))) or (not int(k80) and not int(k81))):
            background_color = "green"
        else:
            background_color = "red"

        SubElement(coach, "rect", x="0", y="0", width="750", height="95", fill=background_color, opacity="0.15")

        SubElement(coach, "line", x1="0", y1="115", x2="40", y2="115", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="60", y1="115", x2="100", y2="115", stroke="black", stroke_width="1")

        bypass = SubElement(coach, "g", transform="translate(40, 115)")
        bypass.append(self.create_contact_svg(not int(k804_state), x_offset=0, label="K804"))
        
        if k804_state:
            background_color = "green"
        else:
            background_color = "red"
            
        SubElement(coach, "rect", x="0", y="95", width="100", height="100", fill=background_color, opacity="0.15")
        SubElement(coach, "line", x1="0", y1="95", x2="100", y2="95", stroke="black", **{"stroke-width": "4"}, opacity="0.35")

        SubElement(coach, "text", x="5", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9"}).text = "S60:"
        SubElement(coach, "text", x="5", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9"}).text = "S62:"
        SubElement(coach, "text", x="50", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9"}).text = "S255:"
        SubElement(coach, "text", x="50", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9"}).text = "S256:"

        if s60 != s60_r:
            SubElement(coach, "text", x="22", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "yellow"}).text = "Error"
        elif s60 == "0":
            SubElement(coach, "text", x="22", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9",  "fill": "green"}).text = "Off"
        else:
            SubElement(coach, "text", x="22", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "red"}).text = "Activo"

        if s62 != s62_r:
            SubElement(coach, "text", x="22", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "yellow"}).text = "Error"
        elif s62 == "0":
            SubElement(coach, "text", x="22", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "green"}).text = "Off"
        else:
            SubElement(coach, "text", x="22", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "red"}).text = "Activo"

        if s255 != s255_r:
            SubElement(coach, "text", x="72", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "yellow"}).text = "Error"
        elif s255 == "0":
            SubElement(coach, "text", x="72", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "green"}).text = "Off"
        else:
            SubElement(coach, "text", x="72", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "red"}).text = "Activo"

        if s256 != s256_r:
            SubElement(coach, "text", x="72", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "yellow"}).text = "Error"
        elif s256 == "0":
            SubElement(coach, "text", x="72", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "green"}).text = "Off"
        else:
            SubElement(coach, "text", x="72", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "red"}).text = "Activo"

        SubElement(coach, "text", x="5", y="125", **{"text-anchor": "left","font-style": "italic","font-size": "7"}).text = "XM06:7"
        SubElement(coach, "text", x="5", y="160", **{"text-anchor": "left","font-style": "italic","font-size": "7"}).text = "XM06:8"

        SubElement(coach, "line", x1="100", y1="115", x2="100", y2="95", stroke="blue", stroke_width="1")
        SubElement(coach, "circle", cx="100",cy="115",r="2",fill="black")
        SubElement(coach, "text", x="102", y="110", text_anchor="middle", font_style="italic", font_size="8").text = "110V"

        SubElement(coach, "line", x1="0", y1="165", x2="150", y2="165", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="150", y1="165", x2="150", y2="115", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="150", y1="115", x2="170", y2="115", stroke="black", stroke_width="1")

        s25_contact_2=SubElement(coach, "g", transform="translate(170, 115)")
        s25_contact_2.append(self.create_contact_svg(not int(s25), label="S25 (NC)"))

        SubElement(coach, "line", x1="190", y1="115", x2="230", y2="115", stroke="black", stroke_width="1")

        k753_coil=SubElement(coach, "g", transform="translate(220, 125)")
        k753_coil.append(self.create_electovalve(int(k753),0, "K753"))

        SubElement(coach, "line", x1="230", y1="145", x2="230", y2="195", stroke="purple", stroke_width="1")
        SubElement(coach, "line", x1="230", y1="195", x2="800", y2="195", stroke="purple", stroke_width="1")
        SubElement(coach, "text", x="233", y="160", text_anchor="middle", font_style="italic", font_size="8").text = "0V (110)"

        if int(k753) == 1:
            bypass_color = "green"
        elif int(k753) == 0:
            bypass_color = "red"

        SubElement(coach, "rect", x="100", y="95", width="650", height="100", fill=bypass_color, opacity="0.15")

        SubElement(coach, "line", x1="750", y1="215", x2="600", y2="215", stroke="orange", stroke_width="1")
        SubElement(coach, "text", x="635", y="225", text_anchor="middle", font_style="italic", font_size="8").text = "24V"

        k753_contact_2=SubElement(coach, "g", transform="translate(580, 215)")
        k753_contact_2.append(self.create_contact_svg(not int(k753), label="K753"))

        SubElement(coach, "line", x1="500", y1="215", x2="580", y2="215", stroke="black", stroke_width="1")

        SubElement(coach, "line", x1="500", y1="215", x2="500", y2="225", stroke="black", stroke_width="1")

        SubElement(coach, "circle", cx="500",cy="225",r="2",fill="black")
        SubElement(coach, "circle", cx="500",cy="275",r="2",fill="black")

        SubElement(coach, "line", x1="0", y1="225", x2="500", y2="225", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="0", y1="275", x2="500", y2="275", stroke="black", stroke_width="1")

        SubElement(coach, "line", x1="500", y1="275", x2="500", y2="285", stroke="black", stroke_width="1")

        SubElement(coach, "line", x1="500", y1="285", x2="750", y2="285", stroke="red", stroke_width="1")
        SubElement(coach, "text", x="635", y="279", text_anchor="middle", font_style="italic", font_size="8").text = "0V (24V)"

        p7 = SubElement(coach, "g", transform="translate(500, 250)")
        p7.append(self.create_led(not int(k753),0, 15, "P7"))

        endcar_led_distance = -(self.num_coaches * 100) + 35
        endcar_distance = -(self.num_coaches * 100)
        bypass_width = (self.num_coaches * 100) + 750

        p7=SubElement(coach, "g", transform=f"translate({endcar_led_distance}, 250)")
        p7.append(self.create_led(not int(k753),0, 15, "P7"))

        SubElement(coach, "rect", x=f"{endcar_distance}", y="195", width=f"{bypass_width}", height="110", fill=bypass_color, opacity="0.15")

        return coach

    def offline_coach(self, coach_id: str, index: int):
        from xml.etree.ElementTree import Element, SubElement

        coach = Element("g")

        SubElement(coach, "rect", x="0", y="0", width="100", height="305", fill="black", opacity="0.5")
        SubElement(
            coach,
            "line",
            x1="100", y1="0", x2="100", y2="315",
            stroke="black",
            **{"stroke-width": "1", "stroke-dasharray": "5, 5"},
            opacity="0.35"
        )
        SubElement(
            coach,
            "text",
            x="50", y="292",
            **{"text-anchor": "middle", "font-style": "italic", "font-size": "10"}
        ).text = f"Coche {index+1}"

        SubElement(
            coach,
            "text",
            x="50", y="162.5",
            fill="white",
            **{
                "text-anchor": "middle",
                "dominant-baseline": "central",
                "font-style": "italic",
                "font-size": "30",
                "transform": "rotate(-90, 50, 152.5)"
            }
        ).text = "OFFLINE"

        return coach

class DoorsGenerator(QSvgWidget):

    def __init__(self, project, endpoint_ids, doors_vars, project_coach_types, scale_factor = 1.25):
        super().__init__()

        self.project = project
        self.endpoint_ids = list(endpoint_ids)

        # Listas de variables (mismo orden que usabas antes)
        self.doors_vars = list(doors_vars)

        # Map de tipos (ya lo tienes en TCMS_vars)
        self.project_coach_types = project_coach_types

        # La var de tipo de coche (la usas para mostrar y para decidir dibujo)
        # OJO: en tu nuevo flujo dijiste que COACH_TYPE está al final de tsc_vars
        self.coach_type_var = self.doors_vars[-1] if self.doors_vars else None
        

        # snapshot actual (lo alimenta vars_warehouse -> build_svg_snapshot)
        self.snapshot = {"doors": {}}

        # Puertas con MaintMode activo (set de tuplas (endpoint_id, 'R'|'L'))
        self._maint_doors = set()
        # Ciclos al inicio del burnin: {(eid, side): (door_base, step_base)}
        self._burnin_baseline = {}

        self.scale_factor = float(scale_factor)
        self.scaled_doors_width = int(800 * self.scale_factor)
        self.scaled_doors_height = int(130 * self.scale_factor)
       
    def set_snapshot(self, snapshot: dict):
        self.snapshot = snapshot or {"doors": {}}
        self.render_from_snapshot()

    def set_maint_doors(self, doors):
        """Actualiza las puertas en MaintMode y redibuja el SVG."""
        self._maint_doors = set(doors)
        self.render_from_snapshot()

    def set_burnin_baseline(self, baseline):
        """Actualiza los ciclos de referencia al inicio del burnin y redibuja.
        baseline: {(eid, side): (door_cycles_base, step_cycles_base) | None}
        - Valor tupla  → establece/actualiza baseline de esa puerta.
        - Valor None   → elimina baseline de esa puerta (burnin detenido en ella).
        Hace merge: las puertas no mencionadas conservan su baseline.
        """
        for key, val in baseline.items():
            if val is None:
                self._burnin_baseline.pop(key, None)
            else:
                self._burnin_baseline[key] = val
        self.render_from_snapshot()

    def render_from_snapshot(self):
        svg = self.generate_svg_from_snapshot()
        self.load(bytearray(svg, encoding="utf-8"))
  
    def generate_svg_from_snapshot(self) -> str:

        coaches_dict = (self.snapshot or {}).get("doors", {}) or {}

        # Orden estable: el orden de endpoint_ids, pero solo los que existan en snapshot
        coach_ids = [eid for eid in self.endpoint_ids[:-1] if eid in coaches_dict]
        self.num_coaches = len(coach_ids)

        # Si no hay nada, dibuja un SVG vacío mínimo
        if self.num_coaches == 0:
            root = Element("svg", xmlns="http://www.w3.org/2000/svg", width="800", height="150")
            return tostring(root, encoding="unicode")

        # Tipos y online por coach (para offsets como el antiguo)
        coach_type_codes = []
        coach_online = []
        for eid in coach_ids:
            st = coaches_dict.get(eid, {}) or {}
            values = st.get("values", {}) or {}
            ct = values.get(self.coach_type_var, "")
            coach_type_codes.append(str(ct))
            coach_online.append(bool(st.get("online", False)))


        base_width = self.num_coaches * 100


        self.pmr_pos = coach_type_codes.index("5") if "5" in coach_type_codes else None
        self.cab_pos = coach_type_codes.index("2") if (self.project == "DB" and "2" in coach_type_codes) else None

        pmr_online = bool(coach_online[self.pmr_pos]) if self.pmr_pos is not None else False
        cab_online = bool(coach_online[self.cab_pos]) if self.cab_pos is not None else False

        corrected_svg_width = base_width

        svg_root = Element(
            "svg",
            xmlns="http://www.w3.org/2000/svg",
            width=str(corrected_svg_width),
            height="130",
            viewBox = f"0 0 {corrected_svg_width} 130"
        )

        self.setFixedSize(int(corrected_svg_width * self.scale_factor), int(130 * self.scale_factor))
        self.scaled_doors_width = int(corrected_svg_width * self.scale_factor)
        self.scaled_doors_height = int(130 * self.scale_factor)
        # print(f"Adjusted SVG width: {corrected_svg_width}, scaled size: {self.scaled_tsc_width}x{self.scaled_tsc_height}")

        # Genera cada coche (grupo <g>) y lo traslada en X
        for idx, eid in enumerate(coach_ids):
            st = coaches_dict.get(eid, {}) or {}
            values = st.get("values", {}) or {}
            coach_type = str(values.get(self.coach_type_var, ""))
            online = bool(st.get("online", False))
            
            coach_g, _flag = self.process_coach_from_values(
                coach_id=eid,
                index=idx,
                coach_type=coach_type,
                values=values,
                online=online,
                pmr_index = self.pmr_pos,
            )

            x_pos = idx * 100

            coach_g.set("transform", f"translate({x_pos}, 0)")
            svg_root.append(coach_g)


        return tostring(svg_root, encoding="unicode")

    def process_coach_from_values(self, coach_id, index, coach_type, values, online=True, pmr_index=None):

        READ_ERR = isagrafInterface.READ_ERROR

        if not online:
            return self.offline_coach(coach_id, index), False

        def build_list(vars_list):
            return [values.get(v, READ_ERR) for v in (vars_list or [])]

        def g(lst, i, default=READ_ERR):
            return lst[i] if (i is not None and i < len(lst)) else default

        doors_data = build_list(self.doors_vars)

        label = ""
        if isinstance(coach_type, str) and coach_type.isdigit():
            label = self.project_coach_types.get(int(coach_type), str(coach_type))

    
        step_closed_r = g(doors_data, 0)
        step_closed_l = g(doors_data, 1)
        closed_n_locked_r = g(doors_data, 2)
        closed_n_locked_l = g(doors_data, 3)
        second_remote_close_r = g(doors_data, 4)
        second_remote_close_l = g(doors_data, 5)
        remote_close_r = g(doors_data, 6)
        remote_close_l = g(doors_data, 7)
        step_open_r = g(doors_data, 8)
        step_open_l = g(doors_data, 9)
        door_open_r = g(doors_data, 10)
        door_open_l = g(doors_data, 11)
        eed_operated_r = g(doors_data, 12)
        eed_operated_l = g(doors_data, 13)
        ead_operated_r = g(doors_data, 14)
        ead_operated_l = g(doors_data, 15)
        emsw_operated_r = g(doors_data, 16)
        emsw_operated_l = g(doors_data, 17)
        door_oos_r = g(doors_data, 18)
        door_oos_l = g(doors_data, 19)
        step_oos_r = g(doors_data, 20)
        step_oos_l = g(doors_data, 21)
        step_manual_release_r = g(doors_data, 22)
        step_manual_release_l = g(doors_data, 23)
        burn_in_active_r = g(doors_data, 24)
        burn_in_active_l = g(doors_data, 25)
        last_burn_in_nok_r = g(doors_data, 26)
        last_burn_in_nok_l = g(doors_data, 27)
        last_burn_in_ok_r = g(doors_data, 28)
        last_burn_in_ok_l = g(doors_data, 29)
        burn_in_ready_r = g(doors_data, 30)
        burn_in_ready_l = g(doors_data, 31)
        code_b_r = g(doors_data, 32)
        code_b_l = g(doors_data, 33)
        code_a_r = g(doors_data, 34)
        code_a_l = g(doors_data, 35)
        pmr_outside_r = g(doors_data, 36)
        pmr_outside_l = g(doors_data, 37)
        pmr_inside_r = g(doors_data, 38)
        pmr_inside_l = g(doors_data, 39)
        echo_OH_r = g(doors_data, 40)
        echo_OH_l = g(doors_data, 41)
        echo_V10_r = g(doors_data, 42)
        echo_V10_l = g(doors_data, 43)
        echo_V3_r = g(doors_data, 44)
        echo_V3_l = g(doors_data, 45)
        echo_step_in_r = g(doors_data, 46)
        echo_step_in_l = g(doors_data, 47)
        echo_red_Stk_r = g(doors_data, 48)
        echo_red_Stk_l = g(doors_data, 49)
        major_sw_r = g(doors_data, 50)
        major_sw_l = g(doors_data, 51)
        minor_sw_r = g(doors_data, 52)
        minor_sw_l = g(doors_data, 53)
        hw_rev_r = g(doors_data, 54)
        hw_rev_l = g(doors_data, 55)
        homog_test_fail_r = g(doors_data, 56)
        homog_test_fail_l = g(doors_data, 57)
        homog_test_ok_r = g(doors_data, 58)
        homog_test_ok_l = g(doors_data, 59)
        homog_test_active_r = g(doors_data, 60)
        homog_test_active_l = g(doors_data, 61)
        uic_15_r = g(doors_data, 62)
        uic_15_l = g(doors_data, 63)
        uic_14_r = g(doors_data, 64)
        uic_14_l = g(doors_data, 65)
        uic_9_r = g(doors_data, 66)
        uic_9_l = g(doors_data, 67)
        uic_lat_mode_r = g(doors_data, 68)
        uic_lat_mode_l = g(doors_data, 69)
        safe_st_r = g(doors_data, 70)
        safe_st_l = g(doors_data, 71)
        tbo_mode_r = g(doors_data, 72)
        tbo_mode_l = g(doors_data, 73)
        obb_mode_r = g(doors_data, 74)
        obb_mode_l = g(doors_data, 75)
        active_release_r = g(doors_data, 76)
        active_release_l = g(doors_data, 77)
        energy_saving_r = g(doors_data, 78)
        energy_saving_l = g(doors_data, 79)
        cycle_count_door_r = g(doors_data, 80)
        cycle_count_door_l = g(doors_data, 81)
        cycle_count_step_r = g(doors_data, 82)
        cycle_count_step_l = g(doors_data, 83)
        failure_rate_r = g(doors_data, 84)
        failure_rate_l = g(doors_data, 85)
        n3_order_r = g(doors_data, 86)
        n3_order_l = g(doors_data, 87)
        
        maint_r = (coach_id, 'R') in self._maint_doors
        maint_l = (coach_id, 'L') in self._maint_doors
        _burnin_r = (burn_in_active_r, last_burn_in_ok_r, last_burn_in_nok_r, burn_in_ready_r)
        _burnin_l = (burn_in_active_l, last_burn_in_ok_l, last_burn_in_nok_l, burn_in_ready_l)

        def _cycle_diff(side, current_door, current_step):
            """Ciclos transcurridos desde el inicio del burnin para este lado.
            Devuelve (door_diff, step_diff) o None si no hay baseline."""
            entry = self._burnin_baseline.get((coach_id, side))
            # print(coach_id, entry)
            if entry is None:
                return None
            door_base, step_base = entry
            try:   door_diff = max(0, int(current_door) - door_base)
            except (ValueError, TypeError): door_diff = 0
            try:   step_diff = max(0, int(current_step) - step_base)
            except (ValueError, TypeError): step_diff = 0
            return (door_diff, step_diff)

        cycles_r = _cycle_diff('R', cycle_count_door_r, cycle_count_step_r)
        cycles_l = _cycle_diff('L', cycle_count_door_l, cycle_count_step_l)

        if coach_type in ['3','4','6','8','9','10']:
                if pmr_index is not None and index > pmr_index:
                    coach = self.normal_coach(label, index, closed_n_locked_l, step_closed_l, door_open_l, step_open_l, uic_15_l, uic_14_l, uic_9_l, tbo_mode_l, obb_mode_l, uic_lat_mode_l, failure_rate_l, code_a_l, code_b_l, door_oos_l, step_oos_l, closed_n_locked_r, step_closed_r, door_open_r, step_open_r, uic_15_r, uic_14_r, uic_9_r, tbo_mode_r, obb_mode_r, uic_lat_mode_r, failure_rate_r, code_a_r, code_b_r, door_oos_r, step_oos_r, burnin_r=_burnin_l, burnin_l=_burnin_r, safe_st_r=safe_st_l, safe_st_l=safe_st_r, maint_r=maint_l, maint_l=maint_r, cycles_r=cycles_l, cycles_l=cycles_r)
                else:
                    coach = self.normal_coach(label, index, closed_n_locked_r, step_closed_r, door_open_r, step_open_r, uic_15_r, uic_14_r, uic_9_r, tbo_mode_r, obb_mode_r, uic_lat_mode_r, failure_rate_r, code_a_r, code_b_r, door_oos_r, step_oos_r, closed_n_locked_l, step_closed_l, door_open_l, step_open_l, uic_15_l, uic_14_l, uic_9_l, tbo_mode_l, obb_mode_l, uic_lat_mode_l, failure_rate_l, code_a_l, code_b_l, door_oos_l, step_oos_l, burnin_r=_burnin_r, burnin_l=_burnin_l, safe_st_r=safe_st_r, safe_st_l=safe_st_l, maint_r=maint_r, maint_l=maint_l, cycles_r=cycles_r, cycles_l=cycles_l)
        elif coach_type in ['5']:
                coach = self.pmr_coach(label, index, closed_n_locked_r, step_closed_r, door_open_r, step_open_r, uic_15_r, uic_14_r, uic_9_r, tbo_mode_r, obb_mode_r, uic_lat_mode_r, failure_rate_r, code_a_r, code_b_r, door_oos_r, step_oos_r, closed_n_locked_l, step_closed_l, door_open_l, step_open_l, uic_15_l, uic_14_l, uic_9_l, tbo_mode_l, obb_mode_l, uic_lat_mode_l, failure_rate_l, code_a_l, code_b_l, door_oos_l, step_oos_l, burnin_r=_burnin_r, burnin_l=_burnin_l, safe_st_r=safe_st_r, safe_st_l=safe_st_l, maint_r=maint_r, maint_l=maint_l, cycles_r=cycles_r, cycles_l=cycles_l)
        elif coach_type in ['2'] and self.project == "DB":
                coach = self.cabcar_coach(label, index)
        elif coach_type in ['7']:
                coach = self.family_coach(label, index)
        elif coach_type in ['11']:
                if pmr_index is not None and index > pmr_index:
                    coach = self.end_coach(label, index, closed_n_locked_l, step_closed_l, door_open_l, step_open_l, uic_15_l, uic_14_l, uic_9_l, tbo_mode_l, obb_mode_l, uic_lat_mode_l, failure_rate_l, code_a_l, code_b_l, door_oos_l, step_oos_l, closed_n_locked_r, step_closed_r, door_open_r, step_open_r, uic_15_r, uic_14_r, uic_9_r, tbo_mode_r, obb_mode_r, uic_lat_mode_r, failure_rate_r, code_a_r, code_b_r, door_oos_r, step_oos_r, burnin_r=_burnin_l, burnin_l=_burnin_r, safe_st_r=safe_st_l, safe_st_l=safe_st_r, maint_r=maint_l, maint_l=maint_r, cycles_r=cycles_l, cycles_l=cycles_r)
                else:
                    coach = self.end_coach(label, index, closed_n_locked_r, step_closed_r, door_open_r, step_open_r, uic_15_r, uic_14_r, uic_9_r, tbo_mode_r, obb_mode_r, uic_lat_mode_r, failure_rate_r, code_a_r, code_b_r, door_oos_r, step_oos_r, closed_n_locked_l, step_closed_l, door_open_l, step_open_l, uic_15_l, uic_14_l, uic_9_l, tbo_mode_l, obb_mode_l, uic_lat_mode_l, failure_rate_l, code_a_l, code_b_l, door_oos_l, step_oos_l, burnin_r=_burnin_r, burnin_l=_burnin_l, safe_st_r=safe_st_r, safe_st_l=safe_st_l, maint_r=maint_r, maint_l=maint_l, cycles_r=cycles_r, cycles_l=cycles_l)
        else:
            return self.offline_coach(coach_id, index), False

        return coach, True

    def _burnin_bg(self, active, ok, nok, ready=0, maintenance = False) -> str:
        """
        Devuelve el color de fondo SVG para una mitad del coche según el estado burnin.
        Prioridad: activo > NOK > OK > ready > '' (sin fondo).
        Acepta int o str "0"/"1".
        """
        def _on(v):
            try:
                return int(v) == 1
            except (ValueError, TypeError):
                return False
        if maintenance:    
            if _on(active): return "#87CEEB"   # azul celeste — burnin en marcha
            if _on(ready):  return "#FFA040"   # naranja      — listo para burnin
            if _on(nok):    return "#CC1111"   # rojo claro   — burnin NOK
            if _on(ok):     return "#90EE90"   # verde claro  — burnin OK

        return ""

    def _mode_grid(self, parent, safe, tb0, lat, obb, uic15, uic14, x_col1, y_row1):
        """
        Dibuja una matriz 2x3 de indicadores de modo en el elemento SVG 'parent'.
        Cada celda: círculo coloreado (verde=activo, gris=inactivo) + label negro.
          Col 1 (x_col1)    : Safe   /  LAT
          Col 2 (x_col1+28) : TB0    /  OBB
          Col 3 (x_col1+56) : UIC15  /  UIC14
          Fila 1 (y_row1)   : Safe / TB0 / UIC15
          Fila 2 (y_row1+10): LAT  / OBB / UIC14
        """
        def _on(v):
            try:
                return int(v) == 1
            except (ValueError, TypeError):
                return False

        x2 = x_col1 + 28
        x3 = x_col1 + 56
        y2 = y_row1 + 10
        items = [
            (safe,  "Safe",  x_col1, y_row1),
            (tb0,   "TB0",   x2,     y_row1),
            (uic15, "U15",   x3,     y_row1),
            (lat,   "LAT",   x_col1, y2),
            (obb,   "OBB",   x2,     y2),
            (uic14, "U14",   x3,     y2),
        ]
        for val, label, x, y in items:
            color = "#00BB00" if _on(val) else "#AAAAAA"
            SubElement(parent, "circle",
                       cx=str(x + 3), cy=str(y - 3), r="3", fill=color)
            SubElement(parent, "text",
                       x=str(x + 8), y=str(y),
                       **{"font-size": "7", "font-family": "sans-serif",
                          "fill": "#222222"}).text = label

    def save_as_png(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Guardar como PNG", "", "Archivos PNG (*.png)"
        )
        if not filename:
            return
        if not filename.lower().endswith(".png"):
            filename += ".png"

        renderer = self.renderer()

        # 1) Usa viewBox si está disponible (más fiable para no cortar)
        vb = renderer.viewBoxF()
        if vb.isValid() and vb.width() > 0 and vb.height() > 0:
            logical_w = vb.width()
            logical_h = vb.height()
        else:
            size = renderer.defaultSize()
            if not size.isValid() or size.width() <= 0 or size.height() <= 0:
                size = self.size()
            logical_w = float(size.width())
            logical_h = float(size.height())

        # 2) Opción A: ancho objetivo en píxeles
        target_width_px = 4000
        scale = target_width_px / max(1.0, logical_w)
        img_w = max(1, int(round(logical_w * scale)))
        img_h = max(1, int(round(logical_h * scale)))

        image = QImage(img_w, img_h, QImage.Format_ARGB32_Premultiplied)
        image.fill(Qt.transparent)

        painter = QPainter(image)
        try:
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setRenderHint(QPainter.TextAntialiasing, True)
            painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

            # 3) Renderiza al rect destino: evita recortes por tamaños lógicos raros
            renderer.render(painter, QRectF(0, 0, img_w, img_h))
        finally:
            painter.end()

        if image.save(filename, "PNG"):
            QMessageBox.information(self, "Éxito", f"Imagen guardada correctamente en:\n{filename}")
        else:
            QMessageBox.critical(self, "Error", f"No se pudo guardar el PNG:\n{filename}")
            
    def create_door_svg(self, pmr, closed_and_locked, step_closed, door_open, step_open, code_a, code_b, failure_rate, side, oos, step_oos, x_offset=0, label=""):
        """
        Representa el estado de un contacto con una etiqueta.
        - opened=True para contacto abierto, False para cerrado.
        - x_offset para desplazar horizontalmente el contacto.
        - label es el texto que se mostrará debajo del contacto.
        """
        door = Element("g", transform=f"translate({x_offset}, 0)")

        if failure_rate:
            SubElement(door, "rect", x="-10", y="-3", width="20", height="6", fill="grey")
        else:
            if code_a:
                SubElement(door, "rect", x="-10", y="-3", width="20", height="6", fill="red")
            elif code_b:
                SubElement(door, "rect", x="-10", y="-3", width="20", height="6", fill="yellow")

            else:
                if oos:
                    SubElement(door, "rect", x="-10", y="-3", width="20", height="6", fill="orange")
                elif closed_and_locked:
                    SubElement(door, "rect", x="-10", y="-3", width="20", height="6", fill="black")
                elif door_open:
                    SubElement(door, "rect", x="-10", y="-3", width="20", height="6", fill="blue")
                else:
                    SubElement(door, "rect", x="-10", y="-3", width="20", height="6", fill="magenta")

                if pmr:
                    if step_oos:
                        if side == "R":
                            SubElement(door, "rect", x="-7", y="-6", width="14", height="3", fill="orange")
                        elif side == "L":
                            SubElement(door, "rect", x="-7", y="3",  width="14", height="3", fill="orange")
                    elif step_closed:
                        if side == "R":
                            SubElement(door, "rect", x="-7", y="-6", width="14", height="3", fill="black")
                        elif side == "L":
                            SubElement(door, "rect", x="-7", y="3",  width="14", height="3", fill="black")
                    elif step_open:
                        if side == "R":
                            SubElement(door, "rect", x="-7", y="-6", width="14", height="3", fill="blue")
                        elif side == "L":
                            SubElement(door, "rect", x="-7", y="3",  width="14", height="3", fill="blue")
                    else:
                        if side == "R":
                            SubElement(door, "rect", x="-7", y="-6", width="14", height="3", fill="magenta")
                        elif side == "L":
                            SubElement(door, "rect", x="-7", y="3",  width="14", height="3", fill="magenta")

        
        
        # if step_closed:
        #     SubElement(door, "rect", x="-7", y="0", width="14", height="4", fill="grey")
        
        # Etiqueta debajo del contacto
        SubElement(door, "text", x="0", y="12", text_anchor="middle", font_style="italic", font_size="8").text = label

        return door
        
    def normal_coach(self, coach_name, coach_pos, closed_and_locked_R, step_closed_R, door_open_R, step_open_R, UIC15_R, UIC14_R, UIC9_R, TB0_R, OBB_R, LAT_R, Failure_rate_R, fail_type_a_R, fail_type_b_R, oos_r, step_oos_r, closed_and_locked_L, step_closed_L, door_open_L, step_open_L, UIC15_L, UIC14_L, UIC9_L, TB0_L, OBB_L, LAT_L, Failure_rate_L, fail_type_a_L, fail_type_b_L, oos_l, step_oos_l, burnin_r=(0,0,0), burnin_l=(0,0,0), safe_st_r="0", safe_st_l="0", maint_r=False, maint_l=False, cycles_r=None, cycles_l=None):

        coach = Element("g")

        # Fondo de color burnin — mitad superior (puerta R) y mitad inferior (puerta L)
        bg_r = self._burnin_bg(*burnin_r, maint_r)
        if bg_r:
            SubElement(coach, "rect", x="0", y="0", width="100", height="50", fill=bg_r, opacity="0.30")
        bg_l = self._burnin_bg(*burnin_l, maint_l)
        if bg_l:
            SubElement(coach, "rect", x="0", y="50", width="100", height="50", fill=bg_l, opacity="0.30")

        SubElement(coach, "line", x1="100", y1="0", x2="100", y2="140", stroke="black", **{"stroke-width": "1", "stroke-dasharray": "5, 5"}, opacity="0.35")
        SubElement(coach, "text", x="50", y="128", **{"text-anchor": "middle", "font-style": "italic", "font-size": "9"}).text = f"Coche {coach_pos+1}: {coach_name}"

        # Matriz de modos — Puerta D (arriba)
        self._mode_grid(coach, safe_st_r, TB0_R, LAT_R, OBB_R, UIC15_R, UIC14_R, x_col1=10, y_row1=10)

        SubElement(coach, "line", x1="0", y1="40", x2="5", y2="40", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="0", y1="60", x2="5", y2="60", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="95", y1="40", x2="100", y2="40", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="95", y1="60", x2="100", y2="60", stroke="black", stroke_width="1")

        SubElement(coach, "line", x1="5", y1="40", x2="5", y2="30", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="5", y1="60", x2="5", y2="70", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="95", y1="40", x2="95", y2="30", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="95", y1="60", x2="95", y2="70", stroke="black", stroke_width="1")

        SubElement(coach, "line", x1="5", y1="30", x2="65", y2="30", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="5", y1="70", x2="65", y2="70", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="85", y1="30", x2="95", y2="30", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="85", y1="70", x2="95", y2="70", stroke="black", stroke_width="1")

        if int(Failure_rate_R) > 240:
            door_r_off = 1
        else:
            door_r_off = 0
        if int(Failure_rate_L) > 240:
            door_l_off = 1
        else:
            door_l_off = 0

        # Contador de ciclos burnin (desde el inicio del burnin)
        if cycles_r is not None:
            SubElement(coach, "text", x="37", y="42",
                       **{"text-anchor": "middle", "font-size": "7", "font-family": "sans-serif", "fill": "#005080"}
                       ).text = f"Ciclos: {cycles_r[0]}"
        if cycles_l is not None:
            SubElement(coach, "text", x="37", y="60",
                       **{"text-anchor": "middle", "font-size": "7", "font-family": "sans-serif", "fill": "#005080"}
                       ).text = f"Ciclos: {cycles_l[0]}"

        # Puerta
        upper_door = SubElement(coach, "g", transform="translate(75, 30)")
        lower_door = SubElement(coach, "g", transform="translate(75, 70)")
        upper_door.append(self.create_door_svg(0, int(closed_and_locked_R), int(step_closed_R), int(door_open_R), int(step_open_R), int(fail_type_a_R), int(fail_type_b_R), int(door_r_off), "R", int(oos_r), int(step_oos_r), x_offset=0, label=""))
        lower_door.append(self.create_door_svg(0, int(closed_and_locked_L), int(step_closed_L), int(door_open_L), int(step_open_L), int(fail_type_a_L), int(fail_type_b_L), int(door_l_off), "L", int(oos_l), int(step_oos_l), x_offset=0, label=""))

        # Matriz de modos — Puerta I (abajo)
        self._mode_grid(coach, safe_st_l, TB0_L, LAT_L, OBB_L, UIC15_L, UIC14_L, x_col1=10, y_row1=86)

        # Indicador de Modo Mantenimiento
        if maint_r or maint_l:
            maint_text = "Mantenimiento D+I" if (maint_r and maint_l) else ("Mantenimiento D" if maint_r else "Mantenimiento I")
            SubElement(coach, "rect", x="2", y="103", width="96", height="14",
                       fill="#FFD580", stroke="#CC9900", **{"stroke-width": "0.5"})
            SubElement(coach, "text", x="50", y="113",
                       **{"text-anchor": "middle", "font-size": "7", "font-family": "sans-serif", "fill": "#664400"}
                       ).text = maint_text
        else:
            maint_text = ("Modo Normal")
            # SubElement(coach, "rect", x="2", y="103", width="96", height="14",
            #            fill="#664400", stroke="#CC9900", **{"stroke-width": "0.5"})
            SubElement(coach, "text", x="50", y="113",
                       **{"text-anchor": "middle", "font-size": "7", "font-family": "sans-serif", "fill": "#664400"}
                       ).text = maint_text

        return coach

    def pmr_coach(self, coach_name, coach_pos, closed_and_locked_R, step_closed_R, door_open_R, step_open_R, UIC15_R, UIC14_R, UIC9_R, TB0_R, OBB_R, LAT_R, Failure_rate_R, fail_type_a_R, fail_type_b_R, oos_r, step_oos_r, closed_and_locked_L, step_closed_L, door_open_L, step_open_L, UIC15_L, UIC14_L, UIC9_L, TB0_L, OBB_L, LAT_L, Failure_rate_L, fail_type_a_L, fail_type_b_L, oos_l, step_oos_l, burnin_r=(0,0,0), burnin_l=(0,0,0), safe_st_r="0", safe_st_l="0", maint_r=False, maint_l=False, cycles_r=None, cycles_l=None):

        coach = Element("g")

        bg_r = self._burnin_bg(*burnin_r, maint_r)
        if bg_r:
            SubElement(coach, "rect", x="0", y="0", width="100", height="50", fill=bg_r, opacity="0.30")
        bg_l = self._burnin_bg(*burnin_l, maint_l)
        if bg_l:
            SubElement(coach, "rect", x="0", y="50", width="100", height="50", fill=bg_l, opacity="0.30")

        SubElement(coach, "line", x1="100", y1="0", x2="100", y2="140", stroke="black", **{"stroke-width": "1", "stroke-dasharray": "5, 5"}, opacity="0.35")
        SubElement(coach, "text", x="50", y="128", **{"text-anchor": "middle", "font-style": "italic", "font-size": "9"}).text = f"Coche {coach_pos+1}: {coach_name}"

        self._mode_grid(coach, safe_st_r, TB0_R, LAT_R, OBB_R, UIC15_R, UIC14_R, x_col1=10, y_row1=10)

        SubElement(coach, "line", x1="0", y1="40", x2="5", y2="40", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="0", y1="60", x2="5", y2="60", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="95", y1="40", x2="100", y2="40", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="95", y1="60", x2="100", y2="60", stroke="black", stroke_width="1")

        SubElement(coach, "line", x1="5", y1="40", x2="5", y2="30", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="5", y1="60", x2="5", y2="70", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="95", y1="40", x2="95", y2="30", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="95", y1="60", x2="95", y2="70", stroke="black", stroke_width="1")

        SubElement(coach, "line", x1="5", y1="30", x2="65", y2="30", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="5", y1="70", x2="65", y2="70", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="85", y1="30", x2="95", y2="30", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="85", y1="70", x2="95", y2="70", stroke="black", stroke_width="1")

        if int(Failure_rate_R) > 240:
            door_r_off = 1
        else:
            door_r_off = 0
        if int(Failure_rate_L) > 240:
            door_l_off = 1
        else:
            door_l_off = 0

        # Contador de ciclos burnin — PMR muestra puerta (Pta) y peldaño (Ped)
        if cycles_r is not None:
            SubElement(coach, "text", x="37", y="38",
                       **{"text-anchor": "middle", "font-size": "7", "font-family": "sans-serif", "fill": "#005080"}
                       ).text = f"Pta: {cycles_r[0]}"
            SubElement(coach, "text", x="37", y="46",
                       **{"text-anchor": "middle", "font-size": "7", "font-family": "sans-serif", "fill": "#005080"}
                       ).text = f"Ped: {cycles_r[1]}"
        if cycles_l is not None:
            SubElement(coach, "text", x="37", y="57",
                       **{"text-anchor": "middle", "font-size": "7", "font-family": "sans-serif", "fill": "#005080"}
                       ).text = f"Pta: {cycles_l[0]}"
            SubElement(coach, "text", x="37", y="65",
                       **{"text-anchor": "middle", "font-size": "7", "font-family": "sans-serif", "fill": "#005080"}
                       ).text = f"Ped: {cycles_l[1]}"

        upper_door = SubElement(coach, "g", transform="translate(75, 30)")
        lower_door = SubElement(coach, "g", transform="translate(75, 70)")
        upper_door.append(self.create_door_svg(1, int(closed_and_locked_R), int(step_closed_R), int(door_open_R), int(step_open_R), int(fail_type_a_R), int(fail_type_b_R), int(door_r_off), "R", int(oos_r), int(step_oos_r), x_offset=0, label=""))
        lower_door.append(self.create_door_svg(1, int(closed_and_locked_L), int(step_closed_L), int(door_open_L), int(step_open_L), int(fail_type_a_L), int(fail_type_b_L), int(door_l_off), "L", int(oos_l), int(step_oos_l), x_offset=0, label=""))

        self._mode_grid(coach, safe_st_l, TB0_L, LAT_L, OBB_L, UIC15_L, UIC14_L, x_col1=10, y_row1=86)

        if maint_r or maint_l:
            maint_text = "Mantenimiento D+I" if (maint_r and maint_l) else ("Mantenimiento D" if maint_r else "Mantenimiento I")
            SubElement(coach, "rect", x="2", y="103", width="96", height="14",
                       fill="#FFD580", stroke="#CC9900", **{"stroke-width": "0.5"})
            SubElement(coach, "text", x="50", y="113",
                       **{"text-anchor": "middle", "font-size": "7", "font-family": "sans-serif", "fill": "#664400"}
                       ).text = maint_text
        else:
            maint_text = ("Modo Normal")
            # SubElement(coach, "rect", x="2", y="103", width="96", height="14",
            #            fill="#664400", stroke="#CC9900", **{"stroke-width": "0.5"})
            SubElement(coach, "text", x="50", y="113",
                       **{"text-anchor": "middle", "font-size": "7", "font-family": "sans-serif", "fill": "#664400"}
                       ).text = maint_text
            
        return coach

    def cabcar_coach(self, coach_name, coach_pos):

        coach = Element("g")

        SubElement(coach, "line", x1="100", y1="0", x2="100", y2="130", stroke="black", **{"stroke-width": "1", "stroke-dasharray": "5, 5"}, opacity="0.35")
        SubElement(coach, "text", x="50", y="128", **{"text-anchor": "middle", "font-style": "italic", "font-size": "9"}).text = f"Coche {coach_pos+1}: {coach_name}"
        
        SubElement(coach, "line", x1="0", y1="40", x2="5", y2="40", stroke="black", stroke_width="1") #Líneas muelles 
        SubElement(coach, "line", x1="0", y1="60", x2="5", y2="60", stroke="black", stroke_width="1") #Líneas muelles
        
        SubElement(coach, "line", x1="5", y1="40", x2="5", y2="30", stroke="black", stroke_width="1") #Líneas muelles
        SubElement(coach, "line", x1="5", y1="60", x2="5", y2="70", stroke="black", stroke_width="1") #Líneas muelles

        SubElement(coach, "line", x1="5", y1="30", x2="65", y2="30", stroke="black", stroke_width="1") #Líneas horizontales
        SubElement(coach, "line", x1="5", y1="70", x2="65", y2="70", stroke="black", stroke_width="1") #Líneas horizontales

        SubElement(coach, "line", x1="65", y1="30", x2="95", y2="45", stroke="black", stroke_width="1") #Líneas diagonales
        SubElement(coach, "line", x1="65", y1="70", x2="95", y2="55", stroke="black", stroke_width="1") #Líneas diagonales

        SubElement(coach, "line", x1="95", y1="45", x2="95", y2="55", stroke="black", stroke_width="1") #Líneas diagonales


        return coach

    def end_coach(self, coach_name, coach_pos, closed_and_locked_R, step_closed_R, door_open_R, step_open_R, UIC15_R, UIC14_R, UIC9_R, TB0_R, OBB_R, LAT_R, Failure_rate_R, fail_type_a_R, fail_type_b_R, oos_r, step_oos_r, closed_and_locked_L, step_closed_L, door_open_L, step_open_L, UIC15_L, UIC14_L, UIC9_L, TB0_L, OBB_L, LAT_L, Failure_rate_L, fail_type_a_L, fail_type_b_L, oos_l, step_oos_l, burnin_r=(0,0,0), burnin_l=(0,0,0), safe_st_r="0", safe_st_l="0", maint_r=False, maint_l=False, cycles_r=None, cycles_l=None):

        coach = Element("g")

        bg_r = self._burnin_bg(*burnin_r, maint_r)
        if bg_r:
            SubElement(coach, "rect", x="0", y="0", width="100", height="50", fill=bg_r, opacity="0.30")
        bg_l = self._burnin_bg(*burnin_l, maint_l)
        if bg_l:
            SubElement(coach, "rect", x="0", y="50", width="100", height="50", fill=bg_l, opacity="0.30")

        SubElement(coach, "line", x1="100", y1="0", x2="100", y2="140", stroke="black", **{"stroke-width": "1", "stroke-dasharray": "5, 5"}, opacity="0.35")
        SubElement(coach, "text", x="50", y="128", **{"text-anchor": "middle", "font-style": "italic", "font-size": "9"}).text = f"Coche {coach_pos+1}: {coach_name}"

        self._mode_grid(coach, safe_st_r, TB0_R, LAT_R, OBB_R, UIC15_R, UIC14_R, x_col1=10, y_row1=10)

        SubElement(coach, "line", x1="95", y1="40", x2="100", y2="40", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="95", y1="60", x2="100", y2="60", stroke="black", stroke_width="1")

        SubElement(coach, "line", x1="95", y1="40", x2="95", y2="30", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="95", y1="60", x2="95", y2="70", stroke="black", stroke_width="1")

        SubElement(coach, "line", x1="95", y1="30", x2="45", y2="30", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="5", y1="30", x2="30", y2="30", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="95", y1="70", x2="45", y2="70", stroke="black", stroke_width="1")
        SubElement(coach, "line", x1="5", y1="70", x2="30", y2="70", stroke="black", stroke_width="1")

        SubElement(coach, "line", x1="5", y1="70", x2="5", y2="30", stroke="black", stroke_width="1")

        if int(Failure_rate_R) > 240:
            door_r_off = 1
        else:
            door_r_off = 0
        if int(Failure_rate_L) > 240:
            door_l_off = 1
        else:
            door_l_off = 0

        # Contador de ciclos burnin (desde el inicio del burnin)
        if cycles_r is not None:
            SubElement(coach, "text", x="37", y="42",
                       **{"text-anchor": "middle", "font-size": "7", "font-family": "sans-serif", "fill": "#005080"}
                       ).text = f"Ciclos: {cycles_r[0]}"
        if cycles_l is not None:
            SubElement(coach, "text", x="37", y="60",
                       **{"text-anchor": "middle", "font-size": "7", "font-family": "sans-serif", "fill": "#005080"}
                       ).text = f"Ciclos: {cycles_l[0]}"

        upper_door = SubElement(coach, "g", transform="translate(35, 30)")
        lower_door = SubElement(coach, "g", transform="translate(35, 70)")
        upper_door.append(self.create_door_svg(0, int(closed_and_locked_R), int(step_closed_R), int(door_open_R), int(step_open_R), int(fail_type_a_R), int(fail_type_b_R), int(door_r_off), "R", int(oos_r), int(step_oos_r), x_offset=0, label=""))
        lower_door.append(self.create_door_svg(0, int(closed_and_locked_L), int(step_closed_L), int(door_open_L), int(step_open_L), int(fail_type_a_L), int(fail_type_b_L), int(door_l_off), "L", int(oos_l), int(step_oos_l), x_offset=0, label=""))

        self._mode_grid(coach, safe_st_l, TB0_L, LAT_L, OBB_L, UIC15_L, UIC14_L, x_col1=10, y_row1=86)

        if maint_r or maint_l:
            maint_text = "Mantenimiento D+I" if (maint_r and maint_l) else ("Mantenimiento D" if maint_r else "Mantenimiento I")
            SubElement(coach, "rect", x="2", y="103", width="96", height="14",
                       fill="#FFD580", stroke="#CC9900", **{"stroke-width": "0.5"})
            SubElement(coach, "text", x="50", y="113",
                       **{"text-anchor": "middle", "font-size": "7", "font-family": "sans-serif", "fill": "#664400"}
                       ).text = maint_text
        else:
            maint_text = ("Modo Normal")
            # SubElement(coach, "rect", x="2", y="103", width="96", height="14",
            #            fill="#664400", stroke="#CC9900", **{"stroke-width": "0.5"})
            SubElement(coach, "text", x="50", y="113",
                       **{"text-anchor": "middle", "font-size": "7", "font-family": "sans-serif", "fill": "#664400"}
                       ).text = maint_text
            
        return coach

    def family_coach(self, coach_name, coach_pos):

        coach = Element("g")

        SubElement(coach, "line", x1="100", y1="0", x2="100", y2="140", stroke="black", **{"stroke-width": "1", "stroke-dasharray": "5, 5"}, opacity="0.35")
        SubElement(coach, "text", x="50", y="128", **{"text-anchor": "middle", "font-style": "italic", "font-size": "9"}).text = f"Coche {coach_pos+1}: {coach_name}"

        SubElement(coach, "line", x1="0", y1="40", x2="5", y2="40", stroke="black", stroke_width="1") #Líneas muelles
        SubElement(coach, "line", x1="0", y1="60", x2="5", y2="60", stroke="black", stroke_width="1") #Líneas muelles
        SubElement(coach, "line", x1="95", y1="40", x2="100", y2="40", stroke="black", stroke_width="1") #Líneas muelles 
        SubElement(coach, "line", x1="95", y1="60", x2="100", y2="60", stroke="black", stroke_width="1") #Líneas muelles
        
        SubElement(coach, "line", x1="5", y1="40", x2="5", y2="30", stroke="black", stroke_width="1") #Líneas muelles
        SubElement(coach, "line", x1="5", y1="60", x2="5", y2="70", stroke="black", stroke_width="1") #Líneas muelles
        SubElement(coach, "line", x1="95", y1="40", x2="95", y2="30", stroke="black", stroke_width="1") #Líneas muelles
        SubElement(coach, "line", x1="95", y1="60", x2="95", y2="70", stroke="black", stroke_width="1") #Líneas muelles

        SubElement(coach, "line", x1="5", y1="30", x2="95", y2="30", stroke="black", stroke_width="1") #Líneas horizontales
        SubElement(coach, "line", x1="5", y1="70", x2="95", y2="70", stroke="black", stroke_width="1") #Líneas horizontales

        return coach

    def offline_coach(self, coach_id: str, index: int):
        from xml.etree.ElementTree import Element, SubElement

        coach = Element("g")

        SubElement(coach, "rect", x="0", y="0", width="100", height="130", fill="black", opacity="0.5")
        SubElement(coach, "line", x1="100", y1="0", x2="100", y2="130",
                   stroke="black", **{"stroke-width": "1", "stroke-dasharray": "5, 5"}, opacity="0.35")
        SubElement(coach, "text", x="50", y="123",
                   **{"text-anchor": "middle", "font-style": "italic", "font-size": "9"}
                   ).text = f"Coche {index+1}"
        SubElement(coach, "text", x="50", y="65", fill="white",
                   **{"text-anchor": "middle", "dominant-baseline": "central",
                      "font-style": "italic", "font-size": "18", "transform": "rotate(-90, 50, 65)"}
                   ).text = "OFFLINE"

        return coach

class DoorLegendSvg(QSvgWidget):
    """
    Panel de leyenda colapsable para el lazo de puertas.
    - Plegado : pestaña estrecha con "Leyenda de puertas" en vertical.
    - Expandido: SVG con los colores y su descripción.
    Clic en cualquier parte para alternar el estado.
    """

    TAB_W     = 50
    CONTENT_W = 220

    LEGEND_ITEMS = [
        ("black",   "Cerrada y bloqueada"),
        ("blue",    "Abierta"),
        ("magenta", "En movimiento"),
        ("orange",  "Condenada"),
        ("red",     "Fallo tipo A (crítico)"),
        ("yellow",  "Fallo tipo B (advertencia)"),
        ("grey",    "Tasa de fallos excedida"),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._expanded = False
        self._h = 300
        self.setCursor(Qt.PointingHandCursor) #El cursor cambia a una mano para indicar que es interactivo
        self.setToolTip("Clic para ver/ocultar la leyenda de colores")
        self._render()

    def set_height(self, h: int):
        """Actualiza la altura del panel; llamar desde set_snapshot del DOORWindow."""
        self._h = max(h, 120)
        self._render()

    def panel_width(self) -> int:
        return self.CONTENT_W if self._expanded else self.TAB_W

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._expanded = not self._expanded
            self._render()
            # Notifica al DOORWindow padre para que reajuste el tamaño
            parent = self.parent()
            while parent is not None:
                if hasattr(parent, "_on_legend_toggled"):
                    parent._on_legend_toggled()
                    break
                parent = parent.parent()
        super().mousePressEvent(event)

    MIN_EXPANDED_H = 335  # altura mínima cuando la leyenda está expandida

    def _render(self):
        w = self.CONTENT_W if self._expanded else self.TAB_W
        h = max(self._h, self.MIN_EXPANDED_H) if self._expanded else self._h
        self.setFixedSize(w, h)

        root = Element(
            "svg",
            xmlns="http://www.w3.org/2000/svg",
            width=str(w),
            height=str(h),
        )

        # Fondo
        SubElement(root, "rect", x="0", y="0", width=str(w), height=str(h),
                   fill="#F0F0F0", stroke="#AAAAAA", **{"stroke-width": "1"})

        if not self._expanded:
            # ---- Estado plegado: texto vertical ----
            cx, cy = (w // 2) + 7 , h // 2
            SubElement(
                root, "text",
                x=str(cx), y=str(cy),
                **{
                    "text-anchor":       "middle",
                    "dominant-baseline": "middle",
                    "font-size":         "14",
                    "font-family":       "sans-serif",
                    "fill":              "#333333",
                    "transform":         f"rotate(-90,{cx},{cy})",
                }
            ).text = "▶ LEYENDA DE PUERTAS"
        else:
            # ---- Estado expandido: leyenda completa ----
            SubElement(
                root, "text",
                x=str(w // 2), y="20",
                **{
                    "text-anchor": "middle",
                    "font-size":   "10",
                    "font-weight": "bold",
                    "font-family": "sans-serif",
                    "fill":        "#333333",
                }
            ).text = "LEYENDA DE COLORES DE PUERTAS"

            SubElement(root, "line",
                       x1="6", y1="28", x2=str(w - 6), y2="28",
                       stroke="#BBBBBB", **{"stroke-width": "1"})

            rx, rw, rh = 8, 22, 14
            y = 40
            for color, desc in self.LEGEND_ITEMS:
                SubElement(root, "rect",
                           x=str(rx), y=str(y),
                           width=str(rw), height=str(rh),
                           fill=color, stroke="#555555",
                           **{"stroke-width": "0.5"})
                SubElement(
                    root, "text",
                    x=str(rx + rw + 6), y=str(y + rh - 2),
                    **{"font-size": "12", "font-family": "sans-serif", "fill": "#222222"}
                ).text = desc
                y += 22

            # ---- Segunda sección: colores de fondo del Burnin Test ----
            y += 6  # pequeño espacio extra
            SubElement(root, "line",
                       x1="6", y1=str(y), x2=str(w - 6), y2=str(y),
                       stroke="#BBBBBB", **{"stroke-width": "1"})
            y += 15
            SubElement(
                root, "text",
                x=str(w // 2), y=str(y),
                **{
                    "text-anchor": "middle",
                    "font-size":   "10",
                    "font-weight": "bold",
                    "font-family": "sans-serif",
                    "fill":        "#333333",
                }
            ).text = "FONDO (BURN-IN TEST)"
            y += 8

            BURNIN_ITEMS = [
                ("#FFA040", "Listo para Burn-In (Ready)"),
                ("#87CEEB", "Burn-In en marcha"),
                ("#90EE90", "Burn-In finalizado OK"),
                ("#CC1111", "Burn-In finalizado NOK"),
            ]
            for color, desc in BURNIN_ITEMS:
                SubElement(root, "rect",
                           x=str(rx), y=str(y),
                           width=str(rw), height=str(rh),
                           fill=color, stroke="#555555",
                           **{"stroke-width": "0.5"})
                SubElement(
                    root, "text",
                    x=str(rx + rw + 6), y=str(y + rh - 2),
                    **{"font-size": "12", "font-family": "sans-serif", "fill": "#222222"}
                ).text = desc
                y += 22

            SubElement(
                root, "text",
                x=str(w // 2), y=str(h - 8),
                **{
                    "text-anchor": "middle",
                    "font-size":   "8",
                    "font-family": "sans-serif",
                    "fill":        "#BBBBBB",
                }
            ).text = "◀ Clic para colapsar"

        self.load(bytearray(tostring(root, encoding="unicode"), "utf-8"))

class DiagnosticWindow(QMainWindow):
    closed = Signal()

    def __init__(self, title: str, fixed_w: int, fixed_h: int, parent=None, scale_factor = 1.0):
        super().__init__(parent)
        self.setWindowTitle(title)
        screen = QApplication.primaryScreen()
        size = screen.size()
        self.setFixedSize(int(min(fixed_w * scale_factor, size.width())), int(fixed_h * scale_factor))

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)

class TSCWindow(DiagnosticWindow):

    def __init__(self, *, project, endpoint_ids, tsc_vars, project_coach_types, tsc_cc_vars,
                 fixed_w: int, fixed_h: int, valid_ips: list, parent=None): #El asterisco indica que los argumentos siguientes deben ser pasados como palabras clave, es decir (project = x, endpoint_ids = y, etc) y no como argumentos posicionales (x, y, etc)
        
        super().__init__(title="TSC", fixed_w=fixed_w, fixed_h=fixed_h, parent=parent)


        central = QWidget()
        lay = QVBoxLayout(central)
        lay.setContentsMargins(6, 6, 6, 6)

        self.valid_ips = valid_ips
        self.project = project

        menubar = self.menuBar()
        export_menu = menubar.addMenu("Exportar")

        self.export_TSC_action = QAction("Guardar como PNG...", self)
        export_menu.addAction(self.export_TSC_action)
        

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(False)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.tsc = TSCGenerator(
            project=project,
            endpoint_ids=endpoint_ids,
            tsc_vars=tsc_vars,
            project_coach_types=project_coach_types,
            tsc_cc_vars=tsc_cc_vars,
        )

        self.export_TSC_action.triggered.connect(self.tsc.save_as_png)

        self.TSC_Diag_window = TSC_Diag_Window(project=self.project, endpoint_ids=endpoint_ids, project_coach_types=project_coach_types,fixed_w=800, fixed_h=400, valid_ips=self.valid_ips)

        self.scroll.setWidget(self.tsc)

        self.btn_diag = QPushButton("Mostrar causas de apertura del lazo")
        self.btn_diag.setCheckable(True)
        self.btn_diag.toggled.connect(self.TSC_Diag_window._on_toggled)
        self.TSC_Diag_window.closed.connect(lambda: self.btn_diag.setChecked(False))  # Para que el botón se desactive si se cierra la ventana de diagnóstico

        self.reset_failures = QPushButton("Reset de fallos de inestabilidad, temperaturas y sensores de rueda")
        self.reset_failures.clicked.connect(self._on_reset_failures_clicked)


        lay.addWidget(self.scroll)
        lay.addWidget(self.btn_diag)
        lay.addWidget(self.reset_failures)

        self.setCentralWidget(central)

        screen = QApplication.primaryScreen()
        self.max_width = screen.availableGeometry().width() - 10  # Deja un margen de 100 píxeles
        self.max_height = screen.availableGeometry().height() - 50  # Deja un margen de 100 píxeles

    def set_snapshot(self, snapshot: dict):
        self.tsc.set_snapshot(snapshot)
        self.setFixedSize(min(self.tsc.scaled_tsc_width, self.max_width), min(self.tsc.scaled_tsc_height + 110, self.max_height))

    def _on_reset_failures_clicked(self):
        mw = self.parent()
        if mw is None or not hasattr(mw, "endpoint_clients") or not hasattr(mw, "endpoint_ids"):
            QMessageBox.warning(self, "Error", "No encuentro endpoint_clients/endpoint_ids en el MainWindow.")
            return

        self.reset_failures.setEnabled(False)

        # diálogo simple de log (opcional)
        dlg = QDialog(self)
        dlg.setWindowTitle("Reseteando fallos…")
        dlg.resize(650, 350)
        lay = QVBoxLayout(dlg)
        txt = QTextEdit()
        txt.setReadOnly(True)
        lay.addWidget(txt)
        btn_cancel = QPushButton("Cancelar")
        lay.addWidget(btn_cancel)
        dlg.show()

        th = QThread(self)
        w = ResetFailuresWorker(mw.endpoint_ids, mw.endpoint_clients, wait_time=1.0, project = self.project)
        w.moveToThread(th)

        th.started.connect(w.start)
        w.log.connect(txt.append)

        def cleanup(ok: bool):
            txt.append("\nFIN: " + ("OK" if ok else "ERROR/CANCELADO"))
            self.reset_failures.setEnabled(True)
            th.quit()

        w.finished.connect(cleanup)
        btn_cancel.clicked.connect(w.cancel)

        th.start()

        # guardar referencias para que no los destruya el GC
        self._reset_thread = th
        self._reset_worker = w
        self._reset_dialog = dlg

class TSC_Diag_Window(DiagnosticWindow):

    def __init__(self, *, project, endpoint_ids, project_coach_types,
                 fixed_w: int, fixed_h: int, valid_ips: list, parent=None):

        self.project = project
        self.endpoint_ids = endpoint_ids
        self.project_coach_types = project_coach_types

        super().__init__(
            title="Causas de apertura de lazo de emergencia",
            fixed_w=fixed_w,
            fixed_h=fixed_h,
            parent=parent
        )

        # ---- TCMS Vars / diccionarios ----
        self._tcms = TCMS_vars()

        menubar = self.menuBar()
        export_menu = menubar.addMenu("Exportar")

        self.export_diag_action = QAction("Exportar tabla a Excel (.xlsx)", self)
        export_menu.addAction(self.export_diag_action)
        self.export_diag_action.triggered.connect(self._export_table_to_excel)

        # TSC_DIAG_VARS contiene SOLO las 32 flags
        # y coinciden en orden con filtered_TSC_DIAG_NAMES
        self._tsc_var_to_desc = dict(zip(
            self._tcms.TSC_DIAG_VARS,
            self._tcms.filtered_TSC_DIAG_NAMES
        ))

        # Dict BCU: keys SOLO desde el '.' en adelante
        self._bcu_diag_dict = getattr(self._tcms, "BCU_DIAGNOSIS_DICT", {})

        # ---- UI tabla ----
        self.table = QTableWidget(80, 4, self)
        self.table.setHorizontalHeaderLabels([
            "Coche",
            "IP",
            "Código de error",
            "Descripción"
        ])

        central = QWidget()
        self.layout = QVBoxLayout(central)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(8)

        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table.setShowGrid(True)
        self.table.setWordWrap(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setFocusPolicy(Qt.StrongFocus)

        vh = self.table.verticalHeader()
        vh.setDefaultSectionSize(26)

        hh = self.table.horizontalHeader()
        hh.setStretchLastSection(False)
        hh.setDefaultAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        hh.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(3, QHeaderView.Stretch)

        self.layout.addWidget(self.table)
        self.setCentralWidget(central)

        self.inverted_diagnostic_vars = [
        'bDNRA_Notlocked2',
        'bDNRA_Notlocked1',
        'bDNRA_Notlocked',
        'bDNRA_OK'
        ]

        self._default_sort_applied = False

        self._last_tsc_diag = {}

    def _on_toggled(self, checked):
        
        if checked:
            self.show()
            self.raise_()
            self.activateWindow()
            screen = QApplication.primaryScreen()
            max_width = screen.availableGeometry().width()  
            max_height = screen.availableGeometry().height() 
            self.move(int((max_width - min(self.size().width(), max_width))/2),int((max_height - min(self.size().height(), max_height))/2))

        else:
            self.close()

    def set_snapshot(self, snapshot: dict):
            
            tsc_diag = snapshot.get("tsc_diag", {})

            if hasattr(self, "_last_tsc_diag") and self._last_tsc_diag == tsc_diag:
                return
        
            self._last_tsc_diag = tsc_diag
            
            header = self.table.horizontalHeader()
            sort_col = header.sortIndicatorSection()
            sort_order = header.sortIndicatorOrder()

            # print("TSC_Diag_Window: Actualizando snapshot...")
            # print(f"Columna de ordenación actual: {sort_col}, Orden: {'Ascendente' if sort_order == Qt.AscendingOrder else 'Descendente'}")
            
            coach_types_by_endpoint = {}
            for endpoint_id, data in snapshot.get("tsc", {}).items():
                vals = (data or {}).get("values") or {}
                coach_types_by_endpoint[endpoint_id] = vals.get(
                    "oVCUCH_TRDP_DS_A000.COM_Vehicle_Type"
                )

            if self.project == "DB" and len(self.endpoint_ids) >= 2:
                last = self.endpoint_ids[-1]
                prev = self.endpoint_ids[-2]
                coach_types_by_endpoint[last] = coach_types_by_endpoint.get(prev)

            rows = []


            for endpoint_id, data in tsc_diag.items():
                diag_vals = (data or {}).get("values") or {}
                
                # lista = [
                #     'BCU_MVB2_DS_30D.bDIBA_Train_S2',
                #     'BCU_MVB2_DS_30D.bDIMGA_Train_S2',
                #     'BCU_MVB2_DS_30D.bDNRA_Notlocked',
                #     'BCU_MVB2_DS_30D.bDIMGA',
                #     'BCU_MVB2_DS_30D.bPBA_Speed',
                #     'BCUCH2_MVB1_DS_30F.bDIMGA_NOK',
                #     'BCUCH2_MVB1_DS_30F.bPBA_Speed_NOK',
                #     'BCUCH2_MVB1_DS_30F.bDIBA_Train_S2_NOK',
                #     'BCUCH1_MVB2_DS_30F.bDIBA_Train_S2_NOK',
                #     'BCUCH1_MVB2_DS_30F.bPBA_Speed_NOK',
                #     'BCUCH1_MVB2_DS_30F.bDIMGA_NOK',
                #     'BCU_MVB1_DS_06E.bDIBA_Train_S2',
                #     'BCU_MVB1_DS_06E.bDIMGA_Train_S2',
                #     'BCUCH1_MVB2_DS_310.bDNRA_OK',
                #     'BCUCH2_MVB1_DS_310.bDNRA_OK',
                #     'BCU_MVB1_DS_06E.bDIMGA',
                #     'BCU_MVB1_DS_06E.bPBA_Speed',
                #     'BCUCH1_MVB2_DS_310.bDNRA_Notlocked2',
                #     'BCUCH1_MVB2_DS_310.bDNRA_Notlocked1',
                #     'BCUCH2_MVB1_DS_310.bDNRA_Notlocked2',
                #     'BCUCH2_MVB1_DS_310.bDNRA_Notlocked1',
                # ]

                # if endpoint_id == "EP1":
                #     test = {k: diag_vals[k] for k in lista}
                    # print(test)
                 
                try:
                    coach_idx = self.endpoint_ids.index(endpoint_id) + 1
                except ValueError:
                    coach_idx = "?"

                coach_type = coach_types_by_endpoint.get(endpoint_id)
                coach_type_str = ""
                try:
                    if coach_type is not None:
                        coach_type_str = self.project_coach_types.get(
                            int(float(coach_type)), str(coach_type)
                        )
                except Exception:
                    coach_type_str = str(coach_type) if coach_type is not None else ""

                coach_label = f"{coach_idx}"
                if coach_type_str:
                    coach_label += f" ({coach_type_str})"

                for var_full, value in diag_vals.items():

                    var_short = var_full.split(".")[-1]

                    if value != "1" and value!= "0":
                        continue
                    
                    if value == "0" and var_short not in self.inverted_diagnostic_vars:
                        continue

                    bcu_hit = self._bcu_diag_dict.get(var_short)
                    if bcu_hit:
                        code = bcu_hit.get("Error Code", var_short)
                        desc = bcu_hit.get("Description", "Descripción no disponible")
                    elif var_full in self._tsc_var_to_desc:
                        code = var_short
                        desc = self._tsc_var_to_desc[var_full]
                    else:
                        code = var_short
                        desc = "Descripción no disponible"

                    if not var_short in self.inverted_diagnostic_vars:
                        rows.append((coach_label, endpoint_id, code, desc))

            self.table.setSortingEnabled(False)
            self.table.clearContents()

            if not rows:
                self.table.setRowCount(1)
                self.table.setItem(0, 0, QTableWidgetItem("-"))
                self.table.setItem(0, 1, QTableWidgetItem("-"))
                self.table.setItem(0, 2, QTableWidgetItem("-"))
                self.table.setItem(0, 3, QTableWidgetItem(
                    "Sin causas activas (TREN DISPUESTO)"
                ))
            else:
                self.table.setRowCount(len(rows))
                for r, (coach_label, ip, code, desc) in enumerate(rows):

                    # ---- Columna 0: Coach label (orden numérico) ----
                    label_str = str(coach_label)
                    label_item = QTableWidgetItem()
                    label_item.setData(Qt.DisplayRole, label_str)  # lo que se ve

                    # coge el número del inicio: "10 (C4301)" -> 10
                    m = re.match(r"\s*(\d+)", label_str)
                    label_num = int(m.group(1)) if m else 10**9
                    label_item.setData(Qt.EditRole, label_num)     # lo que usa Qt para ordenar

                    self.table.setItem(r, 0, label_item)

                    # ---- Resto de columnas igual ----
                    self.table.setItem(r, 1, QTableWidgetItem(str(ip)))
                    self.table.setItem(r, 2, QTableWidgetItem(str(code)))
                    self.table.setItem(r, 3, QTableWidgetItem(str(desc)))

            self.table.setSortingEnabled(True)

            header = self.table.horizontalHeader()
            sort_col = header.sortIndicatorSection()
            sort_order = header.sortIndicatorOrder()

            if not self._default_sort_applied:
                self.table.sortItems(0, Qt.AscendingOrder)  # IP ascendente
                self._default_sort_applied = True
            else:
                self.table.sortItems(sort_col, sort_order)  # mantener lo que eligió el usuario

    def _export_table_to_excel(self):
        
        table = self.table

        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar tabla como...",
            "",
            "Archivos Excel (*.xlsx);;Todos los archivos (*)",
            options=options
        )
        if not file_path:
            return
        if not file_path.lower().endswith(".xlsx"):
            file_path += ".xlsx"
        
        workbook = xlsxwriter.Workbook(file_path)
        worksheet = workbook.add_worksheet("Diagnóstico TSC")

        header_format = workbook.add_format({
            "bold": True,
            "bg_color": "#2F5496",
            "font_color": "#FFFFFF",
            "border": 1,
            "align": "center",
            "valign": "vcenter"
        })
        cell_format = workbook.add_format({
            "border": 1,
            "text_wrap": True,
            "valign": "top",
            "align": "left"
        })

        col_count = table.columnCount()
        headers = []
        
        for c in range(col_count):
            hitem = table.horizontalHeaderItem(c)
            headers.append(hitem.text() if hitem else f"Columna {c}")

        worksheet.write_row(0, 0, headers, header_format)

        rows_for_width = [headers]
        row_count = table.rowCount()

        for r in range(row_count):
            row_values = []
            for c in range(col_count):
                item = table.item(r, c)
                row_values.append(item.text() if item else "")
            worksheet.write_row(r + 1, 0, row_values, cell_format)
            rows_for_width.append(row_values)

        if row_count > 0:
            worksheet.autofilter(0, 0, row_count, col_count - 1)
        worksheet.freeze_panes(1, 0)

        max_widths = [0] * col_count
        for rv in rows_for_width:
            for c, val in enumerate(rv):
                max_widths[c] = max(max_widths[c], len(str(val)))
        for c, max_ch in enumerate(max_widths):
            width = min(max(10, max_ch + 4), 80)
            worksheet.set_column(c, c, width)

        workbook.close()

        try:
            QMessageBox.information(self, "Exportado", f"Tabla exportada correctamente a:\n{file_path}")
        except Exception:
            pass

class Door_Diag_Window(DiagnosticWindow):

    def __init__(self, *, project, endpoint_ids, project_coach_types,
                 fixed_w: int, fixed_h: int, valid_ips: list, parent=None):

        self.project = project
        self.endpoint_ids = endpoint_ids
        self.project_coach_types = project_coach_types
        self.valid_ips = list(valid_ips)

        super().__init__(
            title="Problemas activos en las puertas",
            fixed_w=fixed_w,
            fixed_h=fixed_h,
            parent=parent
        )

        # ---- TCMS Vars / diccionarios ----
        self._tcms = TCMS_vars()

        menubar = self.menuBar()
        export_menu = menubar.addMenu("Exportar")

        self.export_diag_action = QAction("Exportar tabla a Excel (.xlsx)", self)
        export_menu.addAction(self.export_diag_action)
        self.export_diag_action.triggered.connect(self._export_table_to_excel)

        # Dict BCU: keys SOLO desde el '.' en adelante
        self._dcu_diag_dict = getattr(self._tcms, "DCU_DIAGNOSIS_DICT", {})

        # ---- UI tabla ----
        self.table = QTableWidget(80, 5, self)
        self.table.setHorizontalHeaderLabels([
            "Coche",
            "IP",
            "Puerta",
            "Código de error",
            "Descripción"
        ])

        central = QWidget()
        self.layout = QVBoxLayout(central)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(8)

        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table.setShowGrid(True)
        self.table.setWordWrap(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setFocusPolicy(Qt.StrongFocus)

        vh = self.table.verticalHeader()
        vh.setDefaultSectionSize(26)

        hh = self.table.horizontalHeader()
        hh.setStretchLastSection(False)
        hh.setDefaultAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        hh.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(4, QHeaderView.Stretch)

        self.layout.addWidget(self.table)
        self.setCentralWidget(central)

        self._default_sort_applied = False

        self.right_side_telegrams = ['49A', '19B']
        self.left_side_telegrams = ['49C', '19D']

        self._last_door_diag = {}

    def _on_toggled(self, checked):
        
        if checked:
            self.show()
            self.raise_()
            self.activateWindow()
            screen = QApplication.primaryScreen()
            max_width = screen.availableGeometry().width()  
            max_height = screen.availableGeometry().height() 
            self.move(int((max_width - min(self.size().width(), max_width))/2),int((max_height - min(self.size().height(), max_height))/2))

        else:
            self.close()

    def set_snapshot(self, snapshot: dict):

            doors_diag = snapshot.get("doors_diag", {})

            if hasattr(self, "_last_door_diag") and self._last_door_diag == doors_diag:
                return

            self._last_door_diag = doors_diag
            
            header = self.table.horizontalHeader()
            sort_col = header.sortIndicatorSection()
            sort_order = header.sortIndicatorOrder()

            coach_types_by_endpoint = {}
            for endpoint_id, data in doors_diag.items():
                vals = (data or {}).get("values") or {}
                coach_types_by_endpoint[endpoint_id] = vals.get(
                    "oVCUCH_TRDP_DS_A000.COM_Vehicle_Type"
                )

            if self.project == "DB" and len(self.endpoint_ids) >= 2:
                last = self.endpoint_ids[-1]
                prev = self.endpoint_ids[-2]
                coach_types_by_endpoint[last] = coach_types_by_endpoint.get(prev)

            # Índice del coche PMR (tipo 5) para cruzar D/I en coches posteriores
            pmr_idx = None
            for i, eid in enumerate(self.endpoint_ids):
                ct = coach_types_by_endpoint.get(eid)
                try:
                    if ct is not None and int(float(ct)) == 5:
                        pmr_idx = i
                        break
                except (ValueError, TypeError):
                    pass

            rows = []

            for endpoint_id, data in snapshot.get("doors_diag", {}).items():
                diag_vals = (data or {}).get("values") or {}

                try:
                    coach_idx = self.endpoint_ids.index(endpoint_id) + 1
                    coach_col  = coach_idx - 1
                except ValueError:
                    coach_idx = "?"
                    coach_col = -1

                # IP del coche
                try:
                    ip = str(self.valid_ips[coach_col]) if coach_col >= 0 else endpoint_id
                except IndexError:
                    ip = endpoint_id

                coach_type = coach_types_by_endpoint.get(endpoint_id)
                coach_type_str = ""
                try:
                    if coach_type is not None:
                        coach_type_str = self.project_coach_types.get(
                            int(float(coach_type)), str(coach_type)
                        )
                except Exception:
                    coach_type_str = str(coach_type) if coach_type is not None else ""

                coach_label = f"{coach_idx}"
                if coach_type_str:
                    coach_label += f" ({coach_type_str})"

                # ¿Coche posterior al PMR? → D/I visual están cruzados respecto al físico
                post_pmr = pmr_idx is not None and coach_col > pmr_idx

                for var_full, value in diag_vals.items():
                    if any(telegram in var_full for telegram in self.right_side_telegrams):
                        door_side = "Izquierda" if post_pmr else "Derecha"
                    elif any(telegram in var_full for telegram in self.left_side_telegrams):
                        door_side = "Derecha" if post_pmr else "Izquierda"
                    else:
                        door_side = "Desconocida"
                    var_short = var_full.split(".")[-1]

                    if value != "1" and value != "0":
                        continue

                    if value == "1":
                        dcu_hit = self._dcu_diag_dict.get(var_short)
                        if dcu_hit:
                            code = dcu_hit.get("Error Code", var_short)
                            desc = dcu_hit.get("Description", "Descripción no disponible")
                        else:
                            code = var_short
                            desc = "Descripción no disponible"

                        rows.append((coach_label, ip, door_side, code, desc))

            self.table.setSortingEnabled(False)
            self.table.clearContents()

            if not rows:
                self.table.setRowCount(1)
                self.table.setItem(0, 0, QTableWidgetItem("-"))
                self.table.setItem(0, 1, QTableWidgetItem("-"))
                self.table.setItem(0, 2, QTableWidgetItem("-"))
                self.table.setItem(0, 3, QTableWidgetItem("-"))
                self.table.setItem(0, 4, QTableWidgetItem(
                    "Sin causas activas (TREN DISPUESTO)"
                ))
            else:
                self.table.setRowCount(len(rows))
                for r, (coach_label, ip, side, code, desc) in enumerate(rows):

                    # ---- Columna 0: Coach label (orden numérico) ----
                    label_str = str(coach_label)
                    label_item = QTableWidgetItem()
                    label_item.setData(Qt.DisplayRole, label_str)  # lo que se ve

                    # coge el número del inicio: "10 (C4301)" -> 10
                    m = re.match(r"\s*(\d+)", label_str)
                    label_num = int(m.group(1)) if m else 10**9
                    label_item.setData(Qt.EditRole, label_num)     # lo que usa Qt para ordenar

                    self.table.setItem(r, 0, label_item)

                    # ---- Resto de columnas igual ----
                    self.table.setItem(r, 1, QTableWidgetItem(str(ip)))
                    self.table.setItem(r, 2, QTableWidgetItem(str(side)))
                    self.table.setItem(r, 3, QTableWidgetItem(str(code)))
                    self.table.setItem(r, 4, QTableWidgetItem(str(desc)))

            self.table.setSortingEnabled(True)

            header = self.table.horizontalHeader()
            sort_col = header.sortIndicatorSection()
            sort_order = header.sortIndicatorOrder()

            if not self._default_sort_applied:
                self.table.sortItems(0, Qt.AscendingOrder)  # IP ascendente
                self._default_sort_applied = True
            else:
                self.table.sortItems(sort_col, sort_order)  # mantener lo que eligió el usuario

    def _export_table_to_excel(self):
        
        table = self.table

        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar tabla como...",
            "",
            "Archivos Excel (*.xlsx);;Todos los archivos (*)",
            options=options
        )
        if not file_path:
            return
        if not file_path.lower().endswith(".xlsx"):
            file_path += ".xlsx"
        
        workbook = xlsxwriter.Workbook(file_path)
        worksheet = workbook.add_worksheet("Diagnóstico puertas")

        header_format = workbook.add_format({
            "bold": True,
            "bg_color": "#2F5496",
            "font_color": "#FFFFFF",
            "border": 1,
            "align": "center",
            "valign": "vcenter"
        })
        cell_format = workbook.add_format({
            "border": 1,
            "text_wrap": True,
            "valign": "top",
            "align": "left"
        })

        col_count = table.columnCount()
        headers = []
        
        for c in range(col_count):
            hitem = table.horizontalHeaderItem(c)
            headers.append(hitem.text() if hitem else f"Columna {c}")

        worksheet.write_row(0, 0, headers, header_format)

        rows_for_width = [headers]
        row_count = table.rowCount()

        for r in range(row_count):
            row_values = []
            for c in range(col_count):
                item = table.item(r, c)
                row_values.append(item.text() if item else "")
            worksheet.write_row(r + 1, 0, row_values, cell_format)
            rows_for_width.append(row_values)

        if row_count > 0:
            worksheet.autofilter(0, 0, row_count, col_count - 1)
        worksheet.freeze_panes(1, 0)

        max_widths = [0] * col_count
        for rv in rows_for_width:
            for c, val in enumerate(rv):
                max_widths[c] = max(max_widths[c], len(str(val)))
        for c, max_ch in enumerate(max_widths):
            width = min(max(10, max_ch + 4), 80)
            worksheet.set_column(c, c, width)

        workbook.close()

        try:
            QMessageBox.information(self, "Exportado", f"Tabla exportada correctamente a:\n{file_path}")
        except Exception:
            pass

class ResetFailuresWorker(QObject):
    log = Signal(str)
    finished = Signal(bool)

    def __init__(self, endpoint_ids, endpoint_clients, wait_time: float = 1.0, project: str = "DB"):
        super().__init__()
        self.endpoint_ids = list(endpoint_ids)
        self.endpoint_clients = endpoint_clients
        
        if project == "DB":
            self.endpoint_ids = self.endpoint_ids[:-1]

        self.wait_time = float(wait_time)
        self._cancel = False
        self.project = project

        # VARS_LIST (según tu requisito)
        self.MAINT_VARS = [
            "VCUCH_MVB1_DS_64.MaintenaceMode",
            "VCUCH_MVB2_DS_64.MaintenaceMode",
        ]
        self.RELEASE_VARS = [
            "VCUCH_MVB2_DS_64.ReleaseFailureRunInstabCH",
            "VCUCH_MVB1_DS_64.ReleaseFailureRunInstabCH",
        ]

        self._steps = [
            ("MaintenaceMode = 1", {v: 1 for v in self.MAINT_VARS}),
            ("ReleaseFailure = 1", {v: 1 for v in self.RELEASE_VARS}),
            ("ReleaseFailure = 0", {v: 0 for v in self.RELEASE_VARS}),  # “reles a 0”
            ("MaintenaceMode = 0", {v: 0 for v in self.MAINT_VARS}),
        ]
        self._step_idx = 0

        self._we_done = False

    def cancel(self):
        self._cancel = True

    def start(self):
        # arranca el paso 0
        self._run_next_step()

    def _run_next_step(self):

        if not self._we_done:
            self.log.emit("Habilitando escritura por SSH: isacmd -we (EP a EP) ...")
            for eid in self.endpoint_ids:
                if self._cancel:
                    self.log.emit("Cancelado.")
                    self.finished.emit(False)
                    return
                client = self.endpoint_clients.get(eid)
                if client is None:
                    self.log.emit(f"  {eid}: sin cliente")
                    continue
                out = client.ssh_cmd("isacmd -we", wait_time = 5)
                self.log.emit(f"  {eid}: isacmd -we -> {out}")
            
            self._we_done = True
            self.log.emit("Escritura habilitada. Empezando secuencia de reset…")

        if self._cancel:
            self.log.emit("Cancelado.")
            self.finished.emit(False)
            return

        if self._step_idx >= len(self._steps):
            self.log.emit("✅ Reseteo terminado.")
            self.finished.emit(True)
            return

        name, var_map = self._steps[self._step_idx]
        self.log.emit(f"\nPaso {self._step_idx+1}/4: {name}")

        # Escritura (secuencial, simple) sobre TODOS los endpoints
        for eid in self.endpoint_ids:
            if self._cancel:
                self.log.emit("Cancelado.")
                self.finished.emit(False)
                return

            client = self.endpoint_clients.get(eid)
            if client is None:
                self.log.emit(f"  {eid}: sin cliente")
                continue

            ok, ts, st = client.write_vars(var_map, lock=True, wait_time=self.wait_time)
            total = len(st) if st else 0
            oks = sum(1 for v in (st or {}).values() if v is True)
            self.log.emit(f"  {eid}: {'OK' if ok else 'FAIL'} (vars OK {oks}/{total}) ts={ts}")

        # Programar el siguiente paso tras 2 segundos (sin bloquear)
        self._step_idx += 1
        if self._step_idx < len(self._steps):
            self.log.emit("Esperando 2 segundos…")
            QTimer.singleShot(2000, self._run_next_step)
        else:
            # último paso, finalizar
            self._run_next_step()

class BurninLog:
    """
    Almacena el historial de eventos del Burn-In Test y el estado final de cada puerta.

    Formato JSON de exportación:
    {
      "events": [
        {"ts": "2026-03-11 14:32:01", "eid": "EP3", "side": "R",
         "type": "NOK", "cycles_door": 512, "cycles_step": 48,
         "code": "bFoo", "desc": "Descripción del error"},
        ...
      ],
      "completed": [
        {"eid": "EP3", "side": "R", "result": "NOK"},
        ...
      ]
    }
    """

    # Tipos de evento
    START  = "START"
    STOP   = "STOP"
    OK     = "OK"
    NOK    = "NOK"
    ERROR  = "ERROR"
    ALL_OK = "ALL_OK"   # todas las puertas iniciadas han finalizado con OK

    def __init__(self):
        self.events    = []   # list[dict]
        self.completed = {}   # {(eid, side): "OK" | "NOK"}

    def add_event(self, eid: str, side: str, event_type: str,
                  cycles_door: int = 0, cycles_step: int = 0,
                  code: str = "", desc: str = ""):
        self.events.append({
            "ts":          datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "eid":         eid,
            "side":        side,
            "type":        event_type,
            "cycles_door": cycles_door,
            "cycles_step": cycles_step,
            "code":        code,
            "desc":        desc,
        })
        if event_type in (self.OK, self.NOK):
            self.completed[(eid, side)] = event_type

    def merge_from(self, other: "BurninLog"):
        """Fusiona otro log sobre éste (eventos + completed)."""
        self.events.extend(other.events)
        self.completed.update(other.completed)

    def to_dict(self) -> dict:
        return {
            "events": self.events,
            "completed": [
                {"eid": eid, "side": side, "result": result}
                for (eid, side), result in self.completed.items()
            ],
        }

    @classmethod
    def from_dict(cls, d: dict) -> "BurninLog":
        log = cls()
        log.events = d.get("events", [])
        for entry in d.get("completed", []):
            log.completed[(entry["eid"], entry["side"])] = entry["result"]
        return log

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    @classmethod
    def from_json(cls, s: str) -> "BurninLog":
        return cls.from_dict(json.loads(s))

class BurninEventDetector:
    """
    Detecta transiciones de estado en el snapshot de puertas y emite eventos al BurninLog.

    Detecta (0→1 edge-triggered):
      - BurninActive  R/L (índices 24/25): START
      - LastBurninOK  R/L (índices 28/29): OK
      - LastBurninNOK R/L (índices 26/27): NOK
      - Nuevos códigos de error en doors_diag que aparecen mientras hay baseline activo

    Para calcular ciclos relativos consulta DoorsGenerator._burnin_baseline.
    """

    IDX_ACTIVE_R, IDX_ACTIVE_L = 24, 25
    IDX_NOK_R,    IDX_NOK_L    = 26, 27
    IDX_OK_R,     IDX_OK_L     = 28, 29
    IDX_DOOR_R,   IDX_DOOR_L   = 80, 81
    IDX_STEP_R,   IDX_STEP_L   = 82, 83

    def __init__(self, doors_generator, burnin_log: BurninLog, dcu_diag_dict: dict,
                 endpoint_ids: list):
        """
        doors_generator : instancia de DoorsGenerator (para baseline y doors_vars)
        burnin_log      : BurninLog donde se registran los eventos
        dcu_diag_dict   : dict de diagnóstico DCU para resolver códigos de error
        endpoint_ids    : lista de endpoints a testear (sin el agregado DB)
        """
        self._gen          = doors_generator
        self._log          = burnin_log
        self._dcu          = dcu_diag_dict
        # Estado anterior por (eid, side): dict con claves "active","ok","nok"
        self._prev         = {}
        # Códigos de error ya registrados por (eid, side): set de var_short
        self._prev_errors  = {}
        # Puertas que han recibido al menos un evento START en esta sesión
        self._started_doors = set()
        # Conjunto completo de puertas del tren — referencia para ALL_OK
        self._all_doors = frozenset(
            (eid, side) for eid in endpoint_ids for side in ("R", "L")
        )
        # Evita emitir ALL_OK más de una vez por sesión
        self._all_ok_emitted = False

    def _cycles(self, eid: str, side: str, vals: dict, dv: list) -> tuple:
        """Devuelve (cycles_door, cycles_step) relativos al baseline, o (0,0) si no hay."""
        entry = self._gen._burnin_baseline.get((eid, side))
        if entry is None:
            return (0, 0)
        door_base, step_base = entry
        idx_d = self.IDX_DOOR_R if side == "R" else self.IDX_DOOR_L
        idx_s = self.IDX_STEP_R if side == "R" else self.IDX_STEP_L
        try:
            cd = max(0, int(vals.get(dv[idx_d], "0")) - door_base)
        except (ValueError, TypeError, IndexError):
            cd = 0
        try:
            cs = max(0, int(vals.get(dv[idx_s], "0")) - step_base)
        except (ValueError, TypeError, IndexError):
            cs = 0
        return (cd, cs)

    def _val(self, vals: dict, dv: list, idx: int) -> int:
        try:
            return int(vals.get(dv[idx], "0"))
        except (ValueError, TypeError, IndexError):
            return 0

    def process(self, snapshot: dict):
        """Llamar en cada set_snapshot. Detecta transiciones y registra eventos."""
        coaches = snapshot.get("doors", snapshot)
        dv      = self._gen.doors_vars

        for eid, coach_data in coaches.items():
            vals = (coach_data or {}).get("values", {})
            for side in ("R", "L"):
                idx_active = self.IDX_ACTIVE_R if side == "R" else self.IDX_ACTIVE_L
                idx_ok     = self.IDX_OK_R     if side == "R" else self.IDX_OK_L
                idx_nok    = self.IDX_NOK_R    if side == "R" else self.IDX_NOK_L

                active = self._val(vals, dv, idx_active)
                ok     = self._val(vals, dv, idx_ok)
                nok    = self._val(vals, dv, idx_nok)

                prev   = self._prev.get((eid, side), {"active": 0, "ok": 0, "nok": 0})

                cd, cs = self._cycles(eid, side, vals, dv)

                # START
                if active == 1 and prev["active"] == 0:
                    self._log.add_event(eid, side, BurninLog.START, cd, cs)
                    self._started_doors.add((eid, side))

                has_baseline = self._gen._burnin_baseline.get((eid, side)) is not None

                # OK (solo si hubo baseline, es decir el burnin fue nuestro)
                if ok == 1 and prev["ok"] == 0 and has_baseline:
                    self._log.add_event(eid, side, BurninLog.OK, cd, cs)
                    # ALL_OK: todas las puertas del tren han finalizado con OK
                    if (not self._all_ok_emitted
                            and self._all_doors.issubset(self._log.completed)
                            and all(self._log.completed[k] == BurninLog.OK
                                    for k in self._all_doors)):
                        self._log.add_event("", "", BurninLog.ALL_OK)
                        self._all_ok_emitted = True

                # NOK
                if nok == 1 and prev["nok"] == 0 and has_baseline:
                    self._log.add_event(eid, side, BurninLog.NOK, cd, cs)

                self._prev[(eid, side)] = {"active": active, "ok": ok, "nok": nok}

        # Errores nuevos en doors_diag (solo si hay baseline activo en alguna puerta)
        if not self._gen._burnin_baseline:
            return

        right_tels = {'49A', '19B'}
        left_tels  = {'49C', '19D'}

        for eid, data in snapshot.get("doors_diag", {}).items():
            diag_vals = (data or {}).get("values") or {}
            for var_full, value in diag_vals.items():
                if value != "1":
                    continue
                if any(t in var_full for t in right_tels):
                    side = "R"
                elif any(t in var_full for t in left_tels):
                    side = "L"
                else:
                    continue

                # Solo si hay baseline activo para esta puerta
                if self._gen._burnin_baseline.get((eid, side)) is None:
                    continue

                var_short = var_full.split(".")[-1]
                key = (eid, side)
                known = self._prev_errors.setdefault(key, set())
                if var_short in known:
                    continue

                known.add(var_short)
                dcu_hit = self._dcu.get(var_short, {})
                code = dcu_hit.get("Error Code", var_short)
                desc = dcu_hit.get("Description", "Descripción no disponible")
                vals = (snapshot.get("doors", {}).get(eid) or {}).get("values", {})
                dv   = self._gen.doors_vars
                cd, cs = self._cycles(eid, side, vals, dv)
                self._log.add_event(eid, side, BurninLog.ERROR, cd, cs, code, desc)

    def reset_errors(self):
        """Limpia el registro de errores ya notificados (llamar al parar el burnin)."""
        self._prev_errors.clear()

class BurninWorker(QObject):
    """
    Gestiona la secuencia de escritura del Burnin Test de forma asíncrona.

    Secuencia:
      1. start_maint()  → bSW_MaintMode = 1 en puertas seleccionadas
      2. start_burnin() → bSW_BurnInOn  = 1 (llamar cuando BurninReady = 1)
      3. stop()         → BurnInOn = 0, MaintMode = 0

    La supervisión del estado (BurninReady, BurninActive…) se realiza desde el
    hilo principal a través de BurninPanel.refresh_from_snapshot().
    """

    log      = Signal(str)
    finished = Signal(bool)

    _ENDPOINT_R = "VCUCH_CAN_DS_21A"   # endpoint CAN para puerta derecha
    _ENDPOINT_L = "VCUCH_CAN_DS_21C"   # endpoint CAN para puerta izquierda

    def __init__(self, selected_doors: list, endpoint_clients: dict, wait_time: float = 1.0, n3_par: int = 1000):
        """
        Args:
            selected_doors:   lista de (endpoint_id, side) donde side ∈ {'R','L'}
            endpoint_clients: dict {endpoint_id: client}
            wait_time:        tiempo de espera por escritura (s)
            n3_par:           número de ciclos a escribir en N3_par antes de BurnInOn
        """
        super().__init__()
        self.selected_doors   = list(selected_doors) 
        self.endpoint_clients = endpoint_clients
        self.wait_time        = float(wait_time)
        self.n3_par           = int(n3_par)
        self._cancel          = False

    def cancel(self):
        self._cancel = True

    def _can_ep(self, side: str) -> str:
        return self._ENDPOINT_R if side == "R" else self._ENDPOINT_L

    def _write(self, endpoint_id: str, var_name: str, value: int):
        client = self.endpoint_clients.get(endpoint_id)
        if client is None:
            self.log.emit(f"  {endpoint_id}: sin cliente")
            return
        ok, ts, st = client.write_vars({var_name: value}, lock=True, wait_time=self.wait_time)
        self.log.emit(f"  {endpoint_id} {var_name}={value}: {'OK' if ok else 'FAIL'} ts={ts}")

    def start_maint(self):
        """Paso 1: activa MaintMode en las puertas seleccionadas."""
        self.log.emit("Activando MaintMode…")
        for eid, side in self.selected_doors:
            if self._cancel:
                self.log.emit("Cancelado.")
                return
            self._write(eid, f"{self._can_ep(side)}.bSW_MaintMode", 1)
        self.log.emit("MaintMode activado. Esperando Burn-In Ready…")

    def start_burnin(self):
        """Paso 2: escribe N3_par y activa BurnInOn en las puertas seleccionadas."""
        self.log.emit(f"Escribiendo N3_par={self.n3_par}…")
        for eid, side in self.selected_doors:
            if self._cancel:
                self.log.emit("Cancelado.")
                self.finished.emit(False)
                return
            self._write(eid, f"{self._can_ep(side)}.N3_par", self.n3_par)
        self.log.emit("Activando BurnInOn…")
        for eid, side in self.selected_doors:
            if self._cancel:
                self.log.emit("Cancelado.")
                self.finished.emit(False)
                return
            self._write(eid, f"{self._can_ep(side)}.bSW_BurnInOn", 1)
        self.log.emit("Burn-In Test iniciado.")
        self.finished.emit(True)

    def stop(self):
        """Detiene el Burnin Test y desactiva MaintMode."""
        self.log.emit("Deteniendo Burn-In Test…")
        for eid, side in self.selected_doors:
            self._write(eid, f"{self._can_ep(side)}.bSW_BurnInOn",  0)
            self._write(eid, f"{self._can_ep(side)}.bSW_MaintMode", 0)
        self.log.emit("Burn-In Test detenido.")
        self.finished.emit(False)

class BurninPanel(QWidget):
    """
    Panel colapsable para lanzar el Burnin Test sobre las puertas seleccionadas.

    Layout (expandido):
      ┌─[▼ BURN-IN TEST]────────────────────────────────┐
      │  Selección de puertas:                          │
      │  [✓ D] [✓ I]  Coche 1   [✓ D] [✓ I]  Coche 2 … │
      │  [Sel. todo D]  [Sel. todo I]  [Sel. todo]      │
      │  ─────────────────────────────────────────────  │
      │  Prereqs  MaintMode: ●  BurninReady: ●          │
      │           BurninActive: ●  LastOK: ●  LastNOK:● │
      │  ─────────────────────────────────────────────  │
      │  [  Iniciar Maint  ]   [  Iniciar Burnin  ]      │
      │  [        Detener        ]                       │
      │  Log: ─────────────────────────────────────────  │
      │  …                                               │
      └────────────────────────────────────────────────┘
    """

    toggled         = Signal()         # expandir/colapsar → DOORWindow redimensiona
    maint_changed   = Signal(object)   # frozenset de (eid, side) en MaintMode activo
    burnin_baseline = Signal(object)   # dict {(eid, side): (door_base, step_base)}

    def __init__(self, endpoint_ids: list, endpoint_clients: dict, parent=None):
        """
        Args:
            endpoint_ids:     lista ordenada de IDs de endpoint (coches, sin agregado)
            endpoint_clients: dict {endpoint_id: client}
        """
        super().__init__(parent)
        self.endpoint_ids     = list(endpoint_ids)
        self.endpoint_clients = endpoint_clients
        self._expanded        = False
        self._worker          = None
        self._thread          = None
        self._maint_active    = set()   # (eid, side) con MaintMode activo
        self._pmr_index       = None    # índice del coche PMR; coches posteriores tienen R/L cruzados
        self._last_snapshot   = {}
        self._last_doors_vars = []
        self._completed_doors = {}      # {(eid, side): "OK"|"NOK"} cargado desde log

        self._build_ui()
        self._collapse()

    # ------------------------------------------------------------------
    # Construcción de la UI
    # ------------------------------------------------------------------

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(2)

        # ---- Cabecera (botón colapsar/expandir) ----
        self._btn_header = QPushButton("▶  BURN-IN TEST")
        self._btn_header.setCheckable(True)
        self._btn_header.setStyleSheet(
            "QPushButton { text-align:left; padding:4px 8px; }"
        )
        self._btn_header.clicked.connect(self._toggle)
        main_layout.addWidget(self._btn_header)

        # ---- Contenido colapsable ----
        self._content = QWidget()
        content_layout = QVBoxLayout(self._content)
        content_layout.setContentsMargins(6, 4, 6, 4)
        content_layout.setSpacing(4)

        # -- Selección de puertas --
        content_layout.addWidget(QLabel("Selección de puertas:"))
        grid_widget = QWidget()
        self._grid_layout = QGridLayout(grid_widget)
        self._grid_layout.setSpacing(3)
        self._checkboxes = {}   # {(endpoint_id, side): QCheckBox}
        for col, eid in enumerate(self.endpoint_ids):
            coach_num = col + 1
            cb_r = QCheckBox("D")
            cb_l = QCheckBox("I")
            cb_r.setChecked(True)
            cb_l.setChecked(True)
            lbl = QLabel(f"C{coach_num}")
            lbl.setAlignment(Qt.AlignCenter)
            self._grid_layout.addWidget(lbl,  0, col * 3, 1, 2, Qt.AlignCenter)
            self._grid_layout.addWidget(cb_r, 1, col * 3,       Qt.AlignCenter)
            self._grid_layout.addWidget(cb_l, 1, col * 3 + 1,   Qt.AlignCenter)
            self._checkboxes[(eid, "R")] = cb_r
            self._checkboxes[(eid, "L")] = cb_l
            # Separador vertical entre coches (excepto el último)
            if col < len(self.endpoint_ids) - 1:
                sep = QFrame()
                sep.setFrameShape(QFrame.VLine)
                sep.setFrameShadow(QFrame.Sunken)
                self._grid_layout.addWidget(sep, 0, col * 3 + 2, 2, 1)
        content_layout.addWidget(grid_widget)

        # -- Botones de selección rápida --
        sel_layout = QHBoxLayout()
        btn_all_r = QPushButton("Todas D")
        btn_all_l = QPushButton("Todas I")
        btn_all   = QPushButton("Todas")
        btn_none  = QPushButton("Ninguna")
        self._btn_pending = QPushButton("Pendientes")
        self._btn_pending.setVisible(False)
        btn_all_r.clicked.connect(lambda: self._quick_select("R", True))
        btn_all_l.clicked.connect(lambda: self._quick_select("L", True))
        btn_all.clicked.connect(lambda: self._quick_select(None, True))
        btn_none.clicked.connect(lambda: self._quick_select(None, False))
        self._btn_pending.clicked.connect(self._select_pending)
        for b in (btn_all_r, btn_all_l, btn_all, btn_none, self._btn_pending):
            b.setFixedHeight(22)
            sel_layout.addWidget(b)
        content_layout.addLayout(sel_layout)

        content_layout.addWidget(self._make_separator())

        # # -- Estado: MaintMode (local) y BurninReady (desde snapshot) --
        # prereq_layout = QHBoxLayout()
        # self._dot_maint = QLabel("●")
        # self._dot_ready = QLabel("●")
        # self._dot_maint.setStyleSheet("color: #AAAAAA; font-size: 14px;")
        # self._dot_ready.setStyleSheet("color: #AAAAAA; font-size: 14px;")
        # prereq_layout.addWidget(QLabel("MaintMode:"))
        # prereq_layout.addWidget(self._dot_maint)
        # prereq_layout.addSpacing(16)
        # prereq_layout.addWidget(QLabel("Ready:"))
        # prereq_layout.addWidget(self._dot_ready)
        # prereq_layout.addStretch()
        # content_layout.addLayout(prereq_layout)

        # content_layout.addWidget(self._make_separator())

        # -- Selector de ciclos N3 --
        cycles_layout = QHBoxLayout()
        cycles_layout.addWidget(QLabel("Ciclos N3:"))
        self._slider_cycles = QSlider(Qt.Horizontal)
        self._slider_cycles.setRange(500, 2000)
        self._slider_cycles.setValue(500)
        self._slider_cycles.setSingleStep(100)
        self._slider_cycles.setPageStep(100)
        self._slider_cycles.setTickInterval(500)
        self._slider_cycles.setTickPosition(QSlider.TicksBelow)
        self._lbl_cycles = QLabel("500")
        self._lbl_cycles.setFixedWidth(36)
        self._slider_cycles.valueChanged.connect(lambda v: self._lbl_cycles.setText(str(v)))
        cycles_layout.addWidget(self._slider_cycles)
        cycles_layout.addWidget(self._lbl_cycles)
        content_layout.addLayout(cycles_layout)

        content_layout.addWidget(self._make_separator())

        # -- Botones de control --
        ctrl_layout = QHBoxLayout()
        self._btn_maint  = QPushButton("1. Iniciar Maint")
        self._btn_burnin = QPushButton("2. Iniciar Burn-In")
        self._btn_stop   = QPushButton("Detener")
        self._btn_maint.clicked.connect(self._on_start_maint)
        self._btn_burnin.clicked.connect(self._on_start_burnin)
        self._btn_stop.clicked.connect(self._on_stop)
        self._btn_burnin.setEnabled(False)
        self._btn_stop.setEnabled(False)
        for b in (self._btn_maint, self._btn_burnin, self._btn_stop):
            ctrl_layout.addWidget(b)
        content_layout.addLayout(ctrl_layout)

        # -- Log --
        content_layout.addWidget(QLabel("Log:"))
        self._log = QPlainTextEdit()
        self._log.setReadOnly(True)
        self._log.setFixedHeight(80)
        self._log.setStyleSheet("font-size: 10px; font-family: monospace;")
        content_layout.addWidget(self._log)

        main_layout.addWidget(self._content)

    def _make_separator(self):
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        return sep

    # ------------------------------------------------------------------
    # Colapsar / expandir
    # ------------------------------------------------------------------

    def _toggle(self, checked):
        if checked:
            self._expand()
        else:
            self._collapse()
        self.toggled.emit()

    def _collapse(self):
        self._expanded = False
        self._content.hide()
        self._btn_header.setText("▶  BURN-IN TEST")
        self._btn_header.setChecked(False)

    def _expand(self):
        self._expanded = True
        self._content.show()
        self._btn_header.setText("▼  BURN-IN TEST")
        self._btn_header.setChecked(True)

    # ------------------------------------------------------------------
    # Selección rápida
    # ------------------------------------------------------------------

    def _quick_select(self, side, checked: bool):
        for (_, s), cb in self._checkboxes.items():
            if side is None or s == side:
                cb.setChecked(checked)

    def set_pmr_index(self, idx):
        """Índice del coche PMR en endpoint_ids. Coches posteriores tienen R/L físicos cruzados."""
        self._pmr_index = idx

    def set_completed_doors(self, completed: dict):
        """
        Recibe {(eid, side): "OK"|"NOK"} del log cargado.
        Colorea en verde los checkboxes de puertas ya completadas y
        muestra el botón "Pendientes".
        """
        self._completed_doors = dict(completed)
        for (eid, side), result in self._completed_doors.items():
            cb = self._checkboxes.get((eid, side))
            if cb is None:
                continue
            color = "#4CAF50" if result == "OK" else "#E57373"
            cb.setStyleSheet(
                f"QCheckBox {{ background-color: {color}; border-radius: 3px; padding: 1px 3px; }}"
            )
        self._btn_pending.setVisible(bool(self._completed_doors))

    def _select_pending(self):
        """Marca puertas sin resultado OK (pendientes o NOK que hay que repetir)."""
        for (eid, side), cb in self._checkboxes.items():
            cb.setChecked(self._completed_doors.get((eid, side)) != "OK")

    def _selected_doors(self) -> list:
        """Devuelve lista de (endpoint_id, physical_side) para los checkboxes marcados.
        Para coches después del PMR el lado visual D/I se invierte respecto al físico R/L."""
        result = []
        for col, eid in enumerate(self.endpoint_ids):
            for visual_side in ("R", "L"):
                cb = self._checkboxes.get((eid, visual_side))
                if cb and cb.isChecked():
                    if self._pmr_index is not None and col > self._pmr_index:
                        physical_side = "L" if visual_side == "R" else "R"
                    else:
                        physical_side = visual_side
                    result.append((eid, physical_side))
        return result

    # ------------------------------------------------------------------
    # Actualización de estado desde snapshot
    # ------------------------------------------------------------------

    def refresh_from_snapshot(self, snapshot: dict, doors_vars: list):
        """
        Actualiza los indicadores de prerrequisitos con los datos del último snapshot.
        BurninReady R/L → índices 30/31.
        BurninActive R/L → índices 24/25 (solo para bloquear botón si ya activo).
        """
        self._last_snapshot   = snapshot
        self._last_doors_vars = doors_vars
        coaches = snapshot.get("doors", snapshot)   # acepta tanto {doors:{}} como dict plano

        def _any_active(idx_r, idx_l):
            for eid, side in self._selected_doors():
                coach = coaches.get(eid, {})
                vals  = coach.get("values", {})
                idx   = idx_r if side == "R" else idx_l
                try:
                    if int(vals.get(doors_vars[idx], "0")) == 1:
                        return True
                except (ValueError, TypeError):
                    pass
            return False

        ready  = _any_active(30, 31)
        active = _any_active(24, 25)

        # self._dot_ready.setStyleSheet(
        #     "color: #FFA040; font-size: 14px;" if ready else "color: #AAAAAA; font-size: 14px;"
        # )

        # Habilitar "Iniciar Burnin" solo si BurninReady activo y burnin no en marcha
        self._btn_burnin.setEnabled(ready and not active)

    # ------------------------------------------------------------------
    # Acciones de los botones
    # ------------------------------------------------------------------

    def _on_start_maint(self):
        selected = self._selected_doors()
        if not selected:
            self._log.appendPlainText("⚠ No hay puertas seleccionadas.")
            return
        self._maint_active = set(selected)
        # self._dot_maint.setStyleSheet("color: #00BB00; font-size: 14px;")
        self.maint_changed.emit(frozenset(self._maint_active))
        self._start_worker_action("maint", selected)
        self._btn_maint.setEnabled(False)
        self._btn_stop.setEnabled(True)

    def _on_start_burnin(self):
        selected = self._selected_doors()
        if not selected:
            self._log.appendPlainText("⚠ No hay puertas seleccionadas.")
            return
        # Avisar de puertas seleccionadas sin BurninReady
        # BurninReady R/L → índices 30/31
        IDX_READY_R, IDX_READY_L = 30, 31
        coaches  = self._last_snapshot.get("doors", self._last_snapshot)
        dv       = self._last_doors_vars
        for eid, side in selected:
            vals = coaches.get(eid, {}).get("values", {})
            idx_ready = IDX_READY_R if side == "R" else IDX_READY_L
            try:
                ready = int(vals.get(dv[idx_ready], "0")) if dv else 0
            except (ValueError, TypeError, IndexError):
                ready = 0
            if not ready:
                self._log.appendPlainText(f"⚠ {eid} lado {side}: Burn-In Ready no activo, se lanza igualmente.")

        # Capturar baseline de ciclos en el momento de iniciar el burnin
        # cycle_count_door → índice 80/81 (R/L); cycle_count_step → índice 82/83 (R/L)
        IDX_DOOR_R, IDX_DOOR_L = 80, 81
        IDX_STEP_R, IDX_STEP_L = 82, 83
        baseline = {}
        for eid, side in selected:
            vals = coaches.get(eid, {}).get("values", {})
            idx_door = IDX_DOOR_R if side == "R" else IDX_DOOR_L
            idx_step = IDX_STEP_R if side == "R" else IDX_STEP_L
            try:
                door_base = int(vals.get(dv[idx_door], "0")) if dv else 0
            except (ValueError, TypeError, IndexError):
                door_base = 0
            try:
                step_base = int(vals.get(dv[idx_step], "0")) if dv else 0
            except (ValueError, TypeError, IndexError):
                step_base = 0
            baseline[(eid, side)] = (door_base, step_base)
        self.burnin_baseline.emit(baseline)
        n3_par = self._slider_cycles.value()
        self._start_worker_action("burnin", selected, n3_par=n3_par)
        self._btn_burnin.setEnabled(False)

    def _on_stop(self):
        selected = self._selected_doors()
        self._maint_active = set()
        # self._dot_maint.setStyleSheet("color: #AAAAAA; font-size: 14px;")
        self.maint_changed.emit(frozenset())
        self.burnin_baseline.emit({(eid, side): None for eid, side in selected})
        self._start_worker_action("stop", selected)
        self._btn_maint.setEnabled(True)
        self._btn_burnin.setEnabled(False)
        self._btn_stop.setEnabled(False)

    def _start_worker_action(self, action: str, selected: list, n3_par: int = 500):
        # Detener worker anterior si sigue activo
        if self._thread and self._thread.isRunning():
            if self._worker:
                self._worker.cancel()
            self._thread.quit()
            self._thread.wait(2000)

        self._worker = BurninWorker(selected, self.endpoint_clients, n3_par=n3_par)
        self._thread = QThread()
        self._worker.moveToThread(self._thread)
        self._worker.log.connect(self._log.appendPlainText) #Conecta la señal de log del worker al método appendPlainText del widget de log para mostrar los mensajes en la interfaz
        self._worker.finished.connect(self._on_worker_finished)
        method_name = {"maint": "start_maint", "burnin": "start_burnin"}.get(action, action) # Mapea el nombre de la acción al método correspondiente del worker
        self._thread.started.connect(getattr(self._worker, method_name))
        self._thread.start()

    def _on_worker_finished(self, success: bool):
        if self._thread:
            self._thread.quit()

class DOORWindow(DiagnosticWindow):

    def __init__(self, *, project, endpoint_ids, doors_vars, project_coach_types,
            fixed_w: int, fixed_h: int, valid_ips: list, endpoint_clients=None, parent=None): #El asterisco indica que los argumentos siguientes deben ser pasados como palabras clave, es decir (project = x, endpoint_ids = y, etc) y no como argumentos posicionales (x, y, etc)

        super().__init__(title="Lazo de puertas", fixed_w=fixed_w, fixed_h=fixed_h, parent=parent)
        self._endpoint_clients = endpoint_clients or {}


        self.valid_ips = valid_ips
        self.project = project

        menubar = self.menuBar()
        export_menu = menubar.addMenu("Importar / Exportar")

        self.export_Doors_loop_action = QAction("Guardar como PNG...", self)
        export_menu.addAction(self.export_Doors_loop_action)
        export_menu.addSeparator()
        self._action_export_log = QAction("Exportar log Burn-In (.json)...", self)
        self._action_import_log = QAction("Importar log Burn-In (.json)...", self)
        export_menu.addAction(self._action_export_log)
        export_menu.addAction(self._action_import_log)
        self._action_export_log.triggered.connect(self._export_burnin_log)
        self._action_import_log.triggered.connect(self._import_burnin_log)
        export_menu.addSeparator()
        self._action_export_report = QAction("Exportar informe Burn-In (PDF)...", self)
        export_menu.addAction(self._action_export_report)
        self._action_export_report.triggered.connect(self._export_burnin_report)

        self.Door_diag_window = Door_Diag_Window(project=self.project, endpoint_ids=endpoint_ids, project_coach_types=project_coach_types,fixed_w=800, fixed_h=400, valid_ips=self.valid_ips)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(False)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.doors = DoorsGenerator(
            project=project,
            endpoint_ids=endpoint_ids,
            doors_vars=doors_vars,
            project_coach_types=project_coach_types
        )

        self.export_Doors_loop_action.triggered.connect(self.doors.save_as_png)
        self.scroll.setWidget(self.doors)

        # ---- Log y detector de eventos Burn-In ----
        _dcu_diag_dict       = getattr(TCMS_vars(), "DCU_DIAGNOSIS_DICT", {})
        _burnin_ids          = list(self.doors.endpoint_ids[:-1])  # sin el agregado DB
        self._burnin_log     = BurninLog()
        self._event_detector = BurninEventDetector(
            self.doors, self._burnin_log, _dcu_diag_dict, _burnin_ids
        )

        self.btn_diag = QPushButton("Mostrar errores de puertas")
        self.btn_diag.setCheckable(True)
        self.btn_diag.toggled.connect(self.Door_diag_window._on_toggled)
        self.Door_diag_window.closed.connect(lambda: self.btn_diag.setChecked(False))

        # ---- Panel de leyenda ----
        self.legend = DoorLegendSvg()

        # ---- Panel de burnin ----
        _burnin_ids = self.doors.endpoint_ids[:-1]  # coches sin el agregado DB
        self.burnin_panel = BurninPanel(
            endpoint_ids=_burnin_ids,
            endpoint_clients=self._endpoint_clients,
        )

        # ---- Layout: puertas (scroll + burnin + botón) a la izquierda, leyenda a la derecha ----
        content_widget = QWidget()
        lay = QVBoxLayout(content_widget)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(8)
        lay.addWidget(self.scroll)
        lay.addWidget(self.burnin_panel)
        lay.addWidget(self.btn_diag)

        central = QWidget()
        outer = QHBoxLayout(central)
        outer.setContentsMargins(6, 6, 6, 6)
        outer.setSpacing(4)
        outer.addWidget(content_widget)
        outer.addWidget(self.legend, 0, Qt.AlignTop)

        self.setCentralWidget(central)

        screen = QApplication.primaryScreen()
        self.max_width  = screen.availableGeometry().width()  - 10
        self.max_height = screen.availableGeometry().height() - 50

        self.burnin_panel.toggled.connect(self._resize_window)
        self.burnin_panel.maint_changed.connect(self.doors.set_maint_doors)
        self.burnin_panel.burnin_baseline.connect(self.doors.set_burnin_baseline)

    def _on_legend_toggled(self):
        """Llamado por DoorLegendSvg al expandir/colapsar para reajustar la ventana."""
        self._resize_window()

    def _resize_window(self):
        doors_w = min(self.doors.scaled_doors_width, self.max_width)
        doors_h = self.doors.scaled_doors_height
        burnin_h = self.burnin_panel.sizeHint().height()
        btn_h = self.btn_diag.sizeHint().height()
        content_h = doors_h + burnin_h + btn_h + 75
        legend_h = self.legend.height() + 28
        total_h = min(max(content_h, legend_h), self.max_height)
        total_w = min(doors_w + self.legend.panel_width() + 16, self.max_width)
        self.setFixedSize(total_w, total_h)

    def _load_dev_snapshot(self):
        """
        Genera un snapshot sintético para probar el lazo de puertas sin conexión al tren.
        Activo cuando DEV_MODE = True (definido al inicio del fichero).

        Composición del tren simulado:
          - Coche 1     → tipo 11 (end coach)
          - Coches intermedios → tipo aleatorio entre los normales
          - Último coche → tipo 2  (cab car, DB)

        Cada puerta (lado R y lado L) recibe un estado aleatorio e independiente
        entre los 7 colores representados en la leyenda.
        """

        # ---- Referencias a los metadatos del widget de puertas ----
        vars_list      = self.doors.doors_vars   # lista ordenada de variables TRDP
        coach_type_var = self.doors.coach_type_var  # última var: tipo de coche
        endpoint_ids   = self.doors.endpoint_ids[:-1]  # IPs de coches (sin el agregado DB)

        # ---- Tipos de coche disponibles para los intermedios ----
        # 3,4,6,8,9,10 → normal  |  5 → PMR  |  7 → familiar
        MIDDLE_TYPES = ["3", "4", "5", "6", "7", "8", "9", "10"]

        # ---- Tabla de estados de puerta ----
        # Cada entrada: (índice_R_en_vars_list, índice_L_en_vars_list, valor_a_escribir)
        # None representa el estado magenta (ninguna variable activa → todo "0")
        #
        # Prioridad interna de create_door_svg (de mayor a menor):
        #   gris > rojo > amarillo > naranja > negro > azul > magenta
        DOOR_STATES = [
            (2,  3,  "1"),    # negro    – cerrada y bloqueada   (closed_n_locked)
            (10, 11, "1"),    # azul     – abierta               (door_open)
            None,             # magenta  – estado indeterminado  (ninguna var activa)
            (18, 19, "1"),    # naranja  – fuera de servicio     (door_oos)
            (34, 35, "1"),    # rojo     – fallo tipo A          (code_a)
            (32, 33, "1"),    # amarillo – fallo tipo B          (code_b)
            (84, 85, "241"),  # gris     – tasa de fallos > 240  (failure_rate)
            # Fondos de burnin (sólo uno activo a la vez)
            (24, 25, "1"),    # celeste  – burnin en marcha      (burn_in_active)
            (28, 29, "1"),    # verde    – burnin finalizado OK   (last_burn_in_ok)
            (26, 27, "1"),    # rojo claro – burnin finalizado NOK (last_burn_in_nok)
        ]

        def _apply_state(v: dict, state, side: int):
            """
            Escribe en el dict 'v' la variable correspondiente al estado dado.
              side = 0 → lado R (19A)
              side = 1 → lado L (19C)
            Si state es None (magenta) no hace nada; el dict ya parte todo a "0".
            """
            if state is None:
                return
            r_idx, l_idx, val = state
            v[vars_list[r_idx if side == 0 else l_idx]] = val

        # Modos que se randomisan de forma independiente al estado de puerta.
        # Cada tupla: (índice_R, índice_L) en doors_data.
        MODE_VARS = [
            (70, 71),   # safe_st
            (72, 73),   # tbo_mode
            (74, 75),   # obb_mode
            (68, 69),   # uic_lat_mode
            (62, 63),   # uic_15
            (64, 65),   # uic_14
        ]

        def _random_values(coach_type: str) -> dict:
            """
            Construye el dict de valores para un coche:
            - Todas las variables a "0" como base.
            - Tipo de coche asignado.
            - Estado aleatorio e independiente para cada lado de puerta.
            - Modos (Safe, TB0, OBB, LAT, UIC14, UIC15) aleatorios por lado.
            """
            v = {var: "0" for var in vars_list}
            v[coach_type_var] = coach_type
            _apply_state(v, random.choice(DOOR_STATES), 0)  # lado R
            _apply_state(v, random.choice(DOOR_STATES), 1)  # lado L
            # Randomizar modos de forma independiente para cada lado
            for r_idx, l_idx in MODE_VARS:
                v[vars_list[r_idx]] = random.choice(["0", "1"])
                v[vars_list[l_idx]] = random.choice(["0", "1"])
            return v

        # ---- Construcción del snapshot ----
        coaches: dict = {}
        for i, eid in enumerate(endpoint_ids):
            if i == 0:
                coach_type = "11"                       # primero: end coach
            elif i == len(endpoint_ids) - 1:
                coach_type = "2"                        # último:  cab car (DB)
            else:
                coach_type = random.choice(MIDDLE_TYPES)  # intermedios: aleatorio

            coaches[eid] = {"online": True, "values": _random_values(coach_type)}

        # ---- Carga y refresco de la ventana ----
        self.doors.set_snapshot({"doors": coaches})
        self.burnin_panel.set_pmr_index(getattr(self.doors, "pmr_pos", None))
        self.burnin_panel.refresh_from_snapshot({"doors": coaches}, self.doors.doors_vars)
        self.legend.set_height(self.doors.scaled_doors_height)
        self._resize_window()

    def set_snapshot(self, snapshot: dict):
        if DEV_MODE:
            return
        self.doors.set_snapshot(snapshot)
        self.burnin_panel.set_pmr_index(getattr(self.doors, "pmr_pos", None))
        self.burnin_panel.refresh_from_snapshot(snapshot, self.doors.doors_vars)
        self.legend.set_height(self.doors.scaled_doors_height)
        self._resize_window()
        self._event_detector.process(snapshot)

    # ------------------------------------------------------------------
    # Log Burn-In: exportar / importar
    # ------------------------------------------------------------------

    def _generate_dev_burnin_log(self):
        """Genera un BurninLog con datos aleatorios para pruebas en DEV_MODE."""
        log = BurninLog()
        endpoint_ids = self.doors.endpoint_ids[:-1]  # sin el agregado DB
        base_dt = datetime.datetime(2026, 3, 11, 8, 0, 0)
        delta = datetime.timedelta(minutes=0)
        for eid in endpoint_ids:
            for side in ("R", "L"):
                door_cycles = random.randint(0, 200)
                step_cycles = random.randint(0, door_cycles)
                log.events.append({
                    "ts": (base_dt + delta).strftime("%Y-%m-%d %H:%M:%S"),
                    "eid": eid, "side": side, "type": BurninLog.START,
                    "cycles_door": 0, "cycles_step": 0, "code": "", "desc": "",
                })
                delta += datetime.timedelta(minutes=random.randint(1, 5))
                # Posibilidad de uno o dos errores durante el test
                for _ in range(random.randint(0, 2)):
                    err_cycles = random.randint(1, door_cycles) if door_cycles else 0
                    log.events.append({
                        "ts": (base_dt + delta).strftime("%Y-%m-%d %H:%M:%S"),
                        "eid": eid, "side": side, "type": BurninLog.ERROR,
                        "cycles_door": err_cycles, "cycles_step": err_cycles // 2,
                        "code": random.choice(["bFaultA", "bFaultB", "bOvertemp"]),
                        "desc": "Error simulado (DEV_MODE)",
                    })
                    delta += datetime.timedelta(minutes=random.randint(1, 10))
                # Resultado final: OK 70%, NOK 30%
                result = BurninLog.OK if random.random() < 0.7 else BurninLog.NOK
                log.events.append({
                    "ts": (base_dt + delta).strftime("%Y-%m-%d %H:%M:%S"),
                    "eid": eid, "side": side, "type": result,
                    "cycles_door": door_cycles, "cycles_step": step_cycles,
                    "code": "", "desc": "",
                })
                log.completed[(eid, side)] = result
                delta += datetime.timedelta(minutes=random.randint(5, 30))

        # Si todas las puertas terminaron OK → añadir evento ALL_OK
        if log.completed and all(v == BurninLog.OK for v in log.completed.values()):
            log.events.append({
                "ts": (base_dt + delta).strftime("%Y-%m-%d %H:%M:%S"),
                "eid": "", "side": "", "type": BurninLog.ALL_OK,
                "cycles_door": 0, "cycles_step": 0, "code": "", "desc": "",
            })

        return log

    def _export_burnin_log(self):
        if not self._burnin_log.events:
            if DEV_MODE:
                self._burnin_log = self._generate_dev_burnin_log()
            else:
                QMessageBox.information(self, "Log Burn-In", "No hay eventos registrados aún.")
                return
        path, _ = QFileDialog.getSaveFileName(
            self, "Exportar log Burn-In", "",
            "JSON (*.json);;Todos los archivos (*)"
        )
        if not path:
            return
        if not path.lower().endswith(".json"):
            path += ".json"
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self._burnin_log.to_json())
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar:\n{e}")

    def _import_burnin_log(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Importar log Burn-In", "",
            "JSON (*.json);;Todos los archivos (*)"
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                loaded = BurninLog.from_json(f.read())
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar:\n{e}")
            return
        self._burnin_log.merge_from(loaded)
        self.burnin_panel.set_completed_doors(self._burnin_log.completed)

    # ------------------------------------------------------------------
    # PDF report helpers
    # ------------------------------------------------------------------

    # Tipos de coche sin puertas (se excluyen del informe PDF)
    _NO_DOOR_TYPES = {"C4340", "C4322"}

    def _build_burnin_report_tree(self) -> list:
        """
        Devuelve una lista de dicts, uno por coche con puertas (sin el agregado DB
        y sin coches de tipo C4340/C4322 que no tienen puertas):
          {
            "coach_num": int,      # posición 1-based en la composición
            "label": str,          # "COCHE 1 — C4302P" etc.
            "eid": str,
            "type_label": str,     # "C4302P" etc.
            "sides": {
              "R": {"label": str, "result": str|None, "events": list[dict]},
              "L": {"label": str, "result": str|None, "events": list[dict]},
            }
          }
        El swap D/I se aplica a los coches posteriores al PMR.
        """
        pmr_pos        = getattr(self.doors, "pmr_pos", None)
        eid_list       = list(self.doors.endpoint_ids[:-1])   # sin agregado DB
        coach_types    = self.doors.project_coach_types        # {int: str}
        coach_type_var = getattr(self.doors, "coach_type_var", None)
        snapshot       = getattr(self.doors, "snapshot", {}) or {}
        doors_dict     = snapshot.get("doors", snapshot)

        tree = []
        for idx, eid in enumerate(eid_list):
            coach_num = idx + 1
            post_pmr  = pmr_pos is not None and idx > pmr_pos

            # Obtener tipo de coche desde el snapshot en vivo
            type_label = ""
            if coach_type_var:
                vals   = doors_dict.get(eid, {}).get("values", {})
                ct_raw = vals.get(coach_type_var, "")
                try:
                    if ct_raw:
                        type_label = coach_types.get(int(float(ct_raw)), "")
                except (ValueError, TypeError):
                    pass

            # Excluir coches sin puertas
            if type_label in self._NO_DOOR_TYPES:
                continue

            coach_label = f"COCHE {coach_num}"
            if type_label:
                coach_label += f" — {type_label}"

            # Etiquetas de lado (swap post-PMR)
            label_r = "IZQUIERDA" if post_pmr else "DERECHA"
            label_l = "DERECHA"   if post_pmr else "IZQUIERDA"

            sides = {}
            for side, slabel in (("R", label_r), ("L", label_l)):
                evs    = [e for e in self._burnin_log.events if e.get("eid") == eid and e.get("side") == side]
                result = self._burnin_log.completed.get((eid, side))
                sides[side] = {"label": slabel, "result": result, "events": evs}

            tree.append({
                "coach_num":  coach_num,
                "label":      coach_label,
                "eid":        eid,
                "type_label": type_label,
                "is_pmr":     (pmr_pos is not None and idx == pmr_pos),
                "sides":      sides,
            })
        return tree

    def _generate_burnin_pdf_html(self, tree: list, composition: str = "") -> str:
        """Genera el HTML completo para WeasyPrint."""

        # ---- logo ----
        _base    = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        abs_logo = os.path.join(_base, "Talgo_logo.png")
        logo_url = f"file:///{abs_logo.replace(os.sep, '/')}"

        # ---- helpers de color ----
        def result_badge(result):
            if result == BurninLog.OK:  return '<span style="color:#2E7D32;font-weight:bold;">OK</span>'
            if result == BurninLog.NOK: return '<span style="color:#B71C1C;font-weight:bold;">NOK</span>'
            return '<span style="color:#757575;">Pendiente</span>'

        def event_row_color(ev_type):
            if ev_type == BurninLog.OK:    return "#C8E6C9"
            if ev_type == BurninLog.NOK:   return "#FFCDD2"
            if ev_type == BurninLog.ERROR: return "#FFF9C4"
            if ev_type == BurninLog.START: return "#E3F2FD"
            if ev_type == BurninLog.STOP:  return "#F3E5F5"
            if ev_type == BurninLog.ALL_OK:return "#A5D6A7"
            return "#FFFFFF"

        # ---- cabecera (running header) ----
        header_html = f"""
        <div id="header">
          <div class="header-box">
            <div class="logo-area">
              <img src="{logo_url}" alt="Logo">
            </div>
            <div class="middle-area">
              <div class="registro-encabezado">REGISTRO DE PRUEBAS / PRÜFPROTOKOLL</div>
              <div class="registro-inferior">
                <div class="registro-codigo">RPTF-2216-20</div>
                <div class="registro-sublabel">INFORME BURN-IN TEST</div>
                {f'<div class="registro-composicion">F073 COMPOSICIÓN {composition}</div>' if composition else ''}
              </div>
            </div>
            <div class="pagina-area">
              <div class="pagina-label">PÁGINA</div>
              <div class="pagina-numero">
                <span class="page-number"></span> de <span class="page-count"></span>
              </div>
            </div>
          </div>
        </div>"""

        footer_html = """
        <div id="footer">
          <div class="footer-text">
            Este documento y su contenido son propiedad de Patentes Talgo S.L.U. o sus filiales.
            Contiene información confidencial y privada. La reproducción, distribución, utilización
            o comunicación de este documento o parte de él, sin autorización expresa, está estrictamente
            prohibida. Aquellos que contravengan esta disposición se considerarán responsables del pago
            de los daños causados. / <i> Dieses Dokument und sein Inhalt sind
            Eigentum von Patentes Talgo S.L.U. oder seiner Tochtergesellschaften. Dieses Dokument enthält vertrauliche und private Informationen. Die
            vollständige oder teilweise Vervielfältigung, Verbreitung, Verwendung oder Weitergabe dieses Dokuments ohne Genehmigung von Talgo ist
            strengstens verboten. Personen, die gegen diese Bestimmung verstoßen, werden für die entstandenen Schäden haftbar gemacht. </i>
          </div>
        </div>"""

        # ---- índice con líderes punteados y número de página ----
        toc_items = ""
        toc_num = 1
        for entry in tree:
            anchor_coach = f"coach-{entry['coach_num']}"
            toc_items += (
                f'<div class="toc-entry toc-h2">'
                f'<a href="#{anchor_coach}">{toc_num}. {entry["label"]}</a>'
                f'</div>'
            )
            sub = 1
            for side_key in ("R", "L"):
                sd = entry["sides"][side_key]
                anchor_side = f"coach-{entry['coach_num']}-{side_key}"
                toc_items += (
                    f'<div class="toc-entry toc-h3">'
                    f'<a href="#{anchor_side}">{toc_num}.{sub} Puerta {sd["label"]}</a>'
                    f'</div>'
                )
                sub += 1
            toc_num += 1

        toc_html = f"""
        <section>
          <h2 class="toc-title">Índice</h2>
          {toc_items}
        </section>"""

        # ---- contenido: todos los coches sin salto de página entre ellos ----
        content_html = '<section class="content-section">'
        toc_num = 1
        for entry in tree:
            anchor_coach = f"coach-{entry['coach_num']}"
            content_html += f'<h2 id="{anchor_coach}">{toc_num}. {entry["label"]}</h2>'

            sub = 1
            for side_key in ("R", "L"):
                sd = entry["sides"][side_key]
                anchor_side = f"coach-{entry['coach_num']}-{side_key}"
                coach_id_label = entry["type_label"] if entry["type_label"] else entry["eid"]
                content_html += (
                    f'<h3 id="{anchor_side}">'
                    f'{toc_num}.{sub} PUERTA {sd["label"]} ({coach_id_label}) — {result_badge(sd["result"])}'
                    f'</h3>'
                )

                is_pmr = entry["is_pmr"]
                if not sd["events"]:
                    content_html += '<p class="no-events">Sin eventos registrados.</p>'
                else:
                    header_step = '<th>Ciclos Peldaño</th>' if is_pmr else ''
                    content_html += (
                        '<table class="events-table">'
                        '<tr>'
                        '<th>Fecha / Hora</th><th>Tipo</th>'
                        '<th>Ciclos Pta.</th>'
                        + header_step +
                        '<th>Código</th><th>Descripción</th>'
                        '</tr>'
                    )
                    for ev in sd["events"]:
                        bg       = event_row_color(ev.get("type", ""))
                        cycles_d = ev.get("cycles_door", "")
                        cycles_s = ev.get("cycles_step", "")
                        step_td  = f'<td style="text-align:center;">{cycles_s if cycles_s else "—"}</td>' if is_pmr else ''
                        content_html += (
                            f'<tr style="background-color:{bg};">'
                            f'<td>{ev.get("ts","")}</td>'
                            f'<td style="text-align:center;font-weight:bold;">{ev.get("type","")}</td>'
                            f'<td style="text-align:center;">{cycles_d if cycles_d else "—"}</td>'
                            + step_td +
                            f'<td>{ev.get("code","")}</td>'
                            f'<td>{ev.get("desc","")}</td>'
                            f'</tr>'
                        )
                    content_html += "</table>"
                sub += 1
            toc_num += 1
        content_html += "</section>"

        # ---- CSS ----
        css = """
        @page {
            size: A4;
            margin-top: 4.2cm;
            margin-left: 2cm;
            margin-right: 2cm;
            margin-bottom: 3cm;
            @top-center { content: element(header); margin-top: 1cm; }
            @bottom-center { content: element(footer); }
        }
        body { font-family: Calibri, Arial, sans-serif; font-size: 11px; }

        /* ---- Cabecera corriente ---- */
        #header {
            position: running(header);
            height: 2.2cm;
            width: 17cm;
        }
        .header-box {
            margin-top: 0;
            width: 17cm;
            height: 2.2cm;
            display: table;
            border: 1px solid black;
            box-sizing: border-box;
            table-layout: fixed;
        }
        .logo-area {
            display: table-cell;
            width: 3.5cm;
            vertical-align: middle;
            text-align: center;
            border-right: 1px solid black;
        }
        .logo-area img { max-width: 90%; padding: 2px 4px; }
        .middle-area {
            display: table-cell;
            vertical-align: top;
            border-right: 1px solid black;
        }
        .registro-encabezado {
            display: block;
            font-weight: bold;
            font-size: 16px;
            text-align: center;
            padding: 5px 0;
            border-bottom: 1px solid black;
            box-sizing: border-box;
        }
        .registro-inferior {
            display: block;
            text-align: center;
            padding-top: 5px;
        }
        .registro-codigo      { font-weight: bold; font-size: 16px; margin-bottom: 2px; }
        .registro-sublabel    { font-size: 11px; font-weight: normal; }
        .registro-composicion { font-size: 10px; font-weight: bold; margin-top: 2px; }
        .pagina-area {
            display: table-cell;
            width: 2.5cm;
            vertical-align: middle;
            text-align: center;
            font-size: 9px;
        }
        .pagina-label { margin-bottom: 3px; }
        .page-number::after { content: counter(page); }
        .page-count::after  { content: counter(pages); }

        /* ---- Pie de página ---- */
        #footer {
            position: running(footer);
            width: 17cm;
            margin: 0 auto;
        }
        .footer-text {
            font-size: 9px;
            text-align: justify;
            color: rgba(0,0,0,0.4);
            line-height: 1.5;
        }

        /* ---- Índice ---- */
        .toc-title { font-size: 15px; margin-bottom: 0.3cm; border-bottom: 2px solid #455A64; padding-bottom: 3px; }
        .toc-entry { font-size: 11px; margin: 2px 0; }
        .toc-h2 { font-weight: bold; margin-top: 6px; }
        .toc-h3 { margin-left: 1.5cm; font-weight: normal; }
        .toc-entry a {
            text-decoration: none;
            color: black;
            display: block;
        }
        .toc-h2 a::after {
            content: leader('.') target-counter(attr(href url), page);
            font-weight: normal;
        }
        .toc-h3 a::after {
            content: leader('.') target-counter(attr(href url), page);
        }

        /* ---- Salto índice → contenido ---- */
        .content-section { page-break-before: always; }

        /* ---- Cabeceras de sección ---- */
        h2 { font-size: 13px; margin-top: 0.4cm; margin-bottom: 0.15cm;
             border-bottom: 2px solid #455A64; padding-bottom: 3px; }
        h3 { font-size: 11px; margin-top: 0.25cm; margin-bottom: 0.1cm; color: #37474F; }

        /* ---- Tabla de eventos ---- */
        .events-table {
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 0.25cm;
            font-size: 10px;
        }
        .events-table th {
            background-color: #455A64; color: white;
            border: 1px solid #37474F; padding: 3px 5px;
            text-align: left;
        }
        .events-table td {
            border: 1px solid #CFD8DC; padding: 2px 5px;
            vertical-align: top;
        }
        .no-events { font-style: italic; color: #757575; margin: 3px 0 0.2cm 0; }
        """

        html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>{css}</style>
</head>
<body>
  {header_html}
  {footer_html}
  {toc_html}
  {content_html}
</body>
</html>"""
        return html

    def _ask_composition_number(self) -> str | None:
        """
        Muestra un diálogo para introducir el número de composición F073 (01-23).
        Devuelve la cadena "01"–"23" o None si se cancela.
        """
        dlg = QDialog(self)
        dlg.setWindowTitle("Número de composición")
        dlg.setFixedSize(320, 130)

        lay = QVBoxLayout(dlg)
        lay.addWidget(QLabel("Introduzca el número de composición:"))

        row = QHBoxLayout()
        row.addWidget(QLabel("F073 Composición"))

        spin = QSpinBox()
        spin.setRange(1, 23)
        spin.setValue(1)
        spin.setFixedWidth(60)
        # Mostrar siempre con dos dígitos en el visor
        spin.setDisplayIntegerBase(10)

        # Actualizar el cuadro de texto del spinbox al formato "01"-"23"
        def _update_display(val):
            spin.lineEdit().setText(f"{val:02d}")
        spin.valueChanged.connect(_update_display)
        _update_display(spin.value())

        row.addWidget(spin)
        row.addStretch()
        lay.addLayout(row)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setText("Aceptar")
        buttons.button(QDialogButtonBox.Cancel).setText("Cancelar")
        buttons.accepted.connect(dlg.accept)
        buttons.rejected.connect(dlg.reject)
        lay.addWidget(buttons)

        if dlg.exec() == QDialog.Accepted:
            return f"{spin.value():02d}"
        return None

    def _export_burnin_report(self):
        if not self._burnin_log.events:
            if DEV_MODE:
                self._burnin_log = self._generate_dev_burnin_log()
            else:
                QMessageBox.information(self, "Informe Burn-In", "No hay eventos registrados aún.")
                return

        composition = self._ask_composition_number()
        if composition is None:
            return

        path, _ = QFileDialog.getSaveFileName(
            self, "Exportar informe Burn-In", f"informe_burnin_F073-{composition}.pdf",
            "PDF (*.pdf);;Todos los archivos (*)"
        )
        if not path:
            return

        try:
            tree = self._build_burnin_report_tree()
            html = self._generate_burnin_pdf_html(tree, composition)
            base_url = os.path.dirname(os.path.abspath(__file__)) + "/"
            WPHtml(string=html, base_url=base_url).write_pdf(path)
            QMessageBox.information(self, "Informe exportado", f"PDF guardado en:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Error al generar PDF", str(e))

class MainWindow(QMainWindow):
    
    scan_progress_signal = Signal(int)
    ping_result_signal = Signal(int, int, bool, int, int, int, int, int, int)  # row, col, ok, rtt, lost, sent, received, min, max
    diagnosis_config_signal = Signal(dict)

    def __init__(self):
        super().__init__()

        self.ip_data = {
            "DSB_EST": ['10.0.8.64', '10.0.8.128', '10.0.8.192', '10.0.13.128', '10.0.9.64',
                   '10.0.9.128', '10.0.9.192', '10.0.10.0', '10.0.10.64', '10.0.10.128',
                   '10.0.10.192', '10.0.11.0', '10.0.11.64', '10.0.11.128', '10.0.11.192',
                   '10.0.20.10', '10.0.20.74', '10.0.20.138', '10.0.20.202', '10.0.21.10', '10.0.21.74'],
            "DB": ['10.0.16.74', '10.0.16.138', '10.0.16.202', '10.0.17.10', '10.0.17.74',
                   '10.0.17.138', '10.0.17.202', '10.0.18.10', '10.0.18.74', '10.0.18.138',
                   '10.0.18.202', '10.0.19.10', '10.0.19.74', '10.0.19.138', '10.0.19.202',
                   '10.0.20.10', '10.0.20.74', '10.0.20.138', '10.0.20.202', '10.0.21.10', '10.0.21.74'],
            "DSB": ['10.0.8.64', '10.0.8.128', '10.0.8.192', '10.0.13.128', '10.0.9.64',
                    '10.0.9.128', '10.0.9.192', '10.0.10.0', '10.0.10.64', '10.0.10.128',
                    '10.0.10.192', '10.0.11.0', '10.0.11.64', '10.0.11.128', '10.0.11.192',
                    '10.0.12.0', '10.0.12.64', '10.0.12.128', '10.0.12.192', '10.0.13.0', '10.0.13.64'],
            "LOK": ['10.0.16.67'],
            "DB_VCUCH_CABCAR": ['10.0.16.96', '10.0.16.160', '10.0.16.224', '10.0.17.32', '10.0.17.96',
                           '10.0.17.160', '10.0.17.224', '10.0.18.32', '10.0.18.96', '10.0.18.160',
                             '10.0.18.224', '10.0.19.32', '10.0.19.96', '10.0.19.160', '10.0.19.224',
                               '10.0.20.32', '10.0.20.96', '10.0.20.160', '10.0.20.224', '10.0.21.32', '10.0.21.96'],
            "DB_VCUPH_CABCAR": ['10.0.16.64', '10.0.16.128', '10.0.16.192', '10.0.17.0', '10.0.17.64',
                                    '10.0.17.128', '10.0.17.192', '10.0.18.0', '10.0.18.64', '10.0.18.128',
                                    '10.0.18.192', '10.0.19.0', '10.0.19.64', '10.0.19.128', '10.0.19.192',
                                    '10.0.20.0', '10.0.20.64', '10.0.20.128', '10.0.20.192', '10.0.21.0', '10.0.21.64']
        }

        self.TCMS_vars = TCMS_vars()

        self.diag_dict = {
            "COACH_TYPE": self.TCMS_vars.COACH_TYPE,
            "TSC_DB": self.TCMS_vars.TSC_COACH_VARS_DB,
            "TSC_DSB": self.TCMS_vars.TSC_COACH_VARS_DSB,
            "TSC_CC_DB": self.TCMS_vars.TSC_CC_VARS_DB,
            "TSC_DIAG_VARS": self.TCMS_vars.TSC_DIAG_VARS,
            "BCU_DIAG_VARS": self.TCMS_vars.BCU_DIAGNOSIS,
            "BCU_DIAG_VARS_CC": self.TCMS_vars.BCU_DIAGNOSIS_CC,
            "DOORS": self.TCMS_vars.DOORS_LOOP_VARS,
            "DOORS_DIAG_VARS": self.TCMS_vars.DCU_DIAGNOSIS
        }

        self.diag_enabled = {
            "TSC": False,
            "DOORS": False
        }
                    
        self.default_width = 800
        self.default_height = 434

        self.tsc_window = None
        self.doors_window = None
        
        self.setWindowTitle("Herramienta de diagnóstico PES")
        self.setFixedSize(self.default_width, self.default_height)

        self.current_dir = os.path.dirname(__file__)
        self.background_pixmap = QPixmap(self.resource_path("Talgo_logo.png"))
        self.project = None
        self.connection_monitor = None
        
        self.menu_bar = self.menuBar()
        self.create_menus()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.progress_layout = QVBoxLayout()
        self.progress_layout.setAlignment(Qt.AlignCenter)

        self.progress_title = QLabel()
        self.progress_title.setAlignment(Qt.AlignCenter)
        self.progress_title.setVisible(False)
        self.progress_layout.addWidget(self.progress_title)

        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setVisible(False)
        self.progress_layout.addWidget(self.progress_bar)

        self.detected_label = QLabel()
        self.detected_label.setAlignment(Qt.AlignCenter)
        self.detected_label.setVisible(False)
        self.progress_layout.addWidget(self.detected_label)

        self.layout.addLayout(self.progress_layout)

        self.scan_progress_signal.connect(self.coach_scan_progress)
        self.ping_result_signal.connect(self.update_ping_cell)

        self.config = self.load_config()

        # screens = QApplication.screens()
        # for s in screens:
        #     print(f"Screen {s.name()}: {s.size().width()}x{s.size().height()}")

    def resource_path(self, relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(__file__))
        return os.path.join(base_path, relative_path)

    def closeEvent(self, event):
        app.quit()
        event.accept()

    def paintEvent(self, event):
        
        painter = QPainter(self)
        painter.setOpacity(0.05)
        painter.drawPixmap(0, 22, self.width(), self.height(), self.background_pixmap)
        super().paintEvent(event)
 
    def create_menus(self):
        
        ######### MENÚ ARCHIVO ##########
        
        file_menu = self.menu_bar.addMenu("Archivo")
        
        open_action = QAction("Abrir archivo", self)
        open_action.setEnabled(False)
        
        load_data_action = QAction("Cargar excel variables", self)
        load_data_action.setEnabled(False)

        preferences_action = QAction("Preferencias", self)
        preferences_action.setEnabled(True)
        preferences_action.triggered.connect(self.open_preferences)
        
        close_app_action = QAction("Cerrar", self)
        close_app_action.setEnabled(False)
        
        file_menu.addActions([open_action, load_data_action, preferences_action, close_app_action])
        
        ######### MENÚ CONECTAR ##########
        
        connect_menu = self.menu_bar.addMenu("Conectar")

        F073_action = QAction("Composición F073", self)
        F073_action.triggered.connect(lambda: self.set_project("DB", "Composición F073"))
        # F073_action.setEnabled(False)

        F081_action = QAction("Composición F081", self)
        F081_action.triggered.connect(lambda: self.set_project("DSB", "Composición F081"))

        LOK_action = QAction("Locomotora Aislada", self)
        LOK_action.triggered.connect(lambda: self.set_project("LOK", "Locomotora Aislada F073"))
        LOK_action.setEnabled(False)

        connect_menu.addActions([F073_action, F081_action, LOK_action])
        
        ######### MENÚ MONITOR ##########
        
        monitor_menu=self.menu_bar.addMenu("Monitor")
        
        start_monitor_action=QAction("Iniciar captura datos", self)
        start_monitor_action.setEnabled(False)
        
        pause_monitor_action=QAction("Pausar captura datos", self)
        pause_monitor_action.setEnabled(False)
        
        stop_monitor_action=QAction("Pausar y borrar captura datos", self)
        stop_monitor_action.setEnabled(False)
        
        monitor_menu.addActions([start_monitor_action, pause_monitor_action, stop_monitor_action]) 
        
        ######### MENÚ DIAGNÓSTICO ##########
        
        diag_menu=self.menu_bar.addMenu("Diagnóstico")
        
        self.check_TSC_action = QAction("Comprobar estado lazo de seguridad (TSC)", self)
        self.check_TSC_action.setCheckable(True)
        self.check_TSC_action.toggled.connect(self.on_toggle_tsc)
        self.check_TSC_action.setEnabled(False)

        self.check_doors_action = QAction("Comprobar estado lazo de puertas", self)
        self.check_doors_action.setCheckable(True)
        self.check_doors_action.toggled.connect(self.on_toggle_doors)
        self.check_doors_action.setEnabled(False)

        self.massive_ping_action=QAction("Comprobar estado de comunicación de equipos", self)
        self.massive_ping_action.triggered.connect(self.massive_ping)
        self.massive_ping_action.setEnabled(False)
        
        diag_menu.addActions([self.check_TSC_action, self.check_doors_action, self.massive_ping_action])
        
        ######### MENÚ EXPORTAR ##########
        
        # export_menu = self.menu_bar.addMenu("Exportar")
        
        ######### MENÚ AYUDA ##########

        ayuda_menu = self.menu_bar.addMenu("Ayuda")

        # Acción de comprobar actualizaciones
        self.check_updates_action = QAction("Comprobar actualizaciones", self)
        self.check_updates_action.triggered.connect(self.check_for_updates)
        ayuda_menu.addAction(self.check_updates_action)

    def load_config(self):

        if not os.path.exists(CONFIG_FILE):
            return DEFAULT_CONFIG.copy()
        
        try:
            with open(CONFIG_FILE, 'r', encoding="utf-8") as f:
                data = json.load(f)
                # print(data)
                
        except Exception as e:
            print("ERROR: ", e)
            return DEFAULT_CONFIG.copy()
        
        
        cfg = DEFAULT_CONFIG.copy()

        for seccion, valores in data.items():
            # print(seccion, valores)
            if seccion in cfg and isinstance(valores, dict):
                cfg[seccion].update(valores)
        return cfg
            
    def save_config(self):
        with open(CONFIG_FILE, 'w', encoding="utf-8") as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)

    def open_preferences(self):

        def create_general_page():
            w = QWidget()
            layout = QFormLayout(w)
            self.ping_timeout = QSpinBox()
            self.ping_timeout.setRange(50,1001)
            self.ping_timeout.setSuffix(" ms")

            layout.addRow("Timeout para pings:", self.ping_timeout)

            return w
       
        def create_network_page():
            
            w = QWidget()
            layout = QFormLayout(w)

            self.spin_ping_count = QSpinBox()
            self.spin_ping_count.setRange(1,201)
            self.spin_ping_count.setSuffix(" paquetes")

            self.auto_export = QCheckBox("Auto exportar informe de resultados al escanear la red")

            self.max_threads = QSpinBox()
            self.max_threads.setRange(1,50)
            self.max_threads.setSuffix(" hilos en paralelo")

            path_layout = QHBoxLayout()
            self.export_path = QLineEdit()
            self.browse_export = QPushButton("Examinar")

            def path_select():
                filename, _ = QFileDialog.getSaveFileName(
                    self, "Seleccionar ruta de exportación", "network_report.xls", "Archivos excel (*.xlsx);;Todos (*.*)"
                )
                if filename: 
                    self.export_path.setText(filename)
            
            self.browse_export.clicked.connect(path_select)

            layout.addRow("Número de paquetes enviados por ping: ", self.spin_ping_count)
            layout.addRow("Número máximo de hilos en paralelo haciendo ping: ", self.max_threads)
            # layout.addRow("", self.chk_auto_check)

            path_layout.addWidget(self.export_path)
            path_layout.addWidget(self.browse_export)

            
            layout.addRow(self.auto_export)
            layout.addRow("Ruta exportación: ", path_layout)

            return w

        def load_into_widgets(config):
            g = config.get("general", {})

            n = config.get("massive_ping", {})


            self.ping_timeout.setValue(int(g.get("ping_timeout")))

            self.spin_ping_count.setValue(int(n.get("ping_count", "1")))
            self.max_threads.setValue(int(n.get("max_threads", "1")))
            self.auto_export.setChecked(bool(n.get("auto_export")))
            self.export_path.setText(n.get("export_path", ""))
            
        def widgets_into_config(config, save = True):
            # Partimos de la config actual (por ejemplo la que cargaste al abrir la app)
            cfg = copy.deepcopy(config)
  
            
            # Aseguramos que existen las secciones
            g = cfg.setdefault("general", {})
            n = cfg.setdefault("massive_ping", {})

            # ----- general -----
            # Aquí deberías leer los widgets que correspondan a estos campos.
            # Ejemplo (cambia los nombres de los widgets por los tuyos reales):
            
            g["ping_timeout"]     = self.ping_timeout.value()

            # ----- massive_ping -----
            n["ping_count"] = self.spin_ping_count.value()
            n["max_threads"] = self.max_threads.value()
            n["auto_export"] = self.auto_export.isChecked()
            n["export_path"] = self.export_path.text()

            if save:
                # Guardamos en el objeto
                self.config = cfg
                self.save_config()
            else: 
                return cfg

        self.preferences_windows = QWidget()
        self.preferences_windows.setWindowTitle("Configuración")
        self.preferences_windows.resize(800,800)

        self.config = self.load_config()

        # print(self.config)

        splitter = QSplitter(Qt.Horizontal, self)

        self.section_list = QListWidget()
        self.section_list.addItems([
            "General",
            "Comprobación estado de red",
            "Importar/Exportar archivo de configuración"
        ])

        self.pages = QStackedWidget()

        self.page_general = create_general_page()
        self.page_network = create_network_page()
        # self.page_import_export = create_import_export_page()

        self.pages.addWidget(self.page_general)
        self.pages.addWidget(self.page_network)
        # self.pages.addWidget(self.page_import_export)
        
        splitter.addWidget(self.section_list)
        splitter.addWidget(self.pages)
        splitter.setStretchFactor(1, 1)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.Apply, Qt.Horizontal, self)

        apply_btn = buttons.button(QDialogButtonBox.Apply)
        apply_btn.clicked.connect(lambda: widgets_into_config(self.config))

        def on_ok():
            actual_cfg = widgets_into_config(self.config, save = False)

            if self.config != actual_cfg:
                msg = QMessageBox(self)
                msg.setWindowTitle("Guardar cambios")
                msg.setText("¿Desea guardar los cambios realizados?")
                msg.setIcon(QMessageBox.Question)

                guardar = msg.addButton("Guardar", QMessageBox.AcceptRole)
                descartar = msg.addButton("Descartar", QMessageBox.DestructiveRole)
                # cancelar = msg.addButton("Cancelar", QMessageBox.RejectRole)

                msg.exec()
                clicked = msg.clickedButton()
                if clicked == guardar:
                    self.config = actual_cfg
                    self.save_config()
                    self.preferences_windows.close()
                elif clicked == descartar:
                    self.preferences_windows.close()
                else:
                    self.preferences_windows.close()
                    return
            else: 
                self.preferences_windows.close()
                    
        ok_btn = buttons.button(QDialogButtonBox.Ok)
        ok_btn.clicked.connect(on_ok)

        cancel_btn = buttons.button(QDialogButtonBox.Cancel)
        cancel_btn.clicked.connect(self.preferences_windows.close)

        self.section_list.currentRowChanged.connect(self.pages.setCurrentIndex)

        main_layout = QVBoxLayout()
        main_layout.addWidget(splitter)
        main_layout.addWidget(buttons)
        self.preferences_windows.setLayout(main_layout)

        self.preferences_windows.show()

        load_into_widgets(self.config)

    def check_for_updates(self):
        """Muestra el aviso y comprueba si hay una nueva versión"""
        msg = QMessageBox()
        msg.setWindowTitle("Comprobar actualizaciones")
        msg.setText("Compruebe que no está conectado al vehículo y que dispone de conexión a internet.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setIcon(QMessageBox.Information)
        response = msg.exec()

        if response == QMessageBox.Ok:
            try:
                url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"
                with urllib.request.urlopen(url) as resp:
                    data = json.load(resp)

                latest_tag = data.get("tag_name", "")
                assets = data.get("assets", [])

                def to_tuple(v):
                    return tuple(int(x) for x in v.strip("v").split("."))

                if latest_tag and to_tuple(latest_tag) > to_tuple(APP_VERSION):
                    download_url = assets[0]["browser_download_url"] if assets else data["html_url"]

                    update_msg = QMessageBox()
                    update_msg.setWindowTitle("Nueva versión disponible")
                    update_msg.setText(
                        f"Se ha encontrado una nueva versión ({latest_tag}).\n\n¿Desea descargarla ahora?"
                    )
                    update_msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                    update_msg.setIcon(QMessageBox.Question)
                    choice = update_msg.exec()

                    if choice == QMessageBox.Yes:
                        webbrowser.open(download_url)
                else:
                    QMessageBox.information(
                        self, "Sin actualizaciones", "Ya dispone de la última versión disponible."
                    )

            except Exception as e:
                QMessageBox.warning(
                    self,
                    "Error",
                    f"No se pudo comprobar actualizaciones.\n\nDetalles:\n{str(e)}",
                )

    def coach_scan_progress(self, progress, coach_number):
        
        self.detected_label.setText(f"Coches detectados: {0 + coach_number} de {len(self.ip_data[self.project])} posibles.")
        self.progress_bar.setValue(progress)

    def set_project(self, project_value, project_name):

        if hasattr(self, "stop_vars_polling"):
            self.stop_vars_polling()

        self.setMinimumSize(0, 0)
        self.setMaximumSize(16777215, 16777215)

        # Bucle para eliminar widgets del layout
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget:
                # Encuentra todos los atributos que hacen referencia a este widget
                for attr_name, attr_value in list(self.__dict__.items()):
                    if attr_value is widget:
                        # Elimina la referencia al atributo
                        delattr(self, attr_name)
                # Borra el widget del layout
                widget.deleteLater()

        self.adjustSize()

        self.setFixedSize(self.default_width, self.default_height)
                        
        self.project = project_value
    
        self.max_initial_ips =  21 if self.project == "DB" else 15 if self.project == "DSB" else 1
        
        self.progress_title.setText(f"Escaneando composición: {self.project}")
        self.detected_label.setText(f"Coches detectados: {0 + self.max_initial_ips} de {len(self.ip_data[self.project])} posibles.")

        self.progress_bar.setValue(0)
        self.progress_title.setVisible(True)
        self.progress_bar.setVisible(True)
        self.detected_label.setVisible(True)

        self.valid_ips = []
        
        self.scan_thread = ScanThread(self.ip_data[self.project], self.max_initial_ips, self.project, self.ip_data["DB_VCUCH_CABCAR"], self.ip_data["DB_VCUPH_CABCAR"], self.config)
        self.scan_thread.scan_progress.connect(self.coach_scan_progress)
        self.scan_thread.scan_completed.connect(self.on_scan_completed)
        self.scan_thread.start()

    def on_scan_completed(self, valid_ips):
        self.valid_ips = valid_ips

        self.progress_bar.setVisible(False)
        self.detected_label.setVisible(False)
        self.progress_title.setVisible(False)

        # endpoints 1:1 con IPs
        self.endpoint_ids = [f"EP{i+1}" for i in range(len(self.valid_ips))]

        # instancias por endpoint
        self.endpoint_clients = {}
        for eid, ip in zip(self.endpoint_ids, self.valid_ips):
            self.endpoint_clients[eid] = CoachClient(eid, ip, health_vars=[])

        # tabla como ya la tienes (IPs + span tipo cabcar)
        self.create_table()

        self.check_TSC_action.setEnabled(True)
        self.check_doors_action.setEnabled(True)
        self.massive_ping_action.setEnabled(True)

        screen = QApplication.primaryScreen()
        
        max_width = screen.availableGeometry().width()  
        max_height = screen.availableGeometry().height() 

        window_width = window.size().width()
        window_height = window.size().height()
    
        self.move(int((max_width - min(window_width, max_width))/2),200)

        # arrancar polling selectivo (opción 2)
        self.start_vars_polling_selective()

    def stop_vars_polling(self):
        if hasattr(self, "vars_workers") and self.vars_workers:
            for w in self.vars_workers.values():
                try:
                    w.stop()
                except Exception:
                    pass

        if hasattr(self, "vars_threads") and self.vars_threads:
            for th in self.vars_threads.values():
                try:
                    th.quit()
                    th.wait()
                except Exception:
                    pass

        self.vars_workers = {}
        self.vars_threads = {}

        if hasattr(self, "vars_warehouse") and self.vars_warehouse:
            try:
                self.vars_warehouse.stop()
            except Exception:
                pass
            self.vars_warehouse = None

    def start_vars_polling_selective(self):
        self.stop_vars_polling()

        # crea store
        self.vars_warehouse = Vars_Warehouse(self.endpoint_ids, render_hz=10)
        self.vars_warehouse.snapshotUpdated.connect(self.on_vars_snapshot)
        self.vars_warehouse.start()

        self.vars_threads = {}
        self.vars_workers = {}

        # Obtenemos la posición del cabcar
        cabcar_ph_index = len(self.endpoint_ids) - 1 if (self.project == "DB" and len(self.endpoint_ids) >= 2) else None

        for idx, eid in enumerate(self.endpoint_ids):
            client = self.endpoint_clients[eid]

            if cabcar_ph_index is not None and idx == cabcar_ph_index:
                is_cc = True
            else:
                is_cc = False

            th = QThread()
            w = Worker(is_cc=is_cc, project=self.project, endpoint_client=client, vars_to_read=self.diag_dict, diag_enabled=self.diag_enabled, period_s=0.5, wait_time=1.0)

            w.moveToThread(th)
            th.started.connect(w.start)

            self.diagnosis_config_signal.connect(w._update_config)
            w.on_tsc_data.connect(self.vars_warehouse.on_tsc_data)
            w.on_tsc_diag_data.connect(self.vars_warehouse.on_tsc_diag_data)
            w.on_door_data.connect(self.vars_warehouse.on_doors_data)
            w.on_door_diag_data.connect(self.vars_warehouse.on_door_diag_data)
            w.status.connect(self.vars_warehouse.on_status)

            self.vars_threads[eid] = th
            self.vars_workers[eid] = w
            th.start()

    def on_vars_snapshot(self, snapshot: dict):

        # 1) tabla siempre
        self.update_table_from_snapshot(snapshot)

        # 2) si la ventana TSC existe, actualizamos
        if self.check_TSC_action.isChecked() and self.tsc_window is not None:
            tsc_svg_snapshot = self.build_svg_snapshot(snapshot)
            self.tsc_window.set_snapshot(tsc_svg_snapshot)
            self.tsc_window.TSC_Diag_window.set_snapshot(snapshot)
        if self.check_doors_action.isChecked() and self.doors_window is not None:
            self.doors_window.set_snapshot(snapshot)
            self.doors_window.Door_diag_window.set_snapshot(snapshot)

    def update_table_from_snapshot(self, snapshot: dict):

        show_tsc = bool(self.check_TSC_action.isChecked())
        show_doors = bool(self.check_doors_action.isChecked())

        if show_doors:
            coaches = snapshot.get("doors", {})
        else:
            coaches = snapshot.get("tsc", {})

        type_var = self.TCMS_vars.COACH_TYPE[0]  # incluido en tsc_vars

        cab_main_col = len(self.endpoint_ids) - 2 if (self.project == "DB" and len(self.endpoint_ids) >= 2) else None

        for col, eid in enumerate(self.endpoint_ids):
            c = coaches.get(eid, {"online": False, "values": {}})
            online = bool(c.get("online", False))
            values = c.get("values", {}) or {}

            # if eid == "EP1":
                # print(values.get(type_var, ""))

            # fila 0: color por online
            ip_item = self.table.item(0, col)
            if ip_item:
                ip_item.setBackground(QColor(175, 242, 175) if online else QColor(255, 131, 131))

            # fila 1: tipo coche
            if self.project == "DB" and cab_main_col is not None:
                # solo escribir en la columna "normal" del cabcar (col -2); la última está en el span
                if col == cab_main_col:
                    raw = values.get(type_var, "")
                    txt = str(raw)
                    if txt.isdigit():
                        n = int(txt)
                        txt = self.TCMS_vars.COACH_TYPES_DB.get(n, txt)

                    type_item = self.table.item(1, col)
                    if type_item is None:
                        type_item = QTableWidgetItem("")
                        type_item.setTextAlignment(Qt.AlignCenter)
                        self.table.setItem(1, col, type_item)
                    type_item.setText(txt)

            raw = values.get(type_var, "")
            txt = str(raw)
            if txt.isdigit():
                n = int(txt)
                if self.project == "DSB":
                    txt = self.TCMS_vars.COACH_TYPES_DSB.get(n, "Not Valid")
                else:
                    txt = self.TCMS_vars.COACH_TYPES_DB.get(n, "Not Valid")
                    
            type_item = self.table.item(1, col)
            if type_item is None:
                type_item = QTableWidgetItem("")
                type_item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(1, col, type_item)
            type_item.setText(txt)

    def build_svg_snapshot(self, endpoint_snapshot: dict) -> dict:

        # print("Construyendo snapshot para SVG a partir de:", endpoint_snapshot["coaches"]["EP1"])
        ep = endpoint_snapshot.get("tsc", {})

        # Si no es DB o no hay doble IP, no hacemos merge
        if self.project != "DB" or len(self.endpoint_ids) < 2:
            return {"tsc": ep}

        cab_main_col = len(self.endpoint_ids) - 2
        cab_cc_col   = len(self.endpoint_ids) - 1

        out = {}

        # Copia todo menos la IP CC (última)
        for col, eid in enumerate(self.endpoint_ids):
            if col == cab_cc_col:
                continue
            out[eid] = {
                "online": bool(ep.get(eid, {}).get("online", False)),
                "values": dict(ep.get(eid, {}).get("values", {}) or {}),
            }

        eid_main = self.endpoint_ids[cab_main_col]
        eid_cc   = self.endpoint_ids[cab_cc_col]

        main = ep.get(eid_main, {"online": False, "values": {}})
        cc   = ep.get(eid_cc,   {"online": False, "values": {}})

        merged = {}
        merged.update(main.get("values", {}) or {})
        merged.update(cc.get("values", {}) or {})

        merged_online = bool(main.get("online", False)) and bool(cc.get("online", False))

        out[eid_main] = {"online": merged_online, "values": merged}
        return {"tsc": out}

    def on_toggle_tsc(self, checked: bool):
        if checked:
            self.diag_enabled["TSC"] = True
            self.diagnosis_config_signal.emit(self.diag_enabled)

            # Crear ventana si no existe (o si fue cerrada)
            if self.tsc_window is None:
                # tamaño fijo definido por ti:
                FIX_W = 1300
                FIX_H = 350

                # OJO: aquí usas las listas que ya estabas usando para generar el SVG
                # (tsc_vars incluye COACH_TYPE al final)
                if self.project == "DB":
                    tsc_vars = self.TCMS_vars.TSC_COACH_VARS_DB + self.TCMS_vars.COACH_TYPE
                    tsc_cc_vars = self.TCMS_vars.TSC_CC_VARS_DB
                    coach_types = self.TCMS_vars.COACH_TYPES_DB
                else:
                    tsc_vars = self.TCMS_vars.TSC_COACH_VARS_DSB + self.TCMS_vars.COACH_TYPE
                    tsc_cc_vars = []
                    coach_types = self.TCMS_vars.COACH_TYPES_DSB

                self.tsc_window = TSCWindow(
                    project=self.project,
                    endpoint_ids=self.endpoint_ids,
                    tsc_vars=tsc_vars,
                    project_coach_types=coach_types,
                    tsc_cc_vars=tsc_cc_vars,
                    fixed_w=FIX_W,
                    fixed_h=FIX_H,
                    valid_ips=self.valid_ips,
                    parent=self,
                )


                # Si el usuario cierra la ventana -> equivale a desmarcar el check
                self.tsc_window.closed.connect(lambda: self.check_TSC_action.setChecked(False))

            self.tsc_window.show()
            self.tsc_window.raise_()
            self.tsc_window.activateWindow()

            # Render inmediato (sin esperar al siguiente snapshot)
            if self.vars_warehouse is not None:
                snapshot = {
                    "tsc": {
                        eid: {"online": bool(st.get("online", False)), "values": dict(st.get("values", {}) or {})}
                        for eid, st in self.vars_warehouse.tsc_state.items()
                    },
                    "tsc_diag": {
                        eid: {"online": bool(st.get("online", False)), "values": dict(st.get("values", {}) or {})}
                        for eid, st in self.vars_warehouse.tsc_diag_state.items()
                    }
                }
                svg_snapshot = self.build_svg_snapshot(snapshot)
                self.tsc_window.set_snapshot(svg_snapshot)
                self.tsc_window.TSC_Diag_window.set_snapshot(snapshot)
                

            screen = QApplication.primaryScreen()
            max_width = screen.availableGeometry().width()  
            max_height = screen.availableGeometry().height() 

            window_size = self.tsc_window.size()
            self.tsc_window.move(int((max_width - min(window_size.width(), max_width))/2),int((max_height - min(window_size.height(), max_height))/2))

        else:
            self.diag_enabled["TSC"] = False
            self.diagnosis_config_signal.emit(self.diag_enabled)
            
            # Cerrar ventana si está abierta
            if self.tsc_window is not None:
                try:
                    self.tsc_window.close()
                except Exception:
                    pass
                self.tsc_window = None

    def on_toggle_doors(self, checked: bool):
        if checked:
            self.diag_enabled["DOORS"] = True
            self.diagnosis_config_signal.emit(self.diag_enabled)

            # Crear ventana si no existe (o si fue cerrada)
            if self.doors_window is None:
                # tamaño fijo definido por ti:
                FIX_W = 1300
                FIX_H = 400
               
                doors_vars = self.TCMS_vars.DOORS_LOOP_VARS + self.TCMS_vars.COACH_TYPE

                if self.project == "DB":
                    coach_types = self.TCMS_vars.COACH_TYPES_DB
                else:
                    coach_types = self.TCMS_vars.COACH_TYPES_DSB

                

                self.doors_window = DOORWindow(
                    project=self.project,
                    endpoint_ids=self.endpoint_ids,
                    doors_vars=doors_vars,
                    project_coach_types=coach_types,
                    fixed_w=FIX_W,
                    fixed_h=FIX_H,
                    valid_ips=self.valid_ips,
                    endpoint_clients=self.endpoint_clients,
                    parent=self,
                )

                if DEV_MODE:
                    self.doors_window._load_dev_snapshot()

                # Si el usuario cierra la ventana -> equivale a desmarcar el check
                self.doors_window.closed.connect(lambda: self.check_doors_action.setChecked(False))

            self.doors_window.show()
            self.doors_window.raise_()
            self.doors_window.activateWindow()

            # Render inmediato (sin esperar al siguiente snapshot)
            if self.vars_warehouse is not None:
                snapshot = {
                    "doors": {
                        eid: {"online": bool(st.get("online", False)), "values": dict(st.get("values", {}) or {})}
                        for eid, st in self.vars_warehouse.doors_state.items()
                    },
                    "doors_diag": {
                        eid: {"online": bool(st.get("online", False)), "values": dict(st.get("values", {}) or {})}
                        for eid, st in self.vars_warehouse.door_diag_state.items()
                    }
                }


                self.doors_window.set_snapshot(snapshot)   
                self.doors_window.Door_diag_window.set_snapshot(snapshot)


            screen = QApplication.primaryScreen()
            max_width = screen.availableGeometry().width()  
            max_height = screen.availableGeometry().height() 

            window_size = self.doors_window.size()
            self.doors_window.move(int((max_width - min(window_size.width(), max_width))/2),int((max_height - min(window_size.height(), max_height))/2))

        else:
            self.diag_enabled["DOORS"] = False
            self.diagnosis_config_signal.emit(self.diag_enabled)

            # Cerrar ventana si está abierta
            if self.doors_window is not None:
                try:
                    self.doors_window.close()
                except Exception:
                    pass
                self.doors_window = None

    def create_table(self):
        
        headers = []
        for i in range(len(self.valid_ips)):
            # Si es DB y estamos en las dos últimas IPs, cambiar el encabezado
            if self.project == "DB" and i >= len(self.valid_ips) - 2:
                suffix = "VCU_CH" if i == len(self.valid_ips) - 2 else "VCU_PH"
                headers.append(f"Coche {len(self.valid_ips) - 1} ({suffix})")
            else:
                headers.append(f"Coche {i + 1}")

        self.table = QTableWidget(2, len(self.valid_ips))
        self.table.setHorizontalHeaderLabels(headers)
        
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        for col, ip in enumerate(self.valid_ips):
            
            item = QTableWidgetItem(ip)
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(0, col, item)

        # Fusionar solo el tipo de coche (fila 1) si es DB
        if self.project == "DB" and len(self.valid_ips) >= 2:
            last_coach_index = len(self.valid_ips) - 2
            self.table.setSpan(1, last_coach_index, 1, 2)  # Combinar fila 1, columnas -2 y -1


        if len(self.valid_ips) > 1: 
        
            self.table.resizeColumnsToContents()
            self.table.resizeRowsToContents()
    
            self.table_width = sum(self.table.columnWidth(col) for col in range(len(self.valid_ips))) + self.table.verticalHeader().width()
            table_height = sum(self.table.rowHeight(row) for row in range(2)) + self.table.horizontalHeader().height()

            self.setFixedSize(self.table_width + 21, table_height + 42)
 
        else:
            
            header = self.table.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
            self.table.resizeRowsToContents()
            QApplication.processEvents()
            
            self.setFixedSize(self.default_width/2, 115)


        self.layout.addWidget(self.table)
        
        self.check_TSC_action.setEnabled(True)
        self.check_doors_action.setEnabled(True)
        self.massive_ping_action.setEnabled(True)

    def export_to_excel(self, table):
        """Exportar los datos de la tabla a un archivo Excel incluyendo número y tipo de coche.
        Mejora: estilo visual, autofiltro, freeze pane y ancho de columnas adaptado al contenido.
        """
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar como",
            "",
            "Archivos Excel (*.xlsx);;Todos los archivos (*)",
            options=options
        )

        if not file_path:
            return

        # Asegurar extensión
        if not file_path.lower().endswith(".xlsx"):
            file_path += ".xlsx"

        workbook = xlsxwriter.Workbook(file_path)
        worksheet = workbook.add_worksheet("Errores TSC")

        # Formatos
        header_format = workbook.add_format({
            'bold': True, 'bg_color': '#2F5496', 'font_color': '#FFFFFF',
            'border': 1, 'align': 'center', 'valign': 'vcenter'
        })
        coach_header_format = workbook.add_format({
            'bold': True, 'bg_color': '#595959', 'font_color': '#FFFFFF',
            'border': 1, 'align': 'center'
        })
        tipo_format = workbook.add_format({'border': 1, 'align': 'center'})
        cell_format = workbook.add_format({'border': 1, 'text_wrap': True, 'valign': 'top', 'align': 'left'})
        no_errors_format = workbook.add_format({'border': 1, 'bg_color': '#D9D9D9', 'align': 'center'})
        error_code_format = workbook.add_format({'border': 1, 'font_color': '#C00000', 'align': 'center'})

        # Encabezados
        headers = ["Coche", "Tipo", "IP", "Código de Error", "Descripción"]
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)

        # Recorremos la tabla Qt y construimos las filas de exportación
        row_index = 1
        current_coche = ""
        current_ip = ""
        coach_index = -1
        current_tipo = ""

        # Diccionario de tipos según proyecto
        if self.project == "DB":
            type_dict = self.TCMS_vars.COACH_TYPES_DB
        elif self.project == "DSB":
            type_dict = self.TCMS_vars.COACH_TYPES_DSB
        else:
            type_dict = {}

        # Guardar filas para calcular anchos
        rows_for_width = [["Coche", "Tipo", "IP", "Código de Error", "Descripción"]]

        for row in range(table.rowCount()):
            ip_item = table.item(row, 0)
            ip_text = ip_item.text() if ip_item else ""

            # Fila de encabezado tipo "COCHE X (VCU_CH) IP: ..."
            if "COCHE" in ip_text and "IP:" in ip_text:
                import re
                match = re.match(r"COCHE\s+(\d+).*IP:\s+([\d\.]+)", ip_text)
                if match:
                    coche_num = int(match.group(1))
                    ip = match.group(2)
                    current_coche = f"COCHE {coche_num}"
                    current_ip = ip

                    # Buscar índice del IP
                    coach_index = next((i for i, coach in enumerate(self.trainset_coaches) if coach.ip == ip), -1)

                    # Obtener tipo numérico
                    if 0 <= coach_index < len(self.coach_types):
                        tipo_num = self.coach_types[coach_index]

                        # Si es el último VCU en proyecto DB, forzar tipo del anterior
                        if self.project == "DB" and coach_index == len(self.coach_types) - 1:
                            tipo_num = self.coach_types[coach_index - 1]

                        try:
                            tipo_name = type_dict.get(int(tipo_num), "???")
                        except Exception:
                            tipo_name = type_dict.get(tipo_num, "???")
                        current_tipo = f"{tipo_num} ({tipo_name})"
                    else:
                        current_tipo = "???"
                # No escribimos fila de encabezado como fila de detalle, sólo la usamos como contexto
                continue

            # Fila de error
            if ip_text:  # si hay algo en columna 0, usamos esa IP
                ip = ip_text
            else:
                ip = current_ip

            error_code = table.item(row, 1).text() if table.item(row, 1) else ""
            description = table.item(row, 2).text() if table.item(row, 2) else ""

            # Si no tenemos coche contextual, intentar inferir por IP
            if not current_coche:
                coach_index = next((i for i, coach in enumerate(self.trainset_coaches) if coach.ip == ip), -1)
                if coach_index >= 0:
                    current_coche = f"COCHE {coach_index + 1}"
                    tipo_num = self.coach_types[coach_index] if 0 <= coach_index < len(self.coach_types) else None
                    try:
                        tipo_name = type_dict.get(int(tipo_num), "???") if tipo_num is not None else "???"
                    except Exception:
                        tipo_name = type_dict.get(tipo_num, "???")
                    current_tipo = f"{tipo_num} ({tipo_name})" if tipo_num is not None else "???"

            worksheet.write(row_index, 0, current_coche, tipo_format)
            worksheet.write(row_index, 1, current_tipo, tipo_format)

            # IP
            worksheet.write(row_index, 2, ip, cell_format)

            # Código de error (resaltar en rojo si no es "Sin errores activos")
            if error_code and "Sin errores" not in error_code:
                worksheet.write(row_index, 3, error_code, error_code_format)
            elif "Sin errores" in error_code:
                worksheet.write(row_index, 3, error_code, no_errors_format)
            else:
                worksheet.write(row_index, 3, error_code, cell_format)

            worksheet.write(row_index, 4, description, cell_format)

            rows_for_width.append([current_coche, current_tipo, ip, error_code or "", description or ""])
            row_index += 1

        # Autofiltro y freeze pane
        if row_index > 1:
            worksheet.autofilter(0, 0, row_index - 1, len(headers) - 1)
        worksheet.freeze_panes(1, 0)

        # Ajustar anchos de columnas basados en contenido
        max_widths = [0] * len(headers)
        for r in rows_for_width:
            for c, cell in enumerate(r):
                length = len(str(cell))
                if length > max_widths[c]:
                    max_widths[c] = length

        # Convertir longitud de caracteres a ancho razonable en Excel (aprox)
        for col, max_ch in enumerate(max_widths):
            # limit width and add padding
            width = min(max(10, max_ch + 4), 60)
            worksheet.set_column(col, col, width)

        workbook.close()

        # Mensaje corto al usuario
        try:
            QMessageBox.information(self, "Exportado", f"Exportado correctamente a:\n{file_path}")
        except Exception:
            pass

    def massive_ping(self):

        self.msg = QMessageBox(self)
        self.msg.setWindowTitle("Cargando configuración de red")
        self.msg.setText("Cargando configuración de la red de ethernet...")
        self.msg.setStandardButtons(QMessageBox.NoButton)
        self.msg.open()

        QApplication.processEvents()

        self.screen_width = QApplication.primaryScreen().size().width()
        
        if self.project == "DB":
            self.red_eth = self.cargar_red(self.resource_path("F073_IP_Ports_Addressing_00_40.xlsm"))
        elif self.project == "DSB":
            self.red_eth = self.cargar_red(self.resource_path("F081_IP_Ports_Addressing_v13.3_Cabcar.xlsm"))

        self.msg.accept()

        # print(self.red_eth.keys())
        # print(self.red_eth)

        count = 0
        COLS_PER_COACH = 5  # PUERTO, PORT ID, VLAN, DEVICE, IP
        
        for types in self.red_eth.keys():
            coach_count = 0
            coach_count += len(self.red_eth[types])
            coach_count += sum(len(devices) for devices in self.red_eth[types].values())
            if coach_count > count:
                count = coach_count
                # print(self.red_eth[types])
        
        self.massive_ping_window = QWidget()
        self.massive_ping_window.setWindowTitle("Comprobación de estado de comunicación de los equipos")

        table_layout = QVBoxLayout()

        self.massive_ping_table = QTableWidget()
        self.massive_ping_table.setContextMenuPolicy(Qt.CustomContextMenu) # Habilitar menú contextual
        self.massive_ping_table.customContextMenuRequested.connect(self.massive_ping_context_menu) # Conectar petición del menú contextual a la función

        coach_types = []

        for eid in self.vars_warehouse.tsc_state.keys():
            coach_types.append(self.vars_warehouse.tsc_state[eid].get("values", {}).get(self.TCMS_vars.COACH_TYPE[0], "Unknown"))
        
        if self.project == "DB":
            coach_types.pop()  # Eliminar el último tipo que corresponde al cabcar
        
        # print(coach_types)
                
        num_coaches = len(coach_types)

        self.massive_ping_table.setColumnCount(num_coaches * COLS_PER_COACH)  # 5 columnas por coche: PUERTO, VLAN, DEVICE, IP
        self.massive_ping_table.setRowCount(count)

        for col in range(num_coaches):
            esu_id = 0 # Reiniciar ID de ESU para cada coche
            print_row = 1  # Reiniciar fila de impresión para cada coche
            if str(coach_types[col]) == "Unknown":
                tipo = 0
            else: 
                tipo = self.TCMS_vars.COACH_TYPES_DSB[int(coach_types[col])] if self.project == "DSB" else self.TCMS_vars.COACH_TYPES_DB[int(coach_types[col])]
            
            if tipo == "C4302P":
                tipo = "C4302C"
            
            c0 = 5 * col  # desplazamiento de columnas para este coche (bloque de 4 columnas)

            # ---- Fila 0: título del coche (fusionado 4 columnas) ----
            coach_title = QTableWidgetItem(f"Coche {col+1} — {tipo if tipo != 0 else 'Desconocido'}")
            coach_title.setTextAlignment(Qt.AlignCenter)
            coach_title.setBackground(QBrush(QColor(100, 100, 100)))
            coach_title_font = coach_title.font(); coach_title_font.setBold(True); coach_title.setFont(coach_title_font)
            self.massive_ping_table.setItem(0, c0, coach_title)
            self.massive_ping_table.setSpan(0, c0, 1, COLS_PER_COACH)  # fusiona columnas 0..3 del bloque

            print_row = 1

            # Cargar definición de red a partir del TIPO
            esus_dict = self.red_eth.get(tipo, {})  # dict de ESUs para ese tipo
            # Itera ESUs (orden natural del dict; si quieres orden predecible, usa: for esu_name in sorted(esus_dict))

            if not esus_dict == {}:

                for esu_name, ports_dict in esus_dict.items():
                    # ---- Fila de título de ESU (fusionada) ----
                    esu_item = QTableWidgetItem(str(esu_name))
                    esu_item.setTextAlignment(Qt.AlignCenter)
                    esu_font = esu_item.font(); esu_font.setBold(True); esu_item.setFont(esu_font)
                    self.massive_ping_table.setItem(print_row, c0, esu_item)
                    self.massive_ping_table.setSpan(print_row, c0, 1, COLS_PER_COACH)
                    print_row += 1
                    esu_header = ["PORT", "PORT ID", "VLAN", "DEVICE", "IP"]
                    for i, header in enumerate(esu_header):
                        header_item = QTableWidgetItem(header)
                        header_item.setTextAlignment(Qt.AlignCenter)
                        header_font = header_item.font(); header_font.setBold(True); header_item.setFont(header_font)
                        self.massive_ping_table.setItem(print_row, c0 + i, header_item)
                    print_row += 1

                    # ---- Filas de puertos de la ESU ----
                    # ports_dict: {"E0_0": {"vlan":..., "device":..., "ip":...}, ...}
                    port_id = 0
                    for port_name, info in ports_dict.items():  # si quieres orden, usa sorted(ports_dict.items())
                        self.massive_ping_table.setItem(print_row, c0 + 0, QTableWidgetItem(str(port_name)))
                        self.massive_ping_table.setItem(print_row, c0 + 1, QTableWidgetItem(str(port_id)))
                        self.massive_ping_table.setItem(print_row, c0 + 2, QTableWidgetItem(str(info.get("VLAN", ""))))
                        self.massive_ping_table.setItem(print_row, c0 + 3, QTableWidgetItem(str(info.get("Device", ""))))
                        if str(info.get("Device", "")) == "VCU_CH":
                            self.massive_ping_table.setItem(print_row, c0 + 4, QTableWidgetItem(str(self.valid_ips[col])))
                        else: 
                            self.massive_ping_table.setItem(print_row, c0 + 4, QTableWidgetItem(self.calcular_ip(col + 1, info.get("VLAN", 0), esu_id, int(port_id)) if info.get("IP", "") is None else info.get("IP", ""))) #col+1 porque la posición empieza en 1
                        # print(str(info.get("Device", "")), col, info.get("VLAN", 0), esu_id, int(port_id))
                        print_row += 1
                        port_id += 1
                    
                    esu_id += 1 # Incrementar ID de ESU
                    if self.project == "DSB" and esu_id == 2:
                        esu_id = 4  # Saltar ID 3 en DSB
            
        # self.massive_ping_table.setItem(32, 4, QTableWidgetItem(str("192.168.1.139")))

        # Ajustar el ancho de las columnas al contenido
        self.massive_ping_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # Ajustar la altura de las filas al contenido
        self.massive_ping_table.resizeRowsToContents()

        # Calcular el ancho total de la tabla
        total_width = 0

        for col in range(self.massive_ping_table.columnCount()):
            total_width += self.massive_ping_table.columnWidth(col)  # Sumar ancho de cada columna
        
        total_width += self.massive_ping_table.frameWidth() * 2  # Bordes de la tabla

        # print(total_width)
        total_width = min (total_width, self.screen_width - 100)  # No exceder el ancho de la pantalla

        # Ajustar el tamaño de la ventana al ancho total de la tabla
        self.massive_ping_window.resize(total_width + 50, 800)  # Altura fija, pero podrías ajustarla también

        # table_layout.addWidget(menu_bar)
        table_layout.addWidget(self.massive_ping_table)
       
        self.massive_ping_window.setLayout(table_layout)
        self.massive_ping_window.show()

        ping_ip_tuple = []

        for i in range (num_coaches):
            ip_list = []
            for j in range (count):
                test_ip = self.massive_ping_table.item(j, i * 5 + 4).text() if self.massive_ping_table.item(j, i * 5 + 4) is not None else None
                ip_list.append([j, i, test_ip])
            ping_ip_tuple.append(ip_list)

        self.ping_executor = ThreadPoolExecutor(max_workers=self.config["massive_ping"]["max_threads"])

        self.logs = []
        self.ping_counter = 0
        
        for coach_list in ping_ip_tuple:
            for row, col, ip in coach_list:
                if ip is not None and self.is_valid_ip(ip):
                    self.ping_counter += 1
                # print(row, col, ip)
                self.ping_executor.submit(self.ping_ip_worker, row, col * 5 + 4, ip)

        # print(self.ping_counter, "pings en total iniciados.")
        
        # print(ping_ip_tuple)

    def massive_ping_context_menu(self, position):
        if self.massive_ping_table is None:
            return
        
        index = self.massive_ping_table.indexAt(position)
        if not index.isValid():
            return
        row = index.row()
        col = index.column()

        item = self.massive_ping_table.item(row, col)
        if item is None:
            return
        
        ip = (item.text() or "").strip()
        if not self.is_valid_ip(ip):
            return
        
        menu = QMenu()
        action_ping = menu.addAction(f"Rehacer ping a {ip}")

        global_pos = self.massive_ping_table.viewport().mapToGlobal(position)
        action = menu.exec(global_pos)

        if action == action_ping:
            item.setBackground(QBrush())  # Reset color

        self.ping_ip_worker(row, col, ip)

    def update_ping_cell(self, row: int, col: int, ok: bool, enviados: int, recibidos: int, perdidos: int, minimo: int, maximo: int, media: int):

        table = self.massive_ping_table
        if table is None:
            return

        item = table.item(row, col)
        if item is None:
            return
        # print(ok)
        color = QColor(175, 242, 175) if ok else QColor(255, 131, 131)
        item.setBackground(QBrush(color))

        # print(f"Ping a {item.text()}: {'OK' if ok else 'FALLIDO'} - Enviados: {enviados}, Recibidos: {recibidos}, Perdidos: {perdidos}, Mínimo: {minimo}ms, Máximo: {maximo}ms, Media: {media}ms")

        self.logs.append({
            "coche": (col - 4) // 5 + 1,
            "dispositivo": table.item(row, col - 1).text() if table.item(row, col - 1) is not None else "",
            "ip": item.text(),
            "ok": ok,
            "enviados": enviados,
            "recibidos": recibidos,
            "perdidos": perdidos,
            "minimo": minimo,
            "maximo": maximo,
            "media": media
        })

        # comunicar el resultado al hilo de la GUI
        
        self.ping_counter -= 1
        # print(self.ping_counter, "pings restantes.")

        if self.ping_counter == 0 and self.config["massive_ping"]["auto_export"] == True:

            self.export_ping_logs()

    def export_ping_logs(self):
        # print("Exportando logs de ping a ping_logs.xlsx...")

        path = self.config["massive_ping"]["export_path"]

        if path == "" or not os.path.isdir(os.path.dirname(path)):
            # path = r"C:\Users\75815\Desktop\ping_logs.xlsx"
                        
            dialog = QDialog(self)
            dialog.setWindowTitle("Ruta explortación de informe de conexiones de red")
            
            layout = QVBoxLayout()

            label = QLabel("Selecciona la ruta y el nombre del archivo para exportar el informe de conexiones de red:")
            layout.addWidget(label)

            hlayout = QHBoxLayout()
            line_edit = QLineEdit(dialog)
            line_edit.setText(path)
            hlayout.addWidget(line_edit)

            def path_select():
                filename, _ = QFileDialog.getSaveFileName(
                    self, "Seleccionar ruta de exportación", "network_report.xlsx", "Archivos excel (*.xlsx);;Todos (*.*)"
                )
                if filename: 
                    line_edit.setText(filename)
                    self.config["massive_ping"]["export_path"] = line_edit.text()

            browse_button = QPushButton("Examinar...", dialog)
            browse_button.clicked.connect(path_select)
            hlayout.addWidget(browse_button)

            layout.addLayout(hlayout)

            button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, dialog)

            def on_ok():
                self.config["massive_ping"]["export_path"] = line_edit.text()
                self.save_config()
                dialog.accept()

            ok_btn = button_box.button(QDialogButtonBox.Ok)
            ok_btn.clicked.connect(on_ok)

            cancel_btn = button_box.button(QDialogButtonBox.Cancel)
            cancel_btn.clicked.connect(dialog.reject)

            layout.addWidget(button_box)

            dialog.setLayout(layout)
            dialog.exec()

            path = self.config["massive_ping"]["export_path"]
            
        wb = xlsxwriter.Workbook(path)        
        ws = wb.add_worksheet("Ping Logs")
        headers = ["Coche", "Dispositivo", "IP", "Estado", "Enviados", "Recibidos", "Perdidos", "Mínimo (ms)", "Máximo (ms)", "Media (ms)"]

        # Formatos
        header_format = wb.add_format({
            'bold': True, 'bg_color': '#2F5496', 'font_color': '#FFFFFF',
            'border': 1, 'align': 'center', 'valign': 'vcenter'
        })

        cell_format = wb.add_format({'border': 1, 'text_wrap': True, 'valign': 'center', 'align': 'center'})

        ws.write_row(0, 0, headers, header_format)
        row_num = 1
        for log in self.logs:
            row = [
                log["coche"],
                log["dispositivo"],
                log["ip"],
                "OK" if log["ok"] else "FALLIDO",
                log["enviados"],
                log["recibidos"],
                log["perdidos"],
                log["minimo"],
                log["maximo"],
                log["media"]
            ]
            ws.write_row(row_num, 0, row, cell_format = cell_format)
            row_num += 1

        ws.autofilter(0,0,len(self.logs),9)
        ws.freeze_panes(1, 0)

        fake_header=["coche","dispositivo","ip","ok","enviados","recibidos","perdidos","minimo","maximo","media"]

        for col_idx in range(len(headers)):
            max_width = len(headers[col_idx])
            for row in self.logs:
                if len(str(row[fake_header[col_idx]])) > max_width:
                    max_width = len(str(row[fake_header[col_idx]]))
            ws.set_column(col_idx, col_idx, max_width + 5)  

        wb.close()
      
    def ping_ip_worker(self, row: int, col: int, ip: str):
        ok = False
        enviados = recibidos = perdidos = minimo = maximo = media = 0
        has_unreachable = False
        has_timeout = False

        # print(f"Haciendo ping a {ip}...")
        
        if self.is_valid_ip(ip):
            try:
                # Windows: -n 1 (un eco), -w timeout
                result = subprocess.Popen(
                    [   
                        "ping", 
                        "-n", str(self.config["massive_ping"]["ping_count"]), 
                        "-w", str(self.config["general"]["ping_timeout"]), 
                        ip
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    shell=True
                )
                stdout, stderr = result.communicate()
                
                lineas = stdout
                # print(lineas)

                for linea in lineas.splitlines():
                    linea = linea.lower()
                    if "inaccesible" in linea or "unreachable" in linea:
                        has_unreachable = True
                        minimo = maximo = media = self.config["general"]["ping_timeout"]
                    if "tiempo de espera agotado" in linea or "request timed out" in linea:
                        has_timeout = True
                        minimo = maximo = media = self.config["general"]["ping_timeout"]
                    if "paquetes" in linea and "enviados" in linea:
                        numeros = re.findall(r'(\d+)', linea)
                        if len(numeros) >= 3:
                            enviados = int(numeros[0])
                            recibidos = int(numeros[1])
                            perdidos = int(numeros[2])
                            # print(f"Enviados: {enviados}, Recibidos: {recibidos}, Perdidos: {perdidos}")
                    if "media" in linea and "ms" in linea:
                        numeros = re.findall(r'(\d+)\s*ms', linea)
                        if len(numeros) >= 3:
                            minimo = int(numeros[0])
                            maximo = int(numeros[1])
                            media = int(numeros[2])
                            # print(f"Mínimo: {minimo}ms, Máximo: {maximo}ms, Media: {media}ms")

                if recibidos > 0 and perdidos == 0 and not has_unreachable and not has_timeout:
                    ok = True
                else:
                    ok = False
            except Exception:
                ok = False
                enviados = perdidos = self.config["massive_ping"]["ping_count"]
                recibidos = 0
                # minimo = maximo = media = self.config["general"]["ping_timeout"]
                minimo = maximo = media = 0

            self.ping_result_signal.emit(row, col, ok, enviados, recibidos, perdidos, minimo, maximo, media)
        else:
            print("IP NO válida:", ip)
            pass

    def is_valid_ip(self, ip: str) -> bool:
        # print(type(ip))
        pattern = re.compile(r'^\d{1,3}(?:\.\d{1,3}){3}$')
        if not pattern.match(ip):
            # print(ip, "NO OK")
            return False
        try:
            return all(0 <= int(octet) <= 255 for octet in ip.split('.'))
        except ValueError:
            # print(ip, "NO OK")
            return False

    def calcular_ip(self, posicion: int, vlan: int, id_switch: int, id_puerto: int,
                    mask_d20: int = 28, mask_d21: int = 3) -> str:
        """
        Calcula la IP con la lógica:
        10.0.< ((posicion & 28)/4) + vlan*8 >.< ( (posicion & 3)*64 + id_switch*10 + id_puerto ) >
        
        """
        # print(type(posicion), type(vlan), type(id_switch), type(id_puerto))
        if not str(vlan).isdigit() or not (0 <= vlan <= 31):
            return None
        # Tercer octeto: ((posicion & 28) / 4) + vlan*8
        octeto3 = ((posicion & mask_d20) // 4) + (vlan * 8)

        # Cuarto octeto: ((posicion & 3) * 64) + id_switch*10 + id_puerto
        octeto4 = ((posicion & mask_d21) * 64) + (id_switch * 10) + id_puerto

        # Validación básica de rango
        if not (0 <= octeto3 <= 255):
            raise ValueError(f"El tercer octeto quedó fuera de rango: {octeto3}")
        if not (0 <= octeto4 <= 255):
            raise ValueError(f"El cuarto octeto quedó fuera de rango: {octeto4}")

        return f"10.0.{octeto3}.{octeto4}"

    def extraer_codigo_coche(self, texto):
        """De '891.1 - C4328 - ...' saca 'C4328'."""
        if not isinstance(texto, str):
            return None
        m = re.search(r"C\d{4}[A-Z]?", texto)
        return m.group(0) if m else None

    def cargar_red(self, path_excel, sheet_name_DB= "Train IP Addressing (ECN)", reseved_ip_sheetname = "Reserved Fixed IPs", reserved_esus_ip_sheetname="Coaches Types and Number", sheet_name_DSB= "Train IP Addressing 15 CabCar"):
        # leemos con pandas para manejar datos cómodamente
        if self.project == "DB":
            sheet_name = sheet_name_DB
        elif self.project == "DSB":
            sheet_name = sheet_name_DSB
        df = pd.read_excel(path_excel, sheet_name=sheet_name, header=None, dtype=object)

        nrows, ncols = df.shape

        coach_ranges = []
        found = []
        reserved_ips = []

        for r in range(nrows):
            for c in range(ncols):
                val = df.iat[r, c]
                if isinstance(val, str) and self.extraer_codigo_coche(val):
                    found.append((r, c, self.extraer_codigo_coche(val)))
        
        if self.project == "DB":
            reserved = pd.read_excel(path_excel, sheet_name=reseved_ip_sheetname, header=None, dtype=object)
            reserved_esus = pd.read_excel(path_excel, sheet_name=reserved_esus_ip_sheetname, header=None, dtype=object)
            
            nrows_reserved, ncols_reserved = reserved.shape
            nrows_reserved_esus, ncols_reserved_esus = reserved_esus.shape

            
            for rr in range(nrows_reserved):
                for rc in range(ncols_reserved):
                    if reserved.iat[rr, rc] == "IP address":
                        for ip_row in range(rr + 1, nrows_reserved):
                            ip_cell = reserved.iat[ip_row, rc]
                            if isinstance(ip_cell, str) and ip_cell.strip():
                                reserved_ips.append(ip_cell.strip())
                            else:
                                break  # paro en la primera fila vacía del listado de IPs reservadas
            for rr in range(nrows_reserved_esus):
                for rc in range(ncols_reserved_esus):
                    if reserved_esus.iat[rr, rc] == "ESU ID":
                        for ip_row in range(rr + 2, nrows_reserved_esus):
                                for ip_col in range(rc, ncols_reserved_esus):
                                    ip_cell = reserved_esus.iat[ip_row, ip_col]
                                    if isinstance(ip_cell, str) and ip_cell.strip():
                                        reserved_ips.append(ip_cell.strip())
                                    else:
                                        break  # paro en la primera fila vacía del listado de IPs reservadas        

                
        # print(f"Loaded {len(reserved_ips)} reserved IPs.")
        # print(reserved_ips)

                
        if found:
            # usamos las columnas encontradas como starts y el siguiente start define el end
            cols = sorted({c for (_, c, _) in found})
            for i, sc in enumerate(cols):
                ec = cols[i+1] if i+1 < len(cols) else ncols
                # el código lo tomamos de la primera ocurrencia en esa columna
                code = next(code for (r,c,code) in found if c == sc)
                row = next(r for (r,c,code) in found if c == sc)
                coach_ranges.append((sc, ec, code, row))

            # print(f"Detected {len(coach_ranges)}.")
            # print("Coaches:", ", ".join([code for (_, _, code, _) in coach_ranges]))

        # 3) procesar cada coche encontrado buscando las filas "ID" dentro de su rango de columnas
        tren = {}
        for start_col, end_col, coach_code, coach_row in sorted(coach_ranges, key=lambda x: x[0]): # ordenar por start_col, porque coach_ranges es una tupla. x[0] es start_col.
            coach_dict = {}

            # Buscar filas donde en alguna columna del rango aparece la cabecera "ID"
            header_rows = set()
            for col in range(start_col + 1, end_col):
                for r in range(nrows):
                    cell = df.iat[r, col]
                    if isinstance(cell, str) and cell.strip().upper() == "ID":
                        header_rows.add(r)
            # print(header_rows)
            # Para cada header detectado extraemos puertos empezando en header_row + 2
            for col in range(start_col + 1, end_col):
                for header_row in sorted(header_rows):
                    if self.project == "DB":
                        name_row = header_row + 2 + 1 # nombre de switch (se busca en header_row + 2 + 1)
                    elif self.project == "DSB":
                        name_row = header_row + 2  # nombre de switch (se busca en header_row + 2)
                    if not (isinstance(df.iat[header_row, col], str) and df.iat[header_row, col].strip().upper() == "ID"):
                        continue

                    name_cell = df.iat[name_row, col] if name_row < nrows else None
                    if isinstance(name_cell, str) and name_cell.strip():
                        sw_name = name_cell.strip()
                    else:
                        sw_name = f"SW_{header_row}_{col}"

                    ports = {}
                    # port names están en la columna col+1 (igual que en el código original)
                    r = header_row + 2
                    while r < nrows:
                        port_name = df.iat[r, col + 1] if (col + 1) < ncols else None
                        if not (isinstance(port_name, str) and port_name.strip()):
                            break  # param: paro en la primera fila vacía del listado de puertos
                        port_name = port_name.strip()

                        vlan = df.iat[r, col + 3] if (col + 3) < ncols else None
                        device = df.iat[r, col + 4] if (col + 4) < ncols else None
                        ip = df.iat[r, col + 5] if (col + 5) < ncols else None
                        
                        if isinstance(device, float) and math.isnan(device):
                            device = None


                        ports[port_name] = {
                            "VLAN": int(vlan) if pd.notna(vlan) else None,
                            "Device": device,
                            "IP": ip.strip() if isinstance(ip, str) and ip.strip() in reserved_ips and self.project == "DB" else None
                        }

                        r += 1

                    if ports:
                        coach_dict[sw_name] = ports

            tren[coach_code] = coach_dict

        # print(tren.keys())
        
        return tren

if __name__ == "__main__":
    
    if not QApplication.instance():
        app = QApplication(sys.argv)
        app.setStyle(QStyleFactory.create("Fusion"))
    else:
        app = QApplication.instance()

    window = MainWindow()

    screen = QApplication.primaryScreen()
    max_width = screen.availableGeometry().width()  
    max_height = screen.availableGeometry().height() 
    
    window.move(int((max_width - window.default_width)/2),int((max_height - window.default_height)/2))
    window.show()

    sys.exit(app.exec())
    