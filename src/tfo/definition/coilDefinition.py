# -*- coding: utf-8 -*-
import sys
from os.path import join, dirname, realpath

from PySide6.QtGui import QDoubleValidator, QPen, QImage, QPainter, QColor
from PySide6.QtCore import Qt, Signal, QLocale, QIODevice, QTemporaryFile, QSize, QRectF
from PySide6.QtWidgets import QVBoxLayout, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QFrame, QMessageBox, QWidget

from ..utils import gui_utils
from ..utils import gui_geom

from .coilDefinition_ui import Ui_Form

# =============================================================================
# Widget de définition géométrique des bobines
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

class UI_CoilDefinition(QWidget, Ui_Form):

    # Signal quand le widget est modifié par l'utilisateur (non programmatiquement)
    isModified = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.setup()

    def setup(self):

        # Remplacement du QLineEdit et application d'un format d'affichage
        self.ui_le_radSpacerWidth = gui_utils.QLineEditFormat(self.ui_le_radSpacerWidth.parent()).replaceWidget(self.ui_le_radSpacerWidth)
        self.ui_le_radSpacerWidth.setDisplayFormat("%.2f")
        self.ui_le_innerRadius = gui_utils.QLineEditFormat(self.ui_le_innerRadius.parent()).replaceWidget(self.ui_le_innerRadius)
        self.ui_le_innerRadius.setDisplayFormat("%.2f")
        self.ui_le_coilHeight = gui_utils.QLineEditFormat(self.ui_le_coilHeight.parent()).replaceWidget(self.ui_le_coilHeight)
        self.ui_le_coilHeight.setDisplayFormat("%.2f")
        self.ui_le_coilWidth = gui_utils.QLineEditFormat(self.ui_le_coilWidth.parent()).replaceWidget(self.ui_le_coilWidth)
        self.ui_le_coilWidth.setDisplayFormat("%.2f")

        # Passage en gras de certains titres
        self.ui_gBox_coilGeom.setStyleSheet("QGroupBox { font-weight: bold; } ")
        self.ui_gBox_view.setStyleSheet("QGroupBox { font-weight: bold; } ")

        # Initialisation
        self.ui_chk_discs.setChecked(True)
        self.ui_chk_ducts.setChecked(True)
        self.ui_chk_pressboards.setChecked(True)
        self.ui_le_innerRadius.setText("1.0")
        self.ui_spBox_nbre_radSpacers.setMinimum(1)
        self.ui_spBox_nbre_radSpacers.setMaximum(10000)
        self.ui_le_radSpacerWidth.setText("1.0")
        self.ui_spBox_nbreDiscs.setMinimum(1)
        self.ui_spBox_nbreDiscs.setMaximum(10000)

        # Ajouts de valideurs de champs
        locale = QLocale("en")
        locale.setNumberOptions(QLocale.RejectGroupSeparator)
        validator_float_pos = QDoubleValidator(self) # Float positif
        validator_float_pos.setBottom(0.00001)
        validator_float_pos.setNotation(QDoubleValidator.StandardNotation)
        validator_float_pos.setLocale(locale)

        # Application des valideurs
        self.ui_le_radSpacerWidth.setValidator(validator_float_pos)
        self.ui_le_innerRadius.setValidator(validator_float_pos)

        # Champs désactivés
        self.ui_le_coilHeight.setEnabled(False)
        self.ui_le_coilWidth.setEnabled(False)

        ### Scene de représentation de la bobine
        self.scene_coil = QGraphicsScene(self)
        # Vue zoomée
        layout_qFrame = QVBoxLayout(self.ui_frame_viewZoom)
        self.ui_frame_viewZoom.setLayout(layout_qFrame)
        self.ui_frame_viewZoom.setFrameShape(QFrame.NoFrame)
        self.view_zoom = gui_utils.ViewZoomable(self.scene_coil)
        layout_qFrame.addWidget(self.view_zoom)

        # Vue entière
        layout_qFrame = QVBoxLayout(self.ui_frame_viewAll)
        self.ui_frame_viewAll.setLayout(layout_qFrame)
        self.ui_frame_viewAll.setFrameShape(QFrame.NoFrame)
        self.view_all = gui_utils.ViewNonClickable(self.scene_coil)
        layout_qFrame.addWidget(self.view_all)

        self.view_all.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view_all.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        ### Légende
        layout_qFrame = QVBoxLayout(self.ui_frame_legend)
        self.ui_frame_legend.setLayout(layout_qFrame)
        self.ui_frame_legend.setFrameShape(QFrame.NoFrame)
        self.scene_lgd = QGraphicsScene(self.ui_frame_legend)
        self.view_lgd = QGraphicsView(self.scene_lgd)
        layout_qFrame.addWidget(self.view_lgd)

        self.view_lgd.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view_lgd.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        ### Divers
        # Pour les résultats de calculs
        self.dict_thermalDiag = {} # key=id_calcul ; data={dict TR}

        # Rectangle de vue zoomée
        self.activeViewRect = None
        self.pen = QPen(Qt.black, 8.0, Qt.DashDotLine)

        # Bobine
        self.coil = gui_geom.Coil(self.scene_coil, self.scene_lgd, self)

        # Beauté
        self.ui_splitter_A.setSizes([250, 1300])
        self.ui_splitter_B.setSizes([360, 950])
        self.ui_splitter_C.setSizes([400, 200])

        ### Connecteurs
        self.ui_splitter_A.splitterMoved.connect(self.updateGraphicsSize)
        self.ui_splitter_B.splitterMoved.connect(self.updateGraphicsSize)
        self.ui_splitter_C.splitterMoved.connect(self.updateGraphicsSize)
        self.coil.coilUpdated.connect(self.updateGraphicsSize)
        self.coil.isModified.connect(self.emitIsModified)
        self.view_zoom.viewUpdated.connect(self.updateActiveViewRect)
        self.ui_spBox_nbreDiscs.valueChanged.connect(self.coil.setDiscNumber)

        ### Au démarrage
        self.updateActiveViewRect()
        self.connectModification()

    def connectModification(self):
        """
        Connection des éléments pour émission du signal isModified
        """
        # Les sous-connections peuvent être activées par l'utilisateur ou programmatiquement
        self.coil.isModified.connect(self.emitIsModified)
        self.ui_spBox_nbre_radSpacers.valueChanged.connect(self.emitIsModified)
        self.ui_le_radSpacerWidth.textEdited.connect(self.emitIsModified)
        self.ui_le_innerRadius.textEdited.connect(self.emitIsModified)
        self.ui_spBox_nbreDiscs.valueChanged.connect(self.emitIsModified)

    def emitIsModified(self):
        self.isModified.emit()

    def disconnectModification(self):
        """
        Déconnection des éléments à l'émission du signal isModified
        """
        self.coil.isModified.disconnect(self.emitIsModified)
        self.ui_spBox_nbre_radSpacers.valueChanged.disconnect(self.emitIsModified)
        self.ui_le_radSpacerWidth.textEdited.disconnect(self.emitIsModified)
        self.ui_le_innerRadius.textEdited.disconnect(self.emitIsModified)
        self.ui_spBox_nbreDiscs.valueChanged.disconnect(self.emitIsModified)

    def checkDesign(self):
        """
        Vérification du design
        """
        # Liste d'erreurs à corriger
        lst_error = []

        tmp = self.ui_le_radSpacerWidth
        if not tmp.hasAcceptableInput():
            tmp.setStyleSheet("background-color: red;")
            lst_error.append("Radial spacer width value must be strictly positive")
        else:
            tmp.setStyleSheet("")
        tmp = self.ui_le_innerRadius
        if not tmp.hasAcceptableInput():
            tmp.setStyleSheet("background-color: red;")
            lst_error.append("Winding inner radius value must be strictly positive")
        else:
            tmp.setStyleSheet("")

        # La coil est bonne par construction (normalement...)

        return lst_error

    def freezeDesign(self, isFrozen):
        """
        Action lors du (dé)gelage du design
        """
        self.coil.freezeDesign(isFrozen)
        self.ui_spBox_nbre_radSpacers.setEnabled(not isFrozen)
        self.ui_le_radSpacerWidth.setEnabled(not isFrozen)
        self.ui_spBox_nbreDiscs.setEnabled(not isFrozen)
        self.ui_le_innerRadius.setEnabled(not isFrozen)

    def getInnerRadius(self):
        """
        Renvoi le rayon intérieur de la bobine en mm
        """
        return float(self.ui_le_innerRadius.text())

    def setThermalDiagram(self, id_calcul, dict_thermalDiag):
        """
        Définition du diagramme thermique résultats
        """
        self.dict_thermalDiag[id_calcul] = dict_thermalDiag

    def removeLoadedCalcul(self, id_calcul=None):
        """
        Retrait d'un calcul des calculs chargés
        """
        if id_calcul == None:
            # On supprime tout
            self.dict_thermalDiag = {}
            return

        # Suppression du diagramme thermique
        if id_calcul in self.dict_thermalDiag.keys():
            del self.dict_thermalDiag[id_calcul]

    def updateActiveViewRect(self):
        """
        Fonction d'affichage sur la vue non zoomée du rectangle correspondant à la vue zoomée
        """

        # Adaptation de la taille du crayon à la taille de la bobine
        self.pen.setWidthF(min(8.0, self.scene_coil.sceneRect().height()/75.0))
        penWidth = self.pen.widthF()

        # Rectangle zoom (ajusté pour ne pas le voir sur la vue zoomée)
        rect = self.view_zoom.mapToScene(self.view_zoom.viewport().geometry()).boundingRect()
        rect.adjust(-penWidth, -penWidth, penWidth, penWidth)

        # Modification de l'ancien rectangle
        if self.activeViewRect == None:
            self.activeViewRect = QGraphicsRectItem(rect)
            self.activeViewRect.setZValue(100)
            self.scene_coil.addItem(self.activeViewRect)
        else:
            self.activeViewRect.prepareGeometryChange()
            self.activeViewRect.setRect(rect)
        self.activeViewRect.setPen(self.pen)

    def updateGraphicsSize(self):
        """
        MAJ des tailles des graphiques
        """
        self.view_all.fitInView(self.scene_coil.sceneRect(), Qt.KeepAspectRatio)
        self.view_lgd.fitInView(self.scene_lgd.sceneRect(), Qt.KeepAspectRatio)

    def resizeEvent(self, event):
        """
        Permet le redimensionnement lors de la modification de la taille de la fenêtre
        Surcharge
        """
        self.updateGraphicsSize()
        super().resizeEvent(event)

    def showEvent(self, event):
        """
        Pour que la figure soit mise à jour lors du changement de TreeCase dans la MainWindow
        Surcharge
        """
        # MAJ des infos de la coil
        self.coil.updateDiscCalculation()
        self.coil.setDiscNumber(self.ui_spBox_nbreDiscs.value())

        # S'il n'y a pas de disques définis pour la coil, on bloque tout
        if len(self.coil.lst_ui_disc) == 0:
            QMessageBox.critical(self, "TransfoTron",
                                           "You must define discs for this coil before.")
            self.setEnabled(False)
        else:
            if self.coil.lst_ui_disc[0].getDisc() == {}:
                QMessageBox.critical(self, "TransfoTron",
                                           "You must define discs for this coil before.")
                self.setEnabled(False)
            else:
                self.setEnabled(True)

        self.updateGraphicsSize()
        super().showEvent(event)

    def addXMLTree(self, tag_coil, docDom):
        """
        Generation de l'arbre XML
        """
        # MAJ des infos de la coil
        self.coil.updateDiscCalculation()
        self.coil.setDiscNumber(self.ui_spBox_nbreDiscs.value())

        tag_tmp = docDom.createElement('r_inner_m')
        tag_tmp.appendChild(docDom.createTextNode("%f"%(self.getInnerRadius()*1e-3)))
        tag_coil.appendChild(tag_tmp)

        tag_rs = docDom.createElement('radial_spacers')
        tag_coil.appendChild(tag_rs)
        tag_tmp = docDom.createElement('N_spacers')
        tag_tmp.appendChild(docDom.createTextNode("%i"%(self.ui_spBox_nbre_radSpacers.value())))
        tag_rs.appendChild(tag_tmp)
        tag_tmp = docDom.createElement('w_spacer_m')
        tag_tmp.appendChild(docDom.createTextNode("%f"%(float(self.ui_le_radSpacerWidth.text())*1e-3)))
        tag_rs.appendChild(tag_tmp)

        self.coil.addXMLTreeDesign(tag_coil, docDom)

    def addPDF(self, pdf, part, lst_id_calcul=[]):
        """
        Remplissage du fichier PDF
        """
        pdf.set_font()

        if "data_detail" in part:

            # Si la géométrie n'est pas définie, on passe
            if len(self.coil.lst_center) == 0:
                pdf.multi_cell(txt=" "*8 + "Geometry not defined")
                return

            ### Quelques infos
            pdf.multi_cell(txt=" "*8 + "Coil height: %s mm"%self.ui_le_coilHeight.text())
            pdf.multi_cell(txt=" "*8 + "Coil width: %s mm"%self.ui_le_coilWidth.text())
            pdf.multi_cell(txt=" "*8 + "Inner radius: %.1f mm"%self.getInnerRadius())
            pdf.multi_cell(txt=" "*8 + "Number of radial spacers: %i"%self.ui_spBox_nbre_radSpacers.value())
            pdf.multi_cell(txt=" "*8 + "Width radial spacer: %s mm"%self.ui_le_radSpacerWidth.text())
            for d in self.coil.lst_ui_disc:
                d.addPDF(pdf, part, lst_id_calcul)
            pdf.multi_cell(txt=" "*8 + "Total number of discs: %i"%self.ui_spBox_nbreDiscs.value())

            # Récupération du dico_lgd qui contient plein de choses + légende
            dico_lgd = self.coil.legend.dico_lgd
            for k in sorted(dico_lgd.keys()):
                tmp = k.replace("Disc", "discs").replace("Duct", "ducts").replace("Oil guide", "oil guides").replace("Pressboard", "pressboards")
                color = QColor(dico_lgd[k][1])
                pdf.set_fill_color(color.red(), color.green(), color.blue())
                pdf.cell(9)
                pdf.cell(10, h=pdf.font_size + 1, fill=True, border=1)
                pdf.cell(0, txt=" Number of %s: %i"%(tmp, dico_lgd[k][0]), ln=1, h=pdf.font_size + 1)
            pdf.ln()

            ### Image de la coil
            # Changement de page si on est déjà au bout (sinon bug) -- 1 et non 0 car on prend des parties entières...
            if pdf.page_break_trigger - pdf.get_y() - pdf.font_size < 1:
                pdf.add_page()

            # On vire le rect view
            if self.activeViewRect is not None:
                self.scene_coil.removeItem(self.activeViewRect)
                self.activeViewRect = None

            # On déselectionne tout
            self.scene_coil.clearSelection()

            ### Récupération de l'image avec gestion des sauts de page
            rectItems = self.scene_coil.itemsBoundingRect()

            # Largeur max de la coil sur le pdf en mm
            w_coil_pdf = 50.0
            # Largeur de la coil sur la scene QT en mm
            w_coil_scene = rectItems.width()
            # Echelle de passage sur la largeur
            w_scale = w_coil_pdf/w_coil_scene

            # Placement sur 2 colonnes
            lst_x_col = [pdf.w/3 - w_coil_pdf/2, 2*pdf.w/3 - w_coil_pdf/2]
            y_col = pdf.get_y()
            col = 0

            h_printed_pdf = 0.0
            while rectItems.height() - h_printed_pdf > 1:

                if col == 0:
                    y_col = pdf.get_y()
                else:
                    pdf.set_y(y_col)

                # Hauteur de l'image sur le pdf à prendre
                h_tmp_pdf = min((rectItems.height() - h_printed_pdf)*w_scale, pdf.page_break_trigger - pdf.get_y() - pdf.font_size)

                # Zone de la scène à capturer
                rectTmp = QRectF(rectItems.x(), rectItems.y() + h_printed_pdf, w_coil_scene, h_tmp_pdf/w_scale)

                # Calcul de la size en pixel
                scale = min(pdf.max_width_px/rectTmp.toRect().width(), pdf.max_heigth_px/rectTmp.toRect().height())
                targetSize = QSize(rectTmp.toRect().width()*scale, rectTmp.toRect().height()*scale)

                # Extraction de l'image
                pixMap = QImage(targetSize, QImage.Format_ARGB32_Premultiplied)
                pixMap.fill(Qt.white)
                painter = QPainter(self)
                painter.begin(pixMap)
                painter.setRenderHint(QPainter.Antialiasing, True)
                self.scene_coil.render(painter, source=rectTmp)
                painter.end()

                file = QTemporaryFile(self)
                file.open(QIODevice.WriteOnly)
                pixMap.save(file, "PNG")
                file.close()

                # Sur 2 colonnes
                pdf.image(file.fileName(), fmt="png", x=lst_x_col[col], w=w_coil_pdf)
                h_printed_pdf = h_printed_pdf + rectTmp.height()
                col = (col + 1)%len(lst_x_col)

                # Placement d'un saut de page si besoin
                if rectItems.height() - h_printed_pdf > 1 and col == 0:
                    pdf.add_page()

            # Placement final
            if col == 0:
                pdf.add_page()

            # On remet le rect view
            self.updateActiveViewRect()

    def loadXMLTree(self, coil_elt):
        """
        Chargement de l'arbre XML
        """
        # MAJ des infos de la coil
        self.coil.updateDiscCalculation()

        self.disconnectModification()

        # Rayon et nombre de discs
        self.ui_le_innerRadius.setText(float(coil_elt.firstChildElement("r_inner_m").text())*1e3)
        self.ui_spBox_nbreDiscs.setValue(coil_elt.firstChildElement("discs").childNodes().count())
        self.coil.setDiscNumber(self.ui_spBox_nbreDiscs.value())

        # Radial spacers
        e_rs = coil_elt.firstChildElement("radial_spacers")
        self.ui_spBox_nbre_radSpacers.setValue(int(e_rs.firstChildElement("N_spacers").text()))
        self.ui_le_radSpacerWidth.setText(float(e_rs.firstChildElement("w_spacer_m").text())*1e3)

        # Résultats
        lst_res_thermo = []
        tmp = coil_elt.elementsByTagName("res_thermo_K")
        for i in range(tmp.count()):
            lst_res_thermo.append(tmp.item(i).attributes())
        for tr in lst_res_thermo:
            if tr.count() > 0:
                dict_res = {}
                for c in range(tr.count()):
                    attribute = tr.item(c).toAttr()
                    if "id_calcul" in attribute.name():
                        id_calcul = attribute.value()
                    else:
                        dict_res[attribute.name()] = float(attribute.value())
                self.setThermalDiagram(id_calcul, dict_res)

        # Coil
        self.coil.loadXMLTree(coil_elt)

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

    win = UI_CoilDefinition()

    # 3 - Affichage de la fenêtre
    win.show()
    app.exec()