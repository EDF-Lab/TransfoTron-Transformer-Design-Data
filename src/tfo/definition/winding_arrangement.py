# -*- coding: utf-8 -*-
import sys
from os.path import join, dirname, realpath

from PySide6.QtCore import Signal
from PySide6.QtGui import QStandardItem
from PySide6.QtWidgets import QVBoxLayout, QGraphicsScene, QFrame, QWidget

from .coilDefinition import UI_CoilDefinition
from .winding_data import UI_WindingData
from ..utils import gui_geom
from ..utils import gui_utils

from .winding_arrangement_ui import Ui_Form

# =============================================================================
# Widget de definition de la disposition des enroulements
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

class UI_WindingArrangement(QWidget, Ui_Form):

    # Signal quand le winding est modifié (pour MAJ tfo view)
    windingUpdated = Signal()
    # Signal quand le widget est modifié par l'utilisateur (non programmatiquement)
    isModified = Signal()

    def __init__(self, H_wind, L_coil, scene_tfo, model_lst_wind, layout_wind, widg_ratingPlate, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.H_wind = H_wind
        self.L_coil = L_coil
        self.scene_tfo = scene_tfo
        self.model_lst_wind = model_lst_wind
        self.layout_wind = layout_wind
        self.widg_ratingPlate = widg_ratingPlate

        self.setup()

    def setup(self):

        # Passage en gras de certains titres
        self.ui_grpBox_windDir.setStyleSheet("QGroupBox { font-weight: bold; } ")

        # Initialisation des radios buttons
        self.ui_rBut_posDir.setChecked(True)
        self.ui_rBut_classic.setChecked(True)
        self.ui_rBut_shell_simple_classic.setChecked(True)

        # Liste des enroulements compris dans la disposition
        self.lst_UI_WindingData = []
        self.lst_coilThermalData = []
        self.lst_coilElectricalData = []

        ### Représentations des arrangements des enroulements
        height_frame = 200
        winding_dir = self.ui_rBut_posDir.isChecked()

        ## Core-type
        # Classic
        layout_tmp = QVBoxLayout(self.ui_frame_classic)
        self.ui_frame_classic.setLayout(layout_tmp)
        scene_tmp = QGraphicsScene(self.ui_frame_classic)
        view_tmp = gui_utils.ViewResizeAuto(scene_tmp)
        layout_tmp.addWidget(view_tmp)
        self.ui_frame_classic.setFixedHeight(height_frame)
        self.ui_frame_classic.setFrameShape(QFrame.NoFrame)

        self.winding_classic = gui_geom.Winding(self.H_wind, self.L_coil, "classic", winding_dir)
        scene_tmp.addItem(self.winding_classic)

        # Double Classic
        layout_tmp = QVBoxLayout(self.ui_frame_doubleClassic)
        self.ui_frame_doubleClassic.setLayout(layout_tmp)
        scene_tmp = QGraphicsScene(self.ui_frame_doubleClassic)
        view_tmp = gui_utils.ViewResizeAuto(scene_tmp)
        layout_tmp.addWidget(view_tmp)
        self.ui_frame_doubleClassic.setFixedHeight(height_frame)
        self.ui_frame_doubleClassic.setFrameShape(QFrame.NoFrame)

        self.winding_doubleClassic = gui_geom.Winding(self.H_wind, self.L_coil, "double-classic", winding_dir)
        scene_tmp.addItem(self.winding_doubleClassic)

        # Fine Coarse
        layout_tmp = QVBoxLayout(self.ui_frame_fineCoarse)
        self.ui_frame_fineCoarse.setLayout(layout_tmp)
        scene_tmp = QGraphicsScene(self.ui_frame_fineCoarse)
        view_tmp = gui_utils.ViewResizeAuto(scene_tmp)
        layout_tmp.addWidget(view_tmp)
        self.ui_frame_fineCoarse.setFixedHeight(height_frame)
        self.ui_frame_fineCoarse.setFrameShape(QFrame.NoFrame)

        self.winding_fineCoarse = gui_geom.Winding(self.H_wind, self.L_coil, "fine-coarse", winding_dir)
        scene_tmp.addItem(self.winding_fineCoarse)

        # Middle entry
        layout_tmp = QVBoxLayout(self.ui_frame_midEntry)
        self.ui_frame_midEntry.setLayout(layout_tmp)
        scene_tmp = QGraphicsScene(self.ui_frame_midEntry)
        view_tmp = gui_utils.ViewResizeAuto(scene_tmp)
        layout_tmp.addWidget(view_tmp)
        self.ui_frame_midEntry.setFixedHeight(height_frame)
        self.ui_frame_midEntry.setFrameShape(QFrame.NoFrame)

        self.winding_midEntry = gui_geom.Winding(self.H_wind, self.L_coil, "middle-entry", winding_dir)
        scene_tmp.addItem(self.winding_midEntry)

        # One Axial split
        layout_tmp = QVBoxLayout(self.ui_frame_oneAxialSplit)
        self.ui_frame_oneAxialSplit.setLayout(layout_tmp)
        scene_tmp = QGraphicsScene(self.ui_frame_oneAxialSplit)
        view_tmp = gui_utils.ViewResizeAuto(scene_tmp)
        layout_tmp.addWidget(view_tmp)
        self.ui_frame_oneAxialSplit.setFixedHeight(height_frame)
        self.ui_frame_oneAxialSplit.setFrameShape(QFrame.NoFrame)

        self.winding_oneAxialSplit = gui_geom.Winding(self.H_wind, self.L_coil, "one-axial-split", winding_dir)
        scene_tmp.addItem(self.winding_oneAxialSplit)

        # Two Axial split
        layout_tmp = QVBoxLayout(self.ui_frame_twoAxialSplit)
        self.ui_frame_twoAxialSplit.setLayout(layout_tmp)
        scene_tmp = QGraphicsScene(self.ui_frame_twoAxialSplit)
        view_tmp = gui_utils.ViewResizeAuto(scene_tmp)
        layout_tmp.addWidget(view_tmp)
        self.ui_frame_twoAxialSplit.setFixedHeight(height_frame)
        self.ui_frame_twoAxialSplit.setFrameShape(QFrame.NoFrame)

        self.winding_twoAxialSplitTop = gui_geom.Winding(self.H_wind/2, self.L_coil, "two-axial-split-top", winding_dir)
        scene_tmp.addItem(self.winding_twoAxialSplitTop)
        self.winding_twoAxialSplitBottom = gui_geom.Winding(self.H_wind/2, self.L_coil, "two-axial-split-bottom", winding_dir)
        scene_tmp.addItem(self.winding_twoAxialSplitBottom)

        ## Shell type

        # Two windings classic
        layout_tmp = QVBoxLayout(self.ui_frame_shell_simple_classic)
        self.ui_frame_shell_simple_classic.setLayout(layout_tmp)
        scene_tmp = QGraphicsScene(self.ui_frame_shell_simple_classic)
        view_tmp = gui_utils.ViewResizeAuto(scene_tmp)
        layout_tmp.addWidget(view_tmp)
        self.ui_frame_shell_simple_classic.setFixedHeight(height_frame)
        self.ui_frame_shell_simple_classic.setFrameShape(QFrame.NoFrame)

        self.winding_shell_simple_classic_in = gui_geom.Winding(self.H_wind/2, self.L_coil, "shell-simple-classic-in", winding_dir)
        scene_tmp.addItem(self.winding_shell_simple_classic_in)
        self.winding_shell_simple_classic_out = gui_geom.Winding(self.H_wind/2, self.L_coil, "shell-simple-classic-out", winding_dir)
        scene_tmp.addItem(self.winding_shell_simple_classic_out)

        # Two windings diabolo
        layout_tmp = QVBoxLayout(self.ui_frame_shell_simple_diabolo)
        self.ui_frame_shell_simple_diabolo.setLayout(layout_tmp)
        scene_tmp = QGraphicsScene(self.ui_frame_shell_simple_diabolo)
        view_tmp = gui_utils.ViewResizeAuto(scene_tmp)
        layout_tmp.addWidget(view_tmp)
        self.ui_frame_shell_simple_diabolo.setFixedHeight(height_frame)
        self.ui_frame_shell_simple_diabolo.setFrameShape(QFrame.NoFrame)

        self.winding_shell_simple_diabolo_in = gui_geom.Winding(self.H_wind/2, self.L_coil, "shell-simple-diabolo-in", winding_dir)
        scene_tmp.addItem(self.winding_shell_simple_diabolo_in)
        self.winding_shell_simple_diabolo_out = gui_geom.Winding(self.H_wind/2, self.L_coil, "shell-simple-diabolo-out", winding_dir)
        scene_tmp.addItem(self.winding_shell_simple_diabolo_out)

        # Three windings classic
        layout_tmp = QVBoxLayout(self.ui_frame_shell_double_classic)
        self.ui_frame_shell_double_classic.setLayout(layout_tmp)
        scene_tmp = QGraphicsScene(self.ui_frame_shell_double_classic)
        view_tmp = gui_utils.ViewResizeAuto(scene_tmp)
        layout_tmp.addWidget(view_tmp)
        self.ui_frame_shell_double_classic.setFixedHeight(height_frame)
        self.ui_frame_shell_double_classic.setFrameShape(QFrame.NoFrame)

        self.winding_shell_double_classic_in = gui_geom.Winding(self.H_wind/2, self.L_coil, "shell-double-classic-in", winding_dir)
        scene_tmp.addItem(self.winding_shell_double_classic_in)
        self.winding_shell_double_classic_out = gui_geom.Winding(self.H_wind/2, self.L_coil, "shell-double-classic-out", winding_dir)
        scene_tmp.addItem(self.winding_shell_double_classic_out)
        self.winding_shell_double_classic_right = gui_geom.Winding(self.H_wind/2, self.L_coil, "shell-double-classic-right", winding_dir)
        scene_tmp.addItem(self.winding_shell_double_classic_right)

        # Three windings diabolo
        layout_tmp = QVBoxLayout(self.ui_frame_shell_double_diabolo)
        self.ui_frame_shell_double_diabolo.setLayout(layout_tmp)
        scene_tmp = QGraphicsScene(self.ui_frame_shell_double_diabolo)
        view_tmp = gui_utils.ViewResizeAuto(scene_tmp)
        layout_tmp.addWidget(view_tmp)
        self.ui_frame_shell_double_diabolo.setFixedHeight(height_frame)
        self.ui_frame_shell_double_diabolo.setFrameShape(QFrame.NoFrame)

        self.winding_shell_double_diabolo_in = gui_geom.Winding(self.H_wind/2, self.L_coil, "shell-double-diabolo-in", winding_dir)
        scene_tmp.addItem(self.winding_shell_double_diabolo_in)
        self.winding_shell_double_diabolo_left = gui_geom.Winding(self.H_wind/2, self.L_coil, "shell-double-diabolo-left", winding_dir)
        scene_tmp.addItem(self.winding_shell_double_diabolo_left)
        self.winding_shell_double_diabolo_right = gui_geom.Winding(self.H_wind/2, self.L_coil, "shell-double-diabolo-right", winding_dir)
        scene_tmp.addItem(self.winding_shell_double_diabolo_right)

        # Four windings classic
        layout_tmp = QVBoxLayout(self.ui_frame_shell_triple_classic)
        self.ui_frame_shell_triple_classic.setLayout(layout_tmp)
        scene_tmp = QGraphicsScene(self.ui_frame_shell_triple_classic)
        view_tmp = gui_utils.ViewResizeAuto(scene_tmp)
        layout_tmp.addWidget(view_tmp)
        self.ui_frame_shell_triple_classic.setFixedHeight(height_frame)
        self.ui_frame_shell_triple_classic.setFrameShape(QFrame.NoFrame)

        self.winding_shell_triple_classic_in = gui_geom.Winding(self.H_wind/2, self.L_coil, "shell-triple-classic-in", winding_dir)
        scene_tmp.addItem(self.winding_shell_triple_classic_in)
        self.winding_shell_triple_classic_out = gui_geom.Winding(self.H_wind/2, self.L_coil, "shell-triple-classic-out", winding_dir)
        scene_tmp.addItem(self.winding_shell_triple_classic_out)
        self.winding_shell_triple_classic_left = gui_geom.Winding(self.H_wind/2, self.L_coil, "shell-triple-classic-left", winding_dir)
        scene_tmp.addItem(self.winding_shell_triple_classic_left)
        self.winding_shell_triple_classic_right = gui_geom.Winding(self.H_wind/2, self.L_coil, "shell-triple-classic-right", winding_dir)
        scene_tmp.addItem(self.winding_shell_triple_classic_right)

        # Two windings barrel
        layout_tmp = QVBoxLayout(self.ui_frame_shell_simple_barrel)
        self.ui_frame_shell_simple_barrel.setLayout(layout_tmp)
        scene_tmp = QGraphicsScene(self.ui_frame_shell_simple_barrel)
        view_tmp = gui_utils.ViewResizeAuto(scene_tmp)
        layout_tmp.addWidget(view_tmp)
        self.ui_frame_shell_simple_barrel.setFixedHeight(height_frame)
        self.ui_frame_shell_simple_barrel.setFrameShape(QFrame.NoFrame)

        self.winding_shell_simple_barrel_in = gui_geom.Winding(self.H_wind/2, self.L_coil, "shell-simple-barrel-in", winding_dir)
        scene_tmp.addItem(self.winding_shell_simple_barrel_in)
        self.winding_shell_simple_barrel_out = gui_geom.Winding(self.H_wind/2, self.L_coil, "shell-simple-barrel-out", winding_dir)
        scene_tmp.addItem(self.winding_shell_simple_barrel_out)

        # Three windings barrel
        layout_tmp = QVBoxLayout(self.ui_frame_shell_double_barrel)
        self.ui_frame_shell_double_barrel.setLayout(layout_tmp)
        scene_tmp = QGraphicsScene(self.ui_frame_shell_double_barrel)
        view_tmp = gui_utils.ViewResizeAuto(scene_tmp)
        layout_tmp.addWidget(view_tmp)
        self.ui_frame_shell_double_barrel.setFixedHeight(height_frame)
        self.ui_frame_shell_double_barrel.setFrameShape(QFrame.NoFrame)

        self.winding_shell_double_barrel_in = gui_geom.Winding(self.H_wind/2, self.L_coil, "shell-double-barrel-in", winding_dir)
        scene_tmp.addItem(self.winding_shell_double_barrel_in)
        self.winding_shell_double_barrel_left = gui_geom.Winding(self.H_wind/2, self.L_coil, "shell-double-barrel-left", winding_dir)
        scene_tmp.addItem(self.winding_shell_double_barrel_left)
        self.winding_shell_double_barrel_right = gui_geom.Winding(self.H_wind/2, self.L_coil, "shell-double-barrel-right", winding_dir)
        scene_tmp.addItem(self.winding_shell_double_barrel_right)

        ### Connecteurs
        self.ui_rBut_posDir.toggled.connect(self.updateWindingsView)
        self.ui_rBut_posDir.toggled.connect(self.updateWindings)
        self.ui_rBut_classic.toggled.connect(self.updateWindings)
        self.ui_rBut_doubleClassic.toggled.connect(self.updateWindings)
        self.ui_rBut_fineCoarse.toggled.connect(self.updateWindings)
        self.ui_rBut_midEntry.toggled.connect(self.updateWindings)
        self.ui_rBut_oneAxialSplit.toggled.connect(self.updateWindings)
        self.ui_rBut_twoAxialSplit.toggled.connect(self.updateWindings)
        self.ui_rBut_shell_simple_classic.toggled.connect(self.updateWindings)
        self.ui_rBut_shell_simple_diabolo.toggled.connect(self.updateWindings)
        self.ui_rBut_shell_double_diabolo.toggled.connect(self.updateWindings)
        self.ui_rBut_shell_triple_classic.toggled.connect(self.updateWindings)
        self.ui_rBut_shell_double_classic.toggled.connect(self.updateWindings)
        self.ui_rBut_shell_simple_barrel.toggled.connect(self.updateWindings)
        self.ui_rBut_shell_double_barrel.toggled.connect(self.updateWindings)

        self.ui_rBut_classic.toggled.connect(self.setLstCoilData)
        self.ui_rBut_doubleClassic.toggled.connect(self.setLstCoilData)
        self.ui_rBut_fineCoarse.toggled.connect(self.setLstCoilData)
        self.ui_rBut_midEntry.toggled.connect(self.setLstCoilData)
        self.ui_rBut_oneAxialSplit.toggled.connect(self.setLstCoilData)
        self.ui_rBut_twoAxialSplit.toggled.connect(self.setLstCoilData)
        self.ui_rBut_shell_simple_classic.toggled.connect(self.setLstCoilData)
        self.ui_rBut_shell_simple_diabolo.toggled.connect(self.setLstCoilData)
        self.ui_rBut_shell_double_diabolo.toggled.connect(self.setLstCoilData)
        self.ui_rBut_shell_triple_classic.toggled.connect(self.setLstCoilData)
        self.ui_rBut_shell_double_classic.toggled.connect(self.setLstCoilData)
        self.ui_rBut_shell_simple_barrel.toggled.connect(self.setLstCoilData)
        self.ui_rBut_shell_double_barrel.toggled.connect(self.setLstCoilData)

        ### Au démarrage
        self.updateWindingsView()
        self.updateDesign()
        self.setLstCoilData()
        self.connectModification()

    def connectModification(self):
        """
        Connection des éléments pour émission du signal isModified
        """
        # Les sous-connections peuvent être activées par l'utilisateur ou programmatiquement
        self.ui_rBut_posDir.toggled.connect(self.emitIsModified)
        self.ui_rBut_negDir.toggled.connect(self.emitIsModified)
        self.ui_rBut_classic.toggled.connect(self.emitIsModified)
        self.ui_rBut_doubleClassic.toggled.connect(self.emitIsModified)
        self.ui_rBut_fineCoarse.toggled.connect(self.emitIsModified)
        self.ui_rBut_midEntry.toggled.connect(self.emitIsModified)
        self.ui_rBut_oneAxialSplit.toggled.connect(self.emitIsModified)
        self.ui_rBut_twoAxialSplit.toggled.connect(self.emitIsModified)
        self.ui_rBut_shell_simple_classic.toggled.connect(self.emitIsModified)
        self.ui_rBut_shell_simple_diabolo.toggled.connect(self.emitIsModified)
        self.ui_rBut_shell_double_diabolo.toggled.connect(self.emitIsModified)
        self.ui_rBut_shell_triple_classic.toggled.connect(self.emitIsModified)
        self.ui_rBut_shell_double_classic.toggled.connect(self.emitIsModified)
        self.ui_rBut_shell_simple_barrel.toggled.connect(self.emitIsModified)
        self.ui_rBut_shell_double_barrel.toggled.connect(self.emitIsModified)

        for c in self.lst_coilThermalData:
            for c_ui in c["lst_UI_CoilDefinition"]:
                c_ui.isModified.connect(self.emitIsModified)

    def emitIsModified(self):
        self.isModified.emit()

    def disconnectModification(self):
        """
        Déconnection des éléments à l'émission du signal isModified
        """
        self.ui_rBut_posDir.toggled.disconnect(self.emitIsModified)
        self.ui_rBut_negDir.toggled.disconnect(self.emitIsModified)
        self.ui_rBut_classic.toggled.disconnect(self.emitIsModified)
        self.ui_rBut_doubleClassic.toggled.disconnect(self.emitIsModified)
        self.ui_rBut_fineCoarse.toggled.disconnect(self.emitIsModified)
        self.ui_rBut_midEntry.toggled.disconnect(self.emitIsModified)
        self.ui_rBut_oneAxialSplit.toggled.disconnect(self.emitIsModified)
        self.ui_rBut_twoAxialSplit.toggled.disconnect(self.emitIsModified)
        self.ui_rBut_shell_simple_classic.toggled.disconnect(self.emitIsModified)
        self.ui_rBut_shell_simple_diabolo.toggled.disconnect(self.emitIsModified)
        self.ui_rBut_shell_double_diabolo.toggled.disconnect(self.emitIsModified)
        self.ui_rBut_shell_triple_classic.toggled.disconnect(self.emitIsModified)
        self.ui_rBut_shell_double_classic.toggled.disconnect(self.emitIsModified)
        self.ui_rBut_shell_simple_barrel.toggled.disconnect(self.emitIsModified)
        self.ui_rBut_shell_double_barrel.toggled.disconnect(self.emitIsModified)

        for c in self.lst_coilThermalData:
            for c_ui in c["lst_UI_CoilDefinition"]:
                try:
                    c_ui.isModified.disconnect(self.emitIsModified)
                except:
                    pass

    def freezeDesign(self, isFrozen):
        """
        Action lors du (dé)gelage du design
        """
        self.ui_rBut_posDir.setEnabled(not isFrozen)
        self.ui_rBut_negDir.setEnabled(not isFrozen)
        self.ui_rBut_classic.setEnabled(not isFrozen)
        self.ui_rBut_doubleClassic.setEnabled(not isFrozen)
        self.ui_rBut_fineCoarse.setEnabled(not isFrozen)
        self.ui_rBut_midEntry.setEnabled(not isFrozen)
        self.ui_rBut_oneAxialSplit.setEnabled(not isFrozen)
        self.ui_rBut_twoAxialSplit.setEnabled(not isFrozen)
        self.ui_rBut_shell_simple_classic.setEnabled(not isFrozen)
        self.ui_rBut_shell_simple_diabolo.setEnabled(not isFrozen)
        self.ui_rBut_shell_double_diabolo.setEnabled(not isFrozen)
        self.ui_rBut_shell_triple_classic.setEnabled(not isFrozen)
        self.ui_rBut_shell_double_classic.setEnabled(not isFrozen)
        self.ui_rBut_shell_simple_barrel.setEnabled(not isFrozen)
        self.ui_rBut_shell_double_barrel.setEnabled(not isFrozen)

        for c in self.lst_coilThermalData:
            for c_ui in c["lst_UI_CoilDefinition"]:
                c_ui.freezeDesign(isFrozen)

        for w in self.lst_UI_WindingData:
            w.freezeDesign(isFrozen)

    def checkDesign(self):
        """
        Vérification du design
        """
        # Liste d'erreurs à corriger
        lst_error = []

        for w in self.lst_UI_WindingData:
            lst_error = lst_error + w.checkDesign()

        return lst_error

    def updateDesign(self):
        """
        MAJ affichage suite à changement de design
        """
        if self.widg_ratingPlate.isCoreType():
            self.ui_grpBox_core.show()
            self.ui_grpBox_shell.hide()
        else:
            self.ui_grpBox_core.hide()
            self.ui_grpBox_shell.show()

        self.updateWindings()

    def updateWindings(self):
        """
        MAJ des enroulements contenus dans l'arangement en fonction des choix faits
        """
        # Nombre d'enroulements compris dans l'arrangement
        if self.widg_ratingPlate.isCoreType():
            if self.ui_rBut_twoAxialSplit.isChecked():
                nb_windings = 2
            else:
                nb_windings = 1
        else:
            if self.ui_rBut_shell_simple_classic.isChecked() or self.ui_rBut_shell_simple_diabolo.isChecked() or self.ui_rBut_shell_simple_barrel.isChecked():
                nb_windings = 2
            elif self.ui_rBut_shell_double_diabolo.isChecked() or self.ui_rBut_shell_double_classic.isChecked() or self.ui_rBut_shell_double_barrel.isChecked():
                nb_windings = 3
            elif self.ui_rBut_shell_triple_classic.isChecked():
                nb_windings = 4
            else:
                nb_windings = 1

        ### Ajout ou suppression des windings en fonction des choix
        nb_windings_old = len(self.lst_UI_WindingData)
        selection_old = self.isSelected()

        # Suppression des enroulements de trop
        if nb_windings_old > nb_windings:
            for k in range(nb_windings_old - nb_windings):
                wdata = self.lst_UI_WindingData.pop()
                self.scene_tfo.removeItem(wdata.winding)
                for i in range(self.model_lst_wind.rowCount()):
                    if self.model_lst_wind.item(i).widget == wdata:
                        self.model_lst_wind.item(i).delete()
                        break
        # Ajout des enroulements manquants
        if nb_windings > nb_windings_old:
            for k in range(nb_windings - nb_windings_old):
                wdata = UI_WindingData(self.H_wind, self.L_coil, self.widg_ratingPlate, self)
                WindingItem(self.model_lst_wind, wdata, self.layout_wind)
                wdata.selectionChanged.connect(self.setSelected)
                wdata.isModified.connect(self.emitIsModified)
                self.lst_UI_WindingData.append(wdata)
                self.scene_tfo.addItem(wdata.winding)

        ### MAJ des enroulements
        if self.widg_ratingPlate.isCoreType():
            if self.ui_rBut_classic.isChecked():
                self.lst_UI_WindingData[0].winding.setShapeWinding("classic")
                self.lst_UI_WindingData[0].winding.set_H_wind(self.H_wind)
            elif self.ui_rBut_doubleClassic.isChecked():
                self.lst_UI_WindingData[0].winding.setShapeWinding("double-classic")
                self.lst_UI_WindingData[0].winding.set_H_wind(self.H_wind)
            elif self.ui_rBut_fineCoarse.isChecked():
                self.lst_UI_WindingData[0].winding.setShapeWinding("fine-coarse")
                self.lst_UI_WindingData[0].winding.set_H_wind(self.H_wind)
            elif self.ui_rBut_midEntry.isChecked():
                self.lst_UI_WindingData[0].winding.setShapeWinding("middle-entry")
                self.lst_UI_WindingData[0].winding.set_H_wind(self.H_wind)
            elif self.ui_rBut_oneAxialSplit.isChecked():
                self.lst_UI_WindingData[0].winding.setShapeWinding("one-axial-split")
                self.lst_UI_WindingData[0].winding.set_H_wind(self.H_wind)
            elif self.ui_rBut_twoAxialSplit.isChecked():
                self.lst_UI_WindingData[0].winding.setShapeWinding("two-axial-split-top")
                self.lst_UI_WindingData[1].winding.setShapeWinding("two-axial-split-bottom")
                self.lst_UI_WindingData[0].winding.set_H_wind(self.H_wind/2)
                self.lst_UI_WindingData[1].winding.set_H_wind(self.H_wind/2)
            else:
                raise Exception("Shape du winding non reconnue")
        else:
            if self.ui_rBut_shell_simple_classic.isChecked():
                self.lst_UI_WindingData[0].winding.setShapeWinding("shell-simple-classic-in")
                self.lst_UI_WindingData[1].winding.setShapeWinding("shell-simple-classic-out")
                self.lst_UI_WindingData[0].winding.set_H_wind(self.H_wind)
                self.lst_UI_WindingData[1].winding.set_H_wind(self.H_wind)
            elif self.ui_rBut_shell_simple_diabolo.isChecked():
                self.lst_UI_WindingData[0].winding.setShapeWinding("shell-simple-diabolo-in")
                self.lst_UI_WindingData[1].winding.setShapeWinding("shell-simple-diabolo-out")
                self.lst_UI_WindingData[0].winding.set_H_wind(self.H_wind)
                self.lst_UI_WindingData[1].winding.set_H_wind(self.H_wind)
            elif self.ui_rBut_shell_double_diabolo.isChecked():
                self.lst_UI_WindingData[0].winding.setShapeWinding("shell-double-diabolo-in")
                self.lst_UI_WindingData[1].winding.setShapeWinding("shell-double-diabolo-left")
                self.lst_UI_WindingData[2].winding.setShapeWinding("shell-double-diabolo-right")
                self.lst_UI_WindingData[0].winding.set_H_wind(self.H_wind)
                self.lst_UI_WindingData[1].winding.set_H_wind(self.H_wind)
                self.lst_UI_WindingData[2].winding.set_H_wind(self.H_wind)
            elif self.ui_rBut_shell_triple_classic.isChecked():
                self.lst_UI_WindingData[0].winding.setShapeWinding("shell-triple-classic-in")
                self.lst_UI_WindingData[1].winding.setShapeWinding("shell-triple-classic-out")
                self.lst_UI_WindingData[2].winding.setShapeWinding("shell-triple-classic-left")
                self.lst_UI_WindingData[3].winding.setShapeWinding("shell-triple-classic-right")
                self.lst_UI_WindingData[0].winding.set_H_wind(self.H_wind)
                self.lst_UI_WindingData[1].winding.set_H_wind(self.H_wind)
                self.lst_UI_WindingData[2].winding.set_H_wind(self.H_wind)
                self.lst_UI_WindingData[3].winding.set_H_wind(self.H_wind)
            elif self.ui_rBut_shell_double_classic.isChecked():
                self.lst_UI_WindingData[0].winding.setShapeWinding("shell-double-classic-in")
                self.lst_UI_WindingData[1].winding.setShapeWinding("shell-double-classic-out")
                self.lst_UI_WindingData[2].winding.setShapeWinding("shell-double-classic-right")
                self.lst_UI_WindingData[0].winding.set_H_wind(self.H_wind)
                self.lst_UI_WindingData[1].winding.set_H_wind(self.H_wind)
                self.lst_UI_WindingData[2].winding.set_H_wind(self.H_wind)
            elif self.ui_rBut_shell_simple_barrel.isChecked():
                self.lst_UI_WindingData[0].winding.setShapeWinding("shell-simple-barrel-in")
                self.lst_UI_WindingData[1].winding.setShapeWinding("shell-simple-barrel-out")
                self.lst_UI_WindingData[0].winding.set_H_wind(self.H_wind)
                self.lst_UI_WindingData[1].winding.set_H_wind(self.H_wind)
            elif self.ui_rBut_shell_double_barrel.isChecked():
                self.lst_UI_WindingData[0].winding.setShapeWinding("shell-double-barrel-in")
                self.lst_UI_WindingData[1].winding.setShapeWinding("shell-double-barrel-left")
                self.lst_UI_WindingData[2].winding.setShapeWinding("shell-double-barrel-right")
                self.lst_UI_WindingData[0].winding.set_H_wind(self.H_wind)
                self.lst_UI_WindingData[1].winding.set_H_wind(self.H_wind)
                self.lst_UI_WindingData[2].winding.set_H_wind(self.H_wind)
            else:
                raise Exception("Shape du winding non reconnue")

        # Sens
        for wdata in self.lst_UI_WindingData:
            wdata.winding.setWindingDirection(self.ui_rBut_posDir.isChecked())

        # Sélection
        self.setSelected(selection_old)

        # MAJ du CM et du dessin
        self.widg_ratingPlate.updateMagneticCircuit()

    def updateWindingsDisplay(self, lst_x_center_col, R_wind, lst_y_center_col, e_wind_hori=5.0, z_value_wind=1.0):
        """
        MAJ de la représentation synthétique des enroulements de la disposition
        """
        # Dimensions maximales des enroulements de la disposition
        w_max = 0.0
        h_max = 0.0
        for wdata in self.lst_UI_WindingData:
            w_max = max(w_max, wdata.winding.getCoilRectF().width())
            h_max = max(h_max, wdata.winding.getCoilRectF().height())

        # Mise à jour
        if self.widg_ratingPlate.isCoreType():
            R_wind = R_wind + e_wind_hori/2 + w_max/2
        else:
            R_wind = R_wind + 2*e_wind_hori + h_max/2

        for wdata in self.lst_UI_WindingData:
            wdata.winding.setZValue(z_value_wind)
            lst_pos_center = []
            if self.widg_ratingPlate.isCoreType():
                for y in lst_y_center_col:
                    for x in lst_x_center_col:
                        lst_pos_center.append([x + R_wind, y, True])
                        lst_pos_center.append([x - R_wind, y, False])
            else:
                for x in lst_x_center_col:
                    for y in lst_y_center_col:
                        lst_pos_center.append([x, y + R_wind, False])
                        lst_pos_center.append([x, y - R_wind, True])
            wdata.winding.set_lst_pos_center(lst_pos_center)

        if self.widg_ratingPlate.isCoreType():
            R_wind = R_wind + e_wind_hori/2 + w_max/2
        else:
            R_wind = R_wind + 2*e_wind_hori + h_max/2

        return R_wind

    def updateWindingsView(self):
        """
        Mise à jour des windings arrangements
        """
        # Sens de bobinage
        winding_dir = self.ui_rBut_posDir.isChecked()
        self.winding_classic.setWindingDirection(winding_dir)
        self.winding_doubleClassic.setWindingDirection(winding_dir)
        self.winding_fineCoarse.setWindingDirection(winding_dir)
        self.winding_midEntry.setWindingDirection(winding_dir)
        self.winding_oneAxialSplit.setWindingDirection(winding_dir)
        self.winding_twoAxialSplitTop.setWindingDirection(winding_dir)
        self.winding_twoAxialSplitBottom.setWindingDirection(winding_dir)
        self.winding_shell_simple_classic_in.setWindingDirection(winding_dir)
        self.winding_shell_simple_classic_out.setWindingDirection(winding_dir)
        self.winding_shell_simple_diabolo_in.setWindingDirection(winding_dir)
        self.winding_shell_simple_diabolo_out.setWindingDirection(winding_dir)
        self.winding_shell_simple_barrel_in.setWindingDirection(winding_dir)
        self.winding_shell_simple_barrel_out.setWindingDirection(winding_dir)
        self.winding_shell_double_classic_in.setWindingDirection(winding_dir)
        self.winding_shell_double_classic_out.setWindingDirection(winding_dir)
        self.winding_shell_double_classic_right.setWindingDirection(winding_dir)
        self.winding_shell_double_diabolo_in.setWindingDirection(winding_dir)
        self.winding_shell_double_diabolo_left.setWindingDirection(winding_dir)
        self.winding_shell_double_diabolo_right.setWindingDirection(winding_dir)
        self.winding_shell_double_barrel_in.setWindingDirection(winding_dir)
        self.winding_shell_double_barrel_left.setWindingDirection(winding_dir)
        self.winding_shell_double_barrel_right.setWindingDirection(winding_dir)
        self.winding_shell_triple_classic_in.setWindingDirection(winding_dir)
        self.winding_shell_triple_classic_out.setWindingDirection(winding_dir)
        self.winding_shell_triple_classic_left.setWindingDirection(winding_dir)
        self.winding_shell_triple_classic_right.setWindingDirection(winding_dir)

    def setSelected(self, selected, recursive=True):
        """
        Changement de l'état de sélection
        """
        for warr in self.widg_ratingPlate.lst_UI_WindingArrangement:
            if warr == self:
                for wdata in warr.lst_UI_WindingData:
                    wdata.setSelected(selected)
            else:
                if recursive:
                    warr.setSelected(False, False)

    def isSelected(self):
        """
        Renvoi l'état de sélection
        """
        out = False
        for wdata in self.lst_UI_WindingData:
            out = out or wdata.winding.isSelected()
        return out

    def deleteArrangement(self):
        """
        Suppression de la disposition
        """
        for wdata in self.lst_UI_WindingData:
            self.scene_tfo.removeItem(wdata.winding)
            for i in range(self.model_lst_wind.rowCount()):
                if self.model_lst_wind.item(i).widget == wdata:
                    self.model_lst_wind.item(i).delete()
                    break

    def getLstCoilThermalData(self):
        """
        Renvoi la liste des données des bobines thermiques
        """
        self.updateCoilData()
        return self.lst_coilThermalData

    def getLstCoilElectricalData(self):
        """
        Renvoi la liste des données des bobines électriques
        """
        self.updateCoilData()
        return self.lst_coilElectricalData

    def updateCoilData(self):
        """
        MAJ de petits éléments de la coil data, n'écrase pas les infos géométriques & widgets
        """

        # Nom
        if self.widg_ratingPlate.isCoreType():
            if self.ui_rBut_classic.isChecked() or self.ui_rBut_midEntry.isChecked():
                if len(self.lst_coilThermalData) > 0 and len(self.lst_UI_WindingData) > 0:
                    self.lst_coilThermalData[0]["name"] = self.lst_UI_WindingData[0].ui_le_name.text()
                if len(self.lst_coilElectricalData) > 0 and len(self.lst_UI_WindingData) > 0:
                    self.lst_coilElectricalData[0]["name"] = self.lst_UI_WindingData[0].ui_le_name.text()

            elif self.ui_rBut_doubleClassic.isChecked() or self.ui_rBut_oneAxialSplit.isChecked():
                if len(self.lst_coilThermalData) > 1 and len(self.lst_UI_WindingData) > 0:
                    self.lst_coilThermalData[0]["name"] = self.lst_UI_WindingData[0].ui_le_name.text() + "_inner"
                    self.lst_coilThermalData[1]["name"] = self.lst_UI_WindingData[0].ui_le_name.text() + "_outer"
                if len(self.lst_coilElectricalData) > 0 and len(self.lst_UI_WindingData) > 0:
                    self.lst_coilElectricalData[0]["name"] = self.lst_UI_WindingData[0].ui_le_name.text()

            elif self.ui_rBut_fineCoarse.isChecked():
                if len(self.lst_coilThermalData) > 2 and len(self.lst_UI_WindingData) > 0:
                    self.lst_coilThermalData[0]["name"] = self.lst_UI_WindingData[0].ui_le_name.text() + "_main"
                    self.lst_coilThermalData[1]["name"] = self.lst_UI_WindingData[0].ui_le_name.text() + "_coarse"
                    self.lst_coilThermalData[2]["name"] = self.lst_UI_WindingData[0].ui_le_name.text() + "_fine"
                if len(self.lst_coilElectricalData) > 0 and len(self.lst_UI_WindingData) > 0:
                    self.lst_coilElectricalData[0]["name"] = self.lst_UI_WindingData[0].ui_le_name.text()

            elif self.ui_rBut_twoAxialSplit.isChecked():
                if len(self.lst_coilThermalData) > 1 and len(self.lst_UI_WindingData) > 1:
                    name = "%s_%s"%(self.lst_UI_WindingData[0].ui_le_name.text(), self.lst_UI_WindingData[1].ui_le_name.text())
                    self.lst_coilThermalData[0]["name"] = name + "_inner"
                    self.lst_coilThermalData[1]["name"] = name + "_outer"
                if len(self.lst_coilElectricalData) > 1 and len(self.lst_UI_WindingData) > 1:
                    self.lst_coilElectricalData[0]["name"] = self.lst_UI_WindingData[0].ui_le_name.text()
                    self.lst_coilElectricalData[1]["name"] = self.lst_UI_WindingData[1].ui_le_name.text()

            else:
                raise Exception("Shape du winding non reconnue")

        # "UI_WindingArrangement" pour tous
        for c in self.lst_coilThermalData + self.lst_coilElectricalData:
            c["UI_WindingArrangement"] = self

    def setLstCoilData(self):
        """
        Définit la liste des données des bobines thermiques et électriques
        Ecrase les infos & widgets existants sauf les infos gérées par updateCoilData
        """
        if self.widg_ratingPlate.isCoreType():
            # Core type
            if self.ui_rBut_classic.isChecked() or self.ui_rBut_midEntry.isChecked():
                # 1 bobines thermique et 1 électrique
                self.lst_coilThermalData = [{}]
                self.lst_coilElectricalData = [{}]

                # Geometry
                coilDef1 = UI_CoilDefinition()
                coilDef1.isModified.connect(self.emitIsModified)
                self.lst_coilThermalData[0]["lst_UI_CoilDefinition"] = [coilDef1]
                self.lst_coilElectricalData[0]["lst_UI_CoilDefinition"] = [coilDef1]

            elif self.ui_rBut_doubleClassic.isChecked() or self.ui_rBut_oneAxialSplit.isChecked():
                # 2 bobines thermiques et 1 électrique
                self.lst_coilThermalData = [{}, {}]
                self.lst_coilElectricalData = [{}]

                # Geometry
                coilDef1 = UI_CoilDefinition()
                coilDef1.isModified.connect(self.emitIsModified)
                coilDef2 = UI_CoilDefinition()
                coilDef2.isModified.connect(self.emitIsModified)
    #            # On lie les nombres de disques
    #            coilDef1.ui_spBox_nbreDiscs.valueChanged.connect(coilDef2.ui_spBox_nbreDiscs.setValue)
    #            coilDef2.ui_spBox_nbreDiscs.valueChanged.connect(coilDef1.ui_spBox_nbreDiscs.setValue)
                self.lst_coilThermalData[0]["lst_UI_CoilDefinition"] = [coilDef1]
                self.lst_coilThermalData[1]["lst_UI_CoilDefinition"] = [coilDef2]
                self.lst_coilElectricalData[0]["lst_UI_CoilDefinition"] = [coilDef1, coilDef2]

            elif self.ui_rBut_fineCoarse.isChecked():
                # 3 bobines thermiques et 1 électrique
                self.lst_coilThermalData = [{}, {}, {}]
                self.lst_coilElectricalData = [{}]

                # Geometry
                coilDef1 = UI_CoilDefinition()
                coilDef1.isModified.connect(self.emitIsModified)
                coilDef2 = UI_CoilDefinition()
                coilDef2.isModified.connect(self.emitIsModified)
                coilDef3 = UI_CoilDefinition()
                coilDef3.isModified.connect(self.emitIsModified)
                self.lst_coilThermalData[0]["lst_UI_CoilDefinition"] = [coilDef1]
                self.lst_coilThermalData[1]["lst_UI_CoilDefinition"] = [coilDef2]
                self.lst_coilThermalData[2]["lst_UI_CoilDefinition"] = [coilDef3]
                self.lst_coilElectricalData[0]["lst_UI_CoilDefinition"] = [coilDef1, coilDef2, coilDef3]

            elif self.ui_rBut_twoAxialSplit.isChecked():
                # 2 bobines thermiques et 2 électriques
                self.lst_coilThermalData = [{}, {}]
                self.lst_coilElectricalData = [{}, {}]

                # Geometry
                coilDef1 = UI_CoilDefinition()
                coilDef1.isModified.connect(self.emitIsModified)
                coilDef2 = UI_CoilDefinition()
                coilDef2.isModified.connect(self.emitIsModified)
    #            # On lie les nombres de disques
    #            coilDef1.ui_spBox_nbreDiscs.valueChanged.connect(coilDef2.ui_spBox_nbreDiscs.setValue)
    #            coilDef2.ui_spBox_nbreDiscs.valueChanged.connect(coilDef1.ui_spBox_nbreDiscs.setValue)
                self.lst_coilThermalData[0]["lst_UI_CoilDefinition"] = [coilDef1]
                self.lst_coilThermalData[1]["lst_UI_CoilDefinition"] = [coilDef2]
                self.lst_coilElectricalData[0]["lst_UI_CoilDefinition"] = [coilDef1, coilDef2]
                self.lst_coilElectricalData[1]["lst_UI_CoilDefinition"] = [coilDef1, coilDef2]

            else:
                raise Exception("Shape du winding non reconnue")

        else:
            # Shell type, on ne gère pas le design détaillé
            self.lst_coilThermalData = []
            self.lst_coilElectricalData = []

    def addXMLTree(self, tag_ratPlate, docDom):
        """
        Generation de l'arbre XML
        """
        tag_arr = docDom.createElement("winding_arrangement")
        tag_ratPlate.appendChild(tag_arr)

        tag_tmp = docDom.createElement('direction')
        if self.ui_rBut_posDir.isChecked():
            tag_tmp.appendChild(docDom.createTextNode("positive"))
        else:
            tag_tmp.appendChild(docDom.createTextNode("negative"))
        tag_arr.appendChild(tag_tmp)
        tag_tmp = docDom.createElement('style')
        if self.widg_ratingPlate.isCoreType():
            if self.ui_rBut_classic.isChecked():
                tag_tmp.appendChild(docDom.createTextNode("classic"))
            elif self.ui_rBut_doubleClassic.isChecked():
                tag_tmp.appendChild(docDom.createTextNode("double-classic"))
            elif self.ui_rBut_fineCoarse.isChecked():
                tag_tmp.appendChild(docDom.createTextNode("fine-coarse"))
            elif self.ui_rBut_midEntry.isChecked():
                tag_tmp.appendChild(docDom.createTextNode("middle-entry"))
            elif self.ui_rBut_oneAxialSplit.isChecked():
                tag_tmp.appendChild(docDom.createTextNode("one-axial-split"))
            elif self.ui_rBut_twoAxialSplit.isChecked():
                tag_tmp.appendChild(docDom.createTextNode("two-axial-split"))
            else:
                raise Exception("Shape du winding non reconnue")
        else:
            if self.ui_rBut_shell_simple_classic.isChecked():
                tag_tmp.appendChild(docDom.createTextNode("shell-simple-classic"))
            elif self.ui_rBut_shell_simple_diabolo.isChecked():
                tag_tmp.appendChild(docDom.createTextNode("shell-simple-diabolo"))
            elif self.ui_rBut_shell_double_classic.isChecked():
                tag_tmp.appendChild(docDom.createTextNode("shell-double-classic"))
            elif self.ui_rBut_shell_double_diabolo.isChecked():
                tag_tmp.appendChild(docDom.createTextNode("shell-double-diabolo"))
            elif self.ui_rBut_shell_triple_classic.isChecked():
                tag_tmp.appendChild(docDom.createTextNode("shell-triple-classic"))
            elif self.ui_rBut_shell_simple_barrel.isChecked():
                tag_tmp.appendChild(docDom.createTextNode("shell-simple-barrel"))
            elif self.ui_rBut_shell_double_barrel.isChecked():
                tag_tmp.appendChild(docDom.createTextNode("shell-double-barrel"))
            else:
                raise Exception("Shape du winding non reconnue")

        tag_arr.appendChild(tag_tmp)

        for w in self.lst_UI_WindingData:
            w.addXMLTree(tag_arr, docDom)

    def addPDF(self, pdf, part, lst_id_calcul=[]):
        """
        Remplissage du fichier PDF
        """
        pdf.set_font()

        if "data_detail" in part:

            # Nom de la disposition
            name_arr = ' - '.join([wdata.ui_le_name.text() for wdata in self.lst_UI_WindingData])
            pdf.ln()
            pdf.toc_entry("Arrangement %s"%name_arr, 3)

            ### Infos géométriques
            pdf.set_font(style="IU")
            pdf.multi_cell(txt="> Geometrical data:")
            pdf.set_font()

            tmp = " "*8 + "Winding direction: "
            if self.ui_rBut_posDir.isChecked():
                tmp += "positive"
            else:
                tmp += "negative"
            pdf.multi_cell(txt=tmp)

            tmp = " "*8 + "Winding arrangement: "
            if self.widg_ratingPlate.isCoreType():
                if self.ui_rBut_classic.isChecked():
                    tmp += self.ui_rBut_classic.text()
                elif self.ui_rBut_doubleClassic.isChecked():
                    tmp += self.ui_rBut_doubleClassic.text()
                elif self.ui_rBut_midEntry.isChecked():
                    tmp += self.ui_rBut_midEntry.text()
                elif self.ui_rBut_fineCoarse.isChecked():
                    tmp += self.ui_rBut_fineCoarse.text()
                elif self.ui_rBut_oneAxialSplit.isChecked():
                    tmp += self.ui_rBut_oneAxialSplit.text()
                elif self.ui_rBut_twoAxialSplit.isChecked():
                    tmp += self.ui_rBut_twoAxialSplit.text()
                else:
                    raise Exception("Shape du winding non reconnue")
            else:
                if self.ui_rBut_shell_simple_classic.isChecked():
                    tmp += self.ui_rBut_shell_simple_classic.text()
                elif self.ui_rBut_shell_simple_diabolo.isChecked():
                    tmp += self.ui_rBut_shell_simple_diabolo.text()
                elif self.ui_rBut_shell_double_classic.isChecked():
                    tmp += self.ui_rBut_shell_double_classic.text()
                elif self.ui_rBut_shell_double_diabolo.isChecked():
                    tmp += self.ui_rBut_shell_double_diabolo.text()
                elif self.ui_rBut_shell_triple_classic.isChecked():
                    tmp += self.ui_rBut_shell_triple_classic.text()
                elif self.ui_rBut_shell_simple_barrel.isChecked():
                    tmp += self.ui_rBut_shell_simple_barrel.text()
                elif self.ui_rBut_shell_double_barrel.isChecked():
                    tmp += self.ui_rBut_shell_double_barrel.text()
                else:
                    raise Exception("Shape du winding non reconnue")
            pdf.multi_cell(txt=tmp)

            # Infos des enroulements
            for w in self.lst_UI_WindingData:
                pdf.ln()
                w.addPDF(pdf, "data_general", lst_id_calcul)

            # Bobines thermiques
            for c_th in self.getLstCoilThermalData():
                pdf.ln()
                pdf.set_font(style="IU")
                pdf.multi_cell(txt="> Coil %s:"%c_th["name"])
                pdf.set_font()

                for c_def in c_th['lst_UI_CoilDefinition']:
                    c_def.addPDF(pdf, part, lst_id_calcul)

    def loadXMLTree(self, e_arr):
        """
        Chargement de l'arbre XML
        """
        self.disconnectModification()

        w_dir = e_arr.firstChildElement("direction").text()
        if w_dir == "positive":
            self.ui_rBut_posDir.setChecked(True)
        else:
            self.ui_rBut_negDir.setChecked(True)

        w_style = e_arr.firstChildElement("style").text()
        if w_style == "classic":
            self.ui_rBut_classic.setChecked(True)
        elif w_style == "double-classic":
            self.ui_rBut_doubleClassic.setChecked(True)
        elif w_style == "fine-coarse":
            self.ui_rBut_fineCoarse.setChecked(True)
        elif w_style == "middle-entry":
            self.ui_rBut_midEntry.setChecked(True)
        elif w_style == "one-axial-split":
            self.ui_rBut_oneAxialSplit.setChecked(True)
        elif w_style == "two-axial-split":
            self.ui_rBut_twoAxialSplit.setChecked(True)
        elif w_style == "shell-simple-classic":
            self.ui_rBut_shell_simple_classic.setChecked(True)
        elif w_style == "shell-simple-diabolo":
            self.ui_rBut_shell_simple_diabolo.setChecked(True)
        elif w_style == "shell-double-classic":
            self.ui_rBut_shell_double_classic.setChecked(True)
        elif w_style == "shell-double-diabolo":
            self.ui_rBut_shell_double_diabolo.setChecked(True)
        elif w_style == "shell-triple-classic":
            self.ui_rBut_shell_triple_classic.setChecked(True)
        elif w_style == "shell-simple-barrel":
            self.ui_rBut_shell_simple_barrel.setChecked(True)
        elif w_style == "shell-double-barrel":
            self.ui_rBut_shell_double_barrel.setChecked(True)

        n = e_arr.firstChildElement("winding")
        k_wind = 0
        while not n.isNull():
            wind_elt = n.toElement()

            if k_wind < len(self.lst_UI_WindingData):
                self.lst_UI_WindingData[k_wind].loadXMLTree(wind_elt)
                k_wind = k_wind + 1

            n = n.nextSiblingElement("winding")

        self.connectModification()

class WindingItem(QStandardItem):
    """
    Classe représentant un winding
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
        self.model.removeRow(self.model.indexFromItem(self).row())

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
    win = UI_WindingArrangement(100.0, 15.0)

    # 3 - Affichage de la fenêtre
    win.show()

    app.exec()