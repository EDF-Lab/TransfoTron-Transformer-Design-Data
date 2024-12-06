# -*- coding: utf-8 -*-
from PySide6.QtGui import QKeySequence, QMouseEvent, QImage, QPainter
from PySide6.QtCore import Qt, Signal, QEvent, QRectF, QPointF, QDateTime, QThread, QIODevice, QTemporaryFile, QSize
from PySide6.QtWidgets import QStyledItemDelegate, QGraphicsView, QLineEdit, QSpinBox, QComboBox, QDateTimeEdit, QMainWindow, \
                            QDockWidget, QWidget, QVBoxLayout, QDialog, QProgressBar, QPushButton, QPlainTextEdit, QLabel, QApplication, \
                            QPushButton

from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from .toleranceDefinition import UI_ToleranceDefinition

# =============================================================================
# Fichier d'utilitaires de création de graphiques pour transfo_tool
# On y retrouve, entre autres, les figures "génériques"
# =============================================================================

class ViewResizeAuto(QGraphicsView):
    """
    Vue se mettant automatiquement à la bonne taille de son contenu
    """

    def resizeEvent(self, event):

        self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)
        super().resizeEvent(event)

class ViewNonClickable(ViewResizeAuto):
    """
    Vue non cliquable à la souris
    """

    def mousePressEvent(self, event):
        # On ne fait rien et on ne le passe pas au super()
        pass

    def contextMenuEvent(self, event):
        pass

