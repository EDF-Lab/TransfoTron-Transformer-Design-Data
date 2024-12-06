# -*- coding: utf-8 -*-
import sys
from os import makedirs
from os.path import join, dirname, realpath, exists

from PySide6.QtGui import QIcon, QStandardItemModel, QStandardItem
from PySide6.QtCore import Signal, QItemSelection, QIODevice, QTextStream, QFile
from PySide6.QtWidgets import QVBoxLayout, QFrame, QWidget
from PySide6.QtXml import QDomDocument

from .cable_one import UI_Cable

from .cable_all_ui import Ui_Form

# =============================================================================
# Fenêtre de définition des cables
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

class UI_CableAll(QWidget, Ui_Form):

    # Signal quand le widget est modifié par l'utilisateur (non programmatiquement)
    isModified = Signal()

    def __init__(self, ui_main, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.ui_main = ui_main

        self.setup()

    def setup(self):

        ### Pour la génération du pdf
        self.pdf_order = 10

        # Une jolie icone
        self.ui_btn_new.setIcon(QIcon(join(PATHRC, "add.png")))
        self.ui_btn_delete.setIcon(QIcon(join(PATHRC, "edit-delete.png")))

        # Préparation de l'affichage de la liste de cables
        self.model_lst_cable = QStandardItemModel()
        self.ui_listCables.setModel(self.model_lst_cable)
        self.ui_listCables.setFrameShape(QFrame.NoFrame)

        # Ajout d'un layout au ui_frame_cable
        self.layout_cable = QVBoxLayout(self.ui_frame_cable)

        ### Connecteurs
        self.ui_btn_new.clicked.connect(self.newCable)
        self.ui_btn_delete.clicked.connect(self.deleteCable)
        self.ui_listCables.selectionModel().selectionChanged.connect(self.changeCable)
        self.ui_main.isFrozen.connect(self.freezeDesign)

        # Au démarrage
        self.connectModification()

    def connectModification(self):
        """
        Connection des éléments pour émission du signal isModified
        """
        # Les sous-connections peuvent être activées par l'utilisateur ou programmatiquement
        self.ui_btn_new.clicked.connect(self.emitIsModified)
        self.ui_btn_delete.clicked.connect(self.emitIsModified)

        rootItem = self.model_lst_cable.invisibleRootItem()
        for k in range(self.model_lst_cable.rowCount(rootItem.index())):
            cable = self.model_lst_cable.item(k)
            cable.widget.isModified.connect(self.emitIsModified)

    def emitIsModified(self):
        self.isModified.emit()

    def disconnectModification(self):
        """
        Déconnection des éléments à l'émission du signal isModified
        """
        self.ui_btn_new.clicked.disconnect(self.emitIsModified)
        self.ui_btn_delete.clicked.disconnect(self.emitIsModified)

        rootItem = self.model_lst_cable.invisibleRootItem()
        for k in range(self.model_lst_cable.rowCount(rootItem.index())):
            cable = self.model_lst_cable.item(k)
            try:
                cable.widget.isModified.disconnect(self.emitIsModified)
            except:
                pass

    def checkDesign(self):
        """
        Vérification du design
        """
        # Liste d'erreurs à corriger
        lst_error = []

        # Vérification de chacun des cables
        lst_name = []
        rootItem = self.model_lst_cable.invisibleRootItem()
        for k in range(self.model_lst_cable.rowCount(rootItem.index())):
            cable = self.model_lst_cable.item(k).widget

            lst_error = lst_error + cable.checkDesign()

            if cable.ui_le_name.text() in lst_name:
                # Il y a déjà ce nom
                lst_error.append("Several cables have the same name")
            else:
                lst_name.append(cable.ui_le_name.text())

        return lst_error

    def freezeDesign(self, isFrozen):
        """
        Action lors du (dé)gelage du design
        """
        self.ui_btn_new.setEnabled(not isFrozen)
        self.ui_btn_delete.setEnabled(not isFrozen)

    def getLstPropCables(self):
        """
        Récupération de la liste des propriétés des cables de dimension non nulle
        """

        lst_propCables = []

        # Parcours de la liste de cables
        rootItem = self.model_lst_cable.invisibleRootItem()
        for k in range(self.model_lst_cable.rowCount(rootItem.index())):
            cable_prop = self.model_lst_cable.item(k).widget.getCableProperties()
            if cable_prop != {}:
                lst_propCables.append(cable_prop)

        return lst_propCables

    def newCable(self):
        """
        Définition d'un nouveau cable
        """

        widget = UI_Cable(self.ui_main, self)
        item = CableItem(self.model_lst_cable, widget, self.layout_cable)

        # Modifications
        widget.isModified.connect(self.emitIsModified)

        # Mise en surbrillance dans la liste
        self.ui_listCables.setCurrentIndex(item.index())

        return widget

    def deleteCable(self):
        """
        Suppression du cable courant si un cable est sélectionné
        """

        if self.ui_listCables.currentIndex().row() < 0:
            # Aucun cable sélectionné
            return

        # Suppression du cable
        cable_selected = self.model_lst_cable.itemFromIndex(self.ui_listCables.currentIndex())
        cable_selected.delete()
        self.model_lst_cable.removeRow(self.ui_listCables.currentIndex().row())

        # Affichage du nouveau cable sélectionné
        self.changeCable(self.ui_listCables.currentIndex())

        if self.model_lst_cable.rowCount() <= 0:
            self.newCable()

    def changeCable(self, index):
        """
        Changement des propriétés du cable dans l'interface lors d'un changement de sélection
        """

        if self.ui_listCables.currentIndex().row() < 0:
            # Aucun cable sélectionné
            return

        if isinstance(index, QItemSelection):
            if len(index.indexes()) > 0:
                index = index.indexes()[0]
            else:
                return

        # Affichage du widget
        cable_selected = self.model_lst_cable.itemFromIndex(index)
        cable_selected.showWidget()

    def showEvent(self, event):
        """
        A l'affichage
        """
        # S'il n'y a aucun cable, on en met un vide
        # Permet de ne pas avoir un cable vide lors du chargement d'un xml plutot que de le mettre en init
        if self.model_lst_cable.rowCount() <= 0:
            self.newCable()

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

        # Parcours de la liste de cables
        rootItem = self.model_lst_cable.invisibleRootItem()
        for k in range(self.model_lst_cable.rowCount(rootItem.index())):
            cable = self.model_lst_cable.item(k).widget
            cable.addXMLTree(root, docDom)

        # Enregistrement
        header = docDom.createProcessingInstruction("xml", "version=\"1.0\" encoding=\"UTF-8\"")
        docDom.insertBefore(header, root)
        file = QFile(join(path_design, "cable.xml"))
        file.open(QIODevice.WriteOnly)
        out = QTextStream(file)
        docDom.save(out, 4, QDomDocument.EncodingFromDocument)
        file.close()

    def addPDF(self, pdf, part, lst_id_calcul=[]):
        """
        Remplissage du fichier PDF
        """
        pdf.set_font()

        if "data_detail" in part:
            pdf.ln()
            pdf.toc_entry("Cables", 2)

            # Récupération des widgets cable
            rootItem = self.model_lst_cable.invisibleRootItem()
            lst_ui_cable = []
            for k in range(self.model_lst_cable.rowCount(rootItem.index())):
                lst_ui_cable.append(self.model_lst_cable.item(k).widget)

            # Rangement de la liste par ordre alphabétique du nom
            lst_ui_cable.sort(key=lambda x: x.ui_le_name.text())
            for cable in lst_ui_cable:
                cable.addPDF(pdf, part, lst_id_calcul)

    def loadXML(self, tmpSaveDirPath):
        """
        Chargement du fichier xml dans le ttx
        """
        path_xml = join(tmpSaveDirPath, "design", "cable.xml")
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

        n = root.firstChildElement("cable")
        while not n.isNull():
            e_cable = n.toElement()
            self.newCable().loadXMLTree(e_cable)

            n = n.nextSiblingElement("cable")

        self.connectModification()

class CableItem(QStandardItem):
    """
    Classe représentant un cable
    """

    def __init__(self, model, widget, layout):
        super().__init__("--- To define ---")

        self.setEditable(False)
        self.model = model

        # Ajout du cable au modèle
        rootItem = model.invisibleRootItem()
        rootItem.appendRow(self)

        # Enregistrement du widget porté (None s'il n'y en a pas)
        self.widget = widget
        self.layout = layout

        # Pour que le nom du cable se change tout seul
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

    # 2 - Initialization de la fenêtre principale sur la base
    #     de la classe Example qui s'initialize à partir de la
    #     vue dans le fichier layout.ui (créé avec qtdesigner)
    win = UI_CableAll()

    # 3 - Affichage de la fenêtre
    win.show()
    app.exec()