from flask import Flask, jsonify, request, Response
from project.src.finding import Finding
from project.src.db_communicator.mysql_communicator import MySQLCommunicator
from project.src.db_communicator.communicator_exceptions import *

app = Flask(__name__)


@app.route("/finding/<finding_id>", methods=["GET", "DELETE"])
def get_or_delete_finding(finding_id: str):
    if request.method == "GET":
        try:
            finding = MySQLCommunicator.get_finding(finding_id)
            return jsonify(finding.to_dict())
        except FindingNotFoundError as e:
            return jsonify({"error": str(e)}), 404
    elif request.method == "DELETE":
        MySQLCommunicator.delete_finding(finding_id)
        return Response("Deleted Successfully", 200)


@app.route("/finding", methods=["POST"])
def upload_finding():
    json_data = request.json
    finding = Finding.create_from_json(json_data)
    MySQLCommunicator.upload_finding(finding)
    return "Success"


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
