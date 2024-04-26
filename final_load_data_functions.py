import pandas as pd


def get_climate_data(year):
    climate_data_directory = './dataset/climatedata'
    data = pd.read_csv(f'{climate_data_directory}/canada_{year}.csv')
    return data


def get_fire_data(year):
    fire_data_directory = './dataset/firedata'
    data = pd.read_csv(f'{fire_data_directory}/canada_{year}.csv')
    data['fire_occurrence'] = (data['confidence'] >= 90).astype(int)
    return data


def get_mapped_fire_data():
    years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
    directory = './dataset/map_climate_to_fire'
    model_data = None
    for year in years:
        data = pd.read_csv(f"{directory}/mapped_fire_to_climate_{year}.csv")
        if model_data is None:
            model_data = data
        else:
            model_data = pd.concat([model_data, data])
            model_data.reset_index(drop=True, inplace=True)
    return model_data


# def combine_fire_and_climate_data(fire_data, climate_data):
#     fire_data.rename(columns={'acq_date': 'date'}, inplace=True)
#     # Columns to join on
#     on_columns = ['date', 'daynight', 'latitude', 'longitude']
#
#     result = pd.merge(fire_data, climate_data, how='left', left_on=on_columns, right_on=on_columns)
#     result = result.drop(columns=['Unnamed: 0_x', 'Unnamed: 0_y'])
#     return result
#
#
# def get_all_fire_data():
#     years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
#     data = None
#     for year in years:
#         fire_data = get_fire_data(year)
#         if data is None:
#             data = fire_data
#         data = pd.concat([data, fire_data])
#         data.reset_index(drop=True, inplace=True)
#     return data
#
#
# def get_all_climate_data():
#     years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
#     data = None
#     for year in years:
#         climate_data = get_climate_data(year)
#         if data is None:
#             data = climate_data
#         data = pd.concat([data, climate_data])
#         data.reset_index(drop=True, inplace=True)
#     return data
#
#
# def prepare_data():
#     years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
#     data = None
#     for year in years:
#         climate_data = get_climate_data(year)
#         fire_data = get_fire_data(year)
#
#         combined_fire_and_climate_data = combine_fire_and_climate_data(fire_data, climate_data)
#
#         if data is None:
#             data = combined_fire_and_climate_data
#
#         data = pd.concat([model_data, combined_fire_and_climate_data])
#
#         data.reset_index(drop=True, inplace=True)
#     return data
