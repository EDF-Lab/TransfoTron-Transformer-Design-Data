# -*- coding: utf-8 -*-
import sys
from os.path import join, dirname, realpath, isfile, normpath, isdir
from os import listdir

from PySide6.QtWidgets import QApplication, QDialog
from PySide6.QtCore import Qt, QItemSelection, QCoreApplication
from PySide6.QtGui import QStandardItemModel, QStandardItem

from .license_ui import Ui_Dialog

# =============================================================================
# Popup License
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
PATH_FILES = resource_path("files")
##################################################################

class UI_License(QDialog, Ui_Dialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.setup()

    def setup(self):

        # Un titre
        self.setWindowTitle("Licenses")

        # Divers
        self.ui_splitter.setStretchFactor(1, 1)
        self.ui_txt_license.setReadOnly(True)

        # Ajout de tous les textes de licence
        self.model_lst_license = QStandardItemModel()
        self.ui_list_license.setModel(self.model_lst_license)
        rootItem = self.model_lst_license.invisibleRootItem()

        # TransfoTron
        lst_f = ["TransfoTron - Design Data"]
        if not "DD" in QCoreApplication.applicationVersion():
            lst_f.append("TransfoTron - Other Modules")

        for f in lst_f:
            path = normpath(join(resource_path("."), f))
            if isfile(path):
                tmp = QStandardItem(f)
                tmp.setData(path, Qt.UserRole)
                rootItem.appendRow(tmp)

        rootItem.appendRow(QStandardItem("=========="))

        # Autres licenses
        if isdir(PATH_FILES):
            for f in listdir(PATH_FILES):
                path = normpath(join(PATH_FILES, f))
                if isfile(path):
                    tmp = QStandardItem(f)
                    tmp.setData(path, Qt.UserRole)
                    rootItem.appendRow(tmp)

        self.ui_list_license.setCurrentIndex(self.model_lst_license.index(0, 0))

        # Connections
        self.ui_list_license.selectionModel().selectionChanged.connect(self.change_license)

    def change_license(self, index):
        """
        Changement de la license à afficher
        """
        self.ui_txt_license.clear()

        if self.ui_list_license.currentIndex().row() < 0:
            return

        if isinstance(index, QItemSelection):
            if len(index.indexes()) > 0:
                index = index.indexes()[0]
            else:
                return

        # Affichage de la license
        item_license = self.model_lst_license.itemFromIndex(index)
        path = item_license.data(Qt.UserRole)
        if path is None:
            return

        f = open(path, "r", encoding="utf-8")
        self.ui_txt_license.setPlainText(f.read())
        f.close()

    def showEvent(self, event):
        """
        A l'affichage
        """
        self.change_license(self.ui_list_license.currentIndex())

        super().showEvent(event)

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
    win = UI_License()

    # 3 - Affichage de la fenêtre
    win.show()
    app.exec()