from flask_wtf import FlaskForm
from wtforms import DateField, StringField, BooleanField, DecimalField, IntegerField
from wtforms.validators import DataRequired, ValidationError

class GastoForm(FlaskForm):
    quando = DateField('Quando foi?', validators=[DataRequired()])
    quanto = DecimalField('Quanto custou?', validators=[DataRequired()])
    descricao = StringField('Descrição', validators=[DataRequired()])
    parcelado = BooleanField('O pagamento foi parcelado?')
    parcelas = IntegerField('Quantas parcelas?', default=2)
    recorrente = BooleanField('O Pagamento é recorrente?')
    tags = StringField('Tags')

    def validate_parcelas(form, field):
        isParcelado = form.parcelado.data
        if isParcelado and not (form.parcelas.data and int(form.parcelas.data) > 0):
            raise ValidationError("Informe um valor maior que zero")
