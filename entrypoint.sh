#!/bin/sh
# Entrypoint script to make sure that container writes files as 
# the calling user of docker container.

USER_ID=${LOCAL_USER_ID:-9001}
getent passwd $USER_ID
adduser -s /bin/sh -u $USER_ID user -D ||true
echo "Starting with user: $USER_ID"

chown -R $USER_ID:$USER_ID /usr/share/pyntrest
cd /usr/share/pyntrest
exec su-exec $USER_ID ./manage.py "$@"
