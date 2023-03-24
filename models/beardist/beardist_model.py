import pandas as pd
import math


class ColumnHeader:
    def __init__(self, csv_path, first_row_as_header):
        self.csv_path = csv_path
        self.first_row_as_header = first_row_as_header

    def get_column_header(self):
        if self.first_row_as_header:
            header = pd.read_csv(filepath_or_buffer=self.csv_path, skiprows=0,
                                 header=None, nrows=1).values.tolist()[0]
        else:
            header = pd.read_csv(filepath_or_buffer=self.csv_path, skiprows=0,
                                 header=None, nrows=1).values.tolist()[0]
            header = ["Column " + str(i + 1) for i in range(len(header))]

        return header


class ComputeBearDist:
    def __init__(self, csv_path, first_row_as_header, csv_column_header, matched_column_header,
                 angle_format, angle_separator):
        self.csv_path = csv_path
        self.first_row_as_header = first_row_as_header
        self.csv_column_header = csv_column_header
        self.matched_column_header = matched_column_header
        # self.compute_included_angle = compute_included_angle
        # self.compute_excluded_angle = compute_excluded_angle
        self.angle_format = angle_format  # 'Deci Deg' or 'Deg Min Sec'
        self.angle_separator = angle_separator

        self.file_data = None

    def read_csv_data(self):
        if self.first_row_as_header:
            self.file_data = pd.read_csv(filepath_or_buffer=self.csv_path, skiprows=1,
                                         header=None, names=self.csv_column_header).values
        else:
            self.file_data = pd.read_csv(filepath_or_buffer=self.csv_path, skiprows=0,
                                         header=None, names=self.csv_column_header).values

    def compute_beardist(self):
        self.read_csv_data()

        new_csv_data = []
        new_csv_data_header = ['Point', 'Northing', 'Easting', 'Back Target', 'Station', 'Fore Target',
                               'Bearing[Station-Back Target]', 'Distance[Station-Back Target]',
                               'Bearing[Station-Fore Target]', 'Distance[Station-Fore Target]',
                               'Included Angle[Back Target - Station - Fore Target]',
                               'Excluded Angle[Back Target - Station - Fore Target]', ]
        new_csv_data.append(new_csv_data_header)

        point_data = {}

        for line in self.file_data:
            point_name = line[self.csv_column_header.index(self.matched_column_header['Point'])]
            easting = line[self.csv_column_header.index(self.matched_column_header['Easting'])]
            northing = line[self.csv_column_header.index(self.matched_column_header['Northing'])]
            if not pd.isnull(point_name) and not pd.isnull(easting) and \
                    not pd.isnull(northing):
                point_data[point_name] = {'easting': easting, 'northing': northing}

        # Note the below
        for line in self.file_data:
            if not pd.isnull(line[self.csv_column_header.index(
                    self.matched_column_header['Back Target'])]) \
                    and not pd.isnull(line[self.csv_column_header.index(
                    self.matched_column_header['Station'])]) \
                    and not pd.isnull(line[self.csv_column_header.index(
                    self.matched_column_header['Fore Target'])]):
                _point_name = line[self.csv_column_header.index(self.matched_column_header['Point'])]
                _easting = line[self.csv_column_header.index(self.matched_column_header['Easting'])]
                _northing = line[self.csv_column_header.index(self.matched_column_header['Northing'])]
                _back_target = line[self.csv_column_header.index(self.matched_column_header['Back Target'])]
                _fore_target = line[self.csv_column_header.index(self.matched_column_header['Fore Target'])]
                _station = line[self.csv_column_header.index(self.matched_column_header['Station'])]
                _back_target_easting = point_data[_back_target]['easting']
                _back_target_northing = point_data[_back_target]['northing']
                _station_easting = point_data[_station]['easting']
                _station_northing = point_data[_station]['northing']
                _fore_target_easting = point_data[_fore_target]['easting']
                _fore_target_northing = point_data[_fore_target]['northing']

                _easting_change1 = float(_back_target_easting) - float(_station_easting)
                _northing_change1 = float(_back_target_northing) - float(_station_northing)

                _easting_change2 = float(_fore_target_easting) - float(_station_easting)
                _northing_change2 = float(_fore_target_northing) - float(_station_northing)

                _distance1 = ((_easting_change1 ** 2) + (_northing_change1 ** 2)) ** 0.5
                _distance2 = ((_easting_change2 ** 2) + (_northing_change2 ** 2)) ** 0.5

                _bearing1 = math.degrees(math.atan2(_easting_change1, _northing_change1))
                if _bearing1 < 0:
                    _bearing1 += 360

                _bearing2 = math.degrees(math.atan2(_easting_change2, _northing_change2))
                if _bearing2 < 0:
                    _bearing2 += 360

                # if self.compute_included_angle:
                _included_angle = _bearing2 - _bearing1
                # else:
                #   _included_angle = ""

                # if self.compute_excluded_angle:
                _excluded_angle = 360 - (_bearing2 - _bearing1)
                # else:
                #     _excluded_angle = ""

                if str(self.angle_format).lower() == "Deg Min Sec".lower():
                    _bearing1 = from_deci_deg_to_deg_min_sec(_bearing1)
                    _bearing2 = from_deci_deg_to_deg_min_sec(_bearing2)
                    _included_angle = from_deci_deg_to_deg_min_sec(_included_angle)
                    _excluded_angle = from_deci_deg_to_deg_min_sec(_excluded_angle)

                    if str(self.angle_separator).lower().strip() == "space":
                        _bearing1 = format_deg_min_sec(_bearing1, " ")
                        _bearing2 = format_deg_min_sec(_bearing2, " ")
                        _included_angle = format_deg_min_sec(_included_angle, " ")
                        _excluded_angle = format_deg_min_sec(_excluded_angle, " ")

                    else:
                        _bearing1 = format_deg_min_sec(_bearing1, str(self.angle_separator))
                        _bearing2 = format_deg_min_sec(_bearing2, str(self.angle_separator))
                        _included_angle = format_deg_min_sec(_included_angle, str(self.angle_separator))
                        _excluded_angle = format_deg_min_sec(_excluded_angle, str(self.angle_separator))

                new_csv_data_line = [_point_name, _northing, _easting, _back_target, _station,
                                     _fore_target, _bearing1, _distance1, _bearing2,
                                     _distance2, _included_angle, _excluded_angle]

                new_csv_data.append(new_csv_data_line)

        return new_csv_data

    def perform_computations(self):
        try:
            csv_data = self.compute_beardist()

        except:
            csv_data = None

        return csv_data


