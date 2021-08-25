#!/bin/bash

docker build \
    $1 \
    -f docker/pna-dev.Dockerfile \
    -t doublethinklab/pna-dev:latest \
    .
