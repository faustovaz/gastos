from flask import Blueprint, render_template, flash, redirect, url_for
from .forms import GastoForm 
from .services import GastoService

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
    return render_template("gastos_mensais.html")

@views.route("/recurrent")
def recurrent():
    return render_template("gastos_recorrentes.html")

@views.route("/account")
def account():
    return render_template("minha_conta.html")



