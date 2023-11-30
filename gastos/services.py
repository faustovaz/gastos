from dateutil.relativedelta import relativedelta
from datetime import date
import functools
from itertools import groupby
from sqlalchemy.sql import extract, asc
from . import database
from .models import Gasto
from .helpers import shouldInclude

class GastoService():

    def save_form(self, gastoForm):
        gasto = Gasto()
        gastoForm.populate_obj(gasto)
        self.save(gasto)

    def update(self, gastoForm, id):
        gasto = self.find(id)
        gastoForm.populate_obj(gasto)
        self.save(gasto)

    def save(self, gasto):
        if (gasto.parcelado):
            parcelas = int(gasto.parcelas)
            for parcela in range(1, parcelas + 1):
                gasto.parcela_repr = f'({parcela}/{parcelas})'
                gasto.quando = gasto.quando + relativedelta(months = parcela - 1)
                database.session.add(gasto)
            database.session.commit()
        else:
            database.session.add(gasto)
            database.session.commit()

    def list_by_year(self, year):
        all_mensais = self.all_by_year(year)
        recorrentes = self.all_recorrentes()
        all_months = {}
        for month in range(1, 13):
            totals = list(map(lambda gasto: gasto.quanto, all_mensais.get(month, [])))
            recorrentes = self.all_recorrentes_starting_from(month, year)
            totals = totals + list(map(lambda gasto: gasto.quanto, recorrentes))
            total = functools.reduce(lambda x,y: x+y, totals, 0)
            all_months.update({month: total})
        all_months.update({year: year})
        return all_months

    def all_by_year(self, year):
        gastos = database \
                    .session \
                    .query(Gasto) \
                    .filter(extract('year', Gasto.quando) == year) \
                    .all()
        return {month: list(g) for month, g in groupby(gastos, lambda gasto: gasto.quando.month)}

    def all_recorrentes(self):
        return database.session.query(Gasto).filter(Gasto.recorrente == True).all()

    def all_recorrentes_starting_from(self, month, year):
        return list(filter(lambda g: shouldInclude(g.quando, date(year, month, 1)), \
                           self.all_recorrentes()))

    def all_by_month_and_year(self, month, year):
        return database \
                .session \
                .query(Gasto) \
                .filter(extract('month', Gasto.quando) == month) \
                .filter(extract('year', Gasto.quando) == year) \
                .order_by(asc(Gasto.quanto)) \
                .all()

    def find(self, id):
        return database \
                .session \
                .get(Gasto, id)

