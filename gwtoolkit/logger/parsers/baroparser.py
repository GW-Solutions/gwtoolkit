import pandas as pd

from gwtoolkit.conversions import BARO_CONVERSIONS_TO_MH2O
from gwtoolkit.logger.parsers.utils import get_datetime, get_csv_reader


def parse_barometric_pressure_file(fobj, header_row, mappings, units, *, sheetname=None):
    with fobj.open() as f:
        if f.name.endswith('.xlsx'):
            reader = pd.read_excel(f, header=header_row-1, sheet_name=sheetname)
        else:
            reader = pd.read_csv(f, header=header_row-1)
        datetimes = []
        pressures = []
        conversion_func = BARO_CONVERSIONS_TO_MH2O[units.lower()]
        for row in reader.itertuples(index=False):
            datetime = get_datetime(row, mappings)
            pressure = getattr(row, mappings["barometric_pressure"])
            pressure_mh2o = conversion_func(float(pressure))
            datetimes.append(datetime)
            pressures.append(pressure_mh2o)
        dt_index = pd.to_datetime(datetimes)
        return pd.Series(pressures, index=dt_index)

if __name__ == "__main__":
    with open("/home/davebshow/git/depth2water/data/baro_data/Baro.csv", "r", errors='replace') as f:
        parse_barometric_pressure_file(f, 11, {"date": "Date", "time": "Time", "baro_level": "Level"}, "kPa")