
import csv
import mysql.connector
from mysql.connector import Error


def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Student (
            student_id INT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            spi DECIMAL(3,1) NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS CourseRegistration (
            student_id INT NOT NULL,
            course_id VARCHAR(20) NOT NULL,
            PRIMARY KEY (student_id, course_id),
            FOREIGN KEY (student_id) REFERENCES Student(student_id),
            INDEX idx_course (course_id)
        )
    """)

    conn.commit()
    cursor.close()


def import_students(conn, path):
    cursor = conn.cursor()

    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = []

        for row in reader:
            student_id = int(row["student_id"])
            name = row["name"].strip()
            spi = float(row["spi"])

            if not name or not 0 <= spi <= 10:
                raise ValueError("Invalid student data")

            rows.append((student_id, name, spi))

            if len(rows) >= 1000:
                cursor.executemany(
                    "INSERT INTO Student (student_id, name, spi) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE name=VALUES(name), spi=VALUES(spi)",
                    rows
                )
                conn.commit()
                rows.clear()

        if rows:
            cursor.executemany(
                "INSERT INTO Student (student_id, name, spi) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE name=VALUES(name), spi=VALUES(spi)",
                rows
            )

    conn.commit()
    cursor.close()


def import_registrations(conn, path):
    cursor = conn.cursor()

    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = []

        for row in reader:
            student_id = int(row["student_id"])
            course_id = row["course_id"].strip()

            if not course_id:
                raise ValueError("Invalid course ID")

            rows.append((student_id, course_id))

            if len(rows) >= 1000:
                cursor.executemany(
                    "INSERT IGNORE INTO CourseRegistration (student_id, course_id) VALUES (%s, %s)",
                    rows
                )
                conn.commit()
                rows.clear()

        if rows:
            cursor.executemany(
                "INSERT IGNORE INTO CourseRegistration (student_id, course_id) VALUES (%s, %s)",
                rows
            )

    conn.commit()
    cursor.close()


def display_students(conn, course_id, threshold):
    cursor = conn.cursor()

    query = """
        SELECT s.student_id, s.name, s.spi, r.course_id
        FROM Student s
        JOIN CourseRegistration r ON s.student_id = r.student_id
        WHERE r.course_id = %s AND s.spi > %s
        ORDER BY s.spi DESC, s.student_id ASC
    """

    cursor.execute(query, (course_id, threshold))

    for student_id, name, spi, course in cursor.fetchall():
        print(student_id, name, float(spi), course)

    cursor.close()


def main():
    conn = None

    try:
        host = input("MySQL host [localhost]: ").strip() or "localhost"
        user = input("MySQL username: ").strip()
        password = input("MySQL password: ")
        database = input("Database name: ").strip()

        if not user or not database:
            raise ValueError("Username and database are required")

        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        create_tables(conn)

        import_students(conn, input("Student CSV path: ").strip())
        import_registrations(conn, input("Registration CSV path: ").strip())

        course_id = input("Course ID: ").strip()
        threshold = float(input("SPI threshold: "))

        if not course_id or not 0 <= threshold <= 10:
            raise ValueError("Invalid course ID or SPI threshold")

        display_students(conn, course_id, threshold)

    except (Error, OSError, ValueError, KeyError) as error:
        print("Error:", error)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()


if __name__ == "__main__":
    main()
