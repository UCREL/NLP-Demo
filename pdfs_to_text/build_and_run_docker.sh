#!/bin/bash

export USER_ID=$(id -u)
export GROUP_ID=$(id -g)
export DOCKER_EXPORT_DIRECTORY=$PWD/../export_directory
mkdir -p $DOCKER_EXPORT_DIRECTORY
docker-compose --compatibility up --exit-code-from python
docker-compose down