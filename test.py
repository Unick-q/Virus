from PyQt5 import QtWidgets, QtCore, QtGui
import sys
from PyQt5.QtCore import QModelIndex, Qt
import numpy as np

class MyTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data=[[]], parent=None):
        super().__init__(parent)
        self.data = data

    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        if role == QtCore.Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return "Column " + str(section)
            else:
                return "Row " + str(section)

    def columnCount(self, parent=None):
        return len(self.data[0])

    def rowCount(self, parent=None):
        return len(self.data)

    def data(self, index: QModelIndex, role: int):
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            col = index.column()
            return str(self.data[row][col])


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    data = [[11, 12, 13, 14, 15],
            [21, 22, 23, 24, 25],
            [31, 32, 33, 34, 35]]

    # data = np.random.random((10000, 100)) * 100

    model = MyTableModel(data)
    view = QtWidgets.QTableView()
    view.setModel(model)

    view.show()

    sys.exit(app.exec_())