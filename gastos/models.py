from flask_login import UserMixin
from sqlalchemy import UniqueConstraint
from . import database

class Gasto(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    quando = database.Column(database.Date)
    quanto = database.Column(database.Float)
    descricao = database.Column(database.String)
    parcelado = database.Column(database.Boolean)
    parcelas = database.Column(database.Integer)
    parcela_repr = database.Column(database.String)
    recorrente = database.Column(database.Boolean)
    tags = database.Column(database.String)
    gasto_recorrente_id = database.Column(database.Integer, \
                                          database.ForeignKey('gasto.id', \
                                            name = 'fk_gasto_recorrente_id'))
    usuario_id = database.Column(database.Integer, \
                                    database.ForeignKey('user.id', \
                                            name = 'fk_user_id'))
    usuario = database.Relationship('User')

    def to_edit(self):
        return f'/edit/{self.id}'

    def descricao_formatted(self):
        if self.parcelado:
            return f'{self.descricao} {self.parcela_repr}'
        return self.descricao

    def belongs_to(self, current_user):
        return self.usuario_id == current_user.id
    
    def __repr__(self):
        return f'<Gasto id={self.id}, quando={self.quando}, quanto={self.quanto}>'


class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    login = database.Column(database.String)
    password = database.Column(database.String(150))
    UniqueConstraint('login', name='uq_login')
