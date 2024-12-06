# -*- coding: utf-8 -*-
from functools import partial
from statistics import mean
from math import pi, acos, sin, cos
from numpy import array

from PySide6.QtGui import QDoubleValidator, QPen, QFont, QPainterPath, QColor, QPolygonF, QPainter
from PySide6.QtCore import Qt, Signal, QLocale, QObject, QRectF, QSizeF, QLineF, QPointF
from PySide6.QtWidgets import QVBoxLayout, QGraphicsItem, QColorDialog, QGraphicsRectItem, QMenu, QLabel, QWidgetAction, QWidget, QHBoxLayout, QGraphicsLineItem, QGraphicsObject

from . import gui_utils

### Couleurs
# Non défini
COLOR_undefined = Qt.red
# Sens de bobinage
COLOR_positive = QColor(255, 128, 0) # Orange
COLOR_negative = Qt.darkGreen
# Matériaux
COLOR_copper = Qt.yellow
COLOR_varnish = Qt.green
COLOR_pressboard = Qt.blue
COLOR_paper = Qt.darkYellow
COLOR_polyester = Qt.darkCyan
COLOR_magneticCircuit = Qt.gray
COLOR_oil = QColor(247, 226, 84) # Jaune-Orange
COLOR_oilGuide = Qt.black

def getPseudoRandomColor(text,thickness):
    """
    couleur déterministe : utilisé pour les ducts et les pressboards (fonctions ci-dessous)
    """
    if text == 'pressboard':
        R = 30*thickness % 255
        G = 15*thickness % 255
        B = 10*thickness % 255
    elif text == 'duct':
        R = 30*thickness % 255
        G = 60*thickness % 255
        B = 90*thickness % 255
    else:
        raise Exception("Argument '" + str(text) + "' inconnu (valeur attendue : pressboard ou duct)")
    color = QColor.fromRgb(R,G,B)
    return color

COLOR_currentHue = 0.0
def getRandomColor():
    """
    couleur aléatoire : utilisé pour les discs (disc_one.py)
    """
    global COLOR_currentHue
    color = QColor.fromHslF(COLOR_currentHue, 1.0, 0.5)
    COLOR_currentHue = (COLOR_currentHue + 0.618033988749895) % 1.0
    return color


# =============================================================================
# Classes pour les représentations graphiques
# =============================================================================
class Coil(QObject):
    """
    Classe gérant la représentation graphique d'une bobine
    """

    # Signal quand la bobine est mise à jour
    # /!\ hériter également de QGraphicsObject ou de QObject pour que ça marche !
    coilUpdated = Signal()
    # Signal quand la bobine est modifiée par l'utilisateur (non programmatiquement)
    isModified = Signal()

    def __init__(self, scene_coil, scene_lgd, ui_coil):
        super().__init__()

        # Scene
        self.scene_coil = scene_coil
        self.scene_lgd = scene_lgd

        # ui
        self.ui_coil = ui_coil
        self.lst_ui_disc = []
        self.isFrozen = False

        # Listes d'éléments graphiques empilés du bas vers le haut
        self.inner_duct = None
        self.lst_center = []
        self.outer_duct = None

        self.legend = None

        # Données
        self.nb_disc = 1
        self.dict_colorDuct = {}
        self.dict_colorPressboard = {}
        self.disc_width = 1.0
        self.ep_duct_defaut = 1.0

        # Liste des calculs chargés
        self.lst_calcul_loaded = []

        # Connection
        self.ui_coil.ui_chk_discs.stateChanged.connect(self.updateCoil)
        self.ui_coil.ui_chk_ducts.stateChanged.connect(self.updateCoil)
        self.ui_coil.ui_chk_pressboards.stateChanged.connect(self.updateCoil)
        self.ui_coil.ui_btn_symBT.clicked.connect(partial(self.symmetryCoil, "BT"))
        self.ui_coil.ui_btn_symTB.clicked.connect(partial(self.symmetryCoil, "TB"))

        self.ui_coil.ui_btn_symBT.clicked.connect(self.isModified.emit)
        self.ui_coil.ui_btn_symTB.clicked.connect(self.isModified.emit)

    def freezeDesign(self, isFrozen):
        """
        Action lors du (dé)gelage du design
        """
        self.ui_coil.ui_btn_symBT.setEnabled(not isFrozen)
        self.ui_coil.ui_btn_symTB.setEnabled(not isFrozen)
        self.isFrozen = isFrozen

    def addLoadedCalcul(self, dico_param):
        """
        Ajout d'un calcul à la liste des calculs chargés
        """
        # On s'assure de l'unicité des id_calcul
        add = True
        for c in self.lst_calcul_loaded:
            if c["id_calcul"] == dico_param["id_calcul"]:
                add = False
                c = dico_param

        if add:
            self.lst_calcul_loaded.append(dico_param)

    def removeLoadedCalcul(self, id_calcul=None):
        """
        Retrait d'un calcul à la liste des calculs chargés et des éléments
        """
        if id_calcul == None:
            # On supprime tout
            self.lst_calcul_loaded = []
        else:
            # Suppression des calculs chargés
            k_delete = None
            for k in range(len(self.lst_calcul_loaded)):
                if self.lst_calcul_loaded[k]["id_calcul"] == id_calcul:
                    # Par construction, il n'y en a qu'un
                    k_delete = k
                    break

            if k_delete != None:
                del self.lst_calcul_loaded[k_delete]

        # Et des éléments
        for dd in self.lst_center:
            dd.removeLoadedCalcul(id_calcul)

    def addUIDisc(self, ui_disc):
        """
        Ajout d'une descriptiond de disc possible
        """
        self.lst_ui_disc.append(ui_disc)

    def removeUIDisc(self, ui_disc):
        """
        Retrait d'une description de disc possible
        """
        self.lst_ui_disc.remove(ui_disc)

    def updateDiscCalculation(self):
        """
        MAJ du calcul des dimensions des discs
        """
        for ui_disc in self.lst_ui_disc:
            ui_disc.updateCables()
            ui_disc.cableCalculation(False)

    def resetAll(self):
        """
        Reset des infos de la bobine (en cas d'erreur de définition)
        """

        while len(self.lst_center) > 0:
            self.scene_coil.removeItem(self.lst_center.pop(0))
        self.scene_coil.removeItem(self.inner_duct)
        self.inner_duct = None
        self.scene_coil.removeItem(self.outer_duct)
        self.outer_duct = None
        self.scene_coil.removeItem(self.legend)
        self.legend = None

    def setDiscNumber(self, nb_disc):
        """
        Définition du nombre de disques de la coil
        """
        # Nombre de discs
        self.nb_disc = nb_disc

        # Nombre de disc nul, on reset et s'arrête
        if self.nb_disc == 0:
            self.resetAll()
            return

        # S'il n'y a pas de définition de disc, on reset et s'arrête
        if len(self.lst_ui_disc) == 0:
            self.resetAll()
            return

        # Description vide, on reset et s'arrête
        descDisc0 = self.lst_ui_disc[0].getDisc()
        if descDisc0 == {}:
            self.resetAll()
            return
        # On récupère la largeur des disques (la même par construction)
        self.disc_width = descDisc0["h_cable"]*descDisc0["N_cables"]

        # Epaisseur par défaut des canaux
        lst_tmp_cable_thick = []
        for d in self.lst_ui_disc:
            lst_tmp_cable_thick.append(d.getDisc()["t_cable"])
        self.ep_duct_defaut = round(mean(lst_tmp_cable_thick)/2, 1)

        if len(self.lst_center) == 0:
            # 1er affichage
            self.buildCoil()
        else:
            # MAJ des données de la coil
            self.updateCoilData()

        self.updateCoil()

    def buildCoil(self):
        """
        Construction initiale de la bobine à partir des données
        """
        # Légende
        self.legend = Legend()
        self.scene_lgd.addItem(self.legend)

        # Couleurs par défaut
        self.dict_colorDuct[self.ep_duct_defaut] = COLOR_oil
        self.dict_colorPressboard[self.ep_duct_defaut] = COLOR_pressboard

        ### Partie centrale
        # Canal du bas
        tmp = Duct(self)
        tmp.setSize(self.disc_width, self.ep_duct_defaut)
        tmp.setFlag(QGraphicsItem.ItemIsSelectable, True)
        tmp.setZValue(1)
        self.scene_coil.addItem(tmp)
        self.lst_center.append(tmp)

        # Disques + canaux supérieurs
        for k in range(self.nb_disc):
            # Disque
            tmp = Disc(self)
            tmp.setDisc(self.lst_ui_disc[0])
            tmp.setInnerDuctThickness(self.ep_duct_defaut)
            tmp.setOuterDuctThickness(self.ep_duct_defaut)
            tmp.setFlag(QGraphicsItem.ItemIsSelectable, True)
            tmp.setZValue(2)
            self.scene_coil.addItem(tmp)
            self.lst_center.append(tmp)

            # Canal supérieur
            tmp = Duct(self)
            tmp.setSize(self.disc_width, self.ep_duct_defaut)
            tmp.setFlag(QGraphicsItem.ItemIsSelectable, True)
            tmp.setZValue(1)
            self.scene_coil.addItem(tmp)
            self.lst_center.append(tmp)

        ### Canaux verticaux
        # Calcul de la hauteur de la partie centrale
        tmp_height = 0.0
        for k in self.lst_center:
            tmp_height = tmp_height + k.thickness

        # Canal intérieur
        self.inner_duct = Duct(self)
        self.inner_duct.setSize(tmp_height, self.ep_duct_defaut)
        self.inner_duct.rotate(False)
        self.inner_duct.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.inner_duct.setZValue(0)
        self.scene_coil.addItem(self.inner_duct)

        # Canal extérieur
        self.outer_duct = Duct(self)
        self.outer_duct.setSize(tmp_height, self.ep_duct_defaut)
        self.outer_duct.rotate(False)
        self.outer_duct.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.outer_duct.setZValue(0)
        self.scene_coil.addItem(self.outer_duct)

    def updateCoilData(self):
        """
        Mise à jour suite à chgt du nb_disc et/ou de lst_ui_disc
        """
        # Parcours des éléments centraux
        num_disc = 1
        virer = False

        k = 0
        while k < len(self.lst_center):

            if isinstance(self.lst_center[k], Disc):
                if num_disc > self.nb_disc:
                    virer = True
                num_disc = num_disc + 1

                if not self.lst_center[k].ui_disc in self.lst_ui_disc:
                    # Si la description du disc n'existe plus -> disc[0] + MAJ
                    self.lst_center[k].setDisc(self.lst_ui_disc[0])
                else:
                    # Mise à jour du disc existant
                    self.lst_center[k].updateDisc()

            if isinstance(self.lst_center[k], Duct):
                # MAJ taille du duct
                self.lst_center[k].setSize(self.disc_width, None)

            if isinstance(self.lst_center[k], Pressboard):
                # MAJ taille du pressboard
                self.lst_center[k].setSize(self.disc_width, None)

            if virer:
                self.scene_coil.removeItem(self.lst_center.pop(k))
            else:
                k = k + 1

        # Ajout de disc s'il en manque
        for k in range(self.nb_disc - num_disc + 1):
            # Disque
            tmp = Disc(self)
            tmp.setDisc(self.lst_ui_disc[0])
            tmp.setInnerDuctThickness(self.inner_duct.thickness)
            tmp.setOuterDuctThickness(self.outer_duct.thickness)
            tmp.setFlag(QGraphicsItem.ItemIsSelectable, True)
            tmp.setZValue(2)
            self.scene_coil.addItem(tmp)
            self.lst_center.append(tmp)

            # Canal supérieur
            tmp = Duct(self)
            tmp.setSize(self.disc_width, self.ep_duct_defaut)
            tmp.setFlag(QGraphicsItem.ItemIsSelectable, True)
            tmp.setZValue(1)
            self.scene_coil.addItem(tmp)
            self.lst_center.append(tmp)

    def symmetryCoil(self, sensSym):
        """
        Symétrie des éléments de la bobine selon le sens indiqué
        Le milieu est donné par le disque milieu
        """
        num_disc_milieu = int(self.nb_disc/2)
        num_disc = 1
        virer = False
        virerNext = False

        if sensSym == "BT":
            # Sens bas -> haut
            # Suppression des éléments supérieurs
            k = 0
            while k < len(self.lst_center):

                if isinstance(self.lst_center[k], Disc):
                    if num_disc > num_disc_milieu:
                        virer = True
                    num_disc = num_disc + 1

                if virer and self.nb_disc%2 == 0 or virerNext and self.nb_disc%2 == 1:
                    self.scene_coil.removeItem(self.lst_center.pop(k))
                else:
                    k = k + 1

                if virer:
                    virerNext = True

            # Ajout des éléments par symétrie
            for d in list(reversed(self.lst_center))[1:]:
                if isinstance(d, Disc):
                    tmp = Disc(self)
                    tmp.setDisc(d.ui_disc)
                    tmp.setInnerDuctThickness(d.inner_duct_thickness)
                    tmp.setOuterDuctThickness(d.outer_duct_thickness)
                    tmp.setInnerGuide(d.inner_guide)
                    tmp.setOuterGuide(d.outer_guide)
                    tmp.setFlag(QGraphicsItem.ItemIsSelectable, True)
                    tmp.setZValue(2)
                    self.scene_coil.addItem(tmp)
                    self.lst_center.append(tmp)

                elif isinstance(d, Duct):
                    tmp = Duct(self)
                    tmp.setSize(d.height, d.thickness)
                    tmp.setFlag(QGraphicsItem.ItemIsSelectable, True)
                    tmp.setZValue(1)
                    self.scene_coil.addItem(tmp)
                    self.lst_center.append(tmp)

                elif isinstance(d, Pressboard):
                    tmp = Pressboard(self)
                    tmp.setSize(d.height, d.thickness)
                    tmp.setInnerDuctThickness(d.inner_duct_thickness)
                    tmp.setOuterDuctThickness(d.outer_duct_thickness)
                    tmp.setInnerGuide(d.inner_guide)
                    tmp.setOuterGuide(d.outer_guide)
                    tmp.setFlag(QGraphicsItem.ItemIsSelectable, True)
                    tmp.setZValue(2)
                    self.scene_coil.addItem(tmp)
                    self.lst_center.append(tmp)

                else:
                    raise Exception("Objet inconnu")
        else:
            # Sens haut -> bas
            # Suppression des éléments inférieurs
            lst_a_virer = []
            k = len(self.lst_center)-1
            while k >= 0:

                if isinstance(self.lst_center[k], Disc):
                    if num_disc > num_disc_milieu:
                        virer = True
                    num_disc = num_disc + 1

                if virer and self.nb_disc%2 == 0 or virerNext and self.nb_disc%2 == 1:
                    lst_a_virer.append(self.lst_center[k])
                k = k - 1

                if virer:
                    virerNext = True

            # On vire
            for d in lst_a_virer:
                self.lst_center.remove(d)
                self.scene_coil.removeItem(d)

            # Ajout des éléments par symétrie
            for d in list(self.lst_center)[1:]:
                if isinstance(d, Disc):
                    tmp = Disc(self)
                    tmp.setDisc(d.ui_disc)
                    tmp.setInnerDuctThickness(d.inner_duct_thickness)
                    tmp.setOuterDuctThickness(d.outer_duct_thickness)
                    tmp.setInnerGuide(d.inner_guide)
                    tmp.setOuterGuide(d.outer_guide)
                    tmp.setFlag(QGraphicsItem.ItemIsSelectable, True)
                    tmp.setZValue(2)
                    self.scene_coil.addItem(tmp)
                    self.lst_center.insert(0, tmp)

                elif isinstance(d, Duct):
                    tmp = Duct(self)
                    tmp.setSize(d.height, d.thickness)
                    tmp.setFlag(QGraphicsItem.ItemIsSelectable, True)
                    tmp.setZValue(1)
                    self.scene_coil.addItem(tmp)
                    self.lst_center.insert(0, tmp)

                elif isinstance(d, Pressboard):
                    tmp = Pressboard(self)
                    tmp.setSize(d.height, d.thickness)
                    tmp.setInnerDuctThickness(d.inner_duct_thickness)
                    tmp.setOuterDuctThickness(d.outer_duct_thickness)
                    tmp.setInnerGuide(d.inner_guide)
                    tmp.setOuterGuide(d.outer_guide)
                    tmp.setFlag(QGraphicsItem.ItemIsSelectable, True)
                    tmp.setZValue(2)
                    self.scene_coil.addItem(tmp)
                    self.lst_center.insert(0, tmp)

                else:
                    raise Exception("Objet inconnu")

        self.updateCoil()


    def setLegend(self):
        """
        Construction et application de la legende
        """
        dico_lgd = {}

        for d in self.lst_center + [self.inner_duct, self.outer_duct]:
            if isinstance(d, Disc):
                tmp = "Disc " + d.currentDescDisc["name"]
                if not tmp in dico_lgd.keys():
                    dico_lgd[tmp] = [1, d.currentDescDisc["color"]]
                else:
                    dico_lgd[tmp][0] = dico_lgd[tmp][0] + 1

                if d.inner_guide or d.outer_guide:
                    tmp = "Oil guide"
                    if not tmp in dico_lgd.keys():
                        dico_lgd[tmp] = [1, COLOR_oilGuide]
                    else:
                        dico_lgd[tmp][0] = dico_lgd[tmp][0] + 1

            elif isinstance(d, Duct):
                tmp = "Duct %.1f mm"%d.thickness
                if not tmp in dico_lgd.keys():
                    dico_lgd[tmp] = [1, self.getColorDuctThickness(d.thickness)]
                else:
                    dico_lgd[tmp][0] = dico_lgd[tmp][0] + 1

            elif isinstance(d, Pressboard):
                tmp = "Pressboard %.1f mm"%d.thickness
                if not tmp in dico_lgd.keys():
                    dico_lgd[tmp] = [1, self.getColorPressboardThickness(d.thickness)]
                else:
                    dico_lgd[tmp][0] = dico_lgd[tmp][0] + 1

                if d.inner_guide or d.outer_guide:
                    tmp = "Oil guide"
                    if not tmp in dico_lgd.keys():
                        dico_lgd[tmp] = [1, COLOR_oilGuide]
                    else:
                        dico_lgd[tmp][0] = dico_lgd[tmp][0] + 1

            else:
                raise Exception("Objet inconnu")

        self.legend.setLegend(dico_lgd)

    def updateCoil(self):
        """
        MAJ des positions des éléments (ne s'appuie pas sur les données initiales)
        Prend en compte
            - Les listes d'objets graphiques (lst_center, inner_duct, outer_duct)
            - Les dimensions des objets graphiques
        """
        # Origine : en bas à l'intérieur de la bobine
        x0 = 0
        y0 = 0

        ### Partie centrale (disc + duct)
        x = x0 + self.inner_duct.thickness
        y = y0
        tmp_height = 0.0
        num_disc = 1

        for dd in self.lst_center:
            # Geometrie
            dd.setCenter(x + dd.height/2, y - dd.thickness/2)
            if isinstance(dd, Disc) or isinstance(dd, Pressboard):
                dd.setInnerDuctThickness(self.inner_duct.thickness)
                dd.setOuterDuctThickness(self.outer_duct.thickness)

            # Tooltip
            if isinstance(dd, Disc):
                dd.setDiscNumber(num_disc)
                num_disc = num_disc + 1

            # Visibilité
            if isinstance(dd, Disc):
                dd.setVisible(self.ui_coil.ui_chk_discs.isChecked())
            if isinstance(dd, Duct):
                dd.setVisible(self.ui_coil.ui_chk_ducts.isChecked())
            if isinstance(dd, Pressboard):
                dd.setVisible(self.ui_coil.ui_chk_pressboards.isChecked())

            tmp_height = tmp_height + dd.thickness
            y = y - dd.thickness
        x = x + dd.height

        ### Canal intérieur
        self.inner_duct.setSize(tmp_height, None)
        self.inner_duct.setCenter(x0 + self.inner_duct.thickness/2, y0 - self.inner_duct.height/2)
        self.inner_duct.setVisible(self.ui_coil.ui_chk_ducts.isChecked())

        ### Canal extérieur
        self.outer_duct.setSize(tmp_height, None)
        self.outer_duct.setCenter(x + self.outer_duct.thickness/2, y0 - self.outer_duct.height/2)
        self.outer_duct.setVisible(self.ui_coil.ui_chk_ducts.isChecked())

        ### MAJ des dimensions de la bobine
        width = self.disc_width + self.inner_duct.thickness + self.outer_duct.thickness
        self.ui_coil.ui_le_coilWidth.setText(width)
        self.ui_coil.ui_le_coilHeight.setText(tmp_height)

        ### Pour l'affichage
        self.scene_coil.setSceneRect(QRectF(0, -tmp_height, width, tmp_height))

        self.setLegend()

        # Signal
        self.coilUpdated.emit()

    def actChangeThickness(self, le_thickness, type_obj):
        """
        Action de changement de l'epaisseur d'un element en se basant sur le QLineEdit
        Ne s'applique que sur les objets de type type_obj
        """
        for c in self.scene_coil.selectedItems():
            if type(c) == type_obj:
                c.setSize(None, float(le_thickness.text()))

        # On déselectionne tout
        self.scene_coil.clearSelection()

        self.updateCoil()

    def actChangeDisc(self, desc, type_obj):
        """
        Action de changement du type de disc
        Ne s'applique que sur les objets de type type_obj
        """
        for c in self.scene_coil.selectedItems():
            if type(c) == type_obj:
                c.setDisc(desc)

        # On déselectionne tout
        self.scene_coil.clearSelection()

        self.updateCoil()

    def actOilGuide(self, side, type_obj):
        """
        Action d'application d'une chicane
        Ne s'applique que sur les objets de type type_obj
        """
        for c in self.scene_coil.selectedItems():
            if type(c) == type_obj:
                if side == "inner":
                    c.setInnerGuide()
                elif side == "outer":
                    c.setOuterGuide()
                elif side == "remove":
                    c.setInnerGuide(False)
                    c.setOuterGuide(False)
                else:
                    raise Exception("Side inconnu")

        # On déselectionne tout
        self.scene_coil.clearSelection()

        # Pas besoin d'updateCoil
        self.setLegend()

    def actInsertPressboard(self, position, type_obj):
        """
        Action d'ajout d'un carton à la position par rapport à l'objet
        Ne s'applique que sur les objets de type type_obj
        """
        for c in self.scene_coil.selectedItems():
            if type(c) == type_obj:

                pos_objet = self.lst_center.index(c)

                # Pressboard
                tmp_p = Pressboard(self)
                tmp_p.setSize(self.disc_width, self.ep_duct_defaut)
                tmp_p.setInnerDuctThickness(self.inner_duct.thickness)
                tmp_p.setOuterDuctThickness(self.outer_duct.thickness)
                tmp_p.setFlag(QGraphicsItem.ItemIsSelectable, True)
                tmp_p.setZValue(2)
                self.scene_coil.addItem(tmp_p)

                # Canal supérieur
                tmp_d = Duct(self)
                tmp_d.setSize(self.disc_width, self.ep_duct_defaut)
                tmp_d.setFlag(QGraphicsItem.ItemIsSelectable, True)
                tmp_d.setZValue(1)
                self.scene_coil.addItem(tmp_d)

                if position == "above":
                    self.lst_center.insert(pos_objet + 1, tmp_d)
                    self.lst_center.insert(pos_objet + 2, tmp_p)
                elif position == "under":
                    self.lst_center.insert(pos_objet, tmp_p)
                    self.lst_center.insert(pos_objet + 1, tmp_d)
                else:
                    raise Exception("Position inconnue")

        # On déselectionne tout
        self.scene_coil.clearSelection()

        self.updateCoil()

    def resetLoss(self):
        """
        Réinitialisation de toutes les pertes de la bobine
        """
        for dd in self.lst_center:
            if isinstance(dd, Disc):
                dd.dict_loss = {}
        self.lst_calcul_loaded = []

    def actColorDisc(self, ui_disc):
        """
        Changement de la couleur des discs par description
        """

        # Fenêtre de choix de la couleur
        color = QColorDialog.getColor()
        if not color.isValid():
            return

        # Application
        ui_disc.setDiscColor(color)
        self.updateCoilData()

        # On déselectionne tout
        self.scene_coil.clearSelection()

        # MAJ Legende
        self.setLegend()

    def actColorDuct(self, obj):
        """
        Changement de la couleur des canaux par epaisseur
        """

        # Fenêtre de choix de la couleur
        color = QColorDialog.getColor()
        if not color.isValid():
            return

        # Application aux canaux
        self.dict_colorDuct[obj.thickness] = color

        # On déselectionne tout
        self.scene_coil.clearSelection()

        # MAJ Legende
        self.setLegend()

    def getColorDuctThickness(self, thickness):
        if not thickness in self.dict_colorDuct.keys():
            color = getPseudoRandomColor('duct',thickness)
            self.dict_colorDuct[thickness] = color

        return self.dict_colorDuct[thickness]

    def actColorPressboard(self, obj):
        """
        Changement de la couleur des cartons par epaisseur
        """

        # Fenêtre de choix de la couleur
        color = QColorDialog.getColor()
        if not color.isValid():
            return

        # Application aux canaux
        self.dict_colorPressboard[obj.thickness] = color

        # On déselectionne tout
        self.scene_coil.clearSelection()

        self.setLegend()

    def getColorPressboardThickness(self, thickness):
        if not thickness in self.dict_colorPressboard.keys():
            color = getPseudoRandomColor('pressboard',thickness)
            self.dict_colorPressboard[thickness] = color

        return self.dict_colorPressboard[thickness]

    def actRemove(self, type_obj):
        """
        Suppression des objets et du canal supérieur à celui-ci
        Ne s'applique que sur les objets de type type_obj
        """
        for c in self.scene_coil.selectedItems():
            if type(c) == type_obj:

                pos_objet = self.lst_center.index(c)
                self.scene_coil.removeItem(self.lst_center.pop(pos_objet)) # Objet
                self.scene_coil.removeItem(self.lst_center.pop(pos_objet)) # Canal supérieur

        # On déselectionne tout
        self.scene_coil.clearSelection()

        self.updateCoil()

    def addXMLTreeDesign(self, tag_coil, docDom):
        """
        Ajout des données au fichier XML de design
        """

        if self.inner_duct == None or self.outer_duct == None:
            return

        tag_tmp = docDom.createElement('width_m')
        tag_tmp.appendChild(docDom.createTextNode("%e"%(self.disc_width*1e-3)))
        tag_coil.appendChild(tag_tmp)

        tag_vduct = docDom.createElement('vertical_ducts')
        tag_coil.appendChild(tag_vduct)
        tag_d = docDom.createElement('duct')
        tag_vduct.appendChild(tag_d)
        tag_tmp = docDom.createElement('t_duct_m')
        tag_tmp.appendChild(docDom.createTextNode("%e"%(self.inner_duct.thickness*1e-3)))
        tag_d.appendChild(tag_tmp)
        tag_tmp = docDom.createElement('r_center_m')
        tag_tmp.appendChild(docDom.createTextNode("%e"%(self.inner_duct.x_center*1e-3)))
        tag_d.appendChild(tag_tmp)
        tag_d = docDom.createElement('duct')
        tag_vduct.appendChild(tag_d)
        tag_tmp = docDom.createElement('t_duct_m')
        tag_tmp.appendChild(docDom.createTextNode("%e"%(self.outer_duct.thickness*1e-3)))
        tag_d.appendChild(tag_tmp)
        tag_tmp = docDom.createElement('r_center_m')
        tag_tmp.appendChild(docDom.createTextNode("%e"%(self.outer_duct.x_center*1e-3)))
        tag_d.appendChild(tag_tmp)

        # Listes des éléments centraux
        lst_discs = [d for d in self.lst_center if isinstance(d, Disc)]
        lst_ducts = [d for d in self.lst_center if isinstance(d, Duct)]
        lst_pressboards = [d for d in self.lst_center if isinstance(d, Pressboard)]

        tag_disc = docDom.createElement('discs')
        tag_coil.appendChild(tag_disc)
        for d in lst_discs:
            tag_d = docDom.createElement('disc')
            tag_disc.appendChild(tag_d)
            tag_tmp = docDom.createElement('type')
            tag_tmp.appendChild(docDom.createTextNode(d.currentDescDisc["name"]))
            tag_d.appendChild(tag_tmp)
            tag_tmp = docDom.createElement('z_center_m')
            tag_tmp.appendChild(docDom.createTextNode("%e"%(-d.y_center*1e-3)))
            tag_d.appendChild(tag_tmp)
            tag_tmp = docDom.createElement('oil_guides')
            if d.inner_guide and not d.outer_guide:
                tag_tmp.appendChild(docDom.createTextNode("inner"))
            elif d.outer_guide and not d.inner_guide:
                tag_tmp.appendChild(docDom.createTextNode("outer"))
            else:
                tag_tmp.appendChild(docDom.createTextNode("no"))
            tag_d.appendChild(tag_tmp)

        tag_duct = docDom.createElement('horizontal_ducts')
        tag_coil.appendChild(tag_duct)
        for d in lst_ducts:
            tag_d = docDom.createElement('duct')
            tag_duct.appendChild(tag_d)
            tag_tmp = docDom.createElement('t_duct_m')
            tag_tmp.appendChild(docDom.createTextNode("%e"%(d.thickness*1e-3)))
            tag_d.appendChild(tag_tmp)
            tag_tmp = docDom.createElement('z_center_m')
            tag_tmp.appendChild(docDom.createTextNode("%e"%(-d.y_center*1e-3)))
            tag_d.appendChild(tag_tmp)

        tag_pressboard = docDom.createElement('pressboards')
        tag_coil.appendChild(tag_pressboard)
        for d in lst_pressboards:
            tag_d = docDom.createElement('pressboard')
            tag_pressboard.appendChild(tag_d)
            tag_tmp = docDom.createElement('t_pressboard_m')
            tag_tmp.appendChild(docDom.createTextNode("%e"%(d.thickness*1e-3)))
            tag_d.appendChild(tag_tmp)
            tag_tmp = docDom.createElement('z_center_m')
            tag_tmp.appendChild(docDom.createTextNode("%e"%(-d.y_center*1e-3)))
            tag_d.appendChild(tag_tmp)
            tag_tmp = docDom.createElement('oil_guides')
            if d.inner_guide and not d.outer_guide:
                tag_tmp.appendChild(docDom.createTextNode("inner"))
            elif d.outer_guide and not d.inner_guide:
                tag_tmp.appendChild(docDom.createTextNode("outer"))
            else:
                tag_tmp.appendChild(docDom.createTextNode("no"))
            tag_d.appendChild(tag_tmp)

    def addXMLTreeResult(self, id_calcul, tag_coil, docDom):
        """
        Ajout des données au fichier XML de résulats
        """
        if self.inner_duct == None or self.outer_duct == None:
            return

        tag_vduct = docDom.createElement('vertical_ducts')
        tag_coil.appendChild(tag_vduct)

        # Listes des éléments centraux
        lst_discs = [d for d in self.lst_center if isinstance(d, Disc)]
        lst_ducts = [d for d in self.lst_center if isinstance(d, Duct)]
        lst_pressboards = [d for d in self.lst_center if isinstance(d, Pressboard)]

        tag_disc = docDom.createElement('discs')
        tag_coil.appendChild(tag_disc)
        for d in lst_discs:
            tag_d = docDom.createElement('disc')
            tag_disc.appendChild(tag_d)

            # Pertes
            l_disc = d.getLossCable(id_calcul)
            if l_disc is not None:
                for kk in range(len(l_disc)):
                    tag_c = docDom.createElement('cable')
                    tag_d.appendChild(tag_c)
                    tag_l = docDom.createElement('loss_W')
                    tag_l.appendChild(docDom.createTextNode("%f"%l_disc[kk]))
                    tag_c.appendChild(tag_l)

            # Echauffement moyen
            if id_calcul in d.dict_averageTR.keys():
                tag_tmp = docDom.createElement('averageTR_K')
                tag_tmp.appendChild(docDom.createTextNode("%f"%d.dict_averageTR[id_calcul]))
                tag_d.appendChild(tag_tmp)

            # Echauffement maximum
            if id_calcul in d.dict_maxTR.keys():
                tag_tmp = docDom.createElement('maxTR_K')
                tag_tmp.appendChild(docDom.createTextNode("%f"%d.dict_maxTR[id_calcul]))
                tag_d.appendChild(tag_tmp)

        tag_duct = docDom.createElement('horizontal_ducts')
        tag_coil.appendChild(tag_duct)
        for d in lst_ducts:
            tag_d = docDom.createElement('duct')
            tag_duct.appendChild(tag_d)

            # Echauffement moyen
            if id_calcul in d.dict_averageTR.keys():
                tag_tmp = docDom.createElement('averageTR_K')
                tag_tmp.appendChild(docDom.createTextNode("%f"%d.dict_averageTR[id_calcul]))
                tag_d.appendChild(tag_tmp)

            # Vitesse moyenne moyen
            if id_calcul in d.dict_averageVelocity.keys():
                tag_tmp = docDom.createElement('averageVelocity_m.s-1')
                tag_tmp.appendChild(docDom.createTextNode("%f"%d.dict_averageVelocity[id_calcul]))
                tag_d.appendChild(tag_tmp)

        tag_pressboard = docDom.createElement('pressboards')
        tag_coil.appendChild(tag_pressboard)
        for d in lst_pressboards:
            tag_d = docDom.createElement('pressboard')
            tag_pressboard.appendChild(tag_d)

            # Echauffement moyen
            if id_calcul in d.dict_averageTR.keys():
                tag_tmp = docDom.createElement('averageTR_K')
                tag_tmp.appendChild(docDom.createTextNode("%f"%d.dict_averageTR[id_calcul]))
                tag_d.appendChild(tag_tmp)

            # Echauffement maximum
            if id_calcul in d.dict_maxTR.keys():
                tag_tmp = docDom.createElement('maxTR_K')
                tag_tmp.appendChild(docDom.createTextNode("%f"%d.dict_maxTR[id_calcul]))
                tag_d.appendChild(tag_tmp)

    def loadXMLTreeResult(self, coil_elt, id_calcul):
        """
        Chargement des résultats sur la coil
        """
        # La géométrie a déjà été chargée par loadXMLTree

        ### Valeurs locales
