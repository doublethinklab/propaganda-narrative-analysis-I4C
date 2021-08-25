# https://stackoverflow.com/questions/17303531/check-if-postgresql-is-listening
import time

import psycopg2

from pna.dbi import get_connection


if __name__ == '__main__':
    ready = False
    while not ready:
        try:
            conn = get_connection()
            conn.close()
            ready = True
        except psycopg2.OperationalError:
            print('Waiting for server...')
            time.sleep(0.1)
