import sqlite3

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print('Connected to database')
    except Error as e:
        print(e)
    return conn

def select_all_students(conn):

    cur = conn.cursor()
    cur.execute("SELECT * FROM Students")

    rows = cur.fetchall()

    return rows


def select_student_by_studentID(conn, studentID):

    cur = conn.cursor()
    cur.execute("SELECT * FROM Students WHERE ID=?", (studentID,))

    rows = cur.fetchall()
    return rows

def insert_student(conn, student):
    sql = ''' INSERT INTO Students(ID, StudentName, Faculty, Year, Image, ImageURL)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, student)
    conn.commit()
    
    return cur.lastrowid


def convert_image_to_blob(file_path):
    with open(file_path, 'rb') as file:
        blob_data = file.read()
    return blob_data

def main():
    print('sql_query loaded')

if __name__ == '__main__':
    main()