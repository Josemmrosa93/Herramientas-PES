from PySide6.QtWidgets import (
    QApplication, QDialog, QTableWidget, QTableWidgetItem, QAbstractItemView, QSpinBox, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget, QPushButton, QFileDialog, QStyledItemDelegate, QStyle, QStyleOptionViewItem,
    QStyleOptionViewItem, QMenu, QMenuBar, QFrame, QComboBox, QLineEdit, QCheckBox, QLabel, QHBoxLayout, QTextEdit, QToolBar, QColorDialog, QToolButton, QListWidget, QStackedWidget, QFormLayout
)
from PySide6.QtCore import Qt, QSize, QRectF, QSizeF, QMarginsF
from PySide6.QtGui import QTextDocument, QAction, QTextCharFormat, QFont, QKeySequence, QTextCursor, QPainter, QTextDocument, QPageSize, QIcon, QBrush, QColor
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPrintSupport import QPrinter
import sys, os, tempfile, sqlite3, pickle, re
import urllib.parse
from weasyprint import HTML
from bs4 import BeautifulSoup


reg_tit_esp="REGISTRO ALIMENTACIÓN A SERVICIOS E ILUMINACION INTERIOR LOCOMOTORA"
reg_tit_tra="RECORD FOR VERIFICATION OF LIGHTING AND SERVICES PROJECT F081"
reg_code="RPTF-2829-19"
coach_type="C4315"
coach_number=coach_type + "-028"
names=["EDUARDO GRASA","ÓSCAR CARCELÉN","JULIO MARTÍN"]
dates=["21/11/24","30/11/24","05/12/24"]
sign=[]
ppoints=[["5.1.1","5.2.5.3","5.1.8.5","5.6.7.8.3"],["5.1.1","5.2.5.3"],["5.1.1"]]
percentages=["20%","42%","98%"]
result="CONFORME"
managersign="test"
revisions = [
    ["1.0", "21/11/24", "Apartado 3.2", ("Diseño", "1", "Se añadió nueva descripción")],
    ["1.1", "22/11/24", "Apartado 4.1", ("Mejora de proceso", "2", "Corrección de errores ortográficos")],
    ["1.2", "23/11/24", "Apartado 5.3", ("Diseño", "3", "Actualización de requisitos")],
]
tipos_F073 = ["C4302P","C4302S","C4302C","C4322","C4315","C4314","C4301P","C4306","C4328","C4340","L9215","COMP","TREN"]

class HTMLDelegate(QStyledItemDelegate):

    def paint(self, painter, option, index):
        # print("Llamada a paint - Fila:", index.row(), "Columna:", index.column())
        # print("Rectángulo de la celda:", option.rect)
        # print("Estado de la opción:", option.state)
        options = QStyleOptionViewItem(option)
        self.initStyleOption(options, index)

        # Obtener el contenido HTML (solo para la columna de "Contenido")
        html_content = index.data(Qt.DisplayRole) if index.column() == 2 else ""

        # Dibujar el fondo de la celda seleccionada
        if options.state & QStyle.State_Selected:
            painter.save()
            painter.fillRect(options.rect, options.palette.highlight())
            painter.restore()

        # Dibujar el borde inferior manualmente para que no desaparezca
        painter.save()
        painter.setPen(Qt.lightGray)  # Color de la línea de separación
        painter.drawLine(options.rect.bottomLeft(), options.rect.bottomRight())  # Línea inferior de la celda
        painter.restore()

        # Si es la columna de "Contenido" y tiene HTML, renderizarlo
        if index.column() == 2 and html_content:
            document = QTextDocument()
            document.setHtml(html_content)
            document.setTextWidth(options.rect.width())

            # Calcular la altura ideal del contenido
            content_height = document.size().height()
            rect = options.rect

            # Calcular el punto de inicio para centrar el contenido
            text_x = rect.x()  # Para alineación izquierda
            text_y = rect.y() + (rect.height() - content_height) / 2  # Para centrar verticalmente

            # Dibujar el contenido HTML centrado
            painter.save()
            painter.translate(text_x, text_y)
            if options.state & QStyle.State_Selected:
                painter.setPen(options.palette.highlightedText().color())  # Cambiar el color del texto si está seleccionado
            document.drawContents(painter)
            painter.restore()
        else:
            # Para otras columnas, usar el comportamiento predeterminado
            super().paint(painter, options, index)

    def sizeHint(self, option, index):
        if index.column() == 2:
            # Calcular el tamaño necesario para el contenido HTML
            html_content = index.data(Qt.DisplayRole)
            document = QTextDocument()
            document.setHtml(html_content)
            document.setTextWidth(option.rect.width())

            content_height = document.size().height()
            margin = 10  # Margen extra para mejor espaciado

            return QSize(document.idealWidth(), content_height + margin)
        else:
            # Para otras columnas, usar el comportamiento predeterminado
            return super().sizeHint(option, index)

class TreeWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editor de registros PES")
        self.setGeometry(0, 0, 1200, 600)

        self.config_window = PreferencesWindow()

        layout = QVBoxLayout()
        
        # Menú
        self.menubar = QMenuBar(self)
        archivo_menu = QMenu("Archivo", self)
        editar_menu = QMenu("Editar", self)
        exportar_menu = QMenu("Exportar", self)
        
        self.menubar.addMenu(archivo_menu)
        self.menubar.addMenu(editar_menu)
        self.menubar.addMenu(exportar_menu)
        
        layout.setMenuBar(self.menubar)

        # Opciones de exportar

        exportar_pdf_action = QAction("Exportar PDF", self)
        exportar_pdf_action.triggered.connect(self.exportar_pdf)
        exportar_pdf_action.setShortcut("Ctrl+E")
        exportar_menu.addAction(exportar_pdf_action)

        # Opciones de Archivo
        nuevo_action = QAction("Nuevo RPTF", self)
        archivo_menu.addAction(nuevo_action)
        self.nuevo_action = nuevo_action
        self.nuevo_action.setShortcut("Ctrl+N")
        
        cargar_action = QAction("Cargar RPTF", self)
        cargar_action.triggered.connect(self.cargar_rptf)
        archivo_menu.addAction(cargar_action)
        self.cargar_action = cargar_action
        self.cargar_action.setShortcut("Ctrl+L")

        cargar_html_action = QAction("Cargar registro HTML (DOORS)", self)
        cargar_html_action.triggered.connect(self.load_file)  # Conectar a la función load_file
        archivo_menu.addAction(cargar_html_action)
        self.cargar_html_action = cargar_html_action
        self.cargar_html_action.setShortcut("Ctrl+H")  # Atajo de teclado opcional
        
        guardar_action = QAction("Guardar RPTF", self)
        guardar_action.triggered.connect(self.guardar_rptf)
        archivo_menu.addAction(guardar_action)
        guardar_action.setEnabled(False)
        self.guardar_action = guardar_action
        self.guardar_action.setShortcut("Ctrl+S")
        
        guardar_como_action = QAction("Guardar RPTF como..", self)
        guardar_como_action.triggered.connect(self.guardar_rptf_como)
        archivo_menu.addAction(guardar_como_action)
        self.guardar_como_action = guardar_como_action
        self.guardar_como_action.setShortcut("Ctrl+Shift+S")

        preferencias_action = QAction("Preferencias", self)
        preferencias_action.triggered.connect(self.show_preferences)
        archivo_menu.addAction(preferencias_action)
        self.preferencias_action = preferencias_action
        
    
        cerrar_action = QAction("Cerrar RPTF", self)
        cerrar_action.triggered.connect(self.cerrar_rptf)
        archivo_menu.addAction(cerrar_action)
        cerrar_action.setEnabled(False)
        self.cerrar_action = cerrar_action
        self.cerrar_action.setShortcut("Ctrl+C")
        
        # Opciones de Editar
        self.historial = []  # Lista para almacenar estados
        self.historial_redo = []  # Lista para almacenar estados de rehacer
        self.max_historial = 5  # Solo se guardarán los últimos 5 estados

        self.deshacer_action = QAction("Deshacer", self)
        self.deshacer_action.setShortcut("Ctrl+Z")
        self.deshacer_action.triggered.connect(self.deshacer)
        editar_menu.addAction(self.deshacer_action)
        
        self.rehacer_action = QAction("Rehacer", self)
        self.rehacer_action.setShortcut("Ctrl+F")
        self.rehacer_action.triggered.connect(self.rehacer)
        editar_menu.addAction(self.rehacer_action)
        
        # Árbol de pruebas
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Índice", "Tipo de Prueba", "Contenido", "Multimedia"])

        # Centrar el texto de los encabezados "Índice" y "Tipo de Pregunta"
        self.tree.headerItem().setTextAlignment(0, Qt.AlignCenter)  # Índice
        self.tree.headerItem().setTextAlignment(1, Qt.AlignCenter)  # Tipo de Pregunta
        self.tree.headerItem().setTextAlignment(2, Qt.AlignLeft | Qt.AlignVCenter)  # Contenido
        self.tree.headerItem().setTextAlignment(3, Qt.AlignLeft | Qt.AlignVCenter)  # Multimedia

        self.tree.setStyleSheet("""
                QTreeWidget::item {
                    border-bottom: 1px solid #d0d0d0;  /* Línea entre filas */
                    padding: 20px;  /* Espaciado interno */
                    border-right: 1px solid #d0d0d0;
                }
                QTreeWidget::item:selected {
                    background-color: #a0a0a0;  /* Color de fondo seleccionado */
                    color: #ffffff;  /* Color de texto seleccionado */
                }
                QHeaderView::section {
                    background-color: #f0f0f0;  /* Color de fondo */
                    padding: 5px;
                    border: 1px solid #d0d0d0;
                    font-weight: bold;
                    text-align: center;  /* Centrar el texto */
                }
            """)

        # Asignar el delegate personalizado a la columna de "Contenido"
        self.tree.setItemDelegateForColumn(2, HTMLDelegate(self.tree))

        # Conectar la señal de expansión/colapso para ajustar el alto de las filas
        self.tree.expanded.connect(self.adjust_row_heights)
        self.tree.collapsed.connect(self.adjust_row_heights)

        self.tree.setSelectionBehavior(QTreeWidget.SelectRows)  # Seleccionar filas completas
        self.tree.itemExpanded.connect(self.adjust_column_widths_on_expand)

        # Ajustar el ancho de las columnas 0 y 1 al contenido
        self.tree.resizeColumnToContents(0)  # Columna 0
        self.tree.resizeColumnToContents(1)  # Columna 1

        layout.addWidget(self.tree)

        # Crear un QFrame para la línea horizontal
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)
        
        # Sección de inserción de pruebas
        self.insert_layout = QHBoxLayout()
        
        # Combobox para seleccionar el nivel de escritura
        self.nivel_selector = QComboBox()
        self.nivel_selector.addItems(["Escribir debajo al mismo nivel", "Escribir debajo en un subnivel"])
        self.insert_layout.addWidget(self.nivel_selector)
        
        # Combobox para seleccionar el tipo de prueba
        self.tipo_prueba_selector = QComboBox()
        self.tipo_prueba_selector.addItems(["Título", "Texto estático", "Si/No", "Número", "Texto"])
        self.tipo_prueba_selector.currentIndexChanged.connect(self.actualizar_interfaz_tipo_prueba)
        self.insert_layout.addWidget(self.tipo_prueba_selector)
        
        self.contenido_prueba = QTextEdit()
        self.contenido_prueba.setPlaceholderText("Contenido de la prueba")
        self.contenido_prueba.setMaximumHeight(100)

         # Crear una barra de herramientas para los botones de formato
        self.contenido_prueba.cursorPositionChanged.connect(self.actualizar_toolbar)
        
        self.toolbar = QToolBar("Formato")

        # Botón para negrita
        self.bold_action = QAction(QIcon("images/bold_icon.png"), "", self)
        self.bold_action.setFont(QFont("Arial", weight=QFont.Bold))
        self.bold_action.setShortcut(QKeySequence.Bold)
        self.bold_action.setCheckable(True)
        self.bold_action.triggered.connect(self.set_bold)
        self.toolbar.addAction(self.bold_action)

        # Botón para cursiva
        self.italic_action = QAction(QIcon("images/italic_icon.png"), "", self)
        italic_font = QFont("Arial")
        italic_font.setItalic(True)
        self.italic_action.setFont(italic_font)
        self.italic_action.setShortcut(QKeySequence.Italic)
        self.italic_action.setCheckable(True)
        self.italic_action.triggered.connect(self.set_italic)
        self.toolbar.addAction(self.italic_action)

        # Botón para subrayado
        self.underline_action = QAction(QIcon("images/underline_icon.png"), "", self)
        underline_font = QFont("Arial")
        underline_font.setUnderline(True)
        self.underline_action.setFont(underline_font)
        self.underline_action.setShortcut(QKeySequence.Underline)
        self.underline_action.setCheckable(True)
        self.underline_action.triggered.connect(self.set_underline)
        self.toolbar.addAction(self.underline_action)

        # Botón para cambiar color
        self.color = "rgba(0,0,0,1)"
        self.color_action = QAction(QIcon("images/color_icon.png"), "", self)
        color_font = QFont("Arial")
        self.color_action.setFont(color_font)
        self.color_action.setCheckable(False)
        self.color_action.triggered.connect(self.set_color)
        self.toolbar.addAction(self.color_action)

        # Botón para agregar una imagen

        self.insertar_imagen_action = QAction(QIcon("images/image_icon.png"), "", self)
        self.insertar_imagen_action.setToolTip("Insertar imagen")
        image_font = QFont("Arial")
        self.insertar_imagen_action.setFont(image_font)
        self.insertar_imagen_action.triggered.connect(self.abrir_insertar_imagen)
        self.toolbar.addAction(self.insertar_imagen_action)

        # Botón para agregar una tabla

        self.insertar_tabla_action = QAction(QIcon("images/tabla_icon.png"), "", self)
        self.insertar_tabla_action.setToolTip("Insertar imagen")
        table_font = QFont("Arial")
        self.insertar_tabla_action.setFont(table_font)
        self.insertar_tabla_action.triggered.connect(self.abrir_insertar_tabla)
        self.toolbar.addAction(self.insertar_tabla_action)

        self.toolbar.setStyleSheet("""
            QToolButton { 
            border: 1px solid gray;
            border-radius: 1px;
            padding: 2px;                                 
            background-color: #f0f0f0;                
            }     
            QToolButton:checked{
            border: 2px solid gray;
            border-radius: 1px;
            padding: 2px;                                 
            background-color: #f0f0f0;                         
            }                           """)
        
        self.toolbar.setIconSize(QSize(15,15))
        
        # Campos adicionales para el tipo "Número"
        self.unidad_medida = QLineEdit()
        self.unidad_medida.setPlaceholderText("Unidad de medida")
        self.unidad_medida.setVisible(False)
        self.insert_layout.addWidget(self.unidad_medida)
        
        self.valor_minimo = QLineEdit()
        self.valor_minimo.setPlaceholderText("Valor mínimo")
        self.valor_minimo.setVisible(False)
        self.insert_layout.addWidget(self.valor_minimo)
        
        self.valor_maximo = QLineEdit()
        self.valor_maximo.setPlaceholderText("Valor máximo")
        self.valor_maximo.setVisible(False)
        self.insert_layout.addWidget(self.valor_maximo)
        
        self.valor_objetivo = QLineEdit()
        self.valor_objetivo.setPlaceholderText("Valor objetivo")
        self.valor_objetivo.setVisible(False)
        self.insert_layout.addWidget(self.valor_objetivo)
        
        # Botón para agregar la prueba
        self.btn_agregar = QPushButton("Agregar Prueba")
        self.btn_agregar.clicked.connect(self.agregar_prueba)
        self.insert_layout.addWidget(self.btn_agregar)

        # Botón para eliminar punto
        self.btn_eliminar = QPushButton("Eliminar Punto")
        self.btn_eliminar.clicked.connect(self.eliminar_punto)
        self.insert_layout.addWidget(self.btn_eliminar)

        # Checkbox y label para desplazar puntos
        self.checkbox_desplazar = QCheckBox()
        self.label_desplazar = QLabel("Desplazar puntos")
        self.insert_layout.addWidget(self.checkbox_desplazar)
        self.insert_layout.addWidget(self.label_desplazar)

        layout.addLayout(self.insert_layout)

        layout.addWidget(self.toolbar)

        layout.addWidget(self.contenido_prueba)
        
        # Visor de PDF
        self.pdf_view = QPdfView()
        # layout.addWidget(self.pdf_view)
        
        self.pdf_document = QPdfDocument()
        self.pdf_view.setDocument(self.pdf_document)

        # Botón para previsualizar el PDF
        self.btn_preview = QPushButton("Preview PDF")
        self.btn_preview.clicked.connect(self.mostrar_html_preview)
        self.btn_preview.setShortcut("Ctrl+P")
        layout.addWidget(self.btn_preview)
        
        self.setLayout(layout)
        self.db_path = None
        self.conn = None
        self.cursor = None
        self.last_added = None

        # Variable para almacenar el elemento copiado
        self.elemento_copiado = None

        # Conectar el evento de clic derecho en el árbol
        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.mostrar_menu_contextual)

    def abrir_insertar_tabla(self):
        dialogo = InsertarTablaDialog(self)
        if dialogo.exec() == QDialog.Accepted:
            nuevo_html = dialogo.resultado

            print(nuevo_html)

            self.contenido_prueba.insertHtml(nuevo_html)
            self.adjust_row_heights()

    def abrir_insertar_imagen(self):
        contenido_actual = self.limpiar_html_rico(self.contenido_prueba.toHtml())
        print(self.contenido_prueba.toHtml())
        print("###########################################")
        print(contenido_actual)
        dialogo = InsertarImagenDialog(self, contenido_actual)
        if dialogo.exec() == QDialog.Accepted:
            nuevo_html = dialogo.resultado
            # print("EDITADO Y VOLCADO EN CONTENIDO: ", nuevo_html)
            self.contenido_prueba.setHtml(nuevo_html)
            self.adjust_row_heights()

    def exportar_pdf(self):

        html = self.generar_pdf_con_webengine()  # Tu HTML generado

        file_path, _ = QFileDialog.getSaveFileName(self, "Guardar como PDF", "", "Archivos PDF (*.pdf)")
        if not file_path:
            return

        if not file_path.endswith(".pdf"):
            file_path += ".pdf"

        # Configurar impresora
        printer = QPrinter(QPrinter.HighResolution)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(file_path)
        printer.setPageSize(QPageSize(QPageSize.A4))
        printer.setPageMargins(QMarginsF(15, 20, 15, 20))  # En puntos

        # Documento principal
        doc = QTextDocument()
        doc.setDefaultFont(QFont("Calibri", 11))
        doc.setHtml(html)

        # Área imprimible
        page_rect = printer.pageRect(QPrinter.Point)
        page_width = page_rect.width()
        page_height = page_rect.height()
        header_height = 80

        doc.setPageSize(QSizeF(page_width, page_height - header_height))

        painter = QPainter()
        if not painter.begin(printer):
            print("No se pudo iniciar la impresión.")
            return

        total_pages = doc.pageCount()

        for page_number in range(total_pages):
            if page_number > 0:
                printer.newPage()

            # HEADER personalizado (puedes editar esto)
            header_html = f"""
            <div style='font-family: Calibri; font-size:12pt; font-weight: bold; display: flex; justify-content: space-between;'>
                <div>Talgo · Registro F073</div>
                <div>Página {page_number + 1} / {total_pages}</div>
            </div>
            <hr>
            """

            header_doc = QTextDocument()
            header_doc.setDefaultFont(QFont("Calibri", 10))
            header_doc.setHtml(header_html)
            header_doc.setPageSize(QSizeF(page_width, header_height))

            # Dibujar el header
            header_doc.drawContents(painter, QRectF(0, 0, page_width, header_height))

            # Dibujar el contenido desplazado debajo del header
            painter.save()
            painter.translate(0, header_height)
            doc.drawContents(painter, QRectF(0, 0, page_width, page_height - header_height))
            painter.restore()

        painter.end()

        print(f"PDF generado correctamente en: {file_path}")

    def set_bold(self):
        """Aplica o quita el formato de negrita al texto seleccionado."""
        self.aplicar_formato()

    def set_italic(self):
        """Aplica o quita el formato de cursiva al texto seleccionado."""
        self.aplicar_formato()

    def set_underline(self):
        """Aplica o quita el formato de subrayado al texto seleccionado."""
        self.aplicar_formato()

    def limpiar_html_rico(self, html: str) -> str:
        
        if not html or "qt-paragraph-type:empty" in html:
            return ""

        soup = BeautifulSoup(html, "html.parser")
        body = soup.find("body")

        if not body or (not body.get_text(strip=True) and not body.find("img")):
            return ""

        resultado = []

        for tag in body.find_all(recursive=False):
            # Caso especial: <p> con solo imagen (caso típico de imagen insertada)
            if tag.name == "p" and tag.find("img") and len(tag.contents) == 1:
                img = tag.find("img")
                src = img.get("src", "")
                if src.startswith("file:///"):
                    src = urllib.parse.unquote(src[8:])
                    img["src"] = src

                # Detectar alineación desde 'align' o 'style'
                alineacion = tag.get("align")
                estilo = tag.get("style", "")
                if not alineacion:
                    if "text-align: center" in estilo:
                        alineacion = "center"
                    elif "text-align: right" in estilo:
                        alineacion = "right"
                    else:
                        alineacion = "left"

                def extraer_margen(nombre):
                    patron = re.search(fr"{nombre}\s*:\s*([^;]+)", estilo)
                    return patron.group(1).strip() if patron else "0px"
                
                margin_top = extraer_margen("margin-top")
                margin_bottom = extraer_margen("margin-bottom")
                
                # Reconstruir como <div>
                div = soup.new_tag("div")
                div["style"] = f"text-align: {alineacion}; margin-top: {margin_top}; margin-bottom: {margin_bottom};"
                div.append(img)
                resultado.append(div)

            else:
                # Limpiar estilos basura de cualquier etiqueta anidada
                for sub in tag.find_all(True):
                    estilo = sub.get("style", "")
                    estilo_limpio = "; ".join(
                        s.strip() for s in estilo.split(";")
                        if not s.strip().startswith("-qt-") and "text-indent" not in s
                    ).strip("; ")
                    if estilo_limpio:
                        sub["style"] = estilo_limpio
                    elif "style" in sub.attrs:
                        del sub["style"]

                resultado.append(tag)

        return "\n".join(str(e) for e in resultado).strip()

    def aplicar_formato(self):
        cursor = self.contenido_prueba.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)

        formato_actual = cursor.charFormat()

        formato_actual.setFontWeight(QFont.Bold if self.bold_action.isChecked() else QFont.Normal)
        formato_actual.setFontItalic(self.italic_action.isChecked())
        formato_actual.setFontUnderline(self.underline_action.isChecked())

        cursor.mergeCharFormat(formato_actual)
        self.contenido_prueba.mergeCurrentCharFormat(formato_actual)

    def set_color(self):
        """Cambia el color del texto seleccionado."""
        cursor = self.contenido_prueba.textCursor()
        color = QColorDialog.getColor()

        if color.isValid():

            format = QTextCharFormat()
            format.setForeground(color)
            cursor.mergeCharFormat(format)
            self.color = color.name()

            self.contenido_prueba.setCurrentCharFormat(format)

    def actualizar_toolbar(self):
        cursor = self.contenido_prueba.textCursor()
        formato = cursor.charFormat()
        self.bold_action.setChecked(formato.fontWeight() == QFont.Bold)
        self.italic_action.setChecked(formato.fontItalic())
        self.underline_action.setChecked(formato.fontUnderline())
        self.color = formato.foreground().color().name()

        for widget in self.toolbar.findChildren(QToolButton):
                if widget.defaultAction() == self.color_action: 
                    widget.setStyleSheet(f"background-color: {self.color};")
                    break

    def mostrar_menu_contextual(self, pos):
        menu = QMenu()
        copiar_action = QAction("Copiar", self)
        copiar_action.triggered.connect(self.copiar_elemento)
        menu.addAction(copiar_action)

        pegar_action = QAction("Pegar", self)
        pegar_action.triggered.connect(self.pegar_elemento)
        menu.addAction(pegar_action)

        menu.exec(self.tree.viewport().mapToGlobal(pos))

    def copiar_elemento(self, item):
        """Copia el elemento seleccionado para poder pegarlo después."""
        self.elemento_copiado = QTreeWidgetItem()
        self.elemento_copiado.setText(0, item.text(0))
        self.elemento_copiado.setText(1, item.text(1))
        self.elemento_copiado.setText(2, item.text(2))

    def pegar_elemento(self, item, modo):
        """Pega el elemento copiado en la posición especificada."""
        if self.elemento_copiado:
            # Crear un nuevo elemento basado en el copiado
            nuevo_item = QTreeWidgetItem()
            nuevo_item.setText(0, self.elemento_copiado.text(0))
            nuevo_item.setText(1, self.elemento_copiado.text(1))
            nuevo_item.setText(2, self.elemento_copiado.text(2))

            # Copiar los hijos del elemento copiado
            for i in range(self.elemento_copiado.childCount()):
                hijo = self.elemento_copiado.child(i)
                nuevo_hijo = QTreeWidgetItem()
                nuevo_hijo.setText(0, hijo.text(0))
                nuevo_hijo.setText(1, hijo.text(1))
                nuevo_hijo.setText(2, hijo.text(2))
                nuevo_item.addChild(nuevo_hijo)

            # Insertar el nuevo elemento en la posición correcta
            if modo == "debajo_mismo_nivel":
                parent = item.parent()
                if parent:
                    parent.insertChild(parent.indexOfChild(item) + 1, nuevo_item)
                else:
                    self.tree.insertTopLevelItem(self.tree.indexOfTopLevelItem(item) + 1, nuevo_item)
            elif modo == "arriba_mismo_nivel":
                parent = item.parent()
                if parent:
                    parent.insertChild(parent.indexOfChild(item), nuevo_item)
                else:
                    self.tree.insertTopLevelItem(self.tree.indexOfTopLevelItem(item), nuevo_item)
            elif modo == "debajo_subnivel":
                item.addChild(nuevo_item)

            # Actualizar los índices después de pegar
            self.actualizar_indices()

    def reemplazar_rutas_multimedia(self, html, multimedia):
        """Reemplaza las rutas src en el HTML con la ruta absoluta desde la carpeta temporal"""
        if not multimedia or not hasattr(self, 'ole_temp_dir'):
            return html

        ruta_map = {
            os.path.basename(nombre.strip()): os.path.join(self.ole_temp_dir, os.path.basename(nombre.strip()))
            for nombre in multimedia.split(",")
        }

        def reemplazo(match):
            src_original = match.group(1)
            nombre = os.path.basename(src_original)
            if nombre in ruta_map:
                nueva_ruta = ruta_map[nombre].replace(os.sep, '/')
                return f'src="file:///{nueva_ruta}"'
            return match.group(0)

        return re.sub(r'src="([^"]+)"', reemplazo, html)

    def cargar_rptf(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Cargar RPTF", "", "Database Files (*.db)")
        if file_name:
            self.db_path = file_name
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()

            self.ole_temp_dir = tempfile.mkdtemp(prefix="rptf_ole_")
            print(f"Directorio temporal OLE: {self.ole_temp_dir}")

            try:
                self.cursor.execute("SELECT indice, nombre, contenido FROM archivos_ole")
                for indice, nombre, contenido in self.cursor.fetchall():
                    file_path = os.path.join(self.ole_temp_dir, nombre)
                    with open(file_path, "wb") as f:
                        f.write(contenido)
            except Exception as e:
                print(f"No se pudieron extraer archivos OLE: {e}")

            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='registros'")
            if not self.cursor.fetchone():
                self.cursor.execute("""
                    CREATE TABLE registros (
                        indice TEXT PRIMARY KEY,
                        tipo TEXT,
                        contenido TEXT,
                        multimedia TEXT
                    )
                """)
                self.conn.commit()
                return

            self.tree.clear()
            self.cursor.execute("SELECT indice, tipo, contenido, multimedia FROM registros")
            registros = self.cursor.fetchall()

            def ordenar_indice(indice):
                partes = []
                for parte in indice.split('.'):
                    partes.extend(int(p) if p.isdigit() else p for p in parte.split('-'))
                return partes

            registros_ordenados = sorted(registros, key=lambda x: ordenar_indice(x[0]))
            nodos = {}

            for row in registros_ordenados:
                indice, tipo, contenido, multimedia = row

                # Aquí reemplazamos las rutas del contenido HTML
                contenido = self.reemplazar_rutas_multimedia(contenido, multimedia)

                niveles = indice.split(".")
                parent = None

                if len(niveles) == 1:
                    new_item = QTreeWidgetItem([indice, tipo, contenido, multimedia])
                    self.tree.addTopLevelItem(new_item)
                    nodos[indice] = new_item
                else:
                    parent_index = ".".join(niveles[:-1])
                    if parent_index in nodos:
                        parent = nodos[parent_index]
                        new_item = QTreeWidgetItem([indice, tipo, contenido, multimedia])
                        parent.addChild(new_item)
                        nodos[indice] = new_item
                    else:
                        print(f"Advertencia: No se encontró el padre {parent_index} para {indice}, se omitirá.")

            self.guardar_action.setEnabled(True)
            self.guardar_como_action.setEnabled(True)
            self.cerrar_action.setEnabled(True)
            self.adjust_row_heights()
            self.adjust_content_column_width()
            self.tree.resizeColumnToContents(0)
            self.tree.resizeColumnToContents(1)

    def cerrar_rptf(self):
        """Cierra la base de datos y limpia el árbol"""
        if self.conn:
            self.conn.close()
        self.conn = None
        self.db_path = None
        self.tree.clear()
    
        # Deshabilitar botón "Guardar"
        self.guardar_action.setEnabled(False)

    def desplazar_indices(self, siblings, new_index):
        """Desplaza los índices de los elementos hermanos y sus subniveles que tienen un índice mayor o igual al nuevo índice."""
        new_index_parts = [int(x) for x in new_index.split(".")]

        for item in reversed(siblings):  # Iteramos en orden inverso para evitar sobrescribir datos
            item_index_parts = [int(x) for x in item.text(0).split(".")]

            if item_index_parts >= new_index_parts:
                viejo_index = item.text(0)
                nuevo_index = self.incrementar_indice(viejo_index, 1)

                item.setText(0, nuevo_index)

                # Actualizar también todos los subniveles del elemento desplazado
                self.actualizar_subniveles(item, viejo_index, nuevo_index)

    def agregar_prueba(self):
        """Agrega una prueba al árbol en la posición seleccionada y desplaza los elementos si es necesario."""
        self.guardar_estado()  # Guardar estado antes de modificar
        
        selected_item = self.tree.currentItem()
        if not selected_item:
            # Si no hay ningún elemento seleccionado, agregar la prueba al final del árbol
            new_index = str(self.tree.topLevelItemCount() + 1)
            tipo_prueba = self.tipo_prueba_selector.currentText()

            contenido_html = self.limpiar_html_rico(self.contenido_prueba.toHtml())
            
            if tipo_prueba == "Número":
                unidad = self.unidad_medida.text()
                valor_min = self.valor_minimo.text()
                valor_max = self.valor_maximo.text()
                valor_obj = self.valor_objetivo.text()
                
                if not all([unidad, valor_min, valor_max, valor_obj]):
                    print("Todos los campos para el tipo 'Número' deben estar rellenos.")
                    return
                
                contenido = f"Unidad: {unidad}, Mín: {valor_min}, Máx: {valor_max}, Obj: {valor_obj}"
            else: 
                contenido = contenido_html
            
            new_item = QTreeWidgetItem([new_index, tipo_prueba, contenido])
            self.tree.addTopLevelItem(new_item)
            self.tree.setCurrentItem(new_item)
            self.contenido_prueba.clear()
            return
        
        selected_index = selected_item.text(0)
        insert_mode = self.nivel_selector.currentText()
        tipo_prueba = self.tipo_prueba_selector.currentText()


        contenido_html = self.limpiar_html_rico(self.contenido_prueba.toHtml())
        
        if tipo_prueba == "Número":
            unidad = self.unidad_medida.text()
            valor_min = self.valor_minimo.text()
            valor_max = self.valor_maximo.text()
            valor_obj = self.valor_objetivo.text()
            
            if not all([unidad, valor_min, valor_max, valor_obj]):
                print("Todos los campos para el tipo 'Número' deben estar rellenos.")
                return
            
            contenido = f"Unidad: {unidad}, Mín: {valor_min}, Máx: {valor_max}, Obj: {valor_obj}"

        else:
            contenido = contenido_html
        
        new_item = None

        if selected_index:
            selected_items = self.tree.findItems(selected_index, Qt.MatchExactly | Qt.MatchRecursive, 0)
            if selected_items:
                parent_item = selected_items[0]
                parent = parent_item.parent()

                if insert_mode == "Escribir debajo al mismo nivel":
                    if parent:
                        siblings = [parent.child(i) for i in range(parent.childCount())]
                    else:
                        siblings = [self.tree.topLevelItem(i) for i in range(self.tree.topLevelItemCount())]

                    new_index = self.obtener_siguiente_indice(parent, selected_index)
                    self.desplazar_indices(siblings, new_index)
                    
                    new_item = QTreeWidgetItem([new_index, tipo_prueba, contenido])
                    index = parent.indexOfChild(parent_item) if parent else self.tree.indexOfTopLevelItem(parent_item)
                    
                    if parent:
                        parent.insertChild(index + 1, new_item)
                    else:
                        self.tree.insertTopLevelItem(index + 1, new_item)

                elif insert_mode == "Escribir debajo en un subnivel":
                    new_index = self.obtener_siguiente_subnivel(parent_item, selected_index)
                    new_item = QTreeWidgetItem([new_index, tipo_prueba, contenido])
                    parent_item.addChild(new_item)
        else:
            new_index = str(self.tree.topLevelItemCount() + 1)
            new_item = QTreeWidgetItem([new_index, tipo_prueba, contenido])
            self.tree.addTopLevelItem(new_item)


        if new_item:
            self.tree.setCurrentItem(new_item)
        
        self.contenido_prueba.clear()

        self.actualizar_botones_historial()
        self.guardar_como_action.setEnabled(True)
        self.cerrar_action.setEnabled(True)

    def obtener_siguiente_indice(self, parent, selected_index):
        """Genera el siguiente índice disponible en el mismo nivel, considerando subniveles."""
        partes = selected_index.split(".")  # Separar niveles

        if len(partes) == 1:  # Si es un índice de primer nivel (ej: "1", "2", "3")
            try:
                return str(int(selected_index) + 1)  # Incrementar el índice principal
            except ValueError:
                return selected_index + "_err"  # Para depuración en caso de error

        else:  # Si es un subnivel (ej: "1.1", "2.3.5")
            try:
                partes[-1] = str(int(partes[-1]) + 1)  # Incrementar solo la última parte
                return ".".join(partes)  # Reunir las partes nuevamente
            except ValueError:
                return selected_index + ".1"  # Si la última parte no es un número, agregar ".1"

    def obtener_siguiente_subnivel(self, parent_item, selected_index):
        """Genera el siguiente índice en un subnivel correctamente."""
        subindices = []

        for i in range(parent_item.childCount()):
            child_index = parent_item.child(i).text(0)
            parts = child_index.split(".")
            
            if len(parts) > 1 and parts[:-1] == selected_index.split("."):
                try:
                    subindices.append(int(parts[-1]))  # Convertir solo la última parte a número
                except ValueError:
                    continue  # Ignorar valores no numéricos

        if subindices:
            return f"{selected_index}.{max(subindices) + 1}"
        else:
            return f"{selected_index}.1"
  
    def eliminar_punto(self):
        """Elimina un punto seleccionado y maneja el desplazamiento de índices si es necesario."""
        self.guardar_estado()  # Guardar estado antes de modificar
        
        selected_item = self.tree.currentItem()
        
        if not selected_item:
            print("Seleccione un punto para eliminar.")
            return
        
        parent = selected_item.parent()
        selected_index = selected_item.text(0)

        if self.checkbox_desplazar.isChecked():
            if parent:
                siblings = [parent.child(i) for i in range(parent.childCount())]
            else:
                siblings = [self.tree.topLevelItem(i) for i in range(self.tree.topLevelItemCount())]

            base_index = ".".join(selected_index.split(".")[:-1]) if "." in selected_index else selected_index

            for item in siblings:
                item_index = item.text(0)
                if self.es_mayor_o_igual(item_index, selected_index):
                    nuevo_index = self.incrementar_indice(item_index, -1)
                    item.setText(0, nuevo_index)
                    self.actualizar_subniveles(item, item_index, nuevo_index)

            if parent:
                parent.removeChild(selected_item)
            else:
                self.tree.takeTopLevelItem(self.tree.indexOfTopLevelItem(selected_item))
        else:
            selected_item.setText(1, "Eliminado")
            selected_item.setText(2, "Eliminado")

        self.actualizar_botones_historial()  # Habilita o deshabilita deshacer/rehacer según el historial

    def actualizar_botones_historial(self):
        """Habilita o deshabilita los botones de Deshacer y Rehacer según el historial."""
        self.deshacer_action.setEnabled(bool(self.historial))
        self.rehacer_action.setEnabled(bool(self.historial_redo))

    def es_mayor_o_igual(self, index_a, index_b):
        """Verifica si index_a es mayor o igual que index_b en términos de jerarquía."""
        return [int(x) for x in index_a.split(".")] >= [int(x) for x in index_b.split(".")]

    def incrementar_indice(self, index, incremento):
        """Incrementa o decrementa un índice manteniendo la jerarquía."""
        partes = [int(x) for x in index.split(".")]
        partes[-1] += incremento
        return ".".join(str(x) for x in partes)

    def actualizar_subniveles(self, item, viejo_index, nuevo_index):
        """Actualiza los índices de todos los subniveles cuando cambia un nodo padre."""
        for i in range(item.childCount()):
            child = item.child(i)
            child_index = child.text(0)

            if child_index.startswith(viejo_index):  # Solo actualizar los subniveles relacionados
                child_nuevo_index = child_index.replace(viejo_index, nuevo_index, 1)
                child.setText(0, child_nuevo_index)

                # Llamada recursiva para actualizar todos los niveles inferiores
                self.actualizar_subniveles(child, child_index, child_nuevo_index)

    def guardar_rptf(self):
        """Guarda los cambios en la base de datos."""
        try:
            if self.db_path and self.conn:
                print(f"Guardando cambios en la base de datos: {self.db_path}")

                # Limpiar la tabla antes de insertar los nuevos datos
                self.cursor.execute("DELETE FROM registros")
                print("Tabla 'registros' limpiada correctamente.")  # Depuración

                # Guardar todos los datos del árbol en la base de datos
                def guardar_nodos(item, parent_index=""):
                    """Función recursiva para guardar los nodos del árbol en la base de datos."""
                    for i in range(item.childCount()):
                        child = item.child(i)
                        indice = child.text(0)
                        tipo = child.text(1)
                        contenido = child.text(2)

                        # print(f"Guardando nodo: indice={indice}, tipo={tipo}, contenido={contenido}")  # Depuración

                        self.cursor.execute("INSERT INTO registros (indice, tipo, contenido) VALUES (?, ?, ?)",
                                        (indice, tipo, contenido))

                        # Llamada recursiva para guardar subniveles
                        guardar_nodos(child, indice)

                # Guardar elementos del primer nivel
                for i in range(self.tree.topLevelItemCount()):
                    item = self.tree.topLevelItem(i)
                    indice = item.text(0)
                    tipo = item.text(1)
                    contenido = item.text(2)

                    self.cursor.execute("INSERT INTO registros (indice, tipo, contenido) VALUES (?, ?, ?)",
                                    (indice, tipo, contenido))

                    # Guardar los hijos del elemento de primer nivel
                    guardar_nodos(item, indice)

                # Confirmar cambios en la base de datos
                self.conn.commit()
                print("Base de datos guardada exitosamente.")
            else:
                print("No hay una base de datos cargada.")
        except sqlite3.Error as e:
            print(f"Error al guardar la base de datos: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

    def guardar_rptf_como(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Guardar RPTF Como", "", "Database Files (*.db)")
        if file_name:
            nueva_conn = sqlite3.connect(file_name)
            nueva_cursor = nueva_conn.cursor()

            nueva_cursor.execute("""
                CREATE TABLE IF NOT EXISTS registros (
                    indice TEXT PRIMARY KEY,
                    tipo TEXT,
                    contenido TEXT,
                    multimedia TEXT
                )
            """)

            nueva_cursor.execute("""
                CREATE TABLE IF NOT EXISTS archivos_ole (
                    indice TEXT,
                    nombre TEXT,
                    contenido BLOB,
                    PRIMARY KEY (indice, nombre)
                )
            """)

            nueva_cursor.execute("DELETE FROM registros")
            nueva_cursor.execute("DELETE FROM archivos_ole")

            def guardar_nodos(item):
                for i in range(item.childCount()):
                    child = item.child(i)
                    indice = child.text(0)
                    tipo = child.text(1)
                    contenido = child.text(2)
                    multimedia = child.text(3)

                    nueva_cursor.execute("INSERT INTO registros (indice, tipo, contenido, multimedia) VALUES (?, ?, ?, ?)",
                                        (indice, tipo, contenido, multimedia))
                    
                    if multimedia:
                        for ruta in multimedia.split(", "):
                            ruta = ruta.strip()
                            if os.path.exists(ruta):
                                nombre = os.path.basename(ruta)
                                with open(ruta, "rb") as f:
                                    binario = f.read()
                                    nueva_cursor.execute("INSERT OR REPLACE INTO archivos_ole (indice, nombre, contenido) VALUES (?, ?, ?)",
                                                         (indice, nombre, binario))
                    guardar_nodos(child)

            for i in range(self.tree.topLevelItemCount()):
                item = self.tree.topLevelItem(i)
                indice = item.text(0)
                tipo = item.text(1)
                contenido = item.text(2)
                multimedia = item.text(3)

                nueva_cursor.execute("INSERT INTO registros (indice, tipo, contenido, multimedia) VALUES (?, ?, ?, ?)",
                                    (indice, tipo, contenido, multimedia))
                guardar_nodos(item)

            nueva_conn.commit()
            nueva_conn.close()
            self.db_path = file_name
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.guardar_action.setEnabled(True)

    def deserializar_arbol(self, estado_serializado):
        """Restaura el estado del árbol desde una versión serializada, incluyendo la expansión de los nodos."""
        self.tree.clear()

        # Lista para almacenar los nodos que deben expandirse después
        nodos_a_expandir = []

        def agregar_nodos(parent, nodo_data):
            item = QTreeWidgetItem([nodo_data["indice"], nodo_data["tipo"], nodo_data["contenido"]])
            
            if parent:
                parent.addChild(item)
            else:
                self.tree.addTopLevelItem(item)

            # Si el nodo estaba expandido, lo agregamos a la lista
            if nodo_data["expandido"]:
                nodos_a_expandir.append(item)

            for hijo in nodo_data["hijos"]:
                agregar_nodos(item, hijo)

        nodos_recuperados = pickle.loads(estado_serializado)
        for nodo in nodos_recuperados:
            agregar_nodos(None, nodo)

        # 🔹 Asegurar que los nodos expandibles se expandan después de que el árbol se ha restaurado
        for nodo in nodos_a_expandir:
            nodo.setExpanded(True)

    def serializar_arbol(self):
        """Convierte el estado del árbol en un objeto serializable, incluyendo la expansión de los nodos."""
        def obtener_nodos(item):
            return {
                "indice": item.text(0),
                "tipo": item.text(1),
                "contenido": item.text(2),
                "expandido": item.isExpanded(),  # Guardamos el estado de expansión
                "hijos": [obtener_nodos(item.child(i)) for i in range(item.childCount())]
            }

        return pickle.dumps([obtener_nodos(self.tree.topLevelItem(i)) for i in range(self.tree.topLevelItemCount())])

    def guardar_estado(self):
        """Guarda el estado actual del árbol en la pila de historial con límite de 5 pasos."""
        estado_actual = self.serializar_arbol()
        self.historial.append(estado_actual)
        
        if len(self.historial) > self.max_historial:
            self.historial.pop(0)  # Mantener solo los últimos 5 estados
        
        self.historial_redo.clear()  # Limpiamos el historial de rehacer
        self.actualizar_botones_historial()

    def deshacer(self):
        """Deshace el último cambio en el árbol, manteniendo la expansión de los nodos."""
        if self.historial:
            estado_anterior = self.historial.pop()
            self.historial_redo.append(self.serializar_arbol())  # Guardar el estado actual antes de deshacer
            self.deserializar_arbol(estado_anterior)

        self.actualizar_botones_historial()
        self.repaint()  # 🔹 Forzar actualización de la interfaz si es necesario

    def rehacer(self):
        """Rehace el último cambio en el árbol si hay cambios deshechos, manteniendo la expansión de los nodos."""
        if self.historial_redo:
            estado_siguiente = self.historial_redo.pop()
            self.historial.append(self.serializar_arbol())  # Guardar el estado actual antes de rehacer
            self.deserializar_arbol(estado_siguiente)

        self.actualizar_botones_historial()
        self.repaint()  # 🔹 Forzar actualización de la interfaz si es necesario

    def editar_elemento(self, item):
        """Carga el contenido del elemento seleccionado en el campo de edición."""
        self.contenido_prueba.setText(item.text(2))
        self.btn_agregar.setText("Confirmar edición")
        self.btn_agregar.clicked.disconnect()
        self.btn_agregar.clicked.connect(lambda: self.confirmar_edicion(item))

    def confirmar_edicion(self, item):
        """Confirma la edición y actualiza el contenido del elemento en el árbol."""

        print("SACAMOS EL RAW  DE TOHTML DEL SELF CONTENIDO: ", self.contenido_prueba.toHtml())
        nuevo_contenido = self.limpiar_html_rico(self.contenido_prueba.toHtml())

        print("TEXTO REPARADO: ", nuevo_contenido)

        item.setText(2, nuevo_contenido)
        self.btn_agregar.setText("Agregar Prueba")
        self.btn_agregar.clicked.disconnect()
        self.btn_agregar.clicked.connect(self.agregar_prueba)
        self.contenido_prueba.clear()

    def mostrar_menu_contextual(self, pos):
        """Muestra el menú contextual al hacer clic derecho en un elemento del árbol."""
        item = self.tree.itemAt(pos)
        if item:
            menu = QMenu(self)

            # Opción de editar
            editar_action = menu.addAction("Editar")
            editar_action.triggered.connect(lambda: self.editar_elemento(item))

            # Opción de copiar
            copiar_action = menu.addAction("Copiar")
            copiar_action.triggered.connect(lambda: self.copiar_elemento(item))

            # Opción de pegar (solo disponible si hay un elemento copiado)
            if self.elemento_copiado:
                pegar_menu = menu.addMenu("Pegar")
                pegar_debajo_mismo_nivel = pegar_menu.addAction("Pegar debajo al mismo nivel")
                pegar_arriba_mismo_nivel = pegar_menu.addAction("Pegar arriba al mismo nivel")
                pegar_debajo_subnivel = pegar_menu.addAction("Pegar debajo en un subnivel")

                pegar_debajo_mismo_nivel.triggered.connect(lambda: self.pegar_elemento(item, "debajo_mismo_nivel"))
                pegar_arriba_mismo_nivel.triggered.connect(lambda: self.pegar_elemento(item, "arriba_mismo_nivel"))
                pegar_debajo_subnivel.triggered.connect(lambda: self.pegar_elemento(item, "debajo_subnivel"))

            menu.exec(self.tree.viewport().mapToGlobal(pos))

    def actualizar_interfaz_tipo_prueba(self):
        """Actualiza la interfaz según el tipo de prueba seleccionado."""
        tipo_prueba = self.tipo_prueba_selector.currentText()
        
        # Ocultar todos los campos adicionales
        self.unidad_medida.setVisible(False)
        self.valor_minimo.setVisible(False)
        self.valor_maximo.setVisible(False)
        self.valor_objetivo.setVisible(False)
        
        if tipo_prueba == "Número":
            self.unidad_medida.setVisible(True)
            self.valor_minimo.setVisible(True)
            self.valor_maximo.setVisible(True)
            self.valor_objetivo.setVisible(True)
        elif tipo_prueba in ["Texto estático", "Si/No", "Texto"]:
            self.contenido_prueba.setVisible(True)

    def show_preferences(self):
        # Mostrar la ventana de preferencias
        self.config_window.show()

    def get_question_type(self, tal_object_type, object_heading, object_text):
        if tal_object_type == "N/A":
            if object_heading.strip():  # Si hay texto en object_heading, es un título
                return "Título"
            else:  # Si no, es texto estático
                return "Texto estático"
        elif tal_object_type == "Test":
            return "Texto"
        elif tal_object_type == "Step":
            return "Si/No"
        else:
            return "Texto plano"

    def get_content(self, tal_object_type, object_heading, object_text):
        if tal_object_type == "N/A":
            if object_heading.strip():  # Si es un título, usar el heading
                return object_heading
            else:  # Si es texto estático, usar el texto
                return self.format_content(object_text)  # Formatear el contenido
        else:
            return self.format_content(object_text)  # Formatear el contenido

    def format_content(self, object_text):
        formatted_text = str(object_text)
        # Añadir un margen inferior a las imágenes
        formatted_text = formatted_text.replace("<img", '<img style="margin-top: 0px; margin-bottom: 0px;"')
        return formatted_text

    def get_multimedia(self, object_text):
        images = object_text.find_all('img')  # Encontrar todas las etiquetas <img>
        if images:
            img_abs_paths = []  # Lista para almacenar las rutas absolutas de las imágenes
            for img in images:
                img_src = img['src']
                if hasattr(self, 'html_file_path'):  # Verificar si la ruta del archivo HTML está definida
                    html_dir = os.path.dirname(self.html_file_path)  # Obtener el directorio del archivo HTML
                    img_abs_path = os.path.join(html_dir, img_src)  # Construir la ruta absoluta de la imagen
                    img_abs_path = os.path.normpath(img_abs_path)

                    # Reemplazar la ruta relativa con la ruta absoluta en el object_text
                    img['src'] = img_abs_path

                    img_abs_paths.append(img_abs_path)  # Agregar la ruta absoluta a la lista
                else:
                    img_abs_paths.append(img_src)  # Si no hay ruta de archivo HTML, usar la ruta relativa

            return img_abs_paths  # Devolver la lista de rutas absolutas
        return None  # Si no hay imágenes, devolver None

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Abrir Archivo HTML", "", "Archivos HTML (*.htm *.html)")
        if file_path:
            self.parse_html(file_path)

    def parse_html(self, file_path):
        import re

        self.html_file_path = file_path  # Guardar la ruta del archivo HTML
        with open(file_path, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")

        rows = soup.find_all('tr')[1:]  # Ignorar la primera fila (encabezados)
        items_dict = {}

        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 4:
                continue

            tal_object_type = cols[0].text.strip()
            object_number = cols[1].text.strip()
            object_heading = cols[2].text.strip()
            object_text = cols[3]


            # 🔹 Eliminar <div> vacíos o irrelevantes
            for div in object_text.find_all("div"):
                if not div.get_text(strip=True) and not div.find(True):  # sin texto y sin hijos útiles
                    div.decompose()

            # 🔹 Eliminar etiquetas internas innecesarias
            for tag in object_text.find_all(['table', 'tr', 'td']):
                tag.unwrap()

            # 🔹 Eliminar párrafos vacíos
            for p in object_text.find_all('p'):
                if not p.get_text(strip=True):
                    p.decompose()

            # 🔹 Convertir el tag a string
            html = str(object_text).strip()

            # 🔹 Quitar etiquetas <td> si envuelven todo
            if html.lower().startswith("<td>") and html.lower().endswith("</td>"):
                html = html[4:-5].strip()

            # 🔹 Eliminar múltiples <br> o </br> al final
            # print("ANTES:", repr(html[-50:]))  # Muestra el final del HTML original
            html = re.sub(r'(<br\s*/?>|</br>|\s|&nbsp;|<!--.*?-->)+$', '', html, flags=re.IGNORECASE)
            # print("DESPUÉS:", repr(html[-50:]))  # Confirma si se ha limpiado

            # 🔹 Volver a parsear el HTML limpio
            object_text = BeautifulSoup(html, "html.parser")

            # 🔹 Obtener multimedia y contenido limpio
            multimedia_list = self.get_multimedia(object_text)
            question_type = self.get_question_type(tal_object_type, object_heading, object_text)
            content = self.get_content(tal_object_type, object_heading, object_text)
            multimedia = ", ".join(multimedia_list) if multimedia_list else ""

            # 🔹 Crear ítem del árbol
            item = QTreeWidgetItem([object_number, question_type, "", multimedia])
            item.setData(2, Qt.DisplayRole, content)

            # Añadir al árbol
            parent_number = ".".join(object_number.split(".")[:-1])
            parent_item = items_dict.get(parent_number)

            if parent_number and parent_item:
                parent_item.addChild(item)
            else:
                self.tree.addTopLevelItem(item)

            items_dict[object_number] = item

        # 🔹 Ajustar la interfaz
        self.adjust_row_heights()
        self.adjust_content_column_width()
        self.guardar_como_action.setEnabled(True)
        self.cerrar_action.setEnabled(True)

        self.tree.resizeColumnToContents(0)
        self.tree.resizeColumnToContents(1)

    def adjust_row_heights(self):
        # Ajustar el alto de todas las filas visibles
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            self.adjust_item_height(item)

    def adjust_item_height(self, item):
        delegate = self.tree.itemDelegateForColumn(2)  # Obtener el delegate de la columna "Contenido"
        if isinstance(delegate, HTMLDelegate):
            index = self.tree.indexFromItem(item, 2)

            # Crear un QStyleOptionViewItem válido
            option = QStyleOptionViewItem()
            option.rect = self.tree.visualRect(index)  # Obtener el rectángulo visible

            # Obtener el ancho actual de la columna
            column_width = self.tree.columnWidth(2)
            option.rect.setWidth(column_width)  # Asegurar que el QTextDocument use el ancho correcto

            # Calcular el tamaño ideal del contenido HTML
            size_hint = delegate.sizeHint(option, index)
            
            # Ajustar la altura del ítem
            item.setSizeHint(2, QSize(column_width, size_hint.height()))

        # Ajustar también los hijos del ítem si los hay
        for i in range(item.childCount()):
            self.adjust_item_height(item.child(i))

    def adjust_content_column_width(self):
        max_width = 0
        max_item = None  # Para almacenar el ítem con el contenido más ancho

        # Recorrer TODOS los elementos (padres e hijos)
        def traverse_items(item):
            nonlocal max_width, max_item
            for col in range(self.tree.columnCount()):  # Verificar cada columna
                item_width = self.calculate_item_width(item, col)
                if item_width > max_width:
                    max_width = item_width
                    max_item = item  # Actualizar el ítem más ancho

            # Recorrer los hijos del ítem
            for i in range(item.childCount()):
                traverse_items(item.child(i))

        # Recorrer todos los elementos de nivel superior
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            traverse_items(item)

        # Obtener el valor de la columna 0 del ítem más ancho
        if max_item is not None:
            index_value = max_item.text(0)  # Obtener el valor de la columna 0
            print(f"El ítem más ancho tiene el índice: {index_value}")
        else:
            index_value = None
            print("No se encontró ningún ítem con contenido.")

        # Ajustar el ancho de la columna de contenido
        if max_width > 0:
            self.tree.setColumnWidth(2, max_width)  # Ajustar el ancho de la columna 2

        return index_value  # Devolver el valor de la columna 0

    def adjust_column_widths_on_expand(self, item):
        # Ajustar el ancho de las columnas 0 y 1 al contenido
        self.tree.resizeColumnToContents(0)  # Columna 0
        self.tree.resizeColumnToContents(1)  # Columna 1

    def calculate_item_width(self, item, column):
        delegate = self.tree.itemDelegateForColumn(column)
        if isinstance(delegate, HTMLDelegate):
            index = self.tree.indexFromItem(item, column)

            # Crear un documento HTML con el contenido del item
            html_content = index.data(Qt.DisplayRole)
            if not html_content:
                return 0

            document = QTextDocument()
            document.setHtml(html_content)

            # Obtener el ancho ideal del contenido sin restricciones de ancho
            return int(document.idealWidth()) + 10  # Margen extra

        return 0

    def generar_pdf_con_weasyprint(self):

        # Ruta al logo
        abs_path_logo = os.path.abspath("images/Talgo_logo.png")
        logo_url = f"file:///{abs_path_logo.replace(os.sep, '/')}"

        # Procesamiento del árbol
        def procesar_item(item, nivel=0):
            index = item.text(0)
            tipo = item.text(1)
            contenido = item.text(2)

            # Indentación según nivel
            if tipo == "Título":
                margin_left = 20 * nivel
            else: 
                margin_left = 0
            # Clase CSS según tipo
            clase_tipo = "punto"
            if tipo == "Título":
                clase_tipo += "-titulo"
            elif tipo=="Texto estático":
                clase_tipo += "-estatico"
            elif tipo == "Si/No":
                clase_tipo += "-sino"
            elif tipo == "Texto":
                clase_tipo += "-texto"
            # Reemplazar rutas de imágenes dentro del contenido
            def sustituir_ruta_imagenes(match):
                src = match.group(1)
                # Si ya es absoluta y empieza con file://, déjalo igual
                if src.startswith("file://"):
                    return f'src="{src}"'
                abs_path_img = os.path.abspath(src)
                return f'src="file:///{abs_path_img.replace(os.sep, "/")}"'

            contenido = re.sub(r'src="([^"]+)"', sustituir_ruta_imagenes, contenido)

            def simplificar_imagen(match):
                align = match.group(1)
                margin_top = match.group(2)
                margin_bottom = match.group(3)
                src = match.group(4)
                width = match.group(5)

                width_val = re.findall(r'\d+', width)
                width_val = width_val[0] if width_val else "100"

                return (
                    f'<div style="text-align: {align}; margin-top: {margin_top}px; margin-bottom: {margin_bottom}px;">'
                    f'<img style="width: {width_val}px;" src="{src}"/></div>'
                )


            # Regex que captura text-align opcional, y siempre src y width
            contenido = re.sub(
                r'<div[^>]*?text-align:\s*(\w+)[^>]*?margin-top:\s*(\d+)px;[^>]*?margin-bottom:\s*(\d+)px;[^>]*?>\s*'
                r'<img[^>]*?src="([^"]+)"[^>]*?width="([^"]+)"[^>]*?>\s*</div>',
                simplificar_imagen,
                contenido,
                flags=re.IGNORECASE
                )



            contenido = re.sub(r'</?(td|tr|table)[^>]*>','', contenido, flags=re.IGNORECASE)

            # HTML del bloque

            if tipo == "Título":
                bloque = f"""
                <div class="{clase_tipo}" style="margin-left: {margin_left}px;">
                    {index} - {contenido}
                </div>
                """
            elif tipo == "Texto estático":
                bloque = f"""
                <div class="{clase_tipo}" style="margin-left: {margin_left}px;">
                    {contenido}
                </div>
                """
            else:
                bloque = f"""
                <div class="{clase_tipo}" style="margin-left: {margin_left}px;">
                    {index} - {contenido}
                </div>
                """

            # Recursividad para los hijos
            for i in range(item.childCount()):
                bloque += procesar_item(item.child(i), nivel + 1)

            return bloque


        # HEADER HTML con llaves dobles
        header_html = """
        <div id="header" class="header-container">
            <div class="header-box">
                <div class="logo-area">
                    <img src="{logo_url}" alt="Logo">
                </div>
                <div class="middle-area">
                    <div class="registro-encabezado">
                        <span>REGISTRO DE PRUEBAS /</span>
                        <i>TEST RECORD</i>
                    </div>
                    <div class="registro-inferior">
                        <div class="registro-info">
                            <div class="registro-codigo">{reg_code}</div>
                            <div class="registro-label">Código<br><i>Code</i></div>
                        </div>
                        <div class="version-info">
                            <div class="version-numero">1.0</div>
                            <div class="version-label">Versión<br><i>Version</i></div>
                        </div>
                    </div>
                </div>                    
                <div class="pagina-area">
                    <div class="pagina-label">PÁGINA<br><i>PAGE</i></div>
                    <div class="pagina-numero">
                        <span class="page-number"></span> de <span class="page-count"></span>
                    </div>
                </div>
            </div>
        </div>
        """

        # Sustituir variables en el header
        header_html_render = header_html.format(
            logo_url=logo_url,
            reg_code=reg_code,
        )

        footer = """
        <div id="footer" class="footer-container">
            <div class="footer-box">
                <div class="footer-text">
                    Este documento y su contenido son propiedad de Patentes Talgo S.L.U. o sus filiales. Este documento contiene información confidencial privada. La reproducción, distribución, utilización o comunicación de este documento o parte de él, sin autorización expresa, está estrictamente prohibida. Aquellos que contravengan esta disposición se considerarán responsables del pago de los daños causados. / <i>Dieses Dokument und sein Inhalt si nd Eigentum von Patentes Talgo S.L.U. oder seiner Tochtergesellschaften. Dieses Dokument enthält vertraul iche und pr ivate Informati onen. Di e vollständige oder teilweise Vervielfältigung, Verbreitung, Verwendung oder Weitergabe dieses Dokuments ohne Genehmi gung von Talgo ist strengstens verboten. Personen, die gegen diese Bestimmung verstoßen, werden für die entstandenen Schäden haftbar gemacht</i>"
                </div>
            </div>
        </div>
        """

        # PORTADA
        titulo = f"""
        <section class="titulo">
            <h1>{reg_tit_esp} / <i>{reg_tit_tra}</i></h1>
        </section>
        """

        # TABLA DE VEHÍCULOS
        tabla_vehiculo = """
            <table class="tabla-coche" border="1" cellspacing="0" cellpadding="4">
                <tr>
                    <th></th>
                    <th>C4302P</th><th>C4302S</th><th>C4302C</th><th>C4322</th>
                    <th>C4315</th><th>C4314</th><th>C4301P</th><th>C4306</th>
                    <th>C4328</th><th>C4340</th><th>L9215</th>
                    <th>COMP<br><i>ZUGV</i></th>
                    <th>TREN<br><i>ZUG</i></th>
                </tr>
                <tr><td><b>F073</b></td>""" + \
            "".join('<td class="selected"></td>' if tipo == coach_type else '<td></td>' for tipo in tipos_F073) + \
            "</tr></table>"

        # TABLA FIRMAS Y AVANCES
        tabla_firmas = """
            <table class="tabla-titulo-ajustada" cellspacing="0" cellpadding="4">
                <tr>
                    <td>
                        COCHE / MOTRIZ / COMPOSICIÓN / TREN<br>
                        <i>CAR / POWER HEAD / COACHSET / TRAIN</i>
                    </td>
                    <td class="columna-fija"></td>
                </tr>
            </table>

            <table class="tabla-firmas" cellspacing="0" cellpadding="4">
                <!-- Fila de título -->
                <tr>
                    <td colspan="6">
                        CONTROL DE FIRMAS PUESTA EN SERVICIO / 
                        <i>COMMISSIONING SIGNATURES CONTROL</i>
                    </td>
                </tr>
                <!-- Fila de subtítulos -->
                <tr class="fila-subtitulos">
                    <td>NOMBRE<br><i>NAME</i></td>
                    <td>FECHA<br><i>DATE</i></td>
                    <td>FIRMA<br><i>SIGNATURE</i></td>
                    <td>PUNTOS PENDIENTES<br><i>PENDING POINTS</i></td>
                    <td>%REALIZADO<br><i>%COMPLETED</i></td>
                    <td></td> <!-- columna extra por si se quiere -->
                </tr>
                <!-- Filas vacías -->
                <tr><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                <tr><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                <tr><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                <tr><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                <tr><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                <tr><td></td><td></td><td></td><td></td><td></td><td></td></tr>
            </table>
        """
        # CONTENIDO
        contenido = "<section class='page-break'>"
        for i in range(self.tree.topLevelItemCount()):
            contenido += procesar_item(self.tree.topLevelItem(i))

        # test = """<div class="punto-sino">
        #             Esto es una prueba de texto, prueba de texto. es una prueba de texto, prueba de texto. es una prueba de texto, prueba de texto. es una prueba de texto, prueba de texto. es una prueba de texto, prueba de texto. es una prueba de texto, prueba de texto. es una prueba de texto, prueba de texto. es una prueba de texto, prueba de texto.
        #             <div style="text-align: right;">
        #             <img src="file:///C:/Users/75815/Desktop/SW PES/T-REX/images/color_icon.png" style="width: 80px;"/></div>
        #             Esto es una prueba de texto, prueba de texto. es una prueba de texto, prueba de texto. es una prueba de texto, prueba de texto. es una prueba de texto, prueba de texto. es una prueba de texto, prueba de texto. es una prueba de texto, prueba de texto. es una prueba de texto, prueba de texto. es una prueba de texto, prueba de texto.
        #             <div style="text-align: left; margin-top:0px;">
        #             <img src="file:///C:/Users/75815/Desktop/SW PES/T-REX/images/color_icon.png" style="width: 80px;"/></div>
        #             Esto es una prueba de texto, prueba de texto. es una prueba de texto, prueba de texto. es una prueba de texto, prueba de texto. es una prueba de texto, prueba de texto. es una prueba de texto, prueba de texto. es una prueba de texto, prueba de texto. es una prueba de texto, prueba de texto. es una prueba de texto, prueba de texto.
        #             <div style="text-align: center; margin-top:20px;">
        #             <img src="file:///C:/Users/75815/Desktop/SW PES/T-REX/images/color_icon.png" style="width: 80px;"/></div>
        #             Esto es una prueba de texto, prueba de texto. es una prueba de texto, prueba de texto. es una prueba de texto, prueba de texto. es una prueba de texto, prueba de texto. es una prueba de texto, prueba de texto. es una prueba de texto, prueba de texto. es una prueba de texto, prueba de texto. es una prueba de texto, prueba de texto.
        #           </div>"""

        # test = """<div class="punto-sino">
        #     <div style="text-align: center; margin-top:5px; margin-bottom: 5px">
        #     <table style="width: 80%; margin-left: auto; margin-right: auto; border-collapse: collapse; border: 1px solid black;">
        #         <tr>
        #         <td style="border: 1px solid black; padding: 4px;">Celda</td>
        #         <td style="border: 1px solid black; padding: 4px;">Celda</td>
        #         <td style="border: 1px solid black; padding: 4px;">Celda</td>
        #         <td style="border: 1px solid black; padding: 4px;">Celda</td>
        #         <td style="border: 1px solid black; padding: 4px;">Celda</td>
        #         <td style="border: 1px solid black; padding: 4px;">Celda</td>
        #         </tr>
        #         <tr>
        #         <td style="border: 1px solid black; padding: 4px;"><b>NEGRITA</b></td>
        #         <td style="border: 1px solid black; padding: 4px;"><i>CURSIVA</i></td>
        #         <td style="border: 1px solid black; padding: 4px;"><u>SUBRAYADO</u></td>
        #         <td style="border: 1px solid black; padding: 4px; color: blue;"><b><i><u>TODO A LA VEZ</u></i></b></td>
        #         <td style="border: 1px solid black; padding: 4px;">Celda</td>
        #         <td style="border: 1px solid black; padding: 4px;">Celda</td>
        #         </tr>
        #         <tr>
        #         <td style="border: 1px solid black; padding: 4px;">Celda</td>
        #         <td style="border: 1px solid black; padding: 4px;">Celda</td>
        #         <td style="border: 1px solid black; padding: 4px;">Celda</td>
        #         <td style="border: 1px solid black; padding: 4px;">Celda</td>
        #         <td style="border: 1px solid black; padding: 4px;">Celda</td>
        #         <td style="border: 1px solid black; padding: 4px;">Celda</td>
        #         </tr>
        #     </table>
        #     </div>
        #     </div>
        #     """
        # contenido += test


        # CSS
        html = f"""
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                @page {{
                    size: A4;
                    margin-top: 5.5cm;
                    margin-left: 2cm;
                    margin-right: 2cm;
                    margin-bottom: 2.5cm;
                    
                    @top-center {{
                        content: element(header);
                    }}
                    @bottom-center{{
                        content: element(footer);
                    }}
                }}
                body {{
                    font-family: Calibri, Arial, sans-serif;
                    /*background-color: rgba(0, 0, 255, 0.4);*/
                }}
                #header {{
                    position: running(header);
                    height: 2.5cm;
                    width: 17cm;
                    margin: 0 auto;
                }}
                #footer {{
                    position: running(footer);
                    width: 100%;
                    height: 2.5cm;
                    font-size: 8px;
                    text-align: justify;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: rgba(0, 0, 0, 0.4);
                    /* background-color: #f9f9f9; */
                }}
                .header-box {{
                    margin-top: 0.5cm;
                    width: 100%;
                    height: 2.5cm;
                    display: flex;
                    border: 1px solid black;
                    box-sizing: border-box;
                }}
                .logo-area {{
                    height: 2.5cm;
                    width: 3.5cm;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    /* background: rgba(0, 0, 255, 0.4); color de fondo visible */
                }}
                .logo-area img{{
                    max-width: 90%;
                    padding-left: 4px;
                    padding-top: 1px;
                }}
                .middle-area {{
                    width: 11cm;
                    height: 100%;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    box-sizing: border-box;
                    border-right: 1px solid black;
                    border-left: 1px solid black;
                    /* background: rgba(255, 0, 0, 0.1); color de fondo visible */
                }}
                .registro-encabezado {{
                    font-weight: bold;
                    font-size: 16px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    height: 1cm;
                    width: 100%;
                    /*  background: rgba(0, 255, 0, 0.4); color de fondo visible */
                    box-sizing: border-box;
                    border-bottom: 1px solid black;
                    gap: 4.5px;
                    
                }}
                .registro-inferior {{
                    width: 11cm;
                    height: 1.5cm;
                    display: flex;
                    align-items: center;
                }}
                .registro-info {{
                    width: 9cm;
                    height: 100%;
                    text-align: center;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                }}
                .version-info {{
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    width: 2cm;
                    height: 100%;
                    text-align: center;
                    border-left: 1px solid black;
                    /*  background: rgba(0, 0, 255, 0.4); color de fondo visible */
                }}
                .registro-codigo, .version-numero {{
                    margin-bottom: 0.1cm;
                    font-weight: bold;
                    font-size: 16px;
                }}
                .registro-label, .version-label {{
                    font-size: 10px;
                }}
                .titulo{{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    text-align: center;
                    font-size: 14pt;
                    font-weight: bold;
                }}
                .pagina-area {{
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    text-align: center;
                    font-size: 9pt;
                    width: 2.5cm;
                }}
                .pagina-label {{
                    margin-bottom: 0.2cm;
                }}
                .page-number::after{{
                    content: counter(page);
                }}
                .page-count::after{{
                    content: counter(pages);
                }}
                .page-break {{
                    page-break-before: always;
                }}
                .tabla-coche {{
                    border-collapse: collapse;
                    width: 100%;
                    font-size: 12px;
                    font-family: Calibri, sans-serif;
                    margin: 2cm auto;
                }}
                .tabla-coche td.selected {{
                    background-color: rgba(0, 0, 0, 1);
                }}
                .tabla-coche th, .tabla-coche td {{
                    height: 20px;
                    vertical-align: middle;
                    text-align: center;
                    border: 1px solid black;
                    padding: 4px;
                    font-style: italic;
                }}
                .tabla-titulo-ajustada {{
                    font-family: Calibri, Arial, sans-serif;
                    font-size: 12px;
                    border-collapse: collapse;
                    margin-top: 1cm;
                    width: auto;
                    margin-left: 0; /* Alineada a la izquierda */
                    margin-bottom: 0; 
                }}
                .tabla-titulo-ajustada td {{
                    padding: 6px;
                    border: 1px solid black;
                    border-bottom: none;
                    height: 100%;
                }}
                .tabla-titulo-ajustada .columna-fija {{
                    width: 3cm;
                }}
                .tabla-firmas {{
                    font-family: Calibri, Arial, sans-serif;
                    font-size: 12px;
                    border-collapse: collapse;
                    border: 1px solid black;
                    width: 100%;
                    margin: 0;
                }}
                .tabla-firmas td {{
                    padding: 6px;
                    height: 0.6cm;
                    vertical-align: middle;
                    text-align: center;
                    border-top: 1px solid black;
                    border-bottom: 1px solid black;
                }}
                .punto-titulo {{
                    font-family: Calibri;
                    font-size: 11px;
                    font-weight: bold;
                    margin-bottom: 6px;
                    margin-top: 6px;
                    text-decoration: underline;
                }}
                .punto-sino {{
                    width: 100%;
                    font-family: Calibri;
                    font-size: 11px;
                    text-align: justify;   
                    box-sizing: border-box;
                    border: 1px solid black;
                    margin: -1px 0 0 0; 
                    padding: 4px;
                    line-height: 1.35;
                    font-weight: 400;
                }}
                .punto-texto {{
                    width: 100%;
                    font-family: Calibri;
                    font-size: 11px;
                    text-align: justify;   
                    box-sizing: border-box;
                    border: 1px solid black;
                    margin: 0; 
                    padding: 4px;
                    line-height: 1.35;
                    font-weight: 400;
                }}
                .punto-estatico {{
                    width: 100%;
                    font-family: Calibri;
                    font-size: 11px;
                    text-align: justify;
                    font-weight: normal;
                    line-height: 1.35;
                    font-weight: 400;
                }}
            </style>
        </head>
        <body>
            {header_html_render}
            {footer}
            {titulo}
            {tabla_vehiculo}
            {tabla_firmas}
            {contenido}
        </body>
        </html>
        """
        # print(contenido)

        # Exportar a PDF
        output_path = os.path.join(tempfile.gettempdir(), "preview_output.pdf")
        HTML(string=html, base_url=".").write_pdf(output_path)
        return output_path

    def mostrar_html_preview(self):
        import webbrowser
        pdf_path = self.generar_pdf_con_weasyprint()
        webbrowser.open(f"file:///{pdf_path}")

class PreferencesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.config_window()

    def config_window(self):
        # Configuración básica de la ventana
        self.setWindowTitle("Preferencias")
        self.setGeometry(100, 100, 800, 600)

        # Evitar que la ventana se destruya al cerrarse
        self.setAttribute(Qt.WA_DeleteOnClose, False)

        # Layout principal
        self.config_layout = QHBoxLayout(self)

        # Lista de ajustes seleccionables a la izquierda
        self.settings_list = QListWidget()
        self.settings_list.addItems(["Documento"])
        self.settings_list.currentRowChanged.connect(self.change_setting)
        self.config_layout.addWidget(self.settings_list)

        # Área dinámica a la derecha
        self.stacked_widget = QStackedWidget()
        self.config_layout.addWidget(self.stacked_widget)

        # Crear las páginas de configuración
        # self.create_general_page()
        self.create_document_page()
        # self.create_accounts_page()

    def create_general_page(self):
        # Página de configuración general
        general_page = QWidget()
        layout = QFormLayout()

        layout.addRow("Nombre de usuario:", QLineEdit())
        layout.addRow("Idioma:", QLineEdit())
        layout.addRow(QLabel("Opciones avanzadas:"))
        layout.addRow("Habilitar logs", QCheckBox())

        general_page.setLayout(layout)
        self.stacked_widget.addWidget(general_page)

    def actualizar_tipos_vehiculo(self, proyecto_seleccionado):
        # Limpiar el combo de tipos de vehículo
        self.tipo_vehiculo_combo.clear()

        # Definir los tipos de vehículo según el proyecto seleccionado
        if proyecto_seleccionado == "F073":
            self.tipo_vehiculo_combo.addItems(["L9215", "C4301P", "C4302C", "C4302P", "C4302S", "C4306", "C4314", "C4315", "C4322", "C4328", "C4340"])
        # elif proyecto_seleccionado == "F081":
        #     self.tipo_vehiculo_combo.addItems(["Bicicleta", "Patineta", "Autobús"])
        # elif proyecto_seleccionado == "F083":
        #     self.tipo_vehiculo_combo.addItems(["Avión", "Barco", "Tren"])

    def create_document_page(self):
        # Página de configuración de apariencia
        document_page = QWidget()
        layout = QFormLayout()

        proyecto_label = QLabel("Proyecto:")
        self.proyecto_combo = QComboBox()
        self.proyecto_combo.addItems(["F073", "F081"])
        self.proyecto_combo.currentTextChanged.connect(self.actualizar_tipos_vehiculo)

        tipo_vehiculo_label = QLabel ("Tipo de vehículo:")
        self.tipo_vehiculo_combo = QComboBox()


        layout.addRow("Nombre (Código del registro):", QLineEdit())
        layout.addRow(proyecto_label, self.proyecto_combo)
        layout.addRow(tipo_vehiculo_label, self.tipo_vehiculo_combo)
        layout.addRow("Revisión:", QLineEdit())

        # self.actualizar_tipos_vehiculo(self.proyecto)

        document_page.setLayout(layout)
        self.stacked_widget.addWidget(document_page)

    def create_accounts_page(self):
        # Página de configuración de cuentas
        accounts_page = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Configuración de cuentas:"))
        layout.addWidget(QLineEdit("Correo electrónico"))
        layout.addWidget(QLineEdit("Contraseña"))

        accounts_page.setLayout(layout)
        self.stacked_widget.addWidget(accounts_page)

    def change_setting(self, index):
        # Cambiar la página mostrada en función de la selección
        self.stacked_widget.setCurrentIndex(index)

class InsertarImagenDialog(QDialog):
    def __init__(self, parent=None, contenido_actual=""):

        # print("BOTON IMAGEN PULSADO: ", contenido_actual)

        super().__init__(parent)
        self.parent = parent

        self.setWindowTitle("Insertar imagen")
        self.setMinimumSize(800, 400)

        # print("CODIGO LIMPIO: ", contenido_actual)

        layout = QHBoxLayout(self)

        self.vista_previa = QTextEdit()
        self.vista_previa.setReadOnly(True)
        layout.addWidget(self.vista_previa, 1)

        panel_derecho = QVBoxLayout()

        self.html_edit = QTextEdit()
        self.html_edit.setPlainText(contenido_actual)
        panel_derecho.addWidget(QLabel("Código HTML:"))
        panel_derecho.addWidget(self.html_edit, 1)

        form_layout = QFormLayout()

        self.input_ancho = QLineEdit()
        self.input_ancho.setPlaceholderText("px")
        form_layout.addRow("Ancho:", self.input_ancho)

        self.input_alto = QLineEdit()
        self.input_alto.setPlaceholderText("px")
        form_layout.addRow("Alto:", self.input_alto)

        self.input_margin_top = QLineEdit()
        self.input_margin_top.setPlaceholderText("px")
        form_layout.addRow("Margen superior:", self.input_margin_top)

        self.input_margin_bottom = QLineEdit()
        self.input_margin_bottom.setPlaceholderText("px")
        form_layout.addRow("Margen inferior:", self.input_margin_bottom)

        self.combo_alineacion = QComboBox()
        self.combo_alineacion.addItems(["Ninguna", "Izquierda", "Centro", "Derecha"])
        form_layout.addRow("Alineación:", self.combo_alineacion)

        self.boton_imagen = QPushButton("Seleccionar imagen")
        self.boton_imagen.clicked.connect(self.seleccionar_imagen)
        form_layout.addRow(self.boton_imagen)

        panel_derecho.addLayout(form_layout)

        self.boton_aplicar = QPushButton("Aplicar")
        self.boton_aplicar.clicked.connect(self.aplicar)
        panel_derecho.addWidget(self.boton_aplicar)

        layout.addLayout(panel_derecho, 1)

        self.html_edit.textChanged.connect(self.actualizar_preview)
        self.actualizar_preview()

    def actualizar_preview(self):
        html = self.html_edit.toPlainText()
        self.vista_previa.setHtml(html)

    def seleccionar_imagen(self):
        file_filter =(
            "Imágenes (*.png *.jpg *.jpeg *.bmp *.gif);;"
            "Todos los archivos (*.*)"
        )
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar imagen", "", file_filter
        )
        if file_path:
            ancho = self.input_ancho.text().strip()
            alto = self.input_alto.text().strip()
            margen_superior = self.input_margin_top.text().strip()
            margen_inferior = self.input_margin_bottom.text().strip()

            width_attr = ancho if ancho else ""
            height_attr = alto if alto else ""
            
            # ruta_directa = file_path.replace("/", "\\")
            alineacion = self.combo_alineacion.currentText()

            if alineacion == "Centro":
                # Usamos <div> solo para centrar
                etiqueta_img = (
                    f'<div style="text-align: center; margin-top: {margen_superior}px; margin-bottom: {margen_inferior}px;">'
                    f'<img src="{file_path}" '
                    f'width="{width_attr}" height="{height_attr}" />'
                    f'</div>'
                )
            elif alineacion == "Izquierda":
                etiqueta_img = (
                    f'<div style="text-align: left; margin-top: {margen_superior}px; margin-bottom: {margen_inferior}px;">'
                    f'<img src="{file_path}" '
                    f'width="{width_attr}" height="{height_attr}" />'
                    f'</div>'
                )
            elif alineacion == "Derecha":
                etiqueta_img = (
                    f'<div style="text-align: right; margin-top: {margen_superior}px; margin-bottom: {margen_inferior}px;">'
                    f'<img src="{file_path}" '
                    f'width="{width_attr}" height="{height_attr}" />'
                    f'</div>'
                )

            contenido = self.html_edit.toPlainText().strip()

            self.html_edit.setPlainText(contenido + etiqueta_img)
            
    def aplicar(self):
        self.resultado = self.html_edit.toPlainText()
        self.accept()

class ConfigTablaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configuración de tabla")
        self.setMinimumWidth(300)

        layout = QVBoxLayout(self)

        self.filas_spin = QSpinBox()
        self.filas_spin.setRange(1, 100)
        self.filas_spin.setValue(3)
        self.columnas_spin = QSpinBox()
        self.columnas_spin.setRange(1, 100)
        self.columnas_spin.setValue(3)

        layout.addWidget(QLabel("Filas:"))
        layout.addWidget(self.filas_spin)
        layout.addWidget(QLabel("Columnas:"))
        layout.addWidget(self.columnas_spin)

        self.ancho_combo = QComboBox()
        self.ancho_combo.addItems(["Mínimo necesario", "Porcentaje del ancho total"])
        layout.addWidget(QLabel("Tamaño de tabla:"))
        layout.addWidget(self.ancho_combo)

        self.porcentaje_combo = QComboBox()
        self.porcentaje_combo.addItems([f"{i}%" for i in range(10, 101, 10)])
        layout.addWidget(QLabel("Porcentaje (si aplica):"))
        layout.addWidget(self.porcentaje_combo)

        self.alineacion_combo = QComboBox()
        self.alineacion_combo.addItems(["Izquierda", "Centrada", "Derecha"])
        layout.addWidget(QLabel("Alineación:"))
        layout.addWidget(self.alineacion_combo)

        self.borde_color_btn = QPushButton("Seleccionar color de borde")
        self.borde_color_btn.clicked.connect(self.elegir_color_borde)
        self.borde_color = "#000000"
        layout.addWidget(self.borde_color_btn)

        self.borde_espesor = QSpinBox()
        self.borde_espesor.setRange(1, 10)
        self.borde_espesor.setValue(1)
        layout.addWidget(QLabel("Espesor del borde:"))
        layout.addWidget(self.borde_espesor)

        aplicar_btn = QPushButton("Aplicar")
        aplicar_btn.clicked.connect(self.accept)
        layout.addWidget(aplicar_btn)

    def elegir_color_borde(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.borde_color = color.name()
            self.borde_color_btn.setStyleSheet(f"background-color: {self.borde_color};")

    def get_config(self):
        return {
            "filas": self.filas_spin.value(),
            "columnas": self.columnas_spin.value(),
            "ancho": self.ancho_combo.currentText(),
            "porcentaje": self.porcentaje_combo.currentText(),
            "alineacion": self.alineacion_combo.currentText(),
            "borde_color": self.borde_color,
            "borde_espesor": self.borde_espesor.value(),
        }

class InsertarTablaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Insertar tabla")
        self.setMinimumSize(1000, 600)

        self.configuracion_tabla = {
            "filas": 1,
            "columnas": 1,
            "ancho": "Mínimo necesario",
            "porcentaje": "100%",
            "alineacion": "Izquierda",
            "borde_color": "#000000",
            "borde_espesor": 1
        }

        self.formato_copiado = None
        layout = QHBoxLayout(self)
        self.vista_previa = QTextEdit()
        self.vista_previa.setReadOnly(True)
        layout.addWidget(self.vista_previa, 1)

        panel_derecho = QVBoxLayout()
        self.toolbar = QToolBar()

        def add_icon_action(icon, callback=None, checkable=False, menu=None):
            act = QAction(QIcon(f"images/{icon}"), "", self)
            if checkable:
                act.setCheckable(True)
            if callback:
                act.triggered.connect(callback)
            if menu:
                btn = QToolButton()
                btn.setDefaultAction(act)
                btn.setMenu(menu)
                btn.setPopupMode(QToolButton.InstantPopup)
                self.toolbar.addWidget(btn)
            else:
                self.toolbar.addAction(act)
            return act

        self.action_bold = add_icon_action("bold_icon.png", lambda: self.set_format("bold"), checkable=True)
        self.action_italic = add_icon_action("italic_icon.png", lambda: self.set_format("italic"), checkable=True)
        self.action_underline = add_icon_action("underline_icon.png", lambda: self.set_format("underline"), checkable=True)
        self.action_text_color = add_icon_action("color_icon.png", self.set_text_color)
        self.action_bg_color = add_icon_action("background_icon.png", self.set_background_color)
        self.action_copy_format = add_icon_action("copy_format_icon.png", self.copy_format)

        # Menú alineación
        align_menu = QMenu(self)
        align_menu.addAction("Izquierda", lambda: self.set_text_alignment("left"))
        align_menu.addAction("Centro", lambda: self.set_text_alignment("center"))
        align_menu.addAction("Derecha", lambda: self.set_text_alignment("right"))
        self.action_align = add_icon_action("text_align_icon.png", menu=align_menu)

        # Menú bordes
        border_menu = QMenu(self)
        border_menu.addAction("Todos los bordes", lambda: self.set_cell_borders(["top", "bottom", "left", "right"]))
        border_menu.addAction("Ninguno", lambda: self.set_cell_borders([]))
        border_menu.addSeparator()
        border_menu.addAction("Borde superior", lambda: self.set_cell_borders(["top"]))
        border_menu.addAction("Borde inferior", lambda: self.set_cell_borders(["bottom"]))
        border_menu.addAction("Borde izquierdo", lambda: self.set_cell_borders(["left"]))
        border_menu.addAction("Borde derecho", lambda: self.set_cell_borders(["right"]))
        self.action_border = add_icon_action("cell_border_icon.png", menu=border_menu)

        self.action_settings = add_icon_action("settings_icon.png", self.abrir_configuracion)

        panel_derecho.addWidget(self.toolbar)

        self.table = QTableWidget(1, 1)
        self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.table.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.table.itemChanged.connect(self.actualizar_html)
        self.table.itemSelectionChanged.connect(self.actualizar_estilos_toolbar)
        self.table.itemClicked.connect(self.actualizar_estilos_toolbar)
        panel_derecho.addWidget(self.table, 4)

        panel_derecho.addWidget(QLabel("Código HTML:"))
        self.html_edit = QTextEdit()
        self.html_edit.setReadOnly(True)
        panel_derecho.addWidget(self.html_edit, 1)

        aplicar_btn = QPushButton("Aplicar")
        aplicar_btn.clicked.connect(self.aplicar)
        panel_derecho.addWidget(aplicar_btn)

        layout.addLayout(panel_derecho, 2)
        self.actualizar_html()

    def abrir_configuracion(self):
        dlg = ConfigTablaDialog(self)
        if dlg.exec():
            self.configuracion_tabla = dlg.get_config()
            self.reconstruir_tabla()

    def reconstruir_tabla(self):
        cfg = self.configuracion_tabla
        self.table.setRowCount(cfg["filas"])
        self.table.setColumnCount(cfg["columnas"])
        for i in range(cfg["filas"]):
            for j in range(cfg["columnas"]):
                self.table.setItem(i, j, QTableWidgetItem(""))
        self.actualizar_html()

    def actualizar_html(self):
        cfg = self.configuracion_tabla
        style_table = ""

        if cfg["ancho"] == "Mínimo necesario":
            style_table += "display: inline-block;"
        else:
            percent = cfg["porcentaje"]
            style_table += f"width: {percent};"

        borde_css = f"border: {cfg['borde_espesor']}px solid {cfg['borde_color']};"

        if cfg["alineacion"] == "Izquierda":
            wrapper_align = "left"
        elif cfg["alineacion"] == "Centrada":
            wrapper_align = "center"
        else:
            wrapper_align = "right"

        html = f'<div style="text-align: {wrapper_align};"><table style="{style_table} border-collapse: collapse; {borde_css}">\n'
        for i in range(self.table.rowCount()):
            html += "  <tr>\n"
            for j in range(self.table.columnCount()):
                item = self.table.item(i, j)
                if not item:
                    item = QTableWidgetItem("")
                    self.table.setItem(i, j, item)
                texto = item.text()
                estilo = item.data(Qt.UserRole) or {}
                css = f"padding: 4px; border: 1px solid {cfg['borde_color']};"
                if estilo.get("bold"):
                    texto = f"<b>{texto}</b>"
                if estilo.get("italic"):
                    texto = f"<i>{texto}</i>"
                if estilo.get("underline"):
                    texto = f"<u>{texto}</u>"
                if estilo.get("color"):
                    css += f" color: {estilo['color']};"
                if estilo.get("bg"):
                    css += f" background-color: {estilo['bg']};"
                if estilo.get("align"):
                    css += f" text-align: {estilo['align']};"
                html += f'    <td style="{css}">{texto}</td>\n'
            html += "  </tr>\n"
        html += "</table></div>"

        self.html_edit.setPlainText(html)
        self.vista_previa.setHtml(html)

        # Aplicar estilos visuales
        for i in range(self.table.rowCount()):
            for j in range(self.table.columnCount()):
                item = self.table.item(i, j)
                if not item:
                    item = QTableWidgetItem("")
                    self.table.setItem(i, j, item)
                estilo = item.data(Qt.UserRole) or {}
                self.aplicar_estilo_visual(item, estilo)

    def aplicar_estilo_visual(self, item, estilo):
        font = QFont()
        font.setBold(estilo.get("bold", False))
        font.setItalic(estilo.get("italic", False))
        font.setUnderline(estilo.get("underline", False))
        item.setFont(font)
        item.setForeground(QBrush(QColor(estilo.get("color", "#000000"))))
        item.setBackground(QBrush(QColor(estilo.get("bg", "#ffffff"))))

    def set_format(self, tipo):
        for item in self.table.selectedItems():
            estilo = item.data(Qt.UserRole) or {}
            estilo[tipo] = not estilo.get(tipo, False)
            item.setData(Qt.UserRole, estilo)
        self.actualizar_html()

    def set_text_color(self):
        color = QColorDialog.getColor()
        if not color.isValid():
            return
        for item in self.table.selectedItems():
            estilo = item.data(Qt.UserRole) or {}
            estilo["color"] = color.name()
            item.setData(Qt.UserRole, estilo)
        self.actualizar_html()

    def set_background_color(self):
        color = QColorDialog.getColor()
        if not color.isValid():
            return
        for item in self.table.selectedItems():
            estilo = item.data(Qt.UserRole) or {}
            estilo["bg"] = color.name()
            item.setData(Qt.UserRole, estilo)
        self.actualizar_html()

    def set_text_alignment(self, align):
        for item in self.table.selectedItems():
            estilo = item.data(Qt.UserRole) or {}
            estilo["align"] = align
            item.setData(Qt.UserRole, estilo)
        self.actualizar_html()

    def set_cell_borders(self, sides):
        for item in self.table.selectedItems():
            estilo = item.data(Qt.UserRole) or {}
            estilo["borders"] = sides
            item.setData(Qt.UserRole, estilo)
        self.actualizar_html()

    def copy_format(self):
        items = self.table.selectedItems()
        if items:
            self.formato_copiado = items[0].data(Qt.UserRole)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if self.formato_copiado:
            for item in self.table.selectedItems():
                item.setData(Qt.UserRole, self.formato_copiado)
            self.formato_copiado = None
            self.actualizar_html()

    def actualizar_estilos_toolbar(self):
        items = self.table.selectedItems()
        if not items:
            return
        estilo = items[0].data(Qt.UserRole) or {}
        self.action_bold.setChecked(estilo.get("bold", False))
        self.action_italic.setChecked(estilo.get("italic", False))
        self.action_underline.setChecked(estilo.get("underline", False))

    def aplicar(self):
        self.resultado = self.html_edit.toPlainText()
        self.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    registro = TreeWidget()
    registro.show()
    sys.exit(app.exec())