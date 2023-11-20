from . import database

class GastoMensal(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    quando = database.Column(database.Date)
    quanto = database.Column(database.Float)
    descricao = database.Column(database.String)
    parcelado = database.Column(database.Boolean)
    parcelas = database.Column(database.Integer)
    parcela_repr = database.Column(database.String)
    tags = database.Column(database.String)
    gasto_recorrente_id = database.Column(database.Integer, \
                                          database.ForeignKey('gasto_recorrente.id'))

    def to_edit(self):
        return f'/edit/{self.id}'

    def __repr__(self):
        return f'<Gasto Mensal id={self.id}, quando={self.quando}, quanto={self.quanto}>'


class GastoRecorrente(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    quando = database.Column(database.Date)
    quanto = database.Column(database.Float)
    descricao = database.Column(database.String)
    tags = database.Column(database.String)

    def to_edit(self):
        return f'/edit/{self.id}?recurrent'

    def __repr__(self):
        return f'<Gasto Recorrente id={self.id}, quando={self.quando}, quanto={self.quanto}>'
        
    @classmethod
    def of(cls, gasto):
        gastoRecorrente = GastoRecorrente()
        gastoRecorrente.quando = gasto.quando
        gastoRecorrente.quanto = gasto.quanto
        gastoRecorrente.descricao = gasto.descricao
        gastoRecorrente.tags = gasto.tags
        return gastoRecorrente


