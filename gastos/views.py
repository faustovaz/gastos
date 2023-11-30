from flask import Blueprint, render_template, flash, redirect, url_for, request
from functools import reduce
from datetime import date
from .forms import GastoForm
from .services import GastoService
from .helpers import GastosMensaisView, GastoMensalView

views = Blueprint('views', __name__)

@views.route("/add", methods=['GET', 'POST'])
def save():
    gastoForm = GastoForm()
    if gastoForm.validate_on_submit():
        gastoService = GastoService()
        gastoService.save_form(gastoForm)
        flash('Gasto adicionado com sucesso!', category='success')
        return redirect(url_for('views.save'))
    return render_template("add.html", form=gastoForm)

@views.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    gastoService = GastoService()
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
def monthly(year=None):
    year = year if year else date.today().year
    gastoService = GastoService()
    all = gastoService.list_by_year(year)
    return render_template("gastos_mensais.html", gastosMensaisView=GastosMensaisView(year, all))

@views.route("/monthly/<int:month>/<int:year>")
def view_monthly(month, year):
    gastoService = GastoService()
    gastos = gastoService.all_by_month_and_year(month, year)
    return render_template("view_gasto_mensal.html", gastoMensalView=GastoMensalView(month, year, gastos))

@views.route("/recurrent")
def recurrent():
    gastoService = GastoService()
    recorrentes = gastoService.all_recorrentes()
    total = reduce(lambda acc, gasto: acc + gasto.quanto, recorrentes, 0)
    return render_template("gastos_recorrentes.html", gastos=recorrentes, total=total)

@views.route("/account")
def account():
    return render_template("minha_conta.html")

