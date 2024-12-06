# -*- coding: utf-8 -*-
import sys
from os import makedirs
from os.path import join, dirname, realpath, exists
from copy import copy

from PySide6.QtCore import Signal, QIODevice, QTextStream, QFile
from PySide6.QtWidgets import QVBoxLayout, QWidget
from PySide6.QtXml import QDomDocument

from .coilsGeneralDefinition_ui import Ui_Form

# =============================================================================
# Widget de définition des bobines
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

class UI_CoilsGeneralDefinition(QWidget, Ui_Form):

    # Signal quand le widget est modifié par l'utilisateur (non programmatiquement)
    isModified = Signal()

    def __init__(self, widg_ratingPlate, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.widg_ratingPlate = widg_ratingPlate

        self.setup()

    def setup(self):

        # Ajout d'un layout au ui_wdg_coil
        self.layout_coil = QVBoxLayout(self.ui_wdg_coil)

        ### Divers
        self.lst_coilThermalData = []

        ### Connecteurs
        self.ui_cBox_coil.currentIndexChanged.connect(self.changeCoil)

    def emitIsModified(self):
        self.isModified.emit()

    def checkDesign(self):
        """
        Vérification du design
        """
        # Liste d'erreurs à corriger
        lst_error = []

        # Vérification de chacun des coils
        for k in range(self.layout_coil.count()):
            item = self.layout_coil.itemAt(k)
            c_ui = item.widget()
            lst_error = lst_error + c_ui.checkDesign()

        return lst_error

    def changeCoil(self, indexCoilToShow):
        # Parcours du layout et masquage des widgets visibles
        for k in range(self.layout_coil.count()):
            item = self.layout_coil.itemAt(k)
            item.widget().hide()

        # Affichage du widget
        coilToShow = self.lst_coilThermalData[indexCoilToShow]
        for c_ui in coilToShow["lst_UI_CoilDefinition"]:
            c_ui.show()

    def updateCoilThermalData(self):
        """
        Mise à jour de lst_coilThermalData
        """
        # Récupération de la liste des bobines thermiques
        self.lst_coilThermalData = self.widg_ratingPlate.getLstCoilThermalData()
        # Initialisation des coils si besoin
        for c in self.lst_coilThermalData:
            for c_ui in c["lst_UI_CoilDefinition"]:
                if self.layout_coil.indexOf(c_ui) < 0:
                    # On ajoute le widget au layout
                    self.layout_coil.addWidget(c_ui)
                    c_ui.hide()

    def showEvent(self, event):

        self.updateCoilThermalData()

        # Initialisation de la combobox
        self.ui_cBox_coil.currentIndexChanged.disconnect(self.changeCoil)
        coil_old = self.ui_cBox_coil.currentText()

        self.ui_cBox_coil.clear()
        tmp = [k["name"] for k in self.lst_coilThermalData]
        self.ui_cBox_coil.addItems(tmp)

        self.ui_cBox_coil.currentIndexChanged.connect(self.changeCoil)
        if coil_old in tmp:
            self.ui_cBox_coil.setCurrentText(coil_old)
        else:
            self.ui_cBox_coil.setCurrentIndex(0)

        self.changeCoil(self.ui_cBox_coil.currentIndex())

        super().showEvent(event)

    def generateXML(self, tmpSaveDirPath):
        """
        Génération du fichier XML dans le dossier temporaire
        """
        path_design = join(tmpSaveDirPath, "design")
        if not exists(path_design):
            makedirs(path_design)

        docDom = QDomDocument()
        root = docDom.appendChild(docDom.createElement("root"))

        # On met tout à jour
        self.updateCoilThermalData()

        for c in self.lst_coilThermalData:
            tag_c = docDom.createElement('coil')
            root.appendChild(tag_c)
            tag_tmp = docDom.createElement('name')
            tag_tmp.appendChild(docDom.createTextNode(c["name"]))
            tag_c.appendChild(tag_tmp)
            for c_ui in c["lst_UI_CoilDefinition"]:
                c_ui.addXMLTree(tag_c, docDom)

        # Enregistrement
        header = docDom.createProcessingInstruction("xml", "version=\"1.0\" encoding=\"UTF-8\"")
        docDom.insertBefore(header, root)
        file = QFile(join(path_design, "coil.xml"))
        file.open(QIODevice.WriteOnly)
        out = QTextStream(file)
        docDom.save(out, 4, QDomDocument.EncodingFromDocument)
        file.close()

    def loadXML(self, tmpSaveDirPath):
        """
        Chargement du fichier xml dans le ttx
        """
        path_xml = join(tmpSaveDirPath, "design", "coil.xml")
        if not exists(path_xml):
            return

        file = QFile(path_xml)
        doc = QDomDocument()
        if not file.open(QIODevice.ReadOnly):
            file.close()
            raise Exception("Probleme lecture du fichier %s"%path_xml)
        if not doc.setContent(file):
            file.close()
            raise Exception("Probleme lecture du fichier %s"%path_xml)
        file.close()

        root = doc.documentElement()
        if root.isNull():
            return

        # Les windings ont été chargés auparavant
        # Création de lst_coilThermalData
        self.updateCoilThermalData()

        n = root.firstChildElement("coil")
        lst_coil_tmp = copy(self.lst_coilThermalData) # Pour gérer les cas où il y a plusieurs coils avec le même nom
        while not n.isNull():
            e_coil = n.toElement()
            # Chargement des infos sur la 1ère bonne coil
            name_xml = e_coil.firstChildElement("name").text()
            for c in lst_coil_tmp:
                if c["name"] == name_xml:
                    # On charge
                    for c_ui in c["lst_UI_CoilDefinition"]:
                        c_ui.loadXMLTree(e_coil)
                    lst_coil_tmp.remove(c)
                    break

            n = n.nextSiblingElement("coil")

if __name__ == "__main__":
    """
    Point d'entrée à l'exécution du script app.py
    """
    # 1 - Creation de l'application Qt
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)

    # 2 - Initialization de la fenêtre principale sur la base
    #     de la classe Example qui s'initialize à partir de la
    #     vue dans le fichier layout.ui (créé avec qtdesigner)

    from ratingPlate import UI_RatingPlate
    widg_ratingPlate = UI_RatingPlate()

    win = UI_CoilsGeneralDefinition(widg_ratingPlate)

    # 3 - Affichage de la fenêtre
    win.show()
    app.exec()