#        e_vd = coil_elt.firstChildElement("vertical_ducts")
        e_discs = coil_elt.firstChildElement("discs")
        n_disc = e_discs.firstChildElement("disc")
        e_hducts = coil_elt.firstChildElement("horizontal_ducts")
        n_hduct = e_hducts.firstChildElement("duct")
        e_pressboards = coil_elt.firstChildElement("pressboards")
        n_pressboard = e_pressboards.firstChildElement("pressboard")
        for dd in self.lst_center:

            ### Discs
            if isinstance(dd, Disc) and not n_disc.isNull():
                e_disc = n_disc.toElement()

                # Pertes
                lst_loss = []
                n_c = e_disc.firstChildElement("cable")
                while not n_c.isNull():
                    e_c = n_c.toElement()
                    lst_loss.append(float(e_c.firstChildElement("loss_W").text()))
                    n_c = n_c.nextSiblingElement("cable")
                if len(lst_loss) > 0:
                    dd.setLossCable(id_calcul, lst_loss)
                    self.addLoadedCalcul({"id_calcul": id_calcul, "calculation_type": "loss"})

                # Average TR
                n_tmp = e_disc.firstChildElement("averageTR_K")
                if not n_tmp.isNull():
                    dd.setAverageTR(id_calcul, float(n_tmp.text()))
                    self.addLoadedCalcul({"id_calcul": id_calcul, "calculation_type": "thermoHydro"})

                # Max TR
                n_tmp = e_disc.firstChildElement("maxTR_K")
                if not n_tmp.isNull():
                    dd.setMaxTemp(id_calcul, float(n_tmp.text()))
                    self.addLoadedCalcul({"id_calcul": id_calcul, "calculation_type": "thermoHydro"})

                n_disc = n_disc.nextSiblingElement("disc")

            ### Ducts
            elif isinstance(dd, Duct) and not n_hduct.isNull():
                e_hduct = n_hduct.toElement()

                # Average TR
                n_tmp = e_hduct.firstChildElement("averageTR_K")
                if not n_tmp.isNull():
                    dd.setAverageTR(id_calcul, float(n_tmp.text()))
                    self.addLoadedCalcul({"id_calcul": id_calcul, "calculation_type": "thermoHydro"})

                # Average velocity
                n_tmp = e_hduct.firstChildElement("averageVelocity_m.s-1")
                if not n_tmp.isNull():
                    dd.setAverageVelocity(id_calcul, float(n_tmp.text()))
                    self.addLoadedCalcul({"id_calcul": id_calcul, "calculation_type": "thermoHydro"})

                n_hduct = n_hduct.nextSiblingElement("duct")

            ### Pressboards
            elif isinstance(dd, Pressboard) and not n_pressboard.isNull():
                e_pressboard = n_pressboard.toElement()

                # Average TR
                n_tmp = e_pressboard.firstChildElement("averageTR_K")
                if not n_tmp.isNull():
                    dd.setAverageTR(id_calcul, float(n_tmp.text()))
                    self.addLoadedCalcul({"id_calcul": id_calcul, "calculation_type": "thermoHydro"})

                # Max TR
                n_tmp = e_pressboard.firstChildElement("maxTR_K")
                if not n_tmp.isNull():
                    dd.setMaxTemp(id_calcul, float(n_tmp.text()))
                    self.addLoadedCalcul({"id_calcul": id_calcul, "calculation_type": "thermoHydro"})

                n_pressboard = n_pressboard.nextSiblingElement("pressboard")

    def loadXMLTree(self, coil_elt):
        """
        Chargement de l'arbre XML
        """
        # Chargement à partir de l'élément de bobine
        # Un setCoilData a déjà été fait par coilDefinition

        ### Duct verticaux
        e_vd = coil_elt.firstChildElement("vertical_ducts")
        lst_tmp = []
        n = e_vd.firstChildElement("duct")
        while not n.isNull():
            e_duct = n.toElement()
            d_tmp = {"t_duct": float(e_duct.firstChildElement("t_duct_m").text())*1e3, \
                     "r_center": float(e_duct.firstChildElement("r_center_m").text())*1e3}
            lst_tmp.append(d_tmp)
            n = n.nextSiblingElement("duct")

        lst_tmp = sorted(lst_tmp, key = lambda i: i['r_center'])
        if len(lst_tmp) > 0:
            self.inner_duct.setSize(None, lst_tmp[0]["t_duct"])
            if len(lst_tmp) > 1:
                self.outer_duct.setSize(None, lst_tmp[1]["t_duct"])

        ### Discs & Pressboard
        lst_tmp = []
        # Discs
        e_d = coil_elt.firstChildElement("discs")
        n = e_d.firstChildElement("disc")
        while not n.isNull():
            e_disc = n.toElement()
            d_tmp = {"item": "disc", \
                     "type": e_disc.firstChildElement("type").text(), \
                     "z_center": float(e_disc.firstChildElement("z_center_m").text())*1e3, \
                     "oil_guides": e_disc.firstChildElement("oil_guides").text()}
            lst_tmp.append(d_tmp)
            n = n.nextSiblingElement("disc")
        # Pressboards
        e_p = coil_elt.firstChildElement("pressboards")
        n = e_p.firstChildElement("pressboard")
        while not n.isNull():
            e_pressboard = n.toElement()
            d_tmp = {"item": "pressboard", \
                     "t_pressboard": float(e_pressboard.firstChildElement("t_pressboard_m").text())*1e3, \
                     "z_center": float(e_pressboard.firstChildElement("z_center_m").text())*1e3, \
                     "oil_guides": e_pressboard.firstChildElement("oil_guides").text()}
            lst_tmp.append(d_tmp)
            n = n.nextSiblingElement("pressboard")
        # On range tout ça
        lst_tmp = sorted(lst_tmp, key = lambda i: i['z_center'])

        # On parcourt la liste de disc et de pressboard
        k_lst_center = 0
        for kk in range(len(lst_tmp)):

            if lst_tmp[kk]["item"] == "disc":
                while not isinstance(self.lst_center[k_lst_center], Disc):
                    k_lst_center = k_lst_center + 1
                    if k_lst_center > len(self.lst_center):
                        break

                # On charge le 1er disc trouvé
                ui_disc = [d for d in self.lst_ui_disc if d.getDisc()["name"] == lst_tmp[kk]["type"]]
                if len(ui_disc) > 0:
                    self.lst_center[k_lst_center].setDisc(ui_disc[0])
                if lst_tmp[kk]["oil_guides"] == "inner":
                    self.lst_center[k_lst_center].setInnerGuide()
                elif lst_tmp[kk]["oil_guides"] == "outer":
                    self.lst_center[k_lst_center].setOuterGuide()
                else:
                    self.lst_center[k_lst_center].setInnerGuide(False)
                    self.lst_center[k_lst_center].setOuterGuide(False)

                k_lst_center = k_lst_center + 1

            elif lst_tmp[kk]["item"] == "pressboard":
                while not isinstance(self.lst_center[k_lst_center], Duct):
                    k_lst_center = k_lst_center + 1
                    if k_lst_center > len(self.lst_center):
                        break

                # Pressboard
                tmp_p = Pressboard(self)
                tmp_p.setSize(self.disc_width, lst_tmp[kk]["t_pressboard"])
                tmp_p.setInnerDuctThickness(self.inner_duct.thickness)
                tmp_p.setOuterDuctThickness(self.outer_duct.thickness)
                tmp_p.setFlag(QGraphicsItem.ItemIsSelectable, True)
                tmp_p.setZValue(2)
                if lst_tmp[kk]["oil_guides"] == "inner":
                    tmp_p.setInnerGuide()
                elif lst_tmp[kk]["oil_guides"] == "outer":
                    tmp_p.setOuterGuide()
                else:
                    tmp_p.setInnerGuide(False)
                    tmp_p.setOuterGuide(False)
                self.scene_coil.addItem(tmp_p)
                self.lst_center.insert(k_lst_center + 1, tmp_p)

                # Canal supérieur
                tmp_d = Duct(self)
                tmp_d.setSize(self.disc_width, self.ep_duct_defaut)
                tmp_d.setFlag(QGraphicsItem.ItemIsSelectable, True)
                tmp_d.setZValue(1)
                self.scene_coil.addItem(tmp_d)
                self.lst_center.insert(k_lst_center + 2, tmp_d)

                k_lst_center = k_lst_center + 2

        ### Duct horizontaux
        lst_tmp = []
        e_hd = coil_elt.firstChildElement("horizontal_ducts")
        n = e_hd.firstChildElement("duct")
        while not n.isNull():
            e_duct = n.toElement()
            d_tmp = {"t_duct": float(e_duct.firstChildElement("t_duct_m").text())*1e3, \
                     "z_center": float(e_duct.firstChildElement("z_center_m").text())*1e3}
            lst_tmp.append(d_tmp)
            n = n.nextSiblingElement("duct")
        lst_tmp = sorted(lst_tmp, key = lambda i: i['z_center'])

        # Application
        k_d = 0
        for d in self.lst_center:
            if isinstance(d, Duct) and k_d < len(lst_tmp):
                d.setSize(None, lst_tmp[k_d]["t_duct"])

                k_d = k_d + 1

