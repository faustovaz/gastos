from dateutil.relativedelta import relativedelta
from . import database
from .models import GastoMensal, GastoRecorrente
from sqlalchemy.sql import extract
from itertools import groupby
import functools

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
        all_recorrentes = self.all_recorrentes()
        all_months = {}
        for month in range(1, 13):
            values = list(map(lambda gasto: gasto.quanto, all_mensais.get(month, [])))
            values = values + list(map(lambda gasto: gasto.quanto, all_recorrentes))
            total = functools.reduce(lambda x,y: x+y, values, 0)
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

