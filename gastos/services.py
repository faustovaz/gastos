from dateutil.relativedelta import relativedelta
from datetime import date
import functools
from itertools import groupby
from sqlalchemy.sql import extract, asc
from . import database
from .models import GastoMensal, GastoRecorrente
from .helpers import shouldInclude

class GastoService():

    def save_form(self, gastoForm):
        gasto = GastoMensal()
        gastoForm.populate_obj(gasto)
        self.save(gasto)
    
    def update(self, gastoForm, id):
        gasto = self.find_by_id(id)
        gastoForm.populate_obj(gasto)
        self.save(gasto)
                
    def save(self, gasto):
        if (gasto.parcelado):
            self._saveGastoParcelado(gasto)
        elif (gasto.recorrente):
            self._saveGastoRecorrente(gasto)
        else:
            self._saveGastoMensal(gasto)

    def _saveGastoMensal(self, gasto):
        database.session.add(gasto)
        database.session.commit()

    def _saveGastoParcelado(self, gasto):
        parcelas = int(gasto.parcelas)
        for parcela in range(1, parcelas + 1):
            gasto.parcela_repr = f'({parcela}/{parcelas})'
            gasto.quando = gasto.quando + relativedelta(months = parcela - 1)
            database.session.add(gasto)
        database.session.commit()

    def _saveGastoRecorrente(self, gasto):
        gastoRecorrente = GastoRecorrente.of(gasto)
        database.session.add(gastoRecorrente)
        database.session.commit()
    
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

    def all_recorrentes_starting_from(self, month, year):
        return list(filter(lambda g: shouldInclude(g.quando, date(year, month, 1)), self.all_recorrentes()))

    def all_by_month_and_year(self, month, year):
        return database \
                .session \
                .query(GastoMensal) \
                .filter(extract('month', GastoMensal.quando) == month) \
                .filter(extract('year', GastoMensal.quando) == year) \
                .order_by(asc(GastoMensal.quanto)) \
                .all()

    def find_by_id(self, id):
        return database \
                .session \
                .get(GastoMensal, id)

