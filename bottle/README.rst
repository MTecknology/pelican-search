Pelican Search - bottle
-----------------------

This document explains how to set up the bottle.py application that will be
handling search requests. It also explains how to configure this to run behind
uwsgi so that Nginx can talk to it.

Assumptions
-----------

Your site is at /var/www/MYSITE/

You are using MYSITE in sphinxsearch.

Dependencies
------------

This python application requires:

* sqlalchemy
* sphinxalchemy
* bottle
* uwsgi
* uwsgi-plugin-python

Deploying the Application
-------------------------

In this directory is a bottleapp directory. Copy the contents to
*/var/www/MYSITE-search*. Edit */var/www/MYSITE-search/settings.cfg*.

The minimum you need in here is:

    [bottle]
    site_name=MYSITE

Optional settings (defaults):

    sphinx_server=127.0.0.1
    sphinx_port=9306
    sphinx_life=1800

Running with uwsgi
------------------

Edit /etc/uwsgi/apps-available/MYSITE-search.ini

    [uwsgi]
    socket = /run/uwsgi/app/MYSITE-search/socket
    chdir = /var/www/MYSITE-search
    master = true
    plugins = python
    file = app.py
    uid = www-data
    gid = www-data

Save that and follow with:

    service uwsgi restart


You know have a socket at /run/uwsgi/app/MYSITE-search/socket that Nginx is able
to communicate through to talk to your bottle application.