class Disc(QGraphicsRectItem):
    """
    Objet graphique représentant un disque
    """

    def __init__(self, coil, parent=None):
        super().__init__(parent)

        self.coil = coil

        # Données
        # Disc construit suivant x, bool_horizontal sens des cables
        self.bool_horizontal = True
        self.h_cable = 1.0
        self.t_cable = 1.0
        self.N_cables = 1
        self.x_center = 0.0
        self.y_center = 0.0
        self.currentDescDisc = {}
        self.discNumber = 0
        self.ui_disc = None

        # Pour les résultats de calculs
        self.dict_loss = {} # key=id_calcul ; data=liste des pertes en W par cable
        self.dict_maxTR = {} # key=id_calcul ; data=max TR du disc
        self.dict_averageTR = {} # key=id_calcul ; data=average TR du disc

        # Chicanes
        self.inner_guide = False
        self.outer_guide = False
        self.inner_duct_thickness = 1.0
        self.outer_duct_thickness = 1.0

        # Crayon fin par défaut
        self.pen_defaut = QPen(Qt.black, 0.5)
        self.pen_selected = QPen(Qt.red, 0.75, Qt.DashLine)

        # Font
        self.font = QFont()

        self.pen_used = self.pen_defaut # Par défaut

    def removeLoadedCalcul(self, id_calcul=None):
        """
        Retrait d'un calcul des calculs chargés
        """
        if id_calcul == None:
            # On supprime tout
            self.dict_loss = {}
            self.dict_maxTR = {}
            self.dict_averageTR = {}
            return

        if id_calcul in self.dict_loss.keys():
            del self.dict_loss[id_calcul]
        if id_calcul in self.dict_maxTR.keys():
            del self.dict_maxTR[id_calcul]
        if id_calcul in self.dict_averageTR.keys():
            del self.dict_averageTR[id_calcul]

    def getLossCable(self, id_calcul, loss_unit="W"):
        """
        Récupération des pertes par cable du disc
        """
        if not id_calcul in self.dict_loss:
            return None

        if loss_unit == "W":
            return self.dict_loss[id_calcul]

        elif loss_unit == "W/m3":
            # Section de cuivre par cable du disc
            Sc = self.currentDescDisc['cable_origin']['N_strands']*self.currentDescDisc['cable_origin']['h_strand']*self.currentDescDisc['cable_origin']['t_strand']*1e-6

            resu = []
            for nc in range(self.N_cables):
                # Rayon du cable
                Rc = self.coil.ui_coil.getInnerRadius()*1e-3 + (nc + 0.5)*self.h_cable*1e-3
                # Volume de cuivre du cable
                Vc = Sc*2*pi*Rc

                # Enregistrement en W
                resu.append(self.dict_loss[id_calcul][nc]/Vc)

            # Renvoi en W/m3
            return resu

        else:
            raise Exception("Unite des pertes inconnue")

    def setLossCable(self, id_calcul, lst_loss, loss_unit="W"):
        """
        Définition des pertes (en W) par cable du disc
        """

        if len(lst_loss) == 0:
            # Reset des pertes
            self.dict_loss[id_calcul] = lst_loss
            return

        if len(lst_loss) != self.N_cables:
            raise Exception("Incoherence entre la liste des pertes et le nombre de cables")

        if loss_unit == "W":
            self.dict_loss[id_calcul] = lst_loss

        elif loss_unit == "W/m3":
            # Section de cuivre par cable du disc
            Sc = self.currentDescDisc['cable_origin']['N_strands']*self.currentDescDisc['cable_origin']['h_strand']*self.currentDescDisc['cable_origin']['t_strand']*1e-6

            self.dict_loss[id_calcul] = []
            for nc in range(self.N_cables):
                # Rayon du cable
                Rc = self.coil.ui_coil.getInnerRadius()*1e-3 + (nc + 0.5)*self.h_cable*1e-3
                # Volume de cuivre du cable
                Vc = Sc*2*pi*Rc

                # Enregistrement en W
                self.dict_loss[id_calcul].append(lst_loss[nc]*Vc)

        else:
            raise Exception("Unite des pertes inconnue")

    def getLossDisc(self, id_calcul, loss_unit="W"):
        """
        Récupération des pertes du disc
        """
        if not id_calcul in self.dict_loss:
            return None

        if loss_unit == "W":
            return sum(self.dict_loss[id_calcul])

        elif loss_unit == "W/m3":
            # Section de cuivre par cable du disc
            Sc = self.currentDescDisc['cable_origin']['N_strands']*self.currentDescDisc['cable_origin']['h_strand']*self.currentDescDisc['cable_origin']['t_strand']*1e-6

            # Volume de cuivre du disc
            Vc_disc = 0
            for nc in range(self.N_cables):
                # Rayon du cable
                Rc = self.coil.ui_coil.getInnerRadius()*1e-3 + (nc + 0.5)*self.h_cable*1e-3
                # Volume de cuivre
                Vc_disc = Vc_disc + Sc*2*pi*Rc

            # Renvoi en W/m3
            return sum(self.dict_loss[id_calcul])/Vc_disc

        else:
            raise Exception("Unite des pertes inconnue")

    def setLossDisc(self, id_calcul, loss_disc, loss_unit="W"):
        """
        Définition des pertes (en W) par cable uniformément sur le disc à partir de la valeur globale
        """

        # Les pertes volumiques sont uniformes sur tous les cables
        if loss_unit == "W":
            # Section de cuivre par cable du disc
            Sc = self.currentDescDisc['cable_origin']['N_strands']*self.currentDescDisc['cable_origin']['h_strand']*self.currentDescDisc['cable_origin']['t_strand']*1e-6

            # Volume de cuivre du disc
            Vc_disc = 0
            for nc in range(self.N_cables):
                # Rayon du cable
                Rc = self.coil.ui_coil.getInnerRadius()*1e-3 + (nc + 0.5)*self.h_cable*1e-3
                # Volume de cuivre
                Vc_disc = Vc_disc + Sc*2*pi*Rc

            # Pertes volumiques du disc
            loss_disc_volumic = loss_disc/Vc_disc

        elif loss_unit == "W/m3":
            loss_disc_volumic = loss_disc

        else:
            raise Exception("Unite des pertes inconnue")

        # Application
        lst_loss = [loss_disc_volumic]*self.N_cables
        self.setLossCable(id_calcul, lst_loss, "W/m3")

    def setAverageTR(self, id_calcul, aveTR):
        """
        Définition du TR moyen du disque
        """
        self.dict_averageTR[id_calcul] = aveTR

    def setMaxTemp(self, id_calcul, maxTR):
        """
        Définition du TR max du disque
        """
        self.dict_maxTR[id_calcul] = maxTR

    def setDiscNumber(self, number):
        """
        Definition du numero du disc
        """
        self.discNumber = number
        self.setToolTip("Disc n°" + "%i"%self.discNumber)

    def setDisc(self, ui_disc):
        """
        Changement du type de disque
        """
        self.ui_disc = ui_disc
        self.updateDisc()

    def updateDisc(self):
        """
        MAJ de la description du disc
        """
        desc_disc = self.ui_disc.getDisc()
        if desc_disc != {}:
            self.currentDescDisc = desc_disc
            self.setSize(self.currentDescDisc["h_cable"], self.currentDescDisc["t_cable"], self.currentDescDisc["N_cables"])
        else:
            self.currentDescDisc = {}
            self.coil.resetAll()

    def setSize(self, h_cable, t_cable, N_cables):
        self.prepareGeometryChange()
        self.h_cable = h_cable
        self.t_cable = t_cable
        self.N_cables = N_cables
        self.font.setPointSizeF(0.7*min(self.h_cable, self.t_cable))

    def setInnerGuide(self, bool_guide=None):
        """
        Placement d'une chicane à l'interieur
            True : mettre la chicane
            False : enlever la chicane
            None : inverse de la situation courante
        Il ne peut pas y avoir simultanément des chicanes à l'intérieur et à l'extérieur
        """
        if bool_guide == None:
            bool_guide = not self.inner_guide

        self.prepareGeometryChange()
        if self.outer_guide and bool_guide:
            # On retire la chicane exterieure
            self.outer_guide = False
        self.inner_guide = bool_guide

    def setOuterGuide(self, bool_guide=None):
        """
        Placement d'une chicane à l'exterieur
            True : mettre la chicane
            False : enlever la chicane
            None : inverse de la situation courante
        Il ne peut pas y avoir simultanément des chicanes à l'intérieur et à l'extérieur
        """
        if bool_guide == None:
            bool_guide = not self.outer_guide
        self.prepareGeometryChange()
        if self.inner_guide and bool_guide:
            # On retire la chicane interieure
            self.inner_guide = False
        self.outer_guide = bool_guide

    def setInnerDuctThickness(self, inner_duct_thickness):
        self.prepareGeometryChange()
        self.inner_duct_thickness = inner_duct_thickness

    def setOuterDuctThickness(self, outer_duct_thickness):
        self.prepareGeometryChange()
        self.outer_duct_thickness = outer_duct_thickness

    def setCenter(self, x_center, y_center):
        self.prepareGeometryChange()
        self.x_center = x_center
        self.y_center = y_center

    def rotate(self, bool_horizontal):
        self.prepareGeometryChange()
        self.bool_horizontal = bool_horizontal

    def getXYsize(self):
        """
        Renvoie les dimensions en X et Y en tenant compte de l'orientation
        """
        if self.bool_horizontal:
            # Cable horizontal
            return [self.N_cables*self.h_cable, self.t_cable]
        else:
            # Cable vertical
            return [self.N_cables*self.t_cable, self.h_cable]

    @property
    def height(self):
        if self.bool_horizontal:
            return self.N_cables*self.h_cable
        else:
            return self.N_cables*self.t_cable

    @property
    def thickness(self):
        if self.bool_horizontal:
            return self.t_cable
        else:
            return self.h_cable

    def boundingRect(self):
        [x_size, y_size] = self.getXYsize()

        penWidth = self.pen_used.widthF()
        tmp_graph = QRectF(self.x_center - x_size/2 - penWidth/2, self.y_center - y_size/2 - penWidth/2, x_size + penWidth, y_size + penWidth)
        if self.inner_guide:
            tmp_graph.adjust(-self.inner_duct_thickness, 0, self.inner_duct_thickness, 0)
        if self.outer_guide:
            tmp_graph.adjust(0, 0, self.outer_duct_thickness, 0)

        return tmp_graph

    def shape(self):
        # Contour de la forme
        self.path = QPainterPath()
        self.path.addRect(self.boundingRect())
        return self.path

    def paint(self, painter, option, widget=None):

        [x_size, y_size] = self.getXYsize()

        # Point de départ
        x = self.x_center - x_size/2
        y = self.y_center - y_size/2
        # Dimensions du cable
        if self.bool_horizontal:
            x_size_cable = self.h_cable
            y_size_cable = self.t_cable
        else:
            x_size_cable = self.t_cable
            y_size_cable = self.h_cable

        # Crayon
        if self.isSelected() and not self.coil.isFrozen:
            painter.setPen(self.pen_selected)
            self.pen_used = self.pen_selected
        else:
            painter.setPen(self.pen_defaut)
            self.pen_used = self.pen_defaut

        # Représentation des cables
        painter.setBrush(self.currentDescDisc["color"])
        for kk in range(self.N_cables):
            tmp_graph = QRectF(x, y, x_size_cable, y_size_cable)
            painter.drawRect(tmp_graph)
            x = x + x_size_cable

        # Numéro du disc
        tmp_graph = QRectF(self.x_center - x_size/2 + 1, self.y_center - y_size/2, x_size_cable - 1, y_size_cable)
        painter.setPen(self.pen_defaut)
        painter.setFont(self.font)
        painter.drawText(tmp_graph, Qt.AlignCenter | Qt.TextDontClip, "%i" % self.discNumber)
        painter.setPen(self.pen_used)

        # Représentation des chicanes
        if self.inner_guide:
            painter.setBrush(COLOR_oilGuide)
            tmp_graph = QRectF(self.x_center - x_size/2 - self.inner_duct_thickness, y, self.inner_duct_thickness, y_size_cable/5)
            painter.drawRect(tmp_graph)
        if self.outer_guide:
            painter.setBrush(COLOR_oilGuide)
            tmp_graph = QRectF(self.x_center + x_size/2, y, self.outer_duct_thickness, y_size_cable/5)
            painter.drawRect(tmp_graph)

    def contextMenuEvent(self, event):
        """
        Menu contextuel lors d'un clic droit
        """
        if self.coil.isFrozen: return

        # Si il n'y a personne de sélectionné, on sélectionne l'objet cliqué
        if len(self.scene().selectedItems()) == 0:
            self.setSelected(True)

        # On n'affiche le menu que si on est sélectionné
        if not self.isSelected():
            return

        # Création du menu
        menu = QMenu()

        # Infos diverses
        layout = QVBoxLayout()
        lbl = QLabel()
        lbl.setText("Disc settings")
        lbl.setStyleSheet("font-weight: bold")
        lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl)

        # Liste des discs sélectionnés
        lst_num_selected = []
        for d in self.scene().selectedItems():
            if type(d) == type(self):
                lst_num_selected.append(d.discNumber)

        lst_num_selected = sorted(lst_num_selected)
        lst_deb_fin = []
        k_deb = 0
        for k in range(1, len(lst_num_selected)):
            if lst_num_selected[k] != lst_num_selected[k-1] + 1:
                lst_deb_fin.append([lst_num_selected[k_deb], lst_num_selected[k-1]])
                k_deb = k
        lst_deb_fin.append([lst_num_selected[k_deb], lst_num_selected[-1]])

        str_d = "Disc(s) selected n°"
        first = True
        for df in lst_deb_fin:
            if df[0] == df[1]:
                if first:
                    str_d = str_d + "%i"%df[0]
                    first = False
                else:
                    str_d = str_d + ";%i"%df[0]
            else:
                if first:
                    str_d = str_d + "%i-%i"%(df[0], df[1])
                    first = False
                else:
                    str_d = str_d + ";%i-%i"%(df[0], df[1])

        lbl = QLabel()
        lbl.setText(str_d)
        lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl)

        wdg = QWidget()
        wdg.setLayout(layout)
        a = QWidgetAction(menu)
        a.setDefaultWidget(wdg)
        menu.addAction(a)

        menu.addSeparator()

        # Changement du disque
        sub_chgDisc = menu.addMenu("Change disc")
        for k in range(len(self.coil.lst_ui_disc)):
            desc = self.coil.lst_ui_disc[k].getDisc()
            if desc != {}:
                act = sub_chgDisc.addAction(desc["name"])
                act.triggered.connect(partial(self.coil.actChangeDisc, self.coil.lst_ui_disc[k], type(self)))
                act.triggered.connect(self.coil.isModified.emit)
        # Chicanes
        sub_chgDisc = menu.addMenu("Oil guide")
        act = sub_chgDisc.addAction("Inner")
        act.triggered.connect(partial(self.coil.actOilGuide, "inner", type(self)))
        act.triggered.connect(self.coil.isModified.emit)
        act = sub_chgDisc.addAction("Outer")
        act.triggered.connect(partial(self.coil.actOilGuide, "outer", type(self)))
        act.triggered.connect(self.coil.isModified.emit)
        if self.inner_guide or self.outer_guide:
            act = sub_chgDisc.addAction("Remove")
            act.triggered.connect(partial(self.coil.actOilGuide, "remove", type(self)))
            act.triggered.connect(self.coil.isModified.emit)
        # Ajout d'un carton
        sub_pressboard = menu.addMenu("Pressboard")
        act = sub_pressboard.addAction("Insert above")
        act.triggered.connect(partial(self.coil.actInsertPressboard, "above", type(self)))
        act.triggered.connect(self.coil.isModified.emit)
        act = sub_pressboard.addAction("Insert under")
        act.triggered.connect(partial(self.coil.actInsertPressboard, "under", type(self)))
        act.triggered.connect(self.coil.isModified.emit)

        # Changement de la couleur
        act = menu.addAction("Color")
        act.triggered.connect(partial(self.coil.actColorDisc, self.ui_disc))

        # Exécution
        menu.exec_(event.screenPos())

class Duct(QGraphicsRectItem):
    """
    Objet graphique représentant un canal
    """

    def __init__(self, coil, parent=None):
        super().__init__(parent)

        self.coil = coil

        # Données (par défaut, x=height ; y=thickness)
        self.bool_horizontal = True
        self.height = 1.0
        self.thickness = 1.0
        self.x_center = 0.0
        self.y_center = 0.0

        # Pour les résultats de calculs
        self.dict_averageVelocity = {} # key=id_calcul ; data=average velocity du duct
        self.dict_averageTR = {} # key=id_calcul ; data=average TR du duct

        # Crayon fin par défaut
        self.pen_defaut = QPen(Qt.NoPen)
        self.pen_defaut.setWidth(0.)
        self.pen_selected = QPen(Qt.red, 0.75, Qt.DashLine)

        self.pen_used = self.pen_defaut # Par défaut

    def removeLoadedCalcul(self, id_calcul=None):
        """
        Retrait d'un calcul des calculs chargés
        """
        if id_calcul == None:
            # On supprime tout
            self.dict_averageVelocity = {}
            self.dict_averageTR = {}
            return

        if id_calcul in self.dict_averageVelocity.keys():
            del self.dict_averageVelocity[id_calcul]
        if id_calcul in self.dict_averageTR.keys():
            del self.dict_averageTR[id_calcul]

    def setAverageTR(self, id_calcul, aveTR):
        """
        Définition du TR moyen du duct
        """
        self.dict_averageTR[id_calcul] = aveTR

    def setAverageVelocity(self, id_calcul, aveVelo):
        """
        Définition de la vitesse moyenne du duct
        """
        self.dict_averageVelocity[id_calcul] = aveVelo

    def setSize(self, height, thickness):
        if height != None:
            self.height = height
        if thickness != None:
            self.thickness = thickness

    def setCenter(self, x_center, y_center):
        self.prepareGeometryChange()
        self.x_center = x_center
        self.y_center = y_center

    def rotate(self, bool_horizontal):
        self.prepareGeometryChange()
        self.bool_horizontal = bool_horizontal

    def getXYsize(self):
        """
        Renvoie les dimensions en X et Y en tenant compte de l'orientation
        """
        if self.bool_horizontal:
            # Cable horizontal
            return [self.height, self.thickness]
        else:
            # Cable vertical
            return [self.thickness, self.height]

    def boundingRect(self):
        [x_size, y_size] = self.getXYsize()

        penWidth = self.pen_used.widthF()
        tmp_graph = QRectF(self.x_center - x_size/2 - penWidth/2, self.y_center - y_size/2 - penWidth/2, x_size + penWidth, y_size + penWidth)

        return tmp_graph

    def shape(self):
        # Contour de la forme
        self.path = QPainterPath()
        self.path.addRect(self.boundingRect())
        return self.path

    def paint(self, painter, option, widget=None):

        [x_size, y_size] = self.getXYsize()

        # Point de départ
        x = self.x_center - x_size/2
        y = self.y_center - y_size/2

        # Crayon
        if self.isSelected() and not self.coil.isFrozen:
            painter.setPen(self.pen_selected)
            self.pen_used = self.pen_selected
        else:
            painter.setPen(self.pen_defaut)
            self.pen_used = self.pen_defaut

        # Mode de représentation simple
        tmp_graph = QRectF(x, y, x_size, y_size)
        painter.setBrush(self.coil.getColorDuctThickness(self.thickness))
        painter.drawRect(tmp_graph)

    def contextMenuEvent(self, event):
        """
        Menu contextuel lors d'un clic droit
        """
        if self.coil.isFrozen: return

        # Si il n'y a personne de sélectionné, on sélectionne l'objet cliqué
        if len(self.scene().selectedItems()) == 0:
            self.setSelected(True)

        # On n'affiche le menu que si on est sélectionné
        if not self.isSelected():
            return

        # Création du menu
        menu = QMenu()

        # Infos diverses
        lbl = QLabel()
        lbl.setText("Duct settings")
        lbl.setStyleSheet("font-weight: bold")
        lbl.setAlignment(Qt.AlignCenter)
        a = QWidgetAction(menu)
        a.setDefaultWidget(lbl)
        menu.addAction(a)

        menu.addSeparator()

        # Changement de l'épaisseur du canal
        locale = QLocale("en")
        locale.setNumberOptions(QLocale.RejectGroupSeparator)
        validator_float = QDoubleValidator(1.0, 100.0, 3)
        validator_float.setNotation(QDoubleValidator.StandardNotation) # Pas de notation scientifique
        validator_float.setLocale(locale)

        layout = QHBoxLayout()
        lbl = QLabel()
        lbl.setText("Thickness")
        layout.addWidget(lbl)

        le = gui_utils.QLineEditFormat()
        le.setDisplayFormat("%.2f")
        le.setValidator(validator_float)
        le.setText(self.thickness)
        layout.addWidget(le)

        lbl = QLabel()
        lbl.setText("mm")
        layout.addWidget(lbl)

        wdg = QWidget()
        wdg.setLayout(layout)
        a = QWidgetAction(menu)
        a.setDefaultWidget(wdg)
        menu.addAction(a)

        # Changement de la couleur
        act = menu.addAction("Color")
        act.triggered.connect(partial(self.coil.actColorDuct, self))
        act.triggered.connect(self.coil.isModified.emit)

        # Connection
        le.editingFinished.connect(partial(self.coil.actChangeThickness, le, type(self)))
        le.editingFinished.connect(self.coil.isModified.emit)
        le.editingFinished.connect(menu.close)

        # Exécution
        menu.exec_(event.screenPos())

class Pressboard(QGraphicsRectItem):
    """
    Objet graphique représentant un carton
    """

    def __init__(self, coil, parent=None):
        super().__init__(parent)

        self.coil = coil

        # Données (par défaut, x=height ; y=thickness)
        self.bool_horizontal = True
        self.height = 1.0
        self.thickness = 1.0
        self.x_center = 0.0
        self.y_center = 0.0

        # Chicanes
        self.inner_guide = False
        self.outer_guide = False
        self.inner_duct_thickness = 1.0
        self.outer_duct_thickness = 1.0

        # Pour les résultats de calculs
        self.dict_maxTR = {} # key=id_calcul ; data=max TR du disc
        self.dict_averageTR = {} # key=id_calcul ; data=average TR du disc

        # Crayon fin par défaut
        self.pen_defaut = QPen(Qt.black, 0.5)
        self.pen_selected = QPen(Qt.red, 0.75, Qt.DashLine)

        self.pen_used = self.pen_defaut # Par défaut
        self.setToolTip("Pressboard")

    def removeLoadedCalcul(self, id_calcul=None):
        """
        Retrait d'un calcul des calculs chargés
        """
        if id_calcul == None:
            # On supprime tout
            self.dict_maxTR = {}
            self.dict_averageTR = {}
            return

        if id_calcul in self.dict_maxTR.keys():
            del self.dict_maxTR[id_calcul]
        if id_calcul in self.dict_averageTR.keys():
            del self.dict_averageTR[id_calcul]

    def setAverageTR(self, id_calcul, aveTR):
        """
        Définition du TR moyen du disque
        """
        self.dict_averageTR[id_calcul] = aveTR

    def setMaxTemp(self, id_calcul, maxTR):
        """
        Définition du TR max du disque
        """
        self.dict_maxTR[id_calcul] = maxTR

    def setSize(self, height, thickness):
        self.prepareGeometryChange()
        if height != None:
            self.height = height
        if thickness != None:
            self.thickness = thickness

    def setInnerGuide(self, bool_guide=None):
        """
        Placement d'une chicane à l'interieur
            True : mettre la chicane
            False : enlever la chicane
            None : inverse de la situation courante
        Il ne peut pas y avoir simultanément des chicanes à l'intérieur et à l'extérieur
        """
        if bool_guide == None:
            bool_guide = not self.inner_guide

        self.prepareGeometryChange()
        if self.outer_guide and bool_guide:
            # On retire la chicane exterieure
            self.outer_guide = False
        self.inner_guide = bool_guide

    def setOuterGuide(self, bool_guide=None):
        """
        Placement d'une chicane à l'exterieur
            True : mettre la chicane
            False : enlever la chicane
            None : inverse de la situation courante
        Il ne peut pas y avoir simultanément des chicanes à l'intérieur et à l'extérieur
        """
        if bool_guide == None:
            bool_guide = not self.outer_guide
        self.prepareGeometryChange()
        if self.inner_guide and bool_guide:
            # On retire la chicane interieure
            self.inner_guide = False
        self.outer_guide = bool_guide

    def setInnerDuctThickness(self, inner_duct_thickness):
        self.prepareGeometryChange()
        self.inner_duct_thickness = inner_duct_thickness

    def setOuterDuctThickness(self, outer_duct_thickness):
        self.prepareGeometryChange()
        self.outer_duct_thickness = outer_duct_thickness

    def setCenter(self, x_center, y_center):
        self.prepareGeometryChange()
        self.x_center = x_center
        self.y_center = y_center

    def getXYsize(self):
        """
        Renvoie les dimensions en X et Y en tenant compte de l'orientation
        """
        if self.bool_horizontal:
            # Cable horizontal
            return [self.height, self.thickness]
        else:
            # Cable vertical
            return [self.thickness, self.height]

    def boundingRect(self):
        [x_size, y_size] = self.getXYsize()

        penWidth = self.pen_used.widthF()
        tmp_graph = QRectF(self.x_center - x_size/2 - penWidth/2, self.y_center - y_size/2 - penWidth/2, x_size + penWidth, y_size + penWidth)
        if self.inner_guide:
            tmp_graph.adjust(-self.inner_duct_thickness, 0, self.inner_duct_thickness, 0)
        if self.outer_guide:
            tmp_graph.adjust(0, 0, self.outer_duct_thickness, 0)

        return tmp_graph

    def shape(self):
        # Contour de la forme
        self.path = QPainterPath()
        self.path.addRect(self.boundingRect())
        return self.path

    def paint(self, painter, option, widget=None):

        [x_size, y_size] = self.getXYsize()

        # Point de départ
        x = self.x_center - x_size/2
        y = self.y_center - y_size/2

        # Crayon
        if self.isSelected() and not self.coil.isFrozen:
            painter.setPen(self.pen_selected)
            self.pen_used = self.pen_selected
        else:
            painter.setPen(self.pen_defaut)
            self.pen_used = self.pen_defaut

        # Carton
        tmp_graph = QRectF(x, y, x_size, y_size)
        painter.setBrush(self.coil.getColorPressboardThickness(self.thickness))
        painter.drawRect(tmp_graph)

        # Représentation des chicanes
        if self.inner_guide:
            painter.setBrush(COLOR_oilGuide)
            tmp_graph = QRectF(self.x_center - x_size/2 - self.inner_duct_thickness, y, self.inner_duct_thickness, y_size/5)
            painter.drawRect(tmp_graph)
        if self.outer_guide:
            painter.setBrush(COLOR_oilGuide)
            tmp_graph = QRectF(self.x_center + x_size/2, y, self.outer_duct_thickness, y_size/5)
            painter.drawRect(tmp_graph)

    def contextMenuEvent(self, event):
        """
        Menu contextuel lors d'un clic droit
        """
        if self.coil.isFrozen: return

        # Si il n'y a personne de sélectionné, on sélectionne l'objet cliqué
        if len(self.scene().selectedItems()) == 0:
            self.setSelected(True)

        # On n'affiche le menu que si on est sélectionné
        if not self.isSelected():
            return

        # Création du menu
        menu = QMenu()

        # Infos diverses
        lbl = QLabel()
        lbl.setText("Pressboard settings")
        lbl.setStyleSheet("font-weight: bold")
        lbl.setAlignment(Qt.AlignCenter)
        a = QWidgetAction(menu)
        a.setDefaultWidget(lbl)
        menu.addAction(a)

        menu.addSeparator()

        # Changement de l'épaisseur du canal
        locale = QLocale("en")
        locale.setNumberOptions(QLocale.RejectGroupSeparator)
        validator_float = QDoubleValidator(1.0, 100.0, 3)
        validator_float.setNotation(QDoubleValidator.StandardNotation) # Pas de notation scientifique
        validator_float.setLocale(locale)

        layout = QHBoxLayout()
        lbl = QLabel()
        lbl.setText("Thickness")
        layout.addWidget(lbl)

        le = gui_utils.QLineEditFormat()
        le.setDisplayFormat("%.2f")
        le.setValidator(validator_float)
        le.setText(self.thickness)
        layout.addWidget(le)

        lbl = QLabel()
        lbl.setText("mm")
        layout.addWidget(lbl)

        wdg = QWidget()
        wdg.setLayout(layout)
        a = QWidgetAction(menu)
        a.setDefaultWidget(wdg)
        menu.addAction(a)

        # Chicanes
        sub_chgDisc = menu.addMenu("Oil guide")
        act = sub_chgDisc.addAction("Inner")
        act.triggered.connect(partial(self.coil.actOilGuide, "inner", type(self)))
        act.triggered.connect(self.coil.isModified.emit)
        act = sub_chgDisc.addAction("Outer")
        act.triggered.connect(partial(self.coil.actOilGuide, "outer", type(self)))
        act.triggered.connect(self.coil.isModified.emit)
        if self.inner_guide or self.outer_guide:
            act = sub_chgDisc.addAction("Remove")
            act.triggered.connect(partial(self.coil.actOilGuide, "remove", type(self)))
            act.triggered.connect(self.coil.isModified.emit)

        # Changement de la couleur
        act = menu.addAction("Color")
        act.triggered.connect(partial(self.coil.actColorPressboard, self))

        # Pour la suppression du carton
        menu.addSeparator()
        act = menu.addAction("Remove pressboard")
        act.triggered.connect(partial(self.coil.actRemove, type(self)))
        act.triggered.connect(self.coil.isModified.emit)

        # Connection
        le.editingFinished.connect(partial(self.coil.actChangeThickness, le, type(self)))
        le.editingFinished.connect(self.coil.isModified.emit)
        le.editingFinished.connect(menu.close)

        # Exécution
        menu.exec_(event.screenPos())

