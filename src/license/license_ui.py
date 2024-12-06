# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'license.ui'
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
    QListView, QPlainTextEdit, QSizePolicy, QSplitter,
    QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(924, 571)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.ui_splitter = QSplitter(Dialog)
        self.ui_splitter.setObjectName(u"ui_splitter")
        self.ui_splitter.setOrientation(Qt.Horizontal)
        self.ui_list_license = QListView(self.ui_splitter)
        self.ui_list_license.setObjectName(u"ui_list_license")
        self.ui_splitter.addWidget(self.ui_list_license)
        self.ui_txt_license = QPlainTextEdit(self.ui_splitter)
        self.ui_txt_license.setObjectName(u"ui_txt_license")
        self.ui_splitter.addWidget(self.ui_txt_license)

        self.verticalLayout.addWidget(self.ui_splitter)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)

        QWidget.setTabOrder(self.ui_list_license, self.ui_txt_license)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
    # retranslateUi

