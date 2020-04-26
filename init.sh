#!/bin/bash

# Make sure the config files are visible to the appropriate applications.
if [ -f /app/config/whatlastgenre.conf ]; then
		mkdir /root/.whatlastgenre
        ln -s /app/config/whatlastgenre.conf /root/.whatlastgenre/config
fi
if [ -f /app/config/beets.yaml ]; then
		mkdir -p /root/.config/beets
        ln -s /app/config/beets.yaml /root/.config/beets/config.yaml
fi

# Start the web server.
uvicorn --host 0.0.0.0 --port 8080 girandole.app.main:app