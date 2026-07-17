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
    SELECT E.experiment_date, E.experiment_id, 
    ET.type_name AS experiment_type, E.score,
    SP.species_name, E.subject_id
    FROM experiment AS E
    JOIN experiment_type AS ET
        ON ET.experiment_type_id = E.experiment_type_id
    JOIN subject as SU
    ON SU.subject_id = E.subject_id
    JOIN species as SP
    ON SP.species_id = SU.species_id
    WHERE TRUE
    """
        params = {}

        if type is not None:
            query += " AND ET.type_name ILIKE %(type)s"
            params["type"] = type

        if score_over is not None:
            query += " AND E.score > %(score_over)s"
            params["score_over"] = score_over

        query += ";"

        cursor.execute(
            query, params)
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
