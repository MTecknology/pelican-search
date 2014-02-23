Pelican Search - pelican
========================

This document explains how to have pelican create the data needed for the search.

Assumptions
-----------

Your site is at /var/www/MYSITE/

Dependencies
------------

This plugin needs:

* BeautifulSoup4

Pelican Configuration
---------------------

Edit /var/www/MYSITE/pelicanconf.py

Add this to the configuration:

    TEMPLATE_PAGES = {'search_base.html': 'search_base.html'}
    PLUGINS = ['plugins.sphinxsearch']

Search Theme
------------

At minimum, you need a search_base.html in your theme. It would also be a good
idea to modify your theme so that it has a search box somewhere on your site.

search_base.html
~~~~~~~~~~~~~~~~

Edit /var/www/MYSITE/theme/templates/search_base.html

This is likely in another location. Where you create the file *will* have a
*base.html* file in it.

    {% extends "base.html" %}

    {% block headers %}
        {{ super() }}
    {% endblock %}

    {% block title %}Site Search — {{ super() }}{% endblock %}

    {%- block content %}{% raw %}
        {% block content %}
        {% endblock content %}
    {% endraw %}{% endblock content -%}

This template file (along with TEMPLATE_PAGES in your config) will generate
a *search_base.html* file in your *output* directory. This is needed when you
configure the bottle.py applicaiton.

theme modifications
~~~~~~~~~~~~~~~~~~~

You will want to add a search box to your site in some way. It is up to the
theme designer to decide how to do this. At a bare minimum, you will want
something that looks like this.

    <form id="search" method="get" action="/search">
        <input type="text" name="q" size="12" maxlength="120" />                                                                                                                        
        <br /><input type="submit" value="Search" />
    </form>

I won't be able to help further. I'm terrible at design.

Search Plugin
-------------

Now that the theme part is done, we need to add the plugin. Above, I used this:

    PLUGINS = ['plugins.sphinxsearch']

This implies that you have a */var/www/MYSITE/plugins* directory. If you do not,
I would suggest creating one. Inside of this directory is a 'sphinxsearch.py'
file. You will want to place this at */var/www/MYSITE/plugins/sphinxsearch.py*.
You will also want to make sure you have an empty *__init__.py* file inside.

Once the three pieces from above are done, run:

    pelican -c /var/www/MYSITE/pelicanconf.py

If all went well, you will see two extra files in your output directory:

* /var/www/MYSITE/output/search_base.html
* /var/www/MYSITE/output/sphinxsearch.xml

If you see them, then move on to the sphinxsearch section.
