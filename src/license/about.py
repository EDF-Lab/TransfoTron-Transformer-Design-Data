# -*- coding: utf-8 -*-
import sys

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QApplication, QDialog

from .about_ui import Ui_Dialog

# =============================================================================
# Popup About
# =============================================================================

class UI_About(QDialog, Ui_Dialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.setup()

    def setup(self):

        # Un titre
        self.setWindowTitle("About transfoTron")

        # Divers
        self.ui_lbl_version.setText("Version %s"%QCoreApplication.applicationVersion())
        self.ui_lbl_copyright.setText("Copyright EDF 2019-2024")
        self.ui_lbl_assistance.setOpenExternalLinks(True)

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
    win = UI_About()

    # 3 - Affichage de la fenêtre
    win.show()
    app.exec()