# -*- coding: utf-8 -*-
import sys
from os.path import join, dirname, realpath
from math import sqrt

from PySide6.QtGui import QRegularExpressionValidator, QDoubleValidator, QStandardItemModel, QStandardItem, QFont, QBrush
from PySide6.QtCore import Qt, Signal, QRegularExpression, QLocale
from PySide6.QtWidgets import QGraphicsItem, QVBoxLayout, QAbstractItemView, QWidget

from ..utils import gui_geom, gui_utils
from ..utils.GridTableView import GridTableView

from .winding_data_ui import Ui_Form

# =============================================================================
# Widget de definition des données d'un enroulement
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

class UI_WindingData(QWidget, Ui_Form):

    # Signal quand le winding est modifié (pour MAJ tfo view)
    windingUpdated = Signal()
    # Signal quand le widget est modifié par l'utilisateur (non programmatiquement)
    isModified = Signal()
    # Signal quand l'enroulement est sélectionné
    selectionChanged = Signal(bool)

    def __init__(self, H_wind, L_coil, widg_ratingPlate, widg_arrangement, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.H_wind = H_wind
        self.L_coil = L_coil
        self.widg_ratingPlate = widg_ratingPlate
        self.widg_arrangement = widg_arrangement

        self.setup()

    def setup(self):

        # Passage en gras de certains titres
        self.ui_grpBox_regWind.setStyleSheet("QGroupBox { font-weight: bold; } ")
        self.ui_grpBox_main.setStyleSheet("QGroupBox { font-weight: bold; } ")

        # Réglage
        self.ui_spBox_nbreTaps.setMinimum(1)
        self.ui_spBox_nbreTaps.setMaximum(10000)
        self.ui_spBox_nbreTaps_p.setMinimum(0)
        self.ui_spBox_nbreTaps_p.setMaximum(10000)
        self.ui_spBox_nbreTaps_m.setMinimum(0)
        self.ui_spBox_nbreTaps_m.setMaximum(10000)
        self.ui_grpBox_regWind.setChecked(False)

        # Couplage
        self.ui_spBox_phase.setMinimum(0)
        self.ui_spBox_phase.setMaximum(11)

        # Divers
        self.winding = gui_geom.Winding(self.H_wind, self.L_coil) # Winding tel que défini par la fenetre
        self.winding.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.winding.selectionChanged.connect(self.selectionChanged)
        self.ui_widget_table.setMinimumSize(600, 200)
        self.ui_grpBox_regWind.setMinimumSize(400, 0)

        # Ajouts de valideurs de champs
        self.locale = QLocale("en")
        self.locale.setNumberOptions(QLocale.RejectGroupSeparator)
        validator_float_pos = QDoubleValidator(self) # Float positif
        validator_float_pos.setBottom(0.001)
        validator_float_pos.setNotation(QDoubleValidator.StandardNotation)
        validator_float_pos.setLocale(self.locale)
        validator_float_pos0 = QDoubleValidator(self) # Float positif
        validator_float_pos0.setNotation(QDoubleValidator.StandardNotation)
        validator_float_pos0.setLocale(self.locale)
        validator_str = QRegularExpressionValidator(QRegularExpression("[A-Za-z0-9-_]+"), self)
        validator_str_tap = QRegularExpressionValidator(QRegularExpression("\d+[A-Za-z]?"), self)

        # Application des valideurs
        self.ui_le_name.setValidator(validator_str)
        self.ui_le_power.setValidator(validator_float_pos)
        self.ui_le_voltage.setValidator(validator_float_pos)
        self.ui_le_highest_voltage.setValidator(validator_float_pos)
        self.ui_le_highest_voltage_neutral.setValidator(validator_float_pos)
        self.ui_le_regStep_p.setValidator(validator_float_pos0)
        self.ui_le_regStep_m.setValidator(validator_float_pos0)

        # Initialisations
        self.ui_le_power.setText("1.0")
        self.ui_le_voltage.setText("1.0")
        self.ui_le_regStep_p.setText("0.0")
        self.ui_le_regStep_m.setText("0.0")

        # Valeurs Um
        lst_um = [1.1, 3.6, 7.2, 12, 17.5, 24, 36, 52, 72.5, 100, 123, 145, 170, 245, 300, 362, 420, 550, 800, 1100, 1200]
        for um in lst_um:
            self.ui_cBox_highest_voltage.addItem("%s kV"%um, um)
            self.ui_cBox_highest_voltage_neutral.addItem("%s kV"%um, um)
        self.ui_cBox_highest_voltage.addItem("User defined", None)
        self.ui_cBox_highest_voltage_neutral.addItem("User defined", None)
        self.updateUm()

        ### Tableau des prises
        self.layout_table = QVBoxLayout(self.ui_widget_table)
        self.ui_tabV_taps = GridTableView()
        self.layout_table.addWidget(self.ui_tabV_taps)
        self.model_tab_taps = QStandardItemModel(self)
        self.ui_tabV_taps.setModel(self.model_tab_taps)
        self.ui_tabV_taps.setSelectionMode(QAbstractItemView.ContiguousSelection)

        # Titre des colonnes
        nb_lignes_header = 2
        lst_titles = []
        k_col = 0
        lst_titles.append(["Tap", [0, k_col, 2, 1]])
        k_col = k_col + 1
        lst_titles.append(["Tap line-line voltage", [0, k_col, 1, 2]])
        lst_titles += [["% main voltage", [1, k_col, 1, 1]], ["kV", [1, k_col + 1, 1, 1]]]
        k_col = k_col + 2
        lst_titles.append(["Tap power (MVA)", [0, k_col, 2, 1]])
        k_col = k_col + 1
        lst_titles.append(["Tap line current (A)", [0, k_col, 2, 1]])
        k_col = k_col + 1

        self.ui_tabV_taps.setGridHeaderview(Qt.Horizontal, nb_lignes_header, k_col)
        hHeader = self.ui_tabV_taps.gridHeaderview(Qt.Horizontal)
        for title in lst_titles:
            hHeader.setSpan(title[1][0], title[1][1], title[1][2], title[1][3])
            hHeader.setCellLabel(title[1][0], title[1][1], title[0])

        # Choix du mode de classement du tableau
        self.model_tab_taps.setSortRole(Qt.EditRole) # Penser à mettre les données numériques de rangement en EditRole et pas en setText (sinon ordre alphabétique)
        self.ui_tabV_taps.horizontalHeader().setSortIndicator(0, Qt.AscendingOrder)

        # Valideurs de champs
        dlg_str_tap = gui_utils.LineEditValidatorDelegate(validator_str_tap, str_fmt="%i", parent=self.ui_tabV_taps)
        self.ui_tabV_taps.setItemDelegateForColumn(0, dlg_str_tap)
        dlg_float_pos = gui_utils.LineEditValidatorDelegate(validator_float_pos, parent=self.ui_tabV_taps)
        self.ui_tabV_taps.setItemDelegateForColumn(1, dlg_float_pos)
        self.ui_tabV_taps.setItemDelegateForColumn(2, dlg_float_pos)
        self.ui_tabV_taps.setItemDelegateForColumn(3, dlg_float_pos)
        self.ui_tabV_taps.setItemDelegateForColumn(4, dlg_float_pos)

        ### Connecteurs
        self.ui_cBox_ydi.currentIndexChanged.connect(self.widg_ratingPlate.updateStudyName)
        self.ui_cBox_n.currentIndexChanged.connect(self.widg_ratingPlate.updateStudyName)
        self.ui_spBox_phase.valueChanged.connect(self.widg_ratingPlate.updateStudyName)

        self.ui_cBox_ydi.currentIndexChanged.connect(self.updateVectorGroupN)
        self.ui_cBox_n.currentIndexChanged.connect(self.updateUm)
        self.ui_cBox_highest_voltage.currentIndexChanged.connect(self.updateUm)
        self.ui_cBox_highest_voltage_neutral.currentIndexChanged.connect(self.updateUm)
        self.ui_grpBox_regWind.toggled.connect(self.updateTapsNumber)
        self.ui_le_voltage.editingFinished.connect(self.updateLabelVoltage)
        self.ui_cBox_ratedTap.currentIndexChanged.connect(self.updateHighlightedTap)
        self.ui_cBox_ratedTap.currentIndexChanged.connect(self.widg_ratingPlate.updateWindingsData)
        self.ui_rbut_standard.toggled.connect(self.updateFillingMethod)
        self.model_tab_taps.itemChanged.connect(self.calculateRow)

        self.ui_le_power.editingFinished.connect(self.calculateTableUpdateWindingsData)
        self.ui_le_voltage.editingFinished.connect(self.calculateTableUpdateWindingsData)

        self.ui_spBox_nbreTaps.valueChanged.connect(self.updateTapsTable)
        self.ui_spBox_nbreTaps_p.valueChanged.connect(self.updateTapsTable)
        self.ui_spBox_nbreTaps_m.valueChanged.connect(self.updateTapsTable)
        self.ui_le_regStep_p.editingFinished.connect(self.updateTapsTable)
        self.ui_le_regStep_m.editingFinished.connect(self.updateTapsTable)

        ### Au démarrage
        self.updateTooltips()
        self.connectModification()
        self.updateVectorGroupYDI()
        self.updateFillingMethod()
        self.updateLabelVoltage()

    def connectModification(self):
        """
        Connection des éléments pour émission du signal isModified
        """
        # Les sous-connections peuvent être activées par l'utilisateur ou programmatiquement
        self.ui_le_name.textEdited.connect(self.emitIsModified)
        self.ui_le_power.textEdited.connect(self.emitIsModified)
        self.ui_le_voltage.textEdited.connect(self.emitIsModified)
        self.ui_le_highest_voltage.textEdited.connect(self.emitIsModified)
        self.ui_le_highest_voltage_neutral.textEdited.connect(self.emitIsModified)
        self.ui_cBox_highest_voltage.currentIndexChanged.connect(self.emitIsModified)
        self.ui_cBox_highest_voltage_neutral.currentIndexChanged.connect(self.emitIsModified)
        self.ui_le_regStep_p.textEdited.connect(self.emitIsModified)
        self.ui_le_regStep_m.textEdited.connect(self.emitIsModified)
        self.ui_cBox_ydi.currentIndexChanged.connect(self.emitIsModified)
        self.ui_cBox_n.currentIndexChanged.connect(self.emitIsModified)
        self.ui_spBox_phase.valueChanged.connect(self.emitIsModified)
        self.ui_spBox_nbreTaps.valueChanged.connect(self.emitIsModified)
        self.ui_grpBox_regWind.toggled.connect(self.emitIsModified)
        self.ui_cBox_ratedTap.currentIndexChanged.connect(self.emitIsModified)
        self.ui_rbut_standard.toggled.connect(self.emitIsModified)
        self.ui_rbut_userDefined.toggled.connect(self.emitIsModified)
        self.model_tab_taps.itemChanged.connect(self.emitIsModified)

    def emitIsModified(self):
        self.isModified.emit()

    def disconnectModification(self):
        """
        Déconnection des éléments à l'émission du signal isModified
        """
        self.ui_le_name.textEdited.disconnect(self.emitIsModified)
        self.ui_le_power.textEdited.disconnect(self.emitIsModified)
        self.ui_le_voltage.textEdited.disconnect(self.emitIsModified)
        self.ui_le_highest_voltage.textEdited.disconnect(self.emitIsModified)
        self.ui_le_highest_voltage_neutral.textEdited.disconnect(self.emitIsModified)
        self.ui_cBox_highest_voltage.currentIndexChanged.disconnect(self.emitIsModified)
        self.ui_cBox_highest_voltage_neutral.currentIndexChanged.disconnect(self.emitIsModified)
        self.ui_le_regStep_p.textEdited.disconnect(self.emitIsModified)
        self.ui_le_regStep_m.textEdited.disconnect(self.emitIsModified)
        self.ui_cBox_ydi.currentIndexChanged.disconnect(self.emitIsModified)
        self.ui_cBox_n.currentIndexChanged.disconnect(self.emitIsModified)
        self.ui_spBox_phase.valueChanged.disconnect(self.emitIsModified)
        self.ui_spBox_nbreTaps.valueChanged.disconnect(self.emitIsModified)
        self.ui_grpBox_regWind.toggled.disconnect(self.emitIsModified)
        self.ui_cBox_ratedTap.currentIndexChanged.disconnect(self.emitIsModified)
        self.ui_rbut_standard.toggled.disconnect(self.emitIsModified)
        self.ui_rbut_userDefined.toggled.disconnect(self.emitIsModified)
        self.model_tab_taps.itemChanged.disconnect(self.emitIsModified)

    def checkDesign(self):
        """
        Vérification du design
        """
        # Liste d'erreurs à corriger
        lst_error = []

        tmp = self.ui_le_name
        if not tmp.hasAcceptableInput():
            tmp.setStyleSheet("background-color: red;")
            lst_error.append("Winding name must only have A-Z or a-z or 0-9 or - or _ characters")
        else:
            tmp.setStyleSheet("")
        tmp = self.ui_le_power
        if not tmp.hasAcceptableInput():
            tmp.setStyleSheet("background-color: red;")
            lst_error.append("Winding rated power value must be strictly positive")
        else:
            tmp.setStyleSheet("")
        tmp = self.ui_le_voltage
        if not tmp.hasAcceptableInput():
            tmp.setStyleSheet("background-color: red;")
            lst_error.append("Winding main voltage value must be strictly positive")
        else:
            tmp.setStyleSheet("")
        tmp = self.ui_le_highest_voltage
        if not tmp.hasAcceptableInput():
            tmp.setStyleSheet("background-color: red;")
            lst_error.append("Winding highest voltage value must be strictly positive")
        else:
            tmp.setStyleSheet("")
        tmp = self.ui_le_highest_voltage_neutral
        if not tmp.hasAcceptableInput() and self.hasNeutralBushing():
            tmp.setStyleSheet("background-color: red;")
            lst_error.append("Winding neutral highest voltage value must be strictly positive")
        else:
            tmp.setStyleSheet("")
        tmp = self.ui_le_regStep_p
        if not tmp.hasAcceptableInput():
            tmp.setStyleSheet("background-color: red;")
            lst_error.append("Winding regulation step value must be positive")
        else:
            tmp.setStyleSheet("")
        tmp = self.ui_le_regStep_m
        if not tmp.hasAcceptableInput():
            tmp.setStyleSheet("background-color: red;")
            lst_error.append("Winding regulation step value must be positive")
        else:
            tmp.setStyleSheet("")

        return lst_error

    def freezeDesign(self, isFrozen):
        """
        Action lors du (dé)gelage du design
        """
        self.ui_grpBox_main.setEnabled(not isFrozen)
        self.ui_grpBox_regWind.setEnabled(not isFrozen)

        if isFrozen:
            self.ui_tabV_taps.setEditTriggers(QAbstractItemView.NoEditTriggers)
        else:
            self.updateFillingMethod()

    def setSelected(self, selected, emitSignal=False):
        """
        Changement d'état de sélection
        """
        if not emitSignal:
            self.winding.selectionChanged.disconnect(self.selectionChanged)
        self.winding.setSelected(selected)
        if not emitSignal:
            self.winding.selectionChanged.connect(self.selectionChanged)
        if selected:
            self.widg_arrangement.show()
        else:
            self.widg_arrangement.hide()

    def isSelected(self):
        """
        Renvoi l'état de sélection
        """
        return self.winding.isSelected()

    def updateTooltips(self):
        """
        Gestion des tooltips
        """
        # ToolTips
        if self.widg_ratingPlate.isMonophase():
            self.ui_cBox_ydi.setToolTip("Consider the 3 phases bank")
        else:
            self.ui_cBox_ydi.setToolTip("")

    def updateVectorGroupYDI(self):
        """
        Mise à jour de la combobox de couplage ydi
        """
        if len(self.widg_ratingPlate.getLstWindingVoltageDescendingNameAlphabetical()) == 0:
            return
        self.ui_cBox_ydi.currentIndexChanged.disconnect(self.emitIsModified)

        old = self.ui_cBox_ydi.currentText()

        # En mono, on considère le banc triphasé
        tmp = ["y", "d"]
        self.ui_cBox_ydi.clear()
        if self.widg_ratingPlate.getLstWindingVoltageDescendingNameAlphabetical()[0] == self:
            tmp_maj = [c.upper() for c in tmp]
            self.ui_cBox_ydi.addItems(tmp_maj)
            if old.upper() in tmp_maj:
                self.ui_cBox_ydi.setCurrentText(old.upper())
            else:
                self.emitIsModified()
        else:
            self.ui_cBox_ydi.addItems(tmp)
            if old.lower() in tmp:
                self.ui_cBox_ydi.setCurrentText(old.lower())
            else:
                self.emitIsModified()

        self.ui_cBox_ydi.currentIndexChanged.connect(self.emitIsModified)

        self.updateVectorGroupN()

    def updateVectorGroupN(self):
        """
        Mise à jour de la combobox de couplage n
        """
        if len(self.widg_ratingPlate.getLstWindingVoltageDescendingNameAlphabetical()) == 0:
            return

        self.ui_cBox_n.currentIndexChanged.disconnect(self.emitIsModified)

        if self.ui_cBox_ydi.currentText().upper() == "Y":
            old = self.ui_cBox_n.currentText()
            tmp = ["n", ""]

            self.ui_cBox_n.clear()
            if self.widg_ratingPlate.getLstWindingVoltageDescendingNameAlphabetical()[0] == self:
                tmp_maj = [c.upper() for c in tmp]
                self.ui_cBox_n.addItems(tmp_maj)
                if old.upper() in tmp_maj:
                    self.ui_cBox_n.setCurrentText(old.upper())
                else:
                    self.emitIsModified()
            else:
                self.ui_cBox_n.addItems(tmp)
                if old.lower() in tmp:
                    self.ui_cBox_n.setCurrentText(old.lower())
                else:
                    self.emitIsModified()

            self.ui_cBox_n.show()
        else:
            self.ui_cBox_n.hide()

        self.ui_cBox_n.currentIndexChanged.connect(self.emitIsModified)

        self.updateVectorGroupD()
        self.updateUm()

    def updateVectorGroupD(self):
        """
        Mise à jour de la spinbox de dephasage
        """
        if len(self.widg_ratingPlate.getLstWindingVoltageDescendingNameAlphabetical()) == 0:
            return

        if self.widg_ratingPlate.getLstWindingVoltageDescendingNameAlphabetical()[0] == self:
            self.ui_spBox_phase.hide()
        else:
            self.ui_spBox_phase.show()

    def updateUm(self):
        """
        MAJ de la visibilité des champs Um
        """
        # Enroulement
        tmp = self.ui_cBox_highest_voltage.currentData()
        if tmp is None:
            self.ui_le_highest_voltage.setEnabled(True)
        else:
            self.ui_le_highest_voltage.setEnabled(False)
            self.ui_le_highest_voltage.setText("%.1f"%tmp)

        # Neutre
        if self.hasNeutralBushing() or self.widg_ratingPlate.isMonophase():
            self.ui_lbl_Um_n.show()
            self.ui_lbl_unit_n.show()
            self.ui_cBox_highest_voltage_neutral.show()
            self.ui_le_highest_voltage_neutral.show()
            tmp = self.ui_cBox_highest_voltage_neutral.currentData()
            if tmp is None:
                self.ui_le_highest_voltage_neutral.setEnabled(True)
            else:
                self.ui_le_highest_voltage_neutral.setEnabled(False)
                self.ui_le_highest_voltage_neutral.setText("%.1f"%tmp)
        else:
            self.ui_cBox_highest_voltage_neutral.hide()
            self.ui_lbl_Um_n.hide()
            self.ui_le_highest_voltage_neutral.hide()
            self.ui_lbl_unit_n.hide()

    def getVectorGroup(self):
        """
        String de représentation du couplage
        """
        vector_group = self.ui_cBox_ydi.currentText()
        if self.ui_cBox_ydi.currentText().upper() == "Y":
            vector_group = vector_group + self.ui_cBox_n.currentText()

        if len(self.widg_ratingPlate.getLstWindingVoltageDescendingNameAlphabetical()) > 0:
            if self.widg_ratingPlate.getLstWindingVoltageDescendingNameAlphabetical()[0] != self:
                vector_group = vector_group + "%i"%self.ui_spBox_phase.value()

        return vector_group

    def getName(self):
        """
        Renvoi le nom de l'enroulement
        """
        return self.ui_le_name.text()

    def updateLabelVoltage(self):
        """
        Mise à jour du label
        """
        try:
            self.ui_lbl_ratedVoltage.setText("%.1f kV"%float(self.ui_le_voltage.text()))
        except:
            self.ui_lbl_ratedVoltage.setText("%s kV"%self.ui_le_voltage.text())

    def updateTapsNumber(self):
        """
        MAJ du nombre de prises
        """
        if not self.ui_grpBox_regWind.isChecked():
            self.ui_spBox_nbreTaps.setValue(1)
            self.ui_spBox_nbreTaps_p.setValue(0)
            self.ui_spBox_nbreTaps_m.setValue(0)
            self.ui_le_regStep_p.setText("0.0")
            self.ui_le_regStep_m.setText("0.0")
            self.ui_rbut_standard.setChecked(True)

        self.widg_ratingPlate.updateStudyName()

    def updateTapsTable(self):
        """
        MAJ du tableau des prises
        """
        # Nombre total de positions
        if self.ui_rbut_standard.isChecked():
            nb_positions = self.ui_spBox_nbreTaps_p.value() + self.ui_spBox_nbreTaps_m.value() + 1
        else:
            nb_positions = self.ui_spBox_nbreTaps.value()

        # Rajout des lignes
        rootItem = self.model_tab_taps.invisibleRootItem()
        for k in range(nb_positions - self.model_tab_taps.rowCount()):
            row = []

            # Prise
            tmp = QStandardItem()
            if self.ui_rbut_userDefined.isChecked():
                tmp.setData(self.model_tab_taps.rowCount()+1, Qt.EditRole)
            tmp.setData(Qt.AlignCenter, Qt.TextAlignmentRole)
            tmp.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable)
            row.append(tmp)

            # Tension % rated
            tmp = QStandardItem("100.0")
            tmp.setData(Qt.AlignCenter, Qt.TextAlignmentRole)
            tmp.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable)
            row.append(tmp)

            # Tension kV
            tmp = QStandardItem(self.ui_le_voltage.text())
            tmp.setData(Qt.AlignCenter, Qt.TextAlignmentRole)
            tmp.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable)
            row.append(tmp)

            # Puissance prise
            tmp = QStandardItem(self.ui_le_power.text())
            tmp.setData(Qt.AlignCenter, Qt.TextAlignmentRole)
            tmp.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable)
            row.append(tmp)

            # Courant de prise
            tmp = QStandardItem("")
            tmp.setData(Qt.AlignCenter, Qt.TextAlignmentRole)
            tmp.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            row.append(tmp)

            rootItem.appendRow(row)
            if self.ui_rbut_userDefined.isChecked():
                self.calculateRow(row[0])

        # Suppression des lignes
        k = nb_positions
        while k < self.model_tab_taps.rowCount():
            self.model_tab_taps.takeRow(k)

        # En fonction du mode de remplissage
        if self.ui_rbut_standard.isChecked():
            # On redéfini les numéros de prises et les % LL
            self.fillFixedRegulationStep(False)
            # No Backgroung
            self.model_tab_taps.itemChanged.disconnect(self.calculateRow)
            for k in range(self.model_tab_taps.rowCount()):
                for r in range(4):
                    self.model_tab_taps.item(k, r).setData(0, Qt.BackgroundRole)
            self.model_tab_taps.itemChanged.connect(self.calculateRow)
        else:
            # Backgroung jaune sur les cases à éditables
            self.model_tab_taps.itemChanged.disconnect(self.calculateRow)
            for k in range(self.model_tab_taps.rowCount()):
                for r in range(4):
                    self.model_tab_taps.item(k, r).setData(QBrush(Qt.yellow), Qt.BackgroundRole)
            self.model_tab_taps.itemChanged.connect(self.calculateRow)

    def calculateTableUpdateWindingsData(self):
        """
        Recalcul du tableau et mise à jour des données bobines
        """
        self.calculateTable()
        self.widg_ratingPlate.updateWindingsData()

    def calculateTable(self):
        """
        Recalcul du tableau
        """
        for k in range(self.model_tab_taps.rowCount()):
            self.calculateRow(self.model_tab_taps.item(k, 1))

    def calculateRow(self, item):
        """
        Recalcul d'une ligne
        """
        self.model_tab_taps.itemChanged.disconnect(self.calculateRow)

        ### Tension
        if self.model_tab_taps.indexFromItem(item).column() != 2:
            # Modification de la tension en % => Calcul du kV
            try:
                u_pc = float(self.model_tab_taps.item(item.row(), 1).text())/100
            except:
                u_pc = None
                u_kV = None
                self.model_tab_taps.item(item.row(), 2).setText("")
            else:
                try:
                    u_kV = u_pc*float(self.ui_le_voltage.text())
                except:
                    u_kV = None
                    self.model_tab_taps.item(item.row(), 2).setText("")
                else:
                    self.model_tab_taps.item(item.row(), 2).setText("%f"%u_kV)

        else:
            # Modification de la tension en kV => Calcul du %
            try:
                u_kV = float(self.model_tab_taps.item(item.row(), 2).text())
            except:
                u_pc = None
                u_kV = None
                self.model_tab_taps.item(item.row(), 1).setText("")
            else:
                try:
                    u_pc = (u_kV/float(self.ui_le_voltage.text()))*100
                except:
                    u_pc = None
                    self.model_tab_taps.item(item.row(), 1).setText("")
                else:
                    self.model_tab_taps.item(item.row(), 1).setText("%f"%u_pc)

        ### Puissance
        if self.ui_rbut_standard.isChecked():
            self.model_tab_taps.item(item.row(), 3).setText(self.ui_le_power.text())
        try:
            s_tap = float(self.model_tab_taps.item(item.row(), 3).text())
        except:
            s_tap = None

        ### Courant de ligne
        if s_tap != None and u_kV != None and u_kV != 0:
            if self.widg_ratingPlate.isMonophase():
                i_line = 3*s_tap*1000/(u_kV*sqrt(3))
            else:
                i_line = s_tap*1000/(u_kV*sqrt(3))
            self.model_tab_taps.item(item.row(), 4).setText("%f"%i_line)
        else:
            self.model_tab_taps.item(item.row(), 4).setText("")

        ### Mise à jour de la liste des tap
        if self.ui_rbut_userDefined.isChecked():
            self.updateTapComboBox()

        self.model_tab_taps.itemChanged.connect(self.calculateRow)

        ### Surlignage de la prise principale
        self.updateHighlightedTap()

        ### Pour le rangement du tableau (nécessite de le rappeler systématiquement)
        if item.column() == 0:
            self.ui_tabV_taps.setSortingEnabled(True)

        ### Mise à jour de la plaque
        self.widg_ratingPlate.updateStudyName()

    def updateFillingMethod(self):
        """
        MAJ de la méthode de remplissage du tableau des prises
        """

        if self.ui_rbut_standard.isChecked():
            self.ui_gBox_fixed.show()
            self.ui_gBox_user.hide()
            self.ui_lbl_fill.hide()
            self.ui_tabV_taps.setEditTriggers(QAbstractItemView.NoEditTriggers)

        else:
            self.ui_gBox_fixed.hide()
            self.ui_gBox_user.show()
            self.ui_lbl_fill.show()
            self.ui_tabV_taps.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed | QAbstractItemView.AnyKeyPressed)

            # Pour ne pas perdre la première mise en données
            self.ui_spBox_nbreTaps.setValue(self.ui_spBox_nbreTaps_p.value() + self.ui_spBox_nbreTaps_m.value() + 1)

            # Liste des prises possibles
            self.updateTapComboBox()

        self.updateTapsTable()
        self.updateHighlightedTap()

    def updateTapComboBox(self):
        """
        Mise à jour de la liste de choix de la prise assignée
        """
        tap_rated = self.getTapRated()
        lst_taps = []
        for row in range(self.model_tab_taps.rowCount()):
            lst_taps.append(self.model_tab_taps.item(row, 0).text())

        self.ui_cBox_ratedTap.currentIndexChanged.disconnect(self.updateHighlightedTap)

        self.ui_cBox_ratedTap.clear()
        self.ui_cBox_ratedTap.addItems(lst_taps)

        if tap_rated in lst_taps:
            self.ui_cBox_ratedTap.setCurrentText(tap_rated)

        self.ui_cBox_ratedTap.currentIndexChanged.connect(self.updateHighlightedTap)

    def fillFixedRegulationStep(self, updateWindingsData=True):
        """
        Remplissage des colonnes avec un pas de régulation fixe
        """
        self.model_tab_taps.itemChanged.disconnect(self.calculateRow)

        row = 0

        # Prises positives
        for k in range(self.ui_spBox_nbreTaps_p.value()):
            # Numéro de prise
            self.model_tab_taps.item(row, 0).setData(row + 1, Qt.EditRole)

            # Pourcentage
            try:
                u_pc = 100 + (self.ui_spBox_nbreTaps_p.value() - k)*float(self.ui_le_regStep_p.text())
            except:
                self.model_tab_taps.item(row, 1).setText("")
            else:
                self.model_tab_taps.item(row, 1).setText("%f"%u_pc)

            row = row + 1

        # Prise médiane
        self.model_tab_taps.item(row, 0).setData(row + 1, Qt.EditRole)
        self.model_tab_taps.item(row, 1).setText("%f"%100)
        row = row + 1

        # Prises négatives
        for k in range(self.ui_spBox_nbreTaps_m.value()):
            # Numéro de prise
            self.model_tab_taps.item(row, 0).setData(row + 1, Qt.EditRole)

            # Pourcentage
            try:
                u_pc = 100 - (k + 1)*float(self.ui_le_regStep_m.text())
            except:
                self.model_tab_taps.item(row, 1).setText("")
            else:
                self.model_tab_taps.item(row, 1).setText("%f"%u_pc)

            row = row + 1

        self.model_tab_taps.itemChanged.connect(self.calculateRow)

        if updateWindingsData:
            self.calculateTableUpdateWindingsData()
        else:
            self.calculateTable()

    def updateHighlightedTap(self):
        """
        Mise en évidence de la ligne prise assignée
        """
        tap_rated = self.getTapRated()
        font_bold = QFont()
        font_bold.setBold(True)
        font_std = QFont()

        self.model_tab_taps.itemChanged.disconnect(self.calculateRow)

        find = False
        for row in range(self.model_tab_taps.rowCount()):
            if self.model_tab_taps.item(row, 0).text() == tap_rated and not find:
                # C'est la première bonne ligne
                for col in range(self.model_tab_taps.columnCount()):
                    self.model_tab_taps.item(row, col).setFont(font_bold)
                find = True
            else:
                for col in range(self.model_tab_taps.columnCount()):
                    self.model_tab_taps.item(row, col).setFont(font_std)

        self.model_tab_taps.itemChanged.connect(self.calculateRow)

    def getStrRegulation(self):
        """
        Renvoi le string d'écriture de la régulation
        """
        if not self.hasTapChanger():
            return ""

        # Il peut y avoir un écart s'il n'y a pas de prise sur la tension indiquée dans main voltage d'où le fait de ne pas prendre les valeurs du tableau
        min_pc = 100.0
        max_pc = 0.0
        try:
            rated_voltage = self.getTapVoltage()
        except:
            rated_voltage = 0.0

        for row in range(self.model_tab_taps.rowCount()):
            try:
                pc = round((float(self.model_tab_taps.item(row, 2).text())/rated_voltage - 1)*100, 3)
            except:
                continue
            min_pc = min(min_pc, pc)
            max_pc = max(max_pc, pc)

        if abs(min_pc) == abs(max_pc):
            tmp = abs(min_pc)
            if tmp.is_integer():
                return u"\u00B1" + "%i%%"%abs(min_pc)
            else:
                return u"\u00B1" + "%.2f%%"%abs(min_pc)
        else:
            tmp = ""
            if max_pc.is_integer():
                tmp += "%+i%%"%max_pc
            else:
                tmp += "%+.2f%%"%max_pc
            if min_pc.is_integer():
                tmp += ", %+i%%"%min_pc
            else:
                tmp += ", %+.2f%%"%min_pc
            return tmp

    def addXMLTree(self, tag_arr, docDom):
        """
        Generation de l'arbre XML
        """
        tag_wn = docDom.createElement("winding")
        tag_arr.appendChild(tag_wn)

        tag_tmp = docDom.createElement('name')
        tag_tmp.appendChild(docDom.createTextNode(self.ui_le_name.text()))
        tag_wn.appendChild(tag_tmp)
        tag_rv = docDom.createElement('rated_values')
        tag_wn.appendChild(tag_rv)
        tag_tmp = docDom.createElement('power_VA')
        tag_tmp.appendChild(docDom.createTextNode("%e"%(float(self.ui_le_power.text())*1e6)))
        tag_rv.appendChild(tag_tmp)
        tag_tmp = docDom.createElement('LL_voltage_V')
        tag_tmp.appendChild(docDom.createTextNode("%e"%(float(self.ui_le_voltage.text())*1e3)))
        tag_rv.appendChild(tag_tmp)
        tag_tmp = docDom.createElement('Um_voltage_choice')
        tag_tmp.appendChild(docDom.createTextNode(self.ui_cBox_highest_voltage.currentText()))
        tag_rv.appendChild(tag_tmp)
        tag_tmp = docDom.createElement('Um_voltage_V')
        tag_tmp.appendChild(docDom.createTextNode("%e"%(float(self.ui_le_highest_voltage.text())*1e3)))
        tag_rv.appendChild(tag_tmp)
        tag_tmp = docDom.createElement('Um_neutral_voltage_choice')
        tag_tmp.appendChild(docDom.createTextNode(self.ui_cBox_highest_voltage_neutral.currentText()))
        tag_rv.appendChild(tag_tmp)
        tag_tmp = docDom.createElement('Um_neutral_voltage_V')
        tag_tmp.appendChild(docDom.createTextNode("%e"%(float(self.ui_le_highest_voltage_neutral.text())*1e3)))
        tag_rv.appendChild(tag_tmp)

        tag_vg = docDom.createElement('vector_group')
        tag_tmp = docDom.createElement('connection')
        tag_tmp.appendChild(docDom.createTextNode(self.ui_cBox_ydi.currentText().lower()))
        tag_vg.appendChild(tag_tmp)
        tag_tmp = docDom.createElement('neutral')
        if self.hasNeutralBushing():
            tag_tmp.appendChild(docDom.createTextNode("yes"))
        else:
            tag_tmp.appendChild(docDom.createTextNode("no"))
        tag_vg.appendChild(tag_tmp)
        tag_tmp = docDom.createElement('displacement')
        if self.widg_ratingPlate.getLstWindingVoltageDescendingNameAlphabetical()[0] != self:
            tag_tmp.appendChild(docDom.createTextNode("%i"%self.ui_spBox_phase.value()))
        else:
            tag_tmp.appendChild(docDom.createTextNode("0"))
        tag_vg.appendChild(tag_tmp)
        tag_rv.appendChild(tag_vg)

        tag_reg = docDom.createElement('regulation')
        # Configuration
        if self.ui_rbut_standard.isChecked():
            tag_reg.setAttribute("filling_method", "standard")
        else:
            tag_reg.setAttribute("filling_method", "user")
        if self.ui_grpBox_regWind.isChecked():
            tag_reg.setAttribute("regulation", "yes")
        else:
            tag_reg.setAttribute("regulation", "no")
        tag_tmp = docDom.createElement('nb_taps')
        tag_tmp.appendChild(docDom.createTextNode("%i"%self.ui_spBox_nbreTaps.value()))
        tag_reg.appendChild(tag_tmp)
        tag_tmp = docDom.createElement('rated_tap')
        tag_tmp.appendChild(docDom.createTextNode("%s"%self.ui_cBox_ratedTap.currentText()))
        tag_reg.appendChild(tag_tmp)
        tag_tmp = docDom.createElement('nb_taps_p')
        tag_tmp.appendChild(docDom.createTextNode("%i"%self.ui_spBox_nbreTaps_p.value()))
        tag_reg.appendChild(tag_tmp)
        tag_tmp = docDom.createElement('reg_step_p')
        tag_tmp.appendChild(docDom.createTextNode("%s"%self.ui_le_regStep_p.text()))
        tag_reg.appendChild(tag_tmp)
        tag_tmp = docDom.createElement('nb_taps_m')
        tag_tmp.appendChild(docDom.createTextNode("%i"%self.ui_spBox_nbreTaps_m.value()))
        tag_reg.appendChild(tag_tmp)
        tag_tmp = docDom.createElement('reg_step_m')
        tag_tmp.appendChild(docDom.createTextNode("%s"%self.ui_le_regStep_m.text()))
        tag_reg.appendChild(tag_tmp)
        # Tableau
        tag_taps = docDom.createElement('taps')
        for row in range(self.model_tab_taps.rowCount()):
            tag_data = docDom.createElement('data')

            tag_tmp = docDom.createElement('tap')
            tag_tmp.appendChild(docDom.createTextNode(self.model_tab_taps.item(row, 0).text()))
            tag_data.appendChild(tag_tmp)
            tag_tmp = docDom.createElement('u_tap_kV')
            tag_tmp.appendChild(docDom.createTextNode(self.model_tab_taps.item(row, 2).text()))
            tag_data.appendChild(tag_tmp)
            tag_tmp = docDom.createElement('s_tap_MVA')
            tag_tmp.appendChild(docDom.createTextNode(self.model_tab_taps.item(row, 3).text()))
            tag_data.appendChild(tag_tmp)

            tag_taps.appendChild(tag_data)
        tag_reg.appendChild(tag_taps)
        tag_rv.appendChild(tag_reg)

    def addPDF(self, pdf, part, lst_id_calcul=[]):
        """
        Remplissage du fichier PDF
        """
        pdf.set_font()

        if "data_general" in part:

            pdf.set_font(style="IU")
            pdf.multi_cell(txt="> Winding %s:"%self.ui_le_name.text())
            pdf.set_font()

            pdf.multi_cell(txt=" "*8 + "Main power: %.3f MVA"%float(self.ui_le_power.text()))
            tmp = " "*8 + "Main line-line voltage: %.3f kV"%float(self.ui_le_voltage.text())
            tmp = tmp + self.getStrRegulation()
            pdf.multi_cell(txt=tmp)
            pdf.multi_cell(txt=" "*8 + "Vector group: %s"%self.getVectorGroup())
            pdf.multi_cell(txt=" "*8 + "Highest applicable line-line voltage: %.3f kV"%float(self.ui_le_highest_voltage.text()))
            if self.hasNeutralBushing():
                pdf.multi_cell(txt=" "*8 + "Highest applicable neutral voltage: %.3f kV"%float(self.ui_le_highest_voltage_neutral.text()))

            # Tableau des valeurs assignées
            row_title = ["Tap", "LL voltage (%)", "LL voltage (kV)", "Power (MVA)", "Current (A)"]
            tab_data = []
            for row in range(self.model_tab_taps.rowCount()):
                data = []
                for col in range(self.model_tab_taps.columnCount()):
                    # Bidouilles pour avoir le même format d'affichage que dans le tableau
                    dlg = self.ui_tabV_taps.itemDelegate(self.model_tab_taps.item(row, col).index())
                    data.append(dlg.displayText(self.model_tab_taps.item(row, col).text(), self.locale))
                tab_data.append(data)
            if len(tab_data) > 0:
                pdf.ln()
                pdf.set_font(style="IU")
                pdf.multi_cell(txt="> Rated tap values:")
                pdf.set_font()
                pdf.multi_cell(txt=" "*8 + "Rated tap: %s"%self.getTapRated())
                pdf.tableMultiCell(row_title, tab_data)

    def addWord(self, tt_template, part="", prefix=""):
        """
        Remplissage du template Word
        """
        tt_template.addHeader("%s"%self.ui_le_name.text(), 4)
        tt_template.addLine("%s_name"%prefix, self.ui_le_name.text())
        tt_template.addLine("%s_Sr"%prefix, self.ui_le_power.text(), unit="MVA")
        tt_template.addLine("%s_Ur"%prefix, self.ui_le_voltage.text(), unit="kV")
        tt_template.addLine("%s_Um"%prefix, self.ui_le_highest_voltage.text(), unit="kV")
        if self.hasNeutralBushing():
            tt_template.addLine("%s_Um_neutral"%prefix, self.ui_le_highest_voltage_neutral.text(), unit="kV")
        tt_template.addLine("%s_Ur_regulation"%prefix, self.getStrRegulation())
        tt_template.addLine("%s_nb_tap"%prefix, self.model_tab_taps.rowCount())
        tt_template.addLine("%s_rated_tap"%prefix, self.getTapRated())
        tt_template.addLine("%s_vector_group"%prefix, self.getVectorGroup())

        # Tableau des tensions / courants...
        tab_data = []
        for row in range(self.model_tab_taps.rowCount()):
            data = []
            for col in range(self.model_tab_taps.columnCount()):
                data.append(self.model_tab_taps.item(row, col).text())
            tab_data.append(data)
        row_title = ["Tap", "LL voltage (%)", "LL voltage (kV)", "Power (MVA)", "Current (A)"]
        tt_template.addTableRow("%s_rated_values"%prefix, [row_title] + tab_data)
        row_title = ["Prise", "Tension LL (%)", "Tension LL (kV)", "Puissance (MVA)", "Courant (A)"]
        tt_template.addTableRow("%s_rated_values_FR"%prefix, [row_title] + tab_data)

    def loadXMLTree(self, wind_elt):
        """
        Chargement de l'arbre XML
        """
        self.disconnectModification()
        self.ui_cBox_ydi.currentIndexChanged.disconnect(self.updateVectorGroupN)
        self.ui_le_power.editingFinished.disconnect(self.calculateTableUpdateWindingsData)
        self.ui_le_voltage.editingFinished.disconnect(self.calculateTableUpdateWindingsData)
        self.ui_cBox_ratedTap.currentIndexChanged.disconnect(self.widg_ratingPlate.updateWindingsData)

        # Chargement à partir de l'élément d'enroulement
        self.ui_le_name.setText(wind_elt.firstChildElement("name").text())

        e_rv = wind_elt.firstChildElement("rated_values")
        self.ui_le_power.setText("%f"%(float(e_rv.firstChildElement("power_VA").text())/1e6))
        self.ui_le_voltage.setText("%f"%(float(e_rv.firstChildElement("LL_voltage_V").text())/1e3))
        if not e_rv.firstChildElement("Um_voltage_V").isNull():
            self.ui_cBox_highest_voltage.setCurrentText(e_rv.firstChildElement("Um_voltage_choice").text())
            self.ui_le_highest_voltage.setText("%f"%(float(e_rv.firstChildElement("Um_voltage_V").text())/1e3))
            self.ui_cBox_highest_voltage_neutral.setCurrentText(e_rv.firstChildElement("Um_neutral_voltage_choice").text())
            self.ui_le_highest_voltage_neutral.setText("%f"%(float(e_rv.firstChildElement("Um_neutral_voltage_V").text())/1e3))
            self.updateUm()
        self.updateLabelVoltage()

        e_vg = e_rv.firstChildElement("vector_group")
        lst_cBox = [self.ui_cBox_ydi.itemText(i) for i in range(self.ui_cBox_ydi.count())]
        tmp = e_vg.firstChildElement("connection").text()
        if tmp.upper() in lst_cBox:
            self.ui_cBox_ydi.setCurrentText(tmp.upper())
        else:
            self.ui_cBox_ydi.setCurrentText(tmp.lower())
        if e_vg.firstChildElement("neutral").text() == "yes":
            lst_cBox = [self.ui_cBox_n.itemText(i) for i in range(self.ui_cBox_n.count())]
            tmp = "n"
            if tmp.upper() in lst_cBox:
                self.ui_cBox_n.setCurrentText(tmp.upper())
            else:
                self.ui_cBox_n.setCurrentText(tmp.lower())
        else:
            self.ui_cBox_n.setCurrentText("")
        self.ui_spBox_phase.setValue(int(e_vg.firstChildElement("displacement").text()))

        e_reg = e_rv.firstChildElement("regulation")
        if e_reg.attribute("filling_method") == '':
            # Ancien mode de définition du réglage
            self.ui_rbut_standard.setChecked(True)
            nb_taps = int(e_reg.attribute("nb_taps"))
            self.ui_spBox_nbreTaps_m.setValue(int((nb_taps - 1)/2))
            self.ui_spBox_nbreTaps_p.setValue(nb_taps - self.ui_spBox_nbreTaps_m.value() - 1)
            self.ui_le_regStep_p.setText("%.2f"%float(e_reg.attribute("tap_step_100-1")))
            self.ui_le_regStep_m.setText("%.2f"%float(e_reg.attribute("tap_step_100-1")))
            if nb_taps > 1:
                self.ui_grpBox_regWind.setChecked(True)
            self.fillFixedRegulationStep(False)
        else:
            # Nouveau mode de définition du réglage
            if e_reg.attribute("filling_method") == 'standard':
                self.ui_rbut_standard.setChecked(True)
            else:
                self.ui_rbut_userDefined.setChecked(True)
            if e_reg.attribute("regulation") == 'yes':
                self.ui_grpBox_regWind.setChecked(True)
            self.ui_spBox_nbreTaps.setValue(int(e_reg.firstChildElement("nb_taps").text()))
            self.ui_spBox_nbreTaps_p.setValue(int(e_reg.firstChildElement("nb_taps_p").text()))
            self.ui_spBox_nbreTaps_m.setValue(int(e_reg.firstChildElement("nb_taps_m").text()))
            self.ui_le_regStep_p.setText(e_reg.firstChildElement("reg_step_p").text())
            self.ui_le_regStep_m.setText(e_reg.firstChildElement("reg_step_m").text())

            # Remplissage du tableau si on est en mode user
            if self.ui_rbut_userDefined.isChecked():
                self.updateTapsTable()

                e_taps = e_reg.firstChildElement("taps")
                n = e_taps.firstChildElement("data")
                row = 0
                while not n.isNull():
                    e_data = n.toElement()

                    e_tmp = e_data.firstChildElement("tap")
                    try:
                        tap = int(e_tmp.text())
                    except:
                        tap = e_tmp.text()
                    self.model_tab_taps.item(row, 0).setData(tap, Qt.EditRole)
                    e_tmp = e_data.firstChildElement("u_tap_kV")
                    self.model_tab_taps.item(row, 2).setText(e_tmp.text())
                    e_tmp = e_data.firstChildElement("s_tap_MVA")
                    self.model_tab_taps.item(row, 3).setText(e_tmp.text())

                    n = n.nextSiblingElement("data")
                    row = row + 1

                self.updateTapComboBox()

            else:
                # Calculs si mode standard
                self.fillFixedRegulationStep(False)

            self.ui_cBox_ratedTap.setCurrentText(e_reg.firstChildElement("rated_tap").text())

        self.connectModification()
        self.ui_cBox_ratedTap.currentIndexChanged.connect(self.widg_ratingPlate.updateWindingsData)
        self.ui_le_power.editingFinished.connect(self.calculateTableUpdateWindingsData)
        self.ui_le_voltage.editingFinished.connect(self.calculateTableUpdateWindingsData)
        self.ui_cBox_ydi.currentIndexChanged.connect(self.updateVectorGroupN)

        self.widg_ratingPlate.updateWindingsData()

