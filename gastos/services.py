from dateutil.relativedelta import relativedelta
from . import database
from .models import GastoMensal, GastoRecorrente

class GastoService():

    def __init__(self, gastoForm):
        self.gastoForm = gastoForm

    def isParcelado(self):
        return self.gastoForm.parcelado.data

    def isRecorrente(self):
        return self.gastoForm.recorrente.data

    def save(self):
        if self.isParcelado():
            self._saveGastoParcelado()
        elif self.isRecorrente():
            self._saveGastoRecorrente()
        else:
            self._saveGastoMensal()

    def _saveGastoMensal(self):
        gasto = GastoMensal()
        self.gastoForm.populate_obj(gasto)
        database.session.add(gasto)
        database.session.commit()

    def _saveGastoParcelado(self):
        parcelas = int(self.gastoForm.parcelas.data)
        for parcela in range(1, parcelas + 1):
            gasto = GastoMensal()
            self.gastoForm.populate_obj(gasto)
            gasto.parcela_repr = f'({parcela}/{parcelas})'
            gasto.quando = gasto.quando + relativedelta(months = parcela - 1)
            database.session.add(gasto)
        database.session.commit()

    def _saveGastoRecorrente(self):
        gasto = GastoRecorrente()
        self.gastoForm.populate_obj(gasto)
        database.session.add(gasto)
        database.session.commit()

