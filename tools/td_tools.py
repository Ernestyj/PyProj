# -*- coding: utf-8 -*-
# author: Raychee

import teradata
import pandas as pd

class Teradata(object):

    pooling = True

    config = {
        "appName": __name__ + '.Teradata',
        "version": '1.0',
        "runNumber": "0",
        "configureLogging": False
    }

    _pool = {}

    def __init__(self, host, user_name, password, database=None, table=None, **connect_kwargs):
        super(Teradata, self).__init__()
        self.host = host
        self.user_name = user_name
        self.password = password
        self.database = database
        self.table = table

        self.connect_kwargs = connect_kwargs.copy()
        self.connect_kwargs['method'] = self.connect_kwargs.get('method', 'odbc')

    @property
    def session(self):
        session = None
        if self.pooling:
            session = self._pool.get((self.host, self.user_name))
        if session is None:
            session = self._new_session()
            if self.pooling:
                self._pool[(self.host, self.user_name)] = session
        return session

    def query(self, query_string=None,
              select=None, distinct=False, where=None, order_by=None, ascend=True, limit=None,
              database=None, table=None,
              **kwargs):
        if query_string is None:
            if database is None: database = self.database
            if table is None: table = self.table
            clause_select = 'SELECT {} {} {}'.format('DISTINCT' if distinct else '',
                                                     '' if limit is None else 'TOP {}'.format(limit),
                                                     '*' if select is None else select)
            clause_from = 'FROM {}.{}'.format(database, table)
            clause_where = '' if where is None else 'WHERE {}'.format(where)
            clause_order_by = '' if order_by is None else 'ORDER BY {} {}'.format(order_by, 'ASC' if ascend else 'DESC')
            query_string = ' '.join((clause_select, clause_from, clause_where, clause_order_by)) + ';'
        return self._handle_execute(self._query, query_string, **kwargs)

    def upsert(self, data_frame, on=(), database=None, table=None, chunk_size=None, **kwargs):  # frequent used kwargs: batch=True
        if data_frame.shape[0] == 0:
            return
        database = database or self.database
        table = table or self.table
        query_insert_table_schema = ', '.join(data_frame.columns)
        query_insert_value_param = ', '.join(['?'] * data_frame.columns.size)
        if on:
            if isinstance(on, str):
                on = (on,)
            query_update_where_clause = ' AND '.join(col + ' = ?' for col in on)
            query_update_set_columns = list(data_frame.columns)
            for col in on:
                query_update_set_columns.remove(col)
            query_update_set_clause = ', '.join(col + ' = ?' for col in query_update_set_columns)
            query = \
                "UPDATE {database}.{table} " \
                "  SET {query_update_set_clause} " \
                "  WHERE {query_update_where_clause} " \
                "ELSE " \
                "  INSERT INTO {database}.{table} ({query_insert_table_schema}) " \
                "  VALUES ({query_insert_value_param}); ".format(database=database, table=table,
                                                                 query_update_set_clause=query_update_set_clause,
                                                                 query_update_where_clause=query_update_where_clause,
                                                                 query_insert_table_schema=query_insert_table_schema,
                                                                 query_insert_value_param=query_insert_value_param)
        else:
            query = "INSERT INTO {database}.{table} ({query_insert_table_schema}) " \
                    "VALUES ({query_insert_value_param});".format(database=database, table=table,
                                                                  query_insert_table_schema=query_insert_table_schema,
                                                                  query_insert_value_param=query_insert_value_param)

        def query_params(row):
            params = []
            if on:
                params.extend(row[col] for col in query_update_set_columns)
                params.extend(row[col] for col in on)
            params.extend(row)
            return [None if pd.isnull(v) or isinstance(v, float) and pd.np.isinf(v) else v for v in params]

        if chunk_size is None:
            chunk_size = data_frame.shape[0]

        chunk_pos = 0
        while chunk_pos < data_frame.shape[0]:
            data_chunk = data_frame.iloc[chunk_pos:chunk_pos + chunk_size]
            all_query_params = [query_params(row) for index, row in data_chunk.iterrows()]
            self._handle_execute(self._execute_many, query, all_query_params, **kwargs)
            chunk_pos += chunk_size

    def delete(self, where=None, database=None, table=None):
        database = database or self.database
        table = table or self.table
        if where:
            query = "DELETE FROM {database}.{table} WHERE {where};".format(database=database, table=table, where=where)
        else:
            query = "DELETE FROM {database}.{table};".format(database=database, table=table)
        self._handle_execute(self._execute, query)

    def execute(self, *args, **kwargs):
        return self._handle_execute(self._execute, *args, **kwargs)

    def __repr__(self):
        kwargs = [('host', self.host), ('user_name', self.user_name), ('password', self.password),
                  ('database', self.database), ('table', self.table)]
        kwargs.extend(self.connect_kwargs.items())
        return '{}({})'.format(type(self).__name__, ', '.join('{}={!r}'.format(k, v) for k, v in kwargs))

    def _handle_execute(self, execute_fn, *args, **kwargs):
        try:
            return execute_fn(*args, **kwargs)
        except teradata.DatabaseError as err:
            if self.pooling and err.code == 32 and err.sqlState == '08S01':
                self._pool[(self.host, self.user_name)] = self._new_session()
                return execute_fn(*args, **kwargs)
            raise err

    def _new_session(self):
        uda = teradata.UdaExec(**self.config)
        return uda.connect(system=self.host, username=self.user_name, password=self.password, **self.connect_kwargs)

    def _query(self, *args, **kwargs):
        cursor = self.session.execute(*args, **kwargs)
        data = cursor.fetchall()
        if len(cursor.description) == 1 and cursor.description[0][0] in ('RequestText', 'Request Text'):
            result = ''.join(row.values[0] for row in data)
        else:
            result = pd.DataFrame.from_records(data, columns=[d[0] for d in cursor.description])
        return result

    def _execute_many(self, *args, **kwargs):
        return self.session.executemany(*args, **kwargs)

    def _execute(self, *args, **kwargs):
        return self.session.execute(*args, **kwargs)