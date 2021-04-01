#!/bin/bash

export USER_ID=$(id -u)
export GROUP_ID=$(id -g)
docker-compose --compatibility up --exit-code-from python
docker-compose down