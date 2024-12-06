# -*- coding: utf-8 -*-
import sys
from os.path import join, dirname, realpath

from PySide6.QtGui import QRegularExpressionValidator, QPixmap, QDoubleValidator, QImage, QPainter
from PySide6.QtCore import Qt, Signal, QRegularExpression, QLocale, QTemporaryFile, QIODevice, QSize
from PySide6.QtWidgets import QVBoxLayout, QGraphicsScene, QFrame, QWidget

from ..utils import gui_utils
from ..utils import gui_geom

from .cable_one_ui import Ui_Form

# =============================================================================
# Fenêtre de définition d'un cable
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

class UI_Cable(QWidget, Ui_Form):

    # Signal quand le widget est modifié par l'utilisateur (non programmatiquement)
    isModified = Signal()

    def __init__(self, ui_main, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.ui_main = ui_main

        self.setup()

    def setup(self):

        # Remplacement du QLineEdit et application d'un format d'affichage
        self.ui_le_strandHeight = gui_utils.QLineEditFormat(self.ui_le_strandHeight.parent()).replaceWidget(self.ui_le_strandHeight)
        self.ui_le_strandHeight.setDisplayFormat("%.2f")
        self.ui_le_strandThick = gui_utils.QLineEditFormat(self.ui_le_strandThick.parent()).replaceWidget(self.ui_le_strandThick)
        self.ui_le_strandThick.setDisplayFormat("%.2f")
        self.ui_le_paperThick = gui_utils.QLineEditFormat(self.ui_le_paperThick.parent()).replaceWidget(self.ui_le_paperThick)
        self.ui_le_paperThick.setDisplayFormat("%.2f")
        self.ui_le_pressboardThick = gui_utils.QLineEditFormat(self.ui_le_pressboardThick.parent()).replaceWidget(self.ui_le_pressboardThick)
        self.ui_le_pressboardThick.setDisplayFormat("%.2f")
        self.ui_le_varnishThick = gui_utils.QLineEditFormat(self.ui_le_varnishThick.parent()).replaceWidget(self.ui_le_varnishThick)
        self.ui_le_varnishThick.setDisplayFormat("%.2f")
        self.ui_le_cableHeight = gui_utils.QLineEditFormat(self.ui_le_cableHeight.parent()).replaceWidget(self.ui_le_cableHeight)
        self.ui_le_cableHeight.setDisplayFormat("%.2f")
        self.ui_le_cableThick = gui_utils.QLineEditFormat(self.ui_le_cableThick.parent()).replaceWidget(self.ui_le_cableThick)
        self.ui_le_cableThick.setDisplayFormat("%.2f")

        self.ui_le_cableHeight.setEnabled(False)
        self.ui_le_cableThick.setEnabled(False)

        # Préparation de la représentation du cable
        layout_qFrame = QVBoxLayout(self.ui_frame_cable)
        self.ui_frame_cable.setLayout(layout_qFrame)
        self.ui_frame_cable.setFrameShape(QFrame.NoFrame)
        self.scene_cable = QGraphicsScene(self.ui_frame_cable)
        self.view_cable = gui_utils.ViewResizeAuto(self.scene_cable)
        layout_qFrame.addWidget(self.view_cable)
        self.cableView = None

        # Initialisation de la comboBox de types
        cable_types = ["CTC Paper", "CTC Netting tape", "Meplat"]
        self.ui_cBox_type.addItems(cable_types)

        # Nombre de brins
        self.ui_spBox_nbreStrands.setMinimum(1)
        self.ui_spBox_nbreStrands.setMaximum(10000)

        # Ajouts de valideurs de champs
        locale = QLocale("en")
        locale.setNumberOptions(QLocale.RejectGroupSeparator)
        validator_float_pos = QDoubleValidator(self) # Float positif
        validator_float_pos.setBottom(0.00001)
        validator_float_pos.setNotation(QDoubleValidator.StandardNotation)
        validator_float_pos.setLocale(locale)
        validator_float_pos0 = QDoubleValidator(self) # Float positif
        validator_float_pos0.setNotation(QDoubleValidator.StandardNotation)
        validator_float_pos0.setLocale(locale)
        validator_str = QRegularExpressionValidator(QRegularExpression("[A-Za-z0-9-_]+"), self)

        # Application des valideurs
        self.ui_le_name.setValidator(validator_str)
        self.ui_le_strandHeight.setValidator(validator_float_pos)
        self.ui_le_strandThick.setValidator(validator_float_pos)
        self.ui_le_varnishThick.setValidator(validator_float_pos0)
        self.ui_le_paperThick.setValidator(validator_float_pos)
        self.ui_le_pressboardThick.setValidator(validator_float_pos0)

        ### Connecteurs
        self.ui_cBox_type.currentIndexChanged.connect(self.chgtTypeCable)
        self.ui_rb_varnish.clicked.connect(self.setToolTips)
        self.ui_rb_paper.clicked.connect(self.setToolTips)
        self.ui_btn_rotateCable.clicked.connect(self.rotateCable)

        # MAJ figure
        self.ui_cBox_type.currentIndexChanged.connect(self.updateCableView)
        self.ui_le_name.editingFinished.connect(self.updateCableView)
        self.ui_spBox_nbreStrands.valueChanged.connect(self.updateCableView)
        self.ui_le_strandHeight.editingFinished.connect(self.updateCableView)
        self.ui_le_strandThick.editingFinished.connect(self.updateCableView)
        self.ui_le_varnishThick.editingFinished.connect(self.updateCableView)
        self.ui_le_paperThick.editingFinished.connect(self.updateCableView)
        self.ui_le_pressboardThick.editingFinished.connect(self.updateCableView)
        self.ui_rb_varnish.clicked.connect(self.updateCableView)
        self.ui_rb_paper.clicked.connect(self.updateCableView)

        self.ui_le_name.textEdited.connect(self.checkDesign)
        self.ui_le_strandHeight.textEdited.connect(self.checkDesign)
        self.ui_le_strandThick.textEdited.connect(self.checkDesign)
        self.ui_le_varnishThick.textEdited.connect(self.checkDesign)
        self.ui_le_paperThick.textEdited.connect(self.checkDesign)
        self.ui_le_pressboardThick.textEdited.connect(self.checkDesign)

        self.ui_main.isFrozen.connect(self.freezeDesign)

        # Au démarrage
        self.chgtTypeCable()
        self.setToolTips()
        self.connectModification()

    def connectModification(self):
        """
        Connection des éléments pour émission du signal isModified
        """
        # Les sous-connections peuvent être activées par l'utilisateur ou programmatiquement
        self.ui_cBox_type.currentIndexChanged.connect(self.emitIsModified)
        self.ui_le_name.editingFinished.connect(self.emitIsModified)
        self.ui_spBox_nbreStrands.valueChanged.connect(self.emitIsModified)
        self.ui_le_strandHeight.editingFinished.connect(self.emitIsModified)
        self.ui_le_strandThick.editingFinished.connect(self.emitIsModified)
        self.ui_le_varnishThick.editingFinished.connect(self.emitIsModified)
        self.ui_le_paperThick.editingFinished.connect(self.emitIsModified)
        self.ui_le_pressboardThick.editingFinished.connect(self.emitIsModified)
        self.ui_rb_varnish.clicked.connect(self.emitIsModified)
        self.ui_rb_paper.clicked.connect(self.emitIsModified)

    def emitIsModified(self):
        self.isModified.emit()

    def disconnectModification(self):
        """
        Déconnection des éléments à l'émission du signal isModified
        """
        self.ui_cBox_type.currentIndexChanged.disconnect(self.emitIsModified)
        self.ui_le_name.editingFinished.disconnect(self.emitIsModified)
        self.ui_spBox_nbreStrands.valueChanged.disconnect(self.emitIsModified)
        self.ui_le_strandHeight.editingFinished.disconnect(self.emitIsModified)
        self.ui_le_strandThick.editingFinished.disconnect(self.emitIsModified)
        self.ui_le_varnishThick.editingFinished.disconnect(self.emitIsModified)
        self.ui_le_paperThick.editingFinished.disconnect(self.emitIsModified)
        self.ui_le_pressboardThick.editingFinished.disconnect(self.emitIsModified)
        self.ui_rb_varnish.clicked.disconnect(self.emitIsModified)
        self.ui_rb_paper.clicked.disconnect(self.emitIsModified)

    def checkDesign(self):
        """
        Vérification du design
        """
        # Liste d'erreurs à corriger
        lst_error = []

        tmp = self.ui_le_name
        if not tmp.hasAcceptableInput():
            tmp.setStyleSheet("background-color: red;")
            lst_error.append("Cable name must only have A-Z or a-z or 0-9 or - or _ characters")
        else:
            tmp.setStyleSheet("")
        tmp = self.ui_le_strandHeight
        if not tmp.hasAcceptableInput():
            tmp.setStyleSheet("background-color: red;")
            lst_error.append("Strand length value must be strictly positive")
        else:
            tmp.setStyleSheet("")
        tmp = self.ui_le_strandThick
        if not tmp.hasAcceptableInput():
            tmp.setStyleSheet("background-color: red;")
            lst_error.append("Strand width value must be strictly positive")
        else:
            tmp.setStyleSheet("")
        tmp = self.ui_le_varnishThick
        if not tmp.hasAcceptableInput():
            tmp.setStyleSheet("background-color: red;")
            lst_error.append("Strand insulation thickness value must be positive")
        else:
            tmp.setStyleSheet("")
        tmp = self.ui_le_paperThick
        if not tmp.hasAcceptableInput():
            tmp.setStyleSheet("background-color: red;")
            lst_error.append("Paper covering thickness value must be strictly positive")
        else:
            tmp.setStyleSheet("")
        tmp = self.ui_le_pressboardThick
        if not tmp.hasAcceptableInput():
            tmp.setStyleSheet("background-color: red;")
            lst_error.append("Cable pressboard thinckness value must be positive")
        else:
            tmp.setStyleSheet("")

        # Vérification que les cables CTC ont un nombre impair de brins
        if "CTC" in self.ui_cBox_type.currentText():
            if self.ui_spBox_nbreStrands.value()%2 == 0:
                self.ui_spBox_nbreStrands.setStyleSheet("background-color: red;")
                lst_error.append("CTC cable must have an odd number of strands")
            else:
                self.ui_spBox_nbreStrands.setStyleSheet("")
        else:
            self.ui_spBox_nbreStrands.setStyleSheet("")

        if len(lst_error) > 0:
            self.cableView = None
            self.scene_cable.clear()

        return lst_error

    def freezeDesign(self, isFrozen):
        """
        Action lors du (dé)gelage du design
        """
        self.ui_cBox_type.setEnabled(not isFrozen)
        self.ui_le_name.setEnabled(not isFrozen)
        self.ui_spBox_nbreStrands.setEnabled(not isFrozen)
        self.ui_le_strandHeight.setEnabled(not isFrozen)
        self.ui_le_strandThick.setEnabled(not isFrozen)
        self.ui_le_varnishThick.setEnabled(not isFrozen)
        self.ui_le_paperThick.setEnabled(not isFrozen)
        self.ui_le_pressboardThick.setEnabled(not isFrozen)
        self.ui_rb_varnish.setEnabled(not isFrozen)
        self.ui_rb_paper.setEnabled(not isFrozen)

        # Activations en fonction du type de cable
        if not isFrozen: self.chgtTypeCable()

    def chgtTypeCable(self):
        """
        Actions lors du changement de type de cable
        """

        if self.ui_cBox_type.currentText() == "CTC Paper":
            # L'isolation des brins est forcément en vernis pour les CTC
            self.ui_rb_varnish.setChecked(True)
            self.ui_rb_paper.setEnabled(False)
            self.ui_le_pressboardThick.setEnabled(True)
            self.ui_lbl_covering.setText("Paper covering thickness (tc)")

            image = QPixmap(join(PATHRC, "schema_CTC.PNG"))
            image = image.scaledToHeight(225, Qt.SmoothTransformation)

        elif self.ui_cBox_type.currentText() == "CTC Netting tape":
            # L'isolation des brins est forcément en vernis pour les CTC
            self.ui_rb_varnish.setChecked(True)
            self.ui_rb_paper.setEnabled(False)
            self.ui_le_pressboardThick.setEnabled(True)
            self.ui_lbl_covering.setText("Polyester net covering thickness (tc)")

            image = QPixmap(join(PATHRC, "schema_CTC_netting_tape.PNG"))
            image = image.scaledToHeight(225, Qt.SmoothTransformation)

        elif self.ui_cBox_type.currentText() == "Meplat":
            self.ui_rb_paper.setEnabled(True)
            self.ui_lbl_covering.setText("Paper covering thickness (tc)")
            # Pas de pressboard en meplat
            self.ui_le_pressboardThick.setText(0.0)
            self.ui_le_pressboardThick.setEnabled(False)

            image = QPixmap(join(PATHRC, "schema_meplat.PNG"))
            image = image.scaledToWidth(300, Qt.SmoothTransformation)

        else:
            raise Exception("Type de cable inconnu")

        # Insertion de l'image du cable
        self.ui_lbl_cableScheme.setPixmap(image)

        # Adaptation des tool tips
        self.setToolTips()

    def setToolTips(self):
        """
        Fonction de définition des toolTips sur les objets
        """

        self.ui_spBox_nbreStrands.setToolTip("Typically [1-100]")
        self.ui_le_strandHeight.setToolTip("Typically [3.2-12.5] mm")
        self.ui_le_strandThick.setToolTip("Typically [1.3-3.0] mm")
        self.ui_le_pressboardThick.setToolTip("Typically [0-0.105] mm")

        if self.ui_rb_varnish.isChecked():
            self.ui_le_varnishThick.setToolTip("Double side, typically [0.12-0.17] mm")
        else:
            self.ui_le_varnishThick.setToolTip("Double side, typically [0.15-0.30] mm")

        if self.ui_cBox_type.currentText() == "CTC Netting tape":
            self.ui_le_paperThick.setToolTip("Double side, typically 0.56 mm")
        else:
            self.ui_le_paperThick.setToolTip("Double side, typically [0.3-1.25] mm")

    def getCableProperties(self):
        """
        Récupération des propriétés du cable à partir des champs dans un dictionnaire
        """

        prop = {}
        prop["name"] = self.ui_le_name.text()
        prop["type"] = self.ui_cBox_type.currentText()
        prop["N_strands"] = self.ui_spBox_nbreStrands.value()
        try:
            prop["h_strand"] = float(self.ui_le_strandHeight.text())
            prop["t_strand"] = float(self.ui_le_strandThick.text())
        except:
            return {}
        if self.ui_rb_varnish.isChecked():
            prop["type_strandInsulation"] = "varnish"
        else:
            prop["type_strandInsulation"] = "paper"

        # Pressboard uniquement en CTC
        if "CTC" in prop["type"]:
            prop["t_pressboard"] = float(self.ui_le_pressboardThick.text())
        else:
            prop["t_pressboard"] = 0.0

        # Isolation extérieure du cable
        if prop["type"] == "CTC Paper" or prop["type"] == "Meplat":
            prop["type_cableInsulation"] = "paper"
        elif prop["type"] == "CTC Netting tape":
            prop["type_cableInsulation"] = "polyester"
        else:
            raise Exception("Type de cable inconnu")
        prop["t_cableInsulation"] = float(self.ui_le_paperThick.text())

        # Calcul des dimensions du cable à partir de l'epaisseur de vernis
        prop["t_strandInsulation"] = float(self.ui_le_varnishThick.text())

        if prop["type"] == "CTC Paper":
            prop["t_cable"] = 2*(prop["h_strand"] + prop["t_strandInsulation"]) + prop["t_pressboard"] + prop["t_cableInsulation"]
            prop["h_cable"] = (int((prop["N_strands"]-1)/2)+1)*(prop["t_strand"]+prop["t_strandInsulation"]) + prop["t_cableInsulation"]
        elif prop["type"] == "CTC Netting tape":
            prop["t_cable"] = 2*(prop["h_strand"] + prop["t_strandInsulation"]) + prop["t_pressboard"] + prop["t_cableInsulation"]
            prop["h_cable"] = (int((prop["N_strands"]-1)/2)+1)*(prop["t_strand"]+prop["t_strandInsulation"]) + prop["t_cableInsulation"]
        elif prop["type"] == "Meplat":
            prop["t_cable"] = prop["h_strand"] + prop["t_strandInsulation"] + prop["t_cableInsulation"]
            prop["h_cable"] = prop["N_strands"]*(prop["t_strand"]+prop["t_strandInsulation"]) + prop["t_cableInsulation"]
        else:
            raise Exception("Type de cable inconnu")

        # Quelques vérifications pour n'envoyer que des "bons" cables
        if "CTC" in self.ui_cBox_type.currentText():
            if self.ui_spBox_nbreStrands.value()%2 == 0:
                # Cable CTC mal défini
                return {}
        if prop["h_cable"] <= 0.0 and prop["t_cable"] <= 0.0:
            return {}

        return prop

    def updateCableView(self):
        """
        Mise à jour de la vue du cable avec les propriétés indiquées
        """

        # Vérification des champs
        if len(self.checkDesign()) > 0:
            return

        # Récupération des propriétés
        prop = self.getCableProperties()
        if prop == {}:
            return

        # MAJ des dimensions du cable
        self.ui_le_cableHeight.setText(prop["h_cable"])
        self.ui_le_cableThick.setText(prop["t_cable"])

        # MAJ du graphic
        if self.cableView == None:
            cable = gui_geom.Cable()
            cable.setPropCable(prop)
            cable.rotateCenter(90.0) # Horizontal par défaut
            cable.setZValue(0)
            cable.setDrawingMode("detailled")
            self.scene_cable.addItem(cable)
            self.cableView = cable
        else:
            self.cableView.setPropCable(prop)

        # Application de la taille de la scène pour la vue
        self.scene_cable.setSceneRect(self.cableView.boundingRect())
        # Mise à jour de la vue
        self.view_cable.fitInView(self.scene_cable.sceneRect(), Qt.KeepAspectRatio)

    def rotateCable(self):
        if self.cableView == None:
            return

        self.cableView.rotateCenter(90.0)
        # Mise à jour de la vue
        self.scene_cable.setSceneRect(self.cableView.boundingRect())
        self.view_cable.fitInView(self.scene_cable.sceneRect(), Qt.KeepAspectRatio)

    def addXMLTree(self, tag_cables, docDom):
        """
        Generation de l'arbre XML
        """

        cable_prop = self.getCableProperties()
        if cable_prop == {}:
            return

        tag_cn = docDom.createElement("cable")
        tag_cables.appendChild(tag_cn)

        tag_tmp = docDom.createElement('name')
        tag_tmp.appendChild(docDom.createTextNode(cable_prop["name"]))
        tag_cn.appendChild(tag_tmp)
        tag_tmp = docDom.createElement('type')
        tag_tmp.appendChild(docDom.createTextNode(cable_prop["type"]))
        tag_cn.appendChild(tag_tmp)
        tag_tmp = docDom.createElement('cable')
        tag_tmp.setAttribute("insulation", cable_prop["type_cableInsulation"])
        tag_tmp.setAttribute("t_insulation_m", "%e"%(cable_prop["t_cableInsulation"]*1e-3))
        tag_tmp.setAttribute("t_cable_m", "%e"%(cable_prop["t_cable"]*1e-3))
        tag_tmp.setAttribute("h_cable_m", "%e"%(cable_prop["h_cable"]*1e-3))
        tag_cn.appendChild(tag_tmp)
        tag_tmp = docDom.createElement('strands')
        tag_tmp.setAttribute("N_strands", "%i"%(cable_prop["N_strands"]))
        tag_tmp.setAttribute("h_strand_m", "%e"%(cable_prop["h_strand"]*1e-3))
        tag_tmp.setAttribute("t_strand_m", "%e"%(cable_prop["t_strand"]*1e-3))
        tag_tmp.setAttribute("t_insulation_m", "%e"%(cable_prop["t_strandInsulation"]*1e-3))
        tag_tmp.setAttribute("insulation", cable_prop["type_strandInsulation"])
        tag_cn.appendChild(tag_tmp)
        tag_tmp = docDom.createElement('pressboard')
        tag_tmp.setAttribute("t_pressboard_m", "%e"%(cable_prop["t_pressboard"]*1e-3))
        tag_cn.appendChild(tag_tmp)

    def addPDF(self, pdf, part, lst_id_calcul=[]):
        """
        Remplissage du fichier PDF
        """
        pdf.set_font()

        if "data_detail" in part:
            cable_prop = self.getCableProperties()
            if cable_prop == {}:
                return

            pdf.ln()
            pdf.toc_entry("Cable %s"%cable_prop["name"], 3)

            ### Infos
            pdf.multi_cell(txt="Type: %s"%cable_prop["type"])

            pdf.ln()
            pdf.set_font(style="IU")
            pdf.multi_cell(txt="> Cable data:")
            pdf.set_font()
            pdf.multi_cell(txt=" "*8 + "Insulation material: %s"%cable_prop["type_cableInsulation"])
            pdf.multi_cell(txt=" "*8 + "Double-side insulation thickness: %.2f mm"%cable_prop["t_cableInsulation"])
            pdf.multi_cell(txt=" "*8 + "Width: %.2f mm"%cable_prop["t_cable"])
            pdf.multi_cell(txt=" "*8 + "Length: %.2f mm"%cable_prop["h_cable"])

            pdf.ln()
            pdf.set_font(style="IU")
            pdf.multi_cell(txt="> Strands data:")
            pdf.set_font()
            pdf.multi_cell(txt=" "*8 + "Number of strands: %i"%cable_prop["N_strands"])
            pdf.multi_cell(txt=" "*8 + "Insulation material: %s"%cable_prop["type_strandInsulation"])
            pdf.multi_cell(txt=" "*8 + "Double-side insulation thickness: %.2f mm"%cable_prop["t_strandInsulation"])
            pdf.multi_cell(txt=" "*8 + "Width: %.2f mm"%cable_prop["t_strand"])
            pdf.multi_cell(txt=" "*8 + "Length: %.2f mm"%cable_prop["h_strand"])

            if cable_prop["t_pressboard"] > 0:
                pdf.ln()
                pdf.set_font(style="IU")
                pdf.multi_cell(txt="> Pressboard data:")
                pdf.set_font()
                pdf.multi_cell(txt=" "*8 + "Thickness: %.2f mm"%cable_prop["t_pressboard"])

            ### Image
            # On récupère l'image
            rectItems = self.scene_cable.itemsBoundingRect()
            scale = min(pdf.max_width_px/rectItems.toRect().width(), pdf.max_heigth_px/rectItems.toRect().height())
            targetSize = QSize(rectItems.toRect().width()*scale, rectItems.toRect().height()*scale)

            pixMap = QImage(targetSize, QImage.Format_ARGB32_Premultiplied)
            pixMap.fill(Qt.white)
            painter = QPainter(self)
            painter.begin(pixMap)
            painter.setRenderHint(QPainter.Antialiasing, True)
            self.scene_cable.render(painter, source=rectItems)
            painter.end()

            file = QTemporaryFile(self)
            file.open(QIODevice.WriteOnly)
            pixMap.save(file, "PNG")
            file.close()

            # Taille de l'image
            pdf.ln()
            w_items = pdf.pixelToMm(targetSize.width())
            h_items = pdf.pixelToMm(targetSize.height())
            scale = min(1, 100/w_items, 25/h_items)
            pdf.image(file.fileName(), fmt="png", w=w_items*scale, align="C")

    def loadXMLTree(self, e_cable):
        """
        Chargement de l'arbre XML
        """

        if e_cable.isNull():
            return

        self.disconnectModification()

        e_cable_cable = e_cable.firstChildElement("cable")
        e_cable_strands = e_cable.firstChildElement("strands")
        e_cable_pressboard = e_cable.firstChildElement("pressboard")

        self.ui_le_name.setText(e_cable.firstChildElement("name").text())
        self.ui_cBox_type.setCurrentText(e_cable.firstChildElement("type").text())
        self.ui_spBox_nbreStrands.setValue(int(e_cable_strands.attribute("N_strands")))
        self.ui_le_strandHeight.setText(float(e_cable_strands.attribute("h_strand_m"))*1e3)
        self.ui_le_strandThick.setText(float(e_cable_strands.attribute("t_strand_m"))*1e3)
        self.ui_le_varnishThick.setText(float(e_cable_strands.attribute("t_insulation_m"))*1e3)
        self.ui_le_paperThick.setText(float(e_cable_cable.attribute("t_insulation_m"))*1e3)
        self.ui_le_pressboardThick.setText(float(e_cable_pressboard.attribute("t_pressboard_m"))*1e3)

        if e_cable_strands.attribute("insulation") == "varnish":
            self.ui_rb_varnish.setChecked(True)
            self.ui_rb_paper.setChecked(False)
        else:
            self.ui_rb_varnish.setChecked(False)
            self.ui_rb_paper.setChecked(True)

        # Pour différentes choses...
        self.chgtTypeCable()
        self.setToolTips()
        self.updateCableView()

        self.connectModification()

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
    win = UI_Cable()

    # 3 - Affichage de la fenêtre
    win.show()
    app.exec()