
from collections import namedtuple
import re

from gensim import corpora, models
from pymorphy2 import MorphAnalyzer

morph = MorphAnalyzer()


Point = namedtuple('Point', 'x, y, power')


def calc_2d_projection(data):

    """ Размещает токены в двухмерном пространстве
        с учётом того, насколько часто они встречаются вместе

        :param data: Список списков токенов.
        :return: Словарь {'имя_токена': Point}
    """

    data = [
            [token for token in lst
             if token != 'Python']
            for lst in data
        ]
    data = [lst for lst in data if lst]

    id2word = corpora.Dictionary(data)

    corpus = [
        [(id2word.token2id[token], 1) for token in lst]
        for lst in data
        ]

    tfidf = models.TfidfModel(dictionary=id2word)
    dfs = tfidf.dfs
    lsi = models.LsiModel(corpus=corpus, id2word=id2word, num_topics=2)

    result = {
        id2word[i]: Point(x=xy[0], y=xy[1],
                          power=dfs[i])
        for i, xy in enumerate(lsi.projection.u)
        # Для визуализации отбираю только те навыки,
        # которые отмечены ключевыми хотя бы для 5 % вакансий
        if dfs[i]/len(corpus) > 0.05
        }
    return result


def normalize_split(sentence):
    """ Разбивает фразу на массив слов
        и приводит их к основной форме
    """
    sentence = re.sub(r'[^A-zА-Яа-яЁё]', ' ', sentence)
    print(sentence)
    res = [morph.parse(word)[0].normal_form for word in sentence.split()]
    res = [word for word in res if word]
    return res



def w2v_titles_weighed(titled_corpus, tags):
    """ Из корпуса текстов создаёт Word2Vec-модель,
        взвешенную на основе присутствия в текстах
        заданных ключевых слов через веса заголовков
    
    :param titled_corpus: список кортежей [('заголовок', [список_фраз])]
    :param tags: итератор ключевых слов
    :return: Word2Vec-модель библиотеки gensim
    """

    titles = [normalize_split(item[0]) for item in titled_corpus]
    print(titles)
    title_model = models.Word2Vec(titles, size=100, window=5, min_count=2)

    return title_model

