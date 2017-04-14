
from gensim import corpora, models
from collections import namedtuple


Point = namedtuple('Point', 'x, y, power')


def calc_2d_projection(data):

    """ Размещает токены в двухмерном пространстве
        с учётом того, насколько часто они встречаются вместе

        :param data: Список списков токенов.
        :return: Словарь списков {'имя_токена': Point}

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
