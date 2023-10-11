from datetime import date

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
                    "link": f"{month_number}_{year}"
                 })

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

