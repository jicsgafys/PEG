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


class LevelsAdjustment:
    def __init__(self, cvs_path, first_row_as_header, csv_column_header,
                 matched_column_header, weight_type, confidence_level):
        self.csv_path = cvs_path
        self.first_row_as_header = first_row_as_header
        self.csv_column_header = csv_column_header
        self.matched_column_header = matched_column_header
        self.weight_type = weight_type
        self.confidence_level = confidence_level

        self.confidence_level_data = {"65%": 0.935, "80%": 1.282, "90%": 1.645,
                                      "95%": 1.960, "99%": 2.575, "50%": 0.75,
                                      "98%": 2.33}

        self.file_data = None

    def read_csv_data(self):
        if self.first_row_as_header:
            self.file_data = pd.read_csv(filepath_or_buffer=self.csv_path, skiprows=1,
                                         header=None, names=self.csv_column_header).values
        else:
            self.file_data = pd.read_csv(filepath_or_buffer=self.csv_path, skiprows=0,
                                         header=None, names=self.csv_column_header).values

    def generate_matrices(self):
        self.read_csv_data()

        # Loading capturing the points and elevation
        point_data = {}
        provisional_height = {}  # Provisional height of unknown points
        for line in self.file_data:
            point = line[self.csv_column_header.index(self.matched_column_header['Point'])]
            elevation = line[self.csv_column_header.index(self.matched_column_header['Elevation'])]
            BM = line[self.csv_column_header.index(self.matched_column_header['BM'])]

            if not pd.isnull(BM):
                BM = True

            else:
                BM = False

            if not pd.isnull(point):
                point_data[str(point)] = {'elevation': elevation, 'BM': BM}

                if not BM:
                    provisional_height[point] = elevation

        # print(point_data)

        # Forming a table for computing the errors
        # Table header is like [To, From, change(L), weight]
        # The csv_data is looped again
        matrix_data = []
        matrix_data_header = ["To", "From", "Error_change", "Weight"]
        unknown_points = set()
        known_points = set()
        total_count = 0
        for line in self.file_data:
            _to = line[self.csv_column_header.index(self.matched_column_header['To'])]
            _from = line[self.csv_column_header.index(self.matched_column_header['From'])]
            _weight = line[self.csv_column_header.index(self.matched_column_header['Weight'])]
            _to_elev = point_data[_to]['elevation']  # Fetches the elevation of the point
            _from_elev = point_data[_from]['elevation']  # Fetches the elevation of the point
            _to_is_bm = point_data[_to]['BM']  # Checks if the to is a benchmark
            _from_is_bm = point_data[_from]['BM']  # Checks if the from is a benchmark
            _change_elev = line[self.csv_column_header.index(self.matched_column_header['Change_elev'])]
            _change_error = (float(_from_elev) - float(_to_elev)) + _change_elev
            matrix_data.append([_to, _from, _change_error, _weight])

            total_count += 1

            if not _to_is_bm:
                unknown_points.add(_to)

            else:
                known_points.add(_to)

            if not _from_is_bm:
                unknown_points.add(_from)

            else:
                known_points.add(_from)

        # Using the formula x = (A^TWA)^-1(A^TWL)

        A_matrix = []
        W_matrix = []
        L_matrix = []
        L_matrix_label = []  # Contains [From, To]

        A_matrix_header = list(unknown_points)

        for index in range(total_count):
            _to_error = matrix_data[index][matrix_data_header.index("To")]
            _from_error = matrix_data[index][matrix_data_header.index("From")]
            _change_error = matrix_data[index][matrix_data_header.index("Error_change")]
            _weight_error = matrix_data[index][matrix_data_header.index("Weight")]
            A_matrix_line = [0] * len(A_matrix_header)
            L_matrix_line = _change_error
            W_matrix_line = [0] * total_count

            if _to_error not in known_points:
                A_matrix_line[A_matrix_header.index(_to_error)] = 1

            if _from_error not in known_points:
                A_matrix_line[A_matrix_header.index(_from_error)] = -1

            # W_matrix_line[index] = (1/(_weight_error ** 2))
            if self.weight_type == "W":
                _weight_error = _weight_error
            elif self.weight_type == "1/W":
                _weight_error = 1 / _weight_error
            elif self.weight_type == "1/W²":
                _weight_error = 1 / (_weight_error ** 2)

            W_matrix_line[index] = _weight_error

            A_matrix.append(A_matrix_line)
            L_matrix.append(L_matrix_line)
            W_matrix.append(W_matrix_line)
            L_matrix_label.append([_from_error, _to_error])

        return {'A_matrix': A_matrix, 'L_matrix': L_matrix, 'W_matrix': W_matrix,
                'A_matrix_header': A_matrix_header, 'L_matrix_label': L_matrix_label,
                'provisional_height': provisional_height}

    def compute_parameter(self):
        matrices_dict = self.generate_matrices()
        provisional_height = matrices_dict['provisional_height']
        A_matrix_header = matrices_dict['A_matrix_header']
        L_matrix_label = matrices_dict['L_matrix_label']
        A_matrix = np.array(matrices_dict['A_matrix'])
        L_matrix = np.array(matrices_dict['L_matrix'])
        W_matrix = np.array(matrices_dict['W_matrix'])

        # X_matrix = (A^TWA)^-1(A^TWL)
        # let N = (A^TWA) and B = (A^TWL)
        N = np.matmul(np.matmul(A_matrix.transpose(), W_matrix), A_matrix)
        B = np.matmul(np.matmul(A_matrix.transpose(), W_matrix), L_matrix)

        X_matrix = np.matmul(np.linalg.inv(N), B)  # N^-1 * B

        V_matrix = np.subtract(np.matmul(A_matrix, X_matrix), L_matrix)
        variance = np.divide(np.matmul(np.matmul(V_matrix.transpose(), W_matrix), V_matrix),
                             np.array([len(L_matrix)-len(A_matrix_header)]))
        standard_deviation = np.sqrt(variance)

        Cx_matrix = variance[0] * np.linalg.inv(N)

        Cv_part1 = variance[0] * np.linalg.inv(W_matrix)
        Cv_part2 = np.matmul(np.matmul(A_matrix, Cx_matrix), A_matrix.transpose())
        Cv_matrix = np.subtract(Cv_part1, Cv_part2)

        Qxixi_part1 = np.linalg.inv(W_matrix)
        Qxixi_part2 = np.matmul(np.matmul(A_matrix, np.linalg.inv(N)), A_matrix.transpose())
        Qxixi_matrix = np.subtract(Qxixi_part1, Qxixi_part2)

        return {"A_matrix_header": A_matrix_header, "A_matrix": A_matrix,
                "L_matrix_label": L_matrix_label, "L_matrix": L_matrix,
                "W_matrix": W_matrix, "X_matrix": X_matrix, "V_matrix": V_matrix,
                "variance": variance[0], 'standard_deviation': standard_deviation[0],
                'Cx_matrix': Cx_matrix, 'Cv_matrix': Cv_matrix, 'Qxixi_matrix': Qxixi_matrix,
                'provisional_height': provisional_height}

    def build_tables(self):
        matrices_dict = self.compute_parameter()
        A_matrix_header = matrices_dict['A_matrix_header']
        L_matrix_label = matrices_dict['L_matrix_label']
        Qxixi_matrix = matrices_dict["Qxixi_matrix"]
        V_matrix = matrices_dict["V_matrix"]
        standard_deviation = matrices_dict['standard_deviation']
        variance = matrices_dict['variance']
        provisional_height = matrices_dict['provisional_height']
        X_matrix = matrices_dict['X_matrix']
        L_matrix = matrices_dict['L_matrix']
        A_matrix = matrices_dict['A_matrix']
        W_matrix = matrices_dict['W_matrix']
        Cx_matrix = matrices_dict['Cx_matrix']
        Cv_matrix = matrices_dict['Cv_matrix']

        decision_table = []  # Table which contains the lines their residuals, qxixi, v_bar, criteria info,
        decision_table_header = ['FROM', 'TO', 'VI', 'QXIXI', 'V_BAR', 'CRITERIA', 'ACCEPTED/REJECTED']
        decision_table.append(decision_table_header)
        for index, line in enumerate(L_matrix_label):
            _from = line[0]  # From
            _to = line[1]  # To
            qxixi = Qxixi_matrix[index][index]  # The diagonals
            vi = V_matrix[index]
            v_bar = (abs(vi) / (qxixi ** 0.5))
            criteria = self.confidence_level_data[str(self.confidence_level)] * standard_deviation
            accept_reject = "Accepted"
            if v_bar > criteria:
                accept_reject = "Rejected"

            decision_table.append([_from, _to, vi, qxixi, v_bar, criteria, accept_reject])

        correction_table = []
        correction_table_header = ['POINT', 'PROVISIONAL HEIGHT', 'CORRECTION', 'ADJUSTED HEIGHT', '', '', '']
        correction_table.append(correction_table_header)
        for index, point in enumerate(A_matrix_header):
            line_prov_height = provisional_height[point]
            line_cor = X_matrix[A_matrix_header.index(point)]
            line_adjust = line_prov_height + line_cor

            correction_table.append([point, line_prov_height, line_cor, line_adjust, "", "", ""])

        all_tables = decision_table + [['', '', '', '', '', '', '']] + correction_table
        all_tables.append(['', '', '', '', '', '', ''])
        all_tables.append(['DETAIL', '', '', '', '', '', ''])
        all_tables.append(['', '', '', '', '', '', ''])
        # all_tables.append(["A MATRIX HEADER", A_matrix_header, "", '', '', '', ''])
        all_tables.append(["A MATRIX", [A_matrix_header, ] + A_matrix.tolist()[:], "", '', '', '', ''])
        # all_tables.append(["L MATRIX LABEL", L_matrix_label, "", '', '', '', ''])
        all_tables.append(["L MATRIX", [L_matrix_label, ] + L_matrix.tolist()[:], "", '', '', '', ''])
        all_tables.append(["W MATRIX", W_matrix.tolist(), "", '', '', '', ''])
        all_tables.append(["Cx MATRIX", Cx_matrix.tolist(), "", '', '', '', ''])
        all_tables.append(["Cv MATRIX", Cv_matrix.tolist(), "", '', '', '', ''])
        all_tables.append(["VARIANCE", variance, "", '', '', '', ''])
        all_tables.append(["STANDARD DEVIATION", standard_deviation, "", '', '', '', ''])

        return all_tables

    def perform_computations(self):
        try:
            csv_data = self.build_tables()

        except:
            csv_data = None

        return csv_data


