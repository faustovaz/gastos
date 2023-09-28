from flask_wtf import FlaskForm
from wtforms import DateField, StringField, BooleanField, DecimalField
from wtforms.validators import DataRequired

class GastoForm(FlaskForm):
    quando = DateField('Quando foi?', validators=[DataRequired()])
    quanto = DecimalField('Quanto custou?', validators=[DataRequired()])
    descricao = StringField('Descrição')
    parcelado = BooleanField('O pagamento foi parcelado?')
    recorrente = BooleanField('O Pagamento é recorrente?')
