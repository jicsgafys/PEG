import numpy as np
import pandas as pd


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


class ComputeLevels:
    def __init__(self, csv_path, first_row_as_header, csv_column_header,
                 matched_column_header, initial_TBM, final_TBM, misclose_m_value,
                 ):

        self.csv_path = csv_path
        self.first_row_as_header = first_row_as_header
        self.csv_column_header = csv_column_header
        self.matched_column = matched_column_header
        self.initial_TBM = initial_TBM
        self.final_TBM = final_TBM
        self.misclose_m_value = misclose_m_value
        self.misclosure = None
        self.file_data = None

        # self.reduce_levels_rf_data = None

    def read_csv_data(self):
        if self.first_row_as_header:
            self.file_data = pd.read_csv(filepath_or_buffer=self.csv_path, skiprows=1,
                                         header=None, names=self.csv_column_header).values
        else:
            self.file_data = pd.read_csv(filepath_or_buffer=self.csv_path, skiprows=0,
                                         header=None, names=self.csv_column_header).values


class ComputeLevelsRiseFall(ComputeLevels):
    def __init__(self, csv_path, first_row_as_header, csv_column_header,
                 matched_column_header, initial_TBM, final_TBM,
                 misclose_m_value):
        super().__init__(csv_path, first_row_as_header, csv_column_header,
                         matched_column_header, initial_TBM, final_TBM,
                         misclose_m_value)

    def compute_reduce_levels_method(self):
        self.initial_TBM = float(self.initial_TBM)
        self.final_TBM = float(self.initial_TBM)
        self.misclose_m_value = float(self.misclose_m_value)
        self.read_csv_data()

        new_csv_data = []
        new_csv_data_header = ["Remark", 'BS', 'IS', 'FS', 'RISE', 'FALL', 'Initial RL']
        new_csv_data.append(new_csv_data_header)

        active_height = None
        active_RL = self.initial_TBM
        for index, line in enumerate(self.file_data):
            new_csv_line_data = []
            Remark = str(line[self.csv_column_header.index(self.matched_column['Remark'])])
            BS = float(line[self.csv_column_header.index(self.matched_column['BS'])])
            IS = float(line[self.csv_column_header.index(self.matched_column['IS'])])
            FS = float(line[self.csv_column_header.index(self.matched_column['FS'])])
            rise = ""
            fall = ""
            RL = ""

            if index == 0:
                active_height = BS
                RL = active_RL
                active_RL = active_RL

            else:
                if not pd.isnull(IS):
                    change = active_height - IS
                    RL = active_RL + change

                    if change < 0:
                        fall = abs(change)
                    else:
                        rise = abs(change)

                    active_height = IS
                    active_RL = RL

                elif not pd.isnull(FS):
                    change = active_height - FS
                    RL = active_RL + change

                    if change < 0:
                        fall = abs(change)
                    else:
                        rise = abs(change)

                    active_height = BS
                    active_RL = RL

            new_csv_line_data.append(Remark)
            new_csv_line_data.append(BS)
            new_csv_line_data.append(IS)
            new_csv_line_data.append(FS)
            new_csv_line_data.append(rise)
            new_csv_line_data.append(fall)
            new_csv_line_data.append(RL)

            new_csv_data.append(new_csv_line_data)

        return new_csv_data

    def perform_error_checks(self, csv_data):
        # ["Remark", 'BS', 'IS', 'FS', 'RISE', 'FALL', 'Initial RL']
        checks_data = []

        csv_data = csv_data
        csv_header = csv_data[0]

        csv_data_frame = pd.DataFrame(csv_data[1:])
        csv_data_frame.replace("", np.nan, regex=True, inplace=True)

        BS_SUM = csv_data_frame[csv_header.index("BS")].sum()
        IS_SUM = csv_data_frame[csv_header.index("IS")].sum()
        FS_SUM = csv_data_frame[csv_header.index("FS")].sum()
        Rise_SUM = csv_data_frame[csv_header.index("RISE")].sum()
        Fall_SUM = csv_data_frame[csv_header.index("FALL")].sum()

        start_TBM = self.initial_TBM # csv_data[1][-1]
        end_TBM = csv_data[-1][-1]

        BS_FS_change = BS_SUM - FS_SUM
        Rise_Fall_change = Rise_SUM - Fall_SUM
        TBM_change = end_TBM - start_TBM

        checks_data.append(["", '', '', '', '', '', ''])
        checks_data.append(["CHECKS", '', '', '', '', '', ''])
        checks_data.append(["SUM", BS_SUM, IS_SUM, FS_SUM, Rise_SUM, Fall_SUM, ''])
        checks_data.append(["", '', '', '', '', '', ''])
        checks_data.append(["I_RL", self.initial_TBM, '', '', '', '', ''])
        checks_data.append(["F_RL", end_TBM, '', '', '', '', ''])
        checks_data.append(["SUM (BS - FS)", BS_FS_change, '', '', '', '', ''])
        checks_data.append(["SUM (RISE - FALL)", Rise_Fall_change, '', '', '', '', ''])
        checks_data.append(["(F_RL - I_RL)", TBM_change, '', '', '', '', ''])

        return checks_data

    def compute_misclosures(self, csv_data):
        # ["Remark", 'BS', 'IS', 'FS', 'RISE', 'FALL', 'Initial RL']
        misclosure_data = []

        csv_data = csv_data
        csv_header = csv_data[0]

        csv_data_frame = pd.DataFrame(csv_data[1:])
        csv_data_frame.replace("", np.nan, regex=True, inplace=True)

        end_TBM = csv_data[-1][-1]

        change_points = csv_data_frame[csv_header.index("FS")]
        misclose_n_value = sum([not pd.isnull(x) for x in change_points])

        allowable_misclosure = float(self.misclose_m_value) * (misclose_n_value ** 0.5)
        actual_misclosure = end_TBM - self.final_TBM

        misclosure_data.append(["", "", '', '', '', '', ''])
        misclosure_data.append(["MISCLOSURES", '', '', '', '', '', ''])
        misclosure_data.append(["START TBM", self.initial_TBM, '', '', '', '', ''])
        misclosure_data.append(["END TBM", self.final_TBM, '', '', '', '', ''])
        misclosure_data.append(["K", self.misclose_m_value, '', '', '', '', ''])
        misclosure_data.append(["N", misclose_n_value, '', '', '', '', ''])
        misclosure_data.append(["ALLOWABLE MISCLOSURE('K * sqrt(N))", allowable_misclosure, '', '', '', '', ''])
        misclosure_data.append(["ACTUAL MISCLOSURE(F_RL - END TBM)", actual_misclosure, '', '', '', '', ''])

        return misclosure_data

    def correct_reduce_levels(self, csv_data):
        # ["Adj", "Adj RL"]  Added two extra columns to make
        # ["Remark", 'BS', 'IS', 'FS', 'RISE', 'FALL', 'Initial RL', "Adj", "Adj RL"]

        csv_data = csv_data
        csv_header = csv_data[0]

        new_csv_header = list(csv_header) + ["Adj", "Adj RL"]  # Additional columns
        new_csv_data = []

        csv_data_frame = pd.DataFrame(csv_data[1:])
        csv_data_frame.replace("", np.nan, regex=True, inplace=True)

        end_TBM = csv_data[-1][-1]
        change_points = csv_data_frame[csv_header.index("FS")]
        no_of_inst_stations = sum([not pd.isnull(x) for x in change_points])

        actual_misclosure = end_TBM - self.final_TBM

        base_correction = (actual_misclosure / no_of_inst_stations) * -1

        change_point_count = 1
        for index, line in enumerate(csv_data_frame.values):
            initial_RL = line[csv_header.index("Initial RL")]
            FS = line[csv_header.index("FS")]
            error = base_correction * change_point_count
            line_adj_levels_data = list(line) + [error, initial_RL + error]
            if not pd.isnull(FS):
                change_point_count += 1

            if index == 0:
                line_adj_levels_data = list(line) + ['', initial_RL]
            new_csv_data.append(line_adj_levels_data)

        new_csv_data.insert(0, new_csv_header)

        return new_csv_data

    # def save_csv_data(self, filepath):
    #     reduce_levels = self.compute_reduce_levels_method()
    #     error_checks = self.perform_error_checks(reduce_levels)
    #     misclosures = self.compute_misclosures(reduce_levels)
    #     corrected_reduce_levels = self.correct_reduce_levels(reduce_levels)
    #
    #     csv_data = corrected_reduce_levels + error_checks + misclosures
    #
    #     csv_data_frame = pd.DataFrame(csv_data)
    #
    #     csv_data_frame.to_csv(filepath, index=False, header=False)

    def perform_computations(self):
        try:
            reduce_levels = self.compute_reduce_levels_method()
            error_checks = self.perform_error_checks(reduce_levels)
            misclosures = self.compute_misclosures(reduce_levels)
            corrected_reduce_levels = self.correct_reduce_levels(reduce_levels)

            csv_data = corrected_reduce_levels + error_checks + misclosures

        except:
            csv_data = None

        return csv_data


