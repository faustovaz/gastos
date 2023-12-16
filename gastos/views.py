import json
from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from functools import reduce
from datetime import date
from .forms import GastoForm
from .services import GastoService
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
    gastoForm = GastoForm()
    args = request.args
    gasto = gastoService.find(id)
    if gasto:
        if request.method == 'GET':
            gastoForm = GastoForm(obj=gasto)
        if gastoForm.validate_on_submit():
            gastoService.update(gastoForm, id)
            flash("Gasto atualizado com sucesso!", category="success")
    return render_template("edit.html", action=f"{gasto.to_edit()}", form=gastoForm)

@views.route("/")
@views.route("/monthly/")
@views.route("/monthly/<int:year>")
@login_required
def monthly(year=None):
    year = year if year else date.today().year
    gastoService = GastoService(current_user)
    all = gastoService.list_totals_by_year(year)
    return render_template("gastos_mensais.html", gastosMensaisView=GastosMensaisView(year, all))

@views.route("/monthly/<int:month>/<int:year>")
@login_required
def view_monthly(month, year):
    gastoService = GastoService(current_user)
    gastos = gastoService.all_by_month_and_year(month, year)
    return render_template("view_gasto_mensal.html", gastoMensalView=GastoMensalView(month, year, gastos))

@views.route("/recurrent")
@login_required
def recurrent():
    gastoService = GastoService(current_user)
    recorrentes = gastoService.all_recorrentes()
    total = reduce(lambda acc, gasto: acc + gasto.quanto, recorrentes, 0)
    return render_template("gastos_recorrentes.html", gastos=recorrentes, total=total)

@views.route("/add_to_month", methods = ['POST'])
@login_required
def add_to_month():
    service = GastoService(current_user)
    data = json.loads(request.data)
    gasto = service.add_to_month(data['gasto_id'], data['month'])
    if gasto:
        return jsonify({})

@views.route("/account")
@login_required
def account():
    return render_template("minha_conta.html")

