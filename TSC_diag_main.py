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
    QTabWidget,
    QPushButton,
    QDialog,
    QTextEdit,
    QMenuBar,
    QMenu,
    QStyleFactory,
    QInputDialog
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
    QTextCursor
)
from PySide6.QtCore import (
    Qt,
    QThread,
    Signal,
    QTimer,
    QPoint
)
from xml.etree.ElementTree import ( 
    Element,
    SubElement,
    tostring
)
from PySide6.QtSvgWidgets import QSvgWidget
import subprocess
import paramiko
import re
import sys
import os
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Event
from numpy import array_split, concatenate
import time
import xlsxwriter
from threading import Event
import logging

maintenance_mode = 0

PING_TIMEOUT = 100  # Tiempo de espera para el ping en milisegundos.
SSH_TIMEOUT = 5.0  # Tiempo de espera para la conexión SSH, 5.0 para operación en tren.
TEST_TIMEOUT = 4000 # Tiempo de refresco de los datos de diagnóstico, 4000 para operación en tren.
MONITOR_INTERVAL = 10 # Tiempo de refresco para la evaluación de las conexiones.
RESET_PAUSE = 5000 # Tiempo de pausa entre órdenes del reseteo de fallos. 

MODO_PRUEBA = False

PREDEFINED_DSB = ['11', '3', '3', '5', '8', '9', '8', '9', '8', '9', '8', '9', '8', '9', '11']
PREDEFINED_DB_13 = ['11', '9', '8', '10', '8', '9', '7', '6', '5', '4', '3', '3', '2', '2']

