# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'toleranceDefinition.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QComboBox,
    QDialog, QDialogButtonBox, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QPlainTextEdit,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(324, 723)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.ui_lbl_catalog = QLabel(Dialog)
        self.ui_lbl_catalog.setObjectName(u"ui_lbl_catalog")

        self.gridLayout_3.addWidget(self.ui_lbl_catalog, 1, 0, 1, 1)

        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_3.addWidget(self.label_3, 2, 0, 1, 1)

        self.ui_lbl_title = QLabel(Dialog)
        self.ui_lbl_title.setObjectName(u"ui_lbl_title")

        self.gridLayout_3.addWidget(self.ui_lbl_title, 0, 0, 1, 2)

        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_3.addWidget(self.label_4, 4, 0, 1, 1)

        self.ui_cb_catalog = QComboBox(Dialog)
        self.ui_cb_catalog.setObjectName(u"ui_cb_catalog")

        self.gridLayout_3.addWidget(self.ui_cb_catalog, 1, 1, 1, 1)

        self.ui_cb_defOption = QComboBox(Dialog)
        self.ui_cb_defOption.setObjectName(u"ui_cb_defOption")

        self.gridLayout_3.addWidget(self.ui_cb_defOption, 4, 1, 1, 1)

        self.ui_le_reference = QLineEdit(Dialog)
        self.ui_le_reference.setObjectName(u"ui_le_reference")

        self.gridLayout_3.addWidget(self.ui_le_reference, 2, 1, 1, 1)

        self.ui_lbl_nota = QLabel(Dialog)
        self.ui_lbl_nota.setObjectName(u"ui_lbl_nota")

        self.gridLayout_3.addWidget(self.ui_lbl_nota, 3, 0, 1, 1)

        self.ui_txt_nota = QPlainTextEdit(Dialog)
        self.ui_txt_nota.setObjectName(u"ui_txt_nota")

        self.gridLayout_3.addWidget(self.ui_txt_nota, 3, 1, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_3)

        self.ui_gb_A = QGroupBox(Dialog)
        self.ui_gb_A.setObjectName(u"ui_gb_A")
        self.gridLayout = QGridLayout(self.ui_gb_A)
        self.gridLayout.setObjectName(u"gridLayout")
        self.ui_le_A_base = QLineEdit(self.ui_gb_A)
        self.ui_le_A_base.setObjectName(u"ui_le_A_base")

        self.gridLayout.addWidget(self.ui_le_A_base, 2, 0, 2, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.ui_lbl_A_plus = QLabel(self.ui_gb_A)
        self.ui_lbl_A_plus.setObjectName(u"ui_lbl_A_plus")

        self.horizontalLayout.addWidget(self.ui_lbl_A_plus)

        self.ui_le_A_plus = QLineEdit(self.ui_gb_A)
        self.ui_le_A_plus.setObjectName(u"ui_le_A_plus")

        self.horizontalLayout.addWidget(self.ui_le_A_plus)

        self.ui_lbl_A_plus_pc = QLabel(self.ui_gb_A)
        self.ui_lbl_A_plus_pc.setObjectName(u"ui_lbl_A_plus_pc")

        self.horizontalLayout.addWidget(self.ui_lbl_A_plus_pc)

        self.ui_chk_A_plus_included = QCheckBox(self.ui_gb_A)
        self.ui_chk_A_plus_included.setObjectName(u"ui_chk_A_plus_included")

        self.horizontalLayout.addWidget(self.ui_chk_A_plus_included)


        self.gridLayout.addLayout(self.horizontalLayout, 2, 1, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.ui_lbl_A_minus = QLabel(self.ui_gb_A)
        self.ui_lbl_A_minus.setObjectName(u"ui_lbl_A_minus")

        self.horizontalLayout_2.addWidget(self.ui_lbl_A_minus)

        self.ui_le_A_minus = QLineEdit(self.ui_gb_A)
        self.ui_le_A_minus.setObjectName(u"ui_le_A_minus")

        self.horizontalLayout_2.addWidget(self.ui_le_A_minus)

        self.ui_lbl_A_minus_pc = QLabel(self.ui_gb_A)
        self.ui_lbl_A_minus_pc.setObjectName(u"ui_lbl_A_minus_pc")

        self.horizontalLayout_2.addWidget(self.ui_lbl_A_minus_pc)

        self.ui_chk_A_minus_included = QCheckBox(self.ui_gb_A)
        self.ui_chk_A_minus_included.setObjectName(u"ui_chk_A_minus_included")

        self.horizontalLayout_2.addWidget(self.ui_chk_A_minus_included)


        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 1, 1, 1)

        self.ui_chk_A_symetric = QCheckBox(self.ui_gb_A)
        self.ui_chk_A_symetric.setObjectName(u"ui_chk_A_symetric")

        self.gridLayout.addWidget(self.ui_chk_A_symetric, 0, 0, 1, 2)


        self.verticalLayout_2.addWidget(self.ui_gb_A)

        self.ui_gb_B = QGroupBox(Dialog)
        self.ui_gb_B.setObjectName(u"ui_gb_B")
        self.gridLayout_6 = QGridLayout(self.ui_gb_B)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.ui_le_B_base = QLineEdit(self.ui_gb_B)
        self.ui_le_B_base.setObjectName(u"ui_le_B_base")

        self.gridLayout_6.addWidget(self.ui_le_B_base, 2, 0, 2, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.ui_lbl_B_plus = QLabel(self.ui_gb_B)
        self.ui_lbl_B_plus.setObjectName(u"ui_lbl_B_plus")

        self.horizontalLayout_5.addWidget(self.ui_lbl_B_plus)

        self.ui_le_B_plus = QLineEdit(self.ui_gb_B)
        self.ui_le_B_plus.setObjectName(u"ui_le_B_plus")

        self.horizontalLayout_5.addWidget(self.ui_le_B_plus)

        self.ui_chk_B_plus_included = QCheckBox(self.ui_gb_B)
        self.ui_chk_B_plus_included.setObjectName(u"ui_chk_B_plus_included")

        self.horizontalLayout_5.addWidget(self.ui_chk_B_plus_included)


        self.gridLayout_6.addLayout(self.horizontalLayout_5, 2, 1, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.ui_lbl_B_minus = QLabel(self.ui_gb_B)
        self.ui_lbl_B_minus.setObjectName(u"ui_lbl_B_minus")

        self.horizontalLayout_6.addWidget(self.ui_lbl_B_minus)

        self.ui_le_B_minus = QLineEdit(self.ui_gb_B)
        self.ui_le_B_minus.setObjectName(u"ui_le_B_minus")

        self.horizontalLayout_6.addWidget(self.ui_le_B_minus)

        self.ui_chk_B_minus_included = QCheckBox(self.ui_gb_B)
        self.ui_chk_B_minus_included.setObjectName(u"ui_chk_B_minus_included")

        self.horizontalLayout_6.addWidget(self.ui_chk_B_minus_included)


        self.gridLayout_6.addLayout(self.horizontalLayout_6, 3, 1, 1, 1)

        self.ui_chk_B_symetric = QCheckBox(self.ui_gb_B)
        self.ui_chk_B_symetric.setObjectName(u"ui_chk_B_symetric")

        self.gridLayout_6.addWidget(self.ui_chk_B_symetric, 0, 0, 1, 2)


        self.verticalLayout_2.addWidget(self.ui_gb_B)

        self.ui_gb_C = QGroupBox(Dialog)
        self.ui_gb_C.setObjectName(u"ui_gb_C")
        self.gridLayout_7 = QGridLayout(self.ui_gb_C)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.ui_lbl_C_plus = QLabel(self.ui_gb_C)
        self.ui_lbl_C_plus.setObjectName(u"ui_lbl_C_plus")

        self.horizontalLayout_7.addWidget(self.ui_lbl_C_plus)

        self.ui_le_C_plus = QLineEdit(self.ui_gb_C)
        self.ui_le_C_plus.setObjectName(u"ui_le_C_plus")

        self.horizontalLayout_7.addWidget(self.ui_le_C_plus)

        self.ui_chk_C_plus_included = QCheckBox(self.ui_gb_C)
        self.ui_chk_C_plus_included.setObjectName(u"ui_chk_C_plus_included")

        self.horizontalLayout_7.addWidget(self.ui_chk_C_plus_included)


        self.gridLayout_7.addLayout(self.horizontalLayout_7, 1, 0, 1, 1)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.ui_lbl_C_minus = QLabel(self.ui_gb_C)
        self.ui_lbl_C_minus.setObjectName(u"ui_lbl_C_minus")

        self.horizontalLayout_8.addWidget(self.ui_lbl_C_minus)

        self.ui_le_C_minus = QLineEdit(self.ui_gb_C)
        self.ui_le_C_minus.setObjectName(u"ui_le_C_minus")

        self.horizontalLayout_8.addWidget(self.ui_le_C_minus)

        self.ui_chk_C_minus_included = QCheckBox(self.ui_gb_C)
        self.ui_chk_C_minus_included.setObjectName(u"ui_chk_C_minus_included")

        self.horizontalLayout_8.addWidget(self.ui_chk_C_minus_included)


        self.gridLayout_7.addLayout(self.horizontalLayout_8, 2, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.ui_gb_C)

        self.ui_gb_check = QGroupBox(Dialog)
        self.ui_gb_check.setObjectName(u"ui_gb_check")
        self.gridLayout_2 = QGridLayout(self.ui_gb_check)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.ui_le_chk_base = QLineEdit(self.ui_gb_check)
        self.ui_le_chk_base.setObjectName(u"ui_le_chk_base")

        self.gridLayout_2.addWidget(self.ui_le_chk_base, 2, 0, 1, 1)

        self.label_14 = QLabel(self.ui_gb_check)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_14, 3, 0, 1, 1)

        self.ui_lbl_chk_base = QLabel(self.ui_gb_check)
        self.ui_lbl_chk_base.setObjectName(u"ui_lbl_chk_base")

        self.gridLayout_2.addWidget(self.ui_lbl_chk_base, 1, 0, 1, 1)

        self.ui_lbl_chk_okko = QLabel(self.ui_gb_check)
        self.ui_lbl_chk_okko.setObjectName(u"ui_lbl_chk_okko")

        self.gridLayout_2.addWidget(self.ui_lbl_chk_okko, 3, 2, 1, 2)

        self.ui_le_chk_max = QLineEdit(self.ui_gb_check)
        self.ui_le_chk_max.setObjectName(u"ui_le_chk_max")

        self.gridLayout_2.addWidget(self.ui_le_chk_max, 2, 3, 1, 1)

        self.label_13 = QLabel(self.ui_gb_check)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_2.addWidget(self.label_13, 1, 3, 1, 1)

        self.ui_lbl_chk_synthese = QLabel(self.ui_gb_check)
        self.ui_lbl_chk_synthese.setObjectName(u"ui_lbl_chk_synthese")
        self.ui_lbl_chk_synthese.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.ui_lbl_chk_synthese, 0, 0, 1, 4)

        self.label_12 = QLabel(self.ui_gb_check)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_2.addWidget(self.label_12, 1, 1, 1, 1)

        self.ui_le_chk_min = QLineEdit(self.ui_gb_check)
        self.ui_le_chk_min.setObjectName(u"ui_le_chk_min")

        self.gridLayout_2.addWidget(self.ui_le_chk_min, 2, 1, 1, 1)

        self.ui_le_chk_value = QLineEdit(self.ui_gb_check)
        self.ui_le_chk_value.setObjectName(u"ui_le_chk_value")

        self.gridLayout_2.addWidget(self.ui_le_chk_value, 3, 1, 1, 1)


        self.verticalLayout_2.addWidget(self.ui_gb_check)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_16 = QLabel(Dialog)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.gridLayout_4.addWidget(self.label_16, 0, 0, 1, 1)

        self.ui_txt_comments = QPlainTextEdit(Dialog)
        self.ui_txt_comments.setObjectName(u"ui_txt_comments")

        self.gridLayout_4.addWidget(self.ui_txt_comments, 0, 1, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_4)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)

        self.verticalLayout_2.addWidget(self.buttonBox)

        QWidget.setTabOrder(self.ui_cb_catalog, self.ui_le_reference)
        QWidget.setTabOrder(self.ui_le_reference, self.ui_txt_nota)
        QWidget.setTabOrder(self.ui_txt_nota, self.ui_cb_defOption)
        QWidget.setTabOrder(self.ui_cb_defOption, self.ui_chk_A_symetric)
        QWidget.setTabOrder(self.ui_chk_A_symetric, self.ui_le_A_base)
        QWidget.setTabOrder(self.ui_le_A_base, self.ui_le_A_plus)
        QWidget.setTabOrder(self.ui_le_A_plus, self.ui_chk_A_plus_included)
        QWidget.setTabOrder(self.ui_chk_A_plus_included, self.ui_le_A_minus)
        QWidget.setTabOrder(self.ui_le_A_minus, self.ui_chk_A_minus_included)
        QWidget.setTabOrder(self.ui_chk_A_minus_included, self.ui_chk_B_symetric)
        QWidget.setTabOrder(self.ui_chk_B_symetric, self.ui_le_B_base)
        QWidget.setTabOrder(self.ui_le_B_base, self.ui_le_B_plus)
        QWidget.setTabOrder(self.ui_le_B_plus, self.ui_chk_B_plus_included)
        QWidget.setTabOrder(self.ui_chk_B_plus_included, self.ui_le_B_minus)
        QWidget.setTabOrder(self.ui_le_B_minus, self.ui_chk_B_minus_included)
        QWidget.setTabOrder(self.ui_chk_B_minus_included, self.ui_le_C_plus)
        QWidget.setTabOrder(self.ui_le_C_plus, self.ui_chk_C_plus_included)
        QWidget.setTabOrder(self.ui_chk_C_plus_included, self.ui_le_C_minus)
        QWidget.setTabOrder(self.ui_le_C_minus, self.ui_chk_C_minus_included)
        QWidget.setTabOrder(self.ui_chk_C_minus_included, self.ui_le_chk_base)
        QWidget.setTabOrder(self.ui_le_chk_base, self.ui_le_chk_min)
        QWidget.setTabOrder(self.ui_le_chk_min, self.ui_le_chk_max)
        QWidget.setTabOrder(self.ui_le_chk_max, self.ui_le_chk_value)
        QWidget.setTabOrder(self.ui_le_chk_value, self.ui_txt_comments)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.ui_lbl_catalog.setText(QCoreApplication.translate("Dialog", u"Catalog", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Reference", None))
        self.ui_lbl_title.setText(QCoreApplication.translate("Dialog", u"title", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Definition option", None))
        self.ui_lbl_nota.setText(QCoreApplication.translate("Dialog", u"Nota", None))
        self.ui_gb_A.setTitle("")
        self.ui_lbl_A_plus.setText(QCoreApplication.translate("Dialog", u"+", None))
        self.ui_lbl_A_plus_pc.setText(QCoreApplication.translate("Dialog", u"%", None))
        self.ui_chk_A_plus_included.setText(QCoreApplication.translate("Dialog", u"Included", None))
        self.ui_lbl_A_minus.setText(QCoreApplication.translate("Dialog", u"-", None))
        self.ui_lbl_A_minus_pc.setText(QCoreApplication.translate("Dialog", u"%", None))
        self.ui_chk_A_minus_included.setText(QCoreApplication.translate("Dialog", u"Included", None))
        self.ui_chk_A_symetric.setText(QCoreApplication.translate("Dialog", u"Symetric interval", None))
        self.ui_gb_B.setTitle("")
        self.ui_lbl_B_plus.setText(QCoreApplication.translate("Dialog", u"+", None))
        self.ui_chk_B_plus_included.setText(QCoreApplication.translate("Dialog", u"Included", None))
        self.ui_lbl_B_minus.setText(QCoreApplication.translate("Dialog", u"-", None))
        self.ui_chk_B_minus_included.setText(QCoreApplication.translate("Dialog", u"Included", None))
        self.ui_chk_B_symetric.setText(QCoreApplication.translate("Dialog", u"Symetric interval", None))
        self.ui_gb_C.setTitle("")
        self.ui_lbl_C_plus.setText(QCoreApplication.translate("Dialog", u">", None))
        self.ui_chk_C_plus_included.setText(QCoreApplication.translate("Dialog", u"Included", None))
        self.ui_lbl_C_minus.setText(QCoreApplication.translate("Dialog", u"<", None))
        self.ui_chk_C_minus_included.setText(QCoreApplication.translate("Dialog", u"Included", None))
        self.ui_gb_check.setTitle(QCoreApplication.translate("Dialog", u"Check and try me!", None))
        self.label_14.setText(QCoreApplication.translate("Dialog", u"Value to test", None))
        self.ui_lbl_chk_base.setText(QCoreApplication.translate("Dialog", u"Base", None))
        self.ui_lbl_chk_okko.setText(QCoreApplication.translate("Dialog", u"ok_ko", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"Max allowed", None))
        self.ui_lbl_chk_synthese.setText(QCoreApplication.translate("Dialog", u"lbl_synthese", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"Min allowed", None))
        self.label_16.setText(QCoreApplication.translate("Dialog", u"Comments", None))
    # retranslateUi

