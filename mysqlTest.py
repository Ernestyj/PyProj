import bottle
import bottle_mysql

app = bottle.Bottle()
# dbhost is optional, default is localhost
plugin = bottle_mysql.Plugin(dbuser='root', dbpass='root', dbname='community_server', dbhost='202.120.40.24',
                             dictrows=False)
plugin2 = bottle_mysql.Plugin(dbuser='root', dbpass='root', dbname='community_server', dbhost='202.120.40.24',
                             dictrows=False, keyword='rb')

app.install(plugin)
app.install(plugin2)


@app.route('/show/<item>', mysql={'dbname': 'community_server'})
def show(item, rb):
    print('hi')
    rb.execute('select * from user')
    row = rb.fetchone()
    if row:
        return bottle.template('<b>Hello {{name}}</b>!', name=row)
    return bottle.HTTPError(404, "Page not found")

app.run(host='localhost', port=8080)
