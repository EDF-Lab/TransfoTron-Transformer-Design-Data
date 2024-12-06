# -*- coding: utf-8 -*-
import sys
from os.path import join, dirname, realpath
from statistics import mean

from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import Signal, QRegularExpression
from PySide6.QtWidgets import QMessageBox, QWidget

from ..utils import gui_utils
from ..utils import gui_geom

from .disc_one_ui import Ui_Form

# =============================================================================
# Widget de définition d'un disque
# =============================================================================

################## A ADAPTER SELON LE CAS ########################
# Define function to import external files when using PyInstaller.
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        tmp = __package__
        if tmp == None:
            tmp = ""
        base_path = join(sys._MEIPASS, *tmp.split("."))
    except Exception:
        base_path = dirname(realpath(__file__))

    return join(base_path, relative_path)
PATHRC = resource_path("ressources")
##################################################################

class UI_Disc(QWidget, Ui_Form):

    # Signal quand le widget est modifié par l'utilisateur (non programmatiquement)
    isModified = Signal()

    def __init__(self, widg_ratingPlate, widg_cableAll, widg_discAll, ui_main, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.widg_ratingPlate = widg_ratingPlate
        self.widg_cableAll = widg_cableAll
        self.widg_discAll = widg_discAll
        self.ui_main = ui_main

        self.setup()

    def setup(self):

        # Remplacement du QLineEdit et application d'un format d'affichage
        self.ui_le_cableHeight = gui_utils.QLineEditFormat(self.ui_le_cableHeight.parent()).replaceWidget(self.ui_le_cableHeight)
        self.ui_le_cableHeight.setDisplayFormat("%.2f")
        self.ui_le_cableThick = gui_utils.QLineEditFormat(self.ui_le_cableThick.parent()).replaceWidget(self.ui_le_cableThick)
        self.ui_le_cableThick.setDisplayFormat("%.2f")
        self.ui_le_diskWidth = gui_utils.QLineEditFormat(self.ui_le_diskWidth.parent()).replaceWidget(self.ui_le_diskWidth)
        self.ui_le_diskWidth.setDisplayFormat("%.2f")

        # Ajouts de valideurs de champs
        validator_str = QRegularExpressionValidator(QRegularExpression("[A-Za-z0-9-_]+"), self)
        self.ui_le_name.setValidator(validator_str)

        # Nombre de cables par disc
        self.ui_spBox_cableDisc.setMinimum(1)
        self.ui_spBox_cableDisc.setMaximum(10000)

        ### Divers
        self.lst_coilThermalData = []
        self.lst_propCables = []
        self.cable_eq_prop = {}
        self.currentCoilThermalData = None
        self.disc_color = gui_geom.getRandomColor()
        self.ui_le_cableHeight.setEnabled(False)
        self.ui_le_cableThick.setEnabled(False)
        self.ui_le_diskWidth.setEnabled(False)

        ### Conections
        self.ui_cBox_coil.currentIndexChanged.connect(self.cableCalculation)
        self.ui_cBox_coil.currentIndexChanged.connect(self.updateCurrentCoilThermalData)
        self.ui_cBox_cable.currentIndexChanged.connect(self.cableCalculation)
        self.ui_spBox_cableDisc.valueChanged.connect(self.cableCalculation)

        self.ui_main.isFrozen.connect(self.freezeDesign)

        ### Au démarrage
        self.connectModification()

    def connectModification(self):
        """
        Connection des éléments pour émission du signal isModified
        """
        # Les sous-connections peuvent être activées par l'utilisateur ou programmatiquement
        self.ui_le_name.editingFinished.connect(self.emitIsModified)
        self.ui_cBox_coil.currentIndexChanged.connect(self.emitIsModified)
        self.ui_cBox_cable.currentIndexChanged.connect(self.emitIsModified)
        self.ui_spBox_cableDisc.valueChanged.connect(self.emitIsModified)

    def emitIsModified(self):
        self.isModified.emit()

    def disconnectModification(self):
        """
        Déconnection des éléments à l'émission du signal isModified
        """
        self.ui_le_name.editingFinished.disconnect(self.emitIsModified)
        self.ui_cBox_coil.currentIndexChanged.disconnect(self.emitIsModified)
        self.ui_cBox_cable.currentIndexChanged.disconnect(self.emitIsModified)
        self.ui_spBox_cableDisc.valueChanged.disconnect(self.emitIsModified)

    def freezeDesign(self, isFrozen):
        """
        Action lors du (dé)gelage du design
        """
        self.ui_le_name.setEnabled(not isFrozen)
        self.ui_cBox_coil.setEnabled(not isFrozen)
        self.ui_cBox_cable.setEnabled(not isFrozen)
        self.ui_spBox_cableDisc.setEnabled(not isFrozen)

    def checkDesign(self):
        """
        Vérification du design
        """
        # Liste d'erreurs à corriger
        lst_error = []

        tmp = self.ui_le_name
        if not tmp.hasAcceptableInput():
            tmp.setStyleSheet("background-color: red;")
            lst_error.append("Disc name must only have A-Z or a-z or 0-9 or - or _ characters")
        else:
            tmp.setStyleSheet("")

        return lst_error

    def setDiscColor(self, color):
        self.disc_color = color

    def getDisc(self):
        """
        Renvoi du dico représentant le disc défini
        """

        if self.cable_eq_prop == {}:
            # Probleme de definition du disc
            return {}

        disc = {"name": self.ui_le_name.text(), \
                "h_cable": self.cable_eq_prop["h_cable"], \
                "t_cable": self.cable_eq_prop["t_cable"], \
                "N_cables": self.ui_spBox_cableDisc.value(), \
                'cable_origin': self.cable_eq_prop["cable_origin"], \
                "color": self.disc_color}

        return disc

    def removeDisc(self):
        """
        Suppression du disc des lst_UI_CoilDefinition
        Utile en cas de suppression totale du disc (géré en disc_all)
        """
        # Suppresion des précédente coils
        if self.currentCoilThermalData != None:
            for c_ui in self.currentCoilThermalData["lst_UI_CoilDefinition"]:
                c_ui.coil.removeUIDisc(self)

    def updateCurrentCoilThermalData(self):
        """
        MAJ de la coil courante et gestion avec la definition de la geometrie
        """
        # Suppresion des précédente coils
        self.removeDisc()

        # Ajout du disc aux coils
        self.currentCoilThermalData = self.lst_coilThermalData[self.ui_cBox_coil.currentIndex()]
        for c_ui in self.currentCoilThermalData["lst_UI_CoilDefinition"]:
            c_ui.coil.addUIDisc(self)

    def cableCalculation(self, recursif=True):
        """
        Calcul du cable équivalent pour avoir la bonne largeur de bobine
        """
        if self.ui_cBox_cable.count() <= 0:
            # Il n'y a pas de cables correctement définis => on s'arrête
            QMessageBox.critical(self, "Disc definition", \
                                           "Check cables properties", \
                                           QMessageBox.Ok, QMessageBox.Ok)
            self.cable_eq_prop == {}
            return

        ### Détermination de la largeur de la bobine à laquelle correspond ce disc
        # Liste des largeurs "souhaitées" des discs pour cette bobine
        lst_width = []
        rootItem = self.widg_discAll.model_lst_disc.invisibleRootItem()
        for k in range(self.widg_discAll.model_lst_disc.rowCount(rootItem.index())):
            widg_disc = self.widg_discAll.model_lst_disc.item(k).widget
            if widg_disc.lst_coilThermalData[widg_disc.ui_cBox_coil.currentIndex()] == self.lst_coilThermalData[self.ui_cBox_coil.currentIndex()]:
                lst_width.append(widg_disc.largeurSouhaitee())

        # Largeur de la bobine comme moyenne
        width_disc = mean(lst_width)
        self.ui_le_diskWidth.setText(width_disc)

        ### Calcul des propriétés cable équivalent
        ratio = width_disc/self.largeurSouhaitee()

        self.cable_eq_prop = self.lst_propCables[self.ui_cBox_cable.currentIndex()].copy()

        self.cable_eq_prop["t_cable"] = self.lst_propCables[self.ui_cBox_cable.currentIndex()]["t_cable"]
        self.cable_eq_prop["h_cable"] = self.lst_propCables[self.ui_cBox_cable.currentIndex()]["h_cable"]*ratio
        self.cable_eq_prop["cable_origin"] = self.lst_propCables[self.ui_cBox_cable.currentIndex()]

        self.ui_le_cableHeight.setText(self.cable_eq_prop["h_cable"])
        self.ui_le_cableThick.setText(self.cable_eq_prop["t_cable"])

        ### Calcul des propriétés équivalentes pour tous les discs
        if recursif:
            rootItem = self.widg_discAll.model_lst_disc.invisibleRootItem()
            for k in range(self.widg_discAll.model_lst_disc.rowCount(rootItem.index())):
                widg_disc = self.widg_discAll.model_lst_disc.item(k).widget
                widg_disc.cableCalculation(False)

    def largeurSouhaitee(self):
        """
        Calcul de la largeur du disc souhaitée à partir des paramètres bruts
        """
        cable_prop = self.lst_propCables[self.ui_cBox_cable.currentIndex()]
        width = self.ui_spBox_cableDisc.value()*cable_prop["h_cable"]

        return width

    def updateCoilThermalData(self):
        """
        Mise à jour de lst_coilThermalData et de la combobox
        """
        # Récupération de la liste des bobines thermiques où on appliquera les disques
        self.lst_coilThermalData = self.widg_ratingPlate.getLstCoilThermalData()

        # MAJ de la combobox
        self.ui_cBox_coil.currentIndexChanged.disconnect(self.cableCalculation)
        self.ui_cBox_coil.currentIndexChanged.disconnect(self.updateCurrentCoilThermalData)
        self.disconnectModification()
        coil_old = self.ui_cBox_coil.currentText()

        self.ui_cBox_coil.clear()
        tmp = [k["name"] for k in self.lst_coilThermalData]
        self.ui_cBox_coil.addItems(tmp)

        if coil_old in tmp:
            self.ui_cBox_coil.setCurrentText(coil_old)
        else:
            self.ui_cBox_coil.setCurrentIndex(0)
            self.emitIsModified()

        self.ui_cBox_coil.currentIndexChanged.connect(self.cableCalculation)
        self.ui_cBox_coil.currentIndexChanged.connect(self.updateCurrentCoilThermalData)
        self.connectModification()

        self.updateCurrentCoilThermalData()

    def updateCables(self):
        """
        Mise à jour la lst de cables et de la combobox
        """
        # Récupération de la liste des cables (de taille non nulle)
        self.lst_propCables = self.widg_cableAll.getLstPropCables()

        # MAJ de la combobox
        self.ui_cBox_cable.currentIndexChanged.disconnect(self.cableCalculation)
        self.disconnectModification()
        cable_old = self.ui_cBox_cable.currentText()

        self.ui_cBox_cable.clear()
        tmp = [k["name"] for k in self.lst_propCables]
        self.ui_cBox_cable.addItems(tmp)

        if cable_old in tmp:
            self.ui_cBox_cable.setCurrentText(cable_old)
        else:
            self.ui_cBox_cable.setCurrentIndex(0)
            self.emitIsModified()

        self.ui_cBox_cable.currentIndexChanged.connect(self.cableCalculation)
        self.connectModification()

    def showEvent(self, event):

        # Liste de coils
        self.updateCoilThermalData()

        # Liste de cables
        self.updateCables()

        # On refait un calcul
        self.cableCalculation()

        super().showEvent(event)

    def addXMLTree(self, tag_discs, docDom):
        """
        Generation de l'arbre XML
        """
        # Des MAJ
        self.updateCoilThermalData()
        self.updateCables()
        self.cableCalculation()

        # Récupération des propriétés
        disc_prop = self.getDisc()
        if disc_prop == {}:
            return

        tag_dn = docDom.createElement("disc")
        tag_discs.appendChild(tag_dn)

        tag_tmp = docDom.createElement('name')
        tag_tmp.appendChild(docDom.createTextNode(disc_prop["name"]))
        tag_dn.appendChild(tag_tmp)
        tag_tmp = docDom.createElement('coil')
        tag_tmp.appendChild(docDom.createTextNode(self.lst_coilThermalData[self.ui_cBox_coil.currentIndex()]["name"]))
        tag_dn.appendChild(tag_tmp)
        tag_tmp = docDom.createElement('cable')
        tag_tmp.setAttribute("original", disc_prop["cable_origin"]["name"])
        tag_tmp.setAttribute("N_cables", "%i"%(disc_prop["N_cables"]))
        tag_tmp.setAttribute("t_cable_m", "%e"%(disc_prop["t_cable"]*1e-3))
        tag_tmp.setAttribute("h_cable_m", "%e"%(disc_prop["h_cable"]*1e-3))
        tag_dn.appendChild(tag_tmp)

    def addPDF(self, pdf, part, lst_id_calcul=[]):
        """
        Remplissage du fichier PDF
        """
        pdf.set_font()

        if "data_detail" in part:
            disc_prop = self.getDisc()
            if disc_prop == {}:
                return

            if disc_prop["N_cables"] <= 1:
                pdf.multi_cell(txt=" "*8 + "Disc %s: %i cable %s"%(disc_prop["name"], disc_prop["N_cables"], disc_prop["cable_origin"]["name"]))
            else:
                pdf.multi_cell(txt=" "*8 + "Disc %s: %i cables %s"%(disc_prop["name"], disc_prop["N_cables"], disc_prop["cable_origin"]["name"]))

    def loadXMLTree(self, e_disc):
        """
        Chargement de l'arbre XML
        """
        # Des MAJ
        self.updateCoilThermalData()
        self.updateCables()

        if e_disc.isNull():
            return

        self.disconnectModification()

        self.ui_le_name.setText(e_disc.firstChildElement("name").text())
        self.ui_cBox_coil.setCurrentText(e_disc.firstChildElement("coil").text())

        e_disc_cable = e_disc.firstChildElement("cable")
        self.ui_cBox_cable.setCurrentText(e_disc_cable.attribute("original"))
        self.ui_spBox_cableDisc.setValue(int(e_disc_cable.attribute("N_cables")))

        self.cableCalculation()

        self.connectModification()

if __name__ == "__main__":
    """
    Point d'entrée à l'exécution du script app.py
    """
    # 1 - Creation de l'application Qt
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)

    win = UI_Disc()

    # 3 - Affichage de la fenêtre
    win.show()
    app.exec()