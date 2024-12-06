# -*- coding: utf-8 -*-
import sys
from os.path import join, dirname, realpath

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog

from .designCheck_ui import Ui_Dialog

# =============================================================================
# Dialog de lancement d'un calcul
# =============================================================================

class UI_DesignCheck(QDialog, Ui_Dialog):

    def __init__(self, lst_error, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.lst_error = lst_error

        self.setup()

    def setup(self):

        # Un titre
        self.setWindowTitle("Design check")

        # Fenetre non modale
        self.setModal(False)

        # Suppression du bouton "?" dans la barre de titre
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        # Remplissage du txt
        self.ui_txt_errors.setReadOnly(True)
        self.ui_txt_errors.setPlainText("\n".join(self.lst_error))

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
    win = UI_DesignCheck(['a', 'b'])

    # 3 - Affichage de la fenêtre
    win.show()
    app.exec()