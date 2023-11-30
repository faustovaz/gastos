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

    def list_totals_by_year(self, year):
        all_months = {}
        all_mensais = self.group_by_month(self.all_non_recurrent_by_year(year))
        all_recorrentes = self.all_recorrentes()
        for month in range(1, 13):
            recorrentes = self.recorrentes_filtered_by(month, year, all_recorrentes)
            totais_mensal = list(map(lambda gasto: gasto.quanto, all_mensais.get(month, [])))
            totais_recorrentes = list(map(lambda gasto: gasto.quanto, recorrentes))
            totais = totais_mensal + totais_recorrentes
            total = functools.reduce(lambda x,y: x+y , totais, 0)
            all_months.update({month: total})
        all_months.update({year: year})
        return all_months

    def group_by_month(self, gastos):
        return {month: list(g) for month, g in groupby(gastos, lambda gasto: gasto.quando.month)}

    def all_non_recurrent_by_year(self, year):
        return database \
                .session \
                .query(Gasto) \
                .filter(extract('year', Gasto.quando) == year) \
                .filter(Gasto.recorrente == False) \
                .all()

    def all_non_recurrent_by_month(self, month, year):
        return database \
                .session \
                .query(Gasto) \
                .filter(extract('month', Gasto.quando) == month) \
                .filter(extract('year', Gasto.quando) == year) \
                .filter(Gasto.recorrente == False) \
                .order_by(asc(Gasto.quanto)) \
                .all()

    def all_recorrentes(self):
        return database \
                .session \
                .query(Gasto) \
                .filter(Gasto.recorrente == True) \
                .all()

    def recorrentes_filtered_by(self, month, year, recorrentes):
        return list(filter(lambda g: shouldInclude(g.quando, date(year, month, 1)), recorrentes))

    def all_by_month_and_year(self, month, year):
        all_monthly = self.all_non_recurrent_by_month(month, year)
        recurrents = self.recorrentes_filtered_by(month, year, self.all_recorrentes())
        return all_monthly + recurrents

    def find(self, id):
        return database.session.get(Gasto, id)

