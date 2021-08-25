#!/bin/bash

docker-compose -f docker/compose-prod.yml up

docker-compose -f docker/compose-prod.yml down