class LineEditValidatorDelegate(QStyledItemDelegate):
    """
    Délégué pour lineEdit avec un valideur
    """
    def __init__(self, validator, str_fmt="%.3f", parent=None):
        super().__init__(parent)

        self.validator = validator
        self.str_fmt = str_fmt

    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        editor.setValidator(self.validator)
        return editor

    def setEditorData(self, editor, index):
        val = index.model().data(index, Qt.EditRole)
        editor.setText("%s"%val)

    def setModelData(self, editor, model, index):
        try:
            tmp = int(editor.text())
        except:
            try:
                tmp = float(editor.text())
            except:
                tmp = editor.text()
        model.setData(index, tmp, Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def displayText(self, value, locale):
        try:
            format_val = self.str_fmt%float(value)
        except:
            format_val = value
        return format_val

class SpinBoxDelegate(QStyledItemDelegate):
    """
    Délégué pour spinbox
    """
    def __init__(self, minValue=1, maxValue=1, parent=None):
        super().__init__(parent)

        self.lst_item_minVal = []
        self.lst_item_maxVal = []
        self.maxValue = maxValue
        self.minValue = minValue

    def setLstItemMaxValue(self, lst_item_maxVal):
        self.lst_item_maxVal = lst_item_maxVal

    def setLstItemMinValue(self, lst_item_minVal):
        self.lst_item_minVal = lst_item_minVal

    def setMaxValue(self, maxValue):
        self.maxValue = maxValue

    def setMinValue(self, minValue):
        self.minValue = minValue

    def createEditor(self, parent, option, index):
        editor = QSpinBox(parent)
        editor.setFrame(False)
        editor.setSingleStep(1)

        if self.parent() != None and len(self.lst_item_maxVal) > 0:
            maxVal = [k for k in self.lst_item_maxVal if k[0]==self.parent().model().itemFromIndex(index)][0][1]
            editor.setMaximum(maxVal)
        else:
            editor.setMaximum(self.maxValue)

        if self.parent() != None and len(self.lst_item_minVal) > 0:
            minVal = [k for k in self.lst_item_minVal if k[0]==self.parent().model().itemFromIndex(index)][0][1]
            editor.setMinimum(minVal)
        else:
            editor.setMinimum(self.minValue)

        return editor

    def setEditorData(self, editor, index):
        try:
            val = int(index.model().data(index, Qt.EditRole))
        except:
            val = 1
        editor.setValue(val)

    def setModelData(self, editor, model, index):
        editor.interpretText()
        val = editor.value()
        model.setData(index, val, Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

class ComboBoxDelegate(QStyledItemDelegate):
    """
    Délégué pour combobox
    https://wiki.qt.io/Combo_Boxes_in_Item_Views
    """
    def __init__(self, lst_cbox_items=[], lst_cbox_items_in_role=None, parent=None):
        super().__init__(parent)
        self.lst_cbox_items = lst_cbox_items
        self.lst_item_cboxItems = []
        self.lst_cbox_items_in_role = lst_cbox_items_in_role

    def setLstItemCboxItems(self, lst_item_cboxItems):
        self.lst_item_cboxItems = lst_item_cboxItems

    def setLstCboxItems(self, lst_cbox_items):
        self.lst_cbox_items = lst_cbox_items

    def createEditor(self, parent, option, index):
        lst_cbox_items = self.lst_cbox_items
        editor = QComboBox(parent)
        if self.parent() != None and len(self.lst_item_cboxItems) > 0:
            lst_cbox_items = [k for k in self.lst_item_cboxItems if k[0]==self.parent().model().itemFromIndex(index)][0][1]
        elif self.parent() != None and not self.lst_cbox_items_in_role is None:
            item = self.parent().model().itemFromIndex(index)
            data = item.data(self.lst_cbox_items_in_role)
            if not data is None and type(data) == list:
                lst_cbox_items = data
        editor.addItems(lst_cbox_items)
        return editor

    def setEditorData(self, editor, index):
        currentText = index.model().data(index, Qt.EditRole)
        editor.setCurrentText("%s"%currentText)

    def setModelData(self, editor, model, index):
        try:
            tmp = int(editor.currentText())
        except:
            tmp = editor.currentText()
        model.setData(index, tmp, Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

class DateTimeEditDelegate(QStyledItemDelegate):
    """
    Délégué pour DateTimeEdit
    """
    def __init__(self, minDT=None, maxDT=None, defDT=None, formatDT="yyyy-MM-dd hh:mm:ss.zzz", parent=None):
        super().__init__(parent)
        self.minDT = minDT
        self.maxDT = maxDT
        self.defDT = defDT
        self.formatDT = formatDT

        self.lst_item_minDT = []
        self.lst_item_defDT = []
        self.lst_item_maxDT = []

    def setMinDateTime(self, minDT):
        self.minDT = minDT

    def setMaxDateTime(self, maxDT):
        self.maxDT = maxDT

    def setLstItemMinDateTime(self, lst_item_minDT):
        self.lst_item_minDT = lst_item_minDT

    def setLstItemMaxDateTime(self, lst_item_maxDT):
        self.lst_item_maxDT = lst_item_maxDT

    def setLstItemDefaultDateTime(self, lst_item_defDT):
        self.lst_item_defDT = lst_item_defDT

    def setFormatDateTime(self, formatDT):
        self.formatDT = formatDT

    def createEditor(self, parent, option, index):
        editor = QDateTimeEdit(parent)
        editor.setCalendarPopup(True)
        if self.parent() != None and len(self.lst_item_minDT) > 0:
            minDT = [k for k in self.lst_item_minDT if k[0]==self.parent().model().itemFromIndex(index)][0][1]
            editor.setMinimumDateTime(minDT)
        else:
            if self.minDT != None:
                editor.setMinimumDateTime(self.minDT)
        if self.parent() != None and len(self.lst_item_maxDT) > 0:
            maxDT = [k for k in self.lst_item_maxDT if k[0]==self.parent().model().itemFromIndex(index)][0][1]
            editor.setMaximumDateTime(maxDT)
        else:
            if self.maxDT != None:
                editor.setMaximumDateTime(self.maxDT)
        if self.parent() != None and len(self.lst_item_defDT) > 0:
            defDT = [k for k in self.lst_item_defDT if k[0]==self.parent().model().itemFromIndex(index)][0][1]
            editor.setDateTime(defDT)
        else:
            if self.defDT != None:
                editor.setDateTime(self.defDT)
        if self.formatDT != None:
            editor.setDisplayFormat(self.formatDT)
        return editor

    def setEditorData(self, editor, index):
        currentText = index.model().data(index, Qt.EditRole)
        editor.setDateTime(QDateTime.fromString(currentText, editor.displayFormat()))

    def setModelData(self, editor, model, index):
        model.setData(index, editor.dateTime().toString(editor.displayFormat()), Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

class DialogDelegate(QStyledItemDelegate):
    """
    Délégué pour QDialog
    """
    def __init__(self, parent=None):
        super().__init__(parent)

    def editorEvent(self, event, model, option, index):

        if event.type() == QEvent.MouseButtonRelease:
            dialog = model.data(index, Qt.UserRole)
            dialog.exec()
            model.setData(index, dialog.text(), Qt.EditRole)
        return True

class ViewZoomable(QGraphicsView):
    """
    Vue zoomable avec la roulette de la souris
    """

    # Signal quand la vue est changée (pour MAJ de la vue active sur la vue non zoomée)
    viewUpdated = Signal()

    def __init__(self, scene):
        super().__init__(scene)
        self.setDragMode(QGraphicsView.RubberBandDrag)

    def wheelEvent(self, event):
        """
        Zoom in or out of the view.
        """

        if event.modifiers() & Qt.ControlModifier:
            zoomInFactor = 1.25
            zoomOutFactor = 1 / zoomInFactor

            # Save the scene pos
            oldPos = self.mapToScene(event.position().toPoint())

            # Zoom
            if event.angleDelta().y() > 0:
                zoomFactor = zoomInFactor
            else:
                zoomFactor = zoomOutFactor
            self.scale(zoomFactor, zoomFactor)

            # Get the new position
            newPos = self.mapToScene(event.position().toPoint())

            # Move scene to old position
            delta = newPos - oldPos
            self.translate(delta.x(), delta.y())

        else:
            super().wheelEvent(event)

    def mousePressEvent(self, event):

        if event.button() == Qt.MiddleButton and event.modifiers() & Qt.ControlModifier:
            # Activation du mode de drag
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            # Inspiré de https://gist.github.com/Legor/a00760b6d7af32c01357fb7ff76ad86a
            # Le ControlModifier permet de faire cohabiter drag et selection
            event = QMouseEvent(QEvent.GraphicsSceneMousePress,
                                               event.position().toPoint(), Qt.LeftButton, Qt.LeftButton,
                                               Qt.ControlModifier)

        # Faire également le fonctionnement normal sinon problèmes avec la sélection
        # Le filtrage du clic droit permet de ne pas perdre la sélection multiple
        if event.button() != Qt.RightButton: # or len(self.scene().selectedItems())==0
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        # Desactivation du mode de drag
        self.setDragMode(QGraphicsView.RubberBandDrag)

        # A laisser ici
        super().mouseReleaseEvent(event)

        # Sélection multiple avec Shift
        if event.modifiers() & Qt.ShiftModifier:
            pos = self.mapToScene(event.position().toPoint())
            x_tl = min(self.old_pos.x(), pos.x())
            y_tl = min(self.old_pos.y(), pos.y())
            x_br = max(self.old_pos.x(), pos.x())
            y_br = max(self.old_pos.y(), pos.y())
            tmp_rect = QRectF(QPointF(x_tl, y_tl), QPointF(x_br, y_br))
            for i in self.scene().items(tmp_rect, Qt.IntersectsItemShape):
                i.setSelected(True)

        self.old_pos = self.mapToScene(event.position().toPoint())

    def keyPressEvent(self, event):

        if event.matches(QKeySequence.SelectAll):
            # Ctrl + A
            for i in self.scene().items():
                i.setSelected(True)

        super().keyPressEvent(event)

    def paintEvent(self, event):

        # On envoi un signal (sert à la maj du rectangle de vue)
        self.viewUpdated.emit()
        super().paintEvent(event)

class FigCanvas(FigureCanvasQTAgg):
    """
    For bug https://stackoverflow.com/questions/62303973/how-avoid-PySide6-to-crash-when-i-move-qslitter-to-the-edge-with-a-matplotlib-figu
    """
    def resizeEvent(self, event):
        if event.size().width() <= 0 or event.size().height() <= 0:
            return
        super(FigCanvas, self).resizeEvent(event)

# Pour changer les actions du bouton Home
# https://stackoverflow.com/questions/14896580/matplotlib-hooking-in-to-home-back-forward-button-events
home = NavigationToolbar.home
def new_home(self, *args, **kwargs):

    # Récupération de la figure mpl
    view_plt = None
    for k in range(self.parent().layout().count()):
        if isinstance(self.parent().layout().itemAt(k).widget(), FigCanvas):
            view_plt = self.parent().layout().itemAt(k).widget()
            break

    # Reset des limites des axes
    if not view_plt is None:
        fig_plt = view_plt.figure
        for axe in fig_plt.get_axes():
            axe.autoscale()
        fig_plt.canvas.draw_idle()

    # Actions normales
    home(self, *args, **kwargs)
NavigationToolbar.home = new_home

class UI_DockableMPLFigure(QMainWindow):
    """
    Classe pour avoir des figures dockables
    """
    def __init__(self, title=None, parent=None):
        super().__init__(parent)

        self.dockWidget = QDockWidget()
        self.dockWidget.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        if title != None:
            title += " (Double-click here to dock/undock the figure)"
        else:
            title = "(Double-click here to dock/undock the figure)"
        self.dockWidget.setWindowTitle(title)
        self.addDockWidget(Qt.TopDockWidgetArea, self.dockWidget)

        wdg_mpl = QWidget(self.dockWidget)
        self.dockWidget.setWidget(wdg_mpl)
        layout_mpl = QVBoxLayout(wdg_mpl)

        self.fig_plt = plt.Figure()
        self.view_plt = FigCanvas(self.fig_plt)
        layout_mpl.addWidget(self.view_plt)
        toolbar = NavigationToolbar(self.view_plt, wdg_mpl, coordinates=True)

        layout_mpl.addWidget(toolbar)

class QLineEditFormat(QLineEdit):
    """
    QLineEdit permettant d'avoir un display différent de la valeur
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.txt_original = super().text()
        self.str_fmt = "%s"

    def setDisplayFormat(self, str_fmt):
        try:
            txt_formated = self.str_fmt%self.txt_original
        except:
            self.str_fmt = str_fmt
            return
        self.str_fmt = str_fmt
        if txt_formated == super().text():
            self.setText(self.txt_original)

    def text(self):
        try:
            txt_formated = self.str_fmt%self.txt_original
        except:
            return super().text()
        if txt_formated == super().text():
            return "%s"%self.txt_original
        else:
            return super().text()

    def setText(self, txt):
        try:
            txt_formated = self.str_fmt%txt
        except:
            txt_formated = "%s"%txt
        super().setText(txt_formated)
        self.txt_original = txt

    def replaceWidget(self, oldWidget):
        oldWidget.parent().layout().replaceWidget(oldWidget, self)
        oldWidget.close()
        return self

class BackgroungCalculation(QThread):
    """
    Thread de réalisation d'un calcul en arrière plan
    """
    progress_pb = Signal(int)
    txt_log = Signal(str)
    current_result = Signal(object)
    finished = Signal()

    def __init__(self, fct_to_run, fct_args):
        super().__init__()

        self.fct_to_run = fct_to_run
        self.fct_args = fct_args
        self.result = None
        self.lastResult = None

        self.current_result.connect(self.updateLastResult)

    def run(self):
        self.result = self.fct_to_run(progress_pb=self.progress_pb, txt_log=self.txt_log, current_result=self.current_result, **self.fct_args)
        self.lastResult = self.result
        self.finished.emit()

    def stop(self):
        self.terminate()

    def updateLastResult(self, current_result):
        self.lastResult = current_result

    def getResult(self):
        return self.result

    def getLastResult(self):
        return self.lastResult

class CalculationProgressBar(QDialog):
    """
    Progress bar
    """
    def __init__(self, fct_to_run, fct_args={}, title="Calculation in progress...", max_pb=100, showStopButton=False, showCurrentResult=False, autoClose=True, parent=None):
        super().__init__(parent)

        self.fct_to_run = fct_to_run
        self.fct_args = fct_args
        self.title = title
        self.max_pb = max_pb
        self.showStopButton = showStopButton
        self.showCurrentResult = showCurrentResult
        self.autoClose = autoClose

        self.setup()

    def setup(self):

        # Un titre
        self.setWindowTitle(self.title)

        # Suppression du bouton "?" dans la barre de titre et du bouton de maximisation de la fenêtre
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowFlag(Qt.WindowCloseButtonHint, self.showStopButton)

        # Création de la disposition
        layout = QVBoxLayout(self)
        self.setMinimumWidth(300)

        self.ui_progress = QProgressBar(self)
        layout.addWidget(self.ui_progress)
        self.ui_progress.setMinimum(0)

        if self.showCurrentResult:
            self.ui_lbl_current_result = QLabel("Current result:", self)
            layout.addWidget(self.ui_lbl_current_result)
            self.ui_lbl_current_result.hide()
            self.ui_current_result = QLineEdit(self)
            layout.addWidget(self.ui_current_result)
            self.ui_current_result.setReadOnly(True)
            self.ui_current_result.hide()

        self.ui_lbl_txt_log = QLabel("Calculation log:", self)
        layout.addWidget(self.ui_lbl_txt_log)
        self.ui_lbl_txt_log.hide()
        self.ui_txt_log = QPlainTextEdit(self)
        layout.addWidget(self.ui_txt_log)
        self.ui_txt_log.setReadOnly(True)
        self.ui_txt_log.setMinimumHeight(200)
        self.ui_txt_log.hide()

        if self.showStopButton:
            self.ui_button_stop = QPushButton('Stop', self)
            layout.addWidget(self.ui_button_stop)
            self.ui_button_stop.clicked.connect(self.close)

        # Divers
        self.calc = None
        self.cursor = None

        # Démarrage
        self.start()

    def start(self):

        # On passe en mode infini en attendant le premier point
        self.ui_progress.setMaximum(0)

        # Création du Thread
        self.calc = BackgroungCalculation(self.fct_to_run, self.fct_args)

        # Connections
        self.calc.progress_pb.connect(self.onCountChanged)
        self.calc.txt_log.connect(self.onLogUpdated)
        if self.showCurrentResult:
            self.calc.current_result.connect(self.onCurrentResultUpdated)
        self.calc.finished.connect(self.onFinished)

        # On retire l'éventuel WaitCursor
        if not QApplication.overrideCursor() is None:
            self.cursor = QApplication.overrideCursor().shape()
        QApplication.restoreOverrideCursor()

        # Démarrage
        self.calc.start()

    def onCountChanged(self, value):
        if self.ui_progress.maximum() == 0:
            self.ui_progress.setMaximum(self.max_pb)
        self.ui_progress.setValue(value)

    def onCurrentResultUpdated(self, current_result):
        if not self.showCurrentResult:
            return

        if not self.ui_current_result.isVisible():
            self.ui_current_result.show()
            self.ui_lbl_current_result.show()
        self.ui_current_result.setText("%s"%current_result)

    def onLogUpdated(self, txt):
        if not self.ui_txt_log.isVisible():
            self.ui_txt_log.show()
            self.ui_lbl_txt_log.show()
        self.ui_txt_log.appendPlainText(txt)

    def onFinished(self):
        if self.autoClose:
            self.close()
        else:
            self.ui_button_stop.setText("Close")

    def getResult(self):
        if self.calc is None:
            return None
        return self.calc.getResult()

    def getLastResult(self):
        if self.calc is None:
            return None
        return self.calc.getLastResult()

    def closeEvent(self, event):
        if not self.cursor is None:
            QApplication.setOverrideCursor(self.cursor)
        if not self.calc is None:
            self.calc.stop()
        super().closeEvent(event)

def getImageFromQGraphics(scene, rectSource, scale=1.0):
    """
    Renvoi le chemin de l'image PNG avec les items QGraphics
    """
    targetSize = QSize(rectSource.toRect().width()*scale, rectSource.toRect().height()*scale)

    pixMap = QImage(targetSize, QImage.Format_ARGB32_Premultiplied)
    pixMap.fill(Qt.white)
    painter = QPainter()
    painter.begin(pixMap)
    painter.setRenderHint(QPainter.Antialiasing, True)
    scene.render(painter, source=rectSource)
    painter.end()

    file = QTemporaryFile(scene)
    file.open(QIODevice.WriteOnly)
    pixMap.save(file, "PNG")
    file.close()

    return file.fileName(), targetSize

def define_tolerance_on_button(ui_button, **kwargs):
    tolerance = UI_ToleranceDefinition(**kwargs)
    tolerance.updated.connect(ui_button.setText)
    tolerance.update_tolerance() # Pour déclencher une mise à jour
    ui_button.clicked.connect(tolerance.exec)
    return tolerance

def define_format_on_lineEdit(ui_lineEdit, format="%.1f"):
    ui_lineEdit = QLineEditFormat(ui_lineEdit.parent()).replaceWidget(ui_lineEdit)
    ui_lineEdit.setDisplayFormat(format)
    return ui_lineEdit