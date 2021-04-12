#!/bin/bash

export USER_ID=$(id -u)
export GROUP_ID=$(id -g)
export DOCKER_EXPORT_DIRECTORY=$PWD/../export_directory
export TOKEN_STATISTICS_FILE=$PWD/../thesis_token_statistics.json
export TAG_STATISTICS_FILE=$PWD/../thesis_usas_tag_statistics.json
export USAS_CACHE_DIRECTORY=$PWD/usas_cache_directory
mkdir -p $DOCKER_EXPORT_DIRECTORY $USAS_CACHE_DIRECTORY
touch $TOKEN_STATISTICS_FILE $TAG_STATISTICS_FILE
docker-compose up --exit-code-from python
docker-compose down
docker rmi nlp_demo_token_tags_statistics:0.0.1