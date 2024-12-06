# -*- coding: utf-8 -*-
import sys
from os import makedirs
from os.path import join, dirname, realpath, exists

from PySide6.QtGui import QIcon, QStandardItemModel, QStandardItem
from PySide6.QtCore import Signal, QItemSelection, QIODevice, QTextStream, QFile
from PySide6.QtWidgets import QVBoxLayout, QFrame, QWidget
from PySide6.QtXml import QDomDocument

from .disc_one import UI_Disc

from .disc_all_ui import Ui_Form

# =============================================================================
# Widget de définition des disques
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

class UI_DiscAll(QWidget, Ui_Form):

    # Signal quand le widget est modifié par l'utilisateur (non programmatiquement)
    isModified = Signal()

    def __init__(self, widg_ratingPlate, widg_cableAll, ui_main, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.widg_ratingPlate = widg_ratingPlate
        self.widg_cableAll = widg_cableAll
        self.ui_main = ui_main

        self.setup()

    def setup(self):

        # Une jolie icone
        self.ui_btn_new.setIcon(QIcon(join(PATHRC, "add.png")))
        self.ui_btn_delete.setIcon(QIcon(join(PATHRC, "edit-delete.png")))

        # Préparation de l'affichage de la liste de discs
        self.model_lst_disc = QStandardItemModel()
        self.ui_listDisc.setModel(self.model_lst_disc)
        self.ui_listDisc.setFrameShape(QFrame.NoFrame)

        # Ajout d'un layout au ui_frame_discOne
        self.layout_discOne = QVBoxLayout(self.ui_frame_discOne)

        ### Connecteurs
        self.ui_listDisc.selectionModel().selectionChanged.connect(self.changeDisc)
        self.ui_btn_new.clicked.connect(self.newDisc)
        self.ui_btn_delete.clicked.connect(self.deleteDisc)
        self.ui_main.isFrozen.connect(self.freezeDesign)

        ### Au démarrage
        self.connectModification()

    def connectModification(self):
        """
        Connection des éléments pour émission du signal isModified
        """
        # Les sous-connections peuvent être activées par l'utilisateur ou programmatiquement
        self.ui_btn_new.clicked.connect(self.emitIsModified)
        self.ui_btn_delete.clicked.connect(self.emitIsModified)

        rootItem = self.model_lst_disc.invisibleRootItem()
        for k in range(self.model_lst_disc.rowCount(rootItem.index())):
            disc = self.model_lst_disc.item(k)
            disc.widget.isModified.connect(self.emitIsModified)

    def emitIsModified(self):
        self.isModified.emit()

    def disconnectModification(self):
        """
        Déconnection des éléments à l'émission du signal isModified
        """
        self.ui_btn_new.clicked.disconnect(self.emitIsModified)
        self.ui_btn_delete.clicked.disconnect(self.emitIsModified)

        rootItem = self.model_lst_disc.invisibleRootItem()
        for k in range(self.model_lst_disc.rowCount(rootItem.index())):
            disc = self.model_lst_disc.item(k)
            try:
                disc.widget.isModified.disconnect(self.emitIsModified)
            except:
                pass

    def checkDesign(self):
        """
        Vérification du design
        """
        # Liste d'erreurs à corriger
        lst_error = []

        # Vérification de chacun des discs
        lst_name = []
        rootItem = self.model_lst_disc.invisibleRootItem()
        for k in range(self.model_lst_disc.rowCount(rootItem.index())):
            disc = self.model_lst_disc.item(k).widget

            lst_error = lst_error + disc.checkDesign()

            if disc.ui_le_name.text() in lst_name:
                # Il y a déjà ce nom
                lst_error.append("Several discs have the same name")
            else:
                lst_name.append(disc.ui_le_name.text())

        return lst_error

    def freezeDesign(self, isFrozen):
        """
        Action lors du (dé)gelage du design
        """
        self.ui_btn_new.setEnabled(not isFrozen)
        self.ui_btn_delete.setEnabled(not isFrozen)

    def newDisc(self):
        """
        Ajout d'un disc à la liste
        """
        widget = UI_Disc(self.widg_ratingPlate, self.widg_cableAll, self, self.ui_main, self)
        item = DiscItem(self.model_lst_disc, widget, self.layout_discOne)

        # Modifications
        widget.isModified.connect(self.emitIsModified)

        # Mise en surbrillance dans la liste
        self.ui_listDisc.setCurrentIndex(item.index())

        return widget

    def deleteDisc(self):
        """
        Suppression du disc courant si un disc est sélectionné
        """

        if self.ui_listDisc.currentIndex().row() < 0:
            # Aucun disc sélectionné
            return

        # Suppression du disc
        disc_selected = self.model_lst_disc.itemFromIndex(self.ui_listDisc.currentIndex())
        disc_selected.widget.removeDisc()
        disc_selected.delete()
        self.model_lst_disc.removeRow(self.ui_listDisc.currentIndex().row())

        # Affichage du nouveau disc sélectionné
        self.changeDisc(self.ui_listDisc.currentIndex())

        if self.model_lst_disc.rowCount() <= 0:
            self.newDisc()

    def changeDisc(self, index):
        """
        Changement des propriétés du disc dans l'interface lors d'un changement de sélection
        """

        if self.ui_listDisc.currentIndex().row() < 0:
            # Aucun disc sélectionné
            return

        if isinstance(index, QItemSelection):
            if len(index.indexes()) > 0:
                index = index.indexes()[0]
            else:
                return

        # Affichage du widget
        disc_selected = self.model_lst_disc.itemFromIndex(index)
        disc_selected.showWidget()

    def showEvent(self, event):
        """
        A l'affichage
        """
        # S'il n'y a aucun disc, on en met un vide
        # Permet de ne pas avoir un disc vide lors du chargement d'un xml plutot que de le mettre en init
        if self.model_lst_disc.rowCount() <= 0:
            self.newDisc()

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

        # Parcours de la liste de discs
        rootItem = self.model_lst_disc.invisibleRootItem()
        for k in range(self.model_lst_disc.rowCount(rootItem.index())):
            disc = self.model_lst_disc.item(k).widget
            disc.addXMLTree(root, docDom)

        # Enregistrement
        header = docDom.createProcessingInstruction("xml", "version=\"1.0\" encoding=\"UTF-8\"")
        docDom.insertBefore(header, root)
        file = QFile(join(path_design, "disc.xml"))
        file.open(QIODevice.WriteOnly)
        out = QTextStream(file)
        docDom.save(out, 4, QDomDocument.EncodingFromDocument)
        file.close()

    def loadXML(self, tmpSaveDirPath):
        """
        Chargement du fichier xml dans le ttx
        """
        path_xml = join(tmpSaveDirPath, "design", "disc.xml")
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

        self.disconnectModification()

        n = root.firstChildElement("disc")
        while not n.isNull():
            e_disc = n.toElement()
            self.newDisc().loadXMLTree(e_disc)

            n = n.nextSiblingElement("disc")

        self.connectModification()

class DiscItem(QStandardItem):
    """
    Classe représentant un item qui sera dans la liste de discs
    """

    def __init__(self, model, widget, layout):
        super().__init__("--- To define ---")

        self.setEditable(False)
        self.model = model

        # Ajout du disc au modèle
        rootItem = self.model.invisibleRootItem()
        rootItem.appendRow(self)

        # Enregistrement du widget porté
        self.widget = widget
        self.layout = layout

        # Pour que le nom du disc se change tout seul
        self.widget.ui_le_name.textChanged.connect(self.setName)

        # Ajout au layout
        self.layout.addWidget(self.widget)
        self.showWidget()

    def setName(self):
        self.setText(self.widget.ui_le_name.text())
        self.model.sort(0)

    def showWidget(self):

        # Parcours du layout et masquage des widgets visibles
        for k in range(self.layout.count()):
            item = self.layout.itemAt(k)
            item.widget().hide()

        # Affichage du widget
        self.widget.show()

    def delete(self):
        self.widget.hide()
        self.layout.removeWidget(self.widget)

if __name__ == "__main__":
    """
    Point d'entrée à l'exécution du script app.py
    """
    # 1 - Creation de l'application Qt
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)

    win = UI_DiscAll()

    # 3 - Affichage de la fenêtre
    win.show()
    app.exec()