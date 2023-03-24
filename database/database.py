import sqlite3
from utils.paths import DATABASE_FOLDER_PATH

conn = sqlite3.connect(DATABASE_FOLDER_PATH + "database.db")
cur = conn.cursor()

cur.executescript('''

DROP TABLE IF EXISTS notes;
DROP TABLE IF EXISTS todos;

CREATE TABLE notes(note_id INTEGER UNIQUE NOT NULL PRIMARY KEY,
                    title TEXT, body TEXT, created_on TEXT, modified_on TEXT
                    );

CREATE TABLE todos(todo_id INTEGER UNIQUE NOT NULL PRIMARY KEY, 
                    task TEXT, description TEXT, assignees TEXT, start_on TEXT,
                    expected_end_on TEXT, status TEXT, actual_end_on TEXT, created_on TEXT,
                    modified_on TEXT
                    );

''')