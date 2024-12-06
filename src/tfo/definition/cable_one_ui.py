# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cable_one.ui'
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
    QLineEdit, QPushButton, QRadioButton, QSizePolicy,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(896, 525)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.ui_lbl_cableDef = QLabel(Form)
        self.ui_lbl_cableDef.setObjectName(u"ui_lbl_cableDef")

        self.verticalLayout_2.addWidget(self.ui_lbl_cableDef)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_3)

        self.ui_le_name = QLineEdit(Form)
        self.ui_le_name.setObjectName(u"ui_le_name")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.ui_le_name)

        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_4)

        self.ui_cBox_type = QComboBox(Form)
        self.ui_cBox_type.setObjectName(u"ui_cBox_type")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.ui_cBox_type)


        self.horizontalLayout.addLayout(self.formLayout)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_10 = QLabel(Form)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 5, 3, 1, 1)

        self.ui_le_cableThick = QLineEdit(Form)
        self.ui_le_cableThick.setObjectName(u"ui_le_cableThick")
        self.ui_le_cableThick.setEnabled(False)

        self.gridLayout.addWidget(self.ui_le_cableThick, 5, 4, 1, 1)

        self.label_13 = QLabel(Form)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout.addWidget(self.label_13, 1, 2, 1, 1)

        self.label_7 = QLabel(Form)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 3, 0, 1, 1)

        self.label_20 = QLabel(Form)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout.addWidget(self.label_20, 0, 2, 1, 1)

        self.label_14 = QLabel(Form)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout.addWidget(self.label_14, 3, 2, 1, 1)

        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)

        self.label_6 = QLabel(Form)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 1, 0, 1, 1)

        self.ui_le_strandThick = QLineEdit(Form)
        self.ui_le_strandThick.setObjectName(u"ui_le_strandThick")

        self.gridLayout.addWidget(self.ui_le_strandThick, 3, 1, 1, 1)

        self.label_19 = QLabel(Form)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout.addWidget(self.label_19, 5, 5, 1, 1)

        self.ui_le_strandHeight = QLineEdit(Form)
        self.ui_le_strandHeight.setObjectName(u"ui_le_strandHeight")

        self.gridLayout.addWidget(self.ui_le_strandHeight, 1, 1, 1, 1)

        self.label_15 = QLabel(Form)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout.addWidget(self.label_15, 5, 2, 1, 1)

        self.label_16 = QLabel(Form)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout.addWidget(self.label_16, 4, 2, 1, 1)

        self.label_17 = QLabel(Form)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout.addWidget(self.label_17, 3, 5, 1, 1)

        self.ui_le_paperThick = QLineEdit(Form)
        self.ui_le_paperThick.setObjectName(u"ui_le_paperThick")

        self.gridLayout.addWidget(self.ui_le_paperThick, 4, 1, 1, 1)

        self.ui_le_pressboardThick = QLineEdit(Form)
        self.ui_le_pressboardThick.setObjectName(u"ui_le_pressboardThick")

        self.gridLayout.addWidget(self.ui_le_pressboardThick, 5, 1, 1, 1)

        self.ui_lbl_covering = QLabel(Form)
        self.ui_lbl_covering.setObjectName(u"ui_lbl_covering")

        self.gridLayout.addWidget(self.ui_lbl_covering, 4, 0, 1, 1)

        self.label_12 = QLabel(Form)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout.addWidget(self.label_12, 5, 0, 1, 1)

        self.label_9 = QLabel(Form)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 4, 3, 1, 1)

        self.label_8 = QLabel(Form)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 3, 3, 1, 1)

        self.ui_le_varnishThick = QLineEdit(Form)
        self.ui_le_varnishThick.setObjectName(u"ui_le_varnishThick")

        self.gridLayout.addWidget(self.ui_le_varnishThick, 3, 4, 1, 1)

        self.ui_le_cableHeight = QLineEdit(Form)
        self.ui_le_cableHeight.setObjectName(u"ui_le_cableHeight")
        self.ui_le_cableHeight.setEnabled(False)

        self.gridLayout.addWidget(self.ui_le_cableHeight, 4, 4, 1, 1)

        self.label_18 = QLabel(Form)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout.addWidget(self.label_18, 4, 5, 1, 1)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 3, 1, 1)

        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout_4 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.ui_rb_varnish = QRadioButton(self.groupBox)
        self.ui_rb_varnish.setObjectName(u"ui_rb_varnish")
        self.ui_rb_varnish.setChecked(True)

        self.horizontalLayout_4.addWidget(self.ui_rb_varnish)

        self.ui_rb_paper = QRadioButton(self.groupBox)
        self.ui_rb_paper.setObjectName(u"ui_rb_paper")

        self.horizontalLayout_4.addWidget(self.ui_rb_paper)


        self.gridLayout.addWidget(self.groupBox, 1, 4, 1, 1)

        self.ui_spBox_nbreStrands = QSpinBox(Form)
        self.ui_spBox_nbreStrands.setObjectName(u"ui_spBox_nbreStrands")

        self.gridLayout.addWidget(self.ui_spBox_nbreStrands, 0, 1, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)

        self.line_2 = QFrame(Form)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.ui_frame_cable = QFrame(Form)
        self.ui_frame_cable.setObjectName(u"ui_frame_cable")
        self.ui_frame_cable.setFrameShape(QFrame.StyledPanel)
        self.ui_frame_cable.setFrameShadow(QFrame.Raised)

        self.verticalLayout_4.addWidget(self.ui_frame_cable)

        self.ui_btn_rotateCable = QPushButton(Form)
        self.ui_btn_rotateCable.setObjectName(u"ui_btn_rotateCable")

        self.verticalLayout_4.addWidget(self.ui_btn_rotateCable)


        self.horizontalLayout_3.addLayout(self.verticalLayout_4)

        self.line_3 = QFrame(Form)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_3.addWidget(self.line_3)

        self.ui_lbl_cableScheme = QLabel(Form)
        self.ui_lbl_cableScheme.setObjectName(u"ui_lbl_cableScheme")

        self.horizontalLayout_3.addWidget(self.ui_lbl_cableScheme)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        QWidget.setTabOrder(self.ui_le_name, self.ui_cBox_type)
        QWidget.setTabOrder(self.ui_cBox_type, self.ui_spBox_nbreStrands)
        QWidget.setTabOrder(self.ui_spBox_nbreStrands, self.ui_le_strandHeight)
        QWidget.setTabOrder(self.ui_le_strandHeight, self.ui_le_strandThick)
        QWidget.setTabOrder(self.ui_le_strandThick, self.ui_le_paperThick)
        QWidget.setTabOrder(self.ui_le_paperThick, self.ui_le_pressboardThick)
        QWidget.setTabOrder(self.ui_le_pressboardThick, self.ui_rb_varnish)
        QWidget.setTabOrder(self.ui_rb_varnish, self.ui_rb_paper)
        QWidget.setTabOrder(self.ui_rb_paper, self.ui_le_varnishThick)
        QWidget.setTabOrder(self.ui_le_varnishThick, self.ui_le_cableHeight)
        QWidget.setTabOrder(self.ui_le_cableHeight, self.ui_le_cableThick)
        QWidget.setTabOrder(self.ui_le_cableThick, self.ui_btn_rotateCable)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.ui_lbl_cableDef.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">Cable definition</span></p></body></html>", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Name", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Type", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"Cable width (wc)", None))
        self.label_13.setText(QCoreApplication.translate("Form", u"mm", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"Strand width (ws)", None))
        self.label_20.setText("")
        self.label_14.setText(QCoreApplication.translate("Form", u"mm", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Number of strands", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"Strand length (ls)", None))
        self.ui_le_strandThick.setText(QCoreApplication.translate("Form", u"0.0", None))
        self.label_19.setText(QCoreApplication.translate("Form", u"mm", None))
        self.ui_le_strandHeight.setText(QCoreApplication.translate("Form", u"0.0", None))
        self.label_15.setText(QCoreApplication.translate("Form", u"mm", None))
        self.label_16.setText(QCoreApplication.translate("Form", u"mm", None))
        self.label_17.setText(QCoreApplication.translate("Form", u"mm", None))
        self.ui_le_paperThick.setText(QCoreApplication.translate("Form", u"0.0", None))
        self.ui_le_pressboardThick.setText(QCoreApplication.translate("Form", u"0.0", None))
        self.ui_lbl_covering.setText(QCoreApplication.translate("Form", u"Paper covering thickness (tc)", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"Internal pressboard thickness (tp)", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"Cable length (lc)", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"Strand insulation thickness (ti)", None))
        self.ui_le_varnishThick.setText(QCoreApplication.translate("Form", u"0.0", None))
        self.label_18.setText(QCoreApplication.translate("Form", u"mm", None))
        self.label.setText(QCoreApplication.translate("Form", u"Strand insulation type", None))
        self.groupBox.setTitle("")
        self.ui_rb_varnish.setText(QCoreApplication.translate("Form", u"Varnish", None))
        self.ui_rb_paper.setText(QCoreApplication.translate("Form", u"Paper", None))
        self.ui_btn_rotateCable.setText(QCoreApplication.translate("Form", u"Rotate cable view", None))
        self.ui_lbl_cableScheme.setText(QCoreApplication.translate("Form", u"Image avec d\u00e9finition des cotes", None))
    # retranslateUi

