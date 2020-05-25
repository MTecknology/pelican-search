# -*- coding: utf-8 -*-

'''
Sphinx Search
-------------

This pelican plugin generates an xmlpipe2 formatted file that can be used by the
sphinxsearch indexer to index the entire site.
'''

from __future__ import unicode_literals

import os.path
from bs4 import BeautifulSoup
from codecs import open
from datetime import datetime
import zlib

from pelican import signals


class sphinxsearch_xml_generator(object):

    def __init__(self, context, settings, path, theme, output_path, *null):

        self.output_path = output_path
        self.context = context
        self.siteurl = settings.get('SITEURL')
        self.dict_nodes = []

    def build_data(self, page):

        if getattr(page, 'status', 'published') != 'published':
            return

        soup_title = BeautifulSoup(page.title.replace('&nbsp;', ' '))
        page_title = soup_title.get_text(' ', strip=True).replace('“', '"').replace('”', '"').replace('’', "'").replace('^', '&#94;')

        soup_text = BeautifulSoup(page.content)
        page_text = soup_text.get_text(' ', strip=True).replace('“', '"').replace('”', '"').replace('’', "'").replace('¶', ' ').replace('^', '&#94;')
        page_text = ' '.join(page_text.split())

        if getattr(page, 'category', 'None') == 'None':
            page_category = ''
        else:
            page_category = page.category.name

        page_url = self.siteurl + '/' + page.url

        page_time = getattr(page, 'date', datetime(1970, 1, 1, 1, 0)).strftime('%s')

        # There may be possible collisions, but it's the best I can think of.
        page_index = abs(zlib.crc32((page_time + page_url).encode('utf-8')))

        return {'title':  page_title,
                'author': page.author,
                'tags': page_category,
                'url': page_url,
                'content': page_text,
                'slug': page.slug,
                'time': page_time,
                'index': page_index,
                'summary': page.summary}


    def generate_output(self, writer):
        path = os.path.join(self.output_path, 'sphinxsearch.xml')

        pages = self.context['pages'] + self.context['articles']

        for article in self.context['articles']:
            pages += article.translations

        with open(path, 'w', encoding='utf-8') as fd:
            fd.write('<?xml version="1.0" encoding="utf-8"?><sphinx:docset>')
            for page in pages:
                data = self.build_data(page)
                fd.write(
                    '<sphinx:document id="{0}">'
                    '<title>{1}</title>'
                    '<author>{2}</author>'
                    '<category>{3}</category>'
                    '<url>{4}</url>'
                    '<content><![CDATA[{5}]]></content>'
                    '<summary><![CDATA[{6}]]></summary>'
                    '<slug>{7}</slug>'
                    '<published>{8}</published>'
                    '</sphinx:document>'.format(
                        data['index'], data['title'], data['author'],
                        data['tags'], data['url'], data['content'],
                        data['summary'], data['slug'], data['time']))
            fd.write('</sphinx:docset>')
        fd.closed


def get_generators(generators):
    return sphinxsearch_xml_generator


def register():
    signals.get_generators.connect(get_generators)
