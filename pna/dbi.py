import os

import pandas as pd
import psycopg2
from psycopg2 import errors


def get_connection():
    return psycopg2.connect(
        host=os.environ['PGSQL_HOST'],
        port=os.environ['PGSQL_PORT'],
        user=os.environ['PGSQL_USERNAME'],
        password=os.environ['PGSQL_PASSWORD'],
        dbname=os.environ['PGSQL_DB'])


class Repository:

    def all(self, *args, **kwargs):
        raise NotImplementedError

    def create(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError


class NarrativeRepository(Repository):

    def all(self) -> pd.DataFrame:
        with get_connection() as conn:
            sql = 'SELECT * FROM narrative;'
            df = pd.read_sql_query(sql, con=conn)
            return df

    def create(self, code: str, description: str) -> None:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                sql = 'INSERT INTO narrative (code, description) ' \
                      'VALUES (%s, %s)'
                args = (code, description)
                try:
                    cursor.execute(sql, args)
                except errors.UniqueViolation:
                    pass  # it's in there, that's all we need

    def delete(self, code: str) -> None:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                sql = 'DELETE FROM narrative WHERE code = %s;'
                args = (code,)
                cursor.execute(sql, args)


class NarrativeLabelRepository(Repository):

    def all(self) -> pd.DataFrame:
        with get_connection() as conn:
            sql = 'SELECT ' \
                  '    nl.narrative_code, nl.annotator, nl.text, n.description ' \
                  'FROM narrative_label AS nl ' \
                  'INNER JOIN narrative AS n ON n.code = nl.narrative_code;'
            df = pd.read_sql_query(sql, con=conn)
            return df

    def create(self, narrative_code: str, annotator: str, text: str) -> None:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                sql = 'INSERT INTO narrative_label ' \
                      '(narrative_code, annotator, text) ' \
                      'VALUES (%s, %s, %s)'
                args = (narrative_code, annotator, text)
                cursor.execute(sql, args)

    def delete(self, narrative_code: str, annotator: str, text: str) -> None:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                sql = 'DELETE FROM narrative_label ' \
                      'WHERE narrative_code = %s ' \
                      'AND annotator = %s ' \
                      'AND text = %s;'
                args = (narrative_code, annotator, text)
                cursor.execute(sql, args)


class Dbi:

    def __init__(self):
        self.narratives = NarrativeRepository()
        self.narrative_labels = NarrativeLabelRepository()
