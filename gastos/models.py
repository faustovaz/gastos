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
                                          database.ForeignKey('gasto.id'))

    def to_edit(self):
        return f'/edit/{self.id}'

    def __repr__(self):
        return f'<Gasto id={self.id}, quando={self.quando}, quanto={self.quanto}>'

