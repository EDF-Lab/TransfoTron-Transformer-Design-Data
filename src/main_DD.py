# -*- coding: utf-8 -*-
import sys
from os import listdir, remove, walk, startfile
from os.path import join, dirname, realpath, abspath, basename, splitext, normpath
from shutil import rmtree
from datetime import datetime
from functools import partial
from zipfile import ZipFile, ZIP_BZIP2
from multiprocessing import freeze_support

from matplotlib import pyplot as plt
plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.size"] = 10

from PySide6.QtGui import QIcon, QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt, Signal, QItemSelection, QFile, QDir, QIODevice, QTextStream, QSettings, QCoreApplication, QByteArray, QCommandLineParser, QFileInfo, QTemporaryDir
from PySide6.QtWidgets import QMessageBox, QVBoxLayout, QFileDialog, QApplication, QMainWindow
from PySide6.QtXml import QDomDocument

from tfo.definition.ratingPlate import UI_RatingPlate
from tfo.definition.material_properties import UI_MaterialProperties
from tfo.definition.cable_all import UI_CableAll
from tfo.definition.disc_all import UI_DiscAll
from tfo.definition.coilsGeneralDefinition import UI_CoilsGeneralDefinition

from tfo.error.error import UI_Error
from tfo.utils.pdf_generator import PDF
from tfo.utils.designCheck import UI_DesignCheck

from license.about import UI_About
from license.license import UI_License
from main_DD_ui import Ui_MainWindow

# En fonction du mode compilé ou non
if hasattr(sys, "_MEIPASS"):
    print(sys._MEIPASS)

# =============================================================================
# Fenêtre principale, contient l'arbre et gère les différents widgets
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

