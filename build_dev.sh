#!/bin/bash

docker build \
    --no-cache \
    -f docker/pna-dev.Dockerfile \
    -t doublethinklab/pna-dev:latest \
    .
