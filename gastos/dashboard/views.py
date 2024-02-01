from flask import Blueprint, render_template

dashboard = Blueprint('dashboard', __name__)

@dashboard.route("/", methods=['GET'])
def index():
    return render_template("dashboard.html")