class ComputeLevelsHPC(ComputeLevels):
    def __init__(self, csv_path, first_row_as_header, csv_column_header,
                 matched_column_header, initial_TBM, final_TBM,
                 misclose_m_value):
        super().__init__(csv_path, first_row_as_header, csv_column_header,
                         matched_column_header, initial_TBM, final_TBM,
                         misclose_m_value)

    def compute_reduce_levels_method(self):
        self.initial_TBM = float(self.initial_TBM)
        self.final_TBM = float(self.initial_TBM)
        self.misclose_m_value = float(self.misclose_m_value)
        self.read_csv_data()

        new_csv_data = []
        new_csv_data_header = ["Remark", 'BS', 'IS', 'FS', 'HPC', 'Initial RL']
        new_csv_data.append(new_csv_data_header)

        active_HPC = None
        for index, line in enumerate(self.file_data):
            new_csv_line_data = []
            Remark = str(line[self.csv_column_header.index(self.matched_column['Remark'])])
            BS = float(line[self.csv_column_header.index(self.matched_column['BS'])])
            IS = float(line[self.csv_column_header.index(self.matched_column['IS'])])
            FS = float(line[self.csv_column_header.index(self.matched_column['FS'])])
            HPC = ""
            RL = ""

            if index == 0:
                RL = self.initial_TBM
                active_HPC = BS + self.initial_TBM
                HPC = active_HPC

            else:
                if not pd.isnull(IS):
                    RL = active_HPC - IS
                    HPC = active_HPC

                elif not pd.isnull(FS):
                    RL = active_HPC - FS

                    # Note
                    if not pd.isnull(BS):
                        active_HPC = RL + BS
                    else:
                        active_HPC = ""

                    HPC = active_HPC

            new_csv_line_data.append(Remark)
            new_csv_line_data.append(BS)
            new_csv_line_data.append(IS)
            new_csv_line_data.append(FS)
            new_csv_line_data.append(HPC)
            new_csv_line_data.append(RL)

            new_csv_data.append(new_csv_line_data)

        return new_csv_data

    def perform_error_checks(self, csv_data):
        # ["Remark", 'BS', 'IS', 'FS', 'RISE', 'FALL', 'Initial RL']
        checks_data = []

        csv_data = csv_data
        csv_header = csv_data[0]

        csv_data_frame = pd.DataFrame(csv_data[1:])
        csv_data_frame.replace("", np.nan, regex=True, inplace=True)

        BS_SUM = csv_data_frame[csv_header.index("BS")].sum()
        IS_SUM = csv_data_frame[csv_header.index("IS")].sum()
        FS_SUM = csv_data_frame[csv_header.index("FS")].sum()
        HPC_SUM = csv_data_frame[csv_header.index("HPC")].sum()
        Initial_RL_SUM = csv_data_frame[csv_header.index("Initial RL")].sum()

        start_TBM = self.initial_TBM  # csv_data[1][-1]
        end_TBM = csv_data[-1][-1]

        BS_FS_change = BS_SUM - FS_SUM
        TBM_change = end_TBM - start_TBM

        checks_data.append(["", '', '', '', '', ''])
        checks_data.append(["CHECKS", '', '', '', '', ''])
        checks_data.append(["SUM", BS_SUM, IS_SUM, FS_SUM, HPC_SUM, Initial_RL_SUM])
        checks_data.append(["", '', '', '', '', ''])
        checks_data.append(["I_RL", self.initial_TBM, '', '', '', ''])
        checks_data.append(["F_RL", end_TBM, '', '', '', ''])
        checks_data.append(["SUM (BS - FS)", BS_FS_change, '', '', '', ''])
        checks_data.append(["(F_RL - I_RL)", TBM_change, '', '', '', ''])
        checks_data.append(["SUM (I_RL + BS + FS) - F_RL",
                            Initial_RL_SUM + IS_SUM + FS_SUM - self.initial_TBM, '', '', '', ''])
        checks_data.append(["SUM (HPC)", HPC_SUM, '', '', '', ''])

        return checks_data

    def compute_misclosures(self, csv_data):
        # ["Remark", 'BS', 'IS', 'FS', 'RISE', 'FALL', 'Initial RL']
        misclosure_data = []

        csv_data = csv_data
        csv_header = csv_data[0]

        csv_data_frame = pd.DataFrame(csv_data[1:])
        csv_data_frame.replace("", np.nan, regex=True, inplace=True)

        end_TBM = csv_data[-1][-1]

        change_points = csv_data_frame[csv_header.index("FS")]
        misclose_n_value = sum([not pd.isnull(x) for x in change_points])

        allowable_misclosure = self.misclose_m_value * (misclose_n_value ** 0.5)
        actual_misclosure = end_TBM - self.final_TBM

        misclosure_data.append(["", "", '', '', '', '', ''])
        misclosure_data.append(["MISCLOSURES", '', '', '', '', '', ''])
        misclosure_data.append(["START TBM", self.initial_TBM, '', '', '', '', ''])
        misclosure_data.append(["END TBM", self.final_TBM, '', '', '', '', ''])
        misclosure_data.append(["K", self.misclose_m_value, '', '', '', '', ''])
        misclosure_data.append(["N", misclose_n_value, '', '', '', '', ''])
        misclosure_data.append(["ALLOWABLE MISCLOSURE('K * sqrt(N))", allowable_misclosure, '', '', '', '', ''])
        misclosure_data.append(["ACTUAL MISCLOSURE(F_RL - END TBM)", actual_misclosure, '', '', '', '', ''])

        return misclosure_data

    def correct_reduce_levels(self, csv_data):
        # ["Adj", "Adj RL"]  Added two extra columns to make
        # ["Remark", 'BS', 'IS', 'FS', 'RISE', 'FALL', 'Initial RL', "Adj", "Adj RL"]

        csv_data = csv_data
        csv_header = csv_data[0]

        new_csv_header = list(csv_header) + ["Adj", "Adj RL"]  # Additional columns
        new_csv_data = []

        csv_data_frame = pd.DataFrame(csv_data[1:])
        csv_data_frame.replace("", np.nan, regex=True, inplace=True)

        end_TBM = csv_data[-1][-1]
        change_points = csv_data_frame[csv_header.index("FS")]
        no_of_inst_stations = sum([not pd.isnull(x) for x in change_points])

        actual_misclosure = end_TBM - self.final_TBM

        base_correction = (actual_misclosure / no_of_inst_stations) * -1

        change_point_count = 1
        for index, line in enumerate(csv_data_frame.values):
            initial_RL = line[csv_header.index("Initial RL")]
            FS = line[csv_header.index("FS")]
            error = base_correction * change_point_count
            line_adj_levels_data = list(line) + [error, initial_RL + error]
            if not pd.isnull(FS):
                change_point_count += 1

            if index == 0:
                line_adj_levels_data = list(line) + ['', initial_RL]
            new_csv_data.append(line_adj_levels_data)

        new_csv_data.insert(0, new_csv_header)

        return new_csv_data

    def perform_computations(self):
        try:
            reduce_levels = self.compute_reduce_levels_method()
            error_checks = self.perform_error_checks(reduce_levels)
            misclosures = self.compute_misclosures(reduce_levels)
            corrected_reduce_levels = self.correct_reduce_levels(reduce_levels)

            csv_data = corrected_reduce_levels + error_checks + misclosures

        except:
            csv_data = None

        return csv_data


