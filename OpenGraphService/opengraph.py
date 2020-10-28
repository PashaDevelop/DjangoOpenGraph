"""
Модуль для формирования OpenGraph по url
"""
import re

import json

from urllib import request
from bs4 import BeautifulSoup


class OpenGraph(dict):
    """
    Класс для работы с OpenGraph по url
    """
    required_attrs = ['title', 'type', 'image', 'url']
    scrape = False

    def __init__(self, url=None, html=None, scrape=False, **kwargs):
        self.scrape = scrape
        self._url = url
        self.new_param = kwargs.get('new_param')
        self._new_param2 = kwargs.get('new_param2')

        for k in kwargs:
            self[k] = kwargs[k]

        dict.__init__(self)

        if url is not None:
            self.fetch(url)

        if html is not None:
            self.parser(html)

    def __setattr__(self, name: str, val: str):
        self[name] = val

    def __getattr__(self, name: str):
        return self[name]

    def fetch(self, url: str) -> None:
        """
        Забирает HTMl разметку странички по url
        :param url:
        :return:
        """
        raw = request.urlopen(url)
        html = raw.read()
        self.parser(html)

    def parser(self, html: BeautifulSoup) -> None:
        """
        Забирает из HTML разметки нужные теги для формирования OpenGraph
        :param html:
        :return:
        """
        if not isinstance(html, BeautifulSoup):
            doc = BeautifulSoup(html)
        else:
            doc = html
        ogs = doc.html.head.findAll(property=re.compile(r'^og'))
        for og in ogs:
            self[og[u'property'][3:]] = og[u'content']

        if not self.is_valid() and self.scrape:
            for attr in self.required_attrs:
                if not hasattr(self, attr):
                    try:
                        self[attr] = getattr(self, 'scrape_%s' % attr)(doc)
                    except AttributeError:
                        pass

    def is_valid(self) -> bool:
        """
        Проверка валидность источника
        """
        return all([hasattr(self, attr) for attr in self.required_attrs])

    def to_json(self) -> str:
        """
        Экспортирует OpenGraph в формат json
        """
        import_json = True
        if not import_json:
            return "{'error':'there isn't json module'}"

        if not self.is_valid():
            return json.dumps({'error': 'og metadata is not valid'})

        return json.dumps(self)
