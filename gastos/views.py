from flask import Blueprint, render_template, flash, redirect, url_for
from .forms import GastoForm 
from .services import GastoService
from .helpers import GastosMensaisView

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

@views.route("/")
@views.route("/monthly")
def monthly():
    gastoService = GastoService()
    all = gastoService.list_by_year(2023)
    return render_template("gastos_mensais.html", gastosMensaisView=GastosMensaisView(2023, all))

@views.route("/recurrent")
def recurrent():
    return render_template("gastos_recorrentes.html")

@views.route("/account")
def account():
    return render_template("minha_conta.html")



