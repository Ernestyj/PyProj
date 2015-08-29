'''
Bottle-MySQL is a plugin that integrates MySQL with your Bottle
application. It automatically connects to a database at the beginning of a
request, passes the database handle to the route callback and closes the
connection afterwards.
To automatically detect routes that need a database connection, the plugin
searches for route callbacks that require a `db` keyword argument
(configurable) and skips routes that do not. This removes any overhead for
routes that don't need a database connection.
Results are returned as dictionaries.

Usage Example::
'''

__author__ = 'Kaiyang Lv'
__version__ = '0.0.1'
__license__ = None

import inspect
import bottle
import pymysql.cursors


class MySQLPlugin(object):
    '''
        This plugin passes a mysql database handle to route callbacks
    that accept a `db` keyword argument. If a callback does not expect
    such a parameter, no connection is made. You can override the database
    settings on a per-route basis.
    '''

    name = 'mysql'
    api = 2

    def __init__(self, dbuser=None, dbpass=None, dbname=None, dbhost='localhost', dbport=3306, keyword='db',
                 charset='utf8', dictrows=True, autocommit=True):
        self.dbuser = dbuser
        self.dbpass = dbpass
        self.dbname = dbname
        self.dbhost = dbhost
        self.dbport = dbport
        self.keyword = keyword
        self.dictrows = dictrows
        self.autocommit = autocommit
        self.charset = charset

    def setup(self, app):
        '''
        Make sure that other installed plugins don't affect the same keyword argument.
        '''
        for other in app.plugins:
            if not isinstance(other, MySQLPlugin):
                continue
            if other.keyword == self.keyword:
                raise PluginError("Found another mysql plugin with conflicting settings (non-unique keyword).")
            elif other.name == self.name:
                self.name += '_%s' % self.keyword

    def apply(self, callback, route):
        # Override global configuration with route-specific values.
        if 'mysql' in route.config:
            g = lambda key, default: route.config.get('mysql', {}).get(key, default)
        else:
            g = lambda key, default: route.config.get('mysql.' + key, default)
        dbuser = g('dbuser', self.dbuser)
        dbpass = g('dbpass', self.dbpass)
        dbname = g('dbname', self.dbname)
        dbhost = g('dbhost', self.dbhost)
        dbport = g('dbport', self.dbport)
        keyword = g('keyword', self.keyword)
        dictrows = g('dictrows', self.dictrows)
        autocommit = g('autocommit', self.autocommit)
        charset = g('charset', self.charset)

        # Test if the original callback accepts a 'db' keyword.
        # Ignore it if it does not need a database handle.
        _args = inspect.getargspec(route.callback)

        if keyword not in _args.args:
            return callback

        def wrapper(*args, **kwargs):
            con = None
            try:
                kw = {
                    'host': dbhost,
                    'user': dbuser,
                    'password': dbpass,
                    'db': dbname,
                    'charset': charset,
                    'port': dbport
                }

                if dictrows:
                    kw['cursorclass'] = pymysql.cursors.DictCursor

                con = pymysql.connect(**kw)

                cur = con.cursor()
            except bottle.HTTPResponse as e:
                raise bottle.HTTPError(500, 'Database Error', e)

            # Add the connection handle as a keyword argument.
            kwargs[keyword] = cur

            try:
                rv = callback(*args, **kwargs)
                if autocommit:
                    con.commit()
            except pymysql.IntegrityError as e:
                con.rollback()
                raise bottle.HTTPError(500, 'Database Error', e)
            except bottle.HTTPError:
                raise
            except bottle.HTTPResponse:
                if autocommit:
                    con.commit()
                raise
            finally:
                if con:
                    con.close()

            return rv

        return wrapper


Plugin = MySQLPlugin