class UI_Main(QMainWindow, Ui_MainWindow):

    # Signal quand le design est freezé
    isFrozen = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setup()

    def setup(self):

        ### Une jolie icone
        self.setWindowIcon(QIcon(join(PATHRC, "icone.ico")))

        ### Configuration des actions
        # Menu File
        self.action_New.setIcon(QIcon(join(PATHRC, "document-new.png")))
        self.action_Open.setIcon(QIcon(join(PATHRC, "document-open.png")))
        self.action_Save.setIcon(QIcon(join(PATHRC, "document-save.png")))
        self.action_SaveAs.setIcon(QIcon(join(PATHRC, "document-save-as.png")))
        # Menu Design
        self.action_GenPDF.setIcon(QIcon(join(PATHRC, "pdf.png")))
        self.action_Check.setIcon(QIcon(join(PATHRC, "check_green.png")))

        # Ajout d'un layout au ui_activeWidget
        self.ui_layout_activeWidget = QVBoxLayout(self.ui_activeWidget)

        ### Configuration de l'arbre du cas
        # Création du modèle
        self.model = QStandardItemModel()
        self.ui_treeCase.setModel(self.model)
        self.ui_treeCase.setHeaderHidden(True)

        ### Dock comments (sous forme d'onglets et à la bonne taille)
        self.tabifyDockWidget(self.ui_dockCase, self.ui_dockComments)
        self.ui_dockCase.raise_()
        self.resizeDocks([self.ui_dockCase], [2.5*self.ui_dockCase.width()], Qt.Horizontal)
        self.ui_txt_comments.textChanged.connect(self.uiWasModified)

        # Divers
        self.readSettings()
        self.uiChanged = False
        self.designFrozen = False
        self.tmpSaveDirPath = None
        self.curFilePath = None
        self.window_mode = None

        # Connection
        # Toutes les façons possibles de sélectionner un item
        self.ui_treeCase.selectionModel().selectionChanged.connect(self.changeTreeCase)

        # Autres
        self.action_Save.triggered.connect(self.save)
        self.action_SaveAs.triggered.connect(self.saveAs)
        self.action_New.triggered.connect(self.new)
        self.action_Open.triggered.connect(self.openFile)
        self.action_GenPDF.triggered.connect(self.generatePDF)
        self.action_Check.triggered.connect(partial(self.checkDesign, True))
        self.action_About.triggered.connect(UI_About(self).exec)
        self.action_Licenses.triggered.connect(UI_License(self).exec)
        # Au démarrage
        self.deleteTempFiles()

        # On est prêts
        self.ui_statusbar.showMessage("Ready", 2000)

    def changeTreeCase(self, index):
        """
        Action lors du changement de sélection dans l'arbre des cas
        """
        if isinstance(index, QItemSelection):
            if len(index.indexes()) > 0:
                index = index.indexes()[0]
            else:
                return

        # Affichage du nouveau TreeCase (et masquage du précédent)
        if self.model.itemFromIndex(index) is not None:
            self.model.itemFromIndex(index).showWidget()

    def getAllTreeCaseWidget(self, lst_TreeCase, parentIndex=None, onlyVisible=False):
        """
        Renvoi la liste de tous les TreeCase
        lst_TreeCase = [] au 1er appel sinon ça se répète
        """

        if parentIndex == None:
            rootItem = self.model.invisibleRootItem()
            parentIndex = self.model.indexFromItem(rootItem)

        for kk in range(self.model.rowCount(parentIndex)):
            index = self.model.index(kk, 0, parentIndex)
            UI_widget = self.model.itemFromIndex(index).widget

            if UI_widget != None:
                if onlyVisible:
                    if not self.ui_treeCase.isRowHidden(kk, parentIndex):
                        lst_TreeCase.append(UI_widget)
                else:
                    lst_TreeCase.append(UI_widget)

            if self.model.hasChildren(index):
                # En récursif
                lst_TreeCase = self.getAllTreeCaseWidget(lst_TreeCase, index, onlyVisible)

        return lst_TreeCase

    def resetAll(self):
        """
        Redéfinition de l'ensemble des widgets
        """
        # Parcours du layout et masquage des widgets visibles
        for k in range(self.ui_layout_activeWidget.count()):
            item = self.ui_layout_activeWidget.itemAt(k)
            item.widget().hide()

        # Définition du chemin du dossier temporaire
        self.setTempSaveDir()

        # Reset
        self.model.clear()
        rootItem = self.model.invisibleRootItem()

        # Ajout des éléments
        self.widg_ratingPlate = UI_RatingPlate(self, self)
        self.widg_ratingPlate.isModified.connect(self.uiWasModified)
        self.widg_ratingPlate.studyNameUpdated.connect(self.updateWindowTitle)
        self.widg_ratingPlate.updateStudyName()
        self.tree_ratingPlate = TreeCase("Rating plate", rootItem, self.ui_treeCase, self.widg_ratingPlate, self.ui_layout_activeWidget)

        self.tree_material = TreeCase("Material properties", rootItem, self.ui_treeCase, None, self.ui_layout_activeWidget, icons=["folder.png"])
        self.widg_materialOil = UI_MaterialProperties("oil", self, self)
        self.widg_materialOil.isModified.connect(self.uiWasModified)
        TreeCase("Oil", self.tree_material, self.ui_treeCase, self.widg_materialOil, self.ui_layout_activeWidget)
        self.widg_materialCopper = UI_MaterialProperties("copper", self, self)
        self.widg_materialCopper.isModified.connect(self.uiWasModified)
        TreeCase("Copper", self.tree_material, self.ui_treeCase, self.widg_materialCopper, self.ui_layout_activeWidget)
        self.widg_materialPaper = UI_MaterialProperties("paper", self, self)
        self.widg_materialPaper.isModified.connect(self.uiWasModified)
        TreeCase("Paper", self.tree_material, self.ui_treeCase, self.widg_materialPaper, self.ui_layout_activeWidget)
        self.widg_materialVarnish = UI_MaterialProperties("varnish", self, self)
        self.widg_materialVarnish.isModified.connect(self.uiWasModified)
        TreeCase("Varnish/Epoxy", self.tree_material, self.ui_treeCase, self.widg_materialVarnish, self.ui_layout_activeWidget)
        self.widg_materialPressboard = UI_MaterialProperties("pressboard", self, self)
        self.widg_materialPressboard.isModified.connect(self.uiWasModified)
        TreeCase("Pressboard", self.tree_material, self.ui_treeCase, self.widg_materialPressboard, self.ui_layout_activeWidget)

        self.tree_windings = TreeCase("Windings", rootItem, self.ui_treeCase, None, self.ui_layout_activeWidget, icons=["folder.png"])
        self.widg_cableAll = UI_CableAll(self, self)
        self.widg_cableAll.isModified.connect(self.uiWasModified)
        self.tree_cableAll = TreeCase("Cables", self.tree_windings, self.ui_treeCase, self.widg_cableAll, self.ui_layout_activeWidget)
        self.widg_discAll = UI_DiscAll(self.widg_ratingPlate, self.widg_cableAll, self, self)
        self.widg_discAll.isModified.connect(self.uiWasModified)
        self.tree_discAll = TreeCase("Discs", self.tree_windings, self.ui_treeCase, self.widg_discAll, self.ui_layout_activeWidget)
        self.widg_coilsGen = UI_CoilsGeneralDefinition(self.widg_ratingPlate, self)
        self.widg_coilsGen.isModified.connect(self.uiWasModified)
        self.tree_coilsGen = TreeCase("Coils", self.tree_windings, self.ui_treeCase, self.widg_coilsGen, self.ui_layout_activeWidget)

        # Affichage du rating plate
        self.tree_ratingPlate.showWidget()

        # Nom de la fenêtre
        self.updateWindowTitle(self.widg_ratingPlate.updateStudyName())

    def changeMode(self):
        """
        Changement du mode de transfoTron
        """
        # On ne fait rien dans la version DR, mais appelé par RatingPlate

        # Visibles indépendamment du mode
        self.tree_ratingPlate.showItem()

        # Mode design review
        self.tree_material.showItem()
        if hasattr(self, "widg_ratingPlate"):
            if self.widg_ratingPlate.isCoreType():
                self.tree_windings.showItem()
            else:
                self.tree_windings.hideItem()
        else:
            self.tree_windings.hideItem()

        # On fait passer l'info à widg_ratingPlate
        if hasattr(self, "widg_ratingPlate"):
            self.widg_ratingPlate.changeMode(True, False, False)

        self.checkDesign(False)

    def checkDesign(self, showDiag=True):
        """
        Vérification du design
        """
        # Liste d'erreurs à corriger
        lst_error = []

        # Parcours des widgets
        lst_case = self.getAllTreeCaseWidget([], None, True)
        for w in lst_case:
            if "checkDesign" in dir(w):
                lst_error = lst_error + w.checkDesign()
        if len(lst_error) > 0:
            # Affichage
            if showDiag:
                run = UI_DesignCheck(lst_error, self)
                run.show()
            self.action_Check.setIcon(QIcon(join(PATHRC, "check_red.png")))
            return False
        else:
            self.action_Check.setIcon(QIcon(join(PATHRC, "check_green.png")))
            return True

    def new(self):
        """
        Définition d'un nouveau transfo
        """

        if self.maybeSave():
            # On peut tout reseter
            self.resetAll()
            self.setCurrentFile(None)

    def setCurrentFile(self, curFilePath):
        """
        Définition du chemin courant du fichier d'enregistrement
        """
        if curFilePath == None:
            self.curFilePath = None
        else:
            self.curFilePath = abspath(curFilePath)
            # pour retenir le current path au redémarrage de TransfoTron ou dans les autres fenêtres de choix d'un fichier
            settings = QSettings(QCoreApplication.organizationName(), QCoreApplication.applicationName())
            settings.setValue("curPath", dirname(curFilePath))

        if hasattr(self, "widg_ratingPlate"):
            self.updateWindowTitle(self.widg_ratingPlate.updateStudyName())
        else:
            self.updateWindowTitle()

        # Pas de modification car chargement / enregistrement / new
        self.uiChanged = False
        self.setWindowModified(self.uiChanged)

    def updateWindowTitle(self, str_study=None):
        """
        Mise à jour du titre de la fenêtre
        """
        # Version
        shownName = "TransfoTron Design Data v%s"%QCoreApplication.applicationVersion()
        # Nom du fichier
        if not self.curFilePath is None:
            shownName += " - %s"%basename(self.curFilePath)
        # Study
        if not str_study is None:
            shownName += " - %s"%str_study

        self.setWindowTitle(shownName)

    def setTempSaveDir(self):
        """
        Définition du dossier temporaire pour l'extraction du fichier d'enregistrement
        """
        tmp = QTemporaryDir()
        tmp.setAutoRemove(False)
        self.tmpSaveDirPath = tmp.path()
        print(self.tmpSaveDirPath)

    def openFile(self):
        if self.maybeSave():
            path_open, _ = QFileDialog.getOpenFileName(self, "Open TransfoTron file", QSettings(QCoreApplication.organizationName(), QCoreApplication.applicationName()).value("curPath"), "*.ttx")
            if path_open != "":
                self.loadFile(path_open)

    def save(self):
        if self.curFilePath == None:
            return self.saveAs()
        else:
            return self.saveFile(self.curFilePath)

    def saveAs(self):
        ### Chemin d'enregistrement
        path_save, _ = QFileDialog.getSaveFileName(self, "Save TransfoTron file", QSettings(QCoreApplication.organizationName(), QCoreApplication.applicationName()).value("curPath"), "*.ttx")
        if path_save == "":
            return False

        if not path_save[-4:]==".ttx":
            path_save = path_save + ".ttx"

        return self.saveFile(path_save)

    def saveFile(self, path_save):
        """
        Fonction d'enregistrement du fichier
        """
        # Curseur de chargement
        QApplication.setOverrideCursor(Qt.WaitCursor)

        # Nouveau dossier temporaire
        self.setTempSaveDir()

        ### Création des xml dans le dossier temporaire
        ## main.xml
        doc = QDomDocument()
        root = doc.appendChild(doc.createElement("root"))
        root.appendChild(doc.createComment("Created on " + str(datetime.now().isoformat())))
        # Version de TransfoTron
        tag_tmp = doc.createElement("version")
        tag_tmp.appendChild(doc.createTextNode("%s"%QCoreApplication.applicationVersion()))
        root.appendChild(tag_tmp)
        # Ajout du mode
        tag_tmp = doc.createElement("mode")
        lst_mode = ["DR"]
        tag_tmp.appendChild(doc.createTextNode("&".join(lst_mode)))
        root.appendChild(tag_tmp)
        # Ajout des commentaires
        tag_tmp = doc.createElement("comments")
        tag_tmp.appendChild(doc.createTextNode("%s"%self.ui_txt_comments.toPlainText()))
        root.appendChild(tag_tmp)

        # Enregistrement
        header = doc.createProcessingInstruction("xml", "version=\"1.0\" encoding=\"UTF-8\"")
        doc.insertBefore(header, root)
        file = QFile(join(self.tmpSaveDirPath, "main.xml"))
        file.open(QIODevice.WriteOnly)
        out = QTextStream(file)
        doc.save(out, 4, QDomDocument.EncodingFromDocument)
        file.close()

        ## Passage aux autres widgets
        # Parcours des UI_widget
        lst_case = self.getAllTreeCaseWidget([])
        for w in lst_case:
            print("saveFile", w.__class__.__name__)
            w.generateXML(self.tmpSaveDirPath)

        ### Zippage de l'ensemble et enregistrement
        # Récupération de tous les chemins des fichiers
        file_paths = []
        for root, directories, files in walk(self.tmpSaveDirPath):
            for filename in files:
                file_paths.append(join(root, filename))
        # Ecriture du fichier .ttx
        with ZipFile(path_save, 'w', compression=ZIP_BZIP2) as zip_file:
            for file in file_paths:
                zip_file.write(file, arcname=file.replace(self.tmpSaveDirPath, ""))

        self.setCurrentFile(path_save)
        self.ui_statusbar.showMessage("TransfoTron file saved", 2000)
        QApplication.restoreOverrideCursor()

        return True

    def generatePDF(self):
        """
        Génération du fichier pdf
        """
        # Enregistrement du fichier TransfoTron (pour cohérence)
        if not self.maybeSave():
            return False

        # Choix du chemin d'enregistrement
        path_save, _ = QFileDialog.getSaveFileName(self, "Save PDF file", QSettings(QCoreApplication.organizationName(), QCoreApplication.applicationName()).value("curPath"), "*.pdf")
        if path_save == "":
            return False

        if not path_save[-4:]==".pdf":
            path_save = path_save + ".pdf"

        # Curseur de chargement
        QApplication.setOverrideCursor(Qt.WaitCursor)

        ### Création du pdf
        title = self.widg_ratingPlate.updateStudyName()
        v_client = QCoreApplication.applicationVersion()
        v_server = ""
        pdf = PDF(title, v_client, v_server)

        ### Page de garde
        # Eléments centraux
        pdf.set_y(pdf.t_margin+20)
        pdf.ln(10)
        pdf.set_font(style="B", size=20)
        pdf.multi_cell(txt=title, align="C")
        pdf.set_font()
        pdf.ln(5)
        pdf.image(join(PATHRC, "transfo.png"), w=80, align="C")
        pdf.set_y(-pdf.b_margin-80)

        # Chemin du fichier TransfoTron
        if not self.curFilePath is None:
            pdf.set_font(style="I")
            pdf.multi_cell(txt="Report generated from:")
            pdf.multi_cell(txt=self.curFilePath)
            pdf.set_font()
            pdf.ln()

        # Disclaimer
        pdf.set_draw_color(0, 0, 0)
        pdf.set_line_width(0.2)
        pdf.line(pdf.get_x(), pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())

        ### Sommaire
        pdf.add_page()
        pdf.enableFooter = True
        pdf.toc_setLocation()

        ### Contenu
        lst_case = [w for w in self.getAllTreeCaseWidget([]) if hasattr(w, "pdf_order")]
        lst_case = sorted(lst_case, key=lambda x: x.pdf_order)

        # Infos générales
        pdf.toc_entry("Transformer main data", 1)
        for w in lst_case:
            if "addPDF" in dir(w):
                w.addPDF(pdf, "data_general")
        if self.ui_txt_comments.toPlainText() != "":
            # Commentaires
            pdf.add_page()
            pdf.toc_entry("Study comments", 1)
            pdf.multi_cell(txt=self.ui_txt_comments.toPlainText())
        # Données détaillées
        pdf.add_page()
        pdf.toc_entry("Detailed design", 1)
        for w in lst_case:
            if "addPDF" in dir(w):
                w.addPDF(pdf, "data_detail")

        ### Enregistrement du PDF
        try:
            pdf.save(path_save)
        except:
            QMessageBox.critical(self, "TransfoTron", \
                                            "Close the file " + path_save + " and try again.", \
                                            QMessageBox.Ok, QMessageBox.Ok)
            QApplication.restoreOverrideCursor()
            return False

        self.ui_statusbar.showMessage("PDF file generated", 2000)
        QApplication.restoreOverrideCursor()

        # Ouverture du fichier
        startfile(normpath(path_save))

    def deleteTempFiles(self):
        """
        Suppression de tous les fichiers temporaires TransfoTron qui trainent
        Les sorties en erreur n'effacent pas automatiquement ces fichiers
        """
        path_tmp = QDir.tempPath()
        file_prefix = QCoreApplication.applicationName()

        for f in listdir(path_tmp):
            if f[:len(file_prefix)] == file_prefix:
                try:
                    remove(join(path_tmp, f))
                except:
                    rmtree(join(path_tmp, f), ignore_errors=True)

    def loadFile(self, path_open):
        """
        Chargement d'un fichier
        """
        # On reset tout
        self.resetAll()

        # Extension du fichier
        _, ext = splitext(path_open)

        # Curseur de chargement
        QApplication.setOverrideCursor(Qt.WaitCursor)

        if ext == ".ttx":
            ### Dézippage dans le dossier temporaire
            try:
                with ZipFile(path_open, "r") as zip_file:
                    zip_file.extractall(self.tmpSaveDirPath)
            except:
                QApplication.restoreOverrideCursor()
                QMessageBox.warning(self, "TransfoTron", "Cannot read file %s."%path_open)
                QApplication.setOverrideCursor(Qt.WaitCursor)
                return

            ### Chargement des infos
            ## main.xml
            file = QFile(join(self.tmpSaveDirPath, "main.xml"))
            doc = QDomDocument()
            if not file.open(QIODevice.ReadOnly):
                file.close()
                QApplication.restoreOverrideCursor()
                QMessageBox.warning(self, "TransfoTron", "Error while loading XML part: main.xml")
                QApplication.setOverrideCursor(Qt.WaitCursor)
            if not doc.setContent(file):
                file.close()
                QApplication.restoreOverrideCursor()
                QMessageBox.warning(self, "TransfoTron", "Error while loading XML part: main.xml")
                QApplication.setOverrideCursor(Qt.WaitCursor)
            file.close()

            root = doc.documentElement()
            if root.isNull():
                return

            # Commentaires
            tag_tmp = root.firstChildElement("comments")
            if not tag_tmp.isNull():
                self.ui_txt_comments.setPlainText(tag_tmp.text())

            ## Passage aux autres widgets
            # Parcours des UI_widget
            lst_case = self.getAllTreeCaseWidget([])

            for w in lst_case:
                # Parcours par ordre "de haut vers le bas" de la liste du gui
                print("loadXML", w.__class__.__name__)
                if hasattr(sys, "_MEIPASS"):
                    # En mode compilé
                    try:
                        w.loadXML(self.tmpSaveDirPath)
                    except:
                        QApplication.restoreOverrideCursor()
                        QMessageBox.warning(self, "TransfoTron", "Error while loading XML part: %s."%w.__class__.__name__)
                        QApplication.setOverrideCursor(Qt.WaitCursor)
                        print("Error...")
                else:
                    w.loadXML(self.tmpSaveDirPath)

        else:
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, "TransfoTron", "Cannot read file %s."%path_open)
            return

        # Nom du fichier
        self.setCurrentFile(path_open)
        self.ui_statusbar.showMessage("TransfoTron file loaded", 2000)
        QApplication.restoreOverrideCursor()

        # On check le design
        self.checkDesign(False)

    def readSettings(self):
        settings = QSettings(QCoreApplication.organizationName(), QCoreApplication.applicationName())
        geometry = settings.value("geometry", QByteArray())

        if geometry.isEmpty():
            self.setWindowState(Qt.WindowMaximized)
        else:
            self.restoreGeometry(geometry)

    def writeSettings(self):
        settings = QSettings(QCoreApplication.organizationName(), QCoreApplication.applicationName())
        settings.setValue("geometry", self.saveGeometry())

    def uiWasModified(self):
        """
        Méthode appelée lorsque qu'un sous-ui est modifié par l'utilisateur
        """
        # On enregistre le changement
        self.uiChanged = True

        # Affichage du * dans le titre de la fenêtre
        self.setWindowModified(self.uiChanged)

        # On check le design
        self.checkDesign(False)

    def maybeSave(self):

        if not self.uiChanged:
            return True

        ret = QMessageBox.warning(self, "TransfoTron", \
            "Do you want to save the changes?", \
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)

        if ret == QMessageBox.Yes:
            return self.save()
        elif ret == QMessageBox.No:
            return True
        elif ret == QMessageBox.Cancel:
            return False

    def closeEvent(self, event):

        if self.maybeSave():
            self.writeSettings() # Pour se souvenir de la taille et position de la fenetre et du curPath
            self.deleteTempFiles()
            event.accept()
        else:
            event.ignore()

