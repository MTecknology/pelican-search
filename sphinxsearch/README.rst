Pelican Search - sphinxsearch
=============================

This document explains how to get sphinxsearch running and how to get pelican
data into it to be searched.

Assumptions
-----------

Your site is at /var/www/MYSITE/

You are using MYSITE in sphinxsearch.

Installing SphinxSearch
-----------------------

It's usually best to let your package manager decide how to install packages,
but in this case, I prefer installing sphinxsearch manually.

If you choose to do it manually, I will assume that you are capable of following
what will differ for you in the documentation.

Compiling
~~~~~~~~~

One big reason you would choose to compile yourself is if your distro doesn't
provide xmlpipe2. I ended up needing to compile.

If you compile yourself, you will want *--with-xmlpipe2*::

    ./configure --without-mysql --with-xmlpipe2
    make install

You will now be using /usr/local/<foo> instead of /<foo>.

Configuring SphinxSearch
------------------------

Edit /etc/sphinx.conf

You will want this file to look like this::

    source MYSITE {
        type = xmlpipe2
        xmlpipe_command = cat /var/www/MYSITE/output/sphinxsearch.xml
        xmlpipe_fixup_utf8 = 1
        xmlpipe_field = content
        xmlpipe_attr_string = title
        xmlpipe_attr_string = author
        xmlpipe_attr_string = url
        xmlpipe_attr_multi = category
        xmlpipe_attr_string = summary
        xmlpipe_attr_string = slug
        xmlpipe_attr_timestamp = published
    }

    index MYSITE {
        type = plain
        source = MYSITE
        path = /usr/local/var/data/MYSITE
        charset_type = utf-8
        mlock = 1
        enable_star = 1
        expand_keywords = 1
        phrase_boundary = ., ?, !, U+2026 # horizontal ellipsis
        html_strip = 0
        preopen = 1
        # ondisk_dict = 1
    }

    indexer {
        mem_limit = 32M
        # max_xmlpipe2_field = 4M
        # on_file_field_error = skip_document
    }

    searchd {
        #listen = /var/run/searchd.sock
        listen = 9312
        listen = 9306:mysql41
        log = /var/log/searchd.log
        query_log = /var/log/query.log
        read_timeout = 5
        client_timeout = 300
        max_children = 30
        pid_file = /run/searchd.pid
        workers = threads
    }

Save that and follow with::

    indexer --all
    service searchd restart

Updating the Index
------------------

Any time you want to update the search index (after generating new content) run::

    indexer --rotate --quiet MYSITE

I personally prefer only updating once per day. In my root cron, I have::

    @daily /usr/local/bin/indexer --rotate --quiet MYSITE
