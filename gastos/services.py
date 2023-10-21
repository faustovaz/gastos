from dateutil.relativedelta import relativedelta
from datetime import date
import functools
from itertools import groupby
from sqlalchemy.sql import extract, desc
from . import database
from .models import GastoMensal, GastoRecorrente
from .helpers import shouldInclude

class GastoService():

    def __init__(self, gastoForm=None):
        self.gastoForm = gastoForm

    def isParcelado(self):
        return self.gastoForm.parcelado.data

    def isRecorrente(self):
        return self.gastoForm.recorrente.data

    def save(self):
        if self.isParcelado():
            self._saveGastoParcelado()
        elif self.isRecorrente():
            self._saveGastoRecorrente()
        else:
            self._saveGastoMensal()

    def list_by_year(self, year):
        all_mensais = self.all_mensais_by_year(year)
        recorrentes = self.all_recorrentes()
        all_months = {}
        for month in range(1, 13):
            totals = list(map(lambda gasto: gasto.quanto, all_mensais.get(month, [])))
            filtered_recorrentes = list(filter( \
                            lambda g: shouldInclude(g.quando, date(year, month, 1)), recorrentes))
            totals = totals + list(map(lambda gasto: gasto.quanto, filtered_recorrentes))
            total = functools.reduce(lambda x,y: x+y, totals, 0)
            all_months.update({month: total})
        all_months.update({year: year})
        return all_months
    
    def all_mensais_by_year(self, year):
        gastos = database \
                    .session \
                    .query(GastoMensal) \
                    .filter(extract('year', GastoMensal.quando) == year) \
                    .all()
        return {month: list(g) for month, g in groupby(gastos, lambda gasto: gasto.quando.month)}

    def all_recorrentes(self):
        return database \
                .session \
                .query(GastoRecorrente) \
                .all()

    def all_by_month_and_year(self, month, year):
        return database \
                .session \
                .query(GastoMensal) \
                .filter(extract('month', GastoMensal.quando) == month) \
                .filter(extract('year', GastoMensal.quando) == year) \
                .order_by(desc(GastoMensal.quanto)) \
                .all()

    def _saveGastoMensal(self):
        gasto = GastoMensal()
        self.gastoForm.populate_obj(gasto)
        database.session.add(gasto)
        database.session.commit()

    def _saveGastoParcelado(self):
        parcelas = int(self.gastoForm.parcelas.data)
        for parcela in range(1, parcelas + 1):
            gasto = GastoMensal()
            self.gastoForm.populate_obj(gasto)
            gasto.parcela_repr = f'({parcela}/{parcelas})'
            gasto.quando = gasto.quando + relativedelta(months = parcela - 1)
            database.session.add(gasto)
        database.session.commit()

    def _saveGastoRecorrente(self):
        gasto = GastoRecorrente()
        self.gastoForm.populate_obj(gasto)
        database.session.add(gasto)
        database.session.commit()

