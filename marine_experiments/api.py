# pylint: disable=W0612
"""An API for handling marine experiments."""

from flask import Flask, jsonify, request
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
        type = request.args.get("type")
        score_over = request.args.get("score_over")
        valid_types = {"intelligence", "obedience", "aggression"}

        if type is not None:
            type = type.lower()

            if type not in valid_types:
                return {"error": "Invalid value for 'type' parameter"}, 400

        if score_over is not None:
            try:
                score_over = int(score_over)
            except ValueError:
                return {"error": "Invalid value for 'score_over' parameter"}, 400

            if score_over < 0 or score_over > 100:
                return {"error": "Invalid value for 'score_over' parameter"}, 400

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
