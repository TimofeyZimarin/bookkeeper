from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.models.expense import Expense
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class Budget:
    """
    Бюджет.
    summ_day - сумма расходов за день
    summ_week - сумма расходов за неделю
    summ_month - сумма расходов за месяц
    per - период
    lim - лимит расходов
    cat - id категории расходов
    pk - id записи в базе данных
    """
    summ_day: int
    summ_week: int
    summ_month: int
    per: ["day", "week", "month"]
    lim: int | None = None
    cat: int | None = None
    pk: int = 0

    def get_summ(self, expense_repo: AbstractRepository[Expense]) -> None:

        date = datetime.now()

        for x in self.per:
            if x == "day":
                per_expenses = expense_repo.get_all(where={"expense_date": date.strftime('%Y-%m-%d')})

            if x == "week":
                for i in range(date.weekday() + 1):
                    week = date - timedelta(days=i)
                    week_expenses = expense_repo.get_all(where={"expense_date": week.strftime('%Y-%m-%d')})

            if x == "week":
                for i in range(date.day):
                    month = date - timedelta(days=i)
                    month_expenses = expense_repo.get_all(where={"expense_date": month.strftime('%Y-%m-%d')})

        self.summ_day = sum([expenses.amount for expenses in per_expenses])
        self.summ_week = sum([expenses.amount for expenses in week_expenses])
        self.summ_month = sum([expenses.amount for expenses in month_expenses])