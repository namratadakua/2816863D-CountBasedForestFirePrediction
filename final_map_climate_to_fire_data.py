import pandas as pd
import numpy as np
from final_load_data_functions import get_fire_data
from final_load_data_functions import get_climate_data
import logging


def map_climate_to_fire(year):
    log_file_name = f"map_climate_to_fire|_log_{year}.log"
    logging.basicConfig(filename=log_file_name, level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    fire_data = get_fire_data(year)
    climate_data = get_climate_data(year)

    model_df_rows = []

    for index, fire_row in fire_data.iterrows():
        acq_date = fire_row['acq_date']
        day_night = fire_row['daynight']
        fire_longitude = fire_row['longitude']
        fire_latitude = fire_row['latitude']

        date_split = acq_date.split("-")
        year = date_split[0]
        month = date_split[1]
        day = date_split[2]

        filtered_climate_data = climate_data.query(f"`date` == '{acq_date}' and `daynight` == '{day_night}'")

        if len(filtered_climate_data) == 0:
            logging.debug(f"{index} climate data not found {fire_latitude}:{fire_longitude} - {acq_date} - {day_night}")
            continue

        abs_diff_lon = np.abs(filtered_climate_data['longitude'].to_numpy() - fire_longitude)
        lon_index = np.argmin(abs_diff_lon)

        abs_diff_lat = np.abs(filtered_climate_data['latitude'].to_numpy() - fire_latitude)
        lat_index = np.argmin(abs_diff_lat)

        if lon_index != lat_index:
            logging.debug(f"{index} Latitude index {lat_index} does not match longitude index {lon_index}")
            logging.debug(f"{index} Latitude {fire_latitude} longitude {fire_longitude}")
        else:
            new_row = {
                'fire_latitude': fire_latitude,
                'fire_longitude': fire_longitude,
                'climate_latitude': filtered_climate_data.iloc[lon_index,].latitude,
                'climate_longitude': filtered_climate_data.iloc[lon_index,].longitude,
                'daynight': day_night,
                'year': year,
                'month': month,
                'day': day,
                'date': acq_date,
                'brightness': fire_row['brightness'],
                'confidence': fire_row['confidence'],
                'frp': fire_row['frp'],
                'bright_t31': fire_row['bright_t31'],
                'fire_occurrence': fire_row['fire_occurrence'],
                '10m_u_component_of_wind': filtered_climate_data.iloc[lon_index,]['10m_u_component_of_wind'],
                '10m_v_component_of_wind': filtered_climate_data.iloc[lon_index,]['10m_v_component_of_wind'],
                '2m_temperature': filtered_climate_data.iloc[lon_index,]['2m_temperature'],
                'soil_temperature_level_1': filtered_climate_data.iloc[lon_index,]['soil_temperature_level_1'],
                'soil_temperature_level_2': filtered_climate_data.iloc[lon_index,]['soil_temperature_level_2'],
                'soil_temperature_level_3': filtered_climate_data.iloc[lon_index,]['soil_temperature_level_3'],
                'soil_temperature_level_4': filtered_climate_data.iloc[lon_index,]['soil_temperature_level_4'],
                'soil_type': filtered_climate_data.iloc[lon_index,]['soil_type'],
                'total_precipitation': filtered_climate_data.iloc[lon_index,]['total_precipitation'],
                'volumetric_soil_water_layer_1': filtered_climate_data.iloc[lon_index,][
                    'volumetric_soil_water_layer_1'],
                'volumetric_soil_water_layer_2': filtered_climate_data.iloc[lon_index,][
                    'volumetric_soil_water_layer_2'],
                'volumetric_soil_water_layer_3': filtered_climate_data.iloc[lon_index,][
                    'volumetric_soil_water_layer_3'],
                'volumetric_soil_water_layer_4': filtered_climate_data.iloc[lon_index,]['volumetric_soil_water_layer_4']
            }

            model_df_rows.append(new_row)

    column_names = ['fire_latitude',
                    'fire_longitude',
                    'climate_latitude',
                    'climate_longitude',
                    'daynight',
                    'year',
                    'month',
                    'day',
                    'date',
                    'brightness',
                    'confidence',
                    'frp',
                    'bright_t31',
                    'fire_occurrence',
                    '10m_u_component_of_wind',
                    '10m_v_component_of_wind',
                    '2m_temperature',
                    'soil_temperature_level_1',
                    'soil_temperature_level_2',
                    'soil_temperature_level_3',
                    'soil_temperature_level_4',
                    'soil_type',
                    'total_precipitation',
                    'volumetric_soil_water_layer_1',
                    'volumetric_soil_water_layer_2',
                    'volumetric_soil_water_layer_3',
                    'volumetric_soil_water_layer_4']
    result_df = pd.DataFrame(model_df_rows, columns=column_names)

    result_df.to_csv(f"./dataset/map_climate_to_fire/mapped_fire_to_climate_{year}.csv", index=False)
