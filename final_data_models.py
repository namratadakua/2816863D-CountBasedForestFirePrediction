import numpy as np


# This function finds out the smaller range for a longitude
# so that row number in the grid can be identified with fewer iteration
def get_row_range(longitude, row_ranges):
    map_coords = MapCoordinates()
    lower_row_limit = 0
    upper_row_limit = 0
    lower_row_limit_found = False
    upper_row_limit_found = False
    row_check = 0
    while row_check < (len(row_ranges)):
        if not lower_row_limit_found and row_ranges[row_check].llon > longitude:
            lower_row_limit_found = True
            lower_row_limit = row_check if row_check == 0 else (row_check - 1)
        if not upper_row_limit_found and row_ranges[row_check].ulon > longitude:
            upper_row_limit_found = True
            upper_row_limit = row_check
        if lower_row_limit_found and upper_row_limit_found:
            break
        row_check += 1

    if lower_row_limit == upper_row_limit:
        upper_row_limit = upper_row_limit + 2

    lower_row_limit = (lower_row_limit * 111) - 1
    upper_row_limit = (upper_row_limit * 111)

    if upper_row_limit >= map_coords.meridians_length:
        upper_row_limit = map_coords.meridians_length

    return lower_row_limit, upper_row_limit


# This function finds out the smaller range for a latitude
# so that column number in the grid can be identified with fewer iteration
def get_col_range(latitude, column_ranges):
    map_coords = MapCoordinates()
    lower_col_limit = 0
    upper_col_limit = 0
    lower_col_limit_found = False
    upper_col_limit_found = False
    col_check = 0
    while col_check < (len(column_ranges)):
        if not lower_col_limit_found and column_ranges[col_check].llat > latitude:
            lower_col_limit_found = True
            lower_col_limit = col_check if col_check == 0 else col_check - 1
        if not upper_col_limit_found and column_ranges[col_check].ulat > latitude:
            upper_col_limit_found = True
            upper_col_limit = col_check
        if lower_col_limit_found and upper_col_limit_found:
            break
        col_check += 1

    if lower_col_limit == upper_col_limit:
        upper_col_limit += 1

    lower_col_limit = (lower_col_limit * 111) - 1
    upper_col_limit = (upper_col_limit * 111) + 1

    if upper_col_limit >= map_coords.parallels_length:
        upper_col_limit = map_coords.parallels_length

    return lower_col_limit, upper_col_limit


class RowRange:
    def __init__(self, llon, ulon):
        self.llon = llon
        self.ulon = ulon


class ColumnRange:
    def __init__(self, llat, ulat):
        self.llat = llat
        self.ulat = ulat


class FirePoint:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return f"FirePoint( latitude = {self.latitude},  longitude = {self.longitude})"

# Grid Cell holds the information of 1x1km cell
# upper longitude, lower longitude
# upper latitude, lower latitude
# number of fire count
# list of climate data which are considered as fire ignitions
# list of climate data which are not considered as fire ignitions
class GridCell:
    """ This class holds the coordinates - start and end of latitude and longitude """

    def __init__(self, llat, ulat, llon, ulon, fire_count):
        self.llat = llat
        self.ulat = ulat
        self.llon = llon
        self.ulon = ulon
        self.fire_count = fire_count
        self.fire_points = []
        self.non_fire_points = []

    def __repr__(self):
        return f"GridCell( llat = {self.llat},  ulat = {self.ulat}, llon = {self.llon}, ulon = {self.ulon}, fire_count = {self.fire_count}, fire_points_length = {len(self.fire_points)})"


# This class holds the Canada map information
# Latitude and Longitude
# Number of meridians and parallels when the map is divided in 1x1km grid
class MapCoordinates:
    def __init__(self):
        self.llon = -142
        self.ulon = -55
        self.llat = 41
        self.ulat = 70

        self.distance = 1 / 111
        self.parallels = np.arange(self.llat, self.ulat, self.distance)
        self.meridians = np.arange(self.llon, self.ulon, self.distance)
        self.meridians_length = len(self.meridians)  # x-axis - longitude
        self.parallels_length = len(self.parallels)  # y-axis - latitude

# Grid information
# It holds the Grid in a matrix information
# Number of rows = number of meridians
# Number of columns = number of parallels
class FireDataGrid:
    def __init__(self):
        map_coordinates = MapCoordinates()
        self.row_ranges = []
        self.col_ranges = []
        print(f"fire data Row {map_coordinates.meridians_length} and Columns {map_coordinates.parallels_length}")
        grid = np.full(shape=(map_coordinates.meridians_length, map_coordinates.parallels_length), fill_value=None)
        meridians_list = list(map_coordinates.meridians)
        parallels_list = list(map_coordinates.parallels)

        for row in range(0, map_coordinates.meridians_length):
            longitude = meridians_list[row]
            lower_longitude = longitude
            upper_longitude = longitude + map_coordinates.distance
            for col in range(0, map_coordinates.parallels_length):
                latitude = parallels_list[col]
                lower_latitude = latitude
                upper_latitude = latitude + map_coordinates.distance
                # print(type(upper_longitude))
                cell = GridCell(float(lower_latitude),
                                float(upper_latitude),
                                float(lower_longitude),
                                float(upper_longitude), 0)
                # print(cell)
                grid[row, col] = cell
                if row == 0 and (col == 0 or ((col + 1) % 111) == 0):
                    col_range = ColumnRange(lower_latitude, upper_latitude)
                    self.col_ranges.append(col_range)

                # if (col == 0 or ((col + 1) % 111) == 0):
                #     print(f"finished column {row} : {col} ")
            if row == 0 or ((row + 1) % 111) == 0:
                row_range = RowRange(lower_longitude, upper_longitude)
                self.row_ranges.append(row_range)
                print(f"finished row {row} ")

        print("Grid ready================")
        self.grid = grid
