"""
Constant values used for conversions

Pressure conversions currently operate relative to mH2O
"""
atm = 0.096781446
bar = 0.0980638
kPa = 9.80638
mbar = 98.0638
Pa = 9806.38
PSI = 1.422295231
Torr = 73.55388142
ubar = 98063.8
mH2O = 1.0


BARO_CONVERSIONS_TO_MH2O = {
    "atm": lambda x: x / atm,
    "bar": lambda x: x / bar,
    "kpa": lambda x: x / kPa,
    "ubar": lambda x: x / ubar,
    "mbar": lambda x: x / mbar,
    "pa": lambda x: x / Pa,
    "psi": lambda x: x / PSI,
    "tor": lambda x: x / Torr,
    "mh2o": lambda x: x / mH2O
}


BARO_CONVERSIONS_FROM_MH2O ={
    "atm": lambda x: x * atm,
    "bar": lambda x: x * bar,
    "kpa": lambda x: x * kPa,
    "ubar": lambda x: x * ubar,
    "mbar": lambda x: x * mbar,
    "pa": lambda x: x * Pa,
    "psi": lambda x: x * PSI,
    "tor": lambda x: x * Torr,
    "mh2o": lambda x: x * mH2O
}
