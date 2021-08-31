#!/bin/bash

docker-compose -f docker/compose-prod-windows.yml up

docker-compose -f docker/compose-prod-windows.yml down