def save_csv_data(filepath, csv_data):
    # Note that the csv data must be list of lists
    csv_data_frame = pd.DataFrame(csv_data)

    csv_data_frame.to_csv(filepath, index=False, header=False)

    #
    # def save_csv_data(self, filepath):
    #     reduce_levels = self.compute_reduce_levels_method()
    #     error_checks = self.perform_error_checks(reduce_levels)
    #     misclosures = self.compute_misclosures(reduce_levels)
    #     corrected_reduce_levels = self.correct_reduce_levels(reduce_levels)
    #
    #     csv_data = corrected_reduce_levels + error_checks + misclosures
    #
    #     csv_data_frame = pd.DataFrame(csv_data)
    #
    #     csv_data_frame.to_csv(filepath, index=False, header=False)


if __name__ == "__main__":
    old_file_path = "C:\\Users\\USER\\OneDrive\\Desktop\\rise_fall_original.csv"
    new_file_path = "C:\\Users\\USER\\OneDrive\\Desktop\\rise_fall_new.csv"
    # matched_column = {"BS": "BS", "IS": "IS", "FS": "FS", "Rise": "Rise",
    #                   "Fall": "Fall", "Initial RL": "Initial RL", "Adj": "Adj",
    #                   "Adj RL": "Adj RL", "Remark": "Remark"}
    # column = ["BS", "IS", "FS", "Rise", "Fall", "Initial RL", "Adj",
    #           "Adj RL", "Remark"]
    matched_column = {"BS": "1", "IS": "2", "FS": "3", "Rise": "4",
                      "Fall": "5", "Initial RL": "6", "Adj": "7",
                      "Adj RL": "8", "Remark": "9"}
    column = ["1", "2", "3", "4", "5", "6", "7",
              "8", "9"]
    # a = ComputeLevelsHPC(old_file_path, True, column, matched_column, 49.873, 48.710,
    #                           5, 'pC', 'aRL')
    # a.save_csv_data(new_file_path)