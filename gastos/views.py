from flask import Blueprint, render_template
from .forms import GastoForm 

views = Blueprint('views', __name__)

@views.route("/", methods=['GET', 'POST'])
def index():
    gastoForm = GastoForm()
    return render_template("index.html", form=gastoForm)


