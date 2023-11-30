import functools
from datetime import date

def months():
    return {
        1: "Janeiro",
        2: "Fevereiro",
        3: "Março",
        4: "Abril",
        5: "Maio",
        6: "Junho",
        7: "Julho",
        8: "Agosto",
        9: "Setembro",
        10: "Outubro",
        11: "Novembro",
        12: "Dezembro"
    }


def shouldInclude(date1, date2):
    first_date = date(date1.year, date1.month, 1)
    second_date = date(date2.year, date2.month, 1)
    return first_date <= second_date


class GastosMensaisView:
    def __init__(self, year, values):
        self.year = year
        self.values = values
        self.grid = []
        for month_number, month in months().items():
            self.grid.append(
                {   "month_name": month,
                    "key": month_number,
                    "total": values.get(month_number, 0),
                    "link": f"{month_number}/{year}"
                 })


class GastoMensalView:
    def __init__(self, month, year, values):
        self.month = month
        self.year = year
        self.values = values
        self.month_desc = months().get(int(month))

    def all(self):
        return self.values

    def total(self):
        gastos = map(lambda g: g.quanto, self.all())
        return functools.reduce(lambda x,y: x + y, gastos, 0)

    def link_to_month(self):
        return f"/monthly/{self.month}/{self.year}"

    def link_to_year(self):
        return f"/monthly/{self.year}"

