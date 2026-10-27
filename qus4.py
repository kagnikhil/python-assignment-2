
import re
import mysql.connector
from mysql.connector import Error


TABLES = {
    "student": {
        "table": "Student",
        "columns": {"id": "student_id", "name": "name", "spi": "spi"}
    },
    "course": {
        "table": "Course",
        "columns": {"id": "course_id", "name": "name"}
    },
    "registration": {
        "table": "CourseRegistration",
        "columns": {"student_id": "student_id", "course_id": "course_id"}
    }
}

FIELDS = {
    "student.id": "s.student_id",
    "student.name": "s.name",
    "student.spi": "s.spi",
    "course.id": "c.course_id",
    "course.name": "c.name",
    "registration.student_id": "r.student_id",
    "registration.course_id": "r.course_id"
}


def build_query(columns, filters, order_column, direction, limit):
    if not columns or any(col not in FIELDS for col in columns):
        raise ValueError("Invalid selected columns")

    if order_column not in FIELDS:
        raise ValueError("Invalid order column")

    if direction.upper() not in ("ASC", "DESC"):
        raise ValueError("Invalid sort direction")

    if not 1 <= limit <= 1000:
        raise ValueError("Limit must be between 1 and 1000")

    conditions = []
    params = []

    for field, operator, value in filters:
        if field not in FIELDS:
            raise ValueError("Invalid filter column")

        if operator not in ("=", ">", "<", ">=", "<=", "LIKE"):
            raise ValueError("Invalid operator")

        conditions.append(f"{FIELDS[field]} {operator} %s")
        params.append(value)

    select_fields = ", ".join(FIELDS[col] for col in columns)

    query = f"""
        SELECT {select_fields}
        FROM Student s
        JOIN CourseRegistration r ON s.student_id = r.student_id
        JOIN Course c ON r.course_id = c.course_id
    """

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += f" ORDER BY {FIELDS[order_column]} {direction.upper()} LIMIT %s"
    params.append(limit)

    return query, params


def main():
    conn = None

    try:
        user = input("MySQL username: ").strip()
        password = input("MySQL password: ")
        database = input("Database name: ").strip()

        conn = mysql.connector.connect(
            host="localhost",
            user=user,
            password=password,
            database=database
        )

        columns_input = input(
            "Columns (comma separated): "
        ).strip()

        columns = [x.strip().lower() for x in columns_input.split(",")]

        course_id = input("Course ID filter: ").strip()
        order_column = input("Order column: ").strip().lower()
        direction = input("Sort direction (ASC/DESC): ").strip().upper()
        limit = int(input("Limit (1-1000): "))

        filters = []
        if course_id:
            filters.append(("course.id", "=", course_id))

        query, params = build_query(
            columns, filters, order_column, direction, limit
        )

        print("SQL_OK")
        print("SQL template:", " ".join(query.split()))
        print("Parameters:", params)

        cursor = conn.cursor()
        cursor.execute(query, params)

        for row in cursor.fetchall():
            print(*row)

        cursor.close()

    except (Error, ValueError) as error:
        print("Error:", error)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()


if __name__ == "__main__":
    main()
