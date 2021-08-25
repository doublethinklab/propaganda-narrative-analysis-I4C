#!/bin/bash

docker-compose \
    -f docker/compose-dev.yml \
    run \
        dtl-pna \
            python run_app.py

docker-compose \
    -f docker/compose-dev.yml \
    down
