# -*- coding: utf-8 -*-
import sys
from os.path import join, dirname, realpath
from win32com.client import Dispatch
from traceback import format_exception
from datetime import datetime

from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtWidgets import QApplication, QDialog

from .error_ui import Ui_Dialog

# =============================================================================
# Dialog pour l'affichage des erreurs dans une fenêtre
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
##################################################################

class UI_Error(QDialog, Ui_Dialog):

    def __init__(self, ui_main, parent=None):
        """
        Initialization d'abord partir du layout (*.ui), et ensuite
        par l'appel à une méthode propre à la classe (setup)
        """
        ################## NE PAS MODIFIER !!! #####################
        super().__init__(parent)
        self.setupUi(self)
        ############################################################
        self.ui_main = ui_main

        self.setup()

    def setup(self):
        # Titre
        self.setWindowTitle("TransfoTron error")
        self.ui_lbl_title.setStyleSheet("QLabel { font-weight: bold; font-size: 15pt} ")
        image = QPixmap(resource_path("messagebox_critical-256.png")).scaledToHeight(40, Qt.SmoothTransformation)
        self.ui_lbl_image.setPixmap(image)

        # Suppression du bouton "?" dans la barre de titre
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        # Message d'erreur
        self.ui_txt_msg.setReadOnly(True)

        # Connection
        self.ui_btn_copy.clicked.connect(self.copyToClipboard)
        self.ui_btn_mail.clicked.connect(self.generateMail)
        self.ui_btn_close.clicked.connect(self.close)
        self.ui_btn_exit.clicked.connect(QApplication.closeAllWindows)

    def copyToClipboard(self):
        """
        Copie le texte de l'erreur dans le presse papier
        """
        self.ui_txt_msg.selectAll()
        self.ui_txt_msg.copy()

    def generateMail(self):
        """
        Generation d'un mail avec le texte de l'erreur
        """
        try:
            outlook = Dispatch('outlook.application')
        except:
            # Il n'y a pas Outlook, on ne fait rien
            self.ui_btn_mail.setEnabled(False)
            return

        mail = outlook.CreateItem(0)
        mail.To = 'remi.desquiens@edf.fr'
        mail.Subject = '[TransfoTron] Error message'

        txt = "Please add some information about how the bug came out" + "\n"
        txt = txt + "You can attach a file if necessary (screenshot, ttx file, ...)" + "\n"
        txt = txt + "Thank you for helping us!" + "\n"
        txt = txt + "(Le support est aussi assuré en Français !)" + "\n"
        txt = txt + "\n"
        txt = txt + "\n"
        txt = txt + "================================================================" + "\n"
        txt = txt + self.ui_txt_msg.toPlainText()
        txt = txt + "================================================================" + "\n"
        txt = txt + "\n"

        mail.Body = txt

        # On ajoute le dernier TTX en PJ s'il est disponible
        if self.ui_main.curFilePath is not None:
            try:
                mail.Attachments.Add(self.ui_main.curFilePath)
            except:
                pass

        # Show Outlook mail (fenetre non modale)
        mail.Display(False)

    def writeError(self, exctype, value, tb):
        all_exception_lines = "Error generated on " + str(datetime.now().isoformat()) + "\n"
        all_exception_lines += "%s - %s\n"%(QCoreApplication.applicationName(), QCoreApplication.applicationVersion())
        all_exception_lines += "Current File Path: %s\n\n"%self.ui_main.curFilePath

        all_exception_lines += "".join(format_exception(exctype, value, tb))

        self.ui_txt_msg.setPlainText(all_exception_lines)

if __name__ == "__main__":
    """
    Point d'entrée à l'exécution du script app.py
    """

    # Modification de la gestion des erreurs
    def my_exception_hook(exctype, value, tb):
        win = UI_Error()
        win.writeError(exctype, value, tb)
        win.exec()
    sys.excepthook = my_exception_hook

    # 1 - Creation de l'application Qt
    app = QApplication(sys.argv)

    # 2 - Initialization de la fenêtre principale sur la base
    #     de la classe Example qui s'initialize à partir de la
    #     vue dans le fichier layout.ui (créé avec qtdesigner)
    win = UI_Error()

    # 3 - Affichage de la fenêtre
    win.show()
    app.exec()

