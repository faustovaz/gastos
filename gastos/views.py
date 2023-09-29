from flask import Blueprint, render_template, flash
from .forms import GastoForm 
from .models import Gasto
from . import database 

views = Blueprint('views', __name__)

@views.route("/", methods=['GET', 'POST'])
def index():
    gastoForm = GastoForm()
    if gastoForm.validate_on_submit():
        gasto = Gasto()
        gastoForm.populate_obj(gasto)
        database.session.add(gasto)
        database.session.commit()
        flash('Dados salvos com sucesso!', category='success')
    return render_template("index.html", form=gastoForm)


