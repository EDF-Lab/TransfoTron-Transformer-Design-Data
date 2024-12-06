# -*- coding: utf-8 -*-

# https://github.com/eyllanesc/stackoverflow/tree/master/questions/46469720

from PySide6.QtWidgets import QTableView, QAbstractItemView
from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication

from .GridTableHeaderView import GridTableHeaderView

class GridTableView(QTableView):

    def __init__(self, parent=None):
        super().__init__(parent)

    def keyPressEvent (self, e):

        # Suppression du contenu de la case
        if e.key() == Qt.Key_Delete or e.key() == Qt.Key_Backspace:
            if self.editTriggers() == QAbstractItemView.NoEditTriggers:
                return
            for c in self.selectedIndexes():
                item = self.model().itemFromIndex(c)
                if item.isEditable():
                    item.setText("")

        # Passage à la ligne inférieure
        elif e.key() in (Qt.Key_Return, Qt.Key_Enter):
            current = self.currentIndex()
            nextIndex = current.sibling(current.row() + 1, current.column())
            if nextIndex.isValid():
                self.setCurrentIndex(nextIndex)
                if self.model().itemFromIndex(nextIndex).isEditable() and (self.editTriggers() != QAbstractItemView.NoEditTriggers):
                    self.edit(nextIndex)

        # Copier
        elif e.key() == Qt.Key_C and (e.modifiers() & Qt.ControlModifier):
            copied_cells = sorted(self.selectedIndexes())
            copy_text = ''
            max_column = copied_cells[-1].column()
            for c in copied_cells:
                copy_text += self.model().itemFromIndex(c).text()
                if c.column() == max_column:
                    copy_text += '\n'
                else:
                    copy_text += '\t'
            QGuiApplication.clipboard().setText(copy_text)

        # Couper
        elif e.key() == Qt.Key_X and (e.modifiers() & Qt.ControlModifier):
            copied_cells = sorted(self.selectedIndexes())
            copy_text = ''
            max_column = copied_cells[-1].column()
            for c in copied_cells:
                item = self.model().itemFromIndex(c)
                copy_text += item.text()
                if c.column() == max_column:
                    copy_text += '\n'
                else:
                    copy_text += '\t'
                if item.isEditable() and (self.editTriggers() != QAbstractItemView.NoEditTriggers):
                    item.setText("")
            QGuiApplication.clipboard().setText(copy_text)

        # Coller
        elif e.key() == Qt.Key_V and (e.modifiers() & Qt.ControlModifier):
            if self.editTriggers() == QAbstractItemView.NoEditTriggers:
                return
            paste_text = QGuiApplication.clipboard().text()

            # On enlève un éventuel saut de ligne final
            if paste_text[-1:] == '\n':
                paste_text = paste_text[:-1]
            tab = [k.split("\t") for k in paste_text.split("\n")]
            # Il peut y avoir des erreurs si on a pas mis setSelectionMode(QAbstractItemView.ContiguousSelection) sur le tableau à la copie

            r = self.currentIndex().row()
            c = self.currentIndex().column()
            for k_row in range(len(tab)):
                for k_col in range(len(tab[k_row])):
                    item = self.model().item(k_row + r, k_col + c)
                    if item is None:
                        continue
                    if item.isEditable():
                        txt = tab[k_row][k_col]
                        # On converti les virgules en point si ça donne un float
                        try:
                            float(txt.replace(",", "."))
                        except:
                            pass
                        else:
                            txt = txt.replace(",", ".")
                        item.setText(txt)

        else:
            super().keyPressEvent(e)

    def setGridHeaderview(self, orientation, levelsInOrientation, levelsPerpOrientation=0):
        if orientation == Qt.Horizontal:
            if levelsPerpOrientation > 0:
                header = GridTableHeaderView(orientation, levelsInOrientation, levelsPerpOrientation)
            else:
                header = GridTableHeaderView(orientation, levelsInOrientation, self.model().columnCount())
            self.setHorizontalHeader(header)
            header.sectionPressed.connect(self.horizontalHeaderSectionPressed)
        else:
            if levelsPerpOrientation > 0:
                header = GridTableHeaderView(orientation, levelsPerpOrientation, levelsInOrientation)
            else:
                header = GridTableHeaderView(orientation, self.model().rowCount(), levelsInOrientation)
            self.setVerticalHeader(header)
            header.sectionPressed.connect(self.verticalHeaderSectionPressed)

    def gridHeaderview(self, orientation):
        if orientation == Qt.Horizontal:
            header = self.horizontalHeader()
        else:
            header = self.verticalHeader()
        return header

    def horizontalHeaderSectionPressed(self, beginSection, endSection):
        self.clearSelection()
        oldSelectionMode = self.selectionMode()
        self.setSelectionMode(QAbstractItemView.MultiSelection);
        for i in range(beginSection, endSection + 1):
            self.selectColumn(i)
        self.setSelectionMode(oldSelectionMode)

    def verticalHeaderSectionPressed(self, beginSection, endSection):
        self.clearSelection()
        oldSelectionMode = self.selectionMode()
        self.setSelectionMode(QAbstractItemView.MultiSelection);
        for i in range(beginSection, endSection + 1):
            self.selectRow(i)
        self.setSelectionMode(oldSelectionMode)


