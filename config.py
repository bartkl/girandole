from pathlib import Path


Config = {
    "flask_log_through_gunicorn": True,
    "cors": {
        "origins": '*'
    },
    "beets_web": {
        "jsonify_prettyprint_regular": False,
        "include_paths": False
    }
}