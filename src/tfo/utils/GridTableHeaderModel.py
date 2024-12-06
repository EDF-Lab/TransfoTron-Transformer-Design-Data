# -*- coding: utf-8 -*-

# https://github.com/eyllanesc/stackoverflow/tree/master/questions/46469720

from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex

from .TableHeaderItem import TableHeaderItem

class GridTableHeaderModel(QAbstractTableModel):

    ColumnSpanRole = Qt.UserRole + 1
    RowSpanRole = ColumnSpanRole + 1

    def __init__(self, row, column, parent=None):
        super().__init__(parent)
        self.row = row
        self.column = column
        self.rootItem = TableHeaderItem()

    def index(self, row, column, parent=QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        parentItem = TableHeaderItem()
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row, column)
        if not childItem:
            childItem = parentItem.insertChild(row, column)
        return self.createIndex(row, column, childItem)

    def rowCount(self, parent=QModelIndex()):
        return self.row

    def columnCount(self, parent=QModelIndex()):
        return self.column

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        return QAbstractTableModel.flags(index)

    def data(self, index, role):
        if not index.isValid():
            return ""
        if index.row() >= self.row or index.row() < 0 or index.column() >= self.column or index.column() < 0:
            return ""
        item = index.internalPointer()
        return item.data(role)

    def setData(self, index, value, role):
        if index.isValid():
            item = index.internalPointer()
            if role == self.ColumnSpanRole:
                col = index.column()
                span = int(value)
                if span > 0:
                    if col + span - 1 >= self.column:
                        span = self.column - col
                    item.setData(span, self.ColumnSpanRole)
            elif role == self.RowSpanRole:
                row = index.row()
                span = int(value)
                if span > 0:
                    if row + span - 1 > self.row:
                        span = self.column - row
                    item.setData(span, self.RowSpanRole)
            else:
                item.setData(value, role)
            return True
        return False



