Pelican Search - nginx
======================

This document explains how to have Nginx pass search requests to the search
application written in bottle.

Assumptions
-----------

You have the three previous steps working.

Nginx Configuration
-------------------

Edit /etc/nginx/sites-available/<yoursite>

To your *server* block, add this::

    location ^~ /search {
        include uwsgi_params;
        uwsgi_pass unix:/run/uwsgi/app/MYSITE-search/socket;
    }

Save that and follow with::

    service nginx restart
