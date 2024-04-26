import pandas as pd
import logging
from final_data_models import MapCoordinates
from final_data_models import get_row_range
from final_data_models import get_col_range
from final_load_data_functions import get_mapped_fire_data


# This function exports the grid cell data in csv file
# It creates multiple csv files each having cells for 1000 rows
def export_grid_grouped(grid):
    map_coordinates = MapCoordinates()
    grid_rows = []
    column_names = ['cell_center_longitude', 'cell_center_latitude', 'number_of_fire', 'number_of_non_fire']
    count = 1
    for row in range(0, map_coordinates.meridians_length):
        for column in range(0, map_coordinates.parallels_length):
            grid_cell = grid[row, column]
            new_row = {
                'cell_center_longitude': (grid_cell.llon + grid_cell.ulon) / 2,
                'cell_center_latitude': (grid_cell.llat + grid_cell.ulat) / 2,
                'number_of_fire': grid_cell.fire_count,
                'number_of_non_fire': len(grid_cell.non_fire_points)
            }
            grid_rows.append(new_row)
        if row != 0 and row % 1000 == 0:
            result_df = pd.DataFrame(grid_rows, columns=column_names)
            result_df.to_csv(f"./grid_export/export_grid_{count}.csv", index=False)
            grid_rows = []
            count += 1
            print(f"exported till row {row} ")
        if row == 0 or ((row + 1) % 111) == 0:
            print(f"finished row {row} ")

    result_df = pd.DataFrame(grid_rows, columns=column_names)

    result_df.to_csv(f"./gridExport/export_grid_{count}.csv", index=False)


# This function assigns the fire occurrence to respective cell along with climate data.
def set_fire_count(grid, row_ranges, column_ranges):
    all_data = get_mapped_fire_data()
    logging.basicConfig(filename='set_fire_count.log', level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    # fire_occurrence_data = all_data.query("`fire_occurrence` == 1")
    map_coordinates = MapCoordinates()
    for index, fire_data_row in all_data.iterrows():

        latitude = fire_data_row['fire_latitude']
        longitude = fire_data_row['fire_longitude']

        if not (map_coordinates.llat <= latitude <= map_coordinates.ulat):
            logging.debug(f"fire {index} row not found - latitude out of range {latitude}")
            continue

        if not (map_coordinates.llon <= longitude <= map_coordinates.ulon):
            logging.debug(f"fire {index} row not found - longitude out of range {longitude}")
            continue

        fire_occurrence = fire_data_row['fire_occurrence']
        lower_row_limit, upper_row_limit = get_row_range(longitude, row_ranges)
        lower_col_limit, upper_col_limit = get_col_range(latitude, column_ranges)

        # print(f"{lower_row_limit}:{upper_row_limit} - {lower_col_limit}:{upper_col_limit}")

        # Assign the fire data to a grid
        found = False
        row_found = 0
        col_found = 0
        for row in range(lower_row_limit, upper_row_limit):
            for col in range(lower_col_limit, upper_col_limit):
                grid_cell = grid[row, col]

                cell_llat = grid_cell.llat
                cell_ulat = grid_cell.ulat
                cell_llon = grid_cell.llon
                cell_ulon = grid_cell.ulon
                fire_count = grid_cell.fire_count
                fire_points = grid_cell.fire_points
                non_fire_points = grid_cell.non_fire_points

                if (cell_llat <= latitude < cell_ulat) and (cell_llon <= longitude < cell_ulon):
                    found = True
                    if fire_occurrence == 1:
                        fire_count = fire_count + 1
                        grid_cell.fire_count = fire_count
                        fire_points.append(fire_data_row)
                    else:
                        # if fire_count > 0:
                        #     non_fire_points = []
                        # else:
                        non_fire_points.append(fire_data_row)

                    grid_cell.fire_count = fire_count
                    grid_cell.fire_points = fire_points
                    grid_cell.non_fire_points = non_fire_points

                    grid[row, col] = grid_cell
                    # print(f"fire {index} row completed  - {longitude}:{latitude} at {row}:{col} - {grid_cell}")

                    row_found = row
                    col_found = col

                    break

            if found:
                if index % 100 == 0:
                    print(f"fire {index} row completed  - {longitude}:{latitude} at {row}")
                break
        if not found:
            logging.debug(f"fire {index} row not found")
            logging.debug(
                f"fire {index} row not completed {lower_row_limit}:{upper_row_limit} - {lower_col_limit}:{upper_col_limit} - {longitude} : {latitude} - {fire_data_row['date']} -  {fire_data_row['daynight']}")
            for row in range(0, map_coordinates.meridians_length):
                for col in range(0, map_coordinates.parallels_length):
                    grid_cell = grid[row, col]

                    cell_llat = grid_cell.llat
                    cell_ulat = grid_cell.ulat
                    cell_llon = grid_cell.llon
                    cell_ulon = grid_cell.ulon
                    fire_count = grid_cell.fire_count
                    fire_points = grid_cell.fire_points

                    if (cell_llat <= latitude < cell_ulat) and (cell_llon <= longitude < cell_ulon):
                        found = True
                        if fire_occurrence == 1:
                            fire_count = fire_count + 1
                            grid_cell.fire_count = fire_count

                        fire_points.append(fire_data_row)
                        grid_cell.fire_points = fire_points

                        grid[row, col] = grid_cell
                        # print(f"fire {index} row completed  - {longitude}:{latitude} at {row}:{col} - {grid_cell}")
                        row_found = row
                        col_found = col
                        break

                if found:
                    logging.debug(
                        f"retry - fire {index} row completed {longitude}:{latitude} at {row_found} {col_found}")
                    break
        # end of fire_row loop
    return grid
