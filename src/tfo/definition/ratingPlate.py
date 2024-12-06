# -*- coding: utf-8 -*-
import sys
from os import makedirs
from os.path import join, dirname, realpath, exists

from PySide6.QtGui import QDoubleValidator, QRegularExpressionValidator, QStandardItemModel, QIcon, QStandardItem, QBrush
from PySide6.QtCore import Qt, Signal, QRegularExpression, QLocale, QIODevice, QTextStream, QFile, QItemSelection
from PySide6.QtWidgets import QVBoxLayout, QGraphicsScene, QFrame, QHeaderView, QWidget
from PySide6.QtXml import QDomDocument

from .winding_arrangement import UI_WindingArrangement
from ..utils import gui_geom
from ..utils import gui_utils
from ..utils.GridTableView import GridTableView

from .ratingPlate_ui import Ui_Form

# =============================================================================
# Fenetre de definitions de la plaque signalitique du transformateur
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

class UI_RatingPlate(QWidget, Ui_Form):

    # Signal quand le widget est modifié par l'utilisateur (non programmatiquement)
    isModified = Signal()
    # Signal quand la study est MAJ
    studyNameUpdated = Signal(str)

    def __init__(self, ui_main, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.ui_main = ui_main

        self.setup()

    def setup(self):

        self.locale = QLocale("en")
        self.locale.setNumberOptions(QLocale.RejectGroupSeparator)

        ### Pour la génération du pdf
        self.pdf_order = 10

        # Passage en gras de certains titres
        self.ui_grpBox_guarantee.setStyleSheet("QGroupBox { font-weight: bold; } ")
        self.ui_grpBox_windArr.setStyleSheet("QGroupBox { font-weight: bold; } ")
        self.ui_grpBox_coolData.setStyleSheet("QGroupBox { font-weight: bold; } ")
        self.ui_grpBox_method.setStyleSheet("QGroupBox { font-weight: bold; } ")
        self.ui_grpBox_power.setStyleSheet("QGroupBox { font-weight: bold; } ")
        self.ui_grpBox_fansModulation.setStyleSheet("QGroupBox { font-weight: bold; } ")
        self.ui_grpBox_subExchangersModulation.setStyleSheet("QGroupBox { font-weight: bold; } ")

        # Une jolie icone
        self.ui_btn_add.setIcon(QIcon(join(PATHRC, "add.png")))
        self.ui_btn_delete.setIcon(QIcon(join(PATHRC, "edit-delete.png")))
        self.ui_btn_new_FM.setIcon(QIcon(join(PATHRC, "add.png")))
        self.ui_btn_delete_FM.setIcon(QIcon(join(PATHRC, "edit-delete.png")))
        self.ui_btn_new_EM.setIcon(QIcon(join(PATHRC, "add.png")))
        self.ui_btn_delete_EM.setIcon(QIcon(join(PATHRC, "edit-delete.png")))
        self.ui_btn_fat_id.setIcon(self.ui_main.action_fatID.icon())
        self.ui_btn_ope_id.setIcon(self.ui_main.action_opeID.icon())

        # Splitter
        self.ui_splitter_windings.setStretchFactor(1, 1)
        self.ui_splitter_main.setStretchFactor(1, 1)
        self.ui_splitter_tfo.setStretchFactor(1, 1)

        # Remplacement du QLineEdit et application d'un format d'affichage
        self.ui_le_nbreFans_FM = gui_utils.QLineEditFormat(self.ui_le_nbreFans_FM.parent()).replaceWidget(self.ui_le_nbreFans_FM)
        self.ui_le_nbreFans_FM.setDisplayFormat("%i")
        self.ui_le_nbreSubExchangers_EM = gui_utils.QLineEditFormat(self.ui_le_nbreSubExchangers_EM.parent()).replaceWidget(self.ui_le_nbreSubExchangers_EM)
        self.ui_le_nbreSubExchangers_EM.setDisplayFormat("%i")

        ### Number of phases
        self.ui_cb_nbrePhases.addItems(["%i" % 1, "%i" % 3])

        ### Type of cooling
        self.ui_cb_cool_refInt.addItems(["O", "K", "L"])
        self.ui_cb_cool_refIntMode.addItems(["N", "F", "D"])
        self.ui_cb_cool_refExt.addItems(["A", "W"])
        self.ui_cb_cool_refExtMode.addItems(["N", "F"])
        self.ui_cb_oil_flow_unit.addItems(["m3/h", "l/s"])
        self.ui_cb_water_flow_unit.addItems(["m3/h", "l/s"])

        self.ui_spBox_nbOilPumps.setMinimum(1)
        self.ui_spBox_nbOilPumps.setMaximum(100)
        self.ui_spBox_nbWaterPumps.setMinimum(1)
        self.ui_spBox_nbWaterPumps.setMaximum(100)
        self.ui_spBox_nbrePumps_FM.setMinimum(1)
        self.ui_spBox_nbrePumps_FM.setMaximum(100)
        self.ui_spBox_nbreFans_EM.setMinimum(1)
        self.ui_spBox_nbreFans_EM.setMaximum(100)

        ### Tableau des stades de réfrigération - fans modulation
        layout_table = QVBoxLayout(self.ui_widget_FM)
        self.ui_tabV_FM = GridTableView()
        layout_table.addWidget(self.ui_tabV_FM)
        self.model_tab_FM = QStandardItemModel(self)
        self.ui_tabV_FM.setModel(self.model_tab_FM)
        # Titre des colonnes
        lst_titles = ["Cooling stage", "No. of fans\nin operation", "Temp. switch on\nToil > °C", "Temp. switch off\nToil < °C"]
        self.model_tab_FM.setHorizontalHeaderLabels(lst_titles)
        self.model_tab_FM.setColumnCount(len(lst_titles))
        # Pas de numéros de lignes
        self.ui_tabV_FM.verticalHeader().setVisible(False)
        # Largeur auto des colonnes
        self.ui_tabV_FM.horizontalHeader().setStretchLastSection(True)
        self.ui_tabV_FM.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # Délégué pour les nombres de fans
        dlg_spbox_nbreFans = gui_utils.SpinBoxDelegate(minValue=0, maxValue=100, parent=self.ui_tabV_FM)
        self.ui_tabV_FM.setItemDelegateForColumn(1, dlg_spbox_nbreFans)
        # Initialisation
        row = []
        # Stade
        tmp = QStandardItem("1")
        tmp.setData(Qt.AlignCenter, Qt.TextAlignmentRole)
        tmp.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        row.append(tmp)
        # Nbre fans
        tmp = QStandardItem("1")
        tmp.setData(Qt.AlignCenter, Qt.TextAlignmentRole)
        tmp.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable)
        tmp.setData(QBrush(Qt.yellow), Qt.BackgroundRole)
        row.append(tmp)
        # T on
        tmp = QStandardItem("NA")
        tmp.setData(Qt.AlignCenter, Qt.TextAlignmentRole)
        tmp.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        row.append(tmp)
        # T off
        tmp = QStandardItem("NA")
        tmp.setData(Qt.AlignCenter, Qt.TextAlignmentRole)
        tmp.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        row.append(tmp)
        rootItem = self.model_tab_FM.invisibleRootItem()
        rootItem.appendRow(row)

        ### Tableau des stades de réfrigération - sub-exchanger modulation
        layout_table = QVBoxLayout(self.ui_widget_EM)
        self.ui_tabV_EM = GridTableView()
        layout_table.addWidget(self.ui_tabV_EM)
        self.model_tab_EM = QStandardItemModel(self)
        self.ui_tabV_EM.setModel(self.model_tab_EM)
        # Titre des colonnes
        lst_titles = ["Cooling stage", "No. of\nsub-exchangers\nin operation", "Temp. switch on\nToil > °C", "Temp. switch off\nToil < °C"]
        self.model_tab_EM.setHorizontalHeaderLabels(lst_titles)
        self.model_tab_EM.setColumnCount(len(lst_titles))
        # Pas de numéros de lignes
        self.ui_tabV_EM.verticalHeader().setVisible(False)
        # Largeur auto des colonnes
        self.ui_tabV_EM.horizontalHeader().setStretchLastSection(True)
        self.ui_tabV_EM.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # Délégué pour les nombres de fans
        dlg_spbox_nbreFans = gui_utils.SpinBoxDelegate(minValue=0, maxValue=100, parent=self.ui_tabV_EM)
        self.ui_tabV_EM.setItemDelegateForColumn(1, dlg_spbox_nbreFans)
        # Initialisation
        row = []
        # Stade
        tmp = QStandardItem("1")
        tmp.setData(Qt.AlignCenter, Qt.TextAlignmentRole)
        tmp.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        row.append(tmp)
        # Nbre fans
        tmp = QStandardItem("1")
        tmp.setData(Qt.AlignCenter, Qt.TextAlignmentRole)
        tmp.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable)
        tmp.setData(QBrush(Qt.yellow), Qt.BackgroundRole)
        row.append(tmp)
        # T on
        tmp = QStandardItem("NA")
        tmp.setData(Qt.AlignCenter, Qt.TextAlignmentRole)
        tmp.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        row.append(tmp)
        # T off
        tmp = QStandardItem("NA")
        tmp.setData(Qt.AlignCenter, Qt.TextAlignmentRole)
        tmp.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        row.append(tmp)
        rootItem = self.model_tab_EM.invisibleRootItem()
        rootItem.appendRow(row)

        ### Frequence
        self.ui_cb_frequency.addItem("50", 50)
        self.ui_cb_frequency.addItem("60", 60)

        # Ajouts de valideurs de champs
        validator_float_pos = QDoubleValidator(self) # Float positif
        validator_float_pos.setBottom(0.001)
        validator_float_pos.setNotation(QDoubleValidator.StandardNotation)
        validator_float_pos.setLocale(self.locale)
        validator_float_all = QDoubleValidator(self) # Float
        validator_float_all.setNotation(QDoubleValidator.StandardNotation)
        validator_float_all.setLocale(self.locale)
        validator_str = QRegularExpressionValidator(QRegularExpression("[A-Za-z0-9-_]+"), self)

        # Application des valideurs
        self.ui_le_reference.setValidator(validator_str)
        self.ui_le_oilFlow.setValidator(validator_float_pos)
        self.ui_le_waterFlow.setValidator(validator_float_pos)
        self.ui_le_bottomTR.setValidator(validator_float_pos)
        self.ui_le_ambientT.setValidator(validator_float_all)
        self.ui_le_powerPump.setValidator(validator_float_pos)
        self.ui_le_powerFan.setValidator(validator_float_pos)

        dlg_float_pos_FM = gui_utils.LineEditValidatorDelegate(validator_float_pos, parent=self.ui_tabV_FM)
        self.ui_tabV_FM.setItemDelegateForColumn(2, dlg_float_pos_FM)
        self.ui_tabV_FM.setItemDelegateForColumn(3, dlg_float_pos_FM)
        dlg_float_pos_EM = gui_utils.LineEditValidatorDelegate(validator_float_pos, parent=self.ui_tabV_EM)
        self.ui_tabV_EM.setItemDelegateForColumn(2, dlg_float_pos_EM)
        self.ui_tabV_EM.setItemDelegateForColumn(3, dlg_float_pos_EM)

        ### Tolérances
        self.tolerance_topOilGTR = gui_utils.define_tolerance_on_button(self.ui_btn_tolerance_topOilGTR, id_tolerance="TR_top_oil", parent=self)
        self.tolerance_aveWindGTR = gui_utils.define_tolerance_on_button(self.ui_btn_tolerance_aveWindGTR, id_tolerance="TR_average_winding", parent=self)
        self.tolerance_hsGTR = gui_utils.define_tolerance_on_button(self.ui_btn_tolerance_hsGTR, id_tolerance="TR_hot_spot", parent=self)

        # Initialisations
        self.ui_le_oilFlow.setText("1.0")
        self.ui_le_waterFlow.setText("1.0")
        self.ui_le_bottomTR.setText("10.0")
        self.ui_le_ambientT.setText("20.0")
        self.ui_cb_cool_refInt.setCurrentText("O")
        self.ui_cb_cool_refIntMode.setCurrentText("D")
        self.ui_cb_cool_refExt.setCurrentText("A")
        self.ui_cb_cool_refExtMode.setCurrentText("F")
        self.cooling_mode = ""
        self.ui_cb_oil_flow_unit.setCurrentText("m3/h")

        self.ui_rbut_fans.setChecked(True)
        self.ui_le_nbreFans_FM.setEnabled(False)
        self.ui_le_nbreSubExchangers_EM.setEnabled(False)

        self.ui_btn_freeze.hide()
        self.ui_btn_fat_id.hide()
        self.ui_btn_ope_id.hide()

        # Pour que l'onglet Main s'affiche à l'ouverture (sinon c'est l'onglet sur lequel on était lors de l'enregistrement dans Designer qui se mettra)
        self.ui_tabWidget.setCurrentIndex(0)

        ### Données pour la vue
        self.data_view = {}
        self.data_view["L_CM"] = 50.0
        self.data_view["H_fen"] = 125.0
        self.data_view["L_coil"] = 15.0
        self.data_view["e_wind_vert"] = 10.0
        self.data_view["e_wind_hori"] = 5.0

        # Pour l'empilage des graphics
        self.z_value_cm = 0.0
        self.z_value_wind = self.z_value_cm + 1

        self.lst_UI_WindingArrangement = []
        self.CM_graphic = gui_geom.MagneticCircuit(self.data_view["L_CM"])
        self.CM_graphic.setZValue(self.z_value_cm)

        ### Préparation de la représentation du transfo
        self.ui_frame_displayTfo.setMinimumSize(200, 200)
        layout_qFrame = QVBoxLayout(self.ui_frame_displayTfo)
        self.ui_frame_displayTfo.setLayout(layout_qFrame)
        self.ui_frame_displayTfo.setFrameShape(QFrame.NoFrame)
        self.scene_tfo = QGraphicsScene(self.ui_frame_displayTfo)
        self.view_tfo_clickable = gui_utils.ViewResizeAuto(self.scene_tfo)
        self.view_tfo_nonClickable = gui_utils.ViewNonClickable(self.scene_tfo)
        layout_qFrame.addWidget(self.view_tfo_clickable)
        layout_qFrame.addWidget(self.view_tfo_nonClickable)
        self.scene_tfo.addItem(self.CM_graphic)

        ### Légende
        layout_qFrame = QVBoxLayout(self.ui_frame_lgdTfo)
        self.ui_frame_lgdTfo.setLayout(layout_qFrame)
        self.scene_lgdTfo = QGraphicsScene(self.ui_frame_lgdTfo)
        self.view_lgdTfo = gui_utils.ViewResizeAuto(self.scene_lgdTfo)
        layout_qFrame.addWidget(self.view_lgdTfo)
        self.ui_frame_lgdTfo.setMaximumHeight(100.0)
        self.ui_frame_lgdTfo.setMaximumWidth(300.0)
        self.ui_frame_lgdTfo.setFrameShape(QFrame.NoFrame)

        dico_lgd = {}
        dico_lgd["Positive winding direction"] = [-1, gui_geom.COLOR_positive]
        dico_lgd["Negative winding direction"] = [-1, gui_geom.COLOR_negative]
        lgd = gui_geom.Legend()
        self.scene_lgdTfo.addItem(lgd)
        lgd.setLegend(dico_lgd)

        ### Disposition des enroulements
        self.layout_windArr = QVBoxLayout(self.ui_wdg_windArr)
        self.ui_rbut_core.setChecked(True)

        ### Préparation de l'affichage de la liste des enroulements
        self.ui_list_wind.setMinimumSize(150, 100)
        self.model_lst_wind = QStandardItemModel()
        self.ui_list_wind.setModel(self.model_lst_wind)
        # Ajout d'un layout au ui_frame_windData
        self.layout_wind = QVBoxLayout(self.ui_frame_windData)

        ### Connecteurs
        self.ui_le_reference.textEdited.connect(self.updateStudyName)
        self.ui_cb_frequency.currentIndexChanged.connect(self.updateStudyName)
        self.ui_cb_nbrePhases.currentIndexChanged.connect(self.updateNbPhases)
        self.ui_cb_nbrePhases.currentIndexChanged.connect(self.updateWindingsData)
        self.ui_rbut_core.toggled.connect(self.updateDesign)
        self.ui_rbut_core.toggled.connect(self.ui_main.changeMode)
        self.ui_btn_add.clicked.connect(self.addArrangement)
        self.ui_btn_delete.clicked.connect(self.deleteArrangement)
        self.scene_tfo.selectionChanged.connect(self.deleteArrBtn)

        self.ui_cb_nbreLimbs.currentIndexChanged.connect(self.updateMagneticCircuit)
        self.ui_cb_cool_refInt.currentIndexChanged.connect(self.updateCooling)
        self.ui_cb_cool_refInt.currentIndexChanged.connect(self.ui_main.changeMode)
        self.ui_cb_cool_refIntMode.currentIndexChanged.connect(self.updateCooling)
        self.ui_cb_cool_refIntMode.currentIndexChanged.connect(self.ui_main.changeMode)
        self.ui_cb_cool_refExt.currentIndexChanged.connect(self.updateCooling)
        self.ui_cb_cool_refExt.currentIndexChanged.connect(self.ui_main.changeMode)
        self.ui_cb_cool_refExtMode.currentIndexChanged.connect(self.updateCooling)
        self.ui_cb_cool_refExtMode.currentIndexChanged.connect(self.ui_main.changeMode)

        self.ui_list_wind.selectionModel().selectionChanged.connect(self.changeWinding)
        self.ui_tabWidget.currentChanged.connect(self.changeTab)

        self.ui_rbut_fans.toggled.connect(self.changeCoolersMethod)
        self.ui_rbut_subExchangers.toggled.connect(self.changeCoolersMethod)
        self.ui_btn_new_FM.clicked.connect(self.newCoolingStageFM)
        self.ui_btn_delete_FM.clicked.connect(self.deleteCoolingStageFM)
        self.model_tab_FM.itemChanged.connect(self.updateNbreFans)
        self.ui_btn_new_EM.clicked.connect(self.newCoolingStageEM)
        self.ui_btn_delete_EM.clicked.connect(self.deleteCoolingStageEM)
        self.model_tab_EM.itemChanged.connect(self.updateNbreSubExchangers)

        try:
            self.ui_btn_freeze.clicked.connect(self.ui_main.action_Freeze.trigger)
            self.ui_btn_fat_id.clicked.connect(self.ui_main.action_fatID.trigger)
            self.ui_btn_ope_id.clicked.connect(self.ui_main.action_opeID.trigger)
        except:
            # Cas de la version DR
            self.ui_btn_freeze.hide()
            self.ui_btn_fat_id.hide()
            self.ui_btn_ope_id.hide()

        self.ui_main.isFrozen.connect(self.freezeDesign)

        ### Au démarrage
        self.changeTab()
        self.updateCooling()
        self.changeCoolersMethod()
        self.updateNbreFans()
        self.updateNbreSubExchangers()
        self.updateNbPhases()

        # On met par défaut 2 enroulements
        warr = self.addArrangement()
        warr.lst_UI_WindingData[0].ui_le_name.setText("LV")
        warr = self.addArrangement()
        warr.ui_rBut_negDir.setChecked(True) # On met le 2nd enroulement en direction négative
        warr.lst_UI_WindingData[0].ui_le_name.setText("HV")

        self.connectModification()

    def connectModification(self):
        """
        Connection des éléments pour émission du signal isModified
        """
        # Les sous-connections peuvent être activées par l'utilisateur ou programmatiquement
        self.ui_spBox_nbOilPumps.valueChanged.connect(self.emitIsModified)
        self.ui_spBox_nbWaterPumps.valueChanged.connect(self.emitIsModified)
        self.ui_le_oilFlow.textEdited.connect(self.emitIsModified)
        self.ui_le_waterFlow.textEdited.connect(self.emitIsModified)
        self.ui_cb_oil_flow_unit.currentIndexChanged.connect(self.emitIsModified)
        self.ui_cb_water_flow_unit.currentIndexChanged.connect(self.emitIsModified)
        self.ui_le_bottomTR.textEdited.connect(self.emitIsModified)
        self.ui_le_ambientT.textEdited.connect(self.emitIsModified)
        self.ui_le_reference.textEdited.connect(self.emitIsModified)
        self.ui_cb_frequency.currentIndexChanged.connect(self.emitIsModified)
        self.ui_cb_nbrePhases.currentIndexChanged.connect(self.emitIsModified)
        self.ui_rbut_core.toggled.connect(self.emitIsModified)
        self.ui_cb_nbreLimbs.currentIndexChanged.connect(self.emitIsModified)
        self.ui_cb_cool_refInt.currentIndexChanged.connect(self.emitIsModified)
        self.ui_cb_cool_refIntMode.currentIndexChanged.connect(self.emitIsModified)
        self.ui_cb_cool_refExt.currentIndexChanged.connect(self.emitIsModified)
        self.ui_cb_cool_refExtMode.currentIndexChanged.connect(self.emitIsModified)
        self.ui_btn_add.clicked.connect(self.emitIsModified)
        self.ui_btn_delete.clicked.connect(self.emitIsModified)
        self.ui_rbut_fans.toggled.connect(self.emitIsModified)
        self.ui_rbut_subExchangers.toggled.connect(self.emitIsModified)
        self.ui_le_powerPump.textEdited.connect(self.emitIsModified)
        self.ui_le_powerFan.textEdited.connect(self.emitIsModified)
        self.model_tab_FM.itemChanged.connect(self.emitIsModified)
        self.ui_spBox_nbrePumps_FM.valueChanged.connect(self.emitIsModified)
        self.model_tab_EM.itemChanged.connect(self.emitIsModified)
        self.ui_spBox_nbreFans_EM.valueChanged.connect(self.emitIsModified)
        self.tolerance_topOilGTR.updated.connect(self.emitIsModified)
        self.tolerance_aveWindGTR.updated.connect(self.emitIsModified)
        self.tolerance_hsGTR.updated.connect(self.emitIsModified)

    def emitIsModified(self):
        self.isModified.emit()

    def disconnectModification(self):
        """
        Déconnection des éléments à l'émission du signal isModified
        """
        self.ui_spBox_nbOilPumps.valueChanged.disconnect(self.emitIsModified)
        self.ui_spBox_nbWaterPumps.valueChanged.disconnect(self.emitIsModified)
        self.ui_le_oilFlow.textEdited.disconnect(self.emitIsModified)
        self.ui_le_waterFlow.textEdited.disconnect(self.emitIsModified)
        self.ui_cb_oil_flow_unit.currentIndexChanged.disconnect(self.emitIsModified)
        self.ui_cb_water_flow_unit.currentIndexChanged.disconnect(self.emitIsModified)
        self.ui_le_bottomTR.textEdited.disconnect(self.emitIsModified)
        self.ui_le_ambientT.textEdited.disconnect(self.emitIsModified)
        self.ui_le_reference.textEdited.disconnect(self.emitIsModified)
        self.ui_cb_frequency.currentIndexChanged.disconnect(self.emitIsModified)
        self.ui_cb_nbrePhases.currentIndexChanged.disconnect(self.emitIsModified)
        self.ui_rbut_core.toggled.disconnect(self.emitIsModified)
        self.ui_cb_nbreLimbs.currentIndexChanged.disconnect(self.emitIsModified)
        self.ui_cb_cool_refInt.currentIndexChanged.disconnect(self.emitIsModified)
        self.ui_cb_cool_refIntMode.currentIndexChanged.disconnect(self.emitIsModified)
        self.ui_cb_cool_refExt.currentIndexChanged.disconnect(self.emitIsModified)
        self.ui_cb_cool_refExtMode.currentIndexChanged.disconnect(self.emitIsModified)
        self.ui_btn_add.clicked.disconnect(self.emitIsModified)
        self.ui_btn_delete.clicked.disconnect(self.emitIsModified)
        self.ui_rbut_fans.toggled.disconnect(self.emitIsModified)
        self.ui_rbut_subExchangers.toggled.disconnect(self.emitIsModified)
        self.ui_le_powerPump.textEdited.disconnect(self.emitIsModified)
        self.ui_le_powerFan.textEdited.disconnect(self.emitIsModified)
        self.model_tab_FM.itemChanged.disconnect(self.emitIsModified)
        self.ui_spBox_nbrePumps_FM.valueChanged.disconnect(self.emitIsModified)
        self.model_tab_EM.itemChanged.disconnect(self.emitIsModified)
        self.ui_spBox_nbreFans_EM.valueChanged.disconnect(self.emitIsModified)
        self.tolerance_topOilGTR.updated.disconnect(self.emitIsModified)
        self.tolerance_aveWindGTR.updated.disconnect(self.emitIsModified)
        self.tolerance_hsGTR.updated.disconnect(self.emitIsModified)

    def checkDesign(self):
        """
        Vérification du design
        """
        # Liste d'erreurs à corriger
        lst_error = []

        # Vérification du respect des valideurs de champs
        if not self.ui_le_reference.hasAcceptableInput():
            self.ui_le_reference.setStyleSheet("background-color: red;")
            lst_error.append("Transformer reference must only have A-Z or a-z or 0-9 or - or _ characters")
        else:
            self.ui_le_reference.setStyleSheet("")

        # Vérification que les seuils de changements de stades de réfrigération sont cohérents
        dict_coolData = self.getCoolingStageData()
        if "T_on" and "T_off" in dict_coolData.keys():
            for k in range(len(dict_coolData["T_on"])):
                if dict_coolData["T_on"][k] is None or dict_coolData["T_off"][k] is None:
                    continue

                if dict_coolData["T_on"][k] < dict_coolData["T_off"][k]:
                    lst_error.append("Temperatures for cooling stage %i are incoherents"%(k+1))

        for w in self.lst_UI_WindingArrangement:
            lst_error = lst_error + w.checkDesign()

        return lst_error

    def freezeDesign(self, isFrozen):
        """
        Action lors du (dé)gelage du design
        """
        self.ui_spBox_nbOilPumps.setEnabled(not isFrozen)
        self.ui_spBox_nbWaterPumps.setEnabled(not isFrozen)
        self.ui_le_oilFlow.setEnabled(not isFrozen)
        self.ui_le_waterFlow.setEnabled(not isFrozen)
        self.ui_cb_oil_flow_unit.setEnabled(not isFrozen)
        self.ui_cb_water_flow_unit.setEnabled(not isFrozen)
        self.ui_le_bottomTR.setEnabled(not isFrozen)
        self.ui_le_ambientT.setEnabled(not isFrozen)
        self.ui_le_reference.setEnabled(not isFrozen)
        self.ui_cb_nbrePhases.setEnabled(not isFrozen)
        self.ui_cb_frequency.setEnabled(not isFrozen)
        self.ui_rbut_core.setEnabled(not isFrozen)
        self.ui_rbut_shell.setEnabled(not isFrozen)
        self.ui_cb_nbreLimbs.setEnabled(not isFrozen)
        self.ui_cb_cool_refInt.setEnabled(not isFrozen)
        self.ui_cb_cool_refIntMode.setEnabled(not isFrozen)
        self.ui_cb_cool_refExt.setEnabled(not isFrozen)
        self.ui_cb_cool_refExtMode.setEnabled(not isFrozen)
        self.ui_btn_add.setEnabled(not isFrozen)
        self.ui_btn_delete.setEnabled(not isFrozen)
        self.ui_grpBox_method.setEnabled(not isFrozen)
        self.ui_grpBox_power.setEnabled(not isFrozen)
        self.ui_grpBox_fansModulation.setEnabled(not isFrozen)
        self.ui_grpBox_subExchangersModulation.setEnabled(not isFrozen)

        if not isFrozen and not self.ui_main.action_Expert.isChecked():
            # Suppression de tous les résultats chargés
            lst_coilThermalData = self.getLstCoilThermalData()
            for c in lst_coilThermalData:
                for c_ui in c["lst_UI_CoilDefinition"]:
                    c_ui.coil.removeLoadedCalcul()
                    c_ui.removeLoadedCalcul()

        for w in self.lst_UI_WindingArrangement:
            w.freezeDesign(isFrozen)

    def changeMode(self, bool_DR, bool_FAT, bool_ope):
        """
        Actions lors du changement de mode TransfoTron
        """
        if bool_FAT and not (bool_ope or bool_DR):
            # Mode FAT uniquement
            self.ui_grpBox_coolData.hide()
            self.updateCooling()

            self.ui_btn_freeze.show()
            self.ui_btn_fat_id.show()
            self.ui_btn_ope_id.hide()

        elif bool_ope and not (bool_FAT or bool_DR):
            # Mode Operations uniquement
            self.ui_grpBox_coolData.show()
            self.updateCooling()

            self.ui_btn_freeze.show()
            self.ui_btn_fat_id.hide()
            self.ui_btn_ope_id.show()

        else:
            self.ui_grpBox_coolData.show()
            self.updateCooling()

            self.ui_btn_freeze.hide()
            self.ui_btn_fat_id.hide()
            self.ui_btn_ope_id.hide()

    def updateNbPhases(self):
        """
        Mise à jour du nombre de phases et du nombre de jambes du CM
        """

        nb_phases = int(self.ui_cb_nbrePhases.currentText())
        nb_limbs_old = self.ui_cb_nbreLimbs.currentText()

        # Déconnection pendant la manoeuvre
        self.ui_cb_nbreLimbs.currentIndexChanged.disconnect(self.updateMagneticCircuit)

        # Number of limbs
        self.ui_cb_nbreLimbs.clear()
        if nb_phases == 1:
            if self.isCoreType():
                lst_val = ["Unknown (2)", "2", "3", "4"]
                self.ui_cb_nbreLimbs.addItems(lst_val)
                if nb_limbs_old in lst_val:
                    self.ui_cb_nbreLimbs.setCurrentText(nb_limbs_old)
            else:
                lst_val = ["Unknown (3)", "3"]
                self.ui_cb_nbreLimbs.addItems(lst_val)
                if nb_limbs_old in lst_val:
                    self.ui_cb_nbreLimbs.setCurrentText(nb_limbs_old)
        elif nb_phases == 3:
            if self.isCoreType():
                lst_val = ["Unknown (3)", "3", "5"]
                self.ui_cb_nbreLimbs.addItems(lst_val)
                if nb_limbs_old in lst_val:
                    self.ui_cb_nbreLimbs.setCurrentText(nb_limbs_old)
            else:
                lst_val = ["Unknown (9)", "7", "9"]
                self.ui_cb_nbreLimbs.addItems(lst_val)
                if nb_limbs_old in lst_val:
                    self.ui_cb_nbreLimbs.setCurrentText(nb_limbs_old)
        else:
            raise Exception("Nombre de phases impossible")

        # Reconnection
        self.ui_cb_nbreLimbs.currentIndexChanged.connect(self.updateMagneticCircuit)

        # MAJ
        self.updateMagneticCircuit()

    def updateDesign(self):
        """
        MAJ affichage suite à changement de design
        """
        # MAJ du CM par la MAJ du nombre de phases
        self.updateNbPhases()

        # Si cuirassé
        if not self.isCoreType():
            # On ne garde qu'un seul arrangement
            if len(self.lst_UI_WindingArrangement) > 0:
                for warr in self.lst_UI_WindingArrangement[1:]:
                    warr.setSelected(False)
                    warr.deleteArrangement()
                    self.layout_windArr.removeWidget(warr)
                    self.lst_UI_WindingArrangement.remove(warr)

                # Affichage du dernier enroulement
                self.lst_UI_WindingArrangement[-1].setSelected(True)

            # Et on ne permet pas d'en rajouter
            self.ui_btn_add.hide()

        else:
            # On permet de rajouter des arrangements
            self.ui_btn_add.show()

        for warr in self.lst_UI_WindingArrangement:
            warr.updateDesign()

    def addArrangement(self):
        """
        Ajout d'une disposition d'enroulements
        """
        # Création de la disposition
        warr = UI_WindingArrangement(self.data_view["H_fen"] - 2*self.data_view["e_wind_vert"], self.data_view["L_coil"], self.scene_tfo, self.model_lst_wind, self.layout_wind, self)
        warr.isModified.connect(self.emitIsModified)
        warr.updateWindings()

        self.layout_windArr.addWidget(warr)
        self.lst_UI_WindingArrangement.append(warr)
        warr.setSelected(True)

        # MAJ
        self.updateWindingsData()
        self.updateMagneticCircuit()
        self.updateGraphicsSize()

        return warr

    def deleteArrangement(self):
        """
        Suppresion des dispositions d'enroulements sélectionnés
        """
        # A minima 1 enroulement
        if len(self.lst_UI_WindingArrangement) <= 1:
            return

        # Récupération de la liste des dispositions à supprimer
        lst_to_delete = [warr for warr in self.lst_UI_WindingArrangement if warr.isSelected()]
        if len(lst_to_delete) == 0:
            return

        # Et suppression
        for warr in lst_to_delete:
            warr.setSelected(False)
            warr.deleteArrangement()
            self.layout_windArr.removeWidget(warr)
            self.lst_UI_WindingArrangement.remove(warr)

        # Affichage du dernier enroulement
        if len(self.lst_UI_WindingArrangement) > 0:
            self.lst_UI_WindingArrangement[-1].setSelected(True)

        # MAJ
        self.deleteArrBtn()
        self.updateMagneticCircuit()
        self.updateGraphicsSize()

    def deleteArrBtn(self):
        """
        Gestion de l'affichage du bouton de suppression d'une disposition
        """
        lst_selected = [warr for warr in self.lst_UI_WindingArrangement if warr.isSelected()]
        if len(self.lst_UI_WindingArrangement) <= 1 or len(lst_selected) < 1:
            self.ui_btn_delete.hide()
        else:
            self.ui_btn_delete.show()

    def changeWinding(self, index):
        """
        Changement du winding sélectionné dans la liste
        """

        if self.ui_list_wind.currentIndex().row() < 0:
            # Aucun enroulement sélectionné
            return

        if isinstance(index, QItemSelection):
            if len(index.indexes()) > 0:
                index = index.indexes()[0]
            else:
                return

        # Affichage du widget
        wind_selected = self.model_lst_wind.itemFromIndex(index)
        wind_selected.showWidget()
        # Et du winding dans la vue
        for warr in self.lst_UI_WindingArrangement:
            warr.setSelected(False)
        wind_selected.widget.setSelected(True)

    def changeTab(self):
        """
        Action lors du changement de tab
        """
        ### Vue du transfo
        if self.ui_tabWidget.currentWidget() == self.ui_wdg_main:
            # La vue du transfo est cliquable
            self.view_tfo_nonClickable.hide()
            self.view_tfo_clickable.show()
            # On met à jour la sélection
            for warr in self.lst_UI_WindingArrangement:
                warr.setSelected(warr.isSelected(), False)
        else:
            # La vue du transfo est non cliquable
            self.view_tfo_nonClickable.show()
            self.view_tfo_clickable.hide()
            # On déselectionne tout
            for warr in self.lst_UI_WindingArrangement:
                warr.setSelected(False)
        if self.ui_tabWidget.currentWidget() == self.ui_wdg_windings:
            self.ui_list_wind.setCurrentIndex(self.ui_list_wind.currentIndex())
            self.changeWinding(self.ui_list_wind.currentIndex())

    def updateMagneticCircuit(self):
        """
        MAJ du circuit magnétique
        """
        lst_windings_new = []
        for warr in self.lst_UI_WindingArrangement:
            for wdata in warr.lst_UI_WindingData:
                lst_windings_new.append(wdata.winding)
        self.CM_graphic.set_lst_windings(lst_windings_new)
        self.CM_graphic.set_nb_phases(int(self.ui_cb_nbrePhases.currentText()))
        tmp = self.ui_cb_nbreLimbs.currentText()
        if "Unknown" in tmp:
            tmp = tmp[tmp.index("(")+1:tmp.index(")")]
        self.CM_graphic.set_nb_limbs(int(tmp))
        self.CM_graphic.set_core_type(self.isCoreType())

        # MAJ de la représentation
        self.updateGraphicsSize()

    def updateCooling(self):
        """
        Mise à jour du mode de refroidissement
        """
        # Symbole de réfrigération
        self.cooling_mode = "%s%s%s%s"%(self.ui_cb_cool_refInt.currentText(), self.ui_cb_cool_refIntMode.currentText(), self.ui_cb_cool_refExt.currentText(), self.ui_cb_cool_refExtMode.currentText())

        # Infos pompes huile en D ou en F
        if self.ui_cb_cool_refIntMode.currentText() in ["F", "D"] and self.cooling_mode != "ODAF":
            self.ui_lbl_nbOilPumps.show()
            self.ui_spBox_nbOilPumps.show()
            self.ui_lbl_oilFlow.show()
            self.ui_cb_oil_flow_unit.show()
            self.ui_le_oilFlow.show()
        elif self.cooling_mode == "ODAF":
            # Les infos détaillées en D sont dans les panneaux de définition des stades
            self.ui_lbl_nbOilPumps.hide()
            self.ui_spBox_nbOilPumps.hide()
            self.ui_lbl_oilFlow.show()
            self.ui_cb_oil_flow_unit.show()
            self.ui_le_oilFlow.show()
        else:
            self.ui_lbl_nbOilPumps.hide()
            self.ui_spBox_nbOilPumps.hide()
            self.ui_lbl_oilFlow.hide()
            self.ui_cb_oil_flow_unit.hide()
            self.ui_le_oilFlow.hide()

        # Infos pompes eau que en W
        if self.ui_cb_cool_refExt.currentText() == "W":
            self.ui_lbl_nbWaterPumps.show()
            self.ui_spBox_nbWaterPumps.show()
            self.ui_lbl_waterFlow.show()
            self.ui_cb_water_flow_unit.show()
            self.ui_le_waterFlow.show()
        else:
            self.ui_lbl_nbWaterPumps.hide()
            self.ui_spBox_nbWaterPumps.hide()
            self.ui_lbl_waterFlow.hide()
            self.ui_cb_water_flow_unit.hide()
            self.ui_le_waterFlow.hide()

        # Label température ambiante
        if self.ui_cb_cool_refExt.currentText() == "W":
            self.ui_lbl_ambientT.setText("Water temperature")
        else:
            self.ui_lbl_ambientT.setText("Ambient temperature")

        # Infos sur les stades de réfrigération en ODAF uniquement
        if self.cooling_mode != "ODAF" \
            or self.ui_main.action_FAT.isChecked() and not (self.ui_main.action_Operations.isChecked() or self.ui_main.action_DesignReview.isChecked()):
            self.ui_grpBox_method.hide()
            self.ui_grpBox_power.hide()
        else:
            self.ui_grpBox_method.show()
            self.ui_grpBox_power.show()
        self.changeCoolersMethod()

        self.updateStudyName()

    def changeCoolersMethod(self):
        """
        Actions lors du changement de mode de refroidissement
        """
        if self.cooling_mode != "ODAF" \
            or self.ui_main.action_FAT.isChecked() and not (self.ui_main.action_Operations.isChecked() or self.ui_main.action_DesignReview.isChecked()):
            self.ui_grpBox_fansModulation.hide()
            self.ui_grpBox_subExchangersModulation.hide()
            return

        if self.ui_rbut_subExchangers.isChecked():
            self.ui_grpBox_subExchangersModulation.show()
            self.ui_grpBox_fansModulation.hide()
        else:
            self.ui_grpBox_subExchangersModulation.hide()
            self.ui_grpBox_fansModulation.show()

    def newCoolingStageFM(self):
        """
        Ajout d'un stade de réfrigération en modulation du nombre de ventilateurs
        """
        # Dernier stade de réfrigération
        try:
            numStade = int(self.model_tab_FM.item(self.model_tab_FM.rowCount()-1, 0).text())
        except:
            numStade = 0

        row = []
        # Stade
        tmp = QStandardItem("%i"%(numStade+1))
        tmp.setData(Qt.AlignCenter, Qt.TextAlignmentRole)
        tmp.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        row.append(tmp)
        # Nbre fans
        tmp = QStandardItem("1")
        tmp.setData(Qt.AlignCenter, Qt.TextAlignmentRole)
        tmp.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable)
        tmp.setData(QBrush(Qt.yellow), Qt.BackgroundRole)
        row.append(tmp)
        # T on
        tmp = QStandardItem("")
        tmp.setData(Qt.AlignCenter, Qt.TextAlignmentRole)
        tmp.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable)
        tmp.setData(QBrush(Qt.yellow), Qt.BackgroundRole)
        row.append(tmp)
        # T off
        tmp = QStandardItem("")
        tmp.setData(Qt.AlignCenter, Qt.TextAlignmentRole)
        tmp.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable)
        tmp.setData(QBrush(Qt.yellow), Qt.BackgroundRole)
        row.append(tmp)
        rootItem = self.model_tab_FM.invisibleRootItem()
        rootItem.appendRow(row)

        self.updateNbreFans()

    def deleteCoolingStageFM(self):
        """
        Suppression du dernier stade de réfrigération en modulation du nombre de ventilateurs
        """
        if self.model_tab_FM.rowCount() <= 1:
            return

        rootItem = self.model_tab_FM.invisibleRootItem()
        self.model_tab_FM.removeRow(self.model_tab_FM.rowCount()-1, rootItem.index())

        self.updateNbreFans()

    def updateNbreFans(self):
        """
        Mise à jour du nombre total de ventilateurs
        """
        nb_fans = 0
        for k in range(self.model_tab_FM.rowCount()):
            item = self.model_tab_FM.item(k, 1)
            try:
                nb_fans = max(nb_fans, int(item.text()))
            except:
                pass
        self.ui_le_nbreFans_FM.setText(nb_fans)

    def newCoolingStageEM(self):
        """
        Ajout d'un stade de réfrigération en modulation du nombre de sous-échangeurs
        """
        # Dernier stade de réfrigération
        try:
            numStade = int(self.model_tab_EM.item(self.model_tab_EM.rowCount()-1, 0).text())
        except:
            numStade = 0

        row = []
        # Stade
        tmp = QStandardItem("%i"%(numStade+1))
        tmp.setData(Qt.AlignCenter, Qt.TextAlignmentRole)
        tmp.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        row.append(tmp)
        # Nbre sous-échangeurs
        tmp = QStandardItem("1")
        tmp.setData(Qt.AlignCenter, Qt.TextAlignmentRole)
        tmp.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable)
        tmp.setData(QBrush(Qt.yellow), Qt.BackgroundRole)
        row.append(tmp)
        # T on
        tmp = QStandardItem("")
        tmp.setData(Qt.AlignCenter, Qt.TextAlignmentRole)
        tmp.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable)
        tmp.setData(QBrush(Qt.yellow), Qt.BackgroundRole)
        row.append(tmp)
        # T off
        tmp = QStandardItem("")
        tmp.setData(Qt.AlignCenter, Qt.TextAlignmentRole)
        tmp.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable)
        tmp.setData(QBrush(Qt.yellow), Qt.BackgroundRole)
        row.append(tmp)
        rootItem = self.model_tab_EM.invisibleRootItem()
        rootItem.appendRow(row)

        self.updateNbreSubExchangers()

    def deleteCoolingStageEM(self):
        """
        Suppression du dernier stade de réfrigération en modulation du nombre de sous-échangeurs
        """
        if self.model_tab_EM.rowCount() <= 1:
            return

        rootItem = self.model_tab_EM.invisibleRootItem()
        self.model_tab_EM.removeRow(self.model_tab_EM.rowCount()-1, rootItem.index())

        self.updateNbreSubExchangers()

    def updateNbreSubExchangers(self):
        """
        Mise à jour du nombre total de sous-échangeurs
        """
        nb_ssExchangers = 0
        for k in range(self.model_tab_EM.rowCount()):
            item = self.model_tab_EM.item(k, 1)
            try:
                nb_ssExchangers = max(nb_ssExchangers, int(item.text()))
            except:
                pass
        self.ui_le_nbreSubExchangers_EM.setText(nb_ssExchangers)

    def updateWindingsData(self):
        """
        MAJ des enroulements
        """
        # Mise à jour du couplage
        for warr in self.lst_UI_WindingArrangement:
            for wdata in warr.lst_UI_WindingData:
                wdata.updateVectorGroupYDI()

        # Mise à jour du nom de la study
        self.updateStudyName()

    def isMonophase(self):
        """
        Renvoi True si c'est un appareil monophasé
        """
        return int(self.ui_cb_nbrePhases.currentText()) == 1

    def isTriphase(self):
        """
        Renvoi True si c'est un appareil triphasé
        """
        return int(self.ui_cb_nbrePhases.currentText()) == 3

    def isCoreType(self):
        """
        Renvoi True si c'est un appareil colonne
        """
        return self.ui_rbut_core.isChecked()

    def getNumberOilPumps(self):
        """
        Renvoi le nombre de pompes à huile (dépend du mode d'entrée)
        """
        if self.cooling_mode == "ODAF":
            if self.ui_rbut_subExchangers.isChecked():
                try:
                    return int(self.ui_le_nbreSubExchangers_EM.text())
                except:
                    return 0
            else:
                return self.ui_spBox_nbrePumps_FM.value()
        else:
            return self.ui_spBox_nbOilPumps.value()

    def getCoolersAdjustmentMethod(self):
        """
        Renvoi le mode de pilotage de la réfrigération si ODAF
        """
        if self.cooling_mode == "ODAF":
            if self.ui_rbut_subExchangers.isChecked():
                return "exchangers"
            else:
                return "fans"
        else:
            return None

    def getCoolingStageData(self):
        """
        Renvoi les informations de fonctionnement de la réfrigération
        """
        cooling_mode = self.getCoolersAdjustmentMethod()
        if cooling_mode is None:
            return {}

        dict_coolData = {}
        dict_coolData["cooler_mode"] = cooling_mode

        # Débit d'huile en m3/h
        oil_pump_unit = self.ui_cb_oil_flow_unit.currentText()
        if oil_pump_unit == 'm3/h':
            try:
                dict_coolData["oil_flow_pump_m3h"] = float(self.ui_le_oilFlow.text())
            except:
                dict_coolData["oil_flow_pump_m3h"] = 0.0
        elif oil_pump_unit == 'l/s':
            try:
                dict_coolData["oil_flow_pump_m3h"] = 3.6*float(self.ui_le_oilFlow.text())
            except:
                dict_coolData["oil_flow_pump_m3h"] = 0.0
        else:
            raise Exception("Argument '" + str(oil_pump_unit) + "' inconnu (valeur attendue : m3/h ou l/s)")

        # Consommation
        try:
            val = float(self.ui_le_powerPump.text())
        except:
            val = 0
        dict_coolData["power_pump_W"] = val
        try:
            val = float(self.ui_le_powerFan.text())
        except:
            val = 0
        dict_coolData["power_fan_W"] = val

        # Modulation de la réfrigération
        dict_coolData["nb_in_operation"] = []
        dict_coolData["T_on"] = []
        dict_coolData["T_off"] = []
        if cooling_mode == "fans":
            for k in range(self.model_tab_FM.rowCount()):
                try:
                    val = int(self.model_tab_FM.item(k, 1).text())
                except:
                    continue
                dict_coolData["nb_in_operation"].append(val)
                try:
                    val = float(self.model_tab_FM.item(k, 2).text())
                except:
                    val = None
                dict_coolData["T_on"].append(val)
                try:
                    val = float(self.model_tab_FM.item(k, 3).text())
                except:
                    val = None
                dict_coolData["T_off"].append(val)
            dict_coolData["nb_oil_pump"] = self.ui_spBox_nbrePumps_FM.value()
            try:
                val = int(self.ui_le_nbreFans_FM.text())
            except:
                val = 0
            dict_coolData["nb_air_fan"] = val

        elif cooling_mode == "exchangers":
            for k in range(self.model_tab_EM.rowCount()):
                try:
                    val = int(self.model_tab_EM.item(k, 1).text())
                except:
                    continue
                dict_coolData["nb_in_operation"].append(val)
                try:
                    val = float(self.model_tab_EM.item(k, 2).text())
                except:
                    val = None
                dict_coolData["T_on"].append(val)
                try:
                    val = float(self.model_tab_EM.item(k, 3).text())
                except:
                    val = None
                dict_coolData["T_off"].append(val)
            dict_coolData["nb_air_fan"] = self.ui_spBox_nbreFans_EM.value()
            try:
                val = int(self.ui_le_nbreSubExchangers_EM.text())
            except:
                val = 0
            dict_coolData["nb_oil_pump"] = val

        return dict_coolData

    def getLstWinding(self):
        """
        Liste des enroulements
        """
        lst_ui_windData = []
        for warr in self.lst_UI_WindingArrangement:
            for wdata in warr.lst_UI_WindingData:
                lst_ui_windData.append(wdata)
        return lst_ui_windData

    def getLstWindingVoltageDescending(self):
        """
        Liste des enroulements par ordre de tension décroissante et enroulement le + extérieur en 1er
        """
        def tmpFct(w):
            u = w.getTapVoltage()
            if u is None:
                return 0.0
            else:
                return u
        out = list(reversed(sorted(self.getLstWinding(), key=lambda w:tmpFct(w))))
        return out

    def getLstWindingVoltageDescendingNameAlphabetical(self):
        """
        Liste des enroulements par ordre de tension décroissante et par ordre alphabétique
        """
        def tmpFct(w):
            u = w.getTapVoltage()
            if u is None:
                return 0.0
            else:
                return u
        out = list(sorted(self.getLstWinding(), key=lambda w:(-tmpFct(w), w.getName())))
        return out

    def getLstWindingPowerDescending(self):
        """
        Liste des enroulements par ordre de puissance décroissante et enroulement le + extérieur en 1er
        """
        def tmpFct(w):
            p = w.getTapPower()
            if p is None:
                return 0.0
            else:
                return p
        out = list(reversed(sorted(self.getLstWinding(), key=lambda w:tmpFct(w))))
        return out

    def getLstCoilThermalData(self):
        """
        Renvoi la liste des données des bobines thermiques de tous les enroulements
        """

        lst_coilThermalData = []

        for w in self.lst_UI_WindingArrangement:
            lst_coilThermalData = lst_coilThermalData + w.getLstCoilThermalData()

        return lst_coilThermalData

    def getLstCoilElectricalData(self):
        """
        Renvoi la liste des données des bobines électriques de tous les enroulements
        """

        lst_coilElectricalData = []

        for w in self.lst_UI_WindingArrangement:
            lst_coilElectricalData = lst_coilElectricalData + w.getLstCoilElectricalData()

        return lst_coilElectricalData

    def getVectorGroup(self):
        """
        String de représentation du couplage
        """
        # Liste des enroulements rangés
        lst_ui_windDesc = self.getLstWindingVoltageDescendingNameAlphabetical()

        lst_tmp = []
        for w in lst_ui_windDesc:
            lst_tmp.append(w.getVectorGroup())
        return ''.join(lst_tmp)

    def getRatedFrequency(self):
        """
        Renvoi la fréquence assignée
        """
        return self.ui_cb_frequency.currentData()

    def updateStudyName(self):
        """
        Fourniture et MAJ de la study name
        """
        lst_infos = []

        # Nom
        lst_infos.append(self.ui_le_reference.text())

        # Liste des enroulements rangés
        lst_ui_windDesc = self.getLstWindingVoltageDescendingNameAlphabetical()

        # Puissances
        lst_tmp = []
        for w in lst_ui_windDesc:
            tmp = w.getTapPower()
            if tmp is None:
                tmp = 0.0
            if tmp.is_integer():
                lst_tmp.append("%i"%tmp)
            else:
                lst_tmp.append("%.3f"%tmp)
        lst_infos.append('/'.join(lst_tmp) + " MVA")

        # Tensions
        lst_tmp = []
        for w in lst_ui_windDesc:
            tmp = w.getTapVoltage()
            if tmp is None:
                tmp = 0.0
            if tmp.is_integer():
                tmp = "%i"%tmp
            else:
                tmp = "%.3f"%tmp
            tmp = tmp + w.getStrRegulation()
            lst_tmp.append(tmp)
        lst_infos.append('/'.join(lst_tmp) + " kV")

        # Couplages
        lst_infos.append(self.getVectorGroup())

        # Fréquence
        lst_infos.append(self.ui_cb_frequency.currentText() + " Hz")

        # Mode de refroidissement
        lst_infos.append(self.cooling_mode)

        # Mise en forme des infos
        lst_infos = [s for s in lst_infos if s != ""]
        study = ' - '.join(lst_infos)

        self.studyNameUpdated.emit(study)

        return study

    def updateGraphicsSize(self):
        """
        Met à jour les graphiques (reconstruit également)
        """
        # Mise à jour des centres des enroulements
        lst_x_center_col, lst_y_center_col = self.CM_graphic.get_center_col()
        # Et du rayon des enroulements
        if self.isCoreType():
            R_wind = self.data_view["L_CM"]/2
        else:
            R_wind = self.data_view["L_CM"]

        for warr in self.lst_UI_WindingArrangement:
            R_wind = warr.updateWindingsDisplay(lst_x_center_col, R_wind, lst_y_center_col, self.data_view["e_wind_hori"], self.z_value_wind)

        self.scene_tfo.setSceneRect(self.scene_tfo.itemsBoundingRect())

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
        self.updateGraphicsSize()
        super().showEvent(event)

    def generateXML(self, tmpSaveDirPath):
        """
        Génération du fichier XML dans le dossier temporaire
        """
        path_design = join(tmpSaveDirPath, "design")
        if not exists(path_design):
            makedirs(path_design)

        docDom = QDomDocument()
        root = docDom.appendChild(docDom.createElement("root"))

        tag_tmp = docDom.createElement('reference')
        tag_tmp.appendChild(docDom.createTextNode(self.ui_le_reference.text()))
        root.appendChild(tag_tmp)
        tag_tmp = docDom.createElement('phase_nb')
        tag_tmp.appendChild(docDom.createTextNode(self.ui_cb_nbrePhases.currentText()))
        root.appendChild(tag_tmp)
        tag_tmp = docDom.createElement('limbs_nb')
        tag_tmp.appendChild(docDom.createTextNode(self.ui_cb_nbreLimbs.currentText()))
        root.appendChild(tag_tmp)
        tag_tmp = docDom.createElement('rated_freq_Hz')
        tag_tmp.appendChild(docDom.createTextNode(self.ui_cb_frequency.currentText()))
        root.appendChild(tag_tmp)
        tag_tmp = docDom.createElement('design')
        if self.isCoreType():
            tag_tmp.appendChild(docDom.createTextNode("core"))
        else:
            tag_tmp.appendChild(docDom.createTextNode("shell"))
        root.appendChild(tag_tmp)

        tag_cool_type = docDom.createElement('cooling_type')
        tag_tmp = docDom.createElement('internal_medium')
        tag_tmp.appendChild(docDom.createTextNode(self.ui_cb_cool_refInt.currentText()))
        tag_cool_type.appendChild(tag_tmp)
        tag_tmp = docDom.createElement('internal_mode')
        tag_tmp.appendChild(docDom.createTextNode(self.ui_cb_cool_refIntMode.currentText()))
        tag_cool_type.appendChild(tag_tmp)
        tag_tmp = docDom.createElement('external_medium')
        tag_tmp.appendChild(docDom.createTextNode(self.ui_cb_cool_refExt.currentText()))
        tag_cool_type.appendChild(tag_tmp)
        tag_tmp = docDom.createElement('external_mode')
        tag_tmp.appendChild(docDom.createTextNode(self.ui_cb_cool_refExtMode.currentText()))
        tag_cool_type.appendChild(tag_tmp)
        root.appendChild(tag_cool_type)

        tag_cool = docDom.createElement("cooling")
        root.appendChild(tag_cool)

        # Huile
        tag_tmp = docDom.createElement('N_pumps')
        tag_tmp.appendChild(docDom.createTextNode("%i"%(self.getNumberOilPumps())))
        tag_cool.appendChild(tag_tmp)

        oil_pump_unit = self.ui_cb_oil_flow_unit.currentText()
        tag_tmp = docDom.createElement('oil_pump_unit')
        tag_tmp.appendChild(docDom.createTextNode(oil_pump_unit))
        tag_cool.appendChild(tag_tmp)

        ## on enregistre dans les deux unités
            # le serveur n'utilise que les m3/h
            # la valeur en l/s ne sert qu'au client
        # cas où l'utilisateur a sélectionné m3/h
        if oil_pump_unit == 'm3/h':
            oil_pump_m3_hmoins1 = self.ui_le_oilFlow.text()
            try:
                oil_pump_l_smoins1 = str(float(self.ui_le_oilFlow.text())/3.6)
            except:
                oil_pump_l_smoins1 = "0.0"
        # cas où l'utilisateur a sélectionné l/s
        elif oil_pump_unit == 'l/s':
            try:
                oil_pump_m3_hmoins1 = str(3.6*float(self.ui_le_oilFlow.text()))
            except:
                oil_pump_m3_hmoins1 = "0.0"
            oil_pump_l_smoins1 = self.ui_le_oilFlow.text()
        else:
            raise Exception("Argument '" + str(oil_pump_unit) + "' inconnu (valeur attendue : m3/h ou l/s)")

        tag_tmp = docDom.createElement('oil_pump_m3.h-1')
        tag_tmp.appendChild(docDom.createTextNode(oil_pump_m3_hmoins1))
        tag_cool.appendChild(tag_tmp)

        tag_tmp = docDom.createElement('oil_pump_l.s-1')
        tag_tmp.appendChild(docDom.createTextNode(oil_pump_l_smoins1))
        tag_cool.appendChild(tag_tmp)

        # Eau
        tag_tmp = docDom.createElement('N_water_pumps')
        tag_tmp.appendChild(docDom.createTextNode("%i"%(self.ui_spBox_nbWaterPumps.value())))
        tag_cool.appendChild(tag_tmp)

        water_pump_unit = self.ui_cb_water_flow_unit.currentText()
        tag_tmp = docDom.createElement('water_pump_unit')
        tag_tmp.appendChild(docDom.createTextNode(water_pump_unit))
        tag_cool.appendChild(tag_tmp)

        ## on enregistre dans les deux unités
            # le serveur n'utilise que les m3/h
            # la valeur en l/s ne sert qu'au client
        # cas où l'utilisateur a sélectionné m3/h
        if water_pump_unit == 'm3/h':
            water_pump_m3_hmoins1 = self.ui_le_waterFlow.text()
            try:
                water_pump_l_smoins1 = str(float(self.ui_le_waterFlow.text())/3.6)
            except:
                water_pump_l_smoins1 = "0.0"
        # cas où l'utilisateur a sélectionné l/s
        elif water_pump_unit == 'l/s':
            try:
                water_pump_m3_hmoins1 = str(3.6*float(self.ui_le_waterFlow.text()))
            except:
                water_pump_m3_hmoins1 = "0.0"
            water_pump_l_smoins1 = self.ui_le_waterFlow.text()
        else:
            raise Exception("Argument '" + str(water_pump_unit) + "' inconnu (valeur attendue : m3/h ou l/s)")

        tag_tmp = docDom.createElement('water_pump_m3.h-1')
        tag_tmp.appendChild(docDom.createTextNode(water_pump_m3_hmoins1))
        tag_cool.appendChild(tag_tmp)

        tag_tmp = docDom.createElement('water_pump_l.s-1')
        tag_tmp.appendChild(docDom.createTextNode(water_pump_l_smoins1))
        tag_cool.appendChild(tag_tmp)

        tag_tmp = docDom.createElement('oil_bottom_TR_K')
        tag_tmp.appendChild(docDom.createTextNode(self.ui_le_bottomTR.text()))
        tag_cool.appendChild(tag_tmp)
        tag_tmp = docDom.createElement('ambient_T_C')
        tag_tmp.appendChild(docDom.createTextNode(self.ui_le_ambientT.text()))
        tag_cool.appendChild(tag_tmp)

        # Stades de réfrigération & co
        tag_tmp = docDom.createElement('coolers_adjustment_method')
        if self.ui_rbut_fans.isChecked():
            tag_tmp.appendChild(docDom.createTextNode("fans"))
        else:
            tag_tmp.appendChild(docDom.createTextNode("sub-exchangers"))
        tag_cool.appendChild(tag_tmp)
        tag_tmp = docDom.createElement('pump_power_W')
        tag_tmp.appendChild(docDom.createTextNode(self.ui_le_powerPump.text()))
        tag_cool.appendChild(tag_tmp)
        tag_tmp = docDom.createElement('fan_power_W')
        tag_tmp.appendChild(docDom.createTextNode(self.ui_le_powerFan.text()))
        tag_cool.appendChild(tag_tmp)
        # Fans modulation
        tag_FM = docDom.createElement('cooling_stage_FM')
        for row in range(self.model_tab_FM.rowCount()):
            tag_std = docDom.createElement("std_%s"%self.model_tab_FM.item(row,0).text())
            tag_tmp = docDom.createElement('val')
            tag_tmp.appendChild(docDom.createTextNode(self.model_tab_FM.item(row,1).text()))
            tag_std.appendChild(tag_tmp)
            tag_tmp = docDom.createElement('val')
            tag_tmp.appendChild(docDom.createTextNode(self.model_tab_FM.item(row,2).text()))
            tag_std.appendChild(tag_tmp)
            tag_tmp = docDom.createElement('val')
            tag_tmp.appendChild(docDom.createTextNode(self.model_tab_FM.item(row,3).text()))
            tag_std.appendChild(tag_tmp)
            tag_FM.appendChild(tag_std)
        tag_cool.appendChild(tag_FM)
        tag_tmp = docDom.createElement('N_pumps_FM')
        tag_tmp.appendChild(docDom.createTextNode("%i"%(self.ui_spBox_nbrePumps_FM.value())))
        tag_cool.appendChild(tag_tmp)
        # Sub-exchangers modulation
        tag_EM = docDom.createElement('cooling_stage_EM')
        for row in range(self.model_tab_EM.rowCount()):
            tag_std = docDom.createElement("std_%s"%self.model_tab_EM.item(row,0).text())
            tag_tmp = docDom.createElement('val')
            tag_tmp.appendChild(docDom.createTextNode(self.model_tab_EM.item(row,1).text()))
            tag_std.appendChild(tag_tmp)
            tag_tmp = docDom.createElement('val')
            tag_tmp.appendChild(docDom.createTextNode(self.model_tab_EM.item(row,2).text()))
            tag_std.appendChild(tag_tmp)
            tag_tmp = docDom.createElement('val')
            tag_tmp.appendChild(docDom.createTextNode(self.model_tab_EM.item(row,3).text()))
            tag_std.appendChild(tag_tmp)
            tag_EM.appendChild(tag_std)
        tag_cool.appendChild(tag_EM)
        tag_tmp = docDom.createElement('N_fans_EM')
        tag_tmp.appendChild(docDom.createTextNode("%i"%(self.ui_spBox_nbreFans_EM.value())))
        tag_cool.appendChild(tag_tmp)

        root.appendChild(self.tolerance_topOilGTR.generateXMLElement())
        root.appendChild(self.tolerance_aveWindGTR.generateXMLElement())
        root.appendChild(self.tolerance_hsGTR.generateXMLElement())

        for w in self.lst_UI_WindingArrangement:
            w.addXMLTree(root, docDom)

        # Enregistrement
        header = docDom.createProcessingInstruction("xml", "version=\"1.0\" encoding=\"UTF-8\"")
        docDom.insertBefore(header, root)
        file = QFile(join(path_design, "ratingPlate.xml"))
        file.open(QIODevice.WriteOnly)
        out = QTextStream(file)
        docDom.save(out, 4, QDomDocument.EncodingFromDocument)
        file.close()

    def addPDF(self, pdf, part, lst_id_calcul=[]):
        """
        Remplissage du fichier PDF
        """
        pdf.set_font()

        if "data_general" in part:
            pdf.multi_cell(txt="Reference: %s"%self.ui_le_reference.text())
            if self.isCoreType():
                pdf.multi_cell(txt="Design: core-type")
            else:
                pdf.multi_cell(txt="Design: shell-type")
            pdf.multi_cell(txt="Number of phases: %s"%self.ui_cb_nbrePhases.currentText())
            pdf.multi_cell(txt="Number of magnetic circuit limbs: %s"%self.ui_cb_nbreLimbs.currentText())
            pdf.multi_cell(txt="Number of windings: %s"%len(self.getLstWinding()))
            pdf.multi_cell(txt="Rated frequency: %s Hz"%self.ui_cb_frequency.currentText())

            pdf.ln()
            pdf.set_font(style="IU")
            pdf.multi_cell(txt="> Cooling:")
            pdf.set_font()
            pdf.multi_cell(txt=" "*8 + "Type: %s"%self.cooling_mode)

            if (self.ui_main.action_Operations.isChecked() or self.ui_main.action_DesignReview.isChecked()):
                if self.ui_cb_cool_refIntMode.currentText() in ["F", "D"]:
                    pdf.multi_cell(txt=" "*8 + "Number of oil pumps: %i"%self.getNumberOilPumps())
                    try:
                        total = self.getNumberOilPumps()*float(self.ui_le_oilFlow.text())
                    except:
                        total = 0.0
                    if self.ui_cb_oil_flow_unit.currentText() == "m3/h":
                        pdf.multi_cell(txt=" "*8 + "Oil flow per pump: %s m3/h"%self.ui_le_oilFlow.text())
                        pdf.multi_cell(txt=" "*8 + "Total oil flow: %.1f m3/h"%total)
                    elif self.ui_cb_oil_flow_unit.currentText() == "l/s":
                        pdf.multi_cell(txt=" "*8 + "Oil flow per pump: %s l/s"%self.ui_le_oilFlow.text())
                        pdf.multi_cell(txt=" "*8 + "Total oil flow: %.1f l/s"%total)
                    else:
                        raise Exception("Argument '" + str(self.ui_cb_oil_flow_unit.currentText()) + "' inconnu (valeur attendue : m3/h ou l/s)")

                if self.ui_cb_cool_refExt.currentText() == "W":
                    pdf.multi_cell(txt=" "*8 + "Number of water pumps: %i"%self.ui_spBox_nbWaterPumps.value())
                    try:
                        total = self.ui_spBox_nbWaterPumps.value()*float(self.ui_le_waterFlow.text())
                    except:
                        total = 0.0
                    if self.ui_cb_water_flow_unit.currentText() == "m3/h":
                        pdf.multi_cell(txt=" "*8 + "Water flow per pump: %s m3/h"%self.ui_le_waterFlow.text())
                        pdf.multi_cell(txt=" "*8 + "Total water flow: %.1f m3/h"%total)
                    elif self.ui_cb_water_flow_unit.currentText() == "l/s":
                        pdf.multi_cell(txt=" "*8 + "Water flow per pump: %s l/s"%self.ui_le_waterFlow.text())
                        pdf.multi_cell(txt=" "*8 + "Total water flow: %.1f l/s"%total)
                    else:
                        raise Exception("Argument '" + str(self.ui_cb_water_flow_unit.currentText()) + "' inconnu (valeur attendue : m3/h ou l/s)")

                pdf.multi_cell(txt=" "*8 + "Bottom oil temperature rise: %s K"%self.ui_le_bottomTR.text())
                if self.ui_cb_cool_refExt.currentText() == "W":
                    pdf.multi_cell(txt=" "*8 + "Water temperature: %s °C"%self.ui_le_ambientT.text())
                else:
                    pdf.multi_cell(txt=" "*8 + "Ambient temperature: %s °C"%self.ui_le_ambientT.text())

                if self.cooling_mode == "ODAF":
                    # Détail des seuils des stades de réfrigération
                    pdf.ln()
                    pdf.set_font(style="IU")
                    pdf.multi_cell(txt="> Coolers modulation:")
                    pdf.set_font()
                    if self.ui_rbut_subExchangers.isChecked():
                        pdf.multi_cell(txt=" "*8 + "Sub-exchangers modulation")
                        row_title = ["Cooling stage", "No. of sub-exchangers in operation", "Temp. switch on\nToil > °C", "Temp. switch off\nToil < °C"]
                        tab_data = []
                        for row in range(self.model_tab_EM.rowCount()):
                            data = []
                            for col in range(self.model_tab_EM.columnCount()):
                                # Bidouilles pour avoir le même format d'affichage que dans le tableau
                                dlg = self.ui_tabV_EM.itemDelegate(self.model_tab_EM.item(row, col).index())
                                data.append(dlg.displayText(self.model_tab_EM.item(row, col).text(), self.locale))
                            tab_data.append(data)
                        if len(tab_data) > 0:
                            pdf.tableMultiCell(row_title, tab_data)
                        pdf.multi_cell(txt=" "*8 + "Total number of air fans: %i"%self.ui_spBox_nbreFans_EM.value())
                        pdf.multi_cell(txt=" "*8 + "Total number of sub-exchangers: %s"%self.ui_le_nbreSubExchangers_EM.text())
                    else:
                        pdf.multi_cell(txt=" "*8 + "Fans modulation")
                        row_title = ["Cooling stage", "No. of fans in operation", "Temp. switch on\nToil > °C", "Temp. switch off\nToil < °C"]
                        tab_data = []
                        for row in range(self.model_tab_FM.rowCount()):
                            data = []
                            for col in range(self.model_tab_FM.columnCount()):
                                # Bidouilles pour avoir le même format d'affichage que dans le tableau
                                dlg = self.ui_tabV_FM.itemDelegate(self.model_tab_FM.item(row, col).index())
                                data.append(dlg.displayText(self.model_tab_FM.item(row, col).text(), self.locale))
                            tab_data.append(data)
                        if len(tab_data) > 0:
                            pdf.tableMultiCell(row_title, tab_data)
                        pdf.multi_cell(txt=" "*8 + "Total number of oil pumps: %i"%self.ui_spBox_nbrePumps_FM.value())
                        pdf.multi_cell(txt=" "*8 + "Total number of air fans: %s"%self.ui_le_nbreFans_FM.text())

                    pdf.ln()
                    pdf.set_font(style="IU")
                    pdf.multi_cell(txt="> Coolers consumption:")
                    pdf.set_font()
                    pdf.multi_cell(txt=" "*8 + "Per pump: %s W"%self.ui_le_powerPump.text())
                    pdf.multi_cell(txt=" "*8 + "Per fan: %s W"%self.ui_le_powerFan.text())

            pdf.ln()
            pdf.set_font(style="IU")
            pdf.multi_cell(txt="> Tolerance temperature rises:")
            pdf.set_font()
            pdf.multi_cell(txt=" "*8 + "Top oil:")
            self.tolerance_topOilGTR.addPDF(pdf)
            pdf.multi_cell(txt=" "*8 + "Average winding:")
            self.tolerance_aveWindGTR.addPDF(pdf)
            pdf.multi_cell(txt=" "*8 + "Hot-spot:")
            self.tolerance_hsGTR.addPDF(pdf)
            pdf.ln()

            # Image du transfo
            for warr in self.lst_UI_WindingArrangement:
                warr.setSelected(False)
            self.updateGraphicsSize()
            rectItems = self.scene_tfo.itemsBoundingRect()
            scale = min(pdf.max_width_px/rectItems.toRect().width(), pdf.max_heigth_px/rectItems.toRect().height())
            path_png, targetSize = gui_utils.getImageFromQGraphics(self.scene_tfo, rectItems, scale)

            # Taille de l'image
            w_items = pdf.pixelToMm(targetSize.width())
            h_items = pdf.pixelToMm(targetSize.height())
            scale = min(1, pdf.max_width_mm/w_items, 100/h_items)
            pdf.image(path_png, fmt="png", w=w_items*scale, align="C")

            # Liste des enroulements par ordre de tension décroissante
            for w in self.getLstWindingVoltageDescendingNameAlphabetical():
                pdf.ln()
                w.addPDF(pdf, part, lst_id_calcul)

        elif "data_detail" in part:
            pdf.ln()
            pdf.toc_entry("Windings arrangement", 2)

            for w in self.lst_UI_WindingArrangement:
                w.addPDF(pdf, part, lst_id_calcul)

    def addWord(self, tt_template, part="", prefix=""):
        """
        Remplissage du template Word
        """
        tt_template.addHeader("Rating plate", 2)

        ### Main
        tt_template.addHeader("Main", 3)
        tt_template.addLine("RP_main_reference", self.ui_le_reference.text())
        tt_template.addLine("RP_main_nb_phase", self.ui_cb_nbrePhases.currentText())
        if self.isTriphase():
            tt_template.addLine("RP_main_phase_design", "Three-phase")
            tt_template.addLine("RP_main_phase_design_FR", "Triphasé")
        else:
            tt_template.addLine("RP_main_phase_design", "Single-phase")
            tt_template.addLine("RP_main_phase_design_FR", "Monophasé")
        tt_template.addLine("RP_main_frequency", self.ui_cb_frequency.currentText(), unit="Hz")
        if self.isCoreType():
            tt_template.addLine("RP_main_design", "Core-type")
            tt_template.addLine("RP_main_design_FR", "Colonne")
        else:
            tt_template.addLine("RP_main_design", "shell-type")
            tt_template.addLine("RP_main_design_FR", "Cuirassé")
        tt_template.addLine("RP_main_spec_top_oil_TR", self.tolerance_topOilGTR.text(), unit="K")
        tt_template.addLine("RP_main_spec_winding_TR", self.tolerance_aveWindGTR.text(), unit="K")
        tt_template.addLine("RP_main_spec_hotspot_TR", self.tolerance_hsGTR.text(), unit="K")

        # Image du transfo
        for warr in self.lst_UI_WindingArrangement:
            warr.setSelected(False)
        self.updateGraphicsSize()
        rectItems = self.scene_tfo.itemsBoundingRect()
        path_png, _ = gui_utils.getImageFromQGraphics(self.scene_tfo, rectItems)
        tt_template.addImage("RP_main_windings_arrangement", path_png)

        ### Magnetic circuit
        tt_template.addHeader("Magnetic circuit", 3)
        tt_template.addLine("RP_main_magnetic_circuit_nb_limb", self.ui_cb_nbreLimbs.currentText())

        ### Windings
        tt_template.addHeader("Windings", 3)
        tt_template.addLine("RP_windings_nb_winding", len(self.getLstWinding()))
        tt_template.addParagraph("Windings indices are defined voltage descending then alphabetical order of name (1 = highest voltage).")
        for k, w in enumerate(self.getLstWindingVoltageDescendingNameAlphabetical()):
            w.addWord(tt_template, prefix="RP_windings_%i"%(k + 1))

        ### Cooling
        tt_template.addHeader("Cooling", 3)
        tt_template.addLine("RP_cooling_mode", self.cooling_mode)
        if self.ui_cb_cool_refIntMode.currentText() in ["F", "D"]:
            tt_template.addLine("RP_cooling_nb_oil_pump", self.getNumberOilPumps())
            try:
                total = self.getNumberOilPumps()*float(self.ui_le_oilFlow.text())
            except:
                total = 0.0
            if self.ui_cb_oil_flow_unit.currentText() == "m3/h":
                tt_template.addLine("RP_cooling_oil_flow_per_pump", self.ui_le_oilFlow.text(), unit="m3/h")
                tt_template.addLine("RP_cooling_oil_flow_total", total, unit="m3/h")
            elif self.ui_cb_oil_flow_unit.currentText() == "l/s":
                tt_template.addLine("RP_cooling_oil_flow_per_pump", self.ui_le_oilFlow.text(), unit="l/s")
                tt_template.addLine("RP_cooling_oil_flow_total", total, unit="l/s")
            else:
                raise Exception("Argument '" + str(self.ui_cb_oil_flow_unit.currentText()) + "' inconnu (valeur attendue : m3/h ou l/s)")
        if self.ui_cb_cool_refExt.currentText() == "W":
            tt_template.addLine("RP_cooling_nb_water_pump", self.ui_spBox_nbWaterPumps.value())
            try:
                total = self.ui_spBox_nbWaterPumps.value()*float(self.ui_le_waterFlow.text())
            except:
                total = 0.0
            if self.ui_cb_oil_flow_unit.currentText() == "m3/h":
                tt_template.addLine("RP_cooling_water_flow_per_pump", self.ui_le_waterFlow.text(), unit="m3/h")
                tt_template.addLine("RP_cooling_water_flow_total", total, unit="m3/h")
            elif self.ui_cb_oil_flow_unit.currentText() == "l/s":
                tt_template.addLine("RP_cooling_water_flow_per_pump", self.ui_le_waterFlow.text(), unit="l/s")
                tt_template.addLine("RP_cooling_water_flow_total", total, unit="l/s")
            else:
                raise Exception("Argument '" + str(self.ui_cb_water_flow_unit.currentText()) + "' inconnu (valeur attendue : m3/h ou l/s)")

        tt_template.addLine("RP_cooling_bottom_oil_TR", self.ui_le_bottomTR.text(), unit="K")
        if self.ui_cb_cool_refExt.currentText() == "W":
            tt_template.addLine("RP_cooling_water_T", self.ui_le_ambientT.text(), unit="°C")
        else:
            tt_template.addLine("RP_cooling_ambient_T", self.ui_le_ambientT.text(), unit="°C")

        if self.cooling_mode == "ODAF":
            if self.ui_rbut_subExchangers.isChecked():
                tt_template.addLine("RP_cooling_modulation_type", "Sub-exchangers modulation")
                row_title = ["Cooling stage", "No. of sub-exchangers in operation", "Temp. switch on\nToil > °C", "Temp. switch off\nToil < °C"]
                tab_data = []
                for row in range(self.model_tab_EM.rowCount()):
                    data = []
                    for col in range(self.model_tab_EM.columnCount()):
                        data.append(self.model_tab_EM.item(row, col).text())
                    tab_data.append(data)
                tt_template.addTableRow("RP_cooling_modulation_detail", [row_title] + tab_data)
                tt_template.addLine("RP_cooling_modulation_nb_fan", self.ui_spBox_nbreFans_EM.value())
                tt_template.addLine("RP_cooling_modulation_nb_sub_exchanger", self.ui_le_nbreSubExchangers_EM.text())

            else:
                tt_template.addLine("RP_cooling_modulation_type", "Fans modulation")
                row_title = ["Cooling stage", "No. of fans in operation", "Temp. switch on\nToil > °C", "Temp. switch off\nToil < °C"]
                tab_data = []
                for row in range(self.model_tab_FM.rowCount()):
                    data = []
                    for col in range(self.model_tab_FM.columnCount()):
                        data.append(self.model_tab_FM.item(row, col).text())
                    tab_data.append(data)
                tt_template.addTableRow("RP_cooling_modulation_detail", [row_title] + tab_data)
                tt_template.addLine("RP_cooling_modulation_nb_pump", self.ui_spBox_nbrePumps_FM.value())
                tt_template.addLine("RP_cooling_modulation_nb_fan", self.ui_le_nbreFans_FM.text())

            tt_template.addLine("RP_cooling_pump_consumption", self.ui_le_powerPump.text(), unit="W")
            tt_template.addLine("RP_cooling_fan_consumption", self.ui_le_powerFan.text(), unit="W")

    def loadXML(self, tmpSaveDirPath):
        """
        Chargement du fichier xml dans le ttx
        """
        path_xml = join(tmpSaveDirPath, "design", "ratingPlate.xml")
        if not exists(path_xml):
            return

        file = QFile(path_xml)
        doc = QDomDocument()
        if not file.open(QIODevice.ReadOnly):
            file.close()
            raise Exception("Probleme lecture du fichier %s"%path_xml)
        if not doc.setContent(file):
            file.close()
            raise Exception("Probleme lecture du fichier %s"%path_xml)
        file.close()

        root = doc.documentElement()
        if root.isNull():
            return

        self.disconnectModification()

        self.ui_le_reference.setText(root.firstChildElement("reference").text())
        self.ui_cb_nbrePhases.setCurrentText(root.firstChildElement("phase_nb").text())
        self.ui_cb_frequency.setCurrentText(root.firstChildElement("rated_freq_Hz").text())
        if not root.firstChildElement("design").isNull():
            if root.firstChildElement("design").text() == "core":
                self.ui_rbut_core.setChecked(True)
            else:
                self.ui_rbut_shell.setChecked(True)
        self.ui_cb_nbreLimbs.setCurrentText(root.firstChildElement("limbs_nb").text())

        tag_cool_type = root.firstChildElement("cooling_type")
        self.ui_cb_cool_refInt.setCurrentText(tag_cool_type.firstChildElement("internal_medium").text())
        self.ui_cb_cool_refIntMode.setCurrentText(tag_cool_type.firstChildElement("internal_mode").text())
        self.ui_cb_cool_refExt.setCurrentText(tag_cool_type.firstChildElement("external_medium").text())
        self.ui_cb_cool_refExtMode.setCurrentText(tag_cool_type.firstChildElement("external_mode").text())

        tag_cool = root.firstChildElement("cooling")

        # Huile
        self.ui_spBox_nbOilPumps.setValue(int(tag_cool.firstChildElement("N_pumps").text()))

        # attention ! on ne fait pas de if elif else pour rester compatible avec les anciens ttx (pas de champ oil_pump_unit!!!)
        oil_flow_unit = tag_cool.firstChildElement("oil_pump_unit").text()
        if oil_flow_unit == "l/s":
            self.ui_cb_oil_flow_unit.setCurrentText("l/s")
            self.ui_le_oilFlow.setText(tag_cool.firstChildElement("oil_pump_l.s-1").text())
        # si oil_pump_unit n'est pas dans le XML (ancienne version), c'est qu'on était en m3/h donc on passe dans le else
        else:
            self.ui_cb_oil_flow_unit.setCurrentText("m3/h")
            self.ui_le_oilFlow.setText(tag_cool.firstChildElement("oil_pump_m3.h-1").text())

        # Eau (non présent dans les anciens ttx)
        if not tag_cool.firstChildElement("N_water_pumps").isNull():
            self.ui_spBox_nbWaterPumps.setValue(int(tag_cool.firstChildElement("N_water_pumps").text()))
            water_pump_unit = tag_cool.firstChildElement("water_pump_unit").text()
            if water_pump_unit == "l/s":
                self.ui_cb_water_flow_unit.setCurrentText("l/s")
                self.ui_le_waterFlow.setText(tag_cool.firstChildElement("water_pump_l.s-1").text())
            else:
                self.ui_cb_water_flow_unit.setCurrentText("m3/h")
                self.ui_le_waterFlow.setText(tag_cool.firstChildElement("water_pump_m3.h-1").text())

        self.ui_le_bottomTR.setText(tag_cool.firstChildElement("oil_bottom_TR_K").text())
        self.ui_le_ambientT.setText(tag_cool.firstChildElement("ambient_T_C").text())

        # Stades de réfrigération & co (non présent dans les anciens ttx)
        if not tag_cool.firstChildElement("coolers_adjustment_method").isNull():
            if tag_cool.firstChildElement("coolers_adjustment_method").text() == "fans":
                self.ui_rbut_fans.setChecked(True)
            else:
                self.ui_rbut_subExchangers.setChecked(True)
            self.ui_le_powerPump.setText(tag_cool.firstChildElement("pump_power_W").text())
            self.ui_le_powerFan.setText(tag_cool.firstChildElement("fan_power_W").text())

            # Fans modulation
            e_FM = tag_cool.firstChildElement("cooling_stage_FM")
            first_cs = True
            n = e_FM.firstChildElement()
            while not n.isNull():
                e_data = n.toElement()
                if first_cs:
                    first_cs = False
                else:
                    self.newCoolingStageFM()
                row = self.model_tab_FM.rowCount() - 1
                n2 = e_data.firstChildElement("val")
                kk = 1
                while not n2.isNull():
                    e_measurement = n2.toElement()
                    try:
                        tmp = float(e_measurement.text())
                    except:
                        pass
                    else:
                        self.model_tab_FM.item(row, kk).setData(tmp, Qt.EditRole)
                    kk = kk + 1
                    n2 = n2.nextSiblingElement("val")
                n = n.nextSiblingElement()
            self.ui_spBox_nbrePumps_FM.setValue(int(tag_cool.firstChildElement("N_pumps_FM").text()))

            # Sub-exchangers modulation
            e_EM = tag_cool.firstChildElement("cooling_stage_EM")
            first_cs = True
            n = e_EM.firstChildElement()
            while not n.isNull():
                e_data = n.toElement()
                if first_cs:
                    first_cs = False
                else:
                    self.newCoolingStageEM()
                row = self.model_tab_EM.rowCount() - 1
                n2 = e_data.firstChildElement("val")
                kk = 1
                while not n2.isNull():
                    e_measurement = n2.toElement()
                    try:
                        tmp = float(e_measurement.text())
                    except:
                        pass
                    else:
                        self.model_tab_EM.item(row, kk).setData(tmp, Qt.EditRole)
                    kk = kk + 1
                    n2 = n2.nextSiblingElement("val")
                n = n.nextSiblingElement()
            self.ui_spBox_nbreFans_EM.setValue(int(tag_cool.firstChildElement("N_fans_EM").text()))

        tag_guar = root.firstChildElement("guarantee")
        if not tag_guar.isNull():
            # Ancienne méthode
            self.tolerance_topOilGTR.set_user_defined()
            self.tolerance_topOilGTR.set_tolerance({'definition_option': 'C', "value":{"lower": tag_guar.firstChildElement("oil_top_TR_K").text(), "lower_included": True, "greater": "", "greater_included": True}})
            self.tolerance_topOilGTR.update_tolerance()
            self.tolerance_aveWindGTR.set_user_defined()
            self.tolerance_aveWindGTR.set_tolerance({'definition_option': 'C', "value":{"lower": tag_guar.firstChildElement("winding_TR_K").text(), "lower_included": True, "greater": "", "greater_included": True}})
            self.tolerance_aveWindGTR.update_tolerance()
            self.tolerance_hsGTR.set_user_defined()
            self.tolerance_hsGTR.set_tolerance({'definition_option': 'C', "value":{"lower": tag_guar.firstChildElement("hot_spot_TR_K").text(), "lower_included": True, "greater": "", "greater_included": True}})
            self.tolerance_hsGTR.update_tolerance()
        else:
            # Nouvelle méthode↑
            n = root.firstChildElement("tolerance")
            while not n.isNull():
                e_tolerance = n.toElement()
                for tol in [self.tolerance_topOilGTR, self.tolerance_aveWindGTR, self.tolerance_hsGTR]:
                    if e_tolerance.firstChildElement("id_tolerance").text() == tol.id_tolerance:
                        tol.loadXMLElement(e_tolerance)
                n = n.nextSiblingElement("tolerance")

        # Arrangements
        # On supprime le 2ème arrangement ajouté par défaut (pour gérer le cas d'un ttx avec un seul arrangement)
        self.deleteArrangement()

        n = root.firstChildElement("winding_arrangement")
        k_arr = 0
        while not n.isNull():
            e_arr = n.toElement()

            if k_arr < len(self.lst_UI_WindingArrangement):
                self.lst_UI_WindingArrangement[k_arr].loadXMLTree(e_arr)
            else:
                self.addArrangement().loadXMLTree(e_arr)

            k_arr = k_arr + 1
            n = n.nextSiblingElement("winding_arrangement")

        self.connectModification()
        self.updateWindingsData()

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
    win = UI_RatingPlate()

    # 3 - Affichage de la fenêtre
    win.show()
    app.exec()