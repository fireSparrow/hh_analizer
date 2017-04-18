
from http import client
import json
from lxml import html


# hh.ru требует обязательно указывать User-Agent
HEADERS = {"User-Agent": "MyCoolScript"}


class ParseException(Exception):
    pass


class BaseParser:

    SUFFIX = ''
    PARAMS = {}
    extra_params = {}

    def __init__(self):
        self.conn = client.HTTPSConnection("api.hh.ru", 443)
        self.status = None
        self._data = {}

    @property
    def query(self):
        params = dict(self.PARAMS, **self.extra_params)
        pairs = ('{}={}'.format(k, v) for k, v in params.items())
        q = (self.SUFFIX + '?' + '&'.join(pairs))
        return q

    def run(self):
        self.conn.request("GET", self.query, headers=HEADERS)
        resp = self.conn.getresponse()
        if resp.status == 200:
            self.status = resp.status
            string = resp.read().decode(encoding='utf-8')
            self._data = json.loads(string)
        else:
            raise ParseException


class VacanciesListParser(BaseParser):

    SUFFIX = '/vacancies/'
    PARAMS = {
        'text': 'python',
        'salary': 100000,
        'only_with_salary': True,
        # 'per_page': 500,
        'per_page': 20,
    }

    def __init__(self):
        super().__init__()
        self.id_list = []

    def run(self):
        self.id_list = []
        # hh.ru отдаёт не больше 500 вакансий за раз
        # поэтому загружаю их постранично
        page = 0
        stop = False
        while not stop:
            self.extra_params = {'page': page}
            super().run()
            ids = [itm['id'] for itm in self._data['items']]
            if ids:
                self.id_list += ids
                page += 1
                # TODO: убрать из рабочей версии
                stop = True
            else:
                stop = True

    def __iter__(self):
        return iter(self.id_list)


class VacancyParser(BaseParser):

    def __init__(self, id_):
        super().__init__()
        self.SUFFIX = '/vacancies/' + id_
        self.key_skills = []
        self.ul_blocks = []

    def run(self):
        super().run()
        self.key_skills = [itm['name']
                           for itm in self._data['key_skills']]
        descr = self._data['description']
        tags_ul = html.fromstring(descr).xpath('ul')
        xpth = 'string(preceding-sibling::*[string(normalize-space())][1])'
        self.ul_blocks = {
            tag.xpath(xpth):
            [line for line in tag.xpath('li/text()')]
            for tag in tags_ul
        }
