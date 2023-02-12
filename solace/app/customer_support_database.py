import sqlite3

CREATE_INQUIRY_TABLES = 'CREATE TABLE IF NOT EXISTS inquiry (id INTEGER PRIMARY KEY, name TEXT, method TEXT, rating INTEGER);'

INQUIRY_INSERT_QUERY = 'INSERT INTO inquiry (name, email, inquiry) VALUES (?, ?, ?)'

SELECT_EVERYTHING = 'SELECT * FROM inquiry'

