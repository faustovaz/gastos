from flask import Blueprint, render_template, request
from .forms import GastoForm 

views = Blueprint('views', __name__)

@views.route("/", methods=['GET', 'POST'])
def index():
    gastoForm = GastoForm()
    if gastoForm.validate_on_submit():
        pass
    return render_template("index.html", form=gastoForm)


