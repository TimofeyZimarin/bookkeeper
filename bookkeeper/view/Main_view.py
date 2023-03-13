from PySide6 import QtWidgets
from Budget_view import BudgetView
from Expenses_view import ExpensesView


import sys
from PySide6 import QtWidgets


from bookkeeper.models.expense import Expense


class MainWindow(QtWidgets.QWidget):
    """
        Визуализация главного окна
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("The Bookkeeper App")
        self.vbox = QtWidgets.QVBoxLayout()

        self.expenses_label = QtWidgets.QLabel("Последние расходы")
        self.expenses_view = ExpensesView
        self.budget_view = BudgetView

        self.vbox.addWidget(self.expenses_label)
        self.vbox.addWidget(self.expenses_view)
        self.vbox.addWidget(self.budget_view)

        self.exp_modifier = None
        self.cat_adder = None
        self.cats = None

        self.box = QtWidgets.QVBoxLayout()
        self.addButton = QtWidgets.QPushButton("Добавить")
        self.box.addWidget(self.addButton)

        self.resize(1000, 1000)
        self.setLayout(self.box)
        self.show()

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())