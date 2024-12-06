# -*- coding: utf-8 -*-

# https://github.com/eyllanesc/stackoverflow/tree/master/questions/46469720

from PySide6.QtWidgets import QHeaderView, QStyleOptionHeader, QStyle
from PySide6.QtCore import Qt, Signal, QSize, QModelIndex, QRect
from PySide6.QtGui import QPalette

from .GridTableHeaderModel import GridTableHeaderModel

class GridTableHeaderView(QHeaderView):

    sectionPressed = Signal(int, int)

    def __init__(self, orientation, rows, columns, parent=None):
        super().__init__(orientation, parent)

        baseSectionSize = QSize()
        if orientation == Qt.Horizontal:
            baseSectionSize.setWidth(self.defaultSectionSize())
            baseSectionSize.setHeight(40)
        else:
            baseSectionSize.setWidth(50)
            baseSectionSize.setHeight(self.defaultSectionSize())

        model = GridTableHeaderModel(rows, columns)
        for row in range(rows):
            for col in range(columns):
                model.setData(model.index(row, col), baseSectionSize, Qt.SizeHintRole)
        self.setModel(model)

        self.sectionResized.connect(self.onSectionResized)

    def setCellLabel(self, row, column, label):
        self.model().setData(self.model().index(row, column), label, Qt.DisplayRole)

    def setCellBackgroundColor(self, row, column, color):
        self.model().setData(self.model().index(row, column), color, Qt.BackgroundRole)

    def setCellForegroundColor(self, row, column, color):
        self.model().setData(self.model().index(row, column), color, Qt.ForegroundRole)

    def indexAt(self, pos):
        tblModel = self.model()
        rows = tblModel.rowCount()
        cols = tblModel.columnCount()
        logicalIdx = self.logicalIndexAt(pos)
        delta = 0

        if self.orientation() == Qt.Horizontal:
            for row in range(rows):
                cellIndex = tblModel.index(row, logicalIdx)
                if cellIndex.data(Qt.SizeHintRole) is not None:
                    delta += cellIndex.data(Qt.SizeHintRole).height()
                    if pos.y() <= delta:
                        return cellIndex
        else:
            for col in range(cols):
                cellIndex = tblModel.index(logicalIdx, col)
                if cellIndex.data(Qt.SizeHintRole) is not None:
                    delta += cellIndex.data(Qt.SizeHintRole).width()
                    if pos.x() <= delta:
                        return cellIndex

        return QModelIndex()

    def paintSection(self, painter, rect, logicalIndex):
        tblModel = self.model()
        if self.orientation() == Qt.Horizontal:
            level = tblModel.rowCount()
        else:
            level = tblModel.columnCount()

        i = 0
        while i < level:
            if self.orientation() == Qt.Horizontal:
                cellIndex = tblModel.index(i, logicalIndex)
            else:
                cellIndex = tblModel.index(logicalIndex, i)
            cellSize = cellIndex.data(Qt.SizeHintRole)
            sectionRect = QRect(rect)

            # Set position of the cell
            if self.orientation() == Qt.Horizontal:
                sectionRect.setTop(self.rowSpanSize(logicalIndex, 0, i)) # Distance from 0 to i-1 rows
            else:
                sectionRect.setLeft(self.columnSpanSize(logicalIndex, 0, i))
            sectionRect.setSize(cellSize)

            # Check up span column or row
            colSpanIdx = self.columnSpanIndex(cellIndex)
            rowSpanIdx = self.rowSpanIndex(cellIndex)
            if colSpanIdx.isValid():
                colSpanFrom = colSpanIdx.column()
                if colSpanIdx.data(GridTableHeaderModel.ColumnSpanRole) is None:
                    colSpanCnt = 0
                else:
                    colSpanCnt = int(colSpanIdx.data(GridTableHeaderModel.ColumnSpanRole))
                colSpanTo = colSpanFrom + colSpanCnt - 1
                colSpan = self.columnSpanSize(cellIndex.row(), colSpanFrom, colSpanCnt)
                if self.orientation() == Qt.Horizontal:
                    sectionRect.setLeft(self.sectionViewportPosition(colSpanFrom))
                else:
                    sectionRect.setLeft(self.columnSpanSize(logicalIndex, 0, colSpanFrom))
                    i = colSpanTo

                sectionRect.setWidth(colSpan)

                # Check up if the column span index has row span
                subRowSpanData = colSpanIdx.data(GridTableHeaderModel.RowSpanRole)
                if subRowSpanData is not None:
                    subRowSpanFrom = colSpanIdx.row()
                    subRowSpanCnt = int(subRowSpanData)
                    subRowSpanTo = subRowSpanFrom + subRowSpanCnt - 1
                    subRowSpan = self.rowSpanSize(colSpanFrom, subRowSpanFrom, subRowSpanCnt)
                    if self.orientation() == Qt.Vertical:
                        sectionRect.setTop(self.sectionViewportPosition(subRowSpanFrom))
                    else:
                        sectionRect.setTop(self.rowSpanSize(colSpanFrom, 0, subRowSpanFrom))
                        i = subRowSpanTo
                    sectionRect.setHeight(subRowSpan)
                cellIndex = colSpanIdx
            if rowSpanIdx.isValid():
                rowSpanFrom = rowSpanIdx.row()
                if rowSpanIdx.data(GridTableHeaderModel.RowSpanRole) is None:
                    rowSpanCnt = 0
                else:
                    rowSpanCnt = int(rowSpanIdx.data(GridTableHeaderModel.RowSpanRole))
                rowSpanTo = rowSpanFrom + rowSpanCnt - 1
                rowSpan = self.rowSpanSize(cellIndex.column(), rowSpanFrom, rowSpanCnt)
                if self.orientation() == Qt.Vertical:
                    sectionRect.setTop(self.sectionViewportPosition(rowSpanFrom))
                else:
                    sectionRect.setTop(self.rowSpanSize(logicalIndex, 0, rowSpanFrom))
                    i = rowSpanTo
                sectionRect.setHeight(rowSpan)

                # Check up if the row span index has column span
                subColSpanData = rowSpanIdx.data(GridTableHeaderModel.ColumnSpanRole)
                if subColSpanData is not None:
                    subColSpanFrom = rowSpanIdx.column()
                    subColSpanCnt = int(subColSpanData)
                    subColSpanTo = subColSpanFrom + subColSpanCnt - 1
                    subColSpan = self.columnSpanSize(rowSpanFrom, subColSpanFrom, subColSpanCnt)
                    if self.orientation() == Qt.Horizontal:
                        sectionRect.setLeft(self.sectionViewportPosition(subColSpanFrom))
                    else:
                        sectionRect.setLeft(self.columnSpanSize(rowSpanFrom, 0, subColSpanFrom))
                        i = subColSpanTo
                    sectionRect.setWidth(subColSpan)
                cellIndex = rowSpanIdx

            # Draw section with style
            opt = QStyleOptionHeader()
            self.initStyleOption(opt)
            opt.textAlignment = Qt.AlignCenter
            opt.iconAlignment = Qt.AlignVCenter
            opt.section = logicalIndex
            if cellIndex.data(Qt.DisplayRole) is None:
                opt.text = ""
            else:
                opt.text = str(cellIndex.data(Qt.DisplayRole))
            opt.rect = sectionRect

            bg = cellIndex.data(Qt.BackgroundRole)
            fg = cellIndex.data(Qt.ForegroundRole)
            if bg is not None:
                tmp = opt.palette.brush(QPalette.Button)
                tmp.setColor(bg)
                opt.palette.setBrush(QPalette.Button, tmp)
                tmp = opt.palette.brush(QPalette.Window)
                tmp.setColor(bg)
                opt.palette.setBrush(QPalette.Window, tmp)
            if fg is not None:
                tmp = opt.palette.brush(QPalette.ButtonText)
                tmp.setColor(fg)
                opt.palette.setBrush(QPalette.ButtonText, tmp)

            painter.save()
            self.style().drawControl(QStyle.CE_Header, opt, painter, self)
            painter.restore()

            i = i + 1

    def sectionSizeFromContents(self, logicalIndex):
        tblModel = self.model()
        if self.orientation() == Qt.Horizontal:
            level = tblModel.rowCount()
        else:
            level = tblModel.columnCount()

        size = super().sectionSizeFromContents(logicalIndex)
        i = 0
        while i < level:
            if self.orientation() == Qt.Horizontal:
                cellIndex = tblModel.index(i, logicalIndex)
            else:
                cellIndex = tblModel.index(logicalIndex, i)
            colSpanIdx = self.columnSpanIndex(cellIndex)
            rowSpanIdx = self.rowSpanIndex(cellIndex)
            size = cellIndex.data(Qt.SizeHintRole)

            if colSpanIdx.isValid():
                colSpanFrom = colSpanIdx.column()
                if colSpanIdx.data(GridTableHeaderModel.ColumnSpanRole) is None:
                    colSpanCnt = 0
                else:
                    colSpanCnt = int(colSpanIdx.data(GridTableHeaderModel.ColumnSpanRole))
                colSpanTo = colSpanFrom + colSpanCnt - 1
                size.setWidth(self.columnSpanSize(colSpanIdx.row(), colSpanFrom, colSpanCnt))
                if self.orientation() == Qt.Vertical:
                    i = colSpanTo
            if rowSpanIdx.isValid():
                rowSpanFrom = rowSpanIdx.row()
                if rowSpanIdx.data(GridTableHeaderModel.RowSpanRole) is None:
                    rowSpanCnt = 0
                else:
                    rowSpanCnt = int(rowSpanIdx.data(GridTableHeaderModel.RowSpanRole))
                rowSpanTo = rowSpanFrom + rowSpanCnt - 1
                size.setHeight(self.rowSpanSize(rowSpanIdx.column(), rowSpanFrom, rowSpanCnt))
                if self.orientation() == Qt.Horizontal:
                    i = rowSpanTo
            i = i + 1
        return size

    def setRowHeight(self, row, height):
        m = self.model()
        cols = m.columnCount()
        for col in range(cols):
            sz = m.index(row, col).data(Qt.SizeHintRole)
            sz.setHeight(height)
            m.setData(m.index(row, col), sz, Qt.SizeHintRole)
        if self.orientation() == Qt.Vertical:
            self.resizeSection(row, height)

    def setColumnWidth(self, col, width):
        m = self.model()
        rows = m.rowCount()
        for row in range(rows):
            sz = m.index(row, col).data(Qt.SizeHintRole)
            sz.setWidth(width)
            m.setData(m.index(row, col), sz, Qt.SizeHintRole)
        if self.orientation() == Qt.Horizontal:
            self.resizeSection(col, width)

    def setSpan(self, row, column, rowSpanCount=None, columnSpanCount=None):
        if rowSpanCount is None or columnSpanCount is None:
            if self.orientation() == Qt.Horizontal:
                    rowSpanCount = self.model().rowCount()
                    columnSpanCount = 1
            else:
                    rowSpanCount = 1
                    columnSpanCount = self.model().columnCount()

        md = self.model()
        idx = md.index(row, column)
        if rowSpanCount > 0:
            md.setData(idx, rowSpanCount, GridTableHeaderModel.RowSpanRole)
        if columnSpanCount > 0:
            md.setData(idx, columnSpanCount, GridTableHeaderModel.ColumnSpanRole)

    def columnSpanIndex(self, index):
        tblModel = self.model()
        curRow = index.row()
        curCol = index.column()
        i = curCol
        while i >= 0:
            spanIndex = tblModel.index(curRow, i)
            span = spanIndex.data(GridTableHeaderModel.ColumnSpanRole)
            if span is not None:
                if spanIndex.column() + int(span) - 1 >= curCol:
                    return spanIndex
            i = i - 1
        return QModelIndex()

    def rowSpanIndex(self, index):
        tblModel = self.model()
        curRow = index.row()
        curCol = index.column()
        i = curRow
        while i >= 0:
            spanIndex = tblModel.index(i, curCol)
            span = spanIndex.data(GridTableHeaderModel.RowSpanRole)
            if span is not None:
                if spanIndex.row() + int(span) - 1 >= curRow:
                    return spanIndex
            i = i - 1
        return QModelIndex()

    def columnSpanSize(self, row, _from, spanCount):
        tblModel = self.model()
        span = 0
        for i in range(_from, _from + spanCount):
            cellSize = tblModel.index(row, i).data(Qt.SizeHintRole)
            if cellSize is not None:
                span += cellSize.width()
        return span

    def rowSpanSize(self, column, _from, spanCount):
        tblModel = self.model()
        span = 0
        for i in range(_from, _from + spanCount):
            cellSize = tblModel.index(i, column).data(Qt.SizeHintRole)
            if cellSize is not None:
                span += cellSize.height()
        return span

    def getSectionRange(self, index, beginSection, endSection):
        colSpanIdx = self.columnSpanIndex(index)
        rowSpanIdx = self.rowSpanIndex(index)

        if colSpanIdx.isValid():
            colSpanFrom = colSpanIdx.column()
            if colSpanIdx.data(GridTableHeaderModel.ColumnSpanRole) is None:
                colSpanCnt = 0
            else:
                colSpanCnt = int(colSpanIdx.data(GridTableHeaderModel.ColumnSpanRole))

            colSpanTo = colSpanFrom + colSpanCnt - 1
            if self.orientation() == Qt.Horizontal:
                beginSection = colSpanFrom
                endSection = colSpanTo
                index = colSpanIdx
                return [colSpanCnt, beginSection, endSection]
            else:
                subRowSpanData = colSpanIdx.data(GridTableHeaderModel.RowSpanRole)
                if subRowSpanData is not None:
                    subRowSpanFrom = colSpanIdx.row()
                    subRowSpanCnt = int(subRowSpanData)
                    subRowSpanTo = subRowSpanFrom + subRowSpanCnt - 1
                    beginSection = subRowSpanFrom
                    endSection = subRowSpanTo
                    index = colSpanIdx
                    return [subRowSpanCnt, beginSection, endSection]

        if rowSpanIdx.isValid():
            rowSpanFrom = rowSpanIdx.row()
            if rowSpanIdx.data(GridTableHeaderModel.RowSpanRole) is None:
                rowSpanCnt = 0
            else:
                rowSpanCnt = int(rowSpanIdx.data(GridTableHeaderModel.RowSpanRole))
            rowSpanTo = rowSpanFrom + rowSpanCnt - 1
            if self.orientation() == Qt.Vertical:
                beginSection = rowSpanFrom
                endSection = rowSpanTo
                index = rowSpanIdx
                return [rowSpanCnt, beginSection, endSection]
            else:
                subColSpanData = rowSpanIdx.data(GridTableHeaderModel.ColumnSpanRole)
                if subColSpanData is not None:
                    subColSpanFrom = rowSpanIdx.column()
                    subColSpanCnt = int(subColSpanData)
                    subColSpanTo = subColSpanFrom + subColSpanCnt - 1
                    beginSection = subColSpanFrom
                    endSection = subColSpanTo
                    index = rowSpanIdx
                    return [subColSpanCnt, beginSection, endSection]

        return [0, beginSection, endSection]

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        index = self.indexAt(event.pos())

        if index.isValid():
            if self.orientation() == Qt.Horizontal:
                beginSection = index.column()
            else:
                beginSection = index.row()
            endSection = beginSection
            [cnt, beginSection, endSection] = self.getSectionRange(index, beginSection, endSection)
            self.sectionPressed.emit(beginSection, endSection)

    def onSectionResized(self, logicalIndex, oldSize, newSize):
        tblModel = self.model()
        if self.orientation() == Qt.Horizontal:
            level = tblModel.rowCount()
        else:
            level = tblModel.columnCount()
        pos = self.sectionViewportPosition(logicalIndex)
        if self.orientation() == Qt.Horizontal:
            xx = pos
            yy = 0
        else:
            xx = 0
            yy = pos
        sectionRect = QRect(xx, yy, 0, 0)
        for i in range(level):
            if self.orientation() == Qt.Horizontal:
                cellIndex = tblModel.index(i, logicalIndex)
            else:
                cellIndex = tblModel.index(logicalIndex, i)
            cellSize = cellIndex.data(Qt.SizeHintRole)
            # Set position of cell
            if self.orientation() == Qt.Horizontal:
                sectionRect.setTop(self.rowSpanSize(logicalIndex, 0, i))
                cellSize.setWidth(newSize)
            else:
                sectionRect.setLeft(self.columnSpanSize(logicalIndex, 0, i))
                cellSize.setHeight(newSize)
            tblModel.setData(cellIndex, cellSize, Qt.SizeHintRole)

            colSpanIdx = self.columnSpanIndex(cellIndex)
            rowSpanIdx = self.rowSpanIndex(cellIndex)

            if colSpanIdx.isValid():
                colSpanFrom = colSpanIdx.column()
                if self.orientation() == Qt.Horizontal:
                    sectionRect.setLeft(self.sectionViewportPosition(colSpanFrom))
                else:
                    sectionRect.setLeft(self.columnSpanSize(logicalIndex, 0, colSpanFrom))
            if rowSpanIdx.isValid():
                rowSpanFrom = rowSpanIdx.row()
                if self.orientation() == Qt.Vertical:
                    sectionRect.setTop(self.sectionViewportPosition(rowSpanFrom))
                else:
                    sectionRect.setTop(self.rowSpanSize(logicalIndex, 0, rowSpanFrom))
            rToUpdate = QRect(sectionRect)
            rToUpdate.setWidth(self.viewport().width() - sectionRect.left())
            rToUpdate.setHeight(self.viewport().height() - sectionRect.top())
            self.viewport().update(rToUpdate.normalized())

