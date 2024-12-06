# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ratingPlate.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QListView, QPushButton, QRadioButton,
    QScrollArea, QSizePolicy, QSpacerItem, QSpinBox,
    QSplitter, QTabWidget, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1844, 688)
        self.verticalLayout_13 = QVBoxLayout(Form)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.ui_splitter_main = QSplitter(Form)
        self.ui_splitter_main.setObjectName(u"ui_splitter_main")
        self.ui_splitter_main.setOrientation(Qt.Horizontal)
        self.ui_splitter_tfo = QSplitter(self.ui_splitter_main)
        self.ui_splitter_tfo.setObjectName(u"ui_splitter_tfo")
        self.ui_splitter_tfo.setOrientation(Qt.Vertical)
        self.ui_frame_displayTfo = QFrame(self.ui_splitter_tfo)
        self.ui_frame_displayTfo.setObjectName(u"ui_frame_displayTfo")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ui_frame_displayTfo.sizePolicy().hasHeightForWidth())
        self.ui_frame_displayTfo.setSizePolicy(sizePolicy)
        self.ui_frame_displayTfo.setFrameShape(QFrame.StyledPanel)
        self.ui_frame_displayTfo.setFrameShadow(QFrame.Raised)
        self.ui_splitter_tfo.addWidget(self.ui_frame_displayTfo)
        self.layoutWidget = QWidget(self.ui_splitter_tfo)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout_6 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)

        self.ui_frame_lgdTfo = QFrame(self.layoutWidget)
        self.ui_frame_lgdTfo.setObjectName(u"ui_frame_lgdTfo")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.ui_frame_lgdTfo.sizePolicy().hasHeightForWidth())
        self.ui_frame_lgdTfo.setSizePolicy(sizePolicy1)
        self.ui_frame_lgdTfo.setFrameShape(QFrame.StyledPanel)
        self.ui_frame_lgdTfo.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_5.addWidget(self.ui_frame_lgdTfo)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_5)


        self.verticalLayout_6.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_15)

        self.ui_btn_freeze = QPushButton(self.layoutWidget)
        self.ui_btn_freeze.setObjectName(u"ui_btn_freeze")
        self.ui_btn_freeze.setIconSize(QSize(40, 40))

        self.horizontalLayout_14.addWidget(self.ui_btn_freeze)

        self.ui_btn_fat_id = QPushButton(self.layoutWidget)
        self.ui_btn_fat_id.setObjectName(u"ui_btn_fat_id")
        self.ui_btn_fat_id.setIconSize(QSize(40, 40))

        self.horizontalLayout_14.addWidget(self.ui_btn_fat_id)

        self.ui_btn_ope_id = QPushButton(self.layoutWidget)
        self.ui_btn_ope_id.setObjectName(u"ui_btn_ope_id")
        self.ui_btn_ope_id.setIconSize(QSize(40, 40))

        self.horizontalLayout_14.addWidget(self.ui_btn_ope_id)

        self.horizontalSpacer_16 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_16)


        self.verticalLayout_6.addLayout(self.horizontalLayout_14)

        self.verticalSpacer_4 = QSpacerItem(93, 13, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_4)

        self.ui_splitter_tfo.addWidget(self.layoutWidget)
        self.ui_splitter_main.addWidget(self.ui_splitter_tfo)
        self.ui_tabWidget = QTabWidget(self.ui_splitter_main)
        self.ui_tabWidget.setObjectName(u"ui_tabWidget")
        self.ui_tabWidget.setAutoFillBackground(True)
        self.ui_wdg_main = QWidget()
        self.ui_wdg_main.setObjectName(u"ui_wdg_main")
        self.ui_wdg_main.setAutoFillBackground(True)
        self.verticalLayout_10 = QVBoxLayout(self.ui_wdg_main)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.scrollArea = QScrollArea(self.ui_wdg_main)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setAutoFillBackground(True)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1195, 621))
        self.scrollAreaWidgetContents.setAutoFillBackground(True)
        self.verticalLayout_9 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_7 = QLabel(self.scrollAreaWidgetContents)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(30, 0))

        self.gridLayout.addWidget(self.label_7, 2, 2, 1, 1)

        self.label_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)

        self.ui_le_reference = QLineEdit(self.scrollAreaWidgetContents)
        self.ui_le_reference.setObjectName(u"ui_le_reference")

        self.gridLayout.addWidget(self.ui_le_reference, 0, 1, 1, 1)

        self.label_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(150, 0))

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.ui_cb_nbrePhases = QComboBox(self.scrollAreaWidgetContents)
        self.ui_cb_nbrePhases.setObjectName(u"ui_cb_nbrePhases")

        self.gridLayout.addWidget(self.ui_cb_nbrePhases, 1, 1, 1, 1)

        self.label_5 = QLabel(self.scrollAreaWidgetContents)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)

        self.ui_cb_frequency = QComboBox(self.scrollAreaWidgetContents)
        self.ui_cb_frequency.setObjectName(u"ui_cb_frequency")

        self.gridLayout.addWidget(self.ui_cb_frequency, 2, 1, 1, 1)

        self.ui_rbut_core = QRadioButton(self.scrollAreaWidgetContents)
        self.ui_rbut_core.setObjectName(u"ui_rbut_core")

        self.gridLayout.addWidget(self.ui_rbut_core, 3, 1, 1, 1)

        self.ui_rbut_shell = QRadioButton(self.scrollAreaWidgetContents)
        self.ui_rbut_shell.setObjectName(u"ui_rbut_shell")

        self.gridLayout.addWidget(self.ui_rbut_shell, 4, 1, 1, 1)

        self.label_9 = QLabel(self.scrollAreaWidgetContents)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 3, 0, 2, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_5)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.ui_grpBox_guarantee = QGroupBox(self.scrollAreaWidgetContents)
        self.ui_grpBox_guarantee.setObjectName(u"ui_grpBox_guarantee")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.ui_grpBox_guarantee.sizePolicy().hasHeightForWidth())
        self.ui_grpBox_guarantee.setSizePolicy(sizePolicy2)
        self.gridLayout_3 = QGridLayout(self.ui_grpBox_guarantee)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_21 = QLabel(self.ui_grpBox_guarantee)
        self.label_21.setObjectName(u"label_21")

        self.gridLayout_3.addWidget(self.label_21, 2, 2, 1, 1)

        self.label_20 = QLabel(self.ui_grpBox_guarantee)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout_3.addWidget(self.label_20, 2, 0, 1, 1)

        self.label_17 = QLabel(self.ui_grpBox_guarantee)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setMinimumSize(QSize(30, 0))

        self.gridLayout_3.addWidget(self.label_17, 0, 2, 1, 1)

        self.label_19 = QLabel(self.ui_grpBox_guarantee)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_3.addWidget(self.label_19, 1, 2, 1, 1)

        self.label_16 = QLabel(self.ui_grpBox_guarantee)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(150, 0))

        self.gridLayout_3.addWidget(self.label_16, 0, 0, 1, 1)

        self.label_18 = QLabel(self.ui_grpBox_guarantee)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout_3.addWidget(self.label_18, 1, 0, 1, 1)

        self.ui_btn_tolerance_topOilGTR = QPushButton(self.ui_grpBox_guarantee)
        self.ui_btn_tolerance_topOilGTR.setObjectName(u"ui_btn_tolerance_topOilGTR")

        self.gridLayout_3.addWidget(self.ui_btn_tolerance_topOilGTR, 0, 1, 1, 1)

        self.ui_btn_tolerance_aveWindGTR = QPushButton(self.ui_grpBox_guarantee)
        self.ui_btn_tolerance_aveWindGTR.setObjectName(u"ui_btn_tolerance_aveWindGTR")

        self.gridLayout_3.addWidget(self.ui_btn_tolerance_aveWindGTR, 1, 1, 1, 1)

        self.ui_btn_tolerance_hsGTR = QPushButton(self.ui_grpBox_guarantee)
        self.ui_btn_tolerance_hsGTR.setObjectName(u"ui_btn_tolerance_hsGTR")

        self.gridLayout_3.addWidget(self.ui_btn_tolerance_hsGTR, 2, 1, 1, 1)


        self.verticalLayout_7.addWidget(self.ui_grpBox_guarantee)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_6)


        self.horizontalLayout_2.addLayout(self.verticalLayout_7)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout_9.addLayout(self.horizontalLayout_2)

        self.ui_grpBox_windArr = QGroupBox(self.scrollAreaWidgetContents)
        self.ui_grpBox_windArr.setObjectName(u"ui_grpBox_windArr")
        self.verticalLayout_2 = QVBoxLayout(self.ui_grpBox_windArr)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_27 = QLabel(self.ui_grpBox_windArr)
        self.label_27.setObjectName(u"label_27")

        self.verticalLayout_2.addWidget(self.label_27)

        self.ui_wdg_windArr = QWidget(self.ui_grpBox_windArr)
        self.ui_wdg_windArr.setObjectName(u"ui_wdg_windArr")

        self.verticalLayout_2.addWidget(self.ui_wdg_windArr)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_6)

        self.ui_btn_add = QPushButton(self.ui_grpBox_windArr)
        self.ui_btn_add.setObjectName(u"ui_btn_add")
        self.ui_btn_add.setMinimumSize(QSize(110, 0))

        self.horizontalLayout_6.addWidget(self.ui_btn_add)

        self.ui_btn_delete = QPushButton(self.ui_grpBox_windArr)
        self.ui_btn_delete.setObjectName(u"ui_btn_delete")
        self.ui_btn_delete.setMinimumSize(QSize(110, 0))

        self.horizontalLayout_6.addWidget(self.ui_btn_delete)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_7)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)


        self.verticalLayout_9.addWidget(self.ui_grpBox_windArr)

        self.verticalSpacer = QSpacerItem(20, 216, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_9.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_10.addWidget(self.scrollArea)

        self.ui_tabWidget.addTab(self.ui_wdg_main, "")
        self.ui_wdg_mc = QWidget()
        self.ui_wdg_mc.setObjectName(u"ui_wdg_mc")
        self.ui_wdg_mc.setAutoFillBackground(True)
        self.verticalLayout_3 = QVBoxLayout(self.ui_wdg_mc)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_8 = QLabel(self.ui_wdg_mc)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_4.addWidget(self.label_8, 0, 0, 1, 1)

        self.ui_cb_nbreLimbs = QComboBox(self.ui_wdg_mc)
        self.ui_cb_nbreLimbs.setObjectName(u"ui_cb_nbreLimbs")

        self.gridLayout_4.addWidget(self.ui_cb_nbreLimbs, 0, 1, 1, 1)


        self.horizontalLayout_3.addLayout(self.gridLayout_4)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.verticalSpacer_2 = QSpacerItem(20, 530, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)

        self.ui_tabWidget.addTab(self.ui_wdg_mc, "")
        self.ui_wdg_windings = QWidget()
        self.ui_wdg_windings.setObjectName(u"ui_wdg_windings")
        self.ui_wdg_windings.setAutoFillBackground(True)
        self.verticalLayout_11 = QVBoxLayout(self.ui_wdg_windings)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.ui_splitter_windings = QSplitter(self.ui_wdg_windings)
        self.ui_splitter_windings.setObjectName(u"ui_splitter_windings")
        self.ui_splitter_windings.setOrientation(Qt.Horizontal)
        self.ui_list_wind = QListView(self.ui_splitter_windings)
        self.ui_list_wind.setObjectName(u"ui_list_wind")
        self.ui_list_wind.setMaximumSize(QSize(16777215, 16777215))
        self.ui_splitter_windings.addWidget(self.ui_list_wind)
        self.ui_frame_windData = QFrame(self.ui_splitter_windings)
        self.ui_frame_windData.setObjectName(u"ui_frame_windData")
        self.ui_frame_windData.setFrameShape(QFrame.StyledPanel)
        self.ui_frame_windData.setFrameShadow(QFrame.Raised)
        self.ui_splitter_windings.addWidget(self.ui_frame_windData)

        self.verticalLayout_11.addWidget(self.ui_splitter_windings)

        self.ui_tabWidget.addTab(self.ui_wdg_windings, "")
        self.ui_wdg_cooling = QWidget()
        self.ui_wdg_cooling.setObjectName(u"ui_wdg_cooling")
        self.ui_wdg_cooling.setAutoFillBackground(True)
        self.horizontalLayout_13 = QHBoxLayout(self.ui_wdg_cooling)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_6 = QLabel(self.ui_wdg_cooling)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_5.addWidget(self.label_6, 0, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.ui_cb_cool_refInt = QComboBox(self.ui_wdg_cooling)
        self.ui_cb_cool_refInt.setObjectName(u"ui_cb_cool_refInt")

        self.horizontalLayout.addWidget(self.ui_cb_cool_refInt)

        self.ui_cb_cool_refIntMode = QComboBox(self.ui_wdg_cooling)
        self.ui_cb_cool_refIntMode.setObjectName(u"ui_cb_cool_refIntMode")

        self.horizontalLayout.addWidget(self.ui_cb_cool_refIntMode)

        self.ui_cb_cool_refExt = QComboBox(self.ui_wdg_cooling)
        self.ui_cb_cool_refExt.setObjectName(u"ui_cb_cool_refExt")

        self.horizontalLayout.addWidget(self.ui_cb_cool_refExt)

        self.ui_cb_cool_refExtMode = QComboBox(self.ui_wdg_cooling)
        self.ui_cb_cool_refExtMode.setObjectName(u"ui_cb_cool_refExtMode")

        self.horizontalLayout.addWidget(self.ui_cb_cool_refExtMode)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_13)


        self.gridLayout_5.addLayout(self.horizontalLayout, 0, 1, 1, 1)


        self.verticalLayout_12.addLayout(self.gridLayout_5)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.ui_grpBox_coolData = QGroupBox(self.ui_wdg_cooling)
        self.ui_grpBox_coolData.setObjectName(u"ui_grpBox_coolData")
        sizePolicy2.setHeightForWidth(self.ui_grpBox_coolData.sizePolicy().hasHeightForWidth())
        self.ui_grpBox_coolData.setSizePolicy(sizePolicy2)
        self.gridLayout_2 = QGridLayout(self.ui_grpBox_coolData)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.ui_lbl_waterFlow = QLabel(self.ui_grpBox_coolData)
        self.ui_lbl_waterFlow.setObjectName(u"ui_lbl_waterFlow")

        self.gridLayout_2.addWidget(self.ui_lbl_waterFlow, 3, 0, 1, 1)

        self.ui_le_oilFlow = QLineEdit(self.ui_grpBox_coolData)
        self.ui_le_oilFlow.setObjectName(u"ui_le_oilFlow")

        self.gridLayout_2.addWidget(self.ui_le_oilFlow, 1, 1, 1, 1)

        self.ui_le_bottomTR = QLineEdit(self.ui_grpBox_coolData)
        self.ui_le_bottomTR.setObjectName(u"ui_le_bottomTR")

        self.gridLayout_2.addWidget(self.ui_le_bottomTR, 4, 1, 1, 1)

        self.label_12 = QLabel(self.ui_grpBox_coolData)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_2.addWidget(self.label_12, 4, 0, 1, 1)

        self.ui_le_ambientT = QLineEdit(self.ui_grpBox_coolData)
        self.ui_le_ambientT.setObjectName(u"ui_le_ambientT")

        self.gridLayout_2.addWidget(self.ui_le_ambientT, 5, 1, 1, 1)

        self.ui_lbl_oilFlow = QLabel(self.ui_grpBox_coolData)
        self.ui_lbl_oilFlow.setObjectName(u"ui_lbl_oilFlow")

        self.gridLayout_2.addWidget(self.ui_lbl_oilFlow, 1, 0, 1, 1)

        self.label_15 = QLabel(self.ui_grpBox_coolData)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_2.addWidget(self.label_15, 5, 2, 1, 1)

        self.ui_lbl_nbOilPumps = QLabel(self.ui_grpBox_coolData)
        self.ui_lbl_nbOilPumps.setObjectName(u"ui_lbl_nbOilPumps")
        self.ui_lbl_nbOilPumps.setMinimumSize(QSize(150, 0))

        self.gridLayout_2.addWidget(self.ui_lbl_nbOilPumps, 0, 0, 1, 1)

        self.ui_spBox_nbOilPumps = QSpinBox(self.ui_grpBox_coolData)
        self.ui_spBox_nbOilPumps.setObjectName(u"ui_spBox_nbOilPumps")

        self.gridLayout_2.addWidget(self.ui_spBox_nbOilPumps, 0, 1, 1, 1)

        self.ui_lbl_ambientT = QLabel(self.ui_grpBox_coolData)
        self.ui_lbl_ambientT.setObjectName(u"ui_lbl_ambientT")

        self.gridLayout_2.addWidget(self.ui_lbl_ambientT, 5, 0, 1, 1)

        self.ui_cb_oil_flow_unit = QComboBox(self.ui_grpBox_coolData)
        self.ui_cb_oil_flow_unit.setObjectName(u"ui_cb_oil_flow_unit")

        self.gridLayout_2.addWidget(self.ui_cb_oil_flow_unit, 1, 2, 1, 1)

        self.label_13 = QLabel(self.ui_grpBox_coolData)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_2.addWidget(self.label_13, 4, 2, 1, 1)

        self.ui_lbl_nbWaterPumps = QLabel(self.ui_grpBox_coolData)
        self.ui_lbl_nbWaterPumps.setObjectName(u"ui_lbl_nbWaterPumps")
        self.ui_lbl_nbWaterPumps.setMinimumSize(QSize(150, 0))

        self.gridLayout_2.addWidget(self.ui_lbl_nbWaterPumps, 2, 0, 1, 1)

        self.ui_spBox_nbWaterPumps = QSpinBox(self.ui_grpBox_coolData)
        self.ui_spBox_nbWaterPumps.setObjectName(u"ui_spBox_nbWaterPumps")

        self.gridLayout_2.addWidget(self.ui_spBox_nbWaterPumps, 2, 1, 1, 1)

        self.ui_le_waterFlow = QLineEdit(self.ui_grpBox_coolData)
        self.ui_le_waterFlow.setObjectName(u"ui_le_waterFlow")

        self.gridLayout_2.addWidget(self.ui_le_waterFlow, 3, 1, 1, 1)

        self.ui_cb_water_flow_unit = QComboBox(self.ui_grpBox_coolData)
        self.ui_cb_water_flow_unit.setObjectName(u"ui_cb_water_flow_unit")

        self.gridLayout_2.addWidget(self.ui_cb_water_flow_unit, 3, 2, 1, 1)


        self.horizontalLayout_12.addWidget(self.ui_grpBox_coolData)

        self.horizontalSpacer_14 = QSpacerItem(37, 17, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_14)


        self.verticalLayout_12.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.ui_grpBox_method = QGroupBox(self.ui_wdg_cooling)
        self.ui_grpBox_method.setObjectName(u"ui_grpBox_method")
        self.gridLayout_7 = QGridLayout(self.ui_grpBox_method)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.ui_rbut_fans = QRadioButton(self.ui_grpBox_method)
        self.ui_rbut_fans.setObjectName(u"ui_rbut_fans")

        self.gridLayout_7.addWidget(self.ui_rbut_fans, 0, 0, 1, 1)

        self.ui_rbut_subExchangers = QRadioButton(self.ui_grpBox_method)
        self.ui_rbut_subExchangers.setObjectName(u"ui_rbut_subExchangers")

        self.gridLayout_7.addWidget(self.ui_rbut_subExchangers, 1, 0, 1, 1)


        self.horizontalLayout_11.addWidget(self.ui_grpBox_method)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_3)


        self.verticalLayout_12.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.ui_grpBox_power = QGroupBox(self.ui_wdg_cooling)
        self.ui_grpBox_power.setObjectName(u"ui_grpBox_power")
        self.gridLayout_6 = QGridLayout(self.ui_grpBox_power)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.ui_lbl_ambientT_2 = QLabel(self.ui_grpBox_power)
        self.ui_lbl_ambientT_2.setObjectName(u"ui_lbl_ambientT_2")

        self.gridLayout_6.addWidget(self.ui_lbl_ambientT_2, 0, 0, 1, 1)

        self.ui_le_powerPump = QLineEdit(self.ui_grpBox_power)
        self.ui_le_powerPump.setObjectName(u"ui_le_powerPump")

        self.gridLayout_6.addWidget(self.ui_le_powerPump, 0, 1, 1, 1)

        self.label_22 = QLabel(self.ui_grpBox_power)
        self.label_22.setObjectName(u"label_22")

        self.gridLayout_6.addWidget(self.label_22, 0, 2, 1, 1)

        self.ui_lbl_ambientT_3 = QLabel(self.ui_grpBox_power)
        self.ui_lbl_ambientT_3.setObjectName(u"ui_lbl_ambientT_3")

        self.gridLayout_6.addWidget(self.ui_lbl_ambientT_3, 1, 0, 1, 1)

        self.ui_le_powerFan = QLineEdit(self.ui_grpBox_power)
        self.ui_le_powerFan.setObjectName(u"ui_le_powerFan")

        self.gridLayout_6.addWidget(self.ui_le_powerFan, 1, 1, 1, 1)

        self.label_23 = QLabel(self.ui_grpBox_power)
        self.label_23.setObjectName(u"label_23")

        self.gridLayout_6.addWidget(self.label_23, 1, 2, 1, 1)


        self.horizontalLayout_10.addWidget(self.ui_grpBox_power)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_12)


        self.verticalLayout_12.addLayout(self.horizontalLayout_10)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_12.addItem(self.verticalSpacer_7)


        self.horizontalLayout_13.addLayout(self.verticalLayout_12)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.ui_grpBox_fansModulation = QGroupBox(self.ui_wdg_cooling)
        self.ui_grpBox_fansModulation.setObjectName(u"ui_grpBox_fansModulation")
        self.verticalLayout_4 = QVBoxLayout(self.ui_grpBox_fansModulation)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.ui_widget_FM = QWidget(self.ui_grpBox_fansModulation)
        self.ui_widget_FM.setObjectName(u"ui_widget_FM")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.ui_widget_FM.sizePolicy().hasHeightForWidth())
        self.ui_widget_FM.setSizePolicy(sizePolicy3)

        self.verticalLayout_4.addWidget(self.ui_widget_FM)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.ui_btn_new_FM = QPushButton(self.ui_grpBox_fansModulation)
        self.ui_btn_new_FM.setObjectName(u"ui_btn_new_FM")

        self.horizontalLayout_4.addWidget(self.ui_btn_new_FM)

        self.ui_btn_delete_FM = QPushButton(self.ui_grpBox_fansModulation)
        self.ui_btn_delete_FM.setObjectName(u"ui_btn_delete_FM")

        self.horizontalLayout_4.addWidget(self.ui_btn_delete_FM)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_8)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.ui_lbl_ambientT_4 = QLabel(self.ui_grpBox_fansModulation)
        self.ui_lbl_ambientT_4.setObjectName(u"ui_lbl_ambientT_4")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.ui_lbl_ambientT_4)

        self.ui_spBox_nbrePumps_FM = QSpinBox(self.ui_grpBox_fansModulation)
        self.ui_spBox_nbrePumps_FM.setObjectName(u"ui_spBox_nbrePumps_FM")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.ui_spBox_nbrePumps_FM)

        self.ui_lbl_ambientT_5 = QLabel(self.ui_grpBox_fansModulation)
        self.ui_lbl_ambientT_5.setObjectName(u"ui_lbl_ambientT_5")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.ui_lbl_ambientT_5)

        self.ui_le_nbreFans_FM = QLineEdit(self.ui_grpBox_fansModulation)
        self.ui_le_nbreFans_FM.setObjectName(u"ui_le_nbreFans_FM")
        self.ui_le_nbreFans_FM.setEnabled(False)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.ui_le_nbreFans_FM)


        self.horizontalLayout_7.addLayout(self.formLayout)

        self.horizontalSpacer_9 = QSpacerItem(37, 17, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_9)


        self.verticalLayout_4.addLayout(self.horizontalLayout_7)


        self.verticalLayout_8.addWidget(self.ui_grpBox_fansModulation)

        self.ui_grpBox_subExchangersModulation = QGroupBox(self.ui_wdg_cooling)
        self.ui_grpBox_subExchangersModulation.setObjectName(u"ui_grpBox_subExchangersModulation")
        self.verticalLayout_5 = QVBoxLayout(self.ui_grpBox_subExchangersModulation)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.ui_widget_EM = QWidget(self.ui_grpBox_subExchangersModulation)
        self.ui_widget_EM.setObjectName(u"ui_widget_EM")
        sizePolicy3.setHeightForWidth(self.ui_widget_EM.sizePolicy().hasHeightForWidth())
        self.ui_widget_EM.setSizePolicy(sizePolicy3)

        self.verticalLayout_5.addWidget(self.ui_widget_EM)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.ui_btn_new_EM = QPushButton(self.ui_grpBox_subExchangersModulation)
        self.ui_btn_new_EM.setObjectName(u"ui_btn_new_EM")

        self.horizontalLayout_8.addWidget(self.ui_btn_new_EM)

        self.ui_btn_delete_EM = QPushButton(self.ui_grpBox_subExchangersModulation)
        self.ui_btn_delete_EM.setObjectName(u"ui_btn_delete_EM")

        self.horizontalLayout_8.addWidget(self.ui_btn_delete_EM)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_10)


        self.verticalLayout_5.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.ui_lbl_ambientT_6 = QLabel(self.ui_grpBox_subExchangersModulation)
        self.ui_lbl_ambientT_6.setObjectName(u"ui_lbl_ambientT_6")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.ui_lbl_ambientT_6)

        self.ui_spBox_nbreFans_EM = QSpinBox(self.ui_grpBox_subExchangersModulation)
        self.ui_spBox_nbreFans_EM.setObjectName(u"ui_spBox_nbreFans_EM")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.ui_spBox_nbreFans_EM)

        self.ui_lbl_ambientT_7 = QLabel(self.ui_grpBox_subExchangersModulation)
        self.ui_lbl_ambientT_7.setObjectName(u"ui_lbl_ambientT_7")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.ui_lbl_ambientT_7)

        self.ui_le_nbreSubExchangers_EM = QLineEdit(self.ui_grpBox_subExchangersModulation)
        self.ui_le_nbreSubExchangers_EM.setObjectName(u"ui_le_nbreSubExchangers_EM")
        self.ui_le_nbreSubExchangers_EM.setEnabled(False)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.ui_le_nbreSubExchangers_EM)


        self.horizontalLayout_9.addLayout(self.formLayout_2)

        self.horizontalSpacer_11 = QSpacerItem(37, 17, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_11)


        self.verticalLayout_5.addLayout(self.horizontalLayout_9)


        self.verticalLayout_8.addWidget(self.ui_grpBox_subExchangersModulation)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_3)


        self.horizontalLayout_13.addLayout(self.verticalLayout_8)

        self.ui_tabWidget.addTab(self.ui_wdg_cooling, "")
        self.ui_splitter_main.addWidget(self.ui_tabWidget)

        self.verticalLayout_13.addWidget(self.ui_splitter_main)

        QWidget.setTabOrder(self.ui_tabWidget, self.ui_le_reference)
        QWidget.setTabOrder(self.ui_le_reference, self.ui_cb_nbrePhases)
        QWidget.setTabOrder(self.ui_cb_nbrePhases, self.ui_cb_frequency)
        QWidget.setTabOrder(self.ui_cb_frequency, self.ui_rbut_core)
        QWidget.setTabOrder(self.ui_rbut_core, self.ui_rbut_shell)
        QWidget.setTabOrder(self.ui_rbut_shell, self.ui_btn_add)
        QWidget.setTabOrder(self.ui_btn_add, self.ui_btn_delete)
        QWidget.setTabOrder(self.ui_btn_delete, self.ui_cb_nbreLimbs)
        QWidget.setTabOrder(self.ui_cb_nbreLimbs, self.ui_list_wind)
        QWidget.setTabOrder(self.ui_list_wind, self.ui_cb_cool_refInt)
        QWidget.setTabOrder(self.ui_cb_cool_refInt, self.ui_cb_cool_refIntMode)
        QWidget.setTabOrder(self.ui_cb_cool_refIntMode, self.ui_cb_cool_refExt)
        QWidget.setTabOrder(self.ui_cb_cool_refExt, self.ui_cb_cool_refExtMode)
        QWidget.setTabOrder(self.ui_cb_cool_refExtMode, self.ui_spBox_nbOilPumps)
        QWidget.setTabOrder(self.ui_spBox_nbOilPumps, self.ui_le_oilFlow)
        QWidget.setTabOrder(self.ui_le_oilFlow, self.ui_cb_oil_flow_unit)
        QWidget.setTabOrder(self.ui_cb_oil_flow_unit, self.ui_spBox_nbWaterPumps)
        QWidget.setTabOrder(self.ui_spBox_nbWaterPumps, self.ui_le_waterFlow)
        QWidget.setTabOrder(self.ui_le_waterFlow, self.ui_cb_water_flow_unit)
        QWidget.setTabOrder(self.ui_cb_water_flow_unit, self.ui_le_bottomTR)
        QWidget.setTabOrder(self.ui_le_bottomTR, self.ui_le_ambientT)
        QWidget.setTabOrder(self.ui_le_ambientT, self.ui_rbut_fans)
        QWidget.setTabOrder(self.ui_rbut_fans, self.ui_rbut_subExchangers)
        QWidget.setTabOrder(self.ui_rbut_subExchangers, self.ui_le_powerPump)
        QWidget.setTabOrder(self.ui_le_powerPump, self.ui_le_powerFan)
        QWidget.setTabOrder(self.ui_le_powerFan, self.ui_btn_new_FM)
        QWidget.setTabOrder(self.ui_btn_new_FM, self.ui_btn_delete_FM)
        QWidget.setTabOrder(self.ui_btn_delete_FM, self.ui_spBox_nbrePumps_FM)
        QWidget.setTabOrder(self.ui_spBox_nbrePumps_FM, self.ui_le_nbreFans_FM)
        QWidget.setTabOrder(self.ui_le_nbreFans_FM, self.ui_btn_new_EM)
        QWidget.setTabOrder(self.ui_btn_new_EM, self.ui_btn_delete_EM)
        QWidget.setTabOrder(self.ui_btn_delete_EM, self.ui_spBox_nbreFans_EM)
        QWidget.setTabOrder(self.ui_spBox_nbreFans_EM, self.ui_le_nbreSubExchangers_EM)
        QWidget.setTabOrder(self.ui_le_nbreSubExchangers_EM, self.scrollArea)

        self.retranslateUi(Form)

        self.ui_tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.ui_btn_freeze.setText(QCoreApplication.translate("Form", u"Freeze", None))
        self.ui_btn_fat_id.setText(QCoreApplication.translate("Form", u"Configure FAT ID", None))
        self.ui_btn_ope_id.setText(QCoreApplication.translate("Form", u"Configure Operation ID", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"Hz", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Number of phases", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Reference", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>Rated frequency (f<span style=\" vertical-align:sub;\">r</span>)</p></body></html>", None))
        self.ui_rbut_core.setText(QCoreApplication.translate("Form", u"Core-type", None))
        self.ui_rbut_shell.setText(QCoreApplication.translate("Form", u"Shell-type", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"Design", None))
        self.ui_grpBox_guarantee.setTitle(QCoreApplication.translate("Form", u"Thermal specifications", None))
        self.label_21.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>K</p></body></html>", None))
        self.label_20.setText(QCoreApplication.translate("Form", u"Winding hot spot\n"
"temperature rise", None))
        self.label_17.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>K</p></body></html>", None))
        self.label_19.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>K</p></body></html>", None))
        self.label_16.setText(QCoreApplication.translate("Form", u"Top oil temperature rise", None))
        self.label_18.setText(QCoreApplication.translate("Form", u"Average winding\n"
"temperature rise", None))
        self.ui_btn_tolerance_topOilGTR.setText(QCoreApplication.translate("Form", u"Tol", None))
        self.ui_btn_tolerance_aveWindGTR.setText(QCoreApplication.translate("Form", u"Tol", None))
        self.ui_btn_tolerance_hsGTR.setText(QCoreApplication.translate("Form", u"Tol", None))
        self.ui_grpBox_windArr.setTitle(QCoreApplication.translate("Form", u"Windings arrangement", None))
        self.label_27.setText(QCoreApplication.translate("Form", u"Click on a winding to configure it or add a new one at the outer most position.\n"
"If not known, choose \"Classic\" it will have consequences on the Design Review coils definition and on the Load-Losses FAT.", None))
        self.ui_btn_add.setText(QCoreApplication.translate("Form", u"Add new", None))
        self.ui_btn_delete.setText(QCoreApplication.translate("Form", u"Delete selected", None))
        self.ui_tabWidget.setTabText(self.ui_tabWidget.indexOf(self.ui_wdg_main), QCoreApplication.translate("Form", u"Main", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"Number of limbs", None))
        self.ui_tabWidget.setTabText(self.ui_tabWidget.indexOf(self.ui_wdg_mc), QCoreApplication.translate("Form", u"Magnetic circuit", None))
        self.ui_tabWidget.setTabText(self.ui_tabWidget.indexOf(self.ui_wdg_windings), QCoreApplication.translate("Form", u"Windings", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"Type of cooling", None))
        self.ui_grpBox_coolData.setTitle(QCoreApplication.translate("Form", u"Cooling data", None))
        self.ui_lbl_waterFlow.setText(QCoreApplication.translate("Form", u"Water flow per pump", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"Bottom oil temperature rise", None))
        self.ui_lbl_oilFlow.setText(QCoreApplication.translate("Form", u"Oil flow per pump", None))
        self.label_15.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>\u00b0C</p></body></html>", None))
        self.ui_lbl_nbOilPumps.setText(QCoreApplication.translate("Form", u"Number of oil pumps", None))
        self.ui_lbl_ambientT.setText(QCoreApplication.translate("Form", u"Ambient temperature", None))
        self.label_13.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>K</p></body></html>", None))
        self.ui_lbl_nbWaterPumps.setText(QCoreApplication.translate("Form", u"Number of water pumps", None))
        self.ui_grpBox_method.setTitle(QCoreApplication.translate("Form", u"Coolers adjustment method", None))
        self.ui_rbut_fans.setText(QCoreApplication.translate("Form", u"Fans modulation", None))
        self.ui_rbut_subExchangers.setText(QCoreApplication.translate("Form", u"Sub-exchangers modulation", None))
        self.ui_grpBox_power.setTitle(QCoreApplication.translate("Form", u"Power consumption", None))
        self.ui_lbl_ambientT_2.setText(QCoreApplication.translate("Form", u"For 1 pump", None))
        self.ui_le_powerPump.setText(QCoreApplication.translate("Form", u"0.0", None))
        self.label_22.setText(QCoreApplication.translate("Form", u"W", None))
        self.ui_lbl_ambientT_3.setText(QCoreApplication.translate("Form", u"For 1 fan", None))
        self.ui_le_powerFan.setText(QCoreApplication.translate("Form", u"0.0", None))
        self.label_23.setText(QCoreApplication.translate("Form", u"W", None))
        self.ui_grpBox_fansModulation.setTitle(QCoreApplication.translate("Form", u"Cooling stage definition - Fans modulation", None))
        self.ui_btn_new_FM.setText(QCoreApplication.translate("Form", u"New", None))
        self.ui_btn_delete_FM.setText(QCoreApplication.translate("Form", u"Delete last", None))
        self.ui_lbl_ambientT_4.setText(QCoreApplication.translate("Form", u"Total number of oil pumps", None))
        self.ui_lbl_ambientT_5.setText(QCoreApplication.translate("Form", u"Total number of air fans", None))
        self.ui_grpBox_subExchangersModulation.setTitle(QCoreApplication.translate("Form", u"Cooling stage definition - Sub-exchangers modulation", None))
        self.ui_btn_new_EM.setText(QCoreApplication.translate("Form", u"New", None))
        self.ui_btn_delete_EM.setText(QCoreApplication.translate("Form", u"Delete last", None))
        self.ui_lbl_ambientT_6.setText(QCoreApplication.translate("Form", u"Total number of air fans", None))
        self.ui_lbl_ambientT_7.setText(QCoreApplication.translate("Form", u"Total number of sub-exchangers", None))
        self.ui_tabWidget.setTabText(self.ui_tabWidget.indexOf(self.ui_wdg_cooling), QCoreApplication.translate("Form", u"Cooling", None))
    # retranslateUi