class TCMS_vars:
    def __init__(self):
        
        #TIPOS DE COCHE EN FUNCIÓN DEL PROYECTO
        self.COACH_TYPES_DB={1: "L9215", 2: "C4340", 3: "C4301", 4: "C4306", 5: "C4314", 6: "C4315", 7: "C4322", 8: "C4302S", 9: "C4302P", 10: "C4302C", 11: "C4328"}
        self.COACH_TYPES_DSB={1: "1", 2: "2", 3: "C4701", 4: "4", 5: "C4714", 6: "6", 7: "7", 8: "C4702S", 9: "C4702P", 10: "10", 11: "C4728"}
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
        'RIOMSC2r_MVB2_DS_2FB_Failure_Rate' #Tasa de fallos RIOM 2 Redundante (sólo PMR)
        ]
        self.TSC_COACH_VARS_DB = [
        'iVCUCH_IO_DS_A602_S45_X1.DIu_RiomS1isOK',
        'iVCUCH_IO_DS_A602_S45_X1.DIu_SafCon1Loop',
        'iVCUCH_IO_DS_A602_S45_X1.DIu_SafCon2Loop',
        'iVCUCH_IO_DS_A602_S42_X1.DIu_RiomS1isOKB1',
        'iVCUCH_IO_DS_A602_S43_X1.DIu_SafCon1LoopB1',
        '_INPUT_LAYER.BRK_TST_F_Emg_Brk.iIO_DS_A602_S43_X1_DIu_SafCon2Loop_B1',
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
        'RIOMSC2r_MVB2_DS_2FC.TempUnavailBear4'
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
        'BCUCH2_MVB1_DS_311.sDiagnosis23_b2'
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
    ]
        #DICCIONARIO PARA INTERPRETAR LA DIAGNÓSIS
        self.BCU_DIAGNOSIS_DICT = {
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

class ConnectionMonitorThread(QThread):
    connection_status_updated = Signal(str, str)
    
    def __init__(self, vcu_list, check_interval=MONITOR_INTERVAL):
        super().__init__()
        self.vcu_list = vcu_list
        self.check_interval = check_interval
        self.max_workers = len(self.vcu_list)
        self.stop_event = Event()
    
    def run(self):
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # print("FUNCIONANDO")
            while not self.stop_event.is_set():
                future_to_vcu = {executor.submit(self.check_VCU_status, vcu): vcu for vcu in self.vcu_list}
                
                for future in as_completed(future_to_vcu):
                    
                    vcu = future_to_vcu[future]
                    try:
                        status = future.result()
                        # print(vcu.ip, status)
                        self.connection_status_updated.emit(vcu.ip, status)
                        
                    except Exception as e:
                        pass
                        # logger.error(f"Error checking VCU status for {vcu.ip}: {e}")
                
                # Esperar el intervalo de verificación o hasta que se detenga el hilo
                if not self.stop_event.wait(self.check_interval):
                    continue
                else:
                    break
  
    def stop(self):
        # print("PARANDO")
        self.stop_event.set()

    def check_VCU_status(self, vcu):

        if not vcu.SSH_alive():
            status = vcu.reconnect_SSH()
            return status
    
        return "success"
        
class VCU:
    def __init__(self, ip):
        self.ip = ip
        self.USERNAME = "root"
        self.PASSWORD = "root"
        self.READ_COMMAND = "isacmd -r "
        self.WRITE_N_LOCK_COMMAND = "isacmd -wl"
        self.WRITE_N_RELEASE_COMMAND = "isacmd -wr"
        self.WRITE_COMMAND = "isacmd -w"
        self.client = None

    def ping_test(self):
        start_time = time.time()
        try:
            result = subprocess.run(
                ['ping', '-w', str(PING_TIMEOUT), '-n', '1', self.ip],
                stdout=subprocess.DEVNULL,
                shell=True
            )
            ping_time = time.time() - start_time
            # logger.debug(f"Ping time for {self.ip}: {ping_time:.4f} seconds")
            return result.returncode == 0
        except Exception as e:
            # logger.error(f"Ping failed for {self.ip}: {e}")
            return False

    def link_SSH(self):

        try:
            if not self.client:
                self.client = paramiko.SSHClient()
                self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(self.ip, username=self.USERNAME, password=self.PASSWORD, timeout=SSH_TIMEOUT)
            self.connection_status = "success"
            return self.connection_status
        except Exception as e:
            self.client = None
            self.connection_status = "ping_only" if self.ping_test() else "failure"
            # print(f"[{self.ip}] SSH failed: {e}")  # agrega log mínimo
            return self.connection_status

    def close_SSH(self):
        if self.client is not None:
            self.client.close()

    def reconnect_SSH(self):
        try:
            if self.client is not None:
                self.close_SSH()
                self.client = None

            status = self.link_SSH()
            self.connection_status = status  # sincroniza estado
            return status
        except Exception as e:
            self.connection_status = "failure"
            # print(f"[{self.ip}] Reconnect failed: {e}")
            return "failure"

    def SSH_alive(self):
        try:
            if self.client is None:
                return False

            # Esto puede devolver True incluso si el socket ya no sirve
            transport = self.client.get_transport()
            if transport is None or not transport.is_active():
                return False

            # Ahora tratamos de ejecutar un comando trivial
            stdin, stdout, stderr = self.client.exec_command("echo ok", timeout=0.5)
            output = stdout.read().decode().strip()

            return "ok" in output

        except Exception as e:
            # print(f"SSH_alive ERROR on {self.ip}: {e}")
            return False

    def SSH_read(self, VARS_LIST):
        VARS_NUM = len(VARS_LIST)
        if self.client is None:
            if VARS_NUM == 1:
                return "Not Client"
            else:
                return ["Not Client"] * VARS_NUM
        try:
            stdin, stdout, stderr = self.client.exec_command(self.READ_COMMAND + " ".join(VARS_LIST))
            output = stdout.read().decode()
            pattern = r'(\w+):\s*(\d+)\s*\((0x[0-9A-Fa-f]+)\)'
            matches = re.findall(pattern, output)
            if matches:
                values = [dec_val for var, dec_val, hex_val in matches]
            else:
                print(output)
                values = ["N/A"] * VARS_NUM
            
            if VARS_NUM == 1:
                return values[0]
            else:    
                return values[:VARS_NUM]
        except Exception:
            if VARS_NUM == 1:
                return "Not SSH"
            else:
                return ["Not SSH"] * VARS_NUM

    def SSH_write_lock(self, VARS_LIST, VALUES_LIST, VERIFY_FLAG):
        VARS_NUM = len(VARS_LIST)
        print(VARS_LIST)
        if self.client is None:
            return self.ip, ["Comms.Error"] * VARS_NUM
        if len(VARS_LIST) != len(VALUES_LIST):
            return self.ip, "Error: Variable and Value length mismatch"
        try:
            command = self.WRITE_N_LOCK_COMMAND + " " + " ".join(f"{var}={val}" for var, val in zip(VARS_LIST, VALUES_LIST))
            print(self.WRITE_N_LOCK_COMMAND + " " + " ".join(f"{var}={val}" for var, val in zip(VARS_LIST, VALUES_LIST)))
            stdin, stdout, stderr = self.client.exec_command(command)
            errors = stderr.read().decode()
            if errors:
                return self.ip, [f"Error: {errors.strip()}"] * VARS_NUM
            if VERIFY_FLAG:
                _, read_values = self.SSH_read(VARS_LIST)
                return self.ip, ["OK" if str(read_val) == str(write_val) else "Mismatch"
                                 for read_val, write_val in zip(read_values, VALUES_LIST)]
            else:
                return self.ip, ["OK"] * VARS_NUM
        except Exception as e:
            return self.ip, [f"Error: {str(e)}"] * VARS_NUM

    def SSH_release(self, VARS_LIST):
        VARS_NUM = len(VARS_LIST)
        if self.client is None:
            return self.ip, ["Comms.Error"] * VARS_NUM
        try:
            command = self.WRITE_N_RELEASE_COMMAND + " " + " ".join(VARS_LIST)
            stdin, stdout, stderr = self.client.exec_command(command)
            errors = stderr.read().decode()
            if errors:
                return self.ip, [f"Error: {errors.strip()}"] * VARS_NUM
            return self.ip, ["OK"] * VARS_NUM
        except Exception as e:
            return self.ip, [f"Error: {str(e)}"] * VARS_NUM

class ScanThread(QThread):
    
    scan_progress = Signal(int, int)
    scan_completed = Signal(list)

    def __init__(self, ip_list, max_initial_ips, project, cabcar_ips):
        super().__init__()
        self.ip_list = ip_list
        self.max_initial_ips = max_initial_ips
        self.project = project
        self.cabcar_ips = cabcar_ips

    def run(self):

        valid_ips = self.ip_list[:self.max_initial_ips]
        
        for i, ip in enumerate(self.ip_list[self.max_initial_ips:]):
            vcu = VCU(ip)
            if vcu.ping_test():
                valid_ips.append(ip)
            progress= ((i+1)*100)//len(self.ip_list[self.max_initial_ips:])
            coach_number=len(valid_ips)
            self.scan_progress.emit(progress, coach_number)
        
        if self.project == "DB":
            # valid_ips[-1] = self.cabcar_ips[len(valid_ips)-1]
            valid_ips.insert(len(valid_ips) - 1, self.cabcar_ips[len(valid_ips) - 1])

        self.scan_completed.emit(valid_ips)

class TSCGenerator(QSvgWidget):
    
    def __init__(self, vcu_list, coach_types, tsc_vars, project_coach_types, tsc_cc_vars):
        
        super().__init__()
        
        self.vcu_list = vcu_list
        self.coaches_type = coach_types
        self.num_coaches = len(self.vcu_list)
        self.tsc_vars = tsc_vars
        self.tsc_cc_vars = tsc_cc_vars

        print(f"Número de coches: {self.num_coaches}")
        
        self.project_coach_types = project_coach_types

        try:
            self.pmr_index = self.coaches_type.index('5')
        except:
            self.pmr_index = None

    def report_tsc_diag(self, vcu, tsc_diag_vars, BCU_diag_vars, BCU_diag_vars_cc):

        if maintenance_mode == 1: 
            tsc_diagnosis=list(map(str,random.choices([0, 1], k=len(tsc_diag_vars)))) # Crea una lista de valores aleatorios en formato str
            BCU_diagnosis=list(map(str,random.choices([0, 1], k=len(BCU_diag_vars)))) # Crea una lista de valores aleatorios en formato str
            BCU_diagnosis_cc=list(map(str,random.choices([0, 1], k=len(BCU_diag_vars_cc)))) # Crea una lista de valores aleatorios en formato str
     
            parts = array_split(BCU_diagnosis, 5)
            parts_cc = array_split(BCU_diagnosis_cc, 10)
            BCU_diagnosis_1 = parts[0]
            BCU_diagnosis_2 = parts[1]
            BCU_diagnosis_3 = parts[2]
            BCU_diagnosis_4 = parts[3]
            BCU_diagnosis_5 = parts[4]      

            BCU_diagnosis_cc_1 = parts[0]
            BCU_diagnosis_cc_2 = parts[1]
            BCU_diagnosis_cc_3 = parts[2]
            BCU_diagnosis_cc_4 = parts[3]
            BCU_diagnosis_cc_5 = parts[4]      
            BCU_diagnosis_cc_6 = parts[5]
            BCU_diagnosis_cc_7 = parts[6]
            BCU_diagnosis_cc_8 = parts[7]
            BCU_diagnosis_cc_9 = parts[8]
            BCU_diagnosis_cc_10 = parts[9]      

            return tsc_diagnosis, BCU_diagnosis_1, BCU_diagnosis_2, BCU_diagnosis_3, BCU_diagnosis_4, BCU_diagnosis_5, BCU_diagnosis_cc_1, BCU_diagnosis_cc_2, BCU_diagnosis_cc_3, BCU_diagnosis_cc_4, BCU_diagnosis_cc_5, BCU_diagnosis_cc_6, BCU_diagnosis_cc_7, BCU_diagnosis_cc_8, BCU_diagnosis_cc_9, BCU_diagnosis_cc_10 

        tsc_diagnosis = vcu.SSH_read(tsc_diag_vars)

        parts = array_split(BCU_diag_vars, 5)
        parts_cc = array_split(BCU_diag_vars_cc,10)

        BCU_diagnosis_1 = vcu.SSH_read(parts[0])
        BCU_diagnosis_2 = vcu.SSH_read(parts[1])
        BCU_diagnosis_3 = vcu.SSH_read(parts[2])
        BCU_diagnosis_4 = vcu.SSH_read(parts[3])
        BCU_diagnosis_5 = vcu.SSH_read(parts[4])

        BCU_diagnosis_cc_1 = vcu.SSH_read(parts_cc[0])
        BCU_diagnosis_cc_2 = vcu.SSH_read(parts_cc[1])
        BCU_diagnosis_cc_3 = vcu.SSH_read(parts_cc[2])
        BCU_diagnosis_cc_4 = vcu.SSH_read(parts_cc[3])
        BCU_diagnosis_cc_5 = vcu.SSH_read(parts_cc[4])
        BCU_diagnosis_cc_6 = vcu.SSH_read(parts_cc[5])
        BCU_diagnosis_cc_7 = vcu.SSH_read(parts_cc[6])
        BCU_diagnosis_cc_8 = vcu.SSH_read(parts_cc[7])
        BCU_diagnosis_cc_9 = vcu.SSH_read(parts_cc[8])
        BCU_diagnosis_cc_10 = vcu.SSH_read(parts_cc[9])

        
        return tsc_diagnosis, BCU_diagnosis_1, BCU_diagnosis_2, BCU_diagnosis_3, BCU_diagnosis_4, BCU_diagnosis_5, BCU_diagnosis_cc_1, BCU_diagnosis_cc_2, BCU_diagnosis_cc_3, BCU_diagnosis_cc_4, BCU_diagnosis_cc_5, BCU_diagnosis_cc_6, BCU_diagnosis_cc_7, BCU_diagnosis_cc_8, BCU_diagnosis_cc_9, BCU_diagnosis_cc_10 
    
        # return tsc_diagnosis, BCU_diagnosis_1, BCU_diagnosis_2, BCU_diagnosis_3, BCU_diagnosis_4, BCU_diagnosis_5 
    
    def generate_svg(self, project):

        self.project = project

        svg_width = self.num_coaches * 100

        if self.project == "DSB":
            try:
                if self.coaches_type[self.coaches_type.index('5')] is not None:
                    svg_width += 250
            except:
                pass
        if self.project == "DB":
            try:
                if self.coaches_type[self.coaches_type.index('5')] is not None:
                    svg_width += 100
                if self.coaches_type[self.coaches_type.index('2')] is not None:
                    svg_width += 645
            except:
                pass

        svg_root = Element("svg", xmlns="http://www.w3.org/2000/svg", width=str(svg_width), height="300")

        print("TSC Refresh")

        with ThreadPoolExecutor(max_workers=self.num_coaches) as executor:
            futures = {executor.submit(self.process_coach, self.vcu_list[i], self.coaches_type[i], self.tsc_vars, self.project_coach_types, self.tsc_cc_vars): i for i in range(self.num_coaches)}
            for future in as_completed(futures):
                index = futures[future]  # Obtener el índice del coche
                
                try:

                    coach = future.result()  # Obtener el elemento SVG del coche
                    if coach is not None: 
                        x_pos = index * 100

                        if self.project == "DSB":
                        # Aplicar transform para posicionar el coche en el svg
                            try:
                                if index > self.coaches_type.index('5'):
                                    x_pos+=250
                            except:
                                pass

                        if self.project == "DB":
                        # Aplicar transform para posicionar el coche en el svg
                            try:
                                if index > self.coaches_type.index('5'):
                                    x_pos+=100
                            except:
                                pass

                        coach.set("transform", f"translate({x_pos}, 0)")
                        svg_root.append(coach)
                except Exception as e:
                    print(f"Error al procesar el coche {index + 1}: {e}")

        svg_string = tostring(svg_root, encoding = "unicode")
        
        self.svg_widget = QSvgWidget()
        self.svg_widget.load(bytearray(svg_string, encoding="utf-8"))

        self.svg_widget.setMinimumSize(self.num_coaches * 100, 125)

        if self.project == "DSB":
            try:
                if self.coaches_type[self.coaches_type.index('5')] is not None:
                    self.svg_widget.setMinimumSize(svg_width, 125)
            except:
                pass
        if self.project == "DB":
            try:
                if self.coaches_type[self.coaches_type.index('5')] is not None:
                    self.svg_widget.setMinimumSize(svg_width, 125)
            except:
                pass

        return self.svg_widget
        
    def save_as_png(self, timer):
        timer.stop()
        filename, _ = QFileDialog.getSaveFileName(self.svg_widget, "Guardar como PNG", "", "Archivos PNG (*.png)")
        
        if filename:
            if not filename.endswith('.png'):
                filename += '.png'
            
            
            scale = 2
            # Ajustar las dimensiones del PNG basadas en el SVG
            new_width = self.svg_widget.width() * scale
            new_height = self.svg_widget.height() * scale
            
            # Crear una imagen con el tamaño ajustado
            image = QImage(new_width, new_height, QImage.Format_ARGB32)
            image.fill(Qt.transparent)  # Rellenar con transparencia
            
            painter = QPainter(image)
    
            # Escalar el contenido del SVG para ajustarlo al nuevo tamaño
            painter.setTransform(QTransform().scale(2, 2))
            self.svg_widget.render(painter, QPoint(0, 0), QRegion(self.svg_widget.rect()))
            painter.end()
        
            # Guardar la imagen como PNG
            try:
                image.save(filename)
                QMessageBox.information(None, "Éxito", f"Imagen guardada correctamente en {filename}")
            except Exception as e:
                QMessageBox.critical(None, "Error", f"No se pudo guardar el archivo: {e}")
            
            timer.start()

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
        if int(fr_riom_sc1)>199:
            SubElement(coach, "text", x="50", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "red"}).text = "RIOM SC APAGADA"
        elif int(fr_riom_sc1r)>199:
            SubElement(coach, "text", x="50", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "red"}).text = "RIOM SCr APAGADA"
        elif k800_state and k802_state and not k801_state:
            SubElement(coach, "text", x="50", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "green"}).text = "CERRADO POR REDUNDANTE"
        elif k801_state and not k800_state and k802_state:
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
        
        if coach_pos<pmr_index and pmr_index is not None:
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
            
        elif coach_pos>pmr_index and pmr_index is not None:
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
        if int(fr_riom_sc1)>199:
            SubElement(coach, "text", x="50", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "red"}).text = "RIOM SC APAGADA"
        elif int(fr_riom_sc1r)>199:
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

    def pmr_dsb1(self, coach_name, coach_pos, k801_state, k800_state, k802_state, k810_state, k811_state, k812_state, sifa1_state, sifa2_state, sifa1_forzed, sifa2_forzed, k804_state, k814_state, k753_state, s25_state, s60, s60_r, s62, s62_r, s256, s256_r, s255, s255_r, fr_riom_sc1, fr_riom_sc1r, fr_riom_sc2, fr_riom_sc2r):
        
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
        if int(fr_riom_sc1)>199:
            SubElement(coach, "text", x="200", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "red"}).text = "RIOM SC APAGADA"     
        elif int(fr_riom_sc1r)>199:
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

        if s256 != s256_r:
            SubElement(coach, "text", x="72", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "yellow"}).text = "Error"
        elif s256 == "0":
            SubElement(coach, "text", x="72", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "green"}).text = "Off"
        else:
            SubElement(coach, "text", x="72", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "red"}).text = "Activo"
        
        SubElement(coach, "rect", x="-300", y="195", width="442", height="120", fill=bypass_backcolor, opacity="0.15")
        SubElement(coach, "rect", x="142", y="230", width="75", height="100", fill=bypass_backcolor, opacity="0.15")
        SubElement(coach, "rect", x="217", y="195", width="2000", height="120", fill=bypass_backcolor, opacity="0.15")
        
        p810=SubElement(coach, "g", transform="translate(-265, 250)")
        p810.append(self.create_led(bypass_state,0, 15, "P810"))

        p810=SubElement(coach, "g", transform="translate(1415, 250)")
        p810.append(self.create_led(bypass_state,0, 15, "P810"))
        
        return coach

    def pmr_db_dsb2(self, coach_name, coach_pos, k801_state, k800_state, k802_state, k810_state, k811_state, k812_state, k804_state, k814_state, s60, s60_r, s62, s62_r, s256, s256_r):
        
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
        if k800_state and k802_state and not k801_state:
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
        if k810_state and k812_state and not k811_state:
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
                        

        SubElement(coach, "text", x="55", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9"}).text = "S60:"
        SubElement(coach, "text", x="55", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9"}).text = "S62:"
        # SubElement(coach, "text", x="100", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9"}).text = "S255:"
        SubElement(coach, "text", x="100", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9"}).text = "S256:"

        if s60 != s60_r:
            SubElement(coach, "text", x="72", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "yellow"}).text = "Error"
        elif s60 == "0":
            SubElement(coach, "text", x="72", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9",  "fill": "green"}).text = "Off"
        else:
            SubElement(coach, "text", x="72", y="176",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "red"}).text = "Activo"

        if s62 != s62_r:
            SubElement(coach, "text", x="72", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "yellow"}).text = "Error"
        elif s62 == "0":
            SubElement(coach, "text", x="72", y="188",**{"text-anchor": "right","font-sTtyle": "italic","font-size": "9", "fill": "green"}).text = "Off"
        else:
            SubElement(coach, "text", x="72", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "red"}).text = "Activo"

        if s256 != s256_r:
            SubElement(coach, "text", x="122", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "yellow"}).text = "Error"
        elif s256 == "0":
            SubElement(coach, "text", x="122", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "green"}).text = "Off"
        else:
            SubElement(coach, "text", x="122", y="188",**{"text-anchor": "right","font-style": "italic","font-size": "9", "fill": "red"}).text = "Activo"

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

    def cabcar(self, coach_name, coach_pos, k801_state, k800_state, k802_state, k804_state, s60, s60_r, s62, s62_r, s255, s255_r, s256, s256_r, s8, s8_r, s6, s6_r, s10, k1, k80, k81, k82, k83, sifa1_cond, sifa2_cond, s700, s701, s702, s703, s704, k700, k701, k710, k711, k708, k709, k731, k732, k740, k741, s25, s25_r, k753):

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
        if k800_state and k802_state and not k801_state:
            SubElement(coach, "text", x="50", y="75",**{"text-anchor": "middle","font-style": "italic","font-size": "6.5", "fill": "green"}).text = "CERRADO POR REDUNDANTE"
        elif k801_state and not k800_state and k802_state:
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
        s703_contact1.append(self.create_contact_svg(int(s701), label="S703"))

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
        sifa_1.append(self.create_sifa(not int(k82), int(sifa1_cond),0,"SIFA 1"))

        sifa_2=SubElement(coach, "g", transform="translate(675, 40)")
        sifa_2.append(self.create_sifa(not int(k83), int(sifa2_cond),0, "SIFA 2"))
        
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
            bypass_color = "red"
        elif int(k753) == 0:
            bypass_color = "green"

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

    def process_coach(self, vcu, coach_type, tsc_vars, project_coach_types, tsc_cc_vars):

        index = self.vcu_list.index(vcu)
        
        tsc_data = vcu.SSH_read(tsc_vars)
        # print(len(tsc_data))
        # print(f"TSC: {tsc_data}")    

        if index == len(self.vcu_list)-2 and self.project == "DB":

            tsc_data_cc = self.vcu_list[-1].SSH_read(tsc_cc_vars)
            # print(f"TSC CC: {tsc_data_cc}")
        coach = Element("g")

        if maintenance_mode == 1:            
            tsc_data=list(map(str,random.choices([0, 1], k=len(tsc_data)))) # Crea una lista de valores aleatorios en formato str
            if index == len(self.vcu_list)-2 and self.project == "DB":
                tsc_data_cc=list(map(str,random.choices([0, 1], k=len(tsc_data_cc)))) # Crea una lista de valores aleatorios en formato str

        if any(not signal.isdigit() for signal in tsc_data):
            
            if self.project == "DSB":
                    SubElement(coach, "rect", x="0", y="0", width="100", height="305", fill="black", opacity="0.5")
                    SubElement(coach, "line", x1="100", y1="0", x2="100", y2="315", stroke="black", **{"stroke-width": "1", "stroke-dasharray": "5, 5"},opacity="0.35")
                    SubElement(coach, "text", x="50", y="292",**{"text-anchor": "middle","font-style": "italic","font-size": "10"}).text = f"Coche {index+1}"
                    SubElement(coach, "text", x="50", y="162.5", fill="white", **{"text-anchor": "middle","dominant-baseline": "central","font-style": "italic","font-size": "30","transform": "rotate(-90, 50, 152.5)"}).text = "OFFLINE"

                    return coach
            
            if self.project == "DB":
                    SubElement(coach, "rect", x="0", y="0", width="100", height="305", fill="black", opacity="0.5")
                    SubElement(coach, "line", x1="100", y1="0", x2="100", y2="315", stroke="black", **{"stroke-width": "1", "stroke-dasharray": "5, 5"},opacity="0.35")
                    SubElement(coach, "text", x="50", y="292",**{"text-anchor": "middle","font-style": "italic","font-size": "10"}).text = f"Coche {index+1}"
                    SubElement(coach, "text", x="50", y="162.5", fill="white", **{"text-anchor": "middle","dominant-baseline": "central","font-style": "italic","font-size": "30","transform": "rotate(-90, 50, 152.5)"}).text = "OFFLINE"

                    return coach
        
        if self.project == "DSB":
            k800 = tsc_data[0] # 'iVCUCH_IO_DS_A602_S45_X1.DIu_RiomS1isOK'
            k801 = tsc_data[1] # 'iVCUCH_IO_DS_A602_S45_X1.DIu_SafCon1Loop'
            k802 = tsc_data[2] # 'iVCUCH_IO_DS_A602_S45_X1.DIu_SafCon2Loop'
            k810 = tsc_data[3] # 'iVCUCH_IO_DS_A602_S42_X1.DIu_RiomS1isOKB1'
            k811 = tsc_data[4] # 'iVCUCH_IO_DS_A602_S43_X1.DIu_SafCon1LoopB1'
            k812 = tsc_data[5] # 'iVCUCH_IO_DS_A602_S43_X1.DIu_SafCon2LoopB1'
            s25 = tsc_data[6] # 'iVCUCH_IO_DS_A602_S46_X1.DIu_STCMSBypass'
            sifa = tsc_data[7] # 'iVCUCH_IO_DS_A602_S42_X1.DIu_EmBrakValvsOpen'
            sifa1_cond = tsc_data[8] # 'iVCUCH_IO_DS_A602_S46_X1.DIu_SIFA1Cond'
            sifa2_cond = tsc_data[9] # 'iVCUCH_IO_DS_A602_S46_X1.DIu_SIFA2Cond'
            k804 = tsc_data[10] # 'iVCUCH_IO_DS_A602_S45_X1.DIu_BypCoachActiv'
            k814 = tsc_data[11] # 'iVCUCH_IO_DS_A602_S45_X1.DIu_BypPRMActiv'
            k753 = tsc_data[12] # 'iVCUCH_IO_DS_A602_S46_X1.DIu_SafBypasLoopOff'
            s60 = tsc_data[13]  # 'RIOMSC1_MVB1_DS_2EA.DigitalInput10' S60 PRINCIPAL
            s60_r = tsc_data[14] # 'RIOMSC1r_MVB2_DS_2EA.DigitalInput10' S60 REDUNDANTE
            s62 = tsc_data[15] # 'RIOMSC1_MVB1_DS_2EA.DigitalInput11' S62 PRINCIPAL
            s62_r = tsc_data[16] # 'RIOMSC1r_MVB2_DS_2EA.DigitalInput11' S62 REDUNDANTE
            s256 = tsc_data[17] # 'RIOMSC1_MVB1_DS_2EA.DigitalInput4' S256 PRINCIPAL
            s256_r = tsc_data[18] # 'RIOMSC1r_MVB2_DS_2EA.DigitalInput4' S256 REDUNDANTE
            s255 = tsc_data[19] # 'RIOMSC1_MVB1_DS_2EA.DigitalInput3' S255 PRINCIPAL
            s255_r = tsc_data[20] # 'RIOMSC1r_MVB2_DS_2EA.DigitalInput3' S255 REDUNDANTE
            fr_riom_sc1 = tsc_data[21] # 'RIOMSC1_MVB1_DS_2E7'
            fr_riom_sc1r = tsc_data[22] # 'RIOMSC1r_MVB2_DS_2E7'
            fr_riom_sc2 = tsc_data[23] # 'RIOMSC2_MVB1_DS_2E7'
            fr_riom_sc2r = tsc_data[24] # 'RIOMSC2r_MVB2_DS_2E7'

        elif self.project == "DB":
            k800 = tsc_data[0] # 'iVCUCH_IO_DS_A602_S45_X1.DIu_RiomS1isOK'
            k801 = tsc_data[1] # 'iVCUCH_IO_DS_A602_S45_X1.DIu_SafCon1Loop'
            k802 = tsc_data[2] # 'iVCUCH_IO_DS_A602_S45_X1.DIu_SafCon2Loop'
            k810 = tsc_data[3] # 'iVCUCH_IO_DS_A602_S42_X1.DIu_RiomS1isOKB1'
            k811 = tsc_data[4] # 'iVCUCH_IO_DS_A602_S43_X1.DIu_SafCon1LoopB1'
            k812 = tsc_data[5] # 'iVCUCH_IO_DS_A602_S43_X1.DIu_SafCon2LoopB1'
            k804 = tsc_data[6] # 'iVCUCH_IO_DS_A602_S45_X1.DIu_BypCoachActiv'
            k814 = tsc_data[7] # 'iVCUCH_IO_DS_A602_S45_X1.DIu_BypPRMActiv'
            s60 = tsc_data[8]  # 'RIOMSC1_MVB1_DS_2EA.DigitalInput10' S60 PRINCIPAL
            s60_r = tsc_data[9] # 'RIOMSC1r_MVB2_DS_2EA.DigitalInput10' S60 REDUNDANTE
            s62 = tsc_data[10] # 'RIOMSC1_MVB1_DS_2EA.DigitalInput11' S62 PRINCIPAL
            s62_r = tsc_data[11] # 'RIOMSC1r_MVB2_DS_2EA.DigitalInput11' S62 REDUNDANTE
            s256 = tsc_data[12] # 'RIOMSC1_MVB1_DS_2EA.DigitalInput4' S256 PRINCIPAL
            s256_r = tsc_data[13] # 'RIOMSC1r_MVB2_DS_2EA.DigitalInput4' S256 REDUNDANTE
            s255 = tsc_data[14] # 'RIOMSC1_MVB1_DS_2EA.DigitalInput3' S255 PRINCIPAL
            s255_r = tsc_data[15] # 'RIOMSC1r_MVB2_DS_2EA.DigitalInput3' S255 REDUNDANTE

            if index == len(self.vcu_list)-2 and self.project == "DB":
                s8 = tsc_data_cc[0]
                s8_r = tsc_data_cc[1]
                s6 = tsc_data_cc[2]
                s6_r = tsc_data_cc[3]
                s10 = tsc_data_cc[4]
                k1 = tsc_data_cc[5]
                k80 = tsc_data_cc[6]
                k81 = tsc_data_cc[7]
                k82 = tsc_data_cc[8]
                k83 = tsc_data_cc[9]
                sifa1_cond = tsc_data_cc[10]
                sifa2_cond = tsc_data_cc[11]
                s700 = tsc_data_cc[12]
                s701 = tsc_data_cc[13]
                s702 = tsc_data_cc[14]
                s703 = tsc_data_cc[15]
                s704 = tsc_data_cc[16]
                k700 = tsc_data_cc[17]
                k701 = tsc_data_cc[18]
                k710 = tsc_data_cc[19]
                k711 = tsc_data_cc[20]
                k708 = tsc_data_cc[21]
                k709 = tsc_data_cc[21]
                k731 = tsc_data_cc[22]
                k732 = tsc_data_cc[23]
                k740 = tsc_data_cc[24]
                k741 = tsc_data_cc[25]
                s25 = tsc_data_cc[26]
                s25_r = tsc_data_cc[27]
                k753 = tsc_data_cc[28]

        if coach_type == '11':
            coach = self.end_coach(project_coach_types[int(coach_type)], index, k801, k800, k802, k804, s60, s60_r, s62, s62_r, s256, s256_r, s255, s255_r, fr_riom_sc1, fr_riom_sc1r)
        elif coach_type in ['3', '4', '6', '7', '8', '9', '10']:
            coach = self.normal_coach(project_coach_types[int(coach_type)], index, k801, k800, k802, k804, s60, s60_r, s62, s62_r, s256, s256_r, self.pmr_index, fr_riom_sc1, fr_riom_sc1r)
        elif coach_type == '5' and self.project == "DSB":
            coach = self.pmr_dsb1(project_coach_types[int(coach_type)], index, k801, k800, k802, k810, k811, k812, sifa, sifa, sifa1_cond, sifa2_cond, k804, k814, k753, s25, s60, s60_r, s62, s62_r, s256, s256_r, s255, s255_r, fr_riom_sc1, fr_riom_sc1r, fr_riom_sc2, fr_riom_sc2r)
        elif coach_type == '5' and self.project == "DB":
            coach = self.pmr_db_dsb2(project_coach_types[int(coach_type)], index, k801, k800, k802, k810, k811, k812, k804, k814, s60, s60_r, s62, s62_r, s256, s256_r)
        elif coach_type == '2' and self.project == "DB":
            coach = self.cabcar(project_coach_types[int(coach_type)], index, k801, k800, k802, k804, s60, s60_r, s62, s62_r, s255, s255_r, s256, s256_r, s8, s8_r, s6, s6_r, s10, k1, k80, k81, k82, k83, sifa1_cond, sifa2_cond, s700, s701, s702, s703, s704, k700, k701, k710, k711, k708, k709, k731, k732, k740, k741, s25, s25_r, k753)
        return coach
   
