import functools
import copy
from dateutil.relativedelta import relativedelta
from datetime import date
from itertools import groupby
from sqlalchemy.sql import extract, asc
from sqlalchemy.orm.session import make_transient
from . import database
from .models import Gasto
from .helpers import shouldInclude

class GastoService():

    def save(self, gasto_form):
        gasto = Gasto()
        gasto_form.populate_obj(gasto)
        if gasto.parcelado:
            parcelas = int(gasto.parcelas)
            quando = gasto.quando
            for parcela in range(1, parcelas + 1):
                gasto = copy.deepcopy(gasto)
                gasto.parcela_repr = f'({parcela}/{parcelas})'
                gasto.quando = quando + relativedelta(months = parcela - 1)
                database.session.add(gasto)
            database.session.commit()
        else:
            database.session.add(gasto)
            database.session.commit()

    def update(self, gastoForm, id):
        gasto = self.find(id)
        gastoForm.populate_obj(gasto)
        self.save(gasto)

    def list_totals_by_year(self, year):
        all_months = {}
        all_by_year = self.group_by_month(self.all_non_recurrent_by_year(year))
        all_recorrentes = self.all_recorrentes()
        for month in range(1, 13):
            recorrentes = self.recorrentes_filtered_by(month, year, all_recorrentes)
            all_monthly = all_by_year.get(month, [])
            all_monthly = self.remove_duplicates(all_monthly, recorrentes)
            totals = list(map(lambda gasto: gasto.quanto, all_monthly))
            total = functools.reduce(lambda x,y: x+y , totals, 0)
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
        return self.remove_duplicates(all_monthly, recurrents)

    def remove_duplicates(self, all_monthly, recorrentes):
        recorrentes_ids = list(map(lambda g: g.gasto_recorrente_id, all_monthly))
        for recorrente in recorrentes:
            if (recorrente.id not in recorrentes_ids):
                all_monthly.append(recorrente)
        return all_monthly

    def find(self, id):
        return database.session.get(Gasto, id)

    def add_to_month(self, id, month):
        gasto = self.find(id)
        if gasto:
            make_transient(gasto)
            gasto.gasto_recorrente_id = gasto.id
            gasto.id = None
            gasto.recorrente = False
            gasto.parcelas = 0
            gasto.quando = gasto.quando.replace(month=month)
            database.session.add(gasto)
            database.session.commit()
            return gasto
        return None


