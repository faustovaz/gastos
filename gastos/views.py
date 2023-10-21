from flask import Blueprint, render_template, flash, redirect, url_for
from functools import reduce
from datetime import date
from .forms import GastoForm 
from .services import GastoService
from .helpers import GastosMensaisView, GastoMensalView

views = Blueprint('views', __name__)

@views.route("/add", methods=['GET', 'POST'])
def add_new():
    gastoForm = GastoForm()
    if gastoForm.validate_on_submit():
        gastoService = GastoService(gastoForm)
        gastoService.save()
        flash('Gasto adicionado com sucesso!', category='success')
        return redirect(url_for('views.add_new'))
    return render_template("form.html", form=gastoForm)

@views.route("/edit/<id>", methods=['GET'])
def edit(id):
    gastoService = GastoService()
    gasto = gastoService.find_by_id(id)
    gastoForm = GastoForm()
    if gasto:
        gastoForm = GastoForm(obj=gasto)
    return render_template("form.html", form=gastoForm)

@views.route("/")
@views.route("/monthly/")
@views.route("/monthly/<year>")
def monthly(year=None):
    year = int(year) if year and year.isnumeric() else date.today().year
    gastoService = GastoService()
    all = gastoService.list_by_year(year)
    return render_template("gastos_mensais.html", gastosMensaisView=GastosMensaisView(year, all))

@views.route("/monthly/<month>/<year>")
def view_monthly(month, year):
    gastoService = GastoService()
    gastos = gastoService.all_by_month_and_year(month, year)
    recorrentes = gastoService.all_recorrentes()
    
    return render_template("view_gasto_mensal.html", \
                            gastoMensalView=GastoMensalView(month, year, gastos, recorrentes))


@views.route("/recurrent")
def recurrent():
    gastoService = GastoService()
    recorrentes = gastoService.all_recorrentes()
    total = reduce(lambda acc, gasto: acc + gasto.quanto, recorrentes, 0)
    return render_template("gastos_recorrentes.html", gastos=recorrentes, total=total)

@views.route("/account")
def account():
    return render_template("minha_conta.html")