class MainWindow(QMainWindow):
    
    scan_progress_signal = Signal(int)

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
            "DB_CABCAR": ['10.0.16.96', '10.0.16.160', '10.0.16.224', '10.0.17.32', '10.0.17.96',
                           '10.0.17.160', '10.0.17.224', '10.0.18.32', '10.0.18.96', '10.0.18.160',
                             '10.0.18.224', '10.0.19.32', '10.0.19.96', '10.0.19.160', '10.0.19.224',
                               '10.0.20.32', '10.0.20.96', '10.0.20.160', '10.0.20.224', '10.0.21.32', '10.0.21.96']
        }
        
        self.TCMS_vars = TCMS_vars()
        self.timer=QTimer()

        self.default_width = 800
        self.default_height = 434

        self.diag_windows = []

        self.setWindowTitle("Herramienta de diagnóstico PES")
        self.setFixedSize(self.default_width, self.default_height)

        self.current_dir = os.path.dirname(__file__)
        self.background_pixmap = QPixmap(os.path.join(self.current_dir, "Talgo_logo.png"))
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

        self.trainset_coaches = []
        self.connection_states = {}
        self.current_function = None
        
        self.scan_progress_signal.connect(self.coach_scan_progress)

        self.svg_coaches_length_DSB = [100,100,100,350,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100]
        # self.svg_coaches_length_DB = [100,100,100,350,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100]

    def closeEvent(self, event):
        app.quit()
        event.accept()

    def paintEvent(self, event):
        
        painter = QPainter(self)
        painter.setOpacity(0.05)
        painter.drawPixmap(0, 22, self.width(), self.height(), self.background_pixmap)
        super().paintEvent(event)

    def windows_ver(self):
       if hasattr(sys, 'getwindowsversion'):
           winver = sys.getwindowsversion()
           if winver.build >= 22000:
               return "11"
           elif winver.build >= 19000:
               return "10"
 
    def create_menus(self):
        
        ######### MENÚ ARCHIVO ##########
        
        file_menu = self.menu_bar.addMenu("Archivo")
        
        open_action = QAction("Abrir archivo", self)
        open_action.setEnabled(False)
        
        load_data_action = QAction("Cargar excel variables", self)
        load_data_action.setEnabled(False)
        
        close_app_action = QAction("Cerrar", self)
        close_app_action.setEnabled(False)
        
        file_menu.addActions([open_action, load_data_action, close_app_action])
        
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
        
        self.check_TSC_action=QAction("Comprobar estado lazo de seguridad (TSC)", self)
        self.check_TSC_action.triggered.connect(lambda: self.start_timer_with_function(self.draw_tsc))
        self.check_TSC_action.setEnabled(False)
        
        diag_menu.addActions([self.check_TSC_action])
        
        ######### MENÚ EXPORTAR ##########
        
        export_menu = self.menu_bar.addMenu("Exportar")
        
        self.export_TSC_action=QAction("Exportar imagen TSC", self)
        self.export_TSC_action.setEnabled(False)
        self.export_TSC_action.triggered.connect(lambda: self.tsc.save_as_png(self.timer))
        
        export_menu.addActions([self.export_TSC_action])

    def coach_scan_progress(self, progress, coach_number):
        
        self.detected_label.setText(f"Coches detectados: {0 + coach_number} de {len(self.ip_data[self.project])} posibles.")
        self.progress_bar.setValue(progress)

    def set_project(self, project_value, project_name):
        
        self.setMinimumSize(0, 0)
        self.setMaximumSize(16777215, 16777215)

        if self.timer.isActive():
            self.timer.stop()
        
        if self.connection_monitor:
            self.connection_monitor.stop()
            self.connection_monitor.wait()
            self.connection_monitor=None

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

        self.resize(self.default_width, self.default_height)
                        
        self.project = project_value
    
        self.max_initial_ips = 13 if self.project == "DB" else 15 if self.project == "DSB" else 1
        
        self.progress_title.setText(f"Escaneando composición: {self.project}")
        self.detected_label.setText(f"Coches detectados: {0 + self.max_initial_ips} de {len(self.ip_data[self.project])} posibles.")

        self.progress_bar.setValue(0)
        self.progress_title.setVisible(True)
        self.progress_bar.setVisible(True)
        self.detected_label.setVisible(True)

        self.trainset_coaches = []
        self.valid_ips = []
        

        self.scan_thread = ScanThread(self.ip_data[self.project], self.max_initial_ips, self.project, self.ip_data["DB_CABCAR"])
        self.scan_thread.scan_progress.connect(self.coach_scan_progress)
        self.scan_thread.scan_completed.connect(self.on_scan_completed)
        self.scan_thread.start()

    def on_scan_completed(self, valid_ips):
        
        '''Esta función una vez completado el escaneo de ips, establece las ips validas, 
        crea las instancias de VCU, oculta la barra de progreso y los textos y crea la tabla principal.
        Además, inicia el monitor de conexiones SSH por si la conexión con alguna VCU se cae, la reestablezca 
        y vaya cambiando el código de colores de la tabla.'''
        
        self.valid_ips = valid_ips
        self.coaches_type = ["Unknown"] * len(self.valid_ips)
        self.trainset_coaches=[VCU(ip) for ip in self.valid_ips]
        
        self.progress_bar.setVisible(False)
        self.detected_label.setVisible(False)
        self.progress_title.setVisible(False)
        
        self.create_table()
        
        if not self.connection_monitor:

            self.connection_monitor = ConnectionMonitorThread(self.trainset_coaches)
            self.connection_monitor.connection_status_updated.connect(self.on_connection_status_updated)
            
        self.connection_monitor.start()
        
        self.coach_types = [None] * len(self.trainset_coaches)
               
    def on_connection_status_updated(self, ip, status):

        try:

            if ip in self.connection_states and self.connection_states[ip] == status:
                return

            col=self.valid_ips.index(ip)
            
            ip_item=self.table.item(0,col)

            if maintenance_mode == 0 and status != "failure":

                coach_type = self.trainset_coaches[col].SSH_read(self.TCMS_vars.COACH_TYPE)

                # print(f"COL: {col}, IP: {ip}, TIPO: {coach_type}")

                if self.project == "DB":
                    valid_types = self.TCMS_vars.COACH_TYPES_DB
                elif self.project == "DSB":
                    valid_types = self.TCMS_vars.COACH_TYPES_DSB
                else:
                    valid_types = {}

                if str(coach_type).isdigit() and int(coach_type) not in self.TCMS_vars.COACH_TYPES_DB and col != len(self.trainset_coaches)-1:
                
                    self.connection_monitor.stop()
                    self.connection_monitor.wait()

                    msg =f"El tipo de coche (tipo {coach_type}), reportado por la VCU del coche: {col +1} no es válido.\n"
                    msg += "Probablemente exista un problema en la configuración de la mochila de la VCU o en la configuración del GW.\n"
                    msg += "Si desea forzar el tipo de coche, por favor seleccionalo de la lista:\n"

                    options = list(valid_types.values())
                    option_keys = list(valid_types.keys())

                    selected, ok = QInputDialog.getItem(
                        self,
                        "Tipo de coche desconocido",
                        msg,
                        options,
                        editable = False

                    )

                    if ok:
                        selected_index = options.index(selected)
                        coach_type = option_keys[selected_index]
                        self.trainset_coaches[col].SSH_write_lock('oVCUCH_TRDP_DS_A000.COM_Vehicle_Type', int(coach_type))

                    self.connection_monitor.run()

                self.coach_types[col] = coach_type
            
            elif maintenance_mode == 0 and status == "failure":
                coach_type = "Not SSH"

            elif maintenance_mode == 1 and self.project == "DSB":
                coach_type = PREDEFINED_DSB[col]
                self.coach_types[col] = coach_type   
            elif maintenance_mode == 1 and self.project == "DB":
                
                coach_type = PREDEFINED_DB_13[col]

                self.coach_types[col] = coach_type                     

            if coach_type != "Not SSH" and coach_type != "N/A" or maintenance_mode == 1:

                if self.project == "DSB":
                    coach_type_item = QTableWidgetItem(self.TCMS_vars.COACH_TYPES_DSB[int(coach_type)])
                elif self.project == "DB":
                    coach_type_item = QTableWidgetItem(self.TCMS_vars.COACH_TYPES_DB[int(coach_type)])
                elif self.project == "LOK":
                    coach_type_item = QTableWidgetItem("L9215")
            
            else: 
                coach_type_item = QTableWidgetItem("Not SSH")

            coach_type_item.setTextAlignment(Qt.AlignCenter)
            
            # Evitar sobrescribir celda fusionada si es el último coche en proyecto DB
            if self.project == "DB" and col == len(self.valid_ips) - 1:
                # Saltar la última IP (VCU_PH), ya está cubierta por la fusión con la anterior
                pass
            else:
                self.table.setItem(1, col, coach_type_item)


            self.connection_states[ip] = status
            
            if status == "success":
                ip_item.setBackground(QColor(175, 242, 175))
            elif status == "ping_only":
                ip_item.setBackground(QColor(214, 163, 0))
            elif status == "failure":
                ip_item.setBackground(QColor(255, 131, 131))

        except Exception:
            print("aqui")
            pass

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

    def reset_TAR_TEMP_failures(self):
        """Función para reiniciar fallos temporales de TAR en los VCUs del tren."""

        # Detener temporizador si está corriendo
        if hasattr(self, "timer") and self.timer is not None:
            self.timer.stop()

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
        coches_a_usar = [self.trainset_coaches[0]] if MODO_PRUEBA else self.trainset_coaches
        

        # Crear interfaz de progreso
        self.progress_dialog = QDialog()
        self.progress_dialog.setWindowTitle("Escribiendo en VCUs")
        self.progress_dialog.setGeometry(300, 300, 600, 300)

        dialog_layout = QVBoxLayout()
        self.progress_label = QTextEdit()
        self.progress_label.setReadOnly(True)
        modo_texto = " (MODO PRUEBA - SOLO 1 COCHE)" if MODO_PRUEBA else ""
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

    def draw_tsc(self):

        # Crea el separador si no existe
        if not hasattr(self, 'splitter'):
            self.splitter = QFrame()
            self.splitter.setFrameShape(QFrame.HLine)
            self.splitter.setFrameShadow(QFrame.Sunken)
            self.layout.addWidget(self.splitter)

        # Inicializa el área de scroll si no existe
        if not hasattr(self, 'scroll_tsc'):
            self.scroll_tsc = QScrollArea()
            self.scroll_tsc.setWidgetResizable(True)
            self.scroll_tsc.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            self.scroll_tsc.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.layout.addWidget(self.scroll_tsc)

        # Crea el separador si no existe
        if not hasattr(self, 'splitter_2'):
            self.splitter_2 = QFrame()
            self.splitter_2.setFrameShape(QFrame.HLine)
            self.splitter_2.setFrameShadow(QFrame.Sunken)
            self.layout.addWidget(self.splitter_2)
        
        if not hasattr(self, 'trainset_failures_scan'):
            self.trainset_failures_scan = QPushButton("Escanear fallos de composición completa")
            self.layout.addWidget(self.trainset_failures_scan)
            self.trainset_failures_scan.clicked.connect(self.trainset_tsc_failures)

        if not hasattr(self, 'reset_failures'):
            self.reset_failures = QPushButton("Resetear fallos TAR a composición")
            self.layout.addWidget(self.reset_failures)
            self.reset_failures.clicked.connect(self.reset_TAR_TEMP_failures)
    
        # Guarda la posición actual del scroll (si hay contenido previo)
        h_scroll_position = self.scroll_tsc.horizontalScrollBar().value()
        v_scroll_position = self.scroll_tsc.verticalScrollBar().value()

        # Ajusta el tamaño de la ventana principal
        self.setMinimumSize(0, 0)
        self.setMaximumSize(16777215, 16777215)
        self.setFixedSize(self.table_width + 21, 520)

        # Regenera el TSCGenerator si el proyecto ha cambiado
        if not hasattr(self, 'tsc') or self.project != getattr(self, 'tsc_project', None):
            if self.project == "DSB":
                self.tsc = TSCGenerator(self.trainset_coaches, self.coach_types, self.TCMS_vars.TSC_COACH_VARS_DSB, self.TCMS_vars.COACH_TYPES_DSB, self.TCMS_vars.TSC_CC_VARS_DB)
            elif self.project == "DB":
                self.tsc = TSCGenerator(self.trainset_coaches, self.coach_types, self.TCMS_vars.TSC_COACH_VARS_DB, self.TCMS_vars.COACH_TYPES_DB, self.TCMS_vars.TSC_CC_VARS_DB)
            self.tsc_project = self.project  # Guarda el proyecto actual

        # Regenera siempre el SVG para reflejar cambios en los datos
        self.tsc_widget = self.tsc.generate_svg(self.project)

        # Conecta eventos para el clic y el menú contextual
        # self.tsc_widget.mousePressEvent = self.on_mouse_click

        # Actualiza el contenido del área de scroll
        self.scroll_tsc.setWidget(self.tsc_widget)

        # Ajusta la altura del área de scroll según el contenido
        self.scroll_tsc.setMinimumHeight(self.tsc_widget.sizeHint().height() + 20)

        # Restaura la posición del scroll
        self.scroll_tsc.horizontalScrollBar().setValue(h_scroll_position)
        self.scroll_tsc.verticalScrollBar().setValue(v_scroll_position)

        # Habilita la acción de exportación
        self.export_TSC_action.setEnabled(True)

    def diagnose_vcu(self, vcu):
                
                ip = vcu.ip

                if ip == self.trainset_coaches[-1].ip and self.project == "DB": #La diagnosis para el cabcar es distinta, de ahí este IF.
                    parts = array_split(self.TCMS_vars.BCU_DIAGNOSIS_CC, 10)  # Divide las variables en 5 partes    
                    BCU_results_cc = []
                    for part in parts:
                        result = vcu.SSH_read(part)  # Ejecuta el diagnóstico
                        BCU_results_cc.extend(result)

                    print(BCU_results_cc)

                                        # Identificar errores activos en BCU
                    active_errors = []
                    for index, value in enumerate(BCU_results_cc):
                        if value == '1':  # Error activo
                            var_name = self.TCMS_vars.BCU_DIAGNOSIS_CC[index]
                            error_info = self.TCMS_vars.BCU_DIAGNOSIS_DICT.get(var_name.split('.')[-1], {})
                            error_code = error_info.get("Error Code", "Código no disponible")
                            description = error_info.get("Description", "Descripción no disponible")
                            active_errors.append((ip, error_code, description))

                else: #Para el resto de coches normales
                    
                    TAR_TEMP_results=[]
                    TAR_TEMP_results = vcu.SSH_read(self.TCMS_vars.TSC_DIAG_VARS)

                    # Seleccionar solo los índices relevantes
                    relevant_indices = list(range(20, 24)) + list(range(25, 29)) + list(range(31, 47))
                    filtered_TAR_TEMP_results = [TAR_TEMP_results[i] for i in relevant_indices]
                    filtered_TSC_DIAG_VARS = [self.TCMS_vars.TSC_DIAG_VARS[i] for i in relevant_indices]

                    parts = array_split(self.TCMS_vars.BCU_DIAGNOSIS, 10)  # Divide las variables en 5 partes
                    
                    BCU_results = []
                    for part in parts:
                        result = vcu.SSH_read(part)  # Ejecuta el diagnóstico
                        BCU_results.extend(result)
                        # print(BCU_results)

                    if maintenance_mode == 1: 
                        BCU_results = []
                        TAR_TEMP_results = []
                        filtered_TAR_TEMP_results = list(map(str,random.choices([0, 1], k=len(filtered_TSC_DIAG_VARS)))) # Crea una lista de valores aleatorios en formato str
                        BCU_results=list(map(str,random.choices([0, 1], k=len(self.TCMS_vars.BCU_DIAGNOSIS)))) # Crea una lista de valores aleatorios en formato str
                    
                    # Identificar errores activos en BCU
                    active_errors = []
                    for index, value in enumerate(BCU_results):
                        if value == '1':  # Error activo
                            var_name = self.TCMS_vars.BCU_DIAGNOSIS[index]
                            error_info = self.TCMS_vars.BCU_DIAGNOSIS_DICT.get(var_name.split('.')[-1], {})
                            error_code = error_info.get("Error Code", "Código no disponible")
                            description = error_info.get("Description", "Descripción no disponible")
                            active_errors.append((ip, error_code, description))

                    # Identificar errores activos en TAR_TEMP
                    for index, value in enumerate(filtered_TAR_TEMP_results):
                        if value == '1':  # Error activo
                            var_name = filtered_TSC_DIAG_VARS[index]
                            active_errors.append((ip, var_name, self.TCMS_vars.filtered_TSC_DIAG_NAMES[index]))

                # Guardar en el diccionario solo si hay errores
                if active_errors:
                    self.results_dict[ip] = active_errors
                else:
                    self.results_dict[ip] = [("Sin errores activos", "", "")]  # Formato para la tabla

                return ip

    def export_to_excel(self, table):
        """Exportar los datos de la tabla a un archivo Excel incluyendo número y tipo de coche"""

        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar como",
            "",
            "Archivos Excel (*.xlsx);;Todos los archivos (*)",
            options=options
        )

        if file_path:
            workbook = xlsxwriter.Workbook(file_path)
            worksheet = workbook.add_worksheet("Errores TSC")

            # Formatos
            header_format = workbook.add_format({'bold': True, 'bg_color': '#D7E4BC', 'border': 1})
            cell_format = workbook.add_format({'border': 1})

            # Encabezados
            headers = ["Coche", "Tipo", "IP", "Código de Error", "Descripción"]
            for col, header in enumerate(headers):
                worksheet.write(0, col, header, header_format)

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

            print(type_dict)

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

                            tipo_name = type_dict.get(int(tipo_num), "???")
                            print(tipo_num, tipo_name)
                            current_tipo = f"{tipo_num} ({tipo_name})"
                        else:
                            current_tipo = "???"

                    continue  # Saltar fila de encabezado

                # Fila de error
                if ip_text:  # si hay algo en columna 0, usamos esa IP
                    ip = ip_text
                else:
                    ip = current_ip

                error_code = table.item(row, 1).text() if table.item(row, 1) else ""
                description = table.item(row, 2).text() if table.item(row, 2) else ""

                worksheet.write(row_index, 0, current_coche, cell_format)
                worksheet.write(row_index, 1, current_tipo, cell_format)
                worksheet.write(row_index, 2, ip, cell_format)
                worksheet.write(row_index, 3, error_code, cell_format)
                worksheet.write(row_index, 4, description, cell_format)
                row_index += 1

            workbook.close()

    def trainset_tsc_failures(self):

        self.timer.stop()

        self.results_dict={}

        self.progress_dialog = QDialog()
        self.progress_dialog.setWindowTitle("Escaneo de errores en progreso")
        self.progress_dialog.setGeometry(300, 300, 400, 200)

        dialog_layout = QVBoxLayout()
        self.progress_label = QTextEdit()
        self.progress_label.setReadOnly(True)   
        self.progress_label.append("Escaneando fallos a composición, por favor espere...")
        dialog_layout.addWidget(self.progress_label)
        self.progress_dialog.setLayout(dialog_layout)
        self.progress_dialog.show()

        # Ejecutar diagnóstico en paralelo con ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=len(self.trainset_coaches)) as executor:
            checked_coaches = 0
            total = len(self.trainset_coaches)
            futures = {executor.submit(self.diagnose_vcu, vcu): vcu for vcu in self.trainset_coaches}
            for future in as_completed(futures):
                ip = future.result()  # Esperar a que todas las tareas terminen
                checked_coaches+=1 
                self.progress_label.append(f"Escaneando.. ({checked_coaches}/{total}) \nCompletado: {ip}")
                app.processEvents()

        # time.sleep(2)

        self.progress_dialog.accept()

        self.trainset_failures_window = QWidget()
        self.trainset_failures_window.setWindowTitle("Comprobación de errores de TSC a composición")

        table_layout = QVBoxLayout()

        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["IP", "Código de Error", "Descripción"])

        # Crear barra de menú
        menu_bar = QMenuBar(self.trainset_failures_window)
        file_menu = QMenu("Archivo", self.trainset_failures_window)
        export_action = QAction("Exportar a Excel", self.trainset_failures_window)
        file_menu.addAction(export_action)
        menu_bar.addMenu(file_menu)
        export_action.triggered.connect(lambda: self.export_to_excel(table))  # Conectar evento

        # Convertir resultados_dict en una lista de filas para la tabla
        table_data = []
        for ip, errors in self.results_dict.items():
            table_data.append((ip, None, None))  # Indicador de fila combinada
            for error in errors:
                table_data.append(error)

        table.setRowCount(len(table_data))
        for row_idx, (ip, error_code, description) in enumerate(table_data):
            if error_code is None and description is None:  # Si la fila es una fila combinada
                coach_index = next((i for i, coach in enumerate(self.trainset_coaches) if coach.ip == ip), -1)

                # Caso especial para proyecto DB: últimas 2 IPs son el mismo coche
                if self.project == "DB":
                    last_idx = len(self.trainset_coaches) - 1
                    penult_idx = last_idx - 1

                    if coach_index == penult_idx:
                        label = f"COCHE {coach_index + 1} (VCU_CH) IP: {ip}"
                    elif coach_index == last_idx:
                        label = f"COCHE {coach_index} (VCU_PH) IP: {ip}"  # mismo índice que CH
                    else:
                        label = f"COCHE {coach_index + 1} (IP: {ip})"
                else:
                    label = f"COCHE {coach_index + 1} (IP: {ip})"

                item = QTableWidgetItem(label)
                item.setTextAlignment(Qt.AlignCenter)
                item.setBackground(QBrush(QColor(100, 100, 100)))  # Gris oscuro
                item.setForeground(QBrush(QColor(255, 255, 255)))  # Texto blanco
                table.setItem(row_idx, 0, item)
                table.setSpan(row_idx, 0, 1, 3)  # Fusionar las tres columnas

            else:
                table.setItem(row_idx, 0, QTableWidgetItem(ip))
                table.setItem(row_idx, 1, QTableWidgetItem(error_code))
                table.setItem(row_idx, 2, QTableWidgetItem(description))

        # Ajustar el ancho de las columnas al contenido
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # Ajustar la altura de las filas al contenido
        table.resizeRowsToContents()

        # Calcular el ancho total de la tabla
        total_width = table.verticalHeader().width()  # Ancho del header vertical
        total_width += table.frameWidth() * 2  # Bordes de la tabla

        for col in range(self.table.columnCount()):
            total_width += table.columnWidth(col)  # Sumar ancho de cada columna

        if self.table.verticalScrollBar().isVisible():  # Si hay scrollbar, sumarlo
            total_width += table.verticalScrollBar().width()

        # Ajustar el tamaño de la ventana al ancho total de la tabla
        self.trainset_failures_window.resize(total_width + 50, 400)  # Altura fija, pero podrías ajustarla también

        table_layout.addWidget(menu_bar)
        table_layout.addWidget(table)
       
        self.trainset_failures_window.setLayout(table_layout)
        self.trainset_failures_window.show()

        self.timer.start()
 
    def on_mouse_click(self, event):

        self.timer.stop()

        if event.button() == Qt.LeftButton:

            click_position = self.tsc_widget.mapFromGlobal(event.globalPosition().toPoint())
            x_coord = click_position.x()
            acummulated = 0
            # Ejemplo: Determinar el coche según la posición del clic

            for i, length in enumerate(self.svg_coaches_length_DSB):
                acummulated+=int(length)
                if x_coord<acummulated:
                    coach_index = i
                    break
            self.open_coach_diagnostic_window(coach_index)

    def open_coach_diagnostic_window(self, coach_index):

        if self.connection_states[self.trainset_coaches[coach_index].ip] != "success" and maintenance_mode==0:
            self.timer.start()
            return
        
        tsc_diag_data, BCU_diag_data_1, BCU_diag_data_2, BCU_diag_data_3, BCU_diag_data_4, BCU_diag_data_5, BCU_diag_data_cc_1, BCU_diag_data_cc_2, BCU_diag_data_cc_3, BCU_diag_data_cc_4, BCU_diag_data_cc_5, BCU_diag_data_cc_6, BCU_diag_data_cc_7, BCU_diag_data_cc_8, BCU_diag_data_cc_9, BCU_diag_data_cc_10 = self.tsc.report_tsc_diag(self.trainset_coaches[coach_index], self.TCMS_vars.TSC_DIAG_VARS, self.TCMS_vars.BCU_DIAGNOSIS, self.TCMS_vars.BCU_DIAGNOSIS_CC)
        
        if maintenance_mode == 1: 
            BCU_diag_data = concatenate([BCU_diag_data_1, BCU_diag_data_2, BCU_diag_data_3, BCU_diag_data_4, BCU_diag_data_5])
        else:
            BCU_diag_data = BCU_diag_data_1 + BCU_diag_data_2 + BCU_diag_data_3 + BCU_diag_data_4 + BCU_diag_data_5
            BCU_diag_data_cc = BCU_diag_data_cc_1 + BCU_diag_data_cc_2 + BCU_diag_data_cc_3 + BCU_diag_data_cc_4 + BCU_diag_data_cc_5 + BCU_diag_data_cc_6 + BCU_diag_data_cc_7 + BCU_diag_data_cc_8 + BCU_diag_data_cc_9 + BCU_diag_data_cc_10
            
            if len(self.TCMS_vars.TSC_DIAG_VARS) + len(self.TCMS_vars.BCU_DIAGNOSIS) != len(BCU_diag_data) + len(tsc_diag_data):
                print("SE HAN PERDIDO VARIABLES")

        # print(tsc_diag_data)
        # print(BCU_diag_data)

        diag_window = QWidget()
        diag_window.setWindowTitle(f"Diagnóstico Coche {coach_index + 1}")
        layout = QVBoxLayout()

        # Tab principal
        tab_widget = QTabWidget()

        # Crear las tabs
        # loop_opening_tab = QWidget()
        bearing_temp_tab = QWidget()
        TAR_tab = QWidget()
        BCU_diag_tab = QWidget()

        # tab_widget.addTab(loop_opening_tab, "CAUSA DE APERTURA DE LAZO DE SEGURIDAD")
        tab_widget.addTab(bearing_temp_tab, "TEMPERATURA DE RODAMIENTOS")
        tab_widget.addTab(TAR_tab, "INESTABILIDAD DE RODADURA (TAR)")
        tab_widget.addTab(BCU_diag_tab, "DIAGNÓSIS DE BCU")

        # Calcular el ancho necesario en función de los tabs
        total_tab_width = sum(tab_widget.tabBar().tabRect(i).width() for i in range(tab_widget.count()))
        total_tab_width += 30

        # Función para calcular la altura
        def calculate_window_height(index):
            current_widget = tab_widget.widget(index)
            if current_widget:
                # Calcular el tamaño sugerido para el widget actual
                recommended_height = current_widget.sizeHint().height()
                diag_window.setFixedSize(900, recommended_height + 50)  # Ajustar margen

        # Conectar el evento de cambio de pestaña
        tab_widget.currentChanged.connect(calculate_window_height)

        # LAYOUT PARA LAS TEMPERATURAS DE RODAMIENTOS
        temp_vbox = QVBoxLayout()
        temp_unav_vbox = QVBoxLayout()

        vertical_splitter = QFrame()
        vertical_splitter.setFrameShape(QFrame.VLine)
        vertical_splitter.setFrameShadow(QFrame.Sunken)

        bearing_temps_layout = QHBoxLayout()

        # Bandera para indicar si se debe cambiar el color del tab
        highlight_tab_temp = False
        highlight_tab_tar = False

        if self.project == "DSB":
            # Lógica para temperaturas
            if coach_index == 3:
                for i, bearing in enumerate(self.TCMS_vars.BEARING_NAMES):
                    value = tsc_diag_data[i]
                    unav_value = tsc_diag_data[i + 31]

                    # Crear el label para temperatura
                    label = QLabel(f"{bearing}: {value}")
                    if int(unav_value) != 0:
                        label.setStyleSheet("background-color: yellow")
                        highlight_tab_temp = True
                    temp_vbox.addWidget(label)

                    line = QFrame()
                    line.setFrameShape(QFrame.HLine)
                    line.setFrameShadow(QFrame.Sunken)
                    temp_vbox.addWidget(line)

                    # Crear el label para indisponibilidad
                    unav_label = QLabel(f"{self.TCMS_vars.TEMP_UNAV_NAMES[i]}: {unav_value}")
                    if int(unav_value) != 0:
                        unav_label.setStyleSheet("background-color: yellow")
                    temp_unav_vbox.addWidget(unav_label)

                    line = QFrame()
                    line.setFrameShape(QFrame.HLine)
                    line.setFrameShadow(QFrame.Sunken)
                    temp_unav_vbox.addWidget(line)
            else:
                for i, bearing in enumerate(self.TCMS_vars.BEARING_NAMES[:8]):
                    value = tsc_diag_data[i]
                    unav_value = tsc_diag_data[i + 31]

                    label = QLabel(f"{bearing}: {value}")
                    if int(unav_value) != 0:
                        label.setStyleSheet("background-color: yellow")
                        highlight_tab_temp = True
                    temp_vbox.addWidget(label)

                    line = QFrame()
                    line.setFrameShape(QFrame.HLine)
                    line.setFrameShadow(QFrame.Sunken)
                    temp_vbox.addWidget(line)

                    unav_label = QLabel(f"{self.TCMS_vars.TEMP_UNAV_NAMES[i]}: {unav_value}")
                    if int(unav_value) != 0:
                        unav_label.setStyleSheet("background-color: yellow")
                    temp_unav_vbox.addWidget(unav_label)

                    line = QFrame()
                    line.setFrameShape(QFrame.HLine)
                    line.setFrameShadow(QFrame.Sunken)
                    temp_unav_vbox.addWidget(line)

            # Cambiar el color del texto del tab si es necesario
            if highlight_tab_temp:
                tab_widget.tabBar().setTabTextColor(0, Qt.red)

            # Crear widgets contenedores y establecer layouts
            temp_widget = QWidget()
            temp_widget.setLayout(temp_vbox)
            temp_unav_widget = QWidget()
            temp_unav_widget.setLayout(temp_unav_vbox)

            bearing_temps_layout.addWidget(temp_widget)  # Temperaturas
            bearing_temps_layout.addWidget(vertical_splitter)  # Separador
            bearing_temps_layout.addWidget(temp_unav_widget)  # Indisponibilidad de temperaturas

            # Asignar layout al tab de temperaturas de rodamientos
            bearing_temp_tab.setLayout(bearing_temps_layout)

            # LAYOUT PARA TAR
            tar_vbox = QVBoxLayout()
            tar_unav_vbox = QVBoxLayout()

            tar_splitter = QFrame()
            tar_splitter.setFrameShape(QFrame.VLine)
            tar_splitter.setFrameShadow(QFrame.Sunken)

            tar_layout = QHBoxLayout()

            # Definir número de TAR según el índice del coche
            if coach_index == 3:
                tar_count = 4
            else:
                tar_count = 2

            # Procesar TAR y TAR_UNAV
            for i in range(tar_count):
                tar_index = 16 + i
                tar_unav_index = 20 + i

                # Nombres y valores de TAR
                tar_name = self.TCMS_vars.TAR_NAMES[i]
                tar_value = tsc_diag_data[tar_index]

                # Crear el label para TAR
                tar_label = QLabel(f"{tar_name}: {tar_value}")
                if int(tsc_diag_data[tar_unav_index]) != 0:
                    tar_label.setStyleSheet("background-color: yellow")
                    highlight_tab_tar = True
                tar_vbox.addWidget(tar_label)

                # Crear una nueva línea horizontal y añadirla al layout TAR
                line_tar = QFrame()
                line_tar.setFrameShape(QFrame.HLine)
                line_tar.setFrameShadow(QFrame.Sunken)
                tar_vbox.addWidget(line_tar)

                # Nombres y valores de TAR_UNAV
                tar_unav_name = self.TCMS_vars.TAR_UNAV_NAMES[i]
                tar_unav_value = tsc_diag_data[tar_unav_index]
                tar_unav_label = QLabel(f"{tar_unav_name}: {tar_unav_value}")
                if int(tar_unav_value) != 0:
                    tar_unav_label.setStyleSheet("background-color: yellow")
                tar_unav_vbox.addWidget(tar_unav_label)

                # Crear una nueva línea horizontal y añadirla al layout TAR_UNAV
                line_tar_unav = QFrame()
                line_tar_unav.setFrameShape(QFrame.HLine)
                line_tar_unav.setFrameShadow(QFrame.Sunken)
                tar_unav_vbox.addWidget(line_tar_unav)

            # Cambiar el color del texto del tab TAR si es necesario
            if highlight_tab_tar:
                tab_widget.tabBar().setTabTextColor(1, Qt.red)

            # Crear widgets contenedores y establecer layouts
            tar_widget = QWidget()
            tar_widget.setLayout(tar_vbox)
            tar_unav_widget = QWidget()
            tar_unav_widget.setLayout(tar_unav_vbox)

            tar_layout.addWidget(tar_widget)
            tar_layout.addWidget(tar_splitter)
            tar_layout.addWidget(tar_unav_widget)

            # Asignar layout al tab TAR
            TAR_tab.setLayout(tar_layout)

        # #LAYOUT PARA LA DIAGNÓSIS DE BCU

        active_errors = []

        for index, value in enumerate(BCU_diag_data):
            if value == '1':  # Error activo
                var_name = self.TCMS_vars.BCU_DIAGNOSIS[index]
                error_info = self.TCMS_vars.BCU_DIAGNOSIS_DICT.get(var_name.split('.')[-1], {})
                error_code = error_info.get("Error Code", "Código no disponible")
                description = error_info.get("Description", "Descripción no disponible")
                active_errors.append((var_name, error_code, description))

        for index, value in enumerate(BCU_diag_data_cc):
            if value == '1':  # Error activo
                var_name = self.TCMS_vars.BCU_DIAGNOSIS_CC[index]
                error_info = self.TCMS_vars.BCU_DIAGNOSIS_DICT.get(var_name.split('.')[-1], {})
                error_code = error_info.get("Error Code", "Código no disponible")
                description = error_info.get("Description", "Descripción no disponible")
                active_errors.append((var_name, error_code, description))

        # Crear el layout para el tab de BCU Diagnosis
        BCU_diag_layout = QVBoxLayout()

        if active_errors:
            # Crear la tabla
            table = QTableWidget()
            table.setRowCount(len(active_errors))
            table.setColumnCount(3)
            table.setHorizontalHeaderLabels(["Variable", "Código de Error", "Descripción"])

            # Hacer que la tabla ocupe todo el ancho disponible
            table.horizontalHeader().setStretchLastSection(True)
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            # Llenar la tabla con los diagnósticos activos
            for row, (var_name, error_code, description) in enumerate(active_errors):
                table.setItem(row, 0, QTableWidgetItem(var_name))
                table.setItem(row, 1, QTableWidgetItem(error_code))
                table.setItem(row, 2, QTableWidgetItem(description))

            # Añadir la tabla al layout
            BCU_diag_layout.addWidget(table)

            # Cambiar el color del texto del tab a rojo si hay diagnósticos activos
            tab_index = tab_widget.indexOf(BCU_diag_tab)
            tab_widget.tabBar().setTabTextColor(tab_index, Qt.red)

        else:
            # No hay fallos, mostrar un mensaje
            no_fails_label = QLabel("La diagnósis de BCU no reporta fallos")
            no_fails_label.setAlignment(Qt.AlignCenter)
            BCU_diag_layout.addWidget(no_fails_label)

        # Asignar el layout al tab de BCU Diagnosis
        BCU_diag_tab.setLayout(BCU_diag_layout)

        # Añadir el tab_widget al layout principal
        layout.addWidget(tab_widget)
        diag_window.setLayout(layout)

        current_widget = tab_widget.widget(0)
        recommended_height = current_widget.sizeHint().height()
        diag_window.setFixedSize(900, recommended_height + 50)  # Ajustar margen

        # Mostrar ventana
        diag_window.show()

        # Evento para cerrar la ventana y reiniciar el temporizador
        def on_close_event(event):
            self.timer.start()
            event.accept()

        diag_window.closeEvent = on_close_event

        # Guardar referencia a la ventana
        self.diag_windows.append(diag_window)

    def set_timer_function(self, new_function):

        if self.current_function != new_function:
            if self.current_function is not None:
                try:
                    self.timer.timeout.disconnect(self.current_function)  # Desconecta la función anterior si está conectada
                except TypeError:
                    pass  # Ignora el error si la función no está conectada

            self.timer.timeout.connect(new_function)  # Conecta la nueva función
            self.current_function = new_function  # Actualiza la función actual conectada
    
    def start_timer_with_function(self, new_function):

        self.set_timer_function(new_function)
        new_function()  # Llama a la función inmediatamente
        if not self.timer.isActive():  # Verifica si el temporizador no está activo
            self.timer.start(TEST_TIMEOUT)  # Configura el intervalo en 2 segundos

if __name__ == "__main__":
    
    if not QApplication.instance():
        app = QApplication(sys.argv)
        app.setStyle(QStyleFactory.create("Fusion"))
    else:
        app = QApplication.instance()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
