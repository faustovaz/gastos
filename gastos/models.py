from . import database

class Gasto(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    quando = database.Column(database.Date)
    quanto = database.Column(database.Float)
    descricao = database.Column(database.String)
    parcelado = database.Column(database.Boolean)
    recorrente = database.Column(database.Boolean)

    def __repr__(self):
        return f'<Gasto id={self.id}, quando={self.quando}, quanto={self.quanto}>'
