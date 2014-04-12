Pelican Search
==============

This is a collection to add fast, dynamic, and scalable searching to a website
that was generated with `pelican`_. It uses `sphinxsearch`_ as the backend.

Background
----------

`Pelican`_ is a static website generatior. When it is done, the dynamic stuff
is all scripts that execute client side. This is not ideal when it comes to
searching your website.

Two options existed before now. The first was to use an external search service
such as Google to index your site and do the searching for you. The other option
is to generate a json file with your entire website. Any time a user wants to
search your site, they would have to download the javascript application and a
json dump of the entire content on your website and then run the search on their
own computers.

Downloading an entire dump of your website sucks if you have any reasonable
amount of content. It's the only option in some cases, but where it can be
avoided it should be.

Purpose
-------

The purpose of this project is to build a dynamic, scalable, and *fast* search
option for websites. My goal was to build something that would run without
issues on a server with as little as 128MB RAM. It's possible that this will run
well on less but I haven't testet it.

A little warning, we are creating an external search service and hosting it
ourselves. This is usually an incredibly complicated task. This project is half
documentation and half code.

Getting Prepared
----------------

The first thing you need is a functional Pelican website. If you need help with
this, please, see their `Getting Started`_ page.

Assumptions:

* You understand the basics of Linux
* You're using Nginx to host this site
* You can follow gaps in my instructions

Once you've read through the Pelican `Getting Started`_ page, you should also
take a look at my own `Pelican and Nginx`_ blog post. Once you've read and been
able to follow that, you will have a fully functional Pelican website running
behind Nginx. At this point, you're now ready to start adding search magic!

Getting Started
---------------

This project is divided into four sub-projects. Each directory relates to one
piece of the puzzle (documented sub-project). It's best to follow them in order.

* *pelican*: Get pelican generating what we need
* *sphinxsearch*: Get sphinxsearch reading the data pelican created
* *bottle*: Get the search application running
* *nginx*: Make search requests go to the search application

What Happens
------------

The end result is basically this:

* Pelican has extra pieces added to the theme
* Pelican creates a template for the Bottle application
* Pelican creates a dump of the entire site for SphinxSearch to index
* SphinxSearch indexes the site dump Pelican created
* SphinxSearch listens to a port for mysql connections
* Bottle is run by uwsgi
* Bottle takes search arguments in the query string with ?q=
* Bottle makes a connection to the mysql port SphinxSearch opened
* Bottle performs the search
* Bottle returns the search results, themed via the template file Pelican created
* Uwsgi runs the Bottle application
* Uwsgi creates a socket for Nginx to connect to
* Nginx passes /search requests to uwsgi
* User makes a request to Nginx

So:

* User <-> Nginx <-> Pelican (static files)
* User <-> Nginx <-> Uwsgi <-> Bottle <-> SphinxSearch
* Pelican -> <static file> <->SphinxSearch
* Pelican -> <static file> <-> Bottle

Adaptations
-----------

It would be perfectly viable to have pelican generate the XML file and run all
other dynamic pieces on a different server. You could even have the search box
generated send search requestst to search.yourdomain.tld. This would allow you
to host your Pelican site on a static service such as pages.github.com and run
the search on a cheap VPS.

I'd offer a service to run something like this, but that means you're no longer
in control and that obviously defeats a large purpose of this project.


To Do
-----

I'm still not really happy with this project. However, there's only so much any
one person can do. If you're interested, please see if you can help me with any
of the following.

* pelicanconf.py needs to be told to generate the search template, I don't like
  this.
* On first request, it's possible sphinxsearch dropped the connection, I need to
  figure out how to re-establish that connection without just letting the first
  request die.

.. _`pelican`: http://getpelican.com/
.. _`sphinxsearch`: http://sphinxsearch.com/
.. _`Getting Started`: http://docs.getpelican.com/en/3.3.0/getting_started.html
.. _`Pelican and Nginx`: http://michael.lustfield.net/nginx/blog-with-pelican-and-nginx
