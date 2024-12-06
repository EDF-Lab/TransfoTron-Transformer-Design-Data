# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'disc_one.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QLabel, QLineEdit, QSizePolicy, QSpacerItem,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(899, 352)
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.ui_lbl_discDef = QLabel(Form)
        self.ui_lbl_discDef.setObjectName(u"ui_lbl_discDef")

        self.verticalLayout.addWidget(self.ui_lbl_discDef)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)

        self.ui_le_name = QLineEdit(Form)
        self.ui_le_name.setObjectName(u"ui_le_name")

        self.gridLayout_3.addWidget(self.ui_le_name, 0, 1, 1, 1)

        self.label_7 = QLabel(Form)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_3.addWidget(self.label_7, 1, 0, 1, 1)

        self.ui_cBox_coil = QComboBox(Form)
        self.ui_cBox_coil.setObjectName(u"ui_cBox_coil")

        self.gridLayout_3.addWidget(self.ui_cBox_coil, 1, 1, 1, 1)

        self.label_6 = QLabel(Form)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_3.addWidget(self.label_6, 2, 0, 1, 1)

        self.ui_cBox_cable = QComboBox(Form)
        self.ui_cBox_cable.setObjectName(u"ui_cBox_cable")

        self.gridLayout_3.addWidget(self.ui_cBox_cable, 2, 1, 1, 1)

        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_3.addWidget(self.label_5, 3, 0, 1, 1)

        self.ui_spBox_cableDisc = QSpinBox(Form)
        self.ui_spBox_cableDisc.setObjectName(u"ui_spBox_cableDisc")

        self.gridLayout_3.addWidget(self.ui_spBox_cableDisc, 3, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_3)

        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.label_11 = QLabel(Form)
        self.label_11.setObjectName(u"label_11")

        self.verticalLayout.addWidget(self.label_11)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_9 = QLabel(Form)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_2.addWidget(self.label_9, 0, 0, 1, 1)

        self.ui_le_cableHeight = QLineEdit(Form)
        self.ui_le_cableHeight.setObjectName(u"ui_le_cableHeight")
        self.ui_le_cableHeight.setEnabled(False)

        self.gridLayout_2.addWidget(self.ui_le_cableHeight, 0, 1, 1, 1)

        self.label_18 = QLabel(Form)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout_2.addWidget(self.label_18, 0, 2, 1, 1)

        self.label_10 = QLabel(Form)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_2.addWidget(self.label_10, 1, 0, 1, 1)

        self.ui_le_cableThick = QLineEdit(Form)
        self.ui_le_cableThick.setObjectName(u"ui_le_cableThick")
        self.ui_le_cableThick.setEnabled(False)

        self.gridLayout_2.addWidget(self.ui_le_cableThick, 1, 1, 1, 1)

        self.label_19 = QLabel(Form)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_2.addWidget(self.label_19, 1, 2, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_2)

        self.line_2 = QFrame(Form)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_12 = QLabel(Form)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout.addWidget(self.label_12, 0, 0, 1, 1)

        self.ui_le_diskWidth = QLineEdit(Form)
        self.ui_le_diskWidth.setObjectName(u"ui_le_diskWidth")
        self.ui_le_diskWidth.setEnabled(False)

        self.gridLayout.addWidget(self.ui_le_diskWidth, 0, 1, 1, 1)

        self.label_20 = QLabel(Form)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout.addWidget(self.label_20, 0, 2, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.verticalSpacer = QSpacerItem(20, 82, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.ui_lbl_discDef.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">Disc definition</span></p></body></html>", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Name", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"Coil", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"Cable", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Number of cables per disc", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"Cable dimensions adaptation to have the same disc width for geometry building", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"Cable length (lc)", None))
        self.label_18.setText(QCoreApplication.translate("Form", u"mm", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"Cable width (wc)", None))
        self.label_19.setText(QCoreApplication.translate("Form", u"mm", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"Disc width", None))
        self.label_20.setText(QCoreApplication.translate("Form", u"mm", None))
    # retranslateUi

