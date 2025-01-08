import json
from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from functools import reduce
from datetime import date
from .forms import GastoForm, UserForm, SettingsForm
from .services import GastoService, UserService, SettingsService
from .helpers import GastosMensaisView, GastoMensalView

views = Blueprint('views', __name__)

@views.route("/add", methods=['GET', 'POST'])
@login_required
def save():
    gastoForm = GastoForm()
    if gastoForm.validate_on_submit():
        gastoService = GastoService(current_user)
        gastoService.save(gastoForm)
        flash('Gasto adicionado com sucesso!', category='success')
        return redirect(url_for('views.save'))
    return render_template("add.html", form=gastoForm)

@views.route("/edit/<int:id>", methods=['GET', 'POST'])
@login_required
def edit(id):
    gastoService = GastoService(current_user)
    gasto_form = GastoForm()
    args = request.args
    gasto = gastoService.find(id)
    if gasto:
        if request.method == 'GET':
            gasto_form = GastoForm(obj=gasto)
        if gasto_form.validate_on_submit():
            gastoService.update(gasto_form, id)
            flash("Gasto atualizado com sucesso!", category="success")
    return render_template("edit.html", \
                            action=f"{gasto.to_edit()}", \
                            form=gasto_form, \
                            current_user=current_user, \
                            disable_save=not gasto.belongs_to(current_user))

@views.route("/delete/<int:id>", methods=['DELETE'])
@login_required
def delete(id):
    service = GastoService(current_user)
    service.delete(id)
    return jsonify({}) 

@views.route("/")
@views.route("/monthly/")
@views.route("/monthly/<int:year>")
@login_required
def monthly(year=None):
    year = year if year else date.today().year
    gastoService = GastoService(current_user)
    all = gastoService.list_totals_by_year(year)
    return render_template("gastos_mensais.html", \
                            gastosMensaisView=GastosMensaisView(year, all))

@views.route("/monthly/<int:month>/<int:year>")
@login_required
def view_monthly(month, year):
    gastoService = GastoService(current_user)
    gastos = gastoService.all_by_month_and_year(month, year)
    return render_template("view_gasto_mensal.html", \
                        gastoMensalView=GastoMensalView(month, year, gastos))

@views.route("/recurrent")
@login_required
def recurrent():
    gastoService = GastoService(current_user)
    recorrentes = gastoService.all_recorrentes()
    total = reduce(lambda acc, gasto: acc + gasto.quanto, recorrentes, 0)
    return render_template("gastos_recorrentes.html", \
                            gastos=recorrentes, \
                            total=total, \
                            current_user=current_user)

@views.route("/add_to_month", methods = ['POST'])
@login_required
def add_to_month():
    service = GastoService(current_user)
    data = json.loads(request.data)
    gasto = service.add_to_month(data['gasto_id'], data['month'], data['year'])
    if gasto:
        return jsonify({})

@views.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    user_form = UserForm()
    if request.method == 'GET':
        user_form = UserForm(obj=current_user)
    if user_form.validate_on_submit():
        user_service = UserService(current_user)
        user_service.update(user_form)
        flash('Dados atualizados com sucesso!', category='success')
    return render_template("account.html", current_user=current_user, form=user_form)

@views.route("/settings", methods=['GET', 'POST'])
@login_required
def settings():
    settings_form = SettingsForm()
    if request.method == 'GET':
        settings_form = SettingsForm(obj=current_user.settings)
    if request.method == 'POST':
        settings_service = SettingsService(current_user)
        settings_service.update(settings_form)
        flash('Configurações atualizadas com sucesso!', category='success')
    return render_template("settings.html", form=settings_form)

