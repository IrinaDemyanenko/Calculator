"""This is an application for counting spendings or calories."""

import datetime as dt
from typing import Union

Format = '%d.%m.%Y'
today = dt.date.today()   # модуль, класс, метод
formated_today = today.strftime(Format)


class Record:
    """To create expense records."""
    def __init__(
            self, amount: float, comment: str,
            date: str = formated_today) -> None:
        """Parameters:
        amount: Cash or calories amount.
        comment: What has been eaten/spend.
        date: Date when the spend took place (default today),
              Date format: "day.month.year".
        """
        self.amount = amount
        self.comment = comment
        self.date = date

    def __str__(self) -> str:
        """Represents record to a string."""
        return (f'Amount: {self.amount}, comment: {self.comment}, '
                f'date: {self.date}.')


class Calculator:
    """Parent class.
    It is able to keep records and sum records for specific date.
    """
    def __init__(self, limit: Union[int, float]) -> None:
        """Get amount and the reason what for.

        Args:
        limit: Cash amount or calories limit.
        """
        self.limit = limit
        self.records: list[Record] = []

    def add_record(self, new_record: Record) -> None:
        """Adds new record to calculator`s list.

        Args:
        new_record: Spend record.
        """
        self.records.append(new_record)

    def get_today_stats(self) -> Union[float, int]:
        """Gives today`s spend result at a particular moment.

        return: Amount of the money/calories spent.
        """
        sum_spent: Union[int, float] = 0
        for elem in self.records:
            if elem.date == formated_today:
                sum_spent += elem.amount
        return sum_spent

    def get_week_stats(self) -> Union[int, float]:
        """Gives week`s spend result.

        return: Amount of the money/calories spent
        over the last 7 days.
        """
        sum_spent_week: Union[int, float] = 0
        numdays = 7
        dateList_unform = [
            dt.date.today() - dt.timedelta(days=x) for x in range(numdays)
            ]
        dateList = [elem.strftime(Format) for elem in dateList_unform]
        # отформатированные даты используем для перебора дат в записях
        # списка self.records, значения amount для каждой даты суммируем в
        # переменной sum_spent_week
        for elem in dateList:
            for rec in self.records:
                if elem == rec.date:  # если даты совпадают
                    sum_spent_week += rec.amount
        return sum_spent_week

    def get_today_limit(self) -> Union[int, float]:
        """Counts how much money/calories is left for the day.

        return: Amount of the money/calories left.
        """
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):
    """Successor class to the Calculator class."""

    def get_calories_remained(self) -> str:
        """Gives nutritional advice.

        return: Daily calorie intake recommendations.
        """
        calories_limit: Union[int, float] = self.get_today_limit()
        if self.limit > self.get_today_stats():
            return (f'Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {calories_limit} кКал.')
        else:
            return ('Хватит есть!')


class CashCalculator(Calculator):
    """Successor class to the Calculator class."""

    USD_rate: float = 90.1
    EUR_rate: float = 98.2
    RUR_rate: float = 1.0

    def get_today_cash_remained(self, currency: str) -> str:
        """Gives advice on spending.

        Args:
        currency: Settlements are made in three currencies:
        roubles - "rub", euro - "eur", dollars - "usd".
        return: Spending guidelines for today.
        """

        cash: dict[str, tuple[str, float]] = {
            'rub': ('руб', self.RUR_rate),
            'eur': ('Euro', self.EUR_rate),
            'usd': ('USD', self.USD_rate)
            }

        if currency not in cash:
            return ('Выбрано неверное значение валюты. Доступные '
                    'значения: руб, eur, usd.')

        currency_name, currency_rate = cash[currency]

        currency_limit = self.get_today_limit()

        cash_today = abs(currency_limit) / currency_rate

        if cash_today == 0:
            return 'Денег нет, держись!'
        elif cash_today > 0:
            return f'На сегодня осталось {cash_today:.2f} {currency_name}.'
        else:
            return (f'Денег нет, держись: твой долг - {cash_today:.2f} '
                    f'{currency_name}.')


if __name__ == "__main__":
    limit = 1000
    cash_calculator = CashCalculator(limit)
    calories_calculator = CaloriesCalculator(limit)

    # записи для денег
    r1 = Record(amount=145, comment='кофе')
    r2 = Record(amount=300, comment='Серёге за обед')
    r3 = Record(
        amount=3000,
        comment='Бар на Танин день рождения',
        date='08.11.2022')

    # записи для калорий
    r4 = Record(
        amount=118,
        comment='Кусок тортика. И ещё один.')
    r5 = Record(
        amount=84,
        comment='Йогурт.')
    r6 = Record(
        amount=1140,
        comment='Баночка чипсов.',
        date='24.02.2019')

    cash_calculator.add_record(r1)
    cash_calculator.add_record(r2)
    cash_calculator.add_record(r3)

    calories_calculator.add_record(r4)
    calories_calculator.add_record(r5)
    calories_calculator.add_record(r6)

    # вывод результатов
    print(cash_calculator.get_today_cash_remained('rub'))
    print(calories_calculator.get_calories_remained())
