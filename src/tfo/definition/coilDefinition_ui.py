# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'coilDefinition.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QSplitter, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1008, 624)
        self.verticalLayout_4 = QVBoxLayout(Form)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.ui_splitter_A = QSplitter(Form)
        self.ui_splitter_A.setObjectName(u"ui_splitter_A")
        self.ui_splitter_A.setOrientation(Qt.Horizontal)
        self.layoutWidget = QWidget(self.ui_splitter_A)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.ui_gBox_view = QGroupBox(self.layoutWidget)
        self.ui_gBox_view.setObjectName(u"ui_gBox_view")
        self.verticalLayout = QVBoxLayout(self.ui_gBox_view)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.ui_chk_discs = QCheckBox(self.ui_gBox_view)
        self.ui_chk_discs.setObjectName(u"ui_chk_discs")

        self.verticalLayout.addWidget(self.ui_chk_discs)

        self.ui_chk_ducts = QCheckBox(self.ui_gBox_view)
        self.ui_chk_ducts.setObjectName(u"ui_chk_ducts")

        self.verticalLayout.addWidget(self.ui_chk_ducts)

        self.ui_chk_pressboards = QCheckBox(self.ui_gBox_view)
        self.ui_chk_pressboards.setObjectName(u"ui_chk_pressboards")

        self.verticalLayout.addWidget(self.ui_chk_pressboards)


        self.verticalLayout_2.addWidget(self.ui_gBox_view)

        self.ui_gBox_coilGeom = QGroupBox(self.layoutWidget)
        self.ui_gBox_coilGeom.setObjectName(u"ui_gBox_coilGeom")
        self.gridLayout = QGridLayout(self.ui_gBox_coilGeom)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_12 = QLabel(self.ui_gBox_coilGeom)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout.addWidget(self.label_12, 4, 0, 1, 1)

        self.label_10 = QLabel(self.ui_gBox_coilGeom)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 2, 0, 1, 1)

        self.ui_le_radSpacerWidth = QLineEdit(self.ui_gBox_coilGeom)
        self.ui_le_radSpacerWidth.setObjectName(u"ui_le_radSpacerWidth")

        self.gridLayout.addWidget(self.ui_le_radSpacerWidth, 4, 1, 1, 1)

        self.label_13 = QLabel(self.ui_gBox_coilGeom)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout.addWidget(self.label_13, 6, 0, 1, 1)

        self.label_15 = QLabel(self.ui_gBox_coilGeom)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout.addWidget(self.label_15, 6, 2, 1, 1)

        self.label_14 = QLabel(self.ui_gBox_coilGeom)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout.addWidget(self.label_14, 7, 0, 1, 1)

        self.ui_le_coilHeight = QLineEdit(self.ui_gBox_coilGeom)
        self.ui_le_coilHeight.setObjectName(u"ui_le_coilHeight")

        self.gridLayout.addWidget(self.ui_le_coilHeight, 6, 1, 1, 1)

        self.label_11 = QLabel(self.ui_gBox_coilGeom)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout.addWidget(self.label_11, 4, 2, 1, 1)

        self.ui_le_coilWidth = QLineEdit(self.ui_gBox_coilGeom)
        self.ui_le_coilWidth.setObjectName(u"ui_le_coilWidth")

        self.gridLayout.addWidget(self.ui_le_coilWidth, 7, 1, 1, 1)

        self.label_16 = QLabel(self.ui_gBox_coilGeom)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout.addWidget(self.label_16, 7, 2, 1, 1)

        self.ui_spBox_nbre_radSpacers = QSpinBox(self.ui_gBox_coilGeom)
        self.ui_spBox_nbre_radSpacers.setObjectName(u"ui_spBox_nbre_radSpacers")

        self.gridLayout.addWidget(self.ui_spBox_nbre_radSpacers, 2, 1, 1, 1)

        self.ui_le_innerRadius = QLineEdit(self.ui_gBox_coilGeom)
        self.ui_le_innerRadius.setObjectName(u"ui_le_innerRadius")

        self.gridLayout.addWidget(self.ui_le_innerRadius, 5, 1, 1, 1)

        self.label_17 = QLabel(self.ui_gBox_coilGeom)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout.addWidget(self.label_17, 5, 2, 1, 1)

        self.ui_lbl_innerRadius = QLabel(self.ui_gBox_coilGeom)
        self.ui_lbl_innerRadius.setObjectName(u"ui_lbl_innerRadius")

        self.gridLayout.addWidget(self.ui_lbl_innerRadius, 5, 0, 1, 1)

        self.ui_spBox_nbreDiscs = QSpinBox(self.ui_gBox_coilGeom)
        self.ui_spBox_nbreDiscs.setObjectName(u"ui_spBox_nbreDiscs")

        self.gridLayout.addWidget(self.ui_spBox_nbreDiscs, 1, 1, 1, 1)

        self.label_5 = QLabel(self.ui_gBox_coilGeom)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.ui_gBox_coilGeom)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.ui_splitter_A.addWidget(self.layoutWidget)
        self.ui_splitter_B = QSplitter(self.ui_splitter_A)
        self.ui_splitter_B.setObjectName(u"ui_splitter_B")
        self.ui_splitter_B.setOrientation(Qt.Horizontal)
        self.ui_splitter_C = QSplitter(self.ui_splitter_B)
        self.ui_splitter_C.setObjectName(u"ui_splitter_C")
        self.ui_splitter_C.setOrientation(Qt.Vertical)
        self.ui_frame_viewAll = QFrame(self.ui_splitter_C)
        self.ui_frame_viewAll.setObjectName(u"ui_frame_viewAll")
        self.ui_frame_viewAll.setFrameShape(QFrame.StyledPanel)
        self.ui_frame_viewAll.setFrameShadow(QFrame.Raised)
        self.ui_splitter_C.addWidget(self.ui_frame_viewAll)
        self.ui_frame_legend = QFrame(self.ui_splitter_C)
        self.ui_frame_legend.setObjectName(u"ui_frame_legend")
        self.ui_frame_legend.setFrameShape(QFrame.StyledPanel)
        self.ui_frame_legend.setFrameShadow(QFrame.Raised)
        self.ui_splitter_C.addWidget(self.ui_frame_legend)
        self.ui_splitter_B.addWidget(self.ui_splitter_C)
        self.layoutWidget1 = QWidget(self.ui_splitter_B)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.verticalLayout_3 = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.layoutWidget1)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.label)

        self.ui_btn_symTB = QPushButton(self.layoutWidget1)
        self.ui_btn_symTB.setObjectName(u"ui_btn_symTB")

        self.horizontalLayout.addWidget(self.ui_btn_symTB)

        self.ui_btn_symBT = QPushButton(self.layoutWidget1)
        self.ui_btn_symBT.setObjectName(u"ui_btn_symBT")

        self.horizontalLayout.addWidget(self.ui_btn_symBT)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.ui_frame_viewZoom = QFrame(self.layoutWidget1)
        self.ui_frame_viewZoom.setObjectName(u"ui_frame_viewZoom")
        self.ui_frame_viewZoom.setFrameShape(QFrame.StyledPanel)
        self.ui_frame_viewZoom.setFrameShadow(QFrame.Raised)

        self.verticalLayout_3.addWidget(self.ui_frame_viewZoom)

        self.ui_splitter_B.addWidget(self.layoutWidget1)
        self.ui_splitter_A.addWidget(self.ui_splitter_B)

        self.verticalLayout_4.addWidget(self.ui_splitter_A)

        QWidget.setTabOrder(self.ui_chk_discs, self.ui_chk_ducts)
        QWidget.setTabOrder(self.ui_chk_ducts, self.ui_chk_pressboards)
        QWidget.setTabOrder(self.ui_chk_pressboards, self.ui_spBox_nbreDiscs)
        QWidget.setTabOrder(self.ui_spBox_nbreDiscs, self.ui_spBox_nbre_radSpacers)
        QWidget.setTabOrder(self.ui_spBox_nbre_radSpacers, self.ui_le_radSpacerWidth)
        QWidget.setTabOrder(self.ui_le_radSpacerWidth, self.ui_le_innerRadius)
        QWidget.setTabOrder(self.ui_le_innerRadius, self.ui_le_coilHeight)
        QWidget.setTabOrder(self.ui_le_coilHeight, self.ui_le_coilWidth)
        QWidget.setTabOrder(self.ui_le_coilWidth, self.ui_btn_symTB)
        QWidget.setTabOrder(self.ui_btn_symTB, self.ui_btn_symBT)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.ui_gBox_view.setTitle(QCoreApplication.translate("Form", u"View choices", None))
        self.ui_chk_discs.setText(QCoreApplication.translate("Form", u"Discs", None))
        self.ui_chk_ducts.setText(QCoreApplication.translate("Form", u"Oil ducts", None))
        self.ui_chk_pressboards.setText(QCoreApplication.translate("Form", u"Pressboards", None))
        self.ui_gBox_coilGeom.setTitle(QCoreApplication.translate("Form", u"Coil geometry", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"Radial spacers\n"
"width", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"Number of\n"
"radial spacers", None))
        self.label_13.setText(QCoreApplication.translate("Form", u"Coil height", None))
        self.label_15.setText(QCoreApplication.translate("Form", u"mm", None))
        self.label_14.setText(QCoreApplication.translate("Form", u"Coil width", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"mm", None))
        self.label_16.setText(QCoreApplication.translate("Form", u"mm", None))
        self.label_17.setText(QCoreApplication.translate("Form", u"mm", None))
        self.ui_lbl_innerRadius.setText(QCoreApplication.translate("Form", u"Inner radius", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Number of discs", None))
        self.label.setText(QCoreApplication.translate("Form", u"Ctrl + mouse wheel: zoom and geometry drag\n"
"Mouse click, Crtrl, Shift, Ctrl+A: items selection", None))
        self.ui_btn_symTB.setText(QCoreApplication.translate("Form", u"Symmetry top -> bottom", None))
        self.ui_btn_symBT.setText(QCoreApplication.translate("Form", u"Symmetry bottom -> top", None))
    # retranslateUi

