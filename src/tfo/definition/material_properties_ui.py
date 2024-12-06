# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'material_properties.ui'
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
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(658, 357)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.ui_lbl_title = QLabel(Form)
        self.ui_lbl_title.setObjectName(u"ui_lbl_title")

        self.verticalLayout.addWidget(self.ui_lbl_title)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.ui_form_prop = QFormLayout()
        self.ui_form_prop.setObjectName(u"ui_form_prop")
        self.ui_lbl_reference = QLabel(Form)
        self.ui_lbl_reference.setObjectName(u"ui_lbl_reference")

        self.ui_form_prop.setWidget(0, QFormLayout.LabelRole, self.ui_lbl_reference)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.ui_cBox_ref = QComboBox(Form)
        self.ui_cBox_ref.setObjectName(u"ui_cBox_ref")
        self.ui_cBox_ref.setMinimumSize(QSize(150, 0))

        self.horizontalLayout.addWidget(self.ui_cBox_ref)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_6)

        self.ui_btn_clear_plot = QPushButton(Form)
        self.ui_btn_clear_plot.setObjectName(u"ui_btn_clear_plot")

        self.horizontalLayout.addWidget(self.ui_btn_clear_plot)


        self.ui_form_prop.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout)

        self.ui_lbl_density = QLabel(Form)
        self.ui_lbl_density.setObjectName(u"ui_lbl_density")

        self.ui_form_prop.setWidget(1, QFormLayout.LabelRole, self.ui_lbl_density)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.ui_lbl_rho1 = QLabel(Form)
        self.ui_lbl_rho1.setObjectName(u"ui_lbl_rho1")

        self.horizontalLayout_2.addWidget(self.ui_lbl_rho1)

        self.ui_le_rhoA = QLineEdit(Form)
        self.ui_le_rhoA.setObjectName(u"ui_le_rhoA")

        self.horizontalLayout_2.addWidget(self.ui_le_rhoA)

        self.ui_lbl_rho2 = QLabel(Form)
        self.ui_lbl_rho2.setObjectName(u"ui_lbl_rho2")

        self.horizontalLayout_2.addWidget(self.ui_lbl_rho2)

        self.ui_le_rhoB = QLineEdit(Form)
        self.ui_le_rhoB.setObjectName(u"ui_le_rhoB")

        self.horizontalLayout_2.addWidget(self.ui_le_rhoB)

        self.ui_lbl_rho3 = QLabel(Form)
        self.ui_lbl_rho3.setObjectName(u"ui_lbl_rho3")

        self.horizontalLayout_2.addWidget(self.ui_lbl_rho3)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.ui_btn_plot_d = QPushButton(Form)
        self.ui_btn_plot_d.setObjectName(u"ui_btn_plot_d")

        self.horizontalLayout_2.addWidget(self.ui_btn_plot_d)


        self.ui_form_prop.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_2)

        self.ui_lbl_specHeat = QLabel(Form)
        self.ui_lbl_specHeat.setObjectName(u"ui_lbl_specHeat")

        self.ui_form_prop.setWidget(2, QFormLayout.LabelRole, self.ui_lbl_specHeat)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.ui_lbl_cp1 = QLabel(Form)
        self.ui_lbl_cp1.setObjectName(u"ui_lbl_cp1")

        self.horizontalLayout_3.addWidget(self.ui_lbl_cp1)

        self.ui_le_cpA = QLineEdit(Form)
        self.ui_le_cpA.setObjectName(u"ui_le_cpA")

        self.horizontalLayout_3.addWidget(self.ui_le_cpA)

        self.ui_lbl_cp2 = QLabel(Form)
        self.ui_lbl_cp2.setObjectName(u"ui_lbl_cp2")

        self.horizontalLayout_3.addWidget(self.ui_lbl_cp2)

        self.ui_le_cpB = QLineEdit(Form)
        self.ui_le_cpB.setObjectName(u"ui_le_cpB")

        self.horizontalLayout_3.addWidget(self.ui_le_cpB)

        self.ui_lbl_cp3 = QLabel(Form)
        self.ui_lbl_cp3.setObjectName(u"ui_lbl_cp3")

        self.horizontalLayout_3.addWidget(self.ui_lbl_cp3)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.ui_btn_plot_sh = QPushButton(Form)
        self.ui_btn_plot_sh.setObjectName(u"ui_btn_plot_sh")

        self.horizontalLayout_3.addWidget(self.ui_btn_plot_sh)


        self.ui_form_prop.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout_3)

        self.ui_lbl_thermCond = QLabel(Form)
        self.ui_lbl_thermCond.setObjectName(u"ui_lbl_thermCond")

        self.ui_form_prop.setWidget(3, QFormLayout.LabelRole, self.ui_lbl_thermCond)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.ui_lbl_k1 = QLabel(Form)
        self.ui_lbl_k1.setObjectName(u"ui_lbl_k1")

        self.horizontalLayout_4.addWidget(self.ui_lbl_k1)

        self.ui_le_kA = QLineEdit(Form)
        self.ui_le_kA.setObjectName(u"ui_le_kA")

        self.horizontalLayout_4.addWidget(self.ui_le_kA)

        self.ui_lbl_k2 = QLabel(Form)
        self.ui_lbl_k2.setObjectName(u"ui_lbl_k2")

        self.horizontalLayout_4.addWidget(self.ui_lbl_k2)

        self.ui_le_kB = QLineEdit(Form)
        self.ui_le_kB.setObjectName(u"ui_le_kB")

        self.horizontalLayout_4.addWidget(self.ui_le_kB)

        self.ui_lbl_k3 = QLabel(Form)
        self.ui_lbl_k3.setObjectName(u"ui_lbl_k3")

        self.horizontalLayout_4.addWidget(self.ui_lbl_k3)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.ui_btn_plot_tc = QPushButton(Form)
        self.ui_btn_plot_tc.setObjectName(u"ui_btn_plot_tc")

        self.horizontalLayout_4.addWidget(self.ui_btn_plot_tc)


        self.ui_form_prop.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout_4)

        self.ui_lbl_dynaVisco = QLabel(Form)
        self.ui_lbl_dynaVisco.setObjectName(u"ui_lbl_dynaVisco")

        self.ui_form_prop.setWidget(4, QFormLayout.LabelRole, self.ui_lbl_dynaVisco)

        self.ui_layout_visco = QHBoxLayout()
        self.ui_layout_visco.setObjectName(u"ui_layout_visco")
        self.ui_lbl_mu1 = QLabel(Form)
        self.ui_lbl_mu1.setObjectName(u"ui_lbl_mu1")

        self.ui_layout_visco.addWidget(self.ui_lbl_mu1)

        self.ui_le_muA = QLineEdit(Form)
        self.ui_le_muA.setObjectName(u"ui_le_muA")

        self.ui_layout_visco.addWidget(self.ui_le_muA)

        self.ui_lbl_mu2 = QLabel(Form)
        self.ui_lbl_mu2.setObjectName(u"ui_lbl_mu2")

        self.ui_layout_visco.addWidget(self.ui_lbl_mu2)

        self.ui_le_muB = QLineEdit(Form)
        self.ui_le_muB.setObjectName(u"ui_le_muB")

        self.ui_layout_visco.addWidget(self.ui_le_muB)

        self.ui_lbl_mu3 = QLabel(Form)
        self.ui_lbl_mu3.setObjectName(u"ui_lbl_mu3")

        self.ui_layout_visco.addWidget(self.ui_lbl_mu3)

        self.ui_le_muC = QLineEdit(Form)
        self.ui_le_muC.setObjectName(u"ui_le_muC")

        self.ui_layout_visco.addWidget(self.ui_le_muC)

        self.ui_lbl_mu4 = QLabel(Form)
        self.ui_lbl_mu4.setObjectName(u"ui_lbl_mu4")

        self.ui_layout_visco.addWidget(self.ui_lbl_mu4)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.ui_layout_visco.addItem(self.horizontalSpacer_4)

        self.ui_btn_plot_dv = QPushButton(Form)
        self.ui_btn_plot_dv.setObjectName(u"ui_btn_plot_dv")

        self.ui_layout_visco.addWidget(self.ui_btn_plot_dv)


        self.ui_form_prop.setLayout(4, QFormLayout.FieldRole, self.ui_layout_visco)

        self.ui_lbl_dynaVisco_2 = QLabel(Form)
        self.ui_lbl_dynaVisco_2.setObjectName(u"ui_lbl_dynaVisco_2")

        self.ui_form_prop.setWidget(5, QFormLayout.LabelRole, self.ui_lbl_dynaVisco_2)

        self.ui_layout_rhoE = QHBoxLayout()
        self.ui_layout_rhoE.setObjectName(u"ui_layout_rhoE")
        self.ui_lbl_rhoE1 = QLabel(Form)
        self.ui_lbl_rhoE1.setObjectName(u"ui_lbl_rhoE1")

        self.ui_layout_rhoE.addWidget(self.ui_lbl_rhoE1)

        self.ui_le_rhoEA = QLineEdit(Form)
        self.ui_le_rhoEA.setObjectName(u"ui_le_rhoEA")

        self.ui_layout_rhoE.addWidget(self.ui_le_rhoEA)

        self.ui_lbl_rhoE2 = QLabel(Form)
        self.ui_lbl_rhoE2.setObjectName(u"ui_lbl_rhoE2")

        self.ui_layout_rhoE.addWidget(self.ui_lbl_rhoE2)

        self.ui_le_rhoEB = QLineEdit(Form)
        self.ui_le_rhoEB.setObjectName(u"ui_le_rhoEB")

        self.ui_layout_rhoE.addWidget(self.ui_le_rhoEB)

        self.ui_lbl_rhoE3 = QLabel(Form)
        self.ui_lbl_rhoE3.setObjectName(u"ui_lbl_rhoE3")

        self.ui_layout_rhoE.addWidget(self.ui_lbl_rhoE3)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.ui_layout_rhoE.addItem(self.horizontalSpacer_5)

        self.ui_btn_plot_er = QPushButton(Form)
        self.ui_btn_plot_er.setObjectName(u"ui_btn_plot_er")

        self.ui_layout_rhoE.addWidget(self.ui_btn_plot_er)


        self.ui_form_prop.setLayout(5, QFormLayout.FieldRole, self.ui_layout_rhoE)


        self.horizontalLayout_7.addLayout(self.ui_form_prop)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_7)


        self.verticalLayout.addLayout(self.horizontalLayout_7)

        self.ui_frame_plt = QFrame(Form)
        self.ui_frame_plt.setObjectName(u"ui_frame_plt")
        self.ui_frame_plt.setFrameShape(QFrame.StyledPanel)
        self.ui_frame_plt.setFrameShadow(QFrame.Raised)

        self.verticalLayout.addWidget(self.ui_frame_plt)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.ui_lbl_title.raise_()
        self.ui_frame_plt.raise_()
        QWidget.setTabOrder(self.ui_cBox_ref, self.ui_le_rhoA)
        QWidget.setTabOrder(self.ui_le_rhoA, self.ui_le_rhoB)
        QWidget.setTabOrder(self.ui_le_rhoB, self.ui_le_cpA)
        QWidget.setTabOrder(self.ui_le_cpA, self.ui_le_cpB)
        QWidget.setTabOrder(self.ui_le_cpB, self.ui_le_kA)
        QWidget.setTabOrder(self.ui_le_kA, self.ui_le_kB)
        QWidget.setTabOrder(self.ui_le_kB, self.ui_le_muA)
        QWidget.setTabOrder(self.ui_le_muA, self.ui_le_muB)
        QWidget.setTabOrder(self.ui_le_muB, self.ui_le_muC)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.ui_lbl_title.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">Material properties</span></p></body></html>", None))
        self.ui_lbl_reference.setText(QCoreApplication.translate("Form", u"Reference", None))
        self.ui_btn_clear_plot.setText(QCoreApplication.translate("Form", u"Clear Plot", None))
        self.ui_lbl_density.setText(QCoreApplication.translate("Form", u"Density", None))
        self.ui_lbl_rho1.setText(QCoreApplication.translate("Form", u"rho = ", None))
        self.ui_le_rhoA.setText(QCoreApplication.translate("Form", u"0,0", None))
        self.ui_lbl_rho2.setText(QCoreApplication.translate("Form", u"*(T\u00b0C+273.15) + ", None))
        self.ui_le_rhoB.setText(QCoreApplication.translate("Form", u"0,0", None))
        self.ui_lbl_rho3.setText(QCoreApplication.translate("Form", u" kg/m3", None))
