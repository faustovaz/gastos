from flask_wtf import FlaskForm
from wtforms import DateField, StringField, BooleanField, DecimalField, IntegerField, PasswordField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Length
from werkzeug.security import check_password_hash
from .models import User

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
    password = PasswordField('Nova Senha', validators=[DataRequired()])
    confirm_password = PasswordField('Repetir nova senha')

    def validate_password(form, field):
        user = User.query.filter_by(login=form.login.data).first()
        current_passwd = form.current_password.data
        password = form.password.data
        confirm_passwd = form.confirm_password.data
        if not check_password_hash(user.password, current_passwd):
            raise ValidationError("A senha atual está errada")
        if len(password) < 6:
            raise ValidationError("A nova senha deve ter mais que 5 caracteres")
        if password != confirm_passwd:
            raise ValidationError("A nova senha e confirmação da nova estão diferentes")