class TreeCase(QStandardItem):
    """
    Classe représentant un item qui sera dans l'arbre de cas
    """

    def __init__(self, text, nodeParent, treeView, widget, layoutDisplay, icons=["document-new.png", "txt.png"], toolTip=""):
        super().__init__(text)
        self.treeView = treeView
        self.layoutDisplay = layoutDisplay

        # Ajout au parent
        self.icons = icons
        self.setIcon(QIcon(join(PATHRC, self.icons[0])))
        self.setToolTip(toolTip)
        self.setEditable(False)
        nodeParent.appendRow(self)

        self.chargeWidget(widget)

    def chargeWidget(self, widget):
        # Enregistrement du widget porté (None s'il n'y en a pas)
        self.widget = widget
        # Ajout au layout
        if self.widget != None:
            self.layoutDisplay.addWidget(self.widget)
        # Et masquage
        self.hideWidget()

    def showWidget(self):
        # Action uniquement s'il y a un widget
        if self.widget == None:
            return

        # Parcours du layout et masquage des widgets visibles
        for k in range(self.layoutDisplay.count()):
            item = self.layoutDisplay.itemAt(k)
            item.widget().hide()

        # Affichage du widget
        self.widget.show()
        if len(self.icons) > 1:
            self.setIcon(QIcon(join(PATHRC, self.icons[1])))

    def hideWidget(self):
        if self.widget != None:
            self.widget.hide()

    def showItem(self):
        """
        Affichage de l'item dans l'arbre des cas
        """
        # Affichage de l'item
        if self.parent() is None:
            parent = self.treeView.model().invisibleRootItem()
        else:
            parent = self.parent()
        self.treeView.setRowHidden(self.row(), parent.index(), False)
        if self.index() in self.treeView.selectedIndexes():
            self.showWidget()
        # Et de ses enfants
        for k in range(self.rowCount()):
            self.child(k).showItem()

    def hideItem(self):
        """
        Masquage de l'item dans l'arbre des cas
        """
        # Masquage de l'item
        if self.parent() is None:
            parent = self.treeView.model().invisibleRootItem()
        else:
            parent = self.parent()
        self.treeView.setRowHidden(self.row(), parent.index(), True)
        self.hideWidget()
        # Et de ses enfants
        for k in range(self.rowCount()):
            self.child(k).hideItem()

