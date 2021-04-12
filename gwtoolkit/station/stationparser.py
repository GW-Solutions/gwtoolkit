import pandas as pd
import numpy as np
from gwtoolkit.utils import do_ndx_get


def parse_station_file(fobj, header_row, mappings, model_class, source_file, *, sheetname=None):
    with fobj.open() as f:
        if f.name.endswith('.xlsx'):
            reader = pd.read_excel(f, header=header_row-1, sheet_name=int(sheetname) - 1)
        else:
            reader = pd.read_csv(f, header=header_row-1)
        # model_fields = model_class._meta.get_fields()
        column_ndx = {}
        for count, name in enumerate(reader.columns):
            column_ndx[name] = count

        for row in reader.itertuples(index=False):
            # object_dict = {}
            # for field in model_fields:
            #     field_name = field.field_name
            #     if field_name != 'id' and not isinstance(field, ):
            #         object_dict[field_name] = do_ndx_get(row, mappings, field_name)
            station_id = do_ndx_get(row, mappings, 'station_id', column_ndx)
            # import ipdb; ipdb.set_trace()
            if station_id and not pd.isna(station_id):
                yield model_class(
                    accuracy_elevation=do_ndx_get(row, mappings, 'accuracy_elevation', column_ndx),
                    accuracy_location=do_ndx_get(row, mappings, 'accuracy_location', column_ndx),
                    aquifer_number=do_ndx_get(row, mappings, 'aquifer_number', column_ndx),
                    easting_m=do_ndx_get(row, mappings, 'easting_m', column_ndx),
                    ground_elevation_m=do_ndx_get(row, mappings, 'ground_elevation_m', column_ndx),
                    latitude=do_ndx_get(row, mappings, 'latitude', column_ndx),
                    location_name=do_ndx_get(row, mappings, 'location_name', column_ndx),
                    longitude=do_ndx_get(row, mappings, 'longitude', column_ndx),
                    monitoring_status='0',  # TODO hack to get this working
                    monitoring_type=do_ndx_get(row, mappings, 'monitoring_type', column_ndx),
                    northing_m=do_ndx_get(row, mappings, 'northing_m', column_ndx),
                    prov_terr_state_lc=do_ndx_get(row, mappings, 'prov_terr_state_lc', column_ndx),
                    pump_depth_m=do_ndx_get(row, mappings, 'pump_depth_m', column_ndx),
                    sounder_pipe_m=do_ndx_get(row, mappings, 'sounder_pipe_m', column_ndx),
                    station_id=station_id,
                    source_file=source_file,
                    top_of_casing_m=do_ndx_get(row, mappings, 'top_of_casing_m', column_ndx),
                    well_aquifer_type='0',
                    well_depth_m=do_ndx_get(row, mappings, 'well_depth_m', column_ndx),
                    well_id_plate=do_ndx_get(row, mappings, 'well_id_plate', column_ndx),
                    well_tag_number=do_ndx_get(row, mappings, 'well_tag_number', column_ndx),
                    zone=do_ndx_get(row, mappings, 'zone', column_ndx))
