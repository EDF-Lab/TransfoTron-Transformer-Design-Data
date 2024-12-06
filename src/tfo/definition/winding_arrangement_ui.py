# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'winding_arrangement.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QRadioButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(2338, 300)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.ui_grpBox_windDir = QGroupBox(Form)
        self.ui_grpBox_windDir.setObjectName(u"ui_grpBox_windDir")
        self.formLayout = QFormLayout(self.ui_grpBox_windDir)
        self.formLayout.setObjectName(u"formLayout")
        self.ui_rBut_posDir = QRadioButton(self.ui_grpBox_windDir)
        self.ui_rBut_posDir.setObjectName(u"ui_rBut_posDir")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.ui_rBut_posDir)

        self.ui_rBut_negDir = QRadioButton(self.ui_grpBox_windDir)
        self.ui_rBut_negDir.setObjectName(u"ui_rBut_negDir")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.ui_rBut_negDir)


        self.horizontalLayout.addWidget(self.ui_grpBox_windDir)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.ui_grpBox_core = QGroupBox(Form)
        self.ui_grpBox_core.setObjectName(u"ui_grpBox_core")
        self.gridLayout_6 = QGridLayout(self.ui_grpBox_core)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.ui_rBut_doubleClassic = QRadioButton(self.ui_grpBox_core)
        self.ui_rBut_doubleClassic.setObjectName(u"ui_rBut_doubleClassic")

        self.gridLayout_6.addWidget(self.ui_rBut_doubleClassic, 1, 1, 1, 1)

        self.ui_rBut_classic = QRadioButton(self.ui_grpBox_core)
        self.ui_rBut_classic.setObjectName(u"ui_rBut_classic")

        self.gridLayout_6.addWidget(self.ui_rBut_classic, 1, 0, 1, 1)

        self.ui_rBut_oneAxialSplit = QRadioButton(self.ui_grpBox_core)
        self.ui_rBut_oneAxialSplit.setObjectName(u"ui_rBut_oneAxialSplit")

        self.gridLayout_6.addWidget(self.ui_rBut_oneAxialSplit, 1, 4, 1, 1)

        self.ui_rBut_midEntry = QRadioButton(self.ui_grpBox_core)
        self.ui_rBut_midEntry.setObjectName(u"ui_rBut_midEntry")

        self.gridLayout_6.addWidget(self.ui_rBut_midEntry, 1, 3, 1, 1)

        self.ui_rBut_twoAxialSplit = QRadioButton(self.ui_grpBox_core)
        self.ui_rBut_twoAxialSplit.setObjectName(u"ui_rBut_twoAxialSplit")

        self.gridLayout_6.addWidget(self.ui_rBut_twoAxialSplit, 1, 5, 1, 1)

        self.ui_frame_classic = QFrame(self.ui_grpBox_core)
        self.ui_frame_classic.setObjectName(u"ui_frame_classic")
        self.ui_frame_classic.setFrameShape(QFrame.StyledPanel)
        self.ui_frame_classic.setFrameShadow(QFrame.Raised)

        self.gridLayout_6.addWidget(self.ui_frame_classic, 0, 0, 1, 1)

        self.ui_frame_midEntry = QFrame(self.ui_grpBox_core)
        self.ui_frame_midEntry.setObjectName(u"ui_frame_midEntry")
        self.ui_frame_midEntry.setFrameShape(QFrame.StyledPanel)
        self.ui_frame_midEntry.setFrameShadow(QFrame.Raised)

        self.gridLayout_6.addWidget(self.ui_frame_midEntry, 0, 3, 1, 1)

        self.ui_frame_oneAxialSplit = QFrame(self.ui_grpBox_core)
        self.ui_frame_oneAxialSplit.setObjectName(u"ui_frame_oneAxialSplit")
        self.ui_frame_oneAxialSplit.setFrameShape(QFrame.StyledPanel)
        self.ui_frame_oneAxialSplit.setFrameShadow(QFrame.Raised)

        self.gridLayout_6.addWidget(self.ui_frame_oneAxialSplit, 0, 4, 1, 1)

        self.ui_frame_twoAxialSplit = QFrame(self.ui_grpBox_core)
        self.ui_frame_twoAxialSplit.setObjectName(u"ui_frame_twoAxialSplit")
        self.ui_frame_twoAxialSplit.setFrameShape(QFrame.StyledPanel)
        self.ui_frame_twoAxialSplit.setFrameShadow(QFrame.Raised)

        self.gridLayout_6.addWidget(self.ui_frame_twoAxialSplit, 0, 5, 1, 1)

        self.ui_frame_doubleClassic = QFrame(self.ui_grpBox_core)
        self.ui_frame_doubleClassic.setObjectName(u"ui_frame_doubleClassic")
        self.ui_frame_doubleClassic.setFrameShape(QFrame.StyledPanel)
        self.ui_frame_doubleClassic.setFrameShadow(QFrame.Raised)

        self.gridLayout_6.addWidget(self.ui_frame_doubleClassic, 0, 1, 1, 1)

        self.ui_frame_fineCoarse = QFrame(self.ui_grpBox_core)
        self.ui_frame_fineCoarse.setObjectName(u"ui_frame_fineCoarse")
        self.ui_frame_fineCoarse.setFrameShape(QFrame.StyledPanel)
        self.ui_frame_fineCoarse.setFrameShadow(QFrame.Raised)

        self.gridLayout_6.addWidget(self.ui_frame_fineCoarse, 0, 2, 1, 1)

        self.ui_rBut_fineCoarse = QRadioButton(self.ui_grpBox_core)
        self.ui_rBut_fineCoarse.setObjectName(u"ui_rBut_fineCoarse")

        self.gridLayout_6.addWidget(self.ui_rBut_fineCoarse, 1, 2, 1, 1)


        self.horizontalLayout_2.addWidget(self.ui_grpBox_core)

        self.ui_grpBox_shell = QGroupBox(Form)
        self.ui_grpBox_shell.setObjectName(u"ui_grpBox_shell")
        self.gridLayout_7 = QGridLayout(self.ui_grpBox_shell)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.ui_rBut_shell_simple_barrel = QRadioButton(self.ui_grpBox_shell)
        self.ui_rBut_shell_simple_barrel.setObjectName(u"ui_rBut_shell_simple_barrel")

        self.gridLayout_7.addWidget(self.ui_rBut_shell_simple_barrel, 1, 2, 1, 1)

        self.ui_frame_shell_simple_diabolo = QFrame(self.ui_grpBox_shell)
        self.ui_frame_shell_simple_diabolo.setObjectName(u"ui_frame_shell_simple_diabolo")
        self.ui_frame_shell_simple_diabolo.setFrameShape(QFrame.StyledPanel)
        self.ui_frame_shell_simple_diabolo.setFrameShadow(QFrame.Raised)

        self.gridLayout_7.addWidget(self.ui_frame_shell_simple_diabolo, 0, 1, 1, 1)

        self.ui_frame_shell_double_classic = QFrame(self.ui_grpBox_shell)
        self.ui_frame_shell_double_classic.setObjectName(u"ui_frame_shell_double_classic")
        self.ui_frame_shell_double_classic.setFrameShape(QFrame.StyledPanel)
        self.ui_frame_shell_double_classic.setFrameShadow(QFrame.Raised)

        self.gridLayout_7.addWidget(self.ui_frame_shell_double_classic, 0, 3, 1, 1)

        self.ui_frame_shell_double_diabolo = QFrame(self.ui_grpBox_shell)
        self.ui_frame_shell_double_diabolo.setObjectName(u"ui_frame_shell_double_diabolo")
        self.ui_frame_shell_double_diabolo.setFrameShape(QFrame.StyledPanel)
        self.ui_frame_shell_double_diabolo.setFrameShadow(QFrame.Raised)

        self.gridLayout_7.addWidget(self.ui_frame_shell_double_diabolo, 0, 4, 1, 1)

        self.ui_frame_shell_simple_classic = QFrame(self.ui_grpBox_shell)
        self.ui_frame_shell_simple_classic.setObjectName(u"ui_frame_shell_simple_classic")
        self.ui_frame_shell_simple_classic.setFrameShape(QFrame.StyledPanel)
        self.ui_frame_shell_simple_classic.setFrameShadow(QFrame.Raised)

        self.gridLayout_7.addWidget(self.ui_frame_shell_simple_classic, 0, 0, 1, 1)

        self.ui_frame_shell_triple_classic = QFrame(self.ui_grpBox_shell)
        self.ui_frame_shell_triple_classic.setObjectName(u"ui_frame_shell_triple_classic")
        self.ui_frame_shell_triple_classic.setFrameShape(QFrame.StyledPanel)
        self.ui_frame_shell_triple_classic.setFrameShadow(QFrame.Raised)

        self.gridLayout_7.addWidget(self.ui_frame_shell_triple_classic, 0, 6, 1, 1)

        self.ui_rBut_shell_double_diabolo = QRadioButton(self.ui_grpBox_shell)
        self.ui_rBut_shell_double_diabolo.setObjectName(u"ui_rBut_shell_double_diabolo")

        self.gridLayout_7.addWidget(self.ui_rBut_shell_double_diabolo, 1, 4, 1, 1)

        self.ui_rBut_shell_simple_classic = QRadioButton(self.ui_grpBox_shell)
        self.ui_rBut_shell_simple_classic.setObjectName(u"ui_rBut_shell_simple_classic")

        self.gridLayout_7.addWidget(self.ui_rBut_shell_simple_classic, 1, 0, 1, 1)

        self.ui_rBut_shell_triple_classic = QRadioButton(self.ui_grpBox_shell)
        self.ui_rBut_shell_triple_classic.setObjectName(u"ui_rBut_shell_triple_classic")

        self.gridLayout_7.addWidget(self.ui_rBut_shell_triple_classic, 1, 6, 1, 1)

        self.ui_rBut_shell_double_classic = QRadioButton(self.ui_grpBox_shell)
        self.ui_rBut_shell_double_classic.setObjectName(u"ui_rBut_shell_double_classic")

        self.gridLayout_7.addWidget(self.ui_rBut_shell_double_classic, 1, 3, 1, 1)

        self.ui_rBut_shell_simple_diabolo = QRadioButton(self.ui_grpBox_shell)
        self.ui_rBut_shell_simple_diabolo.setObjectName(u"ui_rBut_shell_simple_diabolo")

        self.gridLayout_7.addWidget(self.ui_rBut_shell_simple_diabolo, 1, 1, 1, 1)

        self.ui_frame_shell_simple_barrel = QFrame(self.ui_grpBox_shell)
        self.ui_frame_shell_simple_barrel.setObjectName(u"ui_frame_shell_simple_barrel")
        self.ui_frame_shell_simple_barrel.setFrameShape(QFrame.StyledPanel)
        self.ui_frame_shell_simple_barrel.setFrameShadow(QFrame.Raised)

        self.gridLayout_7.addWidget(self.ui_frame_shell_simple_barrel, 0, 2, 1, 1)

        self.ui_frame_shell_double_barrel = QFrame(self.ui_grpBox_shell)
        self.ui_frame_shell_double_barrel.setObjectName(u"ui_frame_shell_double_barrel")
        self.ui_frame_shell_double_barrel.setFrameShape(QFrame.StyledPanel)
        self.ui_frame_shell_double_barrel.setFrameShadow(QFrame.Raised)

        self.gridLayout_7.addWidget(self.ui_frame_shell_double_barrel, 0, 5, 1, 1)

        self.ui_rBut_shell_double_barrel = QRadioButton(self.ui_grpBox_shell)
        self.ui_rBut_shell_double_barrel.setObjectName(u"ui_rBut_shell_double_barrel")

        self.gridLayout_7.addWidget(self.ui_rBut_shell_double_barrel, 1, 5, 1, 1)


        self.horizontalLayout_2.addWidget(self.ui_grpBox_shell)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 147, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        QWidget.setTabOrder(self.ui_rBut_posDir, self.ui_rBut_negDir)
        QWidget.setTabOrder(self.ui_rBut_negDir, self.ui_rBut_classic)
        QWidget.setTabOrder(self.ui_rBut_classic, self.ui_rBut_doubleClassic)
        QWidget.setTabOrder(self.ui_rBut_doubleClassic, self.ui_rBut_fineCoarse)
        QWidget.setTabOrder(self.ui_rBut_fineCoarse, self.ui_rBut_midEntry)
        QWidget.setTabOrder(self.ui_rBut_midEntry, self.ui_rBut_oneAxialSplit)
        QWidget.setTabOrder(self.ui_rBut_oneAxialSplit, self.ui_rBut_twoAxialSplit)
        QWidget.setTabOrder(self.ui_rBut_twoAxialSplit, self.ui_rBut_shell_simple_classic)
        QWidget.setTabOrder(self.ui_rBut_shell_simple_classic, self.ui_rBut_shell_simple_diabolo)
        QWidget.setTabOrder(self.ui_rBut_shell_simple_diabolo, self.ui_rBut_shell_simple_barrel)
        QWidget.setTabOrder(self.ui_rBut_shell_simple_barrel, self.ui_rBut_shell_double_classic)
        QWidget.setTabOrder(self.ui_rBut_shell_double_classic, self.ui_rBut_shell_double_diabolo)
        QWidget.setTabOrder(self.ui_rBut_shell_double_diabolo, self.ui_rBut_shell_double_barrel)
        QWidget.setTabOrder(self.ui_rBut_shell_double_barrel, self.ui_rBut_shell_triple_classic)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.ui_grpBox_windDir.setTitle(QCoreApplication.translate("Form", u"Direction", None))
        self.ui_rBut_posDir.setText(QCoreApplication.translate("Form", u"Positive", None))
        self.ui_rBut_negDir.setText(QCoreApplication.translate("Form", u"Negative", None))
        self.ui_grpBox_core.setTitle("")
        self.ui_rBut_doubleClassic.setText(QCoreApplication.translate("Form", u"Double classic", None))
        self.ui_rBut_classic.setText(QCoreApplication.translate("Form", u"Classic", None))
        self.ui_rBut_oneAxialSplit.setText(QCoreApplication.translate("Form", u"One winding\n"
"axial split", None))
        self.ui_rBut_midEntry.setText(QCoreApplication.translate("Form", u"Middle entry", None))
        self.ui_rBut_twoAxialSplit.setText(QCoreApplication.translate("Form", u"Two windings\n"
"axial split", None))
        self.ui_rBut_fineCoarse.setText(QCoreApplication.translate("Form", u"Fine coarse", None))
        self.ui_grpBox_shell.setTitle("")
        self.ui_rBut_shell_simple_barrel.setText(QCoreApplication.translate("Form", u"Two windings barrel (4 HL)", None))
        self.ui_rBut_shell_double_diabolo.setText(QCoreApplication.translate("Form", u"Three windings diabolo (4 HL)", None))
        self.ui_rBut_shell_simple_classic.setText(QCoreApplication.translate("Form", u"Two windings classic (2 HL)", None))
        self.ui_rBut_shell_triple_classic.setText(QCoreApplication.translate("Form", u"Four windings classic (4 HL)", None))
        self.ui_rBut_shell_double_classic.setText(QCoreApplication.translate("Form", u"Three windings classic (4 HL)", None))
        self.ui_rBut_shell_simple_diabolo.setText(QCoreApplication.translate("Form", u"Two windings diabolo (2 HL)", None))
        self.ui_rBut_shell_double_barrel.setText(QCoreApplication.translate("Form", u"Three windings barrel (4 HL)", None))
    # retranslateUi

