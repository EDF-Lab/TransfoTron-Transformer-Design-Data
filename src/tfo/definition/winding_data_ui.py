# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'winding_data.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QRadioButton, QSizePolicy, QSpacerItem, QSpinBox,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1105, 693)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.verticalLayout_3 = QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.ui_grpBox_main = QGroupBox(Form)
        self.ui_grpBox_main.setObjectName(u"ui_grpBox_main")
        sizePolicy.setHeightForWidth(self.ui_grpBox_main.sizePolicy().hasHeightForWidth())
        self.ui_grpBox_main.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.ui_grpBox_main)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_4 = QLabel(self.ui_grpBox_main)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 5, 0, 1, 1)

        self.label_25 = QLabel(self.ui_grpBox_main)
        self.label_25.setObjectName(u"label_25")

        self.gridLayout.addWidget(self.label_25, 2, 2, 1, 1)

        self.ui_le_voltage = QLineEdit(self.ui_grpBox_main)
        self.ui_le_voltage.setObjectName(u"ui_le_voltage")

        self.gridLayout.addWidget(self.ui_le_voltage, 2, 1, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.ui_cBox_highest_voltage = QComboBox(self.ui_grpBox_main)
        self.ui_cBox_highest_voltage.setObjectName(u"ui_cBox_highest_voltage")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.ui_cBox_highest_voltage.sizePolicy().hasHeightForWidth())
        self.ui_cBox_highest_voltage.setSizePolicy(sizePolicy1)
        self.ui_cBox_highest_voltage.setMinimumSize(QSize(100, 0))
        self.ui_cBox_highest_voltage.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout_2.addWidget(self.ui_cBox_highest_voltage)

        self.ui_le_highest_voltage = QLineEdit(self.ui_grpBox_main)
        self.ui_le_highest_voltage.setObjectName(u"ui_le_highest_voltage")

        self.horizontalLayout_2.addWidget(self.ui_le_highest_voltage)


        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 1, 1, 1)

        self.label_24 = QLabel(self.ui_grpBox_main)
        self.label_24.setObjectName(u"label_24")

        self.gridLayout.addWidget(self.label_24, 2, 0, 1, 1)

        self.ui_le_power = QLineEdit(self.ui_grpBox_main)
        self.ui_le_power.setObjectName(u"ui_le_power")

        self.gridLayout.addWidget(self.ui_le_power, 1, 1, 1, 1)

        self.ui_lbl_unit_n = QLabel(self.ui_grpBox_main)
        self.ui_lbl_unit_n.setObjectName(u"ui_lbl_unit_n")

        self.gridLayout.addWidget(self.ui_lbl_unit_n, 4, 2, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.ui_cBox_highest_voltage_neutral = QComboBox(self.ui_grpBox_main)
        self.ui_cBox_highest_voltage_neutral.setObjectName(u"ui_cBox_highest_voltage_neutral")
        sizePolicy1.setHeightForWidth(self.ui_cBox_highest_voltage_neutral.sizePolicy().hasHeightForWidth())
        self.ui_cBox_highest_voltage_neutral.setSizePolicy(sizePolicy1)
        self.ui_cBox_highest_voltage_neutral.setMinimumSize(QSize(100, 0))
        self.ui_cBox_highest_voltage_neutral.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout_3.addWidget(self.ui_cBox_highest_voltage_neutral)

        self.ui_le_highest_voltage_neutral = QLineEdit(self.ui_grpBox_main)
        self.ui_le_highest_voltage_neutral.setObjectName(u"ui_le_highest_voltage_neutral")

        self.horizontalLayout_3.addWidget(self.ui_le_highest_voltage_neutral)


        self.gridLayout.addLayout(self.horizontalLayout_3, 4, 1, 1, 1)

        self.label_26 = QLabel(self.ui_grpBox_main)
        self.label_26.setObjectName(u"label_26")

        self.gridLayout.addWidget(self.label_26, 0, 0, 1, 1)

        self.label_27 = QLabel(self.ui_grpBox_main)
        self.label_27.setObjectName(u"label_27")

        self.gridLayout.addWidget(self.label_27, 3, 0, 1, 1)

        self.label_22 = QLabel(self.ui_grpBox_main)
        self.label_22.setObjectName(u"label_22")

        self.gridLayout.addWidget(self.label_22, 1, 0, 1, 1)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.ui_cBox_ydi = QComboBox(self.ui_grpBox_main)
        self.ui_cBox_ydi.setObjectName(u"ui_cBox_ydi")
        self.ui_cBox_ydi.setMinimumSize(QSize(80, 0))
        self.ui_cBox_ydi.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout_7.addWidget(self.ui_cBox_ydi)

        self.ui_cBox_n = QComboBox(self.ui_grpBox_main)
        self.ui_cBox_n.setObjectName(u"ui_cBox_n")
        self.ui_cBox_n.setMinimumSize(QSize(80, 0))
        self.ui_cBox_n.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout_7.addWidget(self.ui_cBox_n)

        self.ui_spBox_phase = QSpinBox(self.ui_grpBox_main)
        self.ui_spBox_phase.setObjectName(u"ui_spBox_phase")
        self.ui_spBox_phase.setMinimumSize(QSize(50, 0))
        self.ui_spBox_phase.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_7.addWidget(self.ui_spBox_phase)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer)


        self.gridLayout.addLayout(self.horizontalLayout_7, 5, 1, 1, 1)

        self.ui_le_name = QLineEdit(self.ui_grpBox_main)
        self.ui_le_name.setObjectName(u"ui_le_name")

        self.gridLayout.addWidget(self.ui_le_name, 0, 1, 1, 1)

        self.ui_lbl_Um_n = QLabel(self.ui_grpBox_main)
        self.ui_lbl_Um_n.setObjectName(u"ui_lbl_Um_n")

        self.gridLayout.addWidget(self.ui_lbl_Um_n, 4, 0, 1, 1)

        self.label_28 = QLabel(self.ui_grpBox_main)
        self.label_28.setObjectName(u"label_28")

        self.gridLayout.addWidget(self.label_28, 3, 2, 1, 1)

        self.label_23 = QLabel(self.ui_grpBox_main)
        self.label_23.setObjectName(u"label_23")

        self.gridLayout.addWidget(self.label_23, 1, 2, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)


        self.horizontalLayout_5.addWidget(self.ui_grpBox_main)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.ui_grpBox_regWind = QGroupBox(Form)
        self.ui_grpBox_regWind.setObjectName(u"ui_grpBox_regWind")
        self.ui_grpBox_regWind.setCheckable(True)
        self.horizontalLayout = QHBoxLayout(self.ui_grpBox_regWind)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.groupBox = QGroupBox(self.ui_grpBox_regWind)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy2)
        self.formLayout_2 = QFormLayout(self.groupBox)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.ui_rbut_standard = QRadioButton(self.groupBox)
        self.ui_rbut_standard.setObjectName(u"ui_rbut_standard")
        self.ui_rbut_standard.setChecked(True)

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.ui_rbut_standard)

        self.ui_rbut_userDefined = QRadioButton(self.groupBox)
        self.ui_rbut_userDefined.setObjectName(u"ui_rbut_userDefined")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.ui_rbut_userDefined)

        self.ui_lbl_fill = QLabel(self.groupBox)
        self.ui_lbl_fill.setObjectName(u"ui_lbl_fill")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.ui_lbl_fill)


        self.horizontalLayout.addWidget(self.groupBox)

        self.ui_gBox_user = QGroupBox(self.ui_grpBox_regWind)
        self.ui_gBox_user.setObjectName(u"ui_gBox_user")
        sizePolicy2.setHeightForWidth(self.ui_gBox_user.sizePolicy().hasHeightForWidth())
        self.ui_gBox_user.setSizePolicy(sizePolicy2)
        self.formLayout = QFormLayout(self.ui_gBox_user)
        self.formLayout.setObjectName(u"formLayout")
        self.ui_lbl_nbreTaps = QLabel(self.ui_gBox_user)
        self.ui_lbl_nbreTaps.setObjectName(u"ui_lbl_nbreTaps")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.ui_lbl_nbreTaps)

        self.ui_spBox_nbreTaps = QSpinBox(self.ui_gBox_user)
        self.ui_spBox_nbreTaps.setObjectName(u"ui_spBox_nbreTaps")
        self.ui_spBox_nbreTaps.setMinimumSize(QSize(80, 0))
        self.ui_spBox_nbreTaps.setMaximumSize(QSize(80, 16777215))

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.ui_spBox_nbreTaps)

        self.ui_lbl_ratedTap = QLabel(self.ui_gBox_user)
        self.ui_lbl_ratedTap.setObjectName(u"ui_lbl_ratedTap")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.ui_lbl_ratedTap)

        self.ui_cBox_ratedTap = QComboBox(self.ui_gBox_user)
        self.ui_cBox_ratedTap.setObjectName(u"ui_cBox_ratedTap")
        self.ui_cBox_ratedTap.setMinimumSize(QSize(80, 0))
        self.ui_cBox_ratedTap.setMaximumSize(QSize(80, 16777215))

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.ui_cBox_ratedTap)


        self.horizontalLayout.addWidget(self.ui_gBox_user)

        self.ui_gBox_fixed = QGroupBox(self.ui_grpBox_regWind)
        self.ui_gBox_fixed.setObjectName(u"ui_gBox_fixed")
        sizePolicy2.setHeightForWidth(self.ui_gBox_fixed.sizePolicy().hasHeightForWidth())
        self.ui_gBox_fixed.setSizePolicy(sizePolicy2)
        self.formLayout_3 = QFormLayout(self.ui_gBox_fixed)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.ui_lbl_regStep_sym1_2 = QLabel(self.ui_gBox_fixed)
        self.ui_lbl_regStep_sym1_2.setObjectName(u"ui_lbl_regStep_sym1_2")
        self.ui_lbl_regStep_sym1_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.ui_lbl_regStep_sym1_2)

        self.ui_spBox_nbreTaps_p = QSpinBox(self.ui_gBox_fixed)
        self.ui_spBox_nbreTaps_p.setObjectName(u"ui_spBox_nbreTaps_p")
        self.ui_spBox_nbreTaps_p.setMinimumSize(QSize(50, 0))
        self.ui_spBox_nbreTaps_p.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_4.addWidget(self.ui_spBox_nbreTaps_p)

        self.ui_lbl_regStep_sym2_2 = QLabel(self.ui_gBox_fixed)
        self.ui_lbl_regStep_sym2_2.setObjectName(u"ui_lbl_regStep_sym2_2")
        self.ui_lbl_regStep_sym2_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.ui_lbl_regStep_sym2_2)

        self.ui_le_regStep_p = QLineEdit(self.ui_gBox_fixed)
        self.ui_le_regStep_p.setObjectName(u"ui_le_regStep_p")
        self.ui_le_regStep_p.setMinimumSize(QSize(40, 0))
        self.ui_le_regStep_p.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_4.addWidget(self.ui_le_regStep_p)

        self.ui_lbl_regStep_sym3_2 = QLabel(self.ui_gBox_fixed)
        self.ui_lbl_regStep_sym3_2.setObjectName(u"ui_lbl_regStep_sym3_2")

        self.horizontalLayout_4.addWidget(self.ui_lbl_regStep_sym3_2)


        self.formLayout_3.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_4)

        self.ui_lbl_ratedVoltage = QLabel(self.ui_gBox_fixed)
        self.ui_lbl_ratedVoltage.setObjectName(u"ui_lbl_ratedVoltage")
        self.ui_lbl_ratedVoltage.setAlignment(Qt.AlignRight|Qt.AlignTop|Qt.AlignTrailing)

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.ui_lbl_ratedVoltage)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.ui_lbl_regStep_sym4_2 = QLabel(self.ui_gBox_fixed)
        self.ui_lbl_regStep_sym4_2.setObjectName(u"ui_lbl_regStep_sym4_2")
        self.ui_lbl_regStep_sym4_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_6.addWidget(self.ui_lbl_regStep_sym4_2)

        self.ui_spBox_nbreTaps_m = QSpinBox(self.ui_gBox_fixed)
        self.ui_spBox_nbreTaps_m.setObjectName(u"ui_spBox_nbreTaps_m")
        self.ui_spBox_nbreTaps_m.setMinimumSize(QSize(50, 0))
        self.ui_spBox_nbreTaps_m.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_6.addWidget(self.ui_spBox_nbreTaps_m)

        self.ui_lbl_regStep_sym5_2 = QLabel(self.ui_gBox_fixed)
        self.ui_lbl_regStep_sym5_2.setObjectName(u"ui_lbl_regStep_sym5_2")
        self.ui_lbl_regStep_sym5_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_6.addWidget(self.ui_lbl_regStep_sym5_2)

        self.ui_le_regStep_m = QLineEdit(self.ui_gBox_fixed)
        self.ui_le_regStep_m.setObjectName(u"ui_le_regStep_m")
        self.ui_le_regStep_m.setMinimumSize(QSize(40, 0))
        self.ui_le_regStep_m.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_6.addWidget(self.ui_le_regStep_m)

        self.ui_lbl_regStep_sym6_2 = QLabel(self.ui_gBox_fixed)
        self.ui_lbl_regStep_sym6_2.setObjectName(u"ui_lbl_regStep_sym6_2")

        self.horizontalLayout_6.addWidget(self.ui_lbl_regStep_sym6_2)


        self.formLayout_3.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout_6)


        self.horizontalLayout.addWidget(self.ui_gBox_fixed)


        self.verticalLayout_2.addWidget(self.ui_grpBox_regWind)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.horizontalLayout_5.addLayout(self.verticalLayout_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.ui_widget_table = QWidget(Form)
        self.ui_widget_table.setObjectName(u"ui_widget_table")
        sizePolicy.setHeightForWidth(self.ui_widget_table.sizePolicy().hasHeightForWidth())
        self.ui_widget_table.setSizePolicy(sizePolicy)

        self.verticalLayout_3.addWidget(self.ui_widget_table)

        QWidget.setTabOrder(self.ui_le_name, self.ui_le_power)
        QWidget.setTabOrder(self.ui_le_power, self.ui_le_voltage)
        QWidget.setTabOrder(self.ui_le_voltage, self.ui_cBox_highest_voltage)
        QWidget.setTabOrder(self.ui_cBox_highest_voltage, self.ui_le_highest_voltage)
        QWidget.setTabOrder(self.ui_le_highest_voltage, self.ui_cBox_highest_voltage_neutral)
        QWidget.setTabOrder(self.ui_cBox_highest_voltage_neutral, self.ui_le_highest_voltage_neutral)
        QWidget.setTabOrder(self.ui_le_highest_voltage_neutral, self.ui_cBox_ydi)
        QWidget.setTabOrder(self.ui_cBox_ydi, self.ui_cBox_n)
        QWidget.setTabOrder(self.ui_cBox_n, self.ui_spBox_phase)
        QWidget.setTabOrder(self.ui_spBox_phase, self.ui_grpBox_regWind)
        QWidget.setTabOrder(self.ui_grpBox_regWind, self.ui_rbut_standard)
        QWidget.setTabOrder(self.ui_rbut_standard, self.ui_rbut_userDefined)
        QWidget.setTabOrder(self.ui_rbut_userDefined, self.ui_spBox_nbreTaps)
        QWidget.setTabOrder(self.ui_spBox_nbreTaps, self.ui_cBox_ratedTap)
        QWidget.setTabOrder(self.ui_cBox_ratedTap, self.ui_spBox_nbreTaps_p)
        QWidget.setTabOrder(self.ui_spBox_nbreTaps_p, self.ui_le_regStep_p)
        QWidget.setTabOrder(self.ui_le_regStep_p, self.ui_spBox_nbreTaps_m)
        QWidget.setTabOrder(self.ui_spBox_nbreTaps_m, self.ui_le_regStep_m)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.ui_grpBox_main.setTitle(QCoreApplication.translate("Form", u"Main data", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Vector group", None))
        self.label_25.setText(QCoreApplication.translate("Form", u"kV", None))
        self.label_24.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>Line-line<br>voltage (U<span style=\" vertical-align:sub;\">r</span>)</p></body></html>", None))
        self.ui_lbl_unit_n.setText(QCoreApplication.translate("Form", u"kV", None))
        self.label_26.setText(QCoreApplication.translate("Form", u"Name", None))
        self.label_27.setText(QCoreApplication.translate("Form", u"<html><head/><body>Highest voltage<br>applicable (U<span style=\" vertical-align:sub;\">m</span>)</body></html>", None))
        self.label_22.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>Power (S<span style=\" vertical-align:sub;\">r</span>)</p></body></html>", None))
        self.ui_lbl_Um_n.setText(QCoreApplication.translate("Form", u"<html><head/><body>Highest voltage<br/>applicable for<br/>neutral (U<span style=\" vertical-align:sub;\">m n</span>)</body></html>", None))
        self.label_28.setText(QCoreApplication.translate("Form", u"kV", None))
        self.label_23.setText(QCoreApplication.translate("Form", u"MVA", None))
        self.ui_grpBox_regWind.setTitle(QCoreApplication.translate("Form", u"Regulating winding", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Filling method", None))
        self.ui_rbut_standard.setText(QCoreApplication.translate("Form", u"Standard", None))
        self.ui_rbut_userDefined.setText(QCoreApplication.translate("Form", u"User defined", None))
        self.ui_lbl_fill.setText(QCoreApplication.translate("Form", u"Tap, LL voltage and power\n"
"columns are editable", None))
        self.ui_gBox_user.setTitle(QCoreApplication.translate("Form", u"Taps definition", None))
        self.ui_lbl_nbreTaps.setText(QCoreApplication.translate("Form", u"Number of taps", None))
        self.ui_lbl_ratedTap.setText(QCoreApplication.translate("Form", u"Rated tap", None))
        self.ui_gBox_fixed.setTitle(QCoreApplication.translate("Form", u"Taps definition", None))
        self.ui_lbl_regStep_sym1_2.setText(QCoreApplication.translate("Form", u"+", None))
        self.ui_lbl_regStep_sym2_2.setText(QCoreApplication.translate("Form", u"x", None))
        self.ui_lbl_regStep_sym3_2.setText(QCoreApplication.translate("Form", u"%", None))
        self.ui_lbl_ratedVoltage.setText(QCoreApplication.translate("Form", u"rated kV", None))
        self.ui_lbl_regStep_sym4_2.setText(QCoreApplication.translate("Form", u"-", None))
        self.ui_lbl_regStep_sym5_2.setText(QCoreApplication.translate("Form", u"x", None))
        self.ui_lbl_regStep_sym6_2.setText(QCoreApplication.translate("Form", u"%", None))
    # retranslateUi

