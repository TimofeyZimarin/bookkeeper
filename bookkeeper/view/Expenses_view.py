from PySide6 import QtWidgets


class ExpensesView(QtWidgets.QTableWidget):
    """
            Визуализация таблицы расходов
    """
    def __init__(self) -> None:
        super().__init__()
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setColumnCount(4)
        self.setRowCount(20)
        self.setHorizontalHeaderLabels(
            "Дата Сумма Категория Комментарий".split())
        self.header = self.horizontalHeader()
        self.header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(
            3, QtWidgets.QHeaderView.Stretch)

