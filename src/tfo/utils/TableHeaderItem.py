# -*- coding: utf-8 -*-

# https://github.com/eyllanesc/stackoverflow/tree/master/questions/46469720

class TableHeaderItem():

    def __init__(self, row=0, column=0, parent=0):
        self.m_parentItem = parent
        self.m_childItems = {}
        self.m_itemData = {}
        self.row = row
        self.column = column

    def insertChild(self, row, col):
        child = TableHeaderItem(row, col, self)
        self.m_childItems[(row, col)] = child
        return child

    def child(self, row, col):
        if (row, col) in self.m_childItems.keys():
            return self.m_childItems[(row, col)]
        return 0

    def parent(self):
        return self.m_parentItem

    def row(self):
        return self.row

    def column(self):
        return self.column

    def setData(self, data, role):
        self.m_itemData[role] = data

    def data(self, role):
        if role in self.m_itemData.keys():
            return self.m_itemData[role]
        return None

    def clear(self):
        for k in self.m_childItems.keys():
            self.m_childItems[k].clear()
        self.m_childItems = {}

