from utils.database import execute_db_query1
from utils.paths import DATABASE_FILE_PATH
import datetime
import pandas as pd


class AddNewNote:
    def __init__(self,):

        self.current_datetime = str(datetime.datetime.now())
        self.query = "INSERT INTO notes VALUES(null, ?, ?, ?, null);"

    def insert(self, title, body):
        parameters = (title, body, self.current_datetime, )
        execute_db_query1(DATABASE_FILE_PATH, self.query, parameters)


class ModifyNote:
    def __init__(self):
        self.current_datetime = str(datetime.datetime.now())
        self.query = "UPDATE notes SET title=?, body=?, modified_on=? WHERE note_id=?;"

    def modify(self, note_id, title, body):
        parameters = (title, body, self.current_datetime, note_id)
        execute_db_query1(DATABASE_FILE_PATH, self.query, parameters)


class RetrieveOneNote:
    def __init__(self):
        self.results_header = ['ID', 'TITLE', 'NOTES', 'CREATED ON', 'MODIFIED ON']

        self.query = "SELECT * FROM notes WHERE note_id=?"

    def get_results_body(self, note_id):
        parameters = (note_id, )
        results = execute_db_query1(DATABASE_FILE_PATH, self.query, parameters).fetchone()

        return results

    def get_results_header(self):
        return self.results_header


class RetrieveAllNotes:
    def __init__(self):
        self.results_header = ['ID', 'TITLE', 'NOTES', 'CREATED ON', 'MODIFIED ON']

        self.query = "SELECT * FROM notes ORDER BY rowid DESC;"

    def get_results_body(self):
        results = execute_db_query1(DATABASE_FILE_PATH, self.query).fetchall()

        return results

    def get_results_header(self):
        return self.results_header


class DeleteNote:
    def __init__(self):
        self.query = "DELETE FROM notes WHERE note_id=?"

    def delete_data(self, note_id):
        parameters = (note_id, )
        execute_db_query1(DATABASE_FILE_PATH, self.query, parameters)


class SearchForNote:
    def __init__(self):
        self.results_header = ['ID', 'TITLE', 'NOTES', 'CREATED ON', 'MODIFIED ON']

        self.query = "SELECT * FROM notes WHERE note_id LIKE ? OR title LIKE ? OR body LIKE ? OR " \
                     "created_on LIKE ? OR modified_on LIKE ? ORDER BY rowid DESC;"

    def get_results_body(self, search_term):
        parameters = ("%" + str(search_term) + "%", ) * 5

        results = execute_db_query1(DATABASE_FILE_PATH, self.query, parameters).fetchall()
        return results

    def get_results_header(self):
        return self.results_header


class ExportAllNotes:
    def __init__(self):
        self.data = RetrieveAllNotes()
        self.data_header = self.data.get_results_header()
        self.data_body = self.data.get_results_body()

    def export_as_csv(self, csv_path):
        data = self.data_body[:].insert(0, self.data_header)
        data_frame = pd.DataFrame(data=data, header=False, index=False)

        data_frame.to_csv(path_or_buf=csv_path)