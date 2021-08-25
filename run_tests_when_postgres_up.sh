#!/bin/bash

python wait_for_postgres.py

if [ -z $1 ]
then
    python -m unittest discover tests
else
    python -m unittest $1
fi
