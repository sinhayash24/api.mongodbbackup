import subprocess
from datetime import date
from flask import jsonify

def perform_backup():

    datestamp = date.today().isoformat()

    backup_name = f"mongo_backup_{datestamp}"

    subprocess.run(
        [
            "docker",
            "exec",
            "mongo",
            "mongodump",
            "--host=localhost:27017",
            f"--out=/backups/{backup_name}"
            "--gzip"
        ],
        check=True
    )

    subprocess.run(
        [
            "docker",
            "cp",
            f"mongo:/backups/{backup_name}",
            "/home/azureuser/mongo-backups/."
        ],
        check=True
    )

    return {
        "status": "success",
        "message": f"Backup created successfully: {backup_name}"
    }


def register_routes(app):

    @app.route("/backup", methods=["POST"])
    def backup():

        try:  
            return jsonify(perform_backup())

        except Exception as ex:

            return jsonify({
                "status": "error",
                "error": str(ex),
            }), 500