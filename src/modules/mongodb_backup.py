import subprocess
from flask import jsonify

def register_routes(app):

    @app.route("/backup", methods=["POST"])
    def backup():

        try:
            result = subprocess.run(
                ["docker", "ps"],
                capture_output=True,
                text=True
            )
    
            return jsonify({
                "status": "success",
                "output": result.stdout,
            })

        except Exception as ex:

            return jsonify({
                "status": "error",
                "error": str(ex),
            }), 500