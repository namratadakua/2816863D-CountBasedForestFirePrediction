import pandas as pd
import logging
from final_data_models import MapCoordinates


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


def prepare_model_data(grid):
    logging.basicConfig(filename='prepare_model_data.log', level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    map_coordinates = MapCoordinates()
    model_df = pd.DataFrame({
        'cell_center_longitude': pd.Series(dtype='float'),
        'cell_center_latitude': pd.Series(dtype='float'),
        'daynight': pd.Series(dtype='str'),
        'year': pd.Series(dtype='str'),
        # 'brightness': pd.Series(dtype='float'),
        # 'confidence': pd.Series(dtype='float'),
        # 'frp': pd.Series(dtype='float'),
        # 'bright_t31': pd.Series(dtype='float'),
        # 'fire_occurrence': pd.Series(dtype='int'),
        'month': pd.Series(dtype='int'),
        'day': pd.Series(dtype='int'),
        '10m_u_component_of_wind': pd.Series(dtype='float'),
        '10m_v_component_of_wind': pd.Series(dtype='float'),
        '2m_temperature': pd.Series(dtype='float'),
        'soil_temperature_level_1': pd.Series(dtype='float'),
        'soil_temperature_level_2': pd.Series(dtype='float'),
        'soil_temperature_level_3': pd.Series(dtype='float'),
        'soil_temperature_level_4': pd.Series(dtype='float'),
        'soil_type': pd.Series(dtype='float'),
        'total_precipitation': pd.Series(dtype='float'),
        'volumetric_soil_water_layer_1': pd.Series(dtype='float'),
        'volumetric_soil_water_layer_2': pd.Series(dtype='float'),
        'volumetric_soil_water_layer_3': pd.Series(dtype='float'),
        'volumetric_soil_water_layer_4': pd.Series(dtype='float'),
        'number_of_fire': pd.Series(dtype='int')
    })

    for row in range(0, map_coordinates.meridians_length):
        for column in range(0, map_coordinates.parallels_length):
            grid_cell = grid[row, column]

            if grid_cell.fire_count > 0:
                fire_point_rows = []
                for fire_point in grid_cell.fire_points:
                    new_row = create_new_fire_point_row(fire_point)
                    fire_point_rows.append(new_row)
                count_df, model_df = group_and_count(fire_point_rows, grid_cell, model_df)
                logging.debug(f"{row}:{column} row completed with count - {grid_cell.fire_count} {len(count_df)} ")

            if len(grid_cell.non_fire_points) > 0:
                grouped_fire_points = create_fire_points_df_with_zero_count(grid_cell)
                model_df = pd.concat([model_df, grouped_fire_points])
                logging.debug(f"{row}:{column} row completed with count - {grid_cell.fire_count} ")
        if row % 100 == 0:
            print(f"grid {row} row completed")
    model_df.to_csv('./dataset/final_model_data.csv')
    return model_df


def create_fire_points_df_with_zero_count(grid_cell):
    fire_point_rows = []
    for fire_point in grid_cell.non_fire_points:
        new_row = create_new_fire_point_row(fire_point)
        fire_point_rows.append(new_row)
    non_fire_point_df = pd.DataFrame(fire_point_rows, columns=column_names)
    grouped_fire_points = non_fire_point_df.groupby(['daynight', 'year', 'month', 'day']).agg({
    #grouped_fire_points = non_fire_point_df.groupby(['daynight', 'year', 'month']).agg({
        '10m_u_component_of_wind': 'mean',
        '10m_v_component_of_wind': 'mean',
        '2m_temperature': 'mean',
        'soil_temperature_level_1': 'mean',
        'soil_temperature_level_2': 'mean',
        'soil_temperature_level_3': 'mean',
        'soil_temperature_level_4': 'mean',
        'soil_type': 'mean',
        'total_precipitation': 'mean',
        'volumetric_soil_water_layer_1': 'mean',
        'volumetric_soil_water_layer_2': 'mean',
        'volumetric_soil_water_layer_3': 'mean',
        'volumetric_soil_water_layer_4': 'mean'
    })
    grouped_fire_points = grouped_fire_points.reset_index()
    grouped_fire_points['cell_center_longitude'] = (grid_cell.llon + grid_cell.ulon) / 2
    grouped_fire_points['cell_center_latitude'] = (grid_cell.llat + grid_cell.ulat) / 2
    grouped_fire_points['number_of_fire'] = 0
    return grouped_fire_points


# Fire points in a cell are grouped based on date and daynight parameter
# and average of climate parameters is calculated along with number of fire points
def group_and_count(fire_point_rows, grid_cell, model_df):
    fire_point_df = pd.DataFrame(fire_point_rows, columns=column_names)
    grouped_fire_points = fire_point_df.groupby(['daynight', 'year', 'month', 'day']).agg({
    #grouped_fire_points = fire_point_df.groupby(['daynight', 'year', 'month']).agg({
        '10m_u_component_of_wind': 'mean',
        '10m_v_component_of_wind': 'mean',
        '2m_temperature': 'mean',
        'soil_temperature_level_1': 'mean',
        'soil_temperature_level_2': 'mean',
        'soil_temperature_level_3': 'mean',
        'soil_temperature_level_4': 'mean',
        'soil_type': 'mean',
        'total_precipitation': 'mean',
        'volumetric_soil_water_layer_1': 'mean',
        'volumetric_soil_water_layer_2': 'mean',
        'volumetric_soil_water_layer_3': 'mean',
        'volumetric_soil_water_layer_4': 'mean'
    })
    grouped_fire_points = grouped_fire_points.reset_index()
    count_df = grouped_fire_points.groupby(['daynight', 'year', 'month', 'day']).size().to_frame(
        name='number_of_fire').reset_index()
    merged_df = grouped_fire_points.merge(count_df, on=['daynight', 'year', 'month', 'day'])
    #merged_df = grouped_fire_points.merge(count_df, on=['daynight', 'year', 'month'])
    merged_df['cell_center_longitude'] = (grid_cell.llon + grid_cell.ulon) / 2
    merged_df['cell_center_latitude'] = (grid_cell.llat + grid_cell.ulat) / 2
    model_df = pd.concat([model_df, merged_df])
    return count_df, model_df


def create_new_fire_point_row(fire_point):
    new_row = {
        'fire_latitude': fire_point.fire_latitude,
        'fire_longitude': fire_point.fire_longitude,
        'climate_latitude': fire_point.climate_latitude,
        'climate_longitude': fire_point.climate_longitude,
        'daynight': fire_point.daynight,
        'year': fire_point.year,
        'month': fire_point.month,
        'day': fire_point.day,
        'date': fire_point.date,
        'brightness': fire_point['brightness'],
        'confidence': fire_point['confidence'],
        'frp': fire_point['frp'],
        'bright_t31': fire_point['bright_t31'],
        'fire_occurrence': fire_point['fire_occurrence'],
        '10m_u_component_of_wind': fire_point['10m_u_component_of_wind'],
        '10m_v_component_of_wind': fire_point['10m_v_component_of_wind'],
        '2m_temperature': fire_point['2m_temperature'],
        'soil_temperature_level_1': fire_point['soil_temperature_level_1'],
        'soil_temperature_level_2': fire_point['soil_temperature_level_2'],
        'soil_temperature_level_3': fire_point['soil_temperature_level_3'],
        'soil_temperature_level_4': fire_point['soil_temperature_level_4'],
        'soil_type': fire_point['soil_type'],
        'total_precipitation': fire_point['total_precipitation'],
        'volumetric_soil_water_layer_1': fire_point['volumetric_soil_water_layer_1'],
        'volumetric_soil_water_layer_2': fire_point['volumetric_soil_water_layer_2'],
        'volumetric_soil_water_layer_3': fire_point['volumetric_soil_water_layer_3'],
        'volumetric_soil_water_layer_4': fire_point['volumetric_soil_water_layer_4']
    }
    return new_row
