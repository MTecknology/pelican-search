#!/usr/bin/python
'''
A basic bottle app skeleton
'''

import bottle
import ConfigParser

from bottle.ext.sqlalchemy import SQLAlchemyPlugin
from sqlalchemy import create_engine, Column, Integer, Sequence, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sphinxalchemy.schema import Index, Attribute, ArrayAttribute


app = application = bottle.Bottle()


conf = ConfigParser.SafeConfigParser({
    'sphinx_server': '127.0.0.1',
    'sphinx_port': '9306',
    'sphinx_life': '900',
    'site_name': None})
conf.read('settings.cfg')

engine = create_engine(
    'sphinx+mysqldb://{}:{}'.format(
        conf.get('bottle', 'sphinx_server'),
        conf.get('bottle', 'sphinx_port')),
    pool_recycle=int(conf.get('bottle', 'sphinx_life')))
app.install(SQLAlchemyPlugin(engine))

documents = Index(conf.get('bottle', 'site_name'),
    MetaData(bind=engine),
    Attribute('title'),
    Attribute('author'),
    Attribute('url'),
    Attribute('summary'),
    Attribute('slug'))


@app.route('/static/<filename:path>')
def static(filename):
    '''
    Serve static files
    '''
    return bottle.static_file(filename, root='./static')


@app.route('/')
@app.route('/search')
@app.route('/search/')
def run_search(db):
    '''
    Run the search and return the results page
    '''
    search_terms = bottle.request.GET.get('q', None)

    if not search_terms:
        return bottle.jinja2_template('noresults.html')

    try:
        rows = db.execute(documents.select().match(search_terms.strip()))
    except:
        return 'Database error: please try your request again.'

    if rows.rowcount > 0:
        return bottle.jinja2_template('results.html', rows=rows)
    else:
        return bottle.jinja2_template('noresults.html')


class StripPathMiddleware(object):
    '''
    Get that slash out of the request
    '''
    def __init__(self, a):
        self.a = a
    def __call__(self, e, h):
        e['PATH_INFO'] = e['PATH_INFO'].rstrip('/')
        return self.a(e, h)


if __name__ == '__main__':
    bottle.run(app=StripPathMiddleware(app),
        host='0.0.0.0',
        port=8080)
