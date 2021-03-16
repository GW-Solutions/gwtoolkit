from gwtoolkit.conversions import BARO_CONVERSIONS_TO_MH2O, BARO_CONVERSIONS_FROM_MH2O


class BarometricPressure:

    def __init__(self, *, value=None, units=None):
        self._value = value
        self._units = units
        self._values = {}
        self._parse_value()

    def set_pressure(self, value, units):
        self._value = value
        self._units = units

    def _parse_value(self):
        if self._units and self._value:
            assert self._units in BARO_CONVERSIONS_TO_MH2O, f'Unrecognized units: {self._units}'
            self._values['mh2o'] = BARO_CONVERSIONS_TO_MH2O[self._units](self._value)
            self._values['atm'] = BARO_CONVERSIONS_FROM_MH2O['atm'](self._mH2O)
            self._values['bar'] = BARO_CONVERSIONS_FROM_MH2O['bar'](self._mH2O)
            self._values['kpa'] = BARO_CONVERSIONS_FROM_MH2O['kpa'](self._mH2O)
            self._values['mbar'] = BARO_CONVERSIONS_FROM_MH2O['mbar'](self._mH2O)
            self._values['pa'] = BARO_CONVERSIONS_FROM_MH2O['pa'](self._mH2O)
            self._values['psi'] = BARO_CONVERSIONS_FROM_MH2O['ps'](self._mH2O)
            self._values['torr'] = BARO_CONVERSIONS_FROM_MH2O['torr'](self._mH2O)
            self._values['ubar'] = BARO_CONVERSIONS_FROM_MH2O['ubar'](self._mH2O)

    def __getattr__(self, value):
        assert value in self._values, f'Unknown attribute {value}'
        return self._values[value]


