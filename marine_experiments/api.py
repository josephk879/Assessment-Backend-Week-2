"""An API for handling marine experiments."""

from datetime import datetime

from flask import Flask, jsonify, request
from psycopg2 import sql

from database_functions import get_db_connection, get_experiments, delete_experiment


app = Flask(__name__)

"""
For testing reasons; please ALWAYS use this connection. 

- Do not make another connection in your code
- Do not close this connection

If you do not understand this instructions; as a coach to explain
"""
conn = get_db_connection("marine_experiments")


@app.get("/")
def home():
    """Returns an informational message."""
    return jsonify({
        "designation": "Project Armada",
        "resource": "JSON-based API",
        "status": "Classified"
    })


@app.route("/experiment", methods=["GET"])
def endpoint_get_experiment():
    """Create GET method for /experiment endpoint."""

    if request.method == "GET":
        type = request.args.get("experiment_type")
        score_over = request.args.get("specific_score")
        type = [type] or [
            "intelligence", "obedience", "aggression"]
        score_over = score_over or 0

        for e_type in type:
            if e_type not in ("intelligence", "obedience", "aggression"):
                raise ValueError("Invalid experiment type")

        if score_over < 0 or score_over > 100:
            raise ValueError("Invalid score.") 400

        experiments = get_experiments(conn, type, score_over)

        return experiments, 200


@app.route("/experiment/<int:id>", methods=["DELETE"])
def endpoint_delete_experiment(id: int):
    """Create DELETE method for /experiment/<int:id> endpoint."""

    if request.method == "DELETE":
        success = delete_experiment(conn, id)

        if not success:
            return {"error": f"Unable to locate experiment with ID {id}."}, 404

        return success, 200


if __name__ == "__main__":
    app.config["DEBUG"] = True
    app.config["TESTING"] = True

    app.run(port=8000, debug=True)

    conn.close()
