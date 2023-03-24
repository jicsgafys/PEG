import pandas as pd

from utils.database import execute_db_query1
from utils.paths import DATABASE_FILE_PATH
import datetime


class AddNewTodo:
    def __init__(self,):

        self.current_datetime = str(datetime.datetime.now())
        self.query = "INSERT INTO todos VALUES(null, ?, ?, ?, ?, ?, ?, ?, ?, null);"

    def insert(self, task, description, assignees, start_date, expect_end_date,
               status, actual_end_data):
        parameters = (task, description, assignees, start_date, expect_end_date,
                      status, actual_end_data, self.current_datetime,)
        execute_db_query1(DATABASE_FILE_PATH, self.query, parameters)


class ModifyTodo:
    def __init__(self):
        self.current_datetime = str(datetime.datetime.now())
        self.query = "UPDATE todos SET task=?, description=?, assignees=?, " \
                     "start_on=?, expected_end_on=?, status=?, actual_end_on=?, " \
                     "modified_on=? WHERE todo_id=?;"

    def modify(self, todo_id, task, description, assignees, start_date, expect_end_date,
               status, actual_end_date):
        parameters = (task, description, assignees, start_date, expect_end_date,
                      status, actual_end_date, self.current_datetime, todo_id)
        execute_db_query1(DATABASE_FILE_PATH, self.query, parameters)


class RetrieveOneTodo:
    def __init__(self):
        """task TEXT, description TEXT, assignees TEXT, start_on TEXT,
                    expected_end_on TEXT, status TEXT, actual_end_on TEXT, created_on TEXT,
                    modified_on TEXT"""
        self.results_header = ['ID', 'TASK', 'DESCRIPTION', 'ASSIGNEES', 'START DATE', 'EXPECTED END DATE',
                               'STATUS', 'ACTUAL END DATE', 'CREATED ON', 'MODIFIED ON']

        self.query = "SELECT * FROM todos WHERE todo_id=?"

    def get_results_body(self, todo_id):
        parameters = (todo_id,)
        results = execute_db_query1(DATABASE_FILE_PATH, self.query, parameters).fetchone()

        return results

    def get_results_header(self):
        return self.results_header


class RetrieveAllTodos:
    def __init__(self):
        self.results_header = ['ID', 'TASK', 'DESCRIPTION', 'ASSIGNEES', 'START DATE', 'EXPECTED END DATE',
                               'STATUS', 'ACTUAL END DATE', 'CREATED ON', 'MODIFIED ON']

        self.query = "SELECT * FROM todos ORDER BY rowid DESC;"

    def get_results_body(self):
        results = execute_db_query1(DATABASE_FILE_PATH, self.query).fetchall()

        return results

    def get_results_header(self):
        return self.results_header


class DeleteTodo:
    def __init__(self):
        self.query = "DELETE FROM todos WHERE todo_id=?"

    def delete_data(self, todo_id):
        parameters = (todo_id, )
        execute_db_query1(DATABASE_FILE_PATH, self.query, parameters)


class SearchForTodo:
    def __init__(self):
        self.results_header = ['ID', 'TASK', 'DESCRIPTION', 'ASSIGNEES', 'START DATE',
                               'EXPECTED END DATE', 'STATUS', 'ACTUAL END DATE', 'CREATED ON',
                               'MODIFIED ON']

        self.query = "SELECT * FROM todos WHERE todo_id LIKE ? OR task LIKE ? OR description LIKE ? OR " \
                     "assignees LIKE ? OR start_on LIKE ? OR expected_end_on LIKE ? OR status LIKE ? OR " \
                     "actual_end_on LIKE ? OR created_on LIKE ? OR modified_on LIKE ? ORDER BY rowid DESC;"

    def get_results_body(self, search_term):
        parameters = ('%' + str(search_term) + '%', ) * 10

        results = execute_db_query1(DATABASE_FILE_PATH, self.query, parameters).fetchall()
        return results

    def get_results_header(self):
        return self.results_header


class ExportAllTodos:
    def __init__(self):
        self.data = RetrieveAllTodos()
        self.data_header = self.data.get_results_header()
        self.data_body = self.data.get_results_body()

    def export_as_csv(self, csv_path):
        data = self.data_body[:].insert(0, self.data_header)
        data_frame = pd.DataFrame(data=data, header=False, index=False)

        data_frame.to_csv(path_or_buf=csv_path)