from http import client
import json


# hh.ru требует обязательно указывать User-Agent
HEADERS = {"User-Agent": "MyCoolScript"}


class ParseException(Exception):
    pass


class Parser:

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

    def start(self):
        self.conn.request("GET", self.query, headers=HEADERS)
        resp = self.conn.getresponse()
        if resp.status == 200:
            self.status = resp.status
            string = resp.read().decode(encoding='utf-8')
            self._data = json.loads(string)
        else:
            raise ParseException


class VacanciesListParser(Parser):

    SUFFIX = '/vacancies/'
    PARAMS = {
        'text': 'python',
        'salary': 100000,
        'only_with_salary': True,
        'per_page': 500,
    }

    def __init__(self):
        super().__init__()
        self.items = []

    def start(self):
        self.items = []
        # hh.ru отдаёт не больше 500 вакансий за раз
        # поэтому загружаю их постранично
        page = 0
        stop = False
        while not stop:
            self.extra_params = {'page': page}
            super().start()
            items = self._data['items']
            if items:
                self.items += items
                page += 1
            else:
                stop = True








vp = VacanciesListParser()
vp.start()
print(vp.status)
print(len(vp.items))