class Legend(QGraphicsRectItem):
    """
    Objet graphique représentant la légende
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Données
        self.H_lgd = 15.0
        self.L_lgd = 5*self.H_lgd
        self.margin = 5.0
        self.dico_lgd = {}
        self.origin = [0, 0]

        # Crayon fin par défaut
        self.pen_defaut = QPen(Qt.black, 0.5)
        self.pen_selected = QPen(Qt.red, 0.75, Qt.DashLine)

        self.pen_used = self.pen_defaut # Par défaut

    def setLegend(self, dico_lgd):
        self.prepareGeometryChange()
        self.dico_lgd = dico_lgd
        height = (self.H_lgd + self.margin)*len(self.dico_lgd.keys())
        width = 4*self.L_lgd + self.margin
        self.scene().setSceneRect(QRectF(self.origin[0], self.origin[1], width, height))

    def boundingRect(self):
        penWidth = self.pen_used.widthF()
        tmp_graph = QRectF(self.origin[0] - penWidth/2, self.origin[1] - penWidth/2, 4*self.L_lgd + self.margin + penWidth, (self.H_lgd + self.margin)*len(self.dico_lgd.keys()) + penWidth)

        return tmp_graph

    def shape(self):
        # Contour de la forme
        self.path = QPainterPath()
        self.path.addRect(self.boundingRect())
        return self.path

    def paint(self, painter, option, widget=None):

        # Crayon
        painter.setPen(self.pen_defaut)
        self.pen_used = self.pen_defaut

        x = self.origin[0]
        y = self.origin[1]

        for l in sorted(self.dico_lgd.keys()):
            # Rectangle
            tmp_graph = QRectF(x, y, self.L_lgd, self.H_lgd)
            painter.setBrush(self.dico_lgd[l][1])
            painter.drawRect(tmp_graph)
            # Texte
            painter.setRenderHint(QPainter.TextAntialiasing, True)
            tmp_graph = QRectF(x + self.L_lgd + self.margin, y, 3*self.L_lgd, self.H_lgd)
            if self.dico_lgd[l][0] > 0:
                painter.drawText(tmp_graph, Qt.AlignLeft, l + " (" + str(self.dico_lgd[l][0]) + ")")
            else:
                painter.drawText(tmp_graph, Qt.AlignLeft, l)
            painter.setRenderHint(QPainter.TextAntialiasing, False)

            x = x
            y = y + self.H_lgd + self.margin

class Arrow(QGraphicsLineItem):
    """
    Objet graphique représentant un fleche
    Largement inspiré de https://doc.qt.io/qt-5/qtwidgets-graphicsview-diagramscene-example.html
    """

    def __init__(self, x1, y1, x2, y2, arrowSize, parent=None):
        super().__init__(parent)

        self.arrowHead = QPolygonF()
        self.arrowSize = arrowSize # Taille de la tête

        # Point de départ [x1, y1]
        self.x1 = x1
        self.y1 = y1
        # Point d'arrivée [x2, y2] avec une flèche
        self.x2 = x2
        self.y2 = y2

        self.myColor = Qt.black

    def setColor(self, color):
        self.myColor = color

    def boundingRect(self):
        extra = (self.pen().width() + 20) / 2.0
        p1 = self.line().p1()
        p2 = self.line().p2()
        return QRectF(p1, QSizeF(p2.x() - p1.x(), p2.y() - p1.y())).normalized().adjusted(-extra, -extra, extra, extra)

    def shape(self):
        path = super().shape()
        path.addPolygon(self.arrowHead)
        return path

    def updatePosition(self):
        line = QLineF(self.x1, self.y1, self.x2, self.y2)
        self.setLine(line)

    def paint(self, painter, option, widget=None):

        painter.setBrush(self.myColor)

        self.setLine(QLineF(QPointF(self.x2, self.y2), QPointF(self.x1, self.y1)))
        line = self.line()

        angle = acos(line.dx() / line.length())
        if line.dy() >= 0:
            angle = (pi * 2.0) - angle

        arrowP1 = line.p1() + QPointF(sin(angle + pi / 3.0) * self.arrowSize,
                                        cos(angle + pi / 3) * self.arrowSize)
        arrowP2 = line.p1() + QPointF(sin(angle + pi - pi / 3.0) * self.arrowSize,
                                        cos(angle + pi - pi / 3.0) * self.arrowSize)

        self.arrowHead.clear()
        for point in [line.p1(), arrowP1, arrowP2]:
            self.arrowHead.append(point)

        painter.drawLine(line)
        painter.drawPolygon(self.arrowHead)

class Winding(QGraphicsObject):
    """
    Objet graphique représentant un winding
    """

    # Signal quand l'enroulement est sélectionné
    selectionChanged = Signal(bool)

    def __init__(self, H_wind, L_coil, shape_winding="simple", winding_dir=None, parent=None):
        super().__init__(parent)

        # Données
        self.lst_pos_center = array([[0, 0, True]]) # [x, y, side]
        self.set_H_wind(H_wind)
        self.L_coil = L_coil
        self.shape_winding = shape_winding
        self.winding_dir = winding_dir

        self.arrowSize = self.L_coil/2.
        self.arrowLength = self.L_coil*3/2
        self.arrowLength1 = self.arrowLength/2
        self.arrowLength2 = L_coil/5

        # Crayon fin par défaut
        self.pen_defaut = QPen(Qt.black, 0.5)
        self.pen_selected = QPen(Qt.red, 3.0, Qt.DashLine)
        self.pen_used = self.pen_defaut # Par défaut

        # Couleur non définie par défaut
        self.myColor = COLOR_undefined

        # Contour de l'enroulement
        self.path = QPainterPath()

    def itemChange(self, change, value):

        if change == QGraphicsItem.ItemSelectedChange:
            self.selectionChanged.emit(value)

        return value

    def set_H_wind(self, H_wind):
        self.H_wind = H_wind
        self.prepareGeometryChange()

    def set_lst_pos_center(self, lst_pos_center):
        self.lst_pos_center = array(lst_pos_center)
        self.prepareGeometryChange()

    def getShapeWinding(self):
        return self.shape_winding

    def setShapeWinding(self, shape_winding):
        self.shape_winding = shape_winding
        self.prepareGeometryChange()

    def setWindingDirection(self, winding_dir):
        self.winding_dir = winding_dir
        self.prepareGeometryChange()

    def getWindingDirection(self):
        return self.winding_dir

    def getCoilRectF(self):

        if self.getShapeWinding() == "simple":
            tmp_rect = QRectF(- self.L_coil/2, - self.H_wind/2, self.L_coil, self.H_wind)

        elif self.getShapeWinding() == "classic":
            tmp_rect = QRectF(- self.L_coil/2, - self.H_wind/2 - self.arrowLength, self.L_coil, self.H_wind + 2*self.arrowLength)

        elif self.getShapeWinding() == "double-classic":
            tmp_rect = QRectF(- 5*self.L_coil/4, - self.H_wind/2 - self.arrowLength, 5*self.L_coil/2, self.H_wind + self.arrowLength + self.arrowLength1)

        elif self.getShapeWinding() == "middle-entry":
            tmp_rect = QRectF(- self.L_coil/2 - self.arrowLength1 - self.arrowSize/2, - self.H_wind/2 - self.arrowLength, self.L_coil + 2*self.arrowLength1 + self.arrowSize/2, self.H_wind + 2*self.arrowLength)

        elif self.getShapeWinding() == "one-axial-split":
            tmp_rect = QRectF(- 6*self.L_coil/4, - self.H_wind/2 - self.arrowLength - 3*self.arrowLength2/2, 6*self.L_coil/2, self.H_wind + self.arrowLength + self.arrowLength1 + 3*self.arrowLength2)

        elif self.getShapeWinding() == "two-axial-split-top" or self.getShapeWinding() == "two-axial-split-bottom":
            # Hauteur complète pour calcul taille fenetre CM & largeur divisée par 2
            tmp_rect = QRectF(- 5*self.L_coil/4, - self.H_wind - self.arrowLength - 3*self.arrowLength2/2, 5*self.L_coil/2, 2*self.H_wind + 2*self.arrowLength + 3*self.arrowLength2)

        elif self.getShapeWinding() == "fine-coarse":
            tmp_rect = QRectF(- 2*self.L_coil, - self.H_wind/2 - self.arrowLength, 4*self.L_coil, self.H_wind + 2*self.arrowLength)

        elif self.getShapeWinding() == "shell-simple-classic-in" or self.getShapeWinding() == "shell-simple-classic-out":
            tmp_rect = QRectF(- 3*self.L_coil, - self.H_wind/2 - self.arrowLength, 6*self.L_coil, self.H_wind + self.arrowLength + self.arrowLength1)

        elif self.getShapeWinding() in ["shell-simple-diabolo-in", "shell-simple-diabolo-out", "shell-double-diabolo-in", "shell-double-diabolo-left", "shell-double-diabolo-right"]:
            tmp_rect = QRectF(- 6*self.L_coil - self.arrowSize/2, - self.H_wind/2 - self.arrowLength, 12*self.L_coil + self.arrowSize/2, self.H_wind + self.arrowLength + self.arrowLength1)

        elif self.getShapeWinding() in ["shell-double-classic-in", "shell-double-classic-out", "shell-double-classic-right"]:
            tmp_rect = QRectF(- 5*self.L_coil, - self.H_wind/2 - self.arrowLength, 10*self.L_coil, self.H_wind + self.arrowLength + self.arrowLength1)

        elif self.getShapeWinding() in ["shell-triple-classic-in", "shell-triple-classic-out", "shell-triple-classic-left", "shell-triple-classic-right"]:
            tmp_rect = QRectF(- 7*self.L_coil, - self.H_wind/2 - self.arrowLength, 14*self.L_coil, self.H_wind + self.arrowLength + self.arrowLength1)

        elif self.getShapeWinding() in ["shell-simple-barrel-in", "shell-simple-barrel-out", "shell-double-barrel-in", "shell-double-barrel-left", "shell-double-barrel-right"]:
            tmp_rect = QRectF(- 6*self.L_coil, - self.H_wind/2 - self.arrowLength, 12*self.L_coil, self.H_wind + 2*self.arrowLength)

        else:
            raise Exception("Shape du winding non reconnue: %s"%self.getShapeWinding())

        return tmp_rect

    def boundingRect(self):
        x_min = min(self.lst_pos_center[:,0])
        x_max = max(self.lst_pos_center[:,0])
        y_min = min(self.lst_pos_center[:,1])
        y_max = max(self.lst_pos_center[:,1])
        penWidth = self.pen_used.widthF()

        if self.getShapeWinding() == "simple":
            rect_wind = QRectF(x_min - self.L_coil/2 - penWidth/2,
                               y_min - self.H_wind/2 - penWidth/2,
                               x_max - x_min + self.L_coil + penWidth,
                               y_max - y_min + self.H_wind + penWidth)

        elif self.getShapeWinding() == "classic":
            rect_wind = QRectF(x_min - self.L_coil/2 - penWidth/2,
                               y_min - self.H_wind/2  - self.arrowLength - penWidth/2,
                               x_max - x_min + self.L_coil + penWidth,
                               y_max - y_min + self.H_wind + penWidth + 2*self.arrowLength)

        elif self.getShapeWinding() == "double-classic":
            rect_wind = QRectF(x_min - 5*self.L_coil/4 - penWidth/2,
                               y_min - self.H_wind/2  - self.arrowLength - penWidth/2,
                               x_max - x_min + 5*self.L_coil/2 + penWidth,
                               y_max - y_min + self.H_wind + penWidth + self.arrowLength + self.arrowLength1)

        elif self.getShapeWinding() == "fine-coarse":
            rect_wind = QRectF(x_min - 2*self.L_coil - penWidth/2,
                               y_min - self.H_wind/2  - self.arrowLength - penWidth/2,
                               x_max - x_min + 4*self.L_coil + penWidth,
                               y_max - y_min + self.H_wind + penWidth + 2*self.arrowLength)

        elif self.getShapeWinding() == "middle-entry":
            rect_wind = QRectF(x_min - self.L_coil/2 - self.arrowLength1 - self.arrowSize/2 - penWidth/2,
                               y_min - self.H_wind/2  - self.arrowLength - penWidth/2,
                               x_max - x_min + self.L_coil + 2*self.arrowLength1 + self.arrowSize/2 + penWidth,
                               y_max - y_min + self.H_wind + penWidth + 2*self.arrowLength)

        elif self.getShapeWinding() == "one-axial-split":
            rect_wind = QRectF(x_min - 6*self.L_coil/4 - penWidth/2,
                               y_min - self.H_wind/2  - self.arrowLength - 3*self.arrowLength2/2 - penWidth/2,
                               x_max - x_min + 6*self.L_coil/2 + penWidth,
                               y_max - y_min + self.H_wind + penWidth + self.arrowLength + self.arrowLength1 + 3*self.arrowLength2)

        elif self.getShapeWinding() == "two-axial-split-top":
            rect_wind = QRectF(x_min - 5*self.L_coil/4 - penWidth/2,
                               y_min - self.H_wind  - self.arrowLength - penWidth/2,
                               x_max - x_min + 5*self.L_coil/2 + penWidth,
                               y_max - y_min + 2*self.H_wind + penWidth + self.arrowLength + self.arrowLength2)

        elif self.getShapeWinding() == "two-axial-split-bottom":
            rect_wind = QRectF(x_min - 5*self.L_coil/4 - penWidth/2,
                               y_min - self.H_wind  - self.arrowLength2/2 - penWidth/2,
                               x_max - x_min + 5*self.L_coil/2 + penWidth,
                               y_max - y_min + 2*self.H_wind + penWidth + self.arrowLength + self.arrowLength2)

        elif self.getShapeWinding() == "shell-simple-classic-in":
            rect_wind = QRectF(x_min - self.L_coil - penWidth/2,
                               y_min - self.H_wind/2 - self.arrowLength - penWidth/2,
                               x_max - x_min + 2*self.L_coil + penWidth,
                               y_max - y_min + self.H_wind + self.arrowLength + penWidth)

        elif self.getShapeWinding() == "shell-simple-classic-out":
            rect_wind = QRectF(x_min - 3*self.L_coil - penWidth/2,
                               y_min - self.H_wind/2 - self.arrowLength - penWidth/2,
                               x_max - x_min + 6*self.L_coil + penWidth,
                               y_max - y_min + self.H_wind + self.arrowLength + self.arrowLength1 + penWidth)

        elif self.getShapeWinding() == "shell-simple-diabolo-in" or self.getShapeWinding() == "shell-double-diabolo-in":
            rect_wind = QRectF(x_min - 6*self.L_coil - penWidth/2 - self.arrowSize/2,
                               y_min - self.H_wind/2 - self.arrowLength - penWidth/2,
                               x_max - x_min + 12*self.L_coil + penWidth + self.arrowSize/2,
                               y_max - y_min + self.H_wind + self.arrowLength + penWidth)

        elif self.getShapeWinding() == "shell-simple-diabolo-out":
            rect_wind = QRectF(x_min - 4*self.L_coil - penWidth/2,
                               y_min - self.H_wind/2 - penWidth/2,
                               x_max - x_min + 8*self.L_coil + penWidth,
                               y_max - y_min + self.H_wind + self.arrowLength + penWidth)

        elif self.getShapeWinding() == "shell-double-diabolo-left":
            rect_wind = QRectF(x_min - 4*self.L_coil - penWidth/2,
                               y_min - self.H_wind/2 - penWidth/2,
                               x_max - x_min + self.L_coil + penWidth,
                               y_max - y_min + self.H_wind + self.arrowLength + penWidth)

        elif self.getShapeWinding() == "shell-double-diabolo-right":
            rect_wind = QRectF(x_min + 3*self.L_coil - penWidth/2,
                               y_min - self.H_wind/2 - penWidth/2,
                               x_max - x_min + self.L_coil + penWidth,
                               y_max - y_min + self.H_wind + self.arrowLength + penWidth)

        elif self.getShapeWinding() == "shell-double-classic-in":
            rect_wind = QRectF(x_min - 7*self.L_coil/2 - penWidth/2,
                               y_min - self.H_wind/2 - self.arrowLength - penWidth/2,
                               x_max - x_min + 7*self.L_coil + penWidth,
                               y_max - y_min + self.H_wind + self.arrowLength + penWidth)

        elif self.getShapeWinding() == "shell-double-classic-out":
            rect_wind = QRectF(x_min - 5*self.L_coil - penWidth/2,
                               y_min - self.H_wind/2 - self.arrowLength - penWidth/2,
                               x_max - x_min + 10*self.L_coil + penWidth,
                               y_max - y_min + self.H_wind + self.arrowLength + self.arrowLength1 + penWidth)

        elif self.getShapeWinding() == "shell-double-classic-right":
            rect_wind = QRectF(x_min - self.L_coil/2 - penWidth/2,
                               y_min - self.H_wind/2 - penWidth/2,
                               x_max - x_min + self.L_coil + penWidth,
                               y_max - y_min + self.H_wind + self.arrowLength + penWidth)

        elif self.getShapeWinding() == "shell-triple-classic-in":
            rect_wind = QRectF(x_min - 11*self.L_coil/2 - penWidth/2,
                               y_min - self.H_wind/2 - self.arrowLength - penWidth/2,
                               x_max - x_min + 11*self.L_coil + penWidth,
                               y_max - y_min + self.H_wind + self.arrowLength + penWidth)

        elif self.getShapeWinding() == "shell-triple-classic-out":
            rect_wind = QRectF(x_min - 7*self.L_coil - penWidth/2,
                               y_min - self.H_wind/2 - self.arrowLength - penWidth/2,
                               x_max - x_min + 14*self.L_coil + penWidth,
                               y_max - y_min + self.H_wind + self.arrowLength + self.arrowLength1 + penWidth)

        elif self.getShapeWinding() == "shell-triple-classic-left":
            rect_wind = QRectF(x_min - 5*self.L_coil/2 - penWidth/2,
                               y_min - self.H_wind/2 - penWidth/2,
                               x_max - x_min + self.L_coil + penWidth,
                               y_max - y_min + self.H_wind + self.arrowLength + penWidth)

        elif self.getShapeWinding() == "shell-triple-classic-right":
            rect_wind = QRectF(x_min + 5*self.L_coil/2 - penWidth/2,
                               y_min - self.H_wind/2 - penWidth/2,
                               x_max - x_min + self.L_coil + penWidth,
                               y_max - y_min + self.H_wind + self.arrowLength + penWidth)

        elif self.getShapeWinding() in ["shell-simple-barrel-in", "shell-double-barrel-in"]:
            rect_wind = QRectF(x_min - 4*self.L_coil - penWidth/2,
                               y_min - self.H_wind/2 - self.arrowLength - penWidth/2,
                               x_max - x_min + 8*self.L_coil + penWidth,
                               y_max - y_min + self.H_wind + self.arrowLength + penWidth)

        elif self.getShapeWinding() == "shell-simple-barrel-out":
            rect_wind = QRectF(x_min - 6*self.L_coil - penWidth/2,
                               y_min - self.H_wind/2 - penWidth/2,
                               x_max - x_min + 12*self.L_coil + penWidth,
                               y_max - y_min + self.H_wind + self.arrowLength + penWidth)

        elif self.getShapeWinding() == "shell-double-barrel-left":
            rect_wind = QRectF(x_min - 6*self.L_coil - penWidth/2,
                               y_min - self.H_wind/2 - penWidth/2,
                               x_max - x_min + 6*self.L_coil + penWidth,
                               y_max - y_min + self.H_wind + self.arrowLength + penWidth)

        elif self.getShapeWinding() == "shell-double-barrel-right":
            rect_wind = QRectF(x_min - penWidth/2,
                               y_min - self.H_wind/2 - penWidth/2,
                               x_max - x_min + 6*self.L_coil + penWidth,
                               y_max - y_min + self.H_wind + self.arrowLength + penWidth)

        else:
            raise Exception("Shape du winding non reconnue: %s"%self.getShapeWinding())

        return rect_wind

    def shape(self):
        # Contour de la forme
        return self.path

    def paint(self, painter, option, widget=None):

        # Reset du contour
        self.path = QPainterPath()

        # Crayon fin en tirets lorsque sélectionné
        if self.isSelected():
            painter.setPen(self.pen_selected)
            self.pen_used = self.pen_selected
        else:
            painter.setPen(self.pen_defaut)
            self.pen_used = self.pen_defaut

        for pos in self.lst_pos_center:
            self.plot_coil(painter, pos[0], pos[1], pos[2], option, widget)

    def plot_coil(self, painter, x_center, y_center, side, option, widget):
        """
        Fonction de dessin d'une bobine:
            - x_center ; y_center : les coordonnées de son centre
            - side : côté de la représentation de la bobine /° colonne (bool) -> pour respecter la symétrie (non nécessaire à toutes les shapes)
        """

        # Couleurs
        if self.getWindingDirection() == True:
            color_1 = COLOR_positive
            color_2 = COLOR_negative
        elif self.getWindingDirection() == False:
            color_2 = COLOR_positive
            color_1 = COLOR_negative
        else:
            # Cas None
            color_2 = COLOR_undefined
            color_1 = COLOR_undefined

        # Traitement
        if self.getShapeWinding() == "simple":

            # Rectangle
            tmp_rect = QRectF(x_center - self.L_coil/2, y_center - self.H_wind/2, self.L_coil, self.H_wind)
            painter.setBrush(color_1)
            painter.drawRect(tmp_rect)
            self.path.addRect(tmp_rect)

        elif self.getShapeWinding() == "classic":

            # Rectangle
            tmp_graph = QRectF(x_center - self.L_coil/2, y_center - self.H_wind/2, self.L_coil, self.H_wind)
            painter.setBrush(color_1)
            painter.drawRect(tmp_graph)

            if side: # Connexions que du côté x+
                # Flèche 1
                tmp_graph = Arrow(x_center, y_center - self.H_wind/2 - self.arrowLength, x_center, y_center - self.H_wind/2, self.arrowSize)
                tmp_graph.paint(painter, option, widget)

                # Flèche 2
                tmp_graph = Arrow(x_center, y_center + self.H_wind/2, x_center, y_center + self.H_wind/2 + self.arrowLength, self.arrowSize)
                tmp_graph.paint(painter, option, widget)

            tmp_rect = QRectF(x_center - self.L_coil/2, y_center - self.H_wind/2 - self.arrowLength, self.L_coil, self.H_wind + 2*self.arrowLength)
            self.path.addRect(tmp_rect)

        elif self.getShapeWinding() == "double-classic":

            if side:
                color_in = color_1
                color_out = color_2
            else:
                color_in = color_2
                color_out = color_1

            # Rectangles
            tmp_graph = QRectF(x_center - 5*self.L_coil/4, y_center - self.H_wind/2, self.L_coil, self.H_wind)
            painter.setBrush(color_in)
            painter.drawRect(tmp_graph)
            tmp_graph = QRectF(x_center + self.L_coil/4, y_center - self.H_wind/2, self.L_coil, self.H_wind)
            painter.setBrush(color_out)
            painter.drawRect(tmp_graph)

            if side: # Connexions que du côté x+
                # Flèche 1
                tmp_graph = Arrow(x_center - 3*self.L_coil/4, y_center - self.H_wind/2 - self.arrowLength, x_center - 3*self.L_coil/4, y_center - self.H_wind/2, self.arrowSize)
                tmp_graph.paint(painter, option, widget)

                # lignes
                tmp_graph = QLineF(x_center - 3*self.L_coil/4, y_center + self.H_wind/2, x_center - 3*self.L_coil/4, y_center + self.H_wind/2 + self.arrowLength1)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center + 3*self.L_coil/4, y_center + self.H_wind/2 + self.arrowLength1, x_center - 3*self.L_coil/4, y_center + self.H_wind/2 + self.arrowLength1)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center + 3*self.L_coil/4, y_center + self.H_wind/2 + self.arrowLength1, x_center + 3*self.L_coil/4, y_center + self.H_wind/2)
                painter.drawLine(tmp_graph)

                # Flèche 2
                tmp_graph = Arrow(x_center + 3*self.L_coil/4, y_center - self.H_wind/2, x_center + 3*self.L_coil/4, y_center - self.H_wind/2 - self.arrowLength, self.arrowSize)
                tmp_graph.paint(painter, option, widget)

            tmp_rect = QRectF(x_center - 5*self.L_coil/4, y_center - self.H_wind/2 - self.arrowLength, 5*self.L_coil/2, self.H_wind + self.arrowLength + self.arrowLength1)
            self.path.addRect(tmp_rect)

        elif self.getShapeWinding() == "fine-coarse":

            if side:
                color_in = color_1
                color_out = color_2
            else:
                color_in = color_2
                color_out = color_1

            # Rectangles
            tmp_graph = QRectF(x_center - 2*self.L_coil, y_center - self.H_wind/2, self.L_coil, self.H_wind)
            painter.setBrush(color_in)
            painter.drawRect(tmp_graph)
            tmp_graph = QRectF(x_center - self.L_coil/2, y_center - self.H_wind/2, self.L_coil, self.H_wind)
            painter.setBrush(color_out)
            painter.drawRect(tmp_graph)
            tmp_graph = QRectF(x_center + self.L_coil, y_center - self.H_wind/2, self.L_coil, self.H_wind)
            painter.setBrush(color_in)
            painter.drawRect(tmp_graph)

            if side: # Connexions que du côté x+
                # Flèche 1
                tmp_graph = Arrow(x_center - 3*self.L_coil/2, y_center - self.H_wind/2 - self.arrowLength, x_center - 3*self.L_coil/2, y_center - self.H_wind/2, self.arrowSize)
                tmp_graph.paint(painter, option, widget)

                # Lignes + inter
                tmp_graph = QLineF(x_center - 3*self.L_coil/2, y_center + self.H_wind/2, x_center - 3*self.L_coil/2, y_center + self.H_wind/2 + 3*self.arrowLength1/4)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center - 3*self.L_coil/2, y_center + self.H_wind/2 + 3*self.arrowLength1/4, x_center - self.L_coil, y_center + self.H_wind/2 + 3*self.arrowLength1/4)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center, y_center + self.H_wind/2, x_center, y_center + self.H_wind/2 + self.arrowLength1/2)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center - self.L_coil/2, y_center + self.H_wind/2 + self.arrowLength1/2, x_center, y_center + self.H_wind/2 + self.arrowLength1/2)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center - self.L_coil/2, y_center + self.H_wind/2 + self.arrowLength1, x_center + 3*self.L_coil/4, y_center + self.H_wind/2 + self.arrowLength1)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center + 3*self.L_coil/4, y_center + self.H_wind/2 + self.arrowLength1, x_center + 3*self.L_coil/4, y_center - self.H_wind/2 - self.arrowLength1)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center - self.L_coil, y_center + self.H_wind/2 + 3*self.arrowLength1/4, x_center - self.L_coil/2, y_center + self.H_wind/2 + self.arrowLength1/2)
                painter.drawLine(tmp_graph)

                # Lignes + regroupement
                tmp_graph = QLineF(x_center, y_center - self.H_wind/2, x_center, y_center - self.H_wind/2 - self.arrowLength1)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center, y_center - self.H_wind/2 - self.arrowLength1, x_center + 3*self.L_coil/2, y_center - self.H_wind/2 - self.arrowLength1)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center + 3*self.L_coil/2, y_center - self.H_wind/2 - self.arrowLength1, x_center + 3*self.L_coil/2, y_center - self.H_wind/2)
                painter.drawLine(tmp_graph)

                # Flèche 2
                tmp_graph = Arrow(x_center + 3*self.L_coil/2, y_center + self.H_wind/2, x_center + 3*self.L_coil/2, y_center + self.H_wind/2 + self.arrowLength, self.arrowSize)
                tmp_graph.paint(painter, option, widget)

            tmp_rect = QRectF(x_center - 5*self.L_coil/4, y_center - self.H_wind/2 - self.arrowLength, 5*self.L_coil/2, self.H_wind + self.arrowLength + self.arrowLength1)
            self.path.addRect(tmp_rect)

        elif self.getShapeWinding() == "middle-entry":

            # Rectangle 1
            tmp_graph = QRectF(x_center - self.L_coil/2, y_center - self.H_wind/2, self.L_coil, self.H_wind/2)
            painter.setBrush(color_1)
            painter.drawRect(tmp_graph)

            # Rectangle 2
            tmp_graph = QRectF(x_center - self.L_coil/2, y_center, self.L_coil, self.H_wind/2)
            painter.setBrush(color_2)
            painter.drawRect(tmp_graph)

            if side: # Connexions que du côté x+
                # Entrée
                tmp_graph = QLineF(x_center + self.L_coil/2 + self.arrowLength1, y_center - self.H_wind/2 - self.arrowLength, x_center + self.L_coil/2 + self.arrowLength1, y_center)
                painter.drawLine(tmp_graph)
                tmp_graph = Arrow(x_center + self.L_coil/2 + self.arrowLength1, y_center, x_center + self.L_coil/2, y_center, self.arrowSize)
                tmp_graph.paint(painter, option, widget)

                # Sortie
                tmp_graph = QLineF(x_center, y_center - self.H_wind/2, x_center, y_center - self.H_wind/2 - self.arrowLength1)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center, y_center - self.H_wind/2 - self.arrowLength1, x_center - (self.L_coil/2 + self.arrowLength1), y_center - self.H_wind/2 - self.arrowLength1)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center, y_center + self.H_wind/2, x_center, y_center + self.H_wind/2 + self.arrowLength1)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center, y_center + self.H_wind/2 + self.arrowLength1, x_center - (self.L_coil/2 + self.arrowLength1), y_center + self.H_wind/2 + self.arrowLength1)
                painter.drawLine(tmp_graph)
                tmp_graph = Arrow(x_center - (self.L_coil/2 + self.arrowLength1), y_center - self.H_wind/2 - self.arrowLength1, x_center - (self.L_coil/2 + self.arrowLength1), y_center + self.H_wind/2 + self.arrowLength, self.arrowSize)
                tmp_graph.paint(painter, option, widget)

            if side:
                tmp_rect = QRectF(x_center - self.L_coil/2 - self.arrowLength1 - 2*self.arrowSize/4, y_center - self.H_wind/2 - self.arrowLength, self.L_coil + 2*self.arrowLength1 + self.arrowSize/2, self.H_wind + 2*self.arrowLength)
            else:
                tmp_rect = QRectF(x_center - self.L_coil/2 - self.arrowLength1, y_center - self.H_wind/2 - self.arrowLength, self.L_coil + 2*self.arrowLength1 + self.arrowSize/2, self.H_wind + 2*self.arrowLength)
            self.path.addRect(tmp_rect)

        elif self.getShapeWinding() == "one-axial-split":

            if side:
                color_in_haut = color_1
                color_in_bas = color_2
                color_out_haut = color_2
                color_out_bas = color_1
            else:
                color_in_haut = color_2
                color_in_bas = color_1
                color_out_haut = color_1
                color_out_bas = color_2

            # En raison de l'espace entre les 2 parties, on modifie la hauteur de l'enroulement pour le dessin
            H_wind_bis = self.H_wind - 3*self.arrowLength2

            ### Haut
            # Rectangles
            tmp_graph = QRectF(x_center - 5*self.L_coil/4, y_center - H_wind_bis/2 - 3*self.arrowLength2/2, self.L_coil, H_wind_bis/2)
            painter.setBrush(color_in_haut)
            painter.drawRect(tmp_graph)
            tmp_graph = QRectF(x_center + self.L_coil/4, y_center - H_wind_bis/2 - 3*self.arrowLength2/2, self.L_coil, H_wind_bis/2)
            painter.setBrush(color_out_haut)
            painter.drawRect(tmp_graph)

            if side: # Connexions que du côté x+
                # Flèches et lignes
                tmp_graph = Arrow(x_center - 3*self.L_coil/4, y_center - H_wind_bis/2 - self.arrowLength - 3*self.arrowLength2/2, x_center - 3*self.L_coil/4, y_center - H_wind_bis/2 - 3*self.arrowLength2/2, self.arrowSize)
                tmp_graph.paint(painter, option, widget)
                tmp_graph = QLineF(x_center - 3*self.L_coil/4, y_center - 3*self.arrowLength2/2, x_center - 3*self.L_coil/4, y_center - self.arrowLength2/2)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center + 3*self.L_coil/4, y_center - self.arrowLength2/2, x_center - 3*self.L_coil/4, y_center - self.arrowLength2/2)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center + 3*self.L_coil/4, y_center - self.arrowLength2/2, x_center + 3*self.L_coil/4, y_center - 3*self.arrowLength2/2)
                painter.drawLine(tmp_graph)
                tmp_graph = Arrow(x_center + 3*self.L_coil/4, y_center - H_wind_bis/2 - 3*self.arrowLength2/2, x_center + 3*self.L_coil/4, y_center - H_wind_bis/2 - self.arrowLength - 3*self.arrowLength2/2, self.arrowSize)
                tmp_graph.paint(painter, option, widget)

            ### Bas
            # Rectangles
            tmp_graph = QRectF(x_center - 5*self.L_coil/4, y_center + 3*self.arrowLength2/2, self.L_coil, H_wind_bis/2)
            painter.setBrush(color_in_bas)
            painter.drawRect(tmp_graph)
            tmp_graph = QRectF(x_center + self.L_coil/4, y_center + 3*self.arrowLength2/2, self.L_coil, H_wind_bis/2)
            painter.setBrush(color_out_bas)
            painter.drawRect(tmp_graph)

            if side: # Connexions que du côté x+
                # Lignes
                tmp_graph = QLineF(x_center - 3*self.L_coil/4, y_center + H_wind_bis/2 + self.arrowLength1 + 3*self.arrowLength2/2, x_center - 3*self.L_coil/4, y_center + H_wind_bis/2 + 3*self.arrowLength2/2)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center - 3*self.L_coil/4, y_center + 3*self.arrowLength2/2, x_center - 3*self.L_coil/4, y_center + self.arrowLength2/2)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center + 3*self.L_coil/4, y_center + self.arrowLength2/2, x_center - 3*self.L_coil/4, y_center + self.arrowLength2/2)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center + 3*self.L_coil/4, y_center + self.arrowLength2/2, x_center + 3*self.L_coil/4, y_center + 3*self.arrowLength2/2)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center + 3*self.L_coil/4, y_center + H_wind_bis/2 + 3*self.arrowLength2/2, x_center + 3*self.L_coil/4, y_center + H_wind_bis/2 + self.arrowLength1 + 3*self.arrowLength2/2)
                painter.drawLine(tmp_graph)

            ### Autres lignes
            if side: # Connexions que du côté x+
                # Lignes
                tmp_graph = QLineF(x_center - 3*self.L_coil/4, y_center + H_wind_bis/2 + self.arrowLength1 + 3*self.arrowLength2/2, x_center - 6*self.L_coil/4, y_center + H_wind_bis/2 + self.arrowLength1 + 3*self.arrowLength2/2)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center + 3*self.L_coil/4, y_center + H_wind_bis/2 + self.arrowLength1 + 3*self.arrowLength2/2, x_center + 6*self.L_coil/4, y_center + H_wind_bis/2 + self.arrowLength1 + 3*self.arrowLength2/2)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center - 6*self.L_coil/4, y_center + H_wind_bis/2 + self.arrowLength1 + 3*self.arrowLength2/2, x_center - 6*self.L_coil/4, y_center - H_wind_bis/2 - self.arrowLength1 - 3*self.arrowLength2/2)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center + 6*self.L_coil/4, y_center + H_wind_bis/2 + self.arrowLength1 + 3*self.arrowLength2/2, x_center + 6*self.L_coil/4, y_center - H_wind_bis/2 - self.arrowLength1 - 3*self.arrowLength2/2)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center - 3*self.L_coil/4, y_center - H_wind_bis/2 - self.arrowLength1 - 3*self.arrowLength2/2, x_center - 6*self.L_coil/4, y_center - H_wind_bis/2 - self.arrowLength1 - 3*self.arrowLength2/2)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center + 3*self.L_coil/4, y_center - H_wind_bis/2 - self.arrowLength1 - 3*self.arrowLength2/2, x_center + 6*self.L_coil/4, y_center - H_wind_bis/2 - self.arrowLength1 - 3*self.arrowLength2/2)
                painter.drawLine(tmp_graph)

            tmp_rect = QRectF(x_center - 6*self.L_coil/4, y_center - H_wind_bis/2 - self.arrowLength - 3*self.arrowLength2/2, 6*self.L_coil/2, H_wind_bis + self.arrowLength + self.arrowLength1 + 3*self.arrowLength2)
            self.path.addRect(tmp_rect)

        elif self.getShapeWinding() == "two-axial-split-top":

            if side:
                color_in_haut = color_1
                color_out_haut = color_2
            else:
                color_in_haut = color_2
                color_out_haut = color_1

            y_center = y_center - 3*self.arrowLength2/4 - self.H_wind/2

            # En raison de l'espace entre les 2 parties, on modifie la hauteur de l'enroulement pour le dessin
            H_wind_bis = self.H_wind - 3*self.arrowLength2/2

            ### Haut
            # Rectangles
            tmp_graph = QRectF(x_center - 5*self.L_coil/4, y_center - H_wind_bis/2, self.L_coil, H_wind_bis)
            painter.setBrush(color_in_haut)
            painter.drawRect(tmp_graph)
            tmp_graph = QRectF(x_center + self.L_coil/4, y_center - H_wind_bis/2, self.L_coil, H_wind_bis)
            painter.setBrush(color_out_haut)
            painter.drawRect(tmp_graph)

            if side: # Connexions que du côté x+
                # Flèches et lignes
                tmp_graph = Arrow(x_center - 3*self.L_coil/4, y_center - H_wind_bis/2 - self.arrowLength, x_center - 3*self.L_coil/4, y_center - H_wind_bis/2, self.arrowSize)
                tmp_graph.paint(painter, option, widget)
                tmp_graph = QLineF(x_center - 3*self.L_coil/4, y_center + H_wind_bis/2, x_center - 3*self.L_coil/4, y_center + H_wind_bis/2 + self.arrowLength2)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center + 3*self.L_coil/4, y_center + H_wind_bis/2 + self.arrowLength2, x_center - 3*self.L_coil/4, y_center + H_wind_bis/2 + self.arrowLength2)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center + 3*self.L_coil/4, y_center + H_wind_bis/2 + self.arrowLength2, x_center + 3*self.L_coil/4, y_center + H_wind_bis/2)
                painter.drawLine(tmp_graph)
                tmp_graph = Arrow(x_center + 3*self.L_coil/4, y_center - H_wind_bis/2, x_center + 3*self.L_coil/4, y_center - H_wind_bis/2 - self.arrowLength, self.arrowSize)
                tmp_graph.paint(painter, option, widget)

            tmp_rect = QRectF(x_center - 5*self.L_coil/4, y_center - H_wind_bis/2 - self.arrowLength, 5*self.L_coil/2, H_wind_bis + self.arrowLength + self.arrowLength2)
            self.path.addRect(tmp_rect)

        elif self.getShapeWinding() == "two-axial-split-bottom":

            if side:
                color_in_bas = color_2
                color_out_bas = color_1
            else:
                color_in_bas = color_1
                color_out_bas = color_2

            y_center = y_center + 3*self.arrowLength2/4 + self.H_wind/2

            # En raison de l'espace entre les 2 parties, on modifie la hauteur de l'enroulement pour le dessin
            H_wind_bis = self.H_wind - 3*self.arrowLength2/2

            ### Bas
            # Rectangles
            tmp_graph = QRectF(x_center - 5*self.L_coil/4, y_center - H_wind_bis/2, self.L_coil, H_wind_bis)
            painter.setBrush(color_in_bas)
            painter.drawRect(tmp_graph)
            tmp_graph = QRectF(x_center + self.L_coil/4, y_center - H_wind_bis/2, self.L_coil, H_wind_bis)
            painter.setBrush(color_out_bas)
            painter.drawRect(tmp_graph)

            if side: # Connexions que du côté x+
                # Flèches et lignes
                tmp_graph = Arrow(x_center - 3*self.L_coil/4, y_center + H_wind_bis/2 + self.arrowLength, x_center - 3*self.L_coil/4, y_center + H_wind_bis/2, self.arrowSize)
                tmp_graph.paint(painter, option, widget)
                tmp_graph = QLineF(x_center - 3*self.L_coil/4, y_center - H_wind_bis/2, x_center - 3*self.L_coil/4, y_center - H_wind_bis/2 - self.arrowLength2)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center + 3*self.L_coil/4, y_center - H_wind_bis/2 - self.arrowLength2, x_center - 3*self.L_coil/4, y_center - H_wind_bis/2 - self.arrowLength2)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center + 3*self.L_coil/4, y_center - H_wind_bis/2 - self.arrowLength2, x_center + 3*self.L_coil/4, y_center - H_wind_bis/2)
                painter.drawLine(tmp_graph)
                tmp_graph = Arrow(x_center + 3*self.L_coil/4, y_center + H_wind_bis/2, x_center + 3*self.L_coil/4, y_center + H_wind_bis/2 + self.arrowLength, self.arrowSize)
                tmp_graph.paint(painter, option, widget)

            tmp_rect = QRectF(x_center - 5*self.L_coil/4, y_center - H_wind_bis/2 - self.arrowLength2, 5*self.L_coil/2, H_wind_bis + self.arrowLength + self.arrowLength2)
            self.path.addRect(tmp_rect)

        elif self.getShapeWinding() == "shell-simple-classic-in":

            # Polygone
            tmp_graph = QPolygonF([QPointF(x_center - self.L_coil, y_center + self.L_coil), QPointF(x_center - self.L_coil, y_center - self.L_coil), QPointF(x_center + self.L_coil, y_center - self.H_wind/2), QPointF(x_center + self.L_coil, y_center + self.H_wind/2)])
            painter.setBrush(color_1)
            painter.drawPolygon(tmp_graph)

            if side: # Connexions que du côté x+
                # Flèches et lignes
                tmp_graph = Arrow(x_center - self.L_coil, y_center - self.H_wind/2 - self.arrowLength, x_center - self.L_coil, y_center - self.L_coil, self.arrowSize)
                tmp_graph.paint(painter, option, widget)
                tmp_graph = Arrow(x_center + self.L_coil, y_center - self.H_wind/2, x_center + self.L_coil, y_center - self.H_wind/2 - self.arrowLength, self.arrowSize)
                tmp_graph.paint(painter, option, widget)

            tmp_rect = QRectF(x_center - self.L_coil, y_center - self.H_wind/2 - self.arrowLength, 2*self.L_coil, self.H_wind + self.arrowLength)
            self.path.addRect(tmp_rect)

        elif self.getShapeWinding() == "shell-simple-classic-out":

            # Rectangles
            tmp_graph = QRectF(x_center - 3*self.L_coil, y_center - self.H_wind/2, self.L_coil, self.H_wind)
            painter.setBrush(color_2)
            painter.drawRect(tmp_graph)
            tmp_graph = QRectF(x_center + 2*self.L_coil, y_center - self.H_wind/2, self.L_coil, self.H_wind)
            painter.setBrush(color_2)
            painter.drawRect(tmp_graph)

            if side: # Connexions que du côté x+
                # Flèches et lignes
                tmp_graph = Arrow(x_center - 2*self.L_coil, y_center - self.H_wind/2 - self.arrowLength, x_center - 2*self.L_coil, y_center - self.H_wind/2, self.arrowSize)
                tmp_graph.paint(painter, option, widget)
                tmp_graph = Arrow(x_center + 2*self.L_coil, y_center - self.H_wind/2, x_center + 2*self.L_coil, y_center - self.H_wind/2 - self.arrowLength, self.arrowSize)
                tmp_graph.paint(painter, option, widget)

                tmp_graph = QLineF(x_center - 3*self.L_coil, y_center + self.H_wind/2, x_center - 3*self.L_coil, y_center + self.H_wind/2 + self.arrowLength1)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center - 3*self.L_coil, y_center + self.H_wind/2 + self.arrowLength1, x_center + 3*self.L_coil, y_center + self.H_wind/2 + self.arrowLength1)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center + 3*self.L_coil, y_center + self.H_wind/2 + self.arrowLength1, x_center + 3*self.L_coil, y_center + self.H_wind/2)
                painter.drawLine(tmp_graph)

            tmp_rect = QRectF(x_center - 3*self.L_coil, y_center - self.H_wind/2 - self.arrowLength, self.L_coil, self.H_wind + self.arrowLength + self.arrowLength1)
            self.path.addRect(tmp_rect)
            tmp_rect = QRectF(x_center + 2*self.L_coil, y_center - self.H_wind/2 - self.arrowLength, self.L_coil, self.H_wind + self.arrowLength + self.arrowLength1)
            self.path.addRect(tmp_rect)

        elif self.getShapeWinding() == "shell-simple-diabolo-in" or self.getShapeWinding() == "shell-double-diabolo-in":

            # Polygones
            tmp_graph = QPolygonF([QPointF(x_center, y_center + self.L_coil), QPointF(x_center, y_center - self.L_coil), QPointF(x_center + 2*self.L_coil, y_center - self.H_wind/2), QPointF(x_center + 2*self.L_coil, y_center + self.H_wind/2)])
            painter.setBrush(color_1)
            painter.drawPolygon(tmp_graph)
            tmp_graph = QPolygonF([QPointF(x_center, y_center + self.L_coil), QPointF(x_center, y_center - self.L_coil), QPointF(x_center - 2*self.L_coil, y_center - self.H_wind/2), QPointF(x_center - 2*self.L_coil, y_center + self.H_wind/2)])
            painter.setBrush(color_2)
            painter.drawPolygon(tmp_graph)

            # Rectangles
            tmp_graph = QRectF(x_center + 5*self.L_coil, y_center - self.H_wind/2, self.L_coil, self.H_wind)
            painter.setBrush(color_1)
            painter.drawRect(tmp_graph)
            tmp_graph = QRectF(x_center - 6*self.L_coil, y_center - self.H_wind/2, self.L_coil, self.H_wind)
            painter.setBrush(color_2)
            painter.drawRect(tmp_graph)

            if side: # Connexions que du côté x+
                # Flèches et lignes
                tmp_graph = Arrow(x_center, y_center - self.H_wind/2 - self.arrowLength, x_center, y_center - self.L_coil, self.arrowSize)
                tmp_graph.paint(painter, option, widget)
                tmp_graph = Arrow(x_center - 6*self.L_coil, y_center - self.H_wind/2, x_center - 6*self.L_coil, y_center - self.H_wind/2 - self.arrowLength, self.arrowSize)
                tmp_graph.paint(painter, option, widget)

                tmp_graph = QLineF(x_center + 2*self.L_coil, y_center - self.H_wind/2, x_center + 2*self.L_coil, y_center - self.H_wind/2 - self.arrowLength1/2)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center + 2*self.L_coil, y_center - self.H_wind/2 - self.arrowLength1/2, x_center + 5*self.L_coil, y_center - self.H_wind/2 - self.arrowLength1/2)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center + 5*self.L_coil, y_center - self.H_wind/2 - self.arrowLength1/2, x_center + 5*self.L_coil, y_center - self.H_wind/2)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center - 2*self.L_coil, y_center - self.H_wind/2, x_center - 2*self.L_coil, y_center - self.H_wind/2 - self.arrowLength1/2)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center - 2*self.L_coil, y_center - self.H_wind/2 - self.arrowLength1/2, x_center - 5*self.L_coil, y_center - self.H_wind/2 - self.arrowLength1/2)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center - 5*self.L_coil, y_center - self.H_wind/2 - self.arrowLength1/2, x_center - 5*self.L_coil, y_center - self.H_wind/2)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center + 6*self.L_coil, y_center - self.H_wind/2, x_center + 6*self.L_coil, y_center - self.H_wind/2 - self.arrowLength1)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center + 6*self.L_coil, y_center - self.H_wind/2 - self.arrowLength1, x_center - 6*self.L_coil, y_center - self.H_wind/2 - self.arrowLength1)
                painter.drawLine(tmp_graph)

            tmp_rect = QRectF(x_center - 2*self.L_coil, y_center - self.H_wind/2 - self.arrowLength, 4*self.L_coil, self.H_wind + self.arrowLength)
            self.path.addRect(tmp_rect)
            tmp_rect = QRectF(x_center - 6*self.L_coil, y_center - self.H_wind/2 - self.arrowLength, self.L_coil, self.H_wind + self.arrowLength)
            self.path.addRect(tmp_rect)
            tmp_rect = QRectF(x_center + 5*self.L_coil, y_center - self.H_wind/2 - self.arrowLength, self.L_coil, self.H_wind + self.arrowLength)
            self.path.addRect(tmp_rect)

        elif self.getShapeWinding() == "shell-simple-diabolo-out":

            # Rectangles
            tmp_graph = QRectF(x_center + 3*self.L_coil, y_center - self.H_wind/2, self.L_coil, self.H_wind)
            painter.setBrush(color_2)
            painter.drawRect(tmp_graph)
            tmp_graph = QRectF(x_center - 4*self.L_coil, y_center - self.H_wind/2, self.L_coil, self.H_wind)
            painter.setBrush(color_1)
            painter.drawRect(tmp_graph)

            if side: # Connexions que du côté x+
                # Flèches et lignes
                tmp_graph = Arrow(x_center - 4*self.L_coil, y_center + self.H_wind/2 + self.arrowLength, x_center - 4*self.L_coil, y_center + self.H_wind/2, self.arrowSize)
                tmp_graph.paint(painter, option, widget)
                tmp_graph = Arrow(x_center - 3*self.L_coil, y_center + self.H_wind/2, x_center - 3*self.L_coil, y_center + self.H_wind/2 + self.arrowLength, self.arrowSize)
                tmp_graph.paint(painter, option, widget)

                tmp_graph = QLineF(x_center - 4*self.L_coil, y_center + self.H_wind/2 + self.arrowLength1, x_center + 4*self.L_coil, y_center + self.H_wind/2 + self.arrowLength1)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center + 4*self.L_coil, y_center + self.H_wind/2 + self.arrowLength1, x_center + 4*self.L_coil, y_center + self.H_wind/2)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center - 3*self.L_coil, y_center + self.H_wind/2 + self.arrowLength1/2, x_center + 3*self.L_coil, y_center + self.H_wind/2 + self.arrowLength1/2)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center + 3*self.L_coil, y_center + self.H_wind/2 + self.arrowLength1/2, x_center + 3*self.L_coil, y_center + self.H_wind/2)
                painter.drawLine(tmp_graph)

            tmp_rect = QRectF(x_center - 4*self.L_coil, y_center - self.H_wind/2, self.L_coil, self.H_wind + self.arrowLength)
            self.path.addRect(tmp_rect)
            tmp_rect = QRectF(x_center + 3*self.L_coil, y_center - self.H_wind/2, self.L_coil, self.H_wind + self.arrowLength)
            self.path.addRect(tmp_rect)

        elif self.getShapeWinding() == "shell-double-diabolo-left":

            # Rectangles
            tmp_graph = QRectF(x_center - 4*self.L_coil, y_center - self.H_wind/2, self.L_coil, self.H_wind)
            painter.setBrush(color_1)
            painter.drawRect(tmp_graph)

            if side: # Connexions que du côté x+
                # Flèches et lignes
                tmp_graph = Arrow(x_center - 4*self.L_coil, y_center + self.H_wind/2 + self.arrowLength, x_center - 4*self.L_coil, y_center + self.H_wind/2, self.arrowSize)
                tmp_graph.paint(painter, option, widget)
                tmp_graph = Arrow(x_center - 3*self.L_coil, y_center + self.H_wind/2, x_center - 3*self.L_coil, y_center + self.H_wind/2 + self.arrowLength, self.arrowSize)
                tmp_graph.paint(painter, option, widget)

            tmp_rect = QRectF(x_center - 4*self.L_coil, y_center - self.H_wind/2, self.L_coil, self.H_wind + self.arrowLength)
            self.path.addRect(tmp_rect)

        elif self.getShapeWinding() == "shell-double-diabolo-right":

            # Rectangles
            tmp_graph = QRectF(x_center + 3*self.L_coil, y_center - self.H_wind/2, self.L_coil, self.H_wind)
            painter.setBrush(color_2)
            painter.drawRect(tmp_graph)

            if side: # Connexions que du côté x+
                # Flèches et lignes
                tmp_graph = Arrow(x_center + 4*self.L_coil, y_center + self.H_wind/2 + self.arrowLength, x_center + 4*self.L_coil, y_center + self.H_wind/2, self.arrowSize)
                tmp_graph.paint(painter, option, widget)
                tmp_graph = Arrow(x_center + 3*self.L_coil, y_center + self.H_wind/2, x_center + 3*self.L_coil, y_center + self.H_wind/2 + self.arrowLength, self.arrowSize)
                tmp_graph.paint(painter, option, widget)

            tmp_rect = QRectF(x_center + 3*self.L_coil, y_center - self.H_wind/2, self.L_coil, self.H_wind + self.arrowLength)
            self.path.addRect(tmp_rect)

        elif self.getShapeWinding() == "shell-double-classic-in":

            # Polygone
            tmp_graph = QPolygonF([QPointF(x_center - 7*self.L_coil/2, y_center + self.L_coil), QPointF(x_center - 7*self.L_coil/2, y_center - self.L_coil), QPointF(x_center - 3*self.L_coil/2, y_center - self.H_wind/2), QPointF(x_center - 3*self.L_coil/2, y_center + self.H_wind/2)])
            painter.setBrush(color_1)
            painter.drawPolygon(tmp_graph)
            # Rectangle
            tmp_graph = QRectF(x_center + 3*self.L_coil/2, y_center - self.H_wind/2, 2*self.L_coil, self.H_wind)
            painter.setBrush(color_1)
            painter.drawRect(tmp_graph)

            if side: # Connexions que du côté x+
                # Flèches et lignes
                tmp_graph = Arrow(x_center - 7*self.L_coil/2, y_center - self.H_wind/2 - self.arrowLength, x_center - 7*self.L_coil/2, y_center - self.L_coil, self.arrowSize)
                tmp_graph.paint(painter, option, widget)
                tmp_graph = Arrow(x_center + 7*self.L_coil/2, y_center - self.H_wind/2, x_center + 7*self.L_coil/2, y_center - self.H_wind/2 - self.arrowLength, self.arrowSize)
                tmp_graph.paint(painter, option, widget)

                tmp_graph = QLineF(x_center - 3*self.L_coil/2, y_center - self.H_wind/2, x_center - 3*self.L_coil/2, y_center - self.H_wind/2 - self.arrowLength1)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center - 3*self.L_coil/2, y_center - self.H_wind/2 - self.arrowLength1, x_center + 3*self.L_coil/2, y_center - self.H_wind/2 - self.arrowLength1)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center + 3*self.L_coil/2, y_center - self.H_wind/2 - self.arrowLength1, x_center + 3*self.L_coil/2, y_center - self.H_wind/2)
                painter.drawLine(tmp_graph)

            tmp_rect = QRectF(x_center - 7*self.L_coil/2, y_center - self.H_wind/2 - self.arrowLength, 2*self.L_coil, self.H_wind + self.arrowLength)
            self.path.addRect(tmp_rect)
            tmp_rect = QRectF(x_center + 3*self.L_coil/2, y_center - self.H_wind/2 - self.arrowLength, 2*self.L_coil, self.H_wind + self.arrowLength)
            self.path.addRect(tmp_rect)

        elif self.getShapeWinding() == "shell-double-classic-out":

            # Rectangles
            tmp_graph = QRectF(x_center - 5*self.L_coil, y_center - self.H_wind/2, self.L_coil/2, self.H_wind)
            painter.setBrush(color_2)
            painter.drawRect(tmp_graph)
            tmp_graph = QRectF(x_center + 9*self.L_coil/2, y_center - self.H_wind/2, self.L_coil/2, self.H_wind)
            painter.setBrush(color_2)
            painter.drawRect(tmp_graph)

            if side: # Connexions que du côté x+
                # Flèches et lignes
                tmp_graph = Arrow(x_center - 9*self.L_coil/2, y_center - self.H_wind/2 - self.arrowLength, x_center - 9*self.L_coil/2, y_center - self.H_wind/2, self.arrowSize)
                tmp_graph.paint(painter, option, widget)
                tmp_graph = Arrow(x_center + 9*self.L_coil/2, y_center - self.H_wind/2, x_center + 9*self.L_coil/2, y_center - self.H_wind/2 - self.arrowLength, self.arrowSize)
                tmp_graph.paint(painter, option, widget)

                tmp_graph = QLineF(x_center - 5*self.L_coil, y_center + self.H_wind/2, x_center - 5*self.L_coil, y_center + self.H_wind/2 + self.arrowLength1)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center - 5*self.L_coil, y_center + self.H_wind/2 + self.arrowLength1, x_center + 5*self.L_coil, y_center + self.H_wind/2 + self.arrowLength1)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center + 5*self.L_coil, y_center + self.H_wind/2 + self.arrowLength1, x_center + 5*self.L_coil, y_center + self.H_wind/2)
                painter.drawLine(tmp_graph)

            tmp_rect = QRectF(x_center - 5*self.L_coil, y_center - self.H_wind/2 - self.arrowLength, self.L_coil/2, self.H_wind + self.arrowLength + self.arrowLength1)
            self.path.addRect(tmp_rect)
            tmp_rect = QRectF(x_center + 9*self.L_coil/2, y_center - self.H_wind/2 - self.arrowLength, self.L_coil/2, self.H_wind + self.arrowLength + self.arrowLength1)
            self.path.addRect(tmp_rect)

        elif self.getShapeWinding() == "shell-double-classic-right":

            # Rectangle
            tmp_graph = QRectF(x_center - self.L_coil/2, y_center - self.H_wind/2, self.L_coil, self.H_wind)
            painter.setBrush(color_2)
            painter.drawRect(tmp_graph)

            if side: # Connexions que du côté x+
                # Flèches et lignes
                tmp_graph = Arrow(x_center - self.L_coil/2, y_center + self.H_wind/2, x_center - self.L_coil/2, y_center + self.H_wind/2 + self.arrowLength, self.arrowSize)
                tmp_graph.paint(painter, option, widget)
                tmp_graph = Arrow(x_center + self.L_coil/2, y_center + self.H_wind/2 + self.arrowLength, x_center + self.L_coil/2, y_center + self.H_wind/2, self.arrowSize)
                tmp_graph.paint(painter, option, widget)

            tmp_rect = QRectF(x_center - self.L_coil/2, y_center - self.H_wind/2, self.L_coil, self.H_wind + self.arrowLength)
            self.path.addRect(tmp_rect)

        elif self.getShapeWinding() == "shell-triple-classic-in":

            # Polygones
            tmp_graph = QPolygonF([QPointF(x_center - 11*self.L_coil/2, y_center + self.L_coil), QPointF(x_center - 11*self.L_coil/2, y_center - self.L_coil), QPointF(x_center - 7*self.L_coil/2, y_center - self.H_wind/2), QPointF(x_center - 7*self.L_coil/2, y_center + self.H_wind/2)])
            painter.setBrush(color_1)
            painter.drawPolygon(tmp_graph)
            tmp_graph = QPolygonF([QPointF(x_center + 9*self.L_coil/2, y_center + self.H_wind/2), QPointF(x_center + 9*self.L_coil/2, y_center - self.H_wind/2), QPointF(x_center + 11*self.L_coil/2, y_center - self.L_coil), QPointF(x_center + 11*self.L_coil/2, y_center + self.L_coil)])
            painter.setBrush(color_1)
            painter.drawPolygon(tmp_graph)
            # Rectangle
            tmp_graph = QRectF(x_center - self.L_coil/2, y_center - self.H_wind/2, 2*self.L_coil, self.H_wind)
            painter.setBrush(color_1)
            painter.drawRect(tmp_graph)

            if side: # Connexions que du côté x+
                # Flèches et lignes
                tmp_graph = Arrow(x_center - 11*self.L_coil/2, y_center - self.H_wind/2 - self.arrowLength, x_center - 11*self.L_coil/2, y_center - self.L_coil, self.arrowSize)
                tmp_graph.paint(painter, option, widget)
                tmp_graph = Arrow(x_center + 3*self.L_coil/2, y_center - self.H_wind/2, x_center + 3*self.L_coil/2, y_center - self.H_wind/2 - self.arrowLength, self.arrowSize)
                tmp_graph.paint(painter, option, widget)

                tmp_graph = QLineF(x_center - 7*self.L_coil/2, y_center - self.H_wind/2, x_center - 7*self.L_coil/2, y_center - self.H_wind/2 - self.arrowLength1)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center - 7*self.L_coil/2, y_center - self.H_wind/2 - self.arrowLength1, x_center + 11*self.L_coil/2, y_center - self.H_wind/2 - self.arrowLength1)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center + 11*self.L_coil/2, y_center - self.H_wind/2 - self.arrowLength1, x_center + 11*self.L_coil/2, y_center - self.L_coil)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center - self.L_coil/2, y_center - self.H_wind/2, x_center - self.L_coil/2, y_center - self.H_wind/2 - self.arrowLength1/2)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center - self.L_coil/2, y_center - self.H_wind/2 - self.arrowLength1/2, x_center + 9*self.L_coil/2, y_center - self.H_wind/2 - self.arrowLength1/2)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center + 9*self.L_coil/2, y_center - self.H_wind/2 - self.arrowLength1/2, x_center + 9*self.L_coil/2, y_center - self.H_wind/2)
                painter.drawLine(tmp_graph)

            tmp_rect = QRectF(x_center - 11*self.L_coil/2, y_center - self.H_wind/2 - self.arrowLength, 2*self.L_coil, self.H_wind + self.arrowLength)
            self.path.addRect(tmp_rect)
            tmp_rect = QRectF(x_center - self.L_coil/2, y_center - self.H_wind/2 - self.arrowLength1/2, 2*self.L_coil, self.H_wind + self.arrowLength1/2)
            self.path.addRect(tmp_rect)
            tmp_rect = QRectF(x_center + 9*self.L_coil/2, y_center - self.H_wind/2 - self.arrowLength1, self.L_coil, self.H_wind + self.arrowLength1)
            self.path.addRect(tmp_rect)

        elif self.getShapeWinding() == "shell-triple-classic-out":

            # Rectangles
            tmp_graph = QRectF(x_center - 7*self.L_coil, y_center - self.H_wind/2, self.L_coil/2, self.H_wind)
            painter.setBrush(color_2)
            painter.drawRect(tmp_graph)
            tmp_graph = QRectF(x_center + 13*self.L_coil/2, y_center - self.H_wind/2, self.L_coil/2, self.H_wind)
            painter.setBrush(color_2)
            painter.drawRect(tmp_graph)

            if side: # Connexions que du côté x+
                # Flèches et lignes
                tmp_graph = Arrow(x_center - 13*self.L_coil/2, y_center - self.H_wind/2 - self.arrowLength, x_center - 13*self.L_coil/2, y_center - self.H_wind/2, self.arrowSize)
                tmp_graph.paint(painter, option, widget)
                tmp_graph = Arrow(x_center + 13*self.L_coil/2, y_center - self.H_wind/2, x_center + 13*self.L_coil/2, y_center - self.H_wind/2 - self.arrowLength, self.arrowSize)
                tmp_graph.paint(painter, option, widget)

                tmp_graph = QLineF(x_center - 7*self.L_coil, y_center + self.H_wind/2, x_center - 7*self.L_coil, y_center + self.H_wind/2 + self.arrowLength1)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center - 7*self.L_coil, y_center + self.H_wind/2 + self.arrowLength1, x_center + 7*self.L_coil, y_center + self.H_wind/2 + self.arrowLength1)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center + 7*self.L_coil, y_center + self.H_wind/2 + self.arrowLength1, x_center + 7*self.L_coil, y_center + self.H_wind/2)
                painter.drawLine(tmp_graph)

            tmp_rect = QRectF(x_center - 7*self.L_coil, y_center - self.H_wind/2 - self.arrowLength, self.L_coil/2, self.H_wind + self.arrowLength + self.arrowLength1)
            self.path.addRect(tmp_rect)
            tmp_rect = QRectF(x_center + 13*self.L_coil/2, y_center - self.H_wind/2 - self.arrowLength, self.L_coil/2, self.H_wind + self.arrowLength + self.arrowLength1)
            self.path.addRect(tmp_rect)

        elif self.getShapeWinding() == "shell-triple-classic-left":

            # Rectangle
            tmp_graph = QRectF(x_center - 5*self.L_coil/2, y_center - self.H_wind/2, self.L_coil, self.H_wind)
            painter.setBrush(color_2)
            painter.drawRect(tmp_graph)

            if side: # Connexions que du côté x+
                # Flèches et lignes
                tmp_graph = Arrow(x_center - 5*self.L_coil/2, y_center + self.H_wind/2 + self.arrowLength, x_center - 5*self.L_coil/2, y_center + self.H_wind/2, self.arrowSize)
                tmp_graph.paint(painter, option, widget)
                tmp_graph = Arrow(x_center - 3*self.L_coil/2, y_center + self.H_wind/2, x_center - 3*self.L_coil/2, y_center + self.H_wind/2 + self.arrowLength, self.arrowSize)
                tmp_graph.paint(painter, option, widget)

            tmp_rect = QRectF(x_center - 5*self.L_coil/2, y_center - self.H_wind/2, self.L_coil, self.H_wind + self.arrowLength)
            self.path.addRect(tmp_rect)

        elif self.getShapeWinding() == "shell-triple-classic-right":

            # Rectangle
            tmp_graph = QRectF(x_center + 5*self.L_coil/2, y_center - self.H_wind/2, self.L_coil, self.H_wind)
            painter.setBrush(color_2)
            painter.drawRect(tmp_graph)

            if side: # Connexions que du côté x+
                # Flèches et lignes
                tmp_graph = Arrow(x_center + 5*self.L_coil/2, y_center + self.H_wind/2 + self.arrowLength, x_center + 5*self.L_coil/2, y_center + self.H_wind/2, self.arrowSize)
                tmp_graph.paint(painter, option, widget)
                tmp_graph = Arrow(x_center + 7*self.L_coil/2, y_center + self.H_wind/2, x_center + 7*self.L_coil/2, y_center + self.H_wind/2 + self.arrowLength, self.arrowSize)
                tmp_graph.paint(painter, option, widget)

            tmp_rect = QRectF(x_center + 5*self.L_coil/2, y_center - self.H_wind/2, self.L_coil, self.H_wind + self.arrowLength)
            self.path.addRect(tmp_rect)

        elif self.getShapeWinding() == "shell-simple-barrel-in" or self.getShapeWinding() == "shell-double-barrel-in":

            # Polygone
            tmp_graph = QPolygonF([QPointF(x_center - 4*self.L_coil, y_center + self.L_coil), QPointF(x_center - 4*self.L_coil, y_center - self.L_coil), QPointF(x_center - 2*self.L_coil, y_center - self.H_wind/2), QPointF(x_center - 2*self.L_coil, y_center + self.H_wind/2)])
            painter.setBrush(color_1)
            painter.drawPolygon(tmp_graph)
            tmp_graph = QPolygonF([QPointF(x_center + 2*self.L_coil, y_center + self.H_wind/2), QPointF(x_center + 2*self.L_coil, y_center - self.H_wind/2), QPointF(x_center + 4*self.L_coil, y_center - self.L_coil), QPointF(x_center + 4*self.L_coil, y_center + self.L_coil)])
            painter.setBrush(color_1)
            painter.drawPolygon(tmp_graph)

            if side: # Connexions que du côté x+
                # Flèches et lignes
                tmp_graph = Arrow(x_center - 4*self.L_coil, y_center - self.H_wind/2 - self.arrowLength, x_center - 4*self.L_coil, y_center - self.L_coil, self.arrowSize)
                tmp_graph.paint(painter, option, widget)
                tmp_graph = Arrow(x_center - 2*self.L_coil, y_center - self.H_wind/2, x_center - 2*self.L_coil, y_center - self.H_wind/2 - self.arrowLength, self.arrowSize)
                tmp_graph.paint(painter, option, widget)

                tmp_graph = QLineF(x_center - 2*self.L_coil, y_center - self.H_wind/2, x_center - 2*self.L_coil, y_center - self.H_wind/2 - self.arrowLength1/2)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center - 2*self.L_coil, y_center - self.H_wind/2 - self.arrowLength1/2, x_center + 2*self.L_coil, y_center - self.H_wind/2 - self.arrowLength1/2)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center + 2*self.L_coil, y_center - self.H_wind/2 - self.arrowLength1/2, x_center + 2*self.L_coil, y_center - self.H_wind/2)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center - 4*self.L_coil, y_center - self.H_wind/2 - self.arrowLength1, x_center + 4*self.L_coil, y_center - self.H_wind/2 - self.arrowLength1)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center + 4*self.L_coil, y_center - self.H_wind/2 - self.arrowLength1, x_center + 4*self.L_coil, y_center - self.L_coil)
                painter.drawLine(tmp_graph)

            tmp_rect = QRectF(x_center - 4*self.L_coil, y_center - self.H_wind/2 - self.arrowLength, 2*self.L_coil, self.H_wind + self.arrowLength)
            self.path.addRect(tmp_rect)
            tmp_rect = QRectF(x_center + 2*self.L_coil, y_center - self.H_wind/2 - self.arrowLength, 2*self.L_coil, self.H_wind + self.arrowLength)
            self.path.addRect(tmp_rect)

        elif self.getShapeWinding() == "shell-simple-barrel-out":

            # Rectangles
            tmp_graph = QRectF(x_center - 6*self.L_coil, y_center - self.H_wind/2, self.L_coil, self.H_wind)
            painter.setBrush(color_2)
            painter.drawRect(tmp_graph)
            tmp_graph = QRectF(x_center + 5*self.L_coil, y_center - self.H_wind/2, self.L_coil, self.H_wind)
            painter.setBrush(color_2)
            painter.drawRect(tmp_graph)
            tmp_graph = QRectF(x_center - self.L_coil, y_center - self.H_wind/2, self.L_coil, self.H_wind)
            painter.setBrush(color_2)
            painter.drawRect(tmp_graph)
            tmp_graph = QRectF(x_center, y_center - self.H_wind/2, self.L_coil, self.H_wind)
            painter.setBrush(color_2)
            painter.drawRect(tmp_graph)

            if side: # Connexions que du côté x+
                # Flèches et lignes
                tmp_graph = Arrow(x_center - 5*self.L_coil, y_center + self.H_wind/2 + self.arrowLength, x_center - 5*self.L_coil, y_center + self.H_wind/2, self.arrowSize)
                tmp_graph.paint(painter, option, widget)
                tmp_graph = Arrow(x_center - self.L_coil, y_center + self.H_wind/2, x_center - self.L_coil, y_center + self.H_wind/2 + self.arrowLength, self.arrowSize)
                tmp_graph.paint(painter, option, widget)

                tmp_graph = QLineF(x_center - self.L_coil, y_center + self.H_wind/2 + self.arrowLength1/3, x_center + self.L_coil, y_center + self.H_wind/2 + self.arrowLength1/3)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center + self.L_coil, y_center + self.H_wind/2 + self.arrowLength1/3, x_center + self.L_coil, y_center + self.H_wind/2)
                painter.drawLine(tmp_graph)

                tmp_graph = QLineF(x_center - 6*self.L_coil, y_center + self.H_wind/2, x_center - 6*self.L_coil, y_center + self.H_wind/2 + 2*self.arrowLength1/3)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center - 6*self.L_coil, y_center + self.H_wind/2 + 2*self.arrowLength1/3, x_center + 6*self.L_coil, y_center + self.H_wind/2 + 2*self.arrowLength1/3)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center + 6*self.L_coil, y_center + self.H_wind/2 + 2*self.arrowLength1/3, x_center + 6*self.L_coil, y_center + self.H_wind/2)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center, y_center + self.H_wind/2 + 2*self.arrowLength1/3, x_center, y_center + self.H_wind/2)
                painter.drawLine(tmp_graph)

                tmp_graph = QLineF(x_center - 5*self.L_coil, y_center + self.H_wind/2 + self.arrowLength1, x_center + 5*self.L_coil, y_center + self.H_wind/2 + self.arrowLength1)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center + 5*self.L_coil, y_center + self.H_wind/2 + self.arrowLength1, x_center + 5*self.L_coil, y_center + self.H_wind/2)
                painter.drawLine(tmp_graph)

            tmp_rect = QRectF(x_center - 6*self.L_coil, y_center - self.H_wind/2 - self.arrowLength, self.L_coil, self.H_wind + 2*self.arrowLength)
            self.path.addRect(tmp_rect)
            tmp_rect = QRectF(x_center + 5*self.L_coil, y_center - self.H_wind/2 - self.arrowLength, self.L_coil, self.H_wind + 2*self.arrowLength)
            self.path.addRect(tmp_rect)
            tmp_rect = QRectF(x_center - self.L_coil, y_center - self.H_wind/2 - self.arrowLength, self.L_coil, self.H_wind + 2*self.arrowLength)
            self.path.addRect(tmp_rect)
            tmp_rect = QRectF(x_center, y_center - self.H_wind/2 - self.arrowLength, self.L_coil, self.H_wind + 2*self.arrowLength)
            self.path.addRect(tmp_rect)

        elif self.getShapeWinding() == "shell-double-barrel-left":

            # Rectangles
            tmp_graph = QRectF(x_center - 6*self.L_coil, y_center - self.H_wind/2, self.L_coil, self.H_wind)
            painter.setBrush(color_2)
            painter.drawRect(tmp_graph)
            tmp_graph = QRectF(x_center - self.L_coil, y_center - self.H_wind/2, self.L_coil, self.H_wind)
            painter.setBrush(color_2)
            painter.drawRect(tmp_graph)

            if side: # Connexions que du côté x+
                # Flèches et lignes
                tmp_graph = Arrow(x_center - 5*self.L_coil, y_center + self.H_wind/2 + self.arrowLength, x_center - 5*self.L_coil, y_center + self.H_wind/2, self.arrowSize)
                tmp_graph.paint(painter, option, widget)
                tmp_graph = Arrow(x_center - self.L_coil, y_center + self.H_wind/2, x_center - self.L_coil, y_center + self.H_wind/2 + self.arrowLength, self.arrowSize)
                tmp_graph.paint(painter, option, widget)

                tmp_graph = QLineF(x_center - 6*self.L_coil, y_center + self.H_wind/2, x_center - 6*self.L_coil, y_center + self.H_wind/2 + 2*self.arrowLength1/3)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center - 6*self.L_coil, y_center + self.H_wind/2 + 2*self.arrowLength1/3, x_center, y_center + self.H_wind/2 + 2*self.arrowLength1/3)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center, y_center + self.H_wind/2 + 2*self.arrowLength1/3, x_center, y_center + self.H_wind/2)
                painter.drawLine(tmp_graph)

            tmp_rect = QRectF(x_center - 6*self.L_coil, y_center - self.H_wind/2 - self.arrowLength, self.L_coil, self.H_wind + 2*self.arrowLength)
            self.path.addRect(tmp_rect)
            tmp_rect = QRectF(x_center - self.L_coil, y_center - self.H_wind/2 - self.arrowLength, self.L_coil, self.H_wind + 2*self.arrowLength)
            self.path.addRect(tmp_rect)

        elif self.getShapeWinding() == "shell-double-barrel-right":

            # Rectangles
            tmp_graph = QRectF(x_center + 5*self.L_coil, y_center - self.H_wind/2, self.L_coil, self.H_wind)
            painter.setBrush(color_2)
            painter.drawRect(tmp_graph)
            tmp_graph = QRectF(x_center, y_center - self.H_wind/2, self.L_coil, self.H_wind)
            painter.setBrush(color_2)
            painter.drawRect(tmp_graph)

            if side: # Connexions que du côté x+
                # Flèches et lignes
                tmp_graph = Arrow(x_center + 5*self.L_coil, y_center + self.H_wind/2 + self.arrowLength, x_center + 5*self.L_coil, y_center + self.H_wind/2, self.arrowSize)
                tmp_graph.paint(painter, option, widget)
                tmp_graph = Arrow(x_center + self.L_coil, y_center + self.H_wind/2, x_center + self.L_coil, y_center + self.H_wind/2 + self.arrowLength, self.arrowSize)
                tmp_graph.paint(painter, option, widget)

                tmp_graph = QLineF(x_center + 6*self.L_coil, y_center + self.H_wind/2, x_center + 6*self.L_coil, y_center + self.H_wind/2 + 2*self.arrowLength1/3)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center, y_center + self.H_wind/2 + 2*self.arrowLength1/3, x_center + 6*self.L_coil, y_center + self.H_wind/2 + 2*self.arrowLength1/3)
                painter.drawLine(tmp_graph)
                tmp_graph = QLineF(x_center, y_center + self.H_wind/2 + 2*self.arrowLength1/3, x_center, y_center + self.H_wind/2)
                painter.drawLine(tmp_graph)

            tmp_rect = QRectF(x_center + 5*self.L_coil, y_center - self.H_wind/2 - self.arrowLength, self.L_coil, self.H_wind + 2*self.arrowLength)
            self.path.addRect(tmp_rect)
            tmp_rect = QRectF(x_center, y_center - self.H_wind/2 - self.arrowLength, self.L_coil, self.H_wind + 2*self.arrowLength)
            self.path.addRect(tmp_rect)

        else:
            raise Exception("Shape du winding non reconnue")

class MagneticCircuit(QGraphicsRectItem):
    """
    Objet graphique représentant un circuit magnétique
    """

    def __init__(self, L_CM, nb_phases=1, nb_limbs=2, lst_windings=[], parent=None):
        super().__init__(parent)

        # Données
        self.L_CM = L_CM
        self.nb_phases = nb_phases
        self.nb_limbs = nb_limbs
        self.e_wind_vert = 10.0
        self.e_wind_hori = 5.0
        self.isCoreType = True

        self.lst_windings = lst_windings

        # Crayon fin par défaut
        self.pen_defaut = QPen(Qt.black, 0.5)
        self.pen_used = self.pen_defaut # Par défaut

        # Couleur non définie par défaut
        self.myColor = COLOR_magneticCircuit

        # Contour de l'enroulement
        self.path = QPainterPath()

    def set_lst_windings(self, lst_windings):
        self.lst_windings = lst_windings
        self.prepareGeometryChange()

    def set_nb_phases(self, nb_phases):
        self.nb_phases = nb_phases
        self.prepareGeometryChange()

    def set_nb_limbs(self, nb_limbs):
        self.nb_limbs = nb_limbs
        self.prepareGeometryChange()

    def set_core_type(self, isCoreType):
        self.isCoreType = isCoreType
        self.prepareGeometryChange()

    def get_H_fen(self):
        """
        Fonction permettant d'obtenir la hauteur de la fenêtre correspondant aux windings
        """

        H_fen = -1
        for w in self.lst_windings:
            H_fen = max(H_fen, w.getCoilRectF().height())

        H_fen = H_fen + 2*self.e_wind_vert
        return H_fen

    def get_L_fen(self):
        """
        Fonction permettant d'obtenir la largeur de la fenêtre correspondant aux windings
        """
        L_fen = self.e_wind_hori
        for w in self.lst_windings:
            if w.getShapeWinding() == "two-axial-split-top" or w.getShapeWinding() == "two-axial-split-bottom":
                L_fen = L_fen + w.getCoilRectF().width()/2 + self.e_wind_hori # Car ils sont superposés
            elif w.getShapeWinding() in ["shell-simple-classic-in", "shell-simple-classic-out", "shell-simple-diabolo-in", "shell-simple-diabolo-out"]:
                L_fen = L_fen + w.getCoilRectF().width()/2 + self.e_wind_hori # Car ils sont imbriqués
            elif w.getShapeWinding() in ["shell-simple-barrel-in", "shell-simple-barrel-out"]:
                L_fen = L_fen + w.getCoilRectF().width()/2 + self.e_wind_hori # Car ils sont imbriqués
            elif w.getShapeWinding() in ["shell-double-diabolo-in", "shell-double-diabolo-left", "shell-double-diabolo-right"]:
                L_fen = L_fen + w.getCoilRectF().width()/3 + self.e_wind_hori # Car ils sont imbriqués
            elif w.getShapeWinding() in ["shell-double-classic-in", "shell-double-classic-out", "shell-double-classic-right"]:
                L_fen = L_fen + w.getCoilRectF().width()/3 + self.e_wind_hori # Car ils sont imbriqués
            elif w.getShapeWinding() in ["shell-double-barrel-in", "shell-double-barrel-left", "shell-double-barrel-right"]:
                L_fen = L_fen + w.getCoilRectF().width()/3 + self.e_wind_hori # Car ils sont imbriqués
            elif w.getShapeWinding() in ["shell-triple-classic-in", "shell-triple-classic-out", "shell-triple-classic-left", "shell-triple-classic-right"]:
                L_fen = L_fen + w.getCoilRectF().width()/4 + self.e_wind_hori # Car ils sont imbriqués
            else:
                L_fen = L_fen + w.getCoilRectF().width() + self.e_wind_hori

        if self.isCoreType:
            L_fen = 2*L_fen + 2*self.e_wind_hori # On ajoute 2*self.e_wind_hori pour la jolitée
        else:
            L_fen = L_fen + 2*self.e_wind_hori # On ajoute 2*self.e_wind_hori pour la jolitée

        return L_fen

    def get_center_col(self):
        """
        Fonction renvoyant les coordonnées des centres des colonnes pour le tracé des enroulements
        """
        # Données
        L_fen = self.get_L_fen()
        H_fen = self.get_H_fen()

        # Coordonnées des centres des colonnes pour les enroulements
        if self.nb_phases == 3:
            ### Appareil triphasé
            if self.isCoreType:
                # Core type
                if self.nb_limbs == 3:
                    lst_y_center_col = [(2*self.L_CM + H_fen)/2]
                    lst_x_center_col = [self.L_CM/2, 3*self.L_CM/2 + L_fen, 5*self.L_CM/2 + 2*L_fen]
                elif self.nb_limbs == 5:
                    lst_y_center_col = [(self.L_CM + H_fen)/2]
                    lst_x_center_col = [self.L_CM + L_fen/2, 2*self.L_CM + 3*L_fen/2, 3*self.L_CM + 5*L_fen/2]
                else:
                    raise Exception("Nombre de jambes non géré")
            else:
                # Shell type
                if self.nb_limbs == 7:
                    lst_y_center_col = [2*self.L_CM + H_fen, 5*self.L_CM + 3*H_fen, 8*self.L_CM + 5*H_fen]
                    lst_x_center_col = [self.L_CM + L_fen/2]
                elif self.nb_limbs == 9:
                    lst_y_center_col = [2*self.L_CM + H_fen]
                    lst_x_center_col = [self.L_CM + L_fen/2, 2*self.L_CM + 3*L_fen/2, 3*self.L_CM + 5*L_fen/2]
                else:
                    raise Exception("Nombre de jambes non géré")

        elif self.nb_phases == 1:
            ### Appareil monophasé
            if self.isCoreType:
                # Core type
                if self.nb_limbs == 2:
                    lst_y_center_col = [(2*self.L_CM + H_fen)/2]
                    lst_x_center_col = [self.L_CM/2, 3*self.L_CM/2 + L_fen]
                elif self.nb_limbs == 3:
                    lst_y_center_col = [(self.L_CM + H_fen)/2]
                    lst_x_center_col = [self.L_CM + L_fen/2]
                elif self.nb_limbs == 4:
                    lst_y_center_col = [(self.L_CM + H_fen)/2]
                    lst_x_center_col = [self.L_CM + L_fen/2, 2*self.L_CM + 3*L_fen/2]
                else:
                    raise Exception("Nombre de jambes non géré")
            else:
                # Shell type
                if self.nb_limbs == 3:
                    lst_y_center_col = [2*self.L_CM + H_fen]
                    lst_x_center_col = [self.L_CM + L_fen/2]
                else:
                    raise Exception("Nombre de jambes non géré")

        else:
            raise Exception("Nombre de phases non géré")

        return lst_x_center_col, lst_y_center_col

    def boundingRect(self):

        # Données
        L_fen = self.get_L_fen()
        H_fen = self.get_H_fen()
        penWidth = self.pen_used.widthF()

        if self.nb_phases == 3:
            ### Appareil triphasé
            if self.isCoreType:
                # Core type
                if self.nb_limbs == 3:
                    tmp_graph = QRectF(-L_fen/2 - penWidth/2, - penWidth/2, 3*self.L_CM + 3*L_fen + penWidth, 2*self.L_CM + H_fen + penWidth)
                elif self.nb_limbs == 5:
                    tmp_graph = QRectF(- penWidth/2, - penWidth/2, 4*self.L_CM + 3*L_fen + penWidth, self.L_CM + H_fen + penWidth)
                else:
                    raise Exception("Nombre de jambes non géré")
            else:
                # Shell type
                if self.nb_limbs == 7:
                    tmp_graph = QRectF(- penWidth/2, - penWidth/2, 2*self.L_CM + L_fen + penWidth, 10*self.L_CM + 6*H_fen + penWidth)
                elif self.nb_limbs == 9:
                    tmp_graph = QRectF(- penWidth/2, - penWidth/2, 4*self.L_CM + 3*L_fen + penWidth, 4*self.L_CM + 2*H_fen + penWidth)
                else:
                    raise Exception("Nombre de jambes non géré")

        elif self.nb_phases == 1:
            ### Appareil monophasé
            if self.isCoreType:
                # Core type
                if self.nb_limbs == 2:
                    tmp_graph = QRectF(-L_fen/2 - penWidth/2, - penWidth/2, 2*self.L_CM + 2*L_fen + penWidth, 2*self.L_CM + H_fen + penWidth)
                elif self.nb_limbs == 3:
                    tmp_graph = QRectF(- penWidth/2, - penWidth/2, 2*self.L_CM + L_fen + penWidth, self.L_CM + H_fen + penWidth)
                elif self.nb_limbs == 4:
                    tmp_graph = QRectF(- penWidth/2, - penWidth/2, 3*self.L_CM + 2*L_fen + penWidth, self.L_CM + H_fen + penWidth)
                else:
                    raise Exception("Nombre de jambes non géré")
            else:
                # Shell type
                if self.nb_limbs == 3:
                    tmp_graph = QRectF(- penWidth/2, - penWidth/2, 2*self.L_CM + L_fen + penWidth, 4*self.L_CM + 2*H_fen + penWidth)
                else:
                    raise Exception("Nombre de jambes non géré")
        else:
            raise Exception("Nombre de phases non géré")

        return tmp_graph

    def shape(self):
        # Contour de la forme
        self.path = QPainterPath()
        self.path.addRect(self.boundingRect())
        return self.path

    def paint(self, painter, option, widget=None):

        # Reset du contour
        self.path = QPainterPath()

        # Données
        L_fen = self.get_L_fen()
        H_fen = self.get_H_fen()

        # Crayon
        painter.setPen(self.pen_defaut)

        ### CM
        if self.nb_phases == 3:
            ### Appareil triphasé
            if self.isCoreType:
                # Core type
                if self.nb_limbs == 3:
                    # Rectangle gris
                    tmp_graph = QRectF(0.0, 0.0, 3*self.L_CM + 2*L_fen, 2*self.L_CM + H_fen)
                    painter.setBrush(COLOR_magneticCircuit)
                    painter.drawRect(tmp_graph)

                    # Rectangle blanc 1
                    tmp_graph = QRectF(self.L_CM, self.L_CM, L_fen, H_fen)
                    painter.setBrush(Qt.white)
                    painter.drawRect(tmp_graph)

                    # Rectangle blanc 2
                    tmp_graph = QRectF(2*self.L_CM + L_fen, self.L_CM, L_fen, H_fen)
                    painter.setBrush(Qt.white)
                    painter.drawRect(tmp_graph)

                elif self.nb_limbs == 5:
                    # Rectangle gris
                    tmp_graph = QRectF(0.0, 0.0, 4*self.L_CM + 3*L_fen, self.L_CM + H_fen)
                    painter.setBrush(COLOR_magneticCircuit)
                    painter.drawRect(tmp_graph)

                    # Rectangle blanc 1
                    tmp_graph = QRectF(self.L_CM/2, self.L_CM/2, L_fen/2, H_fen)
                    painter.setBrush(Qt.white)
                    painter.drawRect(tmp_graph)

                    # Rectangle blanc 2
                    tmp_graph = QRectF(3*self.L_CM/2 + L_fen/2, self.L_CM/2, L_fen, H_fen)
                    painter.setBrush(Qt.white)
                    painter.drawRect(tmp_graph)

                    # Rectangle blanc 3
                    tmp_graph = QRectF(5*self.L_CM/2 + 3*L_fen/2, self.L_CM/2, L_fen, H_fen)
                    painter.setBrush(Qt.white)
                    painter.drawRect(tmp_graph)

                    # Rectangle blanc 4
                    tmp_graph = QRectF(7*self.L_CM/2 + 5*L_fen/2, self.L_CM/2, L_fen/2, H_fen)
                    painter.setBrush(Qt.white)
                    painter.drawRect(tmp_graph)

                else:
                    raise Exception("Nombre de jambes non géré")
            else:
                # Shell type
                if self.nb_limbs == 7:
                    # Rectangle gris
                    tmp_graph = QRectF(0.0, 0.0, 2*self.L_CM + L_fen, 10*self.L_CM + 6*H_fen)
                    painter.setBrush(COLOR_magneticCircuit)
                    painter.drawRect(tmp_graph)

                    # Rectangle blanc 1
                    tmp_graph = QRectF(self.L_CM, self.L_CM, L_fen, H_fen)
                    painter.setBrush(Qt.white)
                    painter.drawRect(tmp_graph)
                    self.path.addRect(tmp_graph)

                    # Rectangle blanc 2
                    tmp_graph = QRectF(self.L_CM, 3*self.L_CM + H_fen, L_fen, H_fen)
                    painter.setBrush(Qt.white)
                    painter.drawRect(tmp_graph)
                    self.path.addRect(tmp_graph)

                    # Rectangle blanc 3
                    tmp_graph = QRectF(self.L_CM, 4*self.L_CM + 2*H_fen, L_fen, H_fen)
                    painter.setBrush(Qt.white)
                    painter.drawRect(tmp_graph)
                    self.path.addRect(tmp_graph)

                    # Rectangle blanc 4
                    tmp_graph = QRectF(self.L_CM, 6*self.L_CM + 3*H_fen, L_fen, H_fen)
                    painter.setBrush(Qt.white)
                    painter.drawRect(tmp_graph)
                    self.path.addRect(tmp_graph)

                    # Rectangle blanc 5
                    tmp_graph = QRectF(self.L_CM, 7*self.L_CM + 4*H_fen, L_fen, H_fen)
                    painter.setBrush(Qt.white)
                    painter.drawRect(tmp_graph)
                    self.path.addRect(tmp_graph)

                    # Rectangle blanc 6
                    tmp_graph = QRectF(self.L_CM, 9*self.L_CM + 5*H_fen, L_fen, H_fen)
                    painter.setBrush(Qt.white)
                    painter.drawRect(tmp_graph)
                    self.path.addRect(tmp_graph)

                elif self.nb_limbs == 9:
                    # Rectangle gris
                    tmp_graph = QRectF(0.0, 0.0, 4*self.L_CM + 3*L_fen, 4*self.L_CM + 2*H_fen)
                    painter.setBrush(COLOR_magneticCircuit)
                    painter.drawRect(tmp_graph)

                    # Rectangle blanc 1
                    tmp_graph = QRectF(self.L_CM, self.L_CM, L_fen, H_fen)
                    painter.setBrush(Qt.white)
                    painter.drawRect(tmp_graph)
                    self.path.addRect(tmp_graph)

                    # Rectangle blanc 2
                    tmp_graph = QRectF(self.L_CM, 3*self.L_CM + H_fen, L_fen, H_fen)
                    painter.setBrush(Qt.white)
                    painter.drawRect(tmp_graph)
                    self.path.addRect(tmp_graph)

                    # Rectangle blanc 3
                    tmp_graph = QRectF(2*self.L_CM + L_fen, self.L_CM, L_fen, H_fen)
                    painter.setBrush(Qt.white)
                    painter.drawRect(tmp_graph)
                    self.path.addRect(tmp_graph)

                    # Rectangle blanc 4
                    tmp_graph = QRectF(2*self.L_CM + L_fen, 3*self.L_CM + H_fen, L_fen, H_fen)
                    painter.setBrush(Qt.white)
                    painter.drawRect(tmp_graph)
                    self.path.addRect(tmp_graph)

                    # Rectangle blanc 5
                    tmp_graph = QRectF(3*self.L_CM + 2*L_fen, self.L_CM, L_fen, H_fen)
                    painter.setBrush(Qt.white)
                    painter.drawRect(tmp_graph)
                    self.path.addRect(tmp_graph)

                    # Rectangle blanc 6
                    tmp_graph = QRectF(3*self.L_CM + 2*L_fen, 3*self.L_CM + H_fen, L_fen, H_fen)
                    painter.setBrush(Qt.white)
                    painter.drawRect(tmp_graph)
                    self.path.addRect(tmp_graph)

                else:
                    raise Exception("Nombre de jambes non géré")

        elif self.nb_phases == 1:
            ### Appareil monophasé
            if self.isCoreType:
                # Core type
                if self.nb_limbs == 2:
                    # Rectangle gris
                    tmp_graph = QRectF(0.0, 0.0, 2*self.L_CM + L_fen, 2*self.L_CM + H_fen)
                    painter.setBrush(COLOR_magneticCircuit)
                    painter.drawRect(tmp_graph)

                    # Rectangle blanc
                    tmp_graph = QRectF(self.L_CM, self.L_CM, L_fen, H_fen)
                    painter.setBrush(Qt.white)
                    painter.drawRect(tmp_graph)
                    self.path.addRect(tmp_graph)

                elif self.nb_limbs == 3:
                    # Rectangle gris
                    tmp_graph = QRectF(0.0, 0.0, 2*self.L_CM + L_fen, self.L_CM + H_fen)
                    painter.setBrush(COLOR_magneticCircuit)
                    painter.drawRect(tmp_graph)

                    # Rectangle blanc 1
                    tmp_graph = QRectF(self.L_CM/2, self.L_CM/2, L_fen/2, H_fen)
                    painter.setBrush(Qt.white)
                    painter.drawRect(tmp_graph)
                    self.path.addRect(tmp_graph)

                    # Rectangle blanc 2
                    tmp_graph = QRectF(3*self.L_CM/2 + L_fen/2, self.L_CM/2, L_fen/2, H_fen)
                    painter.setBrush(Qt.white)
                    painter.drawRect(tmp_graph)
                    self.path.addRect(tmp_graph)

                elif self.nb_limbs == 4:
                    # Rectangle gris
                    tmp_graph = QRectF(0.0, 0.0, 3*self.L_CM + 2*L_fen, self.L_CM + H_fen)
                    painter.setBrush(COLOR_magneticCircuit)
                    painter.drawRect(tmp_graph)

                    # Rectangle blanc 1
                    tmp_graph = QRectF(self.L_CM/2, self.L_CM/2, L_fen/2, H_fen)
                    painter.setBrush(Qt.white)
                    painter.drawRect(tmp_graph)
                    self.path.addRect(tmp_graph)

                    # Rectangle blanc 2
                    tmp_graph = QRectF(3*self.L_CM/2 + L_fen/2, self.L_CM/2, L_fen, H_fen)
                    painter.setBrush(Qt.white)
                    painter.drawRect(tmp_graph)
                    self.path.addRect(tmp_graph)

                    # Rectangle blanc 3
                    tmp_graph = QRectF(5*self.L_CM/2 + 3*L_fen/2, self.L_CM/2, L_fen/2, H_fen)
                    painter.setBrush(Qt.white)
                    painter.drawRect(tmp_graph)

                else:
                    raise Exception("Nombre de jambes non géré")
            else:
                # Shell type
                if self.nb_limbs == 3:
                    # Rectangle gris
                    tmp_graph = QRectF(0.0, 0.0, 2*self.L_CM + L_fen, 4*self.L_CM + 2*H_fen)
                    painter.setBrush(COLOR_magneticCircuit)
                    painter.drawRect(tmp_graph)

                    # Rectangle blanc 1
                    tmp_graph = QRectF(self.L_CM, self.L_CM, L_fen, H_fen)
                    painter.setBrush(Qt.white)
                    painter.drawRect(tmp_graph)
                    self.path.addRect(tmp_graph)

                    # Rectangle blanc 2
                    tmp_graph = QRectF(self.L_CM, 3*self.L_CM + H_fen, L_fen, H_fen)
                    painter.setBrush(Qt.white)
                    painter.drawRect(tmp_graph)
                    self.path.addRect(tmp_graph)

                else:
                    raise Exception("Nombre de jambes non géré")

        else:
            raise Exception("Nombre de phases non géré")

class Cable(QGraphicsRectItem):
    """
    Objet graphique représentant un cable
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Données
        self.prop_cable = None

        # Angle de rotation
        self.angle = 0.0
        self.x_center = 0.0
        self.y_center = 0.0

        # Mode de dessin par défaut
        self.drawingMode = "simple"

        # Liste de cables possibles (pour le contextMenu)
        self.lst_availableCables = []

        # Crayon fin par défaut
        self.pen_detailled = QPen(Qt.black, 0.05)
        self.pen_simple = QPen(Qt.black, 0.5)

        self.pen_used = self.pen_simple # Par défaut

        # Contour du cable
        self.path = QPainterPath()

    def setPropCable(self, prop_cable):
        self.prop_cable = prop_cable
        self.prepareGeometryChange()

    def getPropCable(self):
        return self.prop_cable

    def setDrawingMode(self, mode):
        self.drawingMode = mode

    def setAvailableCables(self, lst_availableCables):
        self.lst_availableCables = lst_availableCables

    def getXYsize(self):
        """
        Renvoie les dimensions en X et Y en tenant compte de l'angle du cable
        """
        prop_cable = self.getPropCable()

        if self.angle % 180 == 0:
            # Cable vertical
            return [prop_cable["t_cable"], prop_cable["h_cable"]]
        elif self.angle % 180 == 90:
            # Cable horizontal
            return [prop_cable["h_cable"], prop_cable["t_cable"]]
        else:
            raise Exception("Cas non pris en compte")

    def getCenter(self):
        return [self.x_center, self.y_center]

    def boundingRect(self):
        [x_center, y_center] = self.getCenter()
        [x_size, y_size] = self.getXYsize()

        penWidth = self.pen_used.widthF()
        tmp_graph = QRectF(x_center - x_size/2 - penWidth/2, y_center - y_size/2 - penWidth/2, x_size + penWidth, y_size + penWidth)

        return tmp_graph

    def shape(self):
        # Contour de la forme
        self.path = QPainterPath()
        self.path.addRect(self.boundingRect())
        return self.path

    def rotateCenter(self, angle):
        self.angle = self.angle + angle
        self.prepareGeometryChange()

    def paint(self, painter, option, widget=None):

        [x_center, y_center] = self.getCenter()
        [x_size, y_size] = self.getXYsize()
        prop_cable = self.getPropCable()

        # Point de départ
        x = x_center - x_size/2
        y = y_center - y_size/2

        if self.drawingMode == "simple" or not "type" in prop_cable.keys():

            # Crayon
            painter.setPen(self.pen_simple)
            self.pen_used = self.pen_simple

            # Mode de représentation simple
            tmp_graph = QRectF(x, y, x_size, y_size)
            painter.setBrush(prop_cable["color_simple"])
            painter.drawRect(tmp_graph)

        elif self.drawingMode == "detailled":
            # Crayon
            painter.setPen(self.pen_detailled)
            self.pen_used = self.pen_detailled

            # Mode de représentation détaillé
            if "CTC" in prop_cable["type"]:

                ### Isolant extérieur
                if self.angle % 180 == 0:
                    tmp_graph = QRectF(x, y, prop_cable["t_cable"], prop_cable["h_cable"])
                elif self.angle % 180 == 90:
                    tmp_graph = QRectF(x, y, prop_cable["h_cable"], prop_cable["t_cable"])
                else:
                    raise Exception("Cas non pris en compte")

                if prop_cable["type"] == "CTC Paper":
                    ### Papier
                    painter.setBrush(COLOR_paper)
                elif prop_cable["type"] == "CTC Netting tape":
                    ### Polyester
                    painter.setBrush(COLOR_polyester)
                else:
                    raise Exception("Type de cable inconnu")
                painter.drawRect(tmp_graph)

                ### Brin CTC
                # Varnish brin + coins
                if self.angle % 180 == 0:
                    xp = x + prop_cable["t_cableInsulation"]/2
                    yp = y + prop_cable["t_cableInsulation"]/2
                    tmp_graph = QRectF(xp, yp, prop_cable["t_cable"] - prop_cable["t_cableInsulation"], prop_cable["t_strand"]+prop_cable["t_strandInsulation"])
                elif self.angle % 180 == 90:
                    xp = x + prop_cable["t_cableInsulation"]/2
                    yp = y + prop_cable["t_cableInsulation"]/2
                    tmp_graph = QRectF(xp, yp, prop_cable["t_strand"]+prop_cable["t_strandInsulation"], prop_cable["t_cable"] - prop_cable["t_cableInsulation"])
                else:
                    raise Exception("Cas non pris en compte")
                painter.setBrush(COLOR_varnish)
                painter.drawRect(tmp_graph)

                # Brin
                if self.angle % 180 == 0:
                    x = xp + (prop_cable["t_cable"] - prop_cable["t_cableInsulation"])/2 - prop_cable["h_strand"]/2
                    y = yp + prop_cable["t_strandInsulation"]/2
                    tmp_graph = QRectF(x, y, prop_cable["h_strand"], prop_cable["t_strand"])
                elif self.angle % 180 == 90:
                    x = xp + prop_cable["t_strandInsulation"]/2
                    y = yp + (prop_cable["t_cable"] - prop_cable["t_cableInsulation"])/2 - prop_cable["h_strand"]/2
                    tmp_graph = QRectF(x, y, prop_cable["t_strand"], prop_cable["h_strand"])
                else:
                    raise Exception("Cas non pris en compte")
                painter.setBrush(COLOR_copper)
                painter.drawRect(tmp_graph)

                ### 1ère rangée de brins
                if self.angle % 180 == 0:
                    x = xp
                    y = yp + prop_cable["t_strand"] + prop_cable["t_strandInsulation"]
                elif self.angle % 180 == 90:
                    x = xp + prop_cable["t_strand"] + prop_cable["t_strandInsulation"]
                    y = yp
                else:
                    raise Exception("Cas non pris en compte")

                for k in range(int((prop_cable["N_strands"]-1)/2)):
                    # Varnish
                    if self.angle % 180 == 0:
                        tmp_graph = QRectF(x, y, prop_cable["h_strand"]+prop_cable["t_strandInsulation"], prop_cable["t_strand"]+prop_cable["t_strandInsulation"])
                    elif self.angle % 180 == 90:
                        tmp_graph = QRectF(x, y, prop_cable["t_strand"]+prop_cable["t_strandInsulation"], prop_cable["h_strand"]+prop_cable["t_strandInsulation"])
                    painter.setBrush(COLOR_varnish)
                    painter.drawRect(tmp_graph)

                    # Brin
                    if self.angle % 180 == 0:
                        x = x + prop_cable["t_strandInsulation"]/2
                        y = y + prop_cable["t_strandInsulation"]/2
                        tmp_graph = QRectF(x, y, prop_cable["h_strand"], prop_cable["t_strand"])
                    elif self.angle % 180 == 90:
                        x = x + prop_cable["t_strandInsulation"]/2
                        y = y + prop_cable["t_strandInsulation"]/2
                        tmp_graph = QRectF(x, y, prop_cable["t_strand"], prop_cable["h_strand"])
                    else:
                        raise Exception("Cas non pris en compte")
                    painter.setBrush(COLOR_copper)
                    painter.drawRect(tmp_graph)

                    if self.angle % 180 == 0:
                        x = xp
                        y = y + prop_cable["t_strand"] + prop_cable["t_strandInsulation"]/2
                    elif self.angle % 180 == 90:
                        x = x + prop_cable["t_strand"] + prop_cable["t_strandInsulation"]/2
                        y = yp
                    else:
                        raise Exception("Cas non pris en compte")

                ### Pressboard
                if self.angle % 180 == 0:
                    x = xp + prop_cable["h_strand"] + prop_cable["t_strandInsulation"]
                    y = yp + prop_cable["t_strand"] + prop_cable["t_strandInsulation"]
                    tmp_graph = QRectF(x, y, prop_cable["t_pressboard"], int((prop_cable["N_strands"]-1)/2)*(prop_cable["t_strand"]+prop_cable["t_strandInsulation"]))
                elif self.angle % 180 == 90:
                    x = xp + prop_cable["t_strand"] + prop_cable["t_strandInsulation"]
                    y = yp + prop_cable["h_strand"] + prop_cable["t_strandInsulation"]
                    tmp_graph = QRectF(x, y, int((prop_cable["N_strands"]-1)/2)*(prop_cable["t_strand"]+prop_cable["t_strandInsulation"]), prop_cable["t_pressboard"])
                else:
                    raise Exception("Cas non pris en compte")
                painter.setBrush(COLOR_pressboard)
                painter.drawRect(tmp_graph)

                ### 2ème rangée de brins
                if self.angle % 180 == 0:
                    x = xp + prop_cable["h_strand"] + prop_cable["t_strandInsulation"] + prop_cable["t_pressboard"]
                    y = yp + prop_cable["t_strand"] + prop_cable["t_strandInsulation"]
                elif self.angle % 180 == 90:
                    x = xp + prop_cable["t_strand"] + prop_cable["t_strandInsulation"]
                    y = yp + prop_cable["h_strand"] + prop_cable["t_strandInsulation"] + prop_cable["t_pressboard"]
                else:
                    raise Exception("Cas non pris en compte")

                for k in range(int((prop_cable["N_strands"]-1)/2)):
                    # Varnish
                    if self.angle % 180 == 0:
                        tmp_graph = QRectF(x, y, prop_cable["h_strand"]+prop_cable["t_strandInsulation"], prop_cable["t_strand"]+prop_cable["t_strandInsulation"])
                    elif self.angle % 180 == 90:
                        tmp_graph = QRectF(x, y, prop_cable["t_strand"]+prop_cable["t_strandInsulation"], prop_cable["h_strand"]+prop_cable["t_strandInsulation"])
                    else:
                        raise Exception("Cas non pris en compte")
                    painter.setBrush(COLOR_varnish)
                    painter.drawRect(tmp_graph)

                    # Brin
                    if self.angle % 180 == 0:
                        x = x + prop_cable["t_strandInsulation"]/2
                        y = y + prop_cable["t_strandInsulation"]/2
                        tmp_graph = QRectF(x, y, prop_cable["h_strand"], prop_cable["t_strand"])
                    elif self.angle % 180 == 90:
                        x = x + prop_cable["t_strandInsulation"]/2
                        y = y + prop_cable["t_strandInsulation"]/2
                        tmp_graph = QRectF(x, y, prop_cable["t_strand"], prop_cable["h_strand"])
                    else:
                        raise Exception("Cas non pris en compte")
                    painter.setBrush(COLOR_copper)
                    painter.drawRect(tmp_graph)

                    if self.angle % 180 == 0:
                        x = xp + prop_cable["h_strand"] + prop_cable["t_strandInsulation"] + prop_cable["t_pressboard"]
                        y = y + prop_cable["t_strand"] + prop_cable["t_strandInsulation"]/2
                    elif self.angle % 180 == 90:
                        x = x + prop_cable["t_strand"] + prop_cable["t_strandInsulation"]/2
                        y = yp + prop_cable["h_strand"] + prop_cable["t_strandInsulation"] + prop_cable["t_pressboard"]
                    else:
                        raise Exception("Cas non pris en compte")

            elif prop_cable["type"] == "Meplat":

                ### Papier
                if self.angle % 180 == 0:
                    tmp_graph = QRectF(x, y, prop_cable["t_cable"], prop_cable["h_cable"])
                elif self.angle % 180 == 90:
                    tmp_graph = QRectF(x, y, prop_cable["h_cable"], prop_cable["t_cable"])
                else:
                    raise Exception("Cas non pris en compte")
                painter.setBrush(COLOR_paper)
                painter.drawRect(tmp_graph)

                ### Rangée de brins avec papier
                if self.angle % 180 == 0:
                    xp = x + prop_cable["t_cableInsulation"]/2
                    y = y + prop_cable["t_cableInsulation"]/2
                elif self.angle % 180 == 90:
                    x = x + prop_cable["t_cableInsulation"]/2
                    yp = y + prop_cable["t_cableInsulation"]/2
                else:
                    raise Exception("Cas non pris en compte")

                for k in range(prop_cable["N_strands"]):

                    # Insulation
                    if self.angle % 180 == 0:
                        tmp_graph = QRectF(xp, y, prop_cable["h_strand"]+prop_cable["t_strandInsulation"], prop_cable["t_strand"]+prop_cable["t_strandInsulation"])
                    elif self.angle % 180 == 90:
                        tmp_graph = QRectF(x, yp, prop_cable["t_strand"]+prop_cable["t_strandInsulation"], prop_cable["h_strand"]+prop_cable["t_strandInsulation"])
                    else:
                        raise Exception("Cas non pris en compte")

                    if prop_cable["type_strandInsulation"] == "paper":
                        painter.setBrush(COLOR_paper)
                    else:
                        painter.setBrush(COLOR_varnish)
                    painter.drawRect(tmp_graph)

                    # Brin
                    if self.angle % 180 == 0:
                        x = xp + prop_cable["t_strandInsulation"]/2
                        y = y + prop_cable["t_strandInsulation"]/2
                        tmp_graph = QRectF(x, y, prop_cable["h_strand"], prop_cable["t_strand"])
                    elif self.angle % 180 == 90:
                        x = x + prop_cable["t_strandInsulation"]/2
                        y = yp + prop_cable["t_strandInsulation"]/2
                        tmp_graph = QRectF(x, y, prop_cable["t_strand"], prop_cable["h_strand"])
                    else:
                        raise Exception("Cas non pris en compte")

                    painter.setBrush(COLOR_copper)
                    painter.drawRect(tmp_graph)

                    if self.angle % 180 == 0:
                        y = y + prop_cable["t_strand"] + prop_cable["t_strandInsulation"]/2
                    elif self.angle % 180 == 90:
                        x = x + prop_cable["t_strand"] + prop_cable["t_strandInsulation"]/2
                    else:
                        raise Exception("Cas non pris en compte")

            else:
                raise Exception("Type de cable inconnu")
        else:
            raise Exception("Mode de représentation inconnu")

