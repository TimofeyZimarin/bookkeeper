from PySide6 import QtWidgets


class BudgetView(QtWidgets.QTableWidget):
    """
            Визуализация таблицы бюджета
    """
    def __init__(self) -> None:
        super().__init__()
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setColumnCount(2)
        self.setRowCount(3)
        self.setHorizontalHeaderLabels(
            "Cумма Бюджет".split())
        self.setVerticalHeaderLabels("День Неделя Месяц".split())
        self.header = self.horizontalHeader()
        self.header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.Stretch)
        self.header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.Stretch)
        self.header.setSectionResizeMode(
            2, QtWidgets.QHeaderView.Stretch)