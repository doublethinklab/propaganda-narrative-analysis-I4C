#!/bin/bash

chmod 700 run_tests_when_postgres_up.sh

docker-compose \
    -f docker/compose-dev.yml \
    run \
        dtl-pna \
            ./run_tests_when_postgres_up.sh $1
docker-compose \
    -f docker/compose-dev.yml \
    down
