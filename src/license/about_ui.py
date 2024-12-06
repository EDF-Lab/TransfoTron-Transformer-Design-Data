# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'about.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QLabel, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(334, 164)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.ui_lbl_name = QLabel(Dialog)
        self.ui_lbl_name.setObjectName(u"ui_lbl_name")

        self.verticalLayout.addWidget(self.ui_lbl_name)

        self.ui_lbl_version = QLabel(Dialog)
        self.ui_lbl_version.setObjectName(u"ui_lbl_version")

        self.verticalLayout.addWidget(self.ui_lbl_version)

        self.ui_lbl_copyright = QLabel(Dialog)
        self.ui_lbl_copyright.setObjectName(u"ui_lbl_copyright")

        self.verticalLayout.addWidget(self.ui_lbl_copyright)

        self.ui_lbl_assistance = QLabel(Dialog)
        self.ui_lbl_assistance.setObjectName(u"ui_lbl_assistance")

        self.verticalLayout.addWidget(self.ui_lbl_assistance)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.ui_lbl_name.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-weight:700;\">transfoTron</span></p></body></html>", None))
        self.ui_lbl_version.setText(QCoreApplication.translate("Dialog", u"Version", None))
        self.ui_lbl_copyright.setText(QCoreApplication.translate("Dialog", u"Copyright EDF 2019-", None))
        self.ui_lbl_assistance.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" text-decoration: underline;\">Assistance: </span></p><p><a href=\"mailto:remi.desquiens@edf.fr\"><span style=\" text-decoration: underline; color:#0000ff;\">remi.desquiens@edf.fr</span></a> and <a href=\"mailto:damien.bortolotti@edf.fr\"><span style=\" text-decoration: underline; color:#0000ff;\">damien.bortolotti@edf.fr</span></a></p></body></html>", None))
    # retranslateUi

