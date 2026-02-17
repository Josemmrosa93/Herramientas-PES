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
    QFrame,
    QFormLayout,
    QPushButton,
    QDialog,
    QTextEdit,
    QMenuBar,
    QMenu,
    QStyleFactory,
    QInputDialog,
    QSplitter,
    QListWidget, 
    QStackedWidget,
    QDialogButtonBox,
    QLineEdit,
    QCheckBox,
    QSpinBox,
)
from PySide6.QtGui import (
    QAction,
    QPixmap,
    QPainter,
    QColor,
    QImage,
    QRegion,
    QTransform,
    QBrush,
    QTextCursor,
    QGuiApplication,
)
from PySide6.QtCore import (
    Qt,
    QThread,
    Signal,
    QTimer,
    QPoint,
    QObject
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


APP_VERSION = "1.0.3"
GITHUB_OWNER = "Josemmrosa93"
GITHUB_REPO = "Herramientas-PES"

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "general":{
        "ssh_username": "root",
        "ssh_password": "root",
        "ping_timeout": 200,
        "ssh_timeout": 5,
        "test_timeout": 1000,
        "monitor_interval": 5,
        "reset_pause": 5000,
    },  
    "massive_ping":{
        "ping_count": "1",
        "max_threads": "50",
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
        'BCUCH1_MVB2_DS_30F.bDIMGA_S0',
        'BCUCH2_MVB1_DS_30F.bDIMGA_S0',
        'BCUCH1_MVB2_DS_30F.bDIBA_S2_NOK',
        'BCUCH2_MVB1_DS_30F.bDIBA_S2_NOK'
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
        'BCUB90_MVB1_DS_612.bDIBA_S2_NOK',
        'BCUB95_MVB2_DS_612.bDIBA_S2_NOK',
    ]
        #DICCIONARIO PARA INTERPRETAR LA DIAGNÓSIS
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

    def _flatten_ts_map(self, ts_map: dict) -> tuple[int, dict]: #El guion bajo en el nombre del método es para indicar que es “privado” (convención, no restricción real), es decir, que se usa sólo dentro del método, no es público
        """
        readValues devuelve {ts_ms: {var: value}}
        Nos quedamos con el ts más reciente para devolver (ts_ms, values_dict).
        """
        if not ts_map:
            return 0, {}
        ts_ms = max(ts_map.keys())
        return ts_ms, ts_map[ts_ms] or {}

    def _all_read_error(self, values: dict) -> bool: #El guion bajo en el nombre del método es para indicar que es “privado” (convención, no restricción real), es decir, que se usa sólo dentro del método, no es público
        """
        True si TODAS las variables leídas son Error! (no accesible / sin conexión / timeout).
        """
        if not values:
            return True
        return all(v == isagrafInterface.READ_ERROR for v in values.values())

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

class Worker(QObject):

    on_tsc_data = Signal(str, object, dict)    # endpoint_id, ts_ms, values
    on_tsc_diag_data = Signal(str, object, dict)    # endpoint_id, ts_ms, values
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

        # Desempaquetamos las opciones de diagnóstico habilitados según la configuración. Esto se modificará en función de lo que se quiera mostrar en la UI (checkboxes).
        self.tsc_enabled = diag_enabled.get("TSC")
        self.tsc_diag_enabled = diag_enabled.get("DIAG_TSC")


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
                    self.tsc_diag_enabled = cfg.get("DIAG_TSC")
                    

                    # print(f"Updated Worker config: TSC_enabled={self.tsc_enabled}, DIAG_TSC_enabled={self.tsc_diag_enabled}")

                # ################################# METEMOS UN DIAGNÓSTICO MÍNIMO PARA MANTENER VIVA LA TABLA ###############################

                if self.tsc_enabled or self.tsc_diag_enabled:
                    self._at_least_one_read = True
                else:
                    self._at_least_one_read = False

                ts_ms = 0

                # ################################ LECTURA DE TSC ################################

                if self.tsc_enabled or not self._at_least_one_read:
                    if not self.is_cc:
                        # print("Reading normal TSC vars:", self.tsc_normal_vars)
                        online, ts_ms, tsc_values = self.client.read_vars(self.tsc_normal_vars, wait_time=self.wait_time)
                    else:
                        # print("Reading CC TSC vars:", self.tsc_cc_vars)                        
                        online, ts_ms, tsc_values = self.client.read_vars(self.tsc_cc_vars, wait_time=self.wait_time)


                    if not online:
                        self.status.emit(self.endpoint_id, False, "offline (READ_ERROR)", ts_ms)
                    else:
                        self.status.emit(self.endpoint_id, True, "ok", ts_ms)

                        if ts_ms >= self._last_ts:
                            self._last_ts = ts_ms
                            reformat_tsc_values = {k: self._to_str_value(v) for k, v in (tsc_values or {}).items()}
                            self.on_tsc_data.emit(self.endpoint_id, ts_ms, reformat_tsc_values)

                # ################################ LECTURA DIAG_TSC ################################
                
                if self.tsc_diag_enabled:
                    if self.is_cc:
                        diag_vars_list = list(self.bcu_diag_vars_cc or [])
                    else:
                        diag_vars_list = list(self.tsc_diag_vars or []) + list(self.bcu_diag_vars or [])

                    online, ts_ms, diag_values = self.client.read_vars(diag_vars_list, wait_time=self.wait_time)

                    # Aquí NO suelo machacar status online/offline general si quieres separarlo,
                    # pero puedes emitir status si te interesa.

                    if ts_ms >= self._last_ts:
                        reformat_diag_values = {k: self._to_str_value(v) for k, v in (diag_values or {}).items()}
                        self.on_tsc_diag_data.emit(self.endpoint_id, ts_ms, reformat_diag_values)
        

                ##################################################################################

            except Exception as e:
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

    def on_status(self, endpoint_id, online, msg, ts_ms):
        st = self.tsc_state.get(endpoint_id)
        if st is None:
            return

        online = bool(online)
        if st["online"] != online:
            st["online"] = online
            if not online:
                st["values"] = {}
            self._dirty = True

    def on_tsc_diag_data(self, endpoint_id, ts_ms, values):
        st = self.tsc_diag_state.get(endpoint_id)
        if st is None:
            return
        st["online"] = True
        st["values"] = values or {}
        self._dirty = True

    def _tick(self):
        if not self._dirty:
            return

        snapshot = {
            "coaches": {
                eid: {"online": bool(st["online"]), "values": dict(st["values"])}
                for eid, st in self.tsc_state.items()
            },
            "tsc_diag": {
                eid: {"online": bool(st["online"]), "values": dict(st["values"])}
                for eid, st in self.tsc_diag_state.items()
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
                print(ip, r.returncode == 0)
                return r.returncode == 0
            except Exception:
                return False

        valid_ips = self.ip_list[:self.max_initial_ips]
        scan_list = self.ip_list[self.max_initial_ips:]
        scan_list_vcuch_cc = self.cabcar_VCUCH_ips[self.max_initial_ips:]
        total = max(1, len(scan_list))

        for i, ip in enumerate(scan_list):
            if ping(ip):
                valid_ips.append(ip)
            if ping(scan_list_vcuch_cc[i]):
                valid_ips.append(scan_list_vcuch_cc[i])

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

    def __init__(self, project, endpoint_ids, tsc_vars, project_coach_types, tsc_cc_vars):
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

        # snapshot actual (lo alimenta vars_warehouse -> build_svg_snapshot)
        self.snapshot = {"coaches": {}}

        # tamaño mínimo inicial
        self.setMinimumSize(800, 300)

    def set_snapshot(self, snapshot: dict):
        self.snapshot = snapshot or {"coaches": {}}
        self.render_from_snapshot()

    def render_from_snapshot(self):
        svg = self.generate_svg_from_snapshot()
        self.load(bytearray(svg, encoding="utf-8"))
  
    def generate_svg_from_snapshot(self) -> str:

        coaches_dict = (self.snapshot or {}).get("coaches", {}) or {}

        # Orden estable: el orden de endpoint_ids, pero solo los que existan en snapshot
        coach_ids = [eid for eid in self.endpoint_ids if eid in coaches_dict]
        self.num_coaches = len(coach_ids)

        # Si no hay nada, dibuja un SVG vacío mínimo (alto antiguo)
        if self.num_coaches == 0:
            root = Element("svg", xmlns="http://www.w3.org/2000/svg", width="800", height="300")
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

        # Ajusta el mínimo del widget para que el scroll area lo respete
        self.setMinimumSize(max(800, corrected_svg_width), 300)

        svg_root = Element(
            "svg",
            xmlns="http://www.w3.org/2000/svg",
            width=str(corrected_svg_width),
            height="300"
        )

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

            s60_b1    = g(tsc_data, 25)
            s60_r_b1  = g(tsc_data, 26)
            s62_b1    = g(tsc_data, 27)
            s62_r_b1  = g(tsc_data, 28)
            s256_b1   = g(tsc_data, 29)
            s256_r_b1 = g(tsc_data, 30)

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
                coach = self.normal_coach(label, index, k801, k800, k802, k804,
                                        s60, s60_r, s62, s62_r, s256, s256_r,
                                        self.pmr_pos, fr_riom_sc1, fr_riom_sc1r)

            return coach, True

    def save_as_png(self):

        filename, _ = QFileDialog.getSaveFileName(self, "Guardar como PNG", "", "Archivos PNG (*.png)")
        
        if filename:
            if not filename.endswith('.png'):
                filename += '.png'
            
            scale = 2
            # Ajustar las dimensiones del PNG basadas en el SVG
            new_width = self.width() * scale
            new_height = self.height() * scale
            
            # Crear una imagen con el tamaño ajustado
            image = QImage(new_width, new_height, QImage.Format_ARGB32)
            image.fill(Qt.transparent)  # Rellenar con transparencia
            
            painter = QPainter(image)
    
            # Escalar el contenido del SVG para ajustarlo al nuevo tamaño
            painter.setTransform(QTransform().scale(2, 2))
            self.render(painter, QPoint(0, 0), QRegion(self.rect()))
            painter.end()
        
            # Guardar la imagen como PNG
            try:
                image.save(filename)
                QMessageBox.information(None, "Éxito", f"Imagen guardada correctamente en {filename}")
            except Exception as e:
                QMessageBox.critical(None, "Error", f"No se pudo guardar el archivo: {e}")
            
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

class DiagnosticWindow(QMainWindow):
    closed = Signal()

    def __init__(self, title: str, fixed_w: int, fixed_h: int, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(int(fixed_w), int(fixed_h))

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)

class TSCWindow(DiagnosticWindow):
    def __init__(self, *, project, endpoint_ids, tsc_vars, project_coach_types, tsc_cc_vars,
                 fixed_w: int, fixed_h: int, parent=None): #El asterisco indica que los argumentos siguientes deben ser pasados como palabras clave, es decir (project = x, endpoint_ids = y, etc) y no como argumentos posicionales (x, y, etc)
        super().__init__(title="TSC", fixed_w=fixed_w, fixed_h=fixed_h, parent=parent)

        central = QWidget()
        lay = QVBoxLayout(central)
        lay.setContentsMargins(6, 6, 6, 6)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.tsc = TSCGenerator(
            project=project,
            endpoint_ids=endpoint_ids,
            tsc_vars=tsc_vars,
            project_coach_types=project_coach_types,
            tsc_cc_vars=tsc_cc_vars,
        )

        self.scroll.setWidget(self.tsc)
        lay.addWidget(self.scroll)
        self.setCentralWidget(central)

    def set_snapshot(self, snapshot: dict):
        self.tsc.set_snapshot(snapshot)

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
            "BCU_DIAG_VARS_CC": self.TCMS_vars.BCU_DIAGNOSIS_CC
        }

        self.diag_enabled = {
            "TSC": False,
            "DIAG_TSC": False,
        }
                    
        self.default_width = 800
        self.default_height = 434

        self.tsc_window = None

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

        self.massive_ping_action=QAction("Comprobar estado de comunicación de equipos", self)
        self.massive_ping_action.triggered.connect(self.massive_ping)
        self.massive_ping_action.setEnabled(False)
        
        diag_menu.addActions([self.check_TSC_action, self.massive_ping_action])
        
        ######### MENÚ EXPORTAR ##########
        
        export_menu = self.menu_bar.addMenu("Exportar")
        
        self.export_TSC_action=QAction("Exportar imagen TSC", self)
        self.export_TSC_action.setEnabled(False)
        # self.export_TSC_action.triggered.connect(self.tsc.save_as_png)
        
        export_menu.addActions([self.export_TSC_action])

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
            self.ssh_timeout = QSpinBox()
            self.ssh_timeout.setRange(4, 15)
            self.ssh_timeout.setSuffix(" s")
            self.test_refresh = QSpinBox()
            self.test_refresh.setRange(1000, 10001)
            self.test_refresh.setSuffix(" ms")
            self.monitor_interval = QSpinBox()
            self.monitor_interval.setRange(2, 10)
            self.monitor_interval.setSuffix(" s")
            self.reset_pause = QSpinBox()
            self.reset_pause.setRange(1000,10001)
            self.reset_pause.setSuffix(" ms")
            # self.chk_minimizado = QCheckBox("Iniciar Minimizado")

            layout.addRow("Timeout para pings:", self.ping_timeout)
            layout.addRow("Timeout para conexión SSH:", self.ssh_timeout)
            layout.addRow("Tiempo de refresco de datos en representación", self.test_refresh)
            layout.addRow("Tiempo de intento de recuperación de conexiones caídas", self.monitor_interval)
            layout.addRow("Tiempo de pausa entre órdenes de reseteo de errores", self.reset_pause)
            # layout.addRow("", self.chk_minimizado)

            return w
       
        def create_network_page():
            
            w = QWidget()
            layout = QFormLayout(w)

            self.spin_ping_count = QSpinBox()
            self.spin_ping_count.setRange(1,201)
            self.spin_ping_count.setSuffix(" paquetes")

            self.auto_export = QCheckBox("Auto exportar informe de resultados al escanear la red")

            self.max_threads = QSpinBox()
            self.max_threads.setRange(1,21)
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
            self.ssh_timeout.setValue(int(g.get("ssh_timeout")))
            self.test_refresh.setValue(int(g.get("test_timeout")))
            self.monitor_interval.setValue(int(g.get("monitor_interval")))
            self.reset_pause.setValue(int(g.get("reset_pause")))

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
            g["ssh_timeout"]      = self.ssh_timeout.value()
            g["test_timeout"]     = self.test_refresh.value()
            g["monitor_interval"] = self.monitor_interval.value()
            g["reset_pause"]      = self.reset_pause.value()

            # ----- massive_ping -----
            n["ping_count"] = self.spin_ping_count.value()
            # print(self.spin_ping_count.value())
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
    
        self.max_initial_ips = 20 if self.project == "DB" else 15 if self.project == "DSB" else 1
        
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
        self.massive_ping_action.setEnabled(True)

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
            w.status.connect(self.vars_warehouse.on_status)

            self.vars_threads[eid] = th
            self.vars_workers[eid] = w
            th.start()

    def on_vars_snapshot(self, snapshot: dict):
        # 1) tabla siempre
        self.update_table_from_snapshot(snapshot)

        # 2) si la ventana TSC existe, actualizamos
        if self.check_TSC_action.isChecked() and self.tsc_window is not None:
            svg_snapshot = self.build_svg_snapshot(snapshot)
            self.tsc_window.set_snapshot(svg_snapshot)

    def update_table_from_snapshot(self, snapshot: dict):
        coaches = snapshot.get("coaches", {})
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
                    txt = self.TCMS_vars.COACH_TYPES_DSB.get(n, txt)
                else:
                    txt = self.TCMS_vars.COACH_TYPES_DB.get(n, txt)
                    
            type_item = self.table.item(1, col)
            if type_item is None:
                type_item = QTableWidgetItem("")
                type_item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(1, col, type_item)
            type_item.setText(txt)

    def build_svg_snapshot(self, endpoint_snapshot: dict) -> dict:

        # print("Construyendo snapshot para SVG a partir de:", endpoint_snapshot["coaches"]["EP1"])
        ep = endpoint_snapshot.get("coaches", {})

        # Si no es DB o no hay doble IP, no hacemos merge
        if self.project != "DB" or len(self.endpoint_ids) < 2:
            return {"coaches": ep}

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
        return {"coaches": out}

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
                    "coaches": {
                        eid: {"online": bool(st.get("online", False)), "values": dict(st.get("values", {}) or {})}
                        for eid, st in self.vars_warehouse.tsc_state.items()
                    }
                }
                svg_snapshot = self.build_svg_snapshot(snapshot)
                self.tsc_window.set_snapshot(svg_snapshot)

            if hasattr(self, "export_TSC_action") and self.export_TSC_action is not None:
                self.export_TSC_action.setEnabled(True)

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

            if hasattr(self, "export_TSC_action") and self.export_TSC_action is not None:
                self.export_TSC_action.setEnabled(False)

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
        self.massive_ping_action.setEnabled(True)

    def reset_TAR_TEMP_failures(self):
        """Función para reiniciar fallos temporales de TAR en los VCUs del tren."""

        # Detener temporizador si está corriendo
        if hasattr(self, "timer") and self.timer is not None:
            # self.timer.stop()
            self.stop_timer()

        # Verificar que hay coches en el tren
        if not self.trainset_coaches:
            print("Error: No hay coches en el conjunto de trenes.")
            return

        # Lista de variables a escribir en los VCUs
        VARS_LIST = [
            "VCUCH_MVB1_DS_64.MaintenaceMode", 
            "VCUCH_MVB2_DS_64.MaintenaceMode",
            "VCUCH_MVB2_DS_64.ReleaseFailureRunInstabCH",
            "VCUCH_MVB1_DS_64.ReleaseFailureRunInstabCH"
            ]

        # Si el modo prueba está activado, solo se usa el primer coche
        coches_a_usar = self.trainset_coaches
        

        # Crear interfaz de progreso
        self.progress_dialog = QDialog()
        self.progress_dialog.setWindowTitle("Escribiendo en VCUs")
        self.progress_dialog.setGeometry(300, 300, 600, 300)

        dialog_layout = QVBoxLayout()
        self.progress_label = QTextEdit()
        self.progress_label.setReadOnly(True)
        modo_texto = ""
        self.progress_label.append(f"Lanzando comandos a las VCU´s, por favor espere...{modo_texto}\n")
        dialog_layout.addWidget(self.progress_label)
        self.progress_dialog.setLayout(dialog_layout)
        self.progress_dialog.show()

        def on_progress_dialog_closed():
            """Reinicia el timer cuando se cierra la ventana."""
            if hasattr(self, "timer") and self.timer is not None:
                self.timer.start()

        # Conectar el evento de cierre de la ventana al reinicio del timer
        self.progress_dialog.finished.connect(on_progress_dialog_closed)

        def ejecutar_comandos(valores):
            """Ejecuta los comandos en los VCUs con los valores dados y llama al callback si se proporciona."""
            for i in range(len(valores)):
                with ThreadPoolExecutor(max_workers=len(coches_a_usar)) as executor:
                    futures = {executor.submit(vcu.SSH_write_lock, [VARS_LIST[i]], [valores[i]], False): vcu for vcu in coches_a_usar}

                    for future in as_completed(futures):
                        coach = futures[future]
                        try:
                            ip, statuses = future.result()
                            coach_number = self.trainset_coaches.index(coach) + 1  

                            self.progress_label.append(f"➡ Variable {VARS_LIST[i]} a {valores[i]} en coche {coach_number} ({ip}):")
                            for status in statuses:
                                self.progress_label.append(f"    - {status}")

                            self.progress_label.append("")
                            self.progress_label.moveCursor(QTextCursor.End)

                        except Exception as e:
                            coach_number = self.trainset_coaches.index(coach) + 1
                            error_text = f"❌ Error en Coche {coach_number}: {e}"
                            print(error_text)
                            self.progress_label.append(f"{error_text}\n")
                            self.progress_label.moveCursor(QTextCursor.End)
                
        ejecutar_comandos([1,1,1,1])
        ejecutar_comandos([0,0,0,0])
        # QTimer.singleShot(RESET_PAUSE, ejecutar_comandos([0,0,0,0]))

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

        if self.project == "DB":
            num_coaches = len(self.trainset_coaches) - 1  # Último coche es cabcar
        elif self.project == "DSB":
            num_coaches = len(self.trainset_coaches)

        self.massive_ping_table.setColumnCount(num_coaches * COLS_PER_COACH)  # 5 columnas por coche: PUERTO, VLAN, DEVICE, IP
        self.massive_ping_table.setRowCount(count)

        for col in range(num_coaches):
            esu_id = 0 # Reiniciar ID de ESU para cada coche
            print_row = 1  # Reiniciar fila de impresión para cada coche
            tipo = self.TCMS_vars.COACH_TYPES_DSB[int(self.coach_types[col])] if self.project == "DSB" else self.TCMS_vars.COACH_TYPES_DB[int(self.coach_types[col])]
            
            if tipo == "C4302P":
                tipo = "C4302C"
            
            c0 = 5 * col  # desplazamiento de columnas para este coche (bloque de 4 columnas)

            # ---- Fila 0: título del coche (fusionado 4 columnas) ----
            coach_title = QTableWidgetItem(f"Coche {col+1} — {tipo}")
            coach_title.setTextAlignment(Qt.AlignCenter)
            coach_title.setBackground(QBrush(QColor(100, 100, 100)))
            coach_title_font = coach_title.font(); coach_title_font.setBold(True); coach_title.setFont(coach_title_font)
            self.massive_ping_table.setItem(0, c0, coach_title)
            self.massive_ping_table.setSpan(0, c0, 1, COLS_PER_COACH)  # fusiona columnas 0..3 del bloque

            print_row = 1

            # Cargar definición de red a partir del TIPO
            esus_dict = self.red_eth.get(tipo, {})  # dict de ESUs para ese tipo
            # Itera ESUs (orden natural del dict; si quieres orden predecible, usa: for esu_name in sorted(esus_dict))
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
                        self.massive_ping_table.setItem(print_row, c0 + 4, QTableWidgetItem(str(self.trainset_coaches[col].ip)))
                    else: 
                        self.massive_ping_table.setItem(print_row, c0 + 4, QTableWidgetItem(self.calcular_ip(col + 1, info.get("VLAN", 0), esu_id, int(port_id)) if info.get("IP", "") is None else info.get("IP", ""))) #col+1 porque la posición empieza en 1
                    # print(str(info.get("Device", "")), col, info.get("VLAN", 0), esu_id, int(port_id))
                    print_row += 1
                    port_id += 1
                
                esu_id += 1 # Incrementar ID de ESU
                if self.project == "DSB" and esu_id == 2:
                    esu_id = 4  # Saltar ID 3 en DSB


        self.massive_ping_table.setItem(32, 4, QTableWidgetItem(str("192.168.1.139")))

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
            # print("IP NO válida:", ip)
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
    window.show()
    sys.exit(app.exec())
    