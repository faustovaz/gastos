from flask_wtf import FlaskForm
from wtforms import DateField, StringField, BooleanField, DecimalField, IntegerField, PasswordField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Length

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


class UserForm(FlaskForm):
    login = StringField('Login', render_kw={'readonly':''})
    current_password = PasswordField('Senha atual', validators=[DataRequired()])
    password = PasswordField('Nova Senha', \
                            validators=[DataRequired(), \
                                EqualTo('confirm_password', 'Senhas precisam ser iguais'), \
                                Length(min=6, message='Senha precisa ser maior que 6 chars')])
    confirm_password = PasswordField('Repetir nova senha')