if __name__ == "__main__":
    """
    Point d'entrée à l'exécution du script app.py
    """
    # Pour que le multiprocessing fonctionne en mode compilé (sans effet sinon)
    # https://docs.python.org/3.7/library/multiprocessing.html?highlight=process#multiprocessing.freeze_support
    freeze_support()

    # 1 - Creation de l'application Qt
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    app.setOrganizationName("TT")
    app.setApplicationName("TransfoTron - Design Data")
    app.setApplicationVersion("1.6.3.DD")

    # 2 - Initialization de la fenêtre principale
    # Récupération des arguments (un fichier à charger)
    parser = QCommandLineParser()
    parser.setApplicationDescription(QCoreApplication.applicationName())
    parser.addHelpOption()
    parser.addVersionOption()
    parser.addPositionalArgument("file", "The file to open.")
    parser.process(app)

    # Lancement
    win = UI_Main()

    # Modification de la gestion des erreurs
    def my_exception_hook(exctype, value, tb):
        win_error = UI_Error(win)
        win_error.writeError(exctype, value, tb)
        win_error.exec()
    if hasattr(sys, "_MEIPASS"):
        # On n'affiche la fenetre d'erreur que si on est compilé
        sys.excepthook = my_exception_hook

    # 3 - Affichage de la fenêtre
    win.show()

    # 4 - Fermeture du splash screen
    try:
        # N'est possible qu'en mode executable
        import pyi_splash
        pyi_splash.close()
    except:
        pass

    # Chargement du chemin en paramètre s'il y en a un
    if len(parser.positionalArguments()) == 0:
        win.new()
    else:
        if not win.window_mode is None:
            win.window_mode.close()
        fullPath = QFileInfo(parser.positionalArguments()[0]).absoluteFilePath()
        win.loadFile(fullPath)

    sys.exit(app.exec())