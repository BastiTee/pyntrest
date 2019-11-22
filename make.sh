#!/bin/bash
set -e
cd "$( cd "$( dirname "$0" )"; pwd )"

DOCKER_IMAGE="basti-tee/pyntrest"
docker build -t $DOCKER_IMAGE .

# docker run -ti --rm \
# -e LOCAL_USER_ID=`id -u $USER` \
# -p 8000:8000 \
# $DOCKER_IMAGE runserver localhost:8000

docker run --name nginx-pyntrest \
-p 8000:80 \
-v $(pwd)/sample_images:/usr/share/nginx/html:ro -ti --rm $DOCKER_IMAGE
