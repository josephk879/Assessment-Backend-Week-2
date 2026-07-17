"""Functions that interact with the database."""

from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection


def get_db_connection(dbname,
                      password="postgres") -> connection:
    """Returns a DB connection."""

    return connect(dbname=dbname,
                   host="localhost",
                   port=5432,
                   password=password,
                   cursor_factory=RealDictCursor)


def get_experiments(conn: connection, type: str | None,
                    score_over: int | None) -> list[dict]:
    """Returns a list of experiments from the database."""

    with conn.cursor() as cursor:
        query = f"""
    SELECT *
    FROM experiment AS E
    JOIN experiment_type AS ET
    WHERE ET.type_name = %(type)s
    AND E.score > %(score_over)s;
    """
        cursor.execute(
            query, {"type": type, "score_over": score_over})
        return cursor.fetchall()


def delete_experiment(conn: connection, id: int) -> dict | None:
    """Deletes an experiment and returns the deleted row."""
    with conn.cursor() as cursor:

        cursor.execute(
            """
            DELETE FROM experiment
            WHERE experiment_id = %(id)s
            RETURNING experiment_id, TO_CHAR(experiment_date, 'YYYY-MM-DD') AS experiment_date;
            """,
            {"id": id},
        )

        return cursor.fetchone()
