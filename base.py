from PyQt6 import QtGui, QtCore, QtWidgets

class Base():
    def create_table(self, table, headers,  data):
        table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        model = QtGui.QStandardItemModel()
        model.clear()
        model.setHorizontalHeaderLabels(headers)
        for item in data:
            row = [QtGui.QStandardItem(str(item[i] if item[i] is not None else "")) for i in range(len(item))]
            model.appendRow(row)
        table.setModel(model)
        table.resizeColumnsToContents()
        table.hideColumn(0)

    def selected_table_data(self, table):
        selected = table.selectionModel().selectedRows()
        index = selected[0]
        model = table.model()
        return model.data(model.index(index.row(), 0))