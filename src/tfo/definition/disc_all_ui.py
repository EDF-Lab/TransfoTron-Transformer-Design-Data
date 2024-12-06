# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'disc_all.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QListView, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(688, 501)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setMaximumSize(QSize(300, 16777215))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.ui_lbl_listDisc = QLabel(self.frame)
        self.ui_lbl_listDisc.setObjectName(u"ui_lbl_listDisc")

        self.verticalLayout.addWidget(self.ui_lbl_listDisc)

        self.ui_listDisc = QListView(self.frame)
        self.ui_listDisc.setObjectName(u"ui_listDisc")
        self.ui_listDisc.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout.addWidget(self.ui_listDisc)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.ui_btn_new = QPushButton(self.frame)
        self.ui_btn_new.setObjectName(u"ui_btn_new")

        self.horizontalLayout_2.addWidget(self.ui_btn_new)

        self.ui_btn_delete = QPushButton(self.frame)
        self.ui_btn_delete.setObjectName(u"ui_btn_delete")

        self.horizontalLayout_2.addWidget(self.ui_btn_delete)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.horizontalLayout.addWidget(self.frame)

        self.ui_frame_discOne = QFrame(Form)
        self.ui_frame_discOne.setObjectName(u"ui_frame_discOne")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ui_frame_discOne.sizePolicy().hasHeightForWidth())
        self.ui_frame_discOne.setSizePolicy(sizePolicy)
        self.ui_frame_discOne.setFrameShape(QFrame.StyledPanel)
        self.ui_frame_discOne.setFrameShadow(QFrame.Raised)

        self.horizontalLayout.addWidget(self.ui_frame_discOne)

        self.horizontalSpacer = QSpacerItem(345, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.ui_lbl_listDisc.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">List of discs</span></p></body></html>", None))
        self.ui_btn_new.setText(QCoreApplication.translate("Form", u"New", None))
        self.ui_btn_delete.setText(QCoreApplication.translate("Form", u"Delete", None))
    # retranslateUi