#if QT_CONFIG(tooltip)
        self.ui_btn_plot_d.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Plot density versus temperature.</p><p>Each time you modify the density parameters, the curve will be updated!</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.ui_btn_plot_d.setText(QCoreApplication.translate("Form", u"Plot", None))
        self.ui_lbl_specHeat.setText(QCoreApplication.translate("Form", u"Specific heat", None))
        self.ui_lbl_cp1.setText(QCoreApplication.translate("Form", u"Cp = ", None))
        self.ui_le_cpA.setText(QCoreApplication.translate("Form", u"0,0", None))
        self.ui_lbl_cp2.setText(QCoreApplication.translate("Form", u"*(T\u00b0C+273.15) + ", None))
        self.ui_le_cpB.setText(QCoreApplication.translate("Form", u"0,0", None))
        self.ui_lbl_cp3.setText(QCoreApplication.translate("Form", u" J/kg/K", None))
#if QT_CONFIG(tooltip)
        self.ui_btn_plot_sh.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Plot specific heat versus temperature.</p><p>Each time you modify the specific heat parameters, the curve will be updated!</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.ui_btn_plot_sh.setText(QCoreApplication.translate("Form", u"Plot", None))
        self.ui_lbl_thermCond.setText(QCoreApplication.translate("Form", u"Thermal conductivity", None))
        self.ui_lbl_k1.setText(QCoreApplication.translate("Form", u"k = ", None))
        self.ui_le_kA.setText(QCoreApplication.translate("Form", u"0,0", None))
        self.ui_lbl_k2.setText(QCoreApplication.translate("Form", u"*(T\u00b0C+273.15) + ", None))
        self.ui_le_kB.setText(QCoreApplication.translate("Form", u"0,0", None))
        self.ui_lbl_k3.setText(QCoreApplication.translate("Form", u"W/m/K", None))
