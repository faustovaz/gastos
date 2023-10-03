from flask import Blueprint, render_template, flash, redirect, url_for
from .forms import GastoForm 
from .services import GastoService

views = Blueprint('views', __name__)

@views.route("/", methods=['GET', 'POST'])
def index():
    gastoForm = GastoForm()
    if gastoForm.validate_on_submit():
        gastoService = GastoService(gastoForm)
        gastoService.save()
        flash('Gasto adicionado com sucesso!', category='success')
        return redirect(url_for('views.index'))
    return render_template("index.html", form=gastoForm)


