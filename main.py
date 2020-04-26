import logging

import beets
import beets.ui
import beetsplug.web

import views
from config import Config


# Beets Web plugin Flask app initialization and configuration.
app = beetsplug.web.app
app.register_blueprint(views.girandole)

app.config['lib'] = beets.ui._open_library(beets.config)


# Logging.
if Config.get('flask_log_through_gunicorn'):
    gunicorn_error_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_error_logger.handlers
    app.logger.setLevel(gunicorn_error_logger.level)


# CORS.
if Config.get('cors'):
    app.logger.info(f"Enabling CORS.")

    from flask_cors import CORS
    
    app.config['CORS_ALLOW_HEADERS'] = "Content-Type"
    CORS(app, resources={
        r"/*": {'origins': Config['cors']['origins']}
    })


if __name__ == '__main__':
    app.run(threaded=True)