def save_csv_data(filepath, csv_data):
    # Note that the csv data must be list of lists
    csv_data_frame = pd.DataFrame(csv_data)

    csv_data_frame.to_csv(filepath, index=False, header=False)


if __name__ == "__main__":
    # old_file_path = "C:\\Users\\USER\\OneDrive\\Desktop\\adj_test_cs2.csv"
    # old_file_path = "C:\\Users\\USER\\OneDrive\\Desktop\\level_adjustment_input.csv"
    # new_file_path = "C:\\Users\\USER\\OneDrive\\Desktop\\level_adjustment_output.csv"
    # new_file_path = "C:\\Users\\USER\\OneDrive\\Desktop\\adj_test_csval.csv"
    old_file_path = "C:\\Users\\USER\\OneDrive\\Desktop\\L1.csv"
    new_file_path = "C:\\Users\\USER\\OneDrive\\Desktop\\L1_output.csv"
    matched_column = {"Point": "1", "Elevation": "3", "BM": "2", "From": "4",
                      "To": "5", "Change_elev": "6", "Weight": "7"}
    column = ["1", "2", "3", "4", "5", "6", "7"]

    aeno = LevelsAdjustment(old_file_path, True, column, matched_column, "1/W²", "99%")
    # matrices = aeno.generate_matrices()
    # print(pd.DataFrame(matrices['A_matrix']).values)
    # print(pd.DataFrame(matrices['L_matrix']).values)
    # print(pd.DataFrame(matrices['W_matrix']).values)
    # print(aeno.build_tables())
    print(save_csv_data(new_file_path, aeno.perform_computations()))


