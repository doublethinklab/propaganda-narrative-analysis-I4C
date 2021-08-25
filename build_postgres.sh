#!/bin/bash

docker build \
    --no-cache \
    -f docker/pna-postgres.Dockerfile \
    -t doublethinklab/pna-postgres:latest \
    .
