import pandas as pd
import numpy as np


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


class ComputeGeoidModel:
    def __init__(self, train_csv_path, train_first_row_as_header,
                 train_csv_column_header, train_matched_column_header,
                 pred_csv_path, pred_first_row_as_header,
                 pred_csv_column_header, pred_matched_column_header,
                 ):
        self.train_csv_path = train_csv_path
        self.train_first_row_as_header = train_first_row_as_header
        self.train_csv_column_header = train_csv_column_header
        self.train_matched_column_header = train_matched_column_header

        self.pred_csv_path = pred_csv_path
        self.pred_first_row_as_header = pred_first_row_as_header
        self.pred_csv_column_header = pred_csv_column_header
        self.pred_matched_column_header = pred_matched_column_header

        self.train_file_data = None
        self.pred_file_data = None

    def read_train_csv_data(self):
        if self.train_first_row_as_header:
            self.train_file_data = pd.read_csv(filepath_or_buffer=self.train_csv_path, skiprows=1,
                                               header=None, names=self.train_csv_column_header).values
        else:
            self.train_file_data = pd.read_csv(filepath_or_buffer=self.train_csv_path, skiprows=0,
                                               header=None, names=self.train_csv_column_header).values

    def read_pred_csv_data(self):
        if self.pred_first_row_as_header:
            self.pred_file_data = pd.read_csv(filepath_or_buffer=self.pred_csv_path, skiprows=1,
                                              header=None, names=self.pred_csv_column_header).values
        else:
            self.pred_file_data = pd.read_csv(filepath_or_buffer=self.pred_csv_path, skiprows=0,
                                              header=None, names=self.pred_csv_column_header).values

    def generate_matrices(self):
        self.read_train_csv_data()

        # Reading the data and storing the base station.
        # Note that the first specified point becomes the
        # base station. However in situations where there are no base station specified,
        # the first point gets selected
        base_station_data = {}
        first_station_data = {}

        for index, line in enumerate(self.train_file_data):
            _station = line[self.train_csv_column_header.index(
                self.train_matched_column_header['Station'])]
            _gps_easting = line[self.train_csv_column_header.index(
                self.train_matched_column_header['GPS Easting'])]
            _gps_northing = line[self.train_csv_column_header.index(
                self.train_matched_column_header['GPS Northing'])]
            _gps_height = line[self.train_csv_column_header.index(
                self.train_matched_column_header['GPS Height'])]
            _orthometric_height = line[self.train_csv_column_header.index(
                self.train_matched_column_header['Orthometric Height'])]

            _base_station = line[self.train_csv_column_header.index(
                self.train_matched_column_header['Base Station'])]

            if index == 0:
                first_station_data = {'gps_easting': _gps_easting, 'gps_northing': _gps_northing,
                                      'gps_height': _gps_height, 'orthometric_height': _orthometric_height}

            if not pd.isnull(_base_station):
                base_station_data = {'gps_easting': _gps_easting, 'gps_northing': _gps_northing,
                                     'gps_height': _gps_height, 'orthometric_height': _orthometric_height}
                break

        if not base_station_data:
            base_station_data = first_station_data

        #  Generating the matrices with respect to the base as follows
        #  N = h - H
        #  N is Geoidal height/Geoid undulation | h is ellipsoidal height | H is orthometric height
        #  (Ni - No) = a(Ei - Eo) - b(Ni - No) + c
        #  The matrix form is
        #   [Ni - No] = [(Ei - Eo) - (Ni - No) 1][a b c]
        #    L        =  A                        X
        #    Ax = L + v
        #    X = (A^TA)^-1 x A^TL

        L_matrix = []
        A_matrix = []
        base_station_N = float(base_station_data['gps_height']) - \
                         float(base_station_data['orthometric_height'])  # No
        base_station_Easting = float(base_station_data['gps_easting'])  # Eo
        base_station_Northing = float(base_station_data['gps_northing'])  # No

        for line in self.train_file_data:
            _gps_easting = line[self.train_csv_column_header.index(
                self.train_matched_column_header['GPS Easting'])]
            _gps_northing = line[self.train_csv_column_header.index(
                self.train_matched_column_header['GPS Northing'])]
            _gps_height = line[self.train_csv_column_header.index(
                self.train_matched_column_header['GPS Height'])]
            _orthometric_height = line[self.train_csv_column_header.index(
                self.train_matched_column_header['Orthometric Height'])]
            _geoidal_height = float(_gps_height) - float(_orthometric_height)

            _geoidal_height_change = _geoidal_height - base_station_N  # GNi - GNo
            _gps_easting_change = float(_gps_easting) - base_station_Easting  # Ei - No
            _gps_northing_change = (float(_gps_northing) - base_station_Northing) * -1

            A_matrix.append([_gps_easting_change, _gps_northing_change, 1])
            L_matrix.append(_geoidal_height_change)

        return {'base_station_data': base_station_data, 'A_matrix': A_matrix,
                'L_matrix': L_matrix}

    def compute_parameters(self):
        matrices_dict = self.generate_matrices()
        #    X = (A^TA)^-1 x A^TL
        base_station_data = matrices_dict['base_station_data']
        A_matrix = np.array(matrices_dict['A_matrix'])
        L_matrix = np.array(matrices_dict['L_matrix'])

        # let N = (A^TA) and B = (A^TL)
        N = np.matmul(A_matrix.transpose(), A_matrix)
        B = np.matmul(A_matrix.transpose(), L_matrix)

        X_matrix = np.matmul(np.linalg.inv(N), B)  # N^-1 * B

        V_matrix = np.subtract(np.matmul(A_matrix, X_matrix), L_matrix)
        variance = np.divide(np.matmul(V_matrix.transpose(), V_matrix),
                                 np.array([len(L_matrix)-len(base_station_data)]))
        standard_deviation = np.sqrt(variance)

        return {'base_station_data': base_station_data, 'X_matrix': X_matrix,
                'V_matrix': V_matrix, 'variance': variance, 'standard_deviation': standard_deviation}

    def estimate_orthometric_heights(self):
        parameters_data = self.compute_parameters()
        base_station_data = parameters_data['base_station_data']
        X_matrix = parameters_data['X_matrix']
        V_matrix = parameters_data['V_matrix']
        variance = parameters_data['variance']
        standard_deviation = parameters_data['standard_deviation']

        # (Ni - No) = a(Easti - Easto) - b(Northi - Northo) + c
        a, b, c = X_matrix[0], X_matrix[1], X_matrix[2]
        No = float(base_station_data['gps_height']) - float(base_station_data['orthometric_height'])
        # print(No, base_station_data['gps_height'], base_station_data['orthometric_height'])
        Easto = base_station_data['gps_easting']
        Northo = base_station_data['gps_northing']
        # print(a, b, c, No, Easto, Northo)

        # N = h - H
        #  N is Geoidal height/Geoid undulation | h is ellipsoidal height | H is orthometric height
        new_data = []
        new_data_header = ["Station", "Northing", "Easting", "GPS/Ellipsoidal Height", "Geoidal Height",
                           'Orthometric Height']
        new_data.append(new_data_header)

        if self.pred_csv_path:
            self.read_pred_csv_data()

            for line in self.pred_file_data:
                _station = line[self.pred_csv_column_header.index(
                    self.pred_matched_column_header['Station'])]
                _gps_easting = line[self.pred_csv_column_header.index(
                    self.pred_matched_column_header['GPS Easting'])]
                _gps_northing = line[self.pred_csv_column_header.index(
                    self.pred_matched_column_header['GPS Northing'])]
                _gps_height = line[self.pred_csv_column_header.index(
                    self.pred_matched_column_header['GPS Height'])]
                _geoidal_height = a * (float(_gps_easting) - Easto) - \
                                  b * (float(_gps_northing) - Northo) + c + No
                _orthometric_height = _gps_height - _geoidal_height

                new_data.append([_station, _gps_northing, _gps_easting, _gps_height, _geoidal_height,
                                 _orthometric_height])

        model = "Geoidal height -" + str(No) + "= " + str(a) + "[Easting -" + str(Easto) + "]" + "- " + \
                str(b) + "[Northing -" + str(Northo) + "] + " + str(c)

        new_data.append(["", "", "", "", "", ""])
        new_data.append(["MODEL DETAILS", "", "", "", "", ""])
        new_data.append(["", "", "", "", "", ""])
        new_data.append(["MODEL", model, "", "", "", ""])
        new_data.append(["X MATRIX", str(X_matrix.tolist()), "", "", "", ""])
        new_data.append(["V MATRIX", str(V_matrix.tolist()), "", "", "", ""])
        new_data.append(["VARIANCE", str(variance[0]), "", "", "", ""])
        new_data.append(["STANDARD DEVIATION", str(standard_deviation[0]), "", "", "", ""])

        return new_data

    def perform_computations(self):
        try:
            csv_data = self.estimate_orthometric_heights()
        except:
            csv_data = None

        return csv_data


def save_csv_data(filepath, csv_data):
    # Note that the csv data must be list of lists
    csv_data_frame = pd.DataFrame(csv_data)

    csv_data_frame.to_csv(filepath, index=False, header=False)


if __name__ == "__main__":
    train_file_path = "C:\\Users\\USER\\OneDrive\\Desktop\\geoid_model_train1.csv"
    pred_file_path = "C:\\Users\\USER\\OneDrive\\Desktop\\geoid_model_pred1.csv"
    output_file_path = "C:\\Users\\USER\\OneDrive\\Desktop\\geoid_model_pred2.csv"
    matched_column1 = {"Station": "1", "Base Station": "2", "GPS Northing": "3", "GPS Easting": "4",
                      "GPS Height": "5", "Orthometric Height": "6"}
    column1 = ["1", "2", "3", "4", "5", "6"]
    matched_column2 = {"Station": "1", "GPS Northing": "2", "GPS Easting": "3",
                       "GPS Height": "4"}
    column2 = ["1", "2", "3", "4", "5"]

    ean = ComputeGeoidModel(train_file_path, True, column1, matched_column1, pred_file_path,
                            True, column2, matched_column2)
    ean.save_csv_data(output_file_path)