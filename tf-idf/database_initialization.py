import os
import util
import sqlite3

conn = sqlite3.connect('data.db')

JOURNAL_CRALWED_FOLDER = os.path.join('link', 'journal')
CONFERENCE_CRALWED_FOLDER = os.path.join('link', 'conference')

conn.execute('''
    CREATE TABLE Page (
        Id INT PRIMARY KEY,
        Type INT,
        Short CHAR(50),
        Name CHAR(200)
    );
    ''')

conn.execute('''
    CREATE TABLE Pub (
        Id Int PRIMARY KEY,
        Title CHAR(500)
    );
    ''')

conn.excute('''
    CREATE TABLE PubPage (
        Id INT PRIMARY KEY,
        Pub Int,
        Page Int
    );
    ''')

cnt = 0
files = util.listdir(JOURNAL_CRALWED_FOLDER)
for file_name in files:
    data = util.load_json(os.path.join(JOURNAL_CRALWED_FOLDER, file_name))
    conn.execute('''
        INSERT INTO Page (Type, Short, Name)
        VALUES (%d, "%s", "%s");
        ''' % (util.PAGE_TYPE_JOURNAL, data['short'], data['name']))
    for short, sub in data['sub'].items():
        conn.execute('''
            INSERT INTO Page (Type, Short, Name)
            VALUES (%d, "%s", "%s");
            ''' % (util.PAGE_TYPE_JOURNAL_SUB, short, data['name']));

    cnt += 1
    print cnt, len(files)

cnt = 0
files = util.listdir(JOURNAL_CRALWED_FOLDER)
for file_name in files:
    data = util.load_json(os.path.join(JOURNAL_CRALWED_FOLDER, file_name))
    conn.execute('''
        INSERT INTO Page (Type, Short, Name)
        VALUES (%d, "%s", "%s");
        ''' % (util.PAGE_TYPE_JOURNAL, data['short'], data['short']))
    cnt += 1
    print cnt, len(files)

conn.commit()
conn.close()
