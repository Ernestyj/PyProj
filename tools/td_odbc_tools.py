try:
    import pypyodbc as pyodbc
except ImportError:
    import pyodbc

import pandas as pd


class Teradata(object):
    """Teradata connection tools use odbc and pandas (for python 2.7)
    """

    _conn_pool = {}

    def __init__(self, host, user_name, password, database=None, table=None):
        super(Teradata, self).__init__()
        self.host = host
        self.user_name = user_name
        self.password = password
        self.database = database
        self.table = table

    def _get_conn(self):
        conn = self._conn_pool.get((self.host, self.user_name))
        if conn is None:
            conn = pyodbc.connect('DRIVER={{Teradata}};DBCNAME={};UID={};PWD={};'
                                  .format(self.host, self.user_name, self.password),
                                  ansi=True, unicode_results=False)
            # self._conn_pool[(self.host, self.user_name)] = conn
        return conn
    
    def query(self, query_string=None,
              select=None, distinct=False, where=None, order_by=None, ascend=True, limit=None,
              database=None, table=None):
        """
        Only for specific use. Run arbitary query and return a pandas table
        """
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
        result = pd.read_sql(query_string, self._get_conn())
        return result.rename(columns=str.upper)
    
    def upsert(self, dataframe, on=(), database=None, table=None):
        """
        Only for specific use.
        """
        if dataframe.shape[0] == 0:
            return
        database = database or self.database
        table = table or self.table
        query_insert_table_schema = ', '.join(dataframe.columns)
        query_insert_value_param = ', '.join(['?'] * dataframe.columns.size)
        if on:
            if isinstance(on, basestring):
                on = (on,)
            query_update_where_clause = ' AND '.join(col + ' = ?' for col in on)
            query_update_set_columns = list(dataframe.columns)
            for col in on:
                query_update_set_columns.remove(col)
            query_update_set_clause = ', '.join(col + ' = ?' for col in query_update_set_columns)
            query = \
                """
                UPDATE {database}.{table}
                    SET {query_update_set_clause}
                    WHERE {query_update_where_clause}
                ELSE
                    INSERT INTO {database}.{table} ({query_insert_table_schema})
                    VALUES ({query_insert_value_param});
                """.format(database=database, table=table,
                           query_update_set_clause=query_update_set_clause,
                           query_update_where_clause=query_update_where_clause,
                           query_insert_table_schema=query_insert_table_schema,
                           query_insert_value_param=query_insert_value_param)
        else:
            query = \
                """
                INSERT INTO {database}.{table} ({query_insert_table_schema})
                VALUES ({query_insert_value_param});
                """.format(database=database, table=table,
                           query_insert_table_schema=query_insert_table_schema,
                           query_insert_value_param=query_insert_value_param)
        conn = self._get_conn()
        cursor = conn.cursor()
        for i_row in xrange(dataframe.shape[0]):
            row = dataframe.iloc[i_row]
            query_params = []
            if on:
                query_params.extend(row[col] for col in query_update_set_columns)
                query_params.extend(row[col] for col in on)
            query_params.extend(row)
            cursor.execute(query, query_params)
        conn.commit()

    def delete(self, where=None, database=None, table=None):
        """
        Only for specific use. Run DELETE command.
        """
        database = database or self.database
        table = table or self.table
        conn = self._get_conn()
        cursor = conn.cursor()
        if where:
            query = \
                """
                DELETE FROM {database}.{table} WHERE {where};
                """.format(database=database, table=table, where=where)
        else:
            query = \
                """
                DELETE FROM {database}.{table};
                """.format(database=database, table=table)
        cursor.execute(query)
        conn.commit()
    
    def commit(self, query_string):
        """
        Only for specific use. Run arbitary command that needs commit.
        """
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute(query_string)
        conn.commit()