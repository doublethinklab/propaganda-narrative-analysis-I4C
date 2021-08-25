FROM postgres:latest

# https://stackoverflow.com/questions/34751814/build-postgres-docker-container-with-initial-schema
COPY schema.sql /docker-entrypoint-initdb.d/
