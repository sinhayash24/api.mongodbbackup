import subprocess
from datetime import datetime, timezone

from flask import jsonify
from modules.config import MongoInstanceConfig


def perform_backup(mongo_config, dbname, backup_path):
    if not dbname:
        raise ValueError("Database name is required.")

    backup_name = f"{dbname}_{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}"

    try:
        subprocess.run(
            [
                "docker",
                "exec",
                mongo_config.container_name,
                "mongodump",
                "--uri",
                mongo_config.connection_string,
                "--db",
                dbname,
                f"--out=/backups/{backup_name}",
                "--gzip",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as error:
        message = error.stderr.strip() if error.stderr else str(error)
        raise RuntimeError(f"mongodump failed for '{dbname}': {message}") from error

    try:
        subprocess.run(
            [
                "docker",
                "cp",
                f"{mongo_config.container_name}:/backups/{backup_name}",
                backup_path,
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as error:
        message = error.stderr.strip() if error.stderr else str(error)
        raise RuntimeError(
            f"Failed to copy backup '{backup_name}' from the MongoDB container: {message}"
        ) from error

    return {
        "status": "success",
        "message": f"Backup created successfully: {backup_name}",
    }


def register_routes(app, key_vault_config, backup_path):
    @app.route("/backup/<mongoid>", methods=["POST"])
    def backup(mongoid):
        try:
            mongo_config = MongoInstanceConfig(
                mongoid,
                key_vault_config,
            )
            backups = [
                perform_backup(mongo_config, dbname, backup_path)
                for dbname in mongo_config.db_names
            ]
            return jsonify({
                "status": "success",
                "backups": backups,
            })

        except Exception as ex:
            return jsonify({
                "status": "error",
                "error": str(ex),
            }), 500
