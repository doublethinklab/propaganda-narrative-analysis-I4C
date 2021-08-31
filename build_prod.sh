#!/bin/bash

docker build \
    -f docker/pna.Dockerfile \
    -t doublethinklab/pna:latest \
    .