#if QT_CONFIG(tooltip)
        self.ui_btn_plot_tc.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Plot thermal conductivity versus temperature.</p><p>Each time you modify the thermal conductivity parameters, the curve will be updated!</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.ui_btn_plot_tc.setText(QCoreApplication.translate("Form", u"Plot", None))
        self.ui_lbl_dynaVisco.setText(QCoreApplication.translate("Form", u"Dynamic viscosity", None))
        self.ui_lbl_mu1.setText(QCoreApplication.translate("Form", u"\u00b5 = ", None))
        self.ui_le_muA.setText(QCoreApplication.translate("Form", u"0,0", None))
        self.ui_lbl_mu2.setText(QCoreApplication.translate("Form", u"*(((T\u00b0C+273.15)/ ", None))
        self.ui_le_muB.setText(QCoreApplication.translate("Form", u"1,0", None))
        self.ui_lbl_mu3.setText(QCoreApplication.translate("Form", u" )^ ", None))
        self.ui_le_muC.setText(QCoreApplication.translate("Form", u"1,0", None))
        self.ui_lbl_mu4.setText(QCoreApplication.translate("Form", u") Pa.s", None))
#if QT_CONFIG(tooltip)
        self.ui_btn_plot_dv.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Plot dynamic viscosity versus temperature.</p><p>Each time you modify the dynamic viscosity parameters, the curve will be updated!</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.ui_btn_plot_dv.setText(QCoreApplication.translate("Form", u"Plot", None))
        self.ui_lbl_dynaVisco_2.setText(QCoreApplication.translate("Form", u"Electrical resistivity", None))
        self.ui_lbl_rhoE1.setText(QCoreApplication.translate("Form", u"rhoE = ", None))
        self.ui_le_rhoEA.setText(QCoreApplication.translate("Form", u"0,0", None))
        self.ui_lbl_rhoE2.setText(QCoreApplication.translate("Form", u"*(T\u00b0C+235)/( ", None))
        self.ui_le_rhoEB.setText(QCoreApplication.translate("Form", u"0,0", None))
        self.ui_lbl_rhoE3.setText(QCoreApplication.translate("Form", u"+235) ohm.m", None))
#if QT_CONFIG(tooltip)
        self.ui_btn_plot_er.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Plot electrical resistivity versus temperature.</p><p>Each time you modify the electrical resistivity parameters, the curve will be updated!</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.ui_btn_plot_er.setText(QCoreApplication.translate("Form", u"Plot", None))
    # retranslateUi

