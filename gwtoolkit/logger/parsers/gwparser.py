import collections
from dateutil import parser
import pandas as pd

from gwtoolkit.logger.parsers.utils import get_datetime, get_csv_reader, md5, do_get, get_float


CompensatedValues = collections.namedtuple(
    "CompensatedValues",
    ["water_level_compensated_m", "logger_depth_m", "depth_to_water_m"])


GroundWaterSourceFile = collections.namedtuple(
    "GroundWaterSourceFile",
    ["filename", "hash"]
)


GroundWater = collections.namedtuple(
    "GroundWater",
    ['approval_level', 'barometric_pressure_m', 'barometric_pressure_source_file', 'comments', 'conductivity_us_cm',
     'datetime', 'downloaded_by', 'grade_code', 'depth_to_water_m', 'depth_to_water_mtoc', 'ground_elevation_m',
     'ground_water_elevation_m', 'source_file', 'logger', 'logger_depth_m', 'station', 'temperature_c', 'water_level_compensated_m',
     'water_level_non_compensated_m']
)


def parse_groundwater_csv_in_memory(fobj,
                                    header_row,
                                    mappings,
                                    logger,
                                    station,
                                    *,
                                    sheetname=None,
                                    baro_ts=None,
                                    baro_file_name=None):
    """Parse groundwater data. Need to handle errors"""
    # gw_file = GroundWaterSourceFile(filename=fobj.name, hash=md5(fobj))
    fobj.file.seek(0)
    with fobj.open() as f:
        # reader = get_csv_reader(f, header_row)
        if f.name.endswith('.xlsx'):
            reader = pd.read_excel(f, header=header_row-1, sheet_name=int(sheetname) - 1, parse_dates=False)
        else:
            reader = pd.read_csv(f, header=header_row-1, parse_dates=False)
        import functools
        partial_dt = functools.partial(get_datetime, mappings=mappings)
        reader['datetime'] = reader.apply(partial_dt, axis=1)
        # Handle manual depth to water measurements
        manual_logger_depth_m = _get_logger_depth(reader, mappings, baro_ts)
        for count, row in enumerate(reader.itertuples(index=False)):
            datetime = get_datetime(row, mappings)
            if baro_ts is not None:
                baro_level_m = _get_barometric_pressure(baro_ts, datetime)
            else:
                baro_level_m = do_get(row, mappings, "barometric_pressure_m")
            comp_values = _get_compensated_values(
                row, mappings, baro_level_m, manual_logger_depth_m=manual_logger_depth_m)
            # TODO: CHECK baro pressure within 3 days
            # if logger:
            #     logger = logger.obj

            gw = GroundWater(
                approval_level=do_get(row, mappings, "approval_level"),
                barometric_pressure_m=baro_level_m,
                barometric_pressure_source_file=baro_file_name,
                comments=do_get(row, mappings, "comments"),
                conductivity_us_cm=do_get(row, mappings, "conductivity_us_cm"),
                datetime=datetime,
                downloaded_by=do_get(row, mappings, "dowloaded_by"),
                grade_code=do_get(row, mappings, "grade_code"),
                depth_to_water_m=comp_values.depth_to_water_m,
                depth_to_water_mtoc=None,
                ground_elevation_m=do_get(row, mappings, "ground_elevation_m"),
                ground_water_elevation_m=do_get(row, mappings, "groundwater_elevation_m"),
                source_file=None,
                logger=logger,
                logger_depth_m=comp_values.logger_depth_m,
                station=station,
                temperature_c=do_get(row, mappings, "temperature_c"),
                water_level_compensated_m=comp_values.water_level_compensated_m,
                water_level_non_compensated_m=do_get(row, mappings, "water_level_non_compensated_m")
            )

            yield gw



def _get_logger_depth(reader, mappings, baro_ts):
    manual_measurement = mappings.get('depth_to_water_manual')
    if manual_measurement:
        manual_measurement_dt = mappings['depth_to_water_manual_time']
        dt = parser.parse(manual_measurement_dt)
        dt_index = pd.to_datetime(reader['datetime'].tolist())

        ndx = dt_index.get_loc(dt, method='nearest')
        closest_row = reader.iloc[ndx]
        barometric_pressure = None
        if baro_ts is not None:
            dt = get_datetime(closest_row, mappings)
            barometric_pressure = _get_barometric_pressure(baro_ts, dt)
        compensated_values = _get_compensated_values(closest_row, mappings, barometric_pressure)
        if compensated_values.water_level_compensated_m:
            return float(manual_measurement) + compensated_values.water_level_compensated_m

def _get_barometric_pressure(baro_ts, datetime):
    # print("Input", datetime, "Nearest", baro_ts.index[baro_ts.index.get_loc(datetime, method='nearest')])
    return baro_ts.iloc[baro_ts.index.get_loc(datetime, method='nearest')]


def _get_compensated_values(row, mappings, barometric_pressure_m, *, manual_logger_depth_m=None):
    """
    Rules:
    level_logger_comp = level_logger_non_comp - barometric pressure
    logger_depth_m = depth_water_m + level_logger_comp | depth_water_mtoc + level_logger_comp - mtoc
    depth_water_m = logger_depth_m - level_logger_comp | ground_elevation + gw_elevation | depth_water_mtoc - mtoc
    """
    depth_to_water_m = get_float(row, mappings, "depth_to_water_m")
    level_logger_compensated = get_float(row, mappings, "water_level_compensated_m")
    level_logger_non_compenstated = get_float(row, mappings, "water_level_non_compensated_m")
    depth_to_water_mtoc = get_float(row, mappings, "depth_to_water_mtoc")
    logger_depth_m = get_float(row, mappings, "logger_depth_m")
    if not logger_depth_m:
        logger_depth_m = manual_logger_depth_m
    logger_depth_mtoc = get_float(row, mappings, "logger_depth_mtoc")  # TODO use value
    mtoc = get_float(row, mappings, "mtoc")  #TODO: Fix this name
    ground_elevation_m = get_float(row, mappings, "ground_elevation_m")
    groundwater_elevation_m = get_float(row, mappings, "groundwater_elevation_m")
    if level_logger_compensated is None:
        if level_logger_non_compenstated and barometric_pressure_m:
            level_logger_compensated = float(level_logger_non_compenstated) - float(barometric_pressure_m)
    if logger_depth_m is None:
        if depth_to_water_m and level_logger_compensated:
            logger_depth_m = depth_to_water_m + level_logger_compensated
        elif depth_to_water_mtoc and level_logger_compensated and mtoc:
            logger_depth_m = depth_to_water_mtoc + level_logger_compensated - mtoc
    if depth_to_water_m is None:
        if logger_depth_m and level_logger_compensated:
            depth_to_water_m = logger_depth_m - level_logger_compensated
        elif ground_elevation_m and groundwater_elevation_m:
            depth_to_water_m = ground_elevation_m + groundwater_elevation_m
        elif depth_to_water_mtoc and mtoc:
            depth_to_water_m = depth_to_water_mtoc - mtoc
    # if depth_to_water_m is None:
    #     raise Exception("Input must contains enough data to derive Depth to Water (m)")
    return CompensatedValues(level_logger_compensated, logger_depth_m, depth_to_water_m)





if __name__ == "__main__":
    pass