def save_csv_data(filepath, csv_data):
    csv_data_frame = pd.DataFrame(csv_data)

    csv_data_frame.to_csv(filepath, index=False, header=False)


def from_deci_deg_to_deg_min_sec(angle):
    deg = int(angle)
    _min = int((angle - deg) * 60)
    sec = (((angle - deg) * 60) - _min) * 60

    return deg, _min, sec


def from_deg_min_sec_to_deci_deg(deg, _min, sec):
    deci_deg = float(deg) + (float(_min) / 60) + (float(sec) / 3600)

    return deci_deg


def format_deg_min_sec(deg_min_sec, separator):
    angle = deg_min_sec  # A tuple
    new_angle = ""
    for item in angle:
        new_angle += str(item) + str(separator)

    new_angle = new_angle.rstrip(str(separator))

    return new_angle


if __name__ == '__main__':
    # _northing_change1 = 697764.821 - 697879.42
    # _easting_change1 = 648169.783 - 648173.073
    # _northing_change1 = 697762.222 - 697764.821
    # _easting_change1 = 648103.677 - 648169.783
    # _northing_change1 = 697876.017 - 697762.222
    # _easting_change1 = 648107.762 - 648103.677
    # _northing_change1 = 697879.42 - 697876.017
    # _easting_change1 = 648173.073 - 648107.762
    # _bearing1 = math.degrees(math.atan2(_easting_change1, _northing_change1))

    # if _bearing1 < 0:
    #     _bearing1 += 360
    # print(_bearing1)

    old_file_path = "C:\\Users\\USER\\OneDrive\\Desktop\\my_trial.csv"
    new_file_path = "C:\\Users\\USER\\OneDrive\\Desktop\\my_trial_courage.csv"
    matched_column = {"Point": "Point", "Easting": "Easting", "Northing": "Northing",
                      "Back Target": "Back Target",
                      "Station": "Station", "Fore Target": "Fore Target"}
    column = ["Point", "Northing", "Easting", "Back Target", "Station", "Fore Target"]
    mena = ComputeBearDist(old_file_path, True, column, matched_column, "Deg", "-")
    save_csv_data(new_file_path, mena.perform_computations(), )
    # print(from_deci_deg_to_deg_min_sec(267.7485391))
    # print(from_deg_min_sec_to_deci_deg(267, 44, 54.7407600000588))