# =============================================================================
# Calcul de caractéristiques électriques de l'enroulement
# =============================================================================
    def hasNeutralBushing(self):
        """
        Renvoi True si l'enroulement à un neutre sorti
        """
        if self.ui_cBox_ydi.currentText().upper() == "Y":
            if self.ui_cBox_n.currentText().upper() == "N":
                return True
        return False

    def hasTapChanger(self):
        """
        Renvoi True si l'enroulement à un changeur de prise et plus d'une prise
        """
        if self.ui_rbut_standard.isChecked():
            return (self.ui_spBox_nbreTaps_p.value() + self.ui_spBox_nbreTaps_m.value()) > 0 and self.ui_grpBox_regWind.isChecked()
        else:
            return self.ui_spBox_nbreTaps.value() > 1 and self.ui_grpBox_regWind.isChecked()

    def getTapRated(self):
        """
        Renvoi la prise assignée
        """
        if self.ui_rbut_standard.isChecked():
            tap_rated = "%i"%(self.ui_spBox_nbreTaps_p.value() + 1)
        else:
            tap_rated = self.ui_cBox_ratedTap.currentText()

        return tap_rated

    def getNbrePositions(self):
        """
        Renvoi le nombre de positions
        """
        if self.ui_rbut_standard.isChecked():
            nb_pos = self.ui_spBox_nbreTaps_p.value() + self.ui_spBox_nbreTaps_m.value() + 1
        else:
            nb_pos = self.ui_spBox_nbreTaps.value()

        return nb_pos

    def getLstPositions(self):
        """
        Renvoi la liste des positions
        """
        lst_taps = []
        for row in range(self.model_tab_taps.rowCount()):
            lst_taps.append(self.model_tab_taps.item(row, 0).text())
        return lst_taps

    def getTapVoltage(self, tap=None):
        """
        Calcul de la tension LL de prise sur la prise spécifiée (sinon rated) (kV)
        """
        if tap is None:
            tap = self.getTapRated()

        for row in range(self.model_tab_taps.rowCount()):
            if self.model_tab_taps.item(row, 0).text() == tap:
                try:
                    u_tap = float(self.model_tab_taps.item(row, 2).text())
                except:
                    u_tap = 0.0

                return u_tap

        return None

    def getTapPower(self, tap=None):
        """
        Récupération de la puissance de prise sur la prise spécifiée (sinon rated) (MVA)
        """
        if tap is None:
            tap = self.getTapRated()

        for row in range(self.model_tab_taps.rowCount()):
            if self.model_tab_taps.item(row, 0).text() == tap:
                try:
                    s_tap = float(self.model_tab_taps.item(row, 3).text())
                except:
                    s_tap = 0.0

                return s_tap

        return None

    def getTapCurrent(self, tap=None, s_r=None):
        """
        Calcul des courants assignés sur la prise spécifiée (sinon rated) et pour la puissance donnée (sinon de prise) (A)
        """
        if tap is None:
            tap = self.getTapRated()
        if s_r is None:
            s_r = self.getTapPower(tap)
            if s_r is None:
                return [None, None]

        # Puissance de l'enroulement (kVA)
        s_r = s_r*1e3

        # Tension assignée de l'enroulement (kV)
        u_r = self.getTapVoltage(tap)
        if u_r is None:
            return [None, None]

        # Courant assigné de ligne (A)
        if self.widg_ratingPlate.isMonophase():
            i_line = 3*s_r/(u_r*sqrt(3))
        else:
            i_line = s_r/(u_r*sqrt(3))

        # Courant assigné de la bobine (A)
        if self.ui_cBox_ydi.currentText().upper() == 'Y':
            i_coil = i_line
        else:
            # on est sur un enroulement delta
            i_coil = i_line/sqrt(3)

        return [i_line, i_coil]

    def getHighestVoltage(self, neutral_included=True):
        """
        Renvoi la tension maximale admissible de l'enroulement avec ou sans le neutre
        """
        tmp = self.ui_cBox_highest_voltage.currentData()
        if tmp is None:
            try:
                um = float(self.ui_le_highest_voltage.text())
            except:
                return None
        else:
            um = tmp

        if neutral_included:
            um_n = self.getHighestVoltageNeutral()
            if um_n is None:
                return um
            return min(um, um_n)
        return um

    def getHighestVoltageNeutral(self):
        """
        Renvoi la tension maximale admissible sur le neutre
        """
        if self.hasNeutralBushing() or self.widg_ratingPlate.isMonophase():
            tmp = self.ui_cBox_highest_voltage_neutral.currentData()
            if tmp is None:
                try:
                    um_n = float(self.ui_le_highest_voltage_neutral.text())
                except:
                    return None
                return um_n
            else:
                return tmp
        return None

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
    win = UI_WindingData()

    # 3 - Affichage de la fenêtre
    win.show()

    app.exec()