import functools
import copy
from dateutil.relativedelta import relativedelta
from datetime import date
from itertools import groupby
from sqlalchemy.sql import extract, asc
from sqlalchemy.orm.session import make_transient
from werkzeug.security import generate_password_hash
from . import database
from .models import Gasto, User, Settings
from .helpers import shouldInclude

class GastoService():

    def __init__(self, current_user):
        self.current_user = current_user

    def save(self, gasto_form):
        gasto = Gasto()
        gasto_form.populate_obj(gasto)
        gasto.usuario_id = self.current_user.id
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

    def update(self, gasto_form, id):
        gasto = self.find(id)
        if gasto.belongs_to(self.current_user):
            gasto_form.populate_obj(gasto)
            database.session.add(gasto)
            database.session.commit()

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
        filters = self.__filters(extract('year', Gasto.quando) == year, \
                                    Gasto.recorrente == False)
        return database \
                .session \
                .query(Gasto) \
                .filter(*filters) \
                .all()

    def all_non_recurrent_by_month(self, month, year):
        filters = self.__filters(extract('month', Gasto.quando) == month, \
                                    extract('year', Gasto.quando) == year, \
                                    Gasto.recorrente == False)
        return database \
                .session \
                .query(Gasto) \
                .filter(*filters) \
                .order_by(asc(Gasto.quanto)) \
                .all()

    def all_recorrentes(self):
        filters = self.__filters(Gasto.recorrente == True)
        return database \
                .session \
                .query(Gasto) \
                .filter(*filters) \
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

    def delete(self, id):
        gasto = self.find(id)
        if gasto and gasto.usuario_id == self.current_user.id:
            database.session.delete(gasto)
            database.session.commit()

    def __filters(self, *filters):
        filter_to_apply = list(filters)
        if (self.current_user.settings.show_only_my_expenses):
            filter_to_apply.append(Gasto.usuario_id == self.current_user.id)
        return filter_to_apply


class UserService():
    
    def __init__(self, current_user):
        self.current_user = current_user
    
    def update(self, user_form):
        user = database.session.get(User, self.current_user.id)
        user_form.populate_obj(user)
        user.password = generate_password_hash(user.password, method='scrypt')
        database.session.add(user)
        database.session.commit()


class SettingsService():
    
    def __init__(self, current_user):
        self.current_user = current_user

    def update(self, settings_form):
        settings = Settings.query.filter_by(user_id=self.current_user.id).first()
        settings_form.populate_obj(settings)
        database.session.add(settings)
        database.session.commit()