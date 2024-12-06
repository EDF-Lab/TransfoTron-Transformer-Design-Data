# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'error.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QHBoxLayout,
    QLabel, QPlainTextEdit, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(469, 274)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.ui_lbl_image = QLabel(Dialog)
        self.ui_lbl_image.setObjectName(u"ui_lbl_image")

        self.horizontalLayout.addWidget(self.ui_lbl_image)

        self.ui_lbl_title = QLabel(Dialog)
        self.ui_lbl_title.setObjectName(u"ui_lbl_title")

        self.horizontalLayout.addWidget(self.ui_lbl_title)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.ui_txt_msg = QPlainTextEdit(Dialog)
        self.ui_txt_msg.setObjectName(u"ui_txt_msg")

        self.verticalLayout.addWidget(self.ui_txt_msg)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.ui_btn_copy = QPushButton(Dialog)
        self.ui_btn_copy.setObjectName(u"ui_btn_copy")

        self.gridLayout.addWidget(self.ui_btn_copy, 0, 0, 1, 1)

        self.ui_btn_mail = QPushButton(Dialog)
        self.ui_btn_mail.setObjectName(u"ui_btn_mail")

        self.gridLayout.addWidget(self.ui_btn_mail, 0, 1, 1, 1)

        self.ui_btn_close = QPushButton(Dialog)
        self.ui_btn_close.setObjectName(u"ui_btn_close")

        self.gridLayout.addWidget(self.ui_btn_close, 0, 2, 1, 1)

        self.ui_btn_exit = QPushButton(Dialog)
        self.ui_btn_exit.setObjectName(u"ui_btn_exit")

        self.gridLayout.addWidget(self.ui_btn_exit, 0, 3, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.ui_lbl_image.setText(QCoreApplication.translate("Dialog", u"image", None))
        self.ui_lbl_title.setText(QCoreApplication.translate("Dialog", u"Something went wrong...", None))
        self.ui_btn_copy.setText(QCoreApplication.translate("Dialog", u"Copy to clipboard", None))
        self.ui_btn_mail.setText(QCoreApplication.translate("Dialog", u"Generate Outlook email", None))
        self.ui_btn_close.setText(QCoreApplication.translate("Dialog", u"Close dialog", None))
        self.ui_btn_exit.setText(QCoreApplication.translate("Dialog", u"Exit TransfoTron", None))
    # retranslateUi

