#!/usr/bin/python3

import os
import sys
import math

import array

import statistics

from matplotlib import rc
rc('font', family='Droid Sans', weight='normal', size=14)

import matplotlib.pyplot as plt


class WikiGraph:

    def load_from_file(self, filename):
        print('Загружаю граф из файла: ' + filename)

        with open(filename, 'r', encoding = 'utf-8') as f:
            (n, _nlinks) = tuple(map(int, f.readline().split()))
            self._titles = []
            self._sizes = array.array('L', [0]*n)
            self._links = array.array('L', [0]*_nlinks)
            self._redirect = array.array('B', [0]*n)
            self._offset = array.array('L', [0]*(n+1))
            k = 0
            for i in range(n):
                self._titles.append(f.readline())
                self._sizes[i], self._redirect[i], e = tuple(map(int, f.readline().split()))
                for j in range(e):
                    self._links[k] = int(f.readline())
                    k+=1
                self._offset[i+1]= self._offset[i]+e
        print('Граф загружен')

    def get_number_of_links_from(self, _id):
        return self._offset[_id+1] -self._offset[_id]

    def get_links_from(self, _id):
        return self._links[self._offset[_id]: self._offset[_id+1]]

    def get_id(self, title):
        return self._titles.index(title)

    def get_number_of_pages(self):
        return len(self._titles)

    def is_redirect(self, _id):
        return self._redirect[_id] == 1

    def get_title(self, _id):
        return self._titles[_id]

    def get_page_size(self, _id):
        return self._sizes[_id]

    def bfs(self, start):
        sid = self.get_id(start)
        D = [None] * (self.get_number_of_pages())
        D[sid] = 0
        Q = [sid]
        Qstart = 0
        while Qstart < len(Q):
            u = Q[Qstart]
            Qstart += 1
            for v in self.get_links_from(u):
                if D[v] is None:
                    D[v] = D[u] + 1
                    Q.append(v)
        return D

    def path(self, D, a, current, lis):
        lis.append(current)
        if current == a:
            return [self.get_title(lis[i]) for i in range(len(lis) - 1, -1, -1)]
        min = float('+inf')
        b = current
        for neighbour in self.get_links_from(b):
            if D[neighbour] != None and D[neighbour] < min:
                min = D[neighbour]
                current = neighbour
        return path(D, a, current, lis)

def hist(fname, data, bins, xlabel, ylabel, title, facecolor='green', alpha=0.5, transparent=True, **kwargs):
    plt.clf()
    # TODO: нарисовать гистограмму и сохранить в файл


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Использование: wiki_stats.py <файл с графом статей>')
        sys.exit(-1)

    if os.path.isfile(sys.argv[1]):
        wg = WikiGraph()
        wg.load_from_file(sys.argv[1])
    else:
        print('Файл с графом не найден')
        sys.exit(-1)

    n = wg.get_number_of_pages()
    titles = [wg.get_title(i) for i in range(n)]
    redirect = array.array('B', [1 if wg.is_redirect(i) else 0 for i in range(n)])
    nlinksfrom = array.array('L', [wg.get_number_of_links_from(i) for i in range(n)])
    b = array.array('L', [0 for i in range(n)])
    for i in range(n):
        if wg.is_redirect(i):
            continue
        a = wg.get_links_from(i)
        for page in (a):
            b[page]+=1
    c = array.array('L', [0 for i in range(n)])
    for i in range(n):
        if not wg.is_redirect(i):
            continue
        a = wg.get_links_from(i)
        for page in (a):
            c[page]+=1
    # D = wg.bfs('Python')
    # path = wg.path(D, wg.get_id('Python'), wg.get_id('Список_файловых_систем'), list())
    # print(path)
    print('Количество статей с перенаправлением: ', sum(redirect))
    print('минимальное количество ссылок из статьи: ', min(nlinksfrom))
    print('количество статей с минимальным количеством ссылок: ', len([1 for i in range(n) if wg.get_number_of_links_from(i) == min(nlinksfrom)]))
    print('максимальное количество ссылок из статьи: ', max(nlinksfrom))
    print('количество статей с максимальным количеством ссылок:', len([1 for i in range(n) if wg.get_number_of_links_from(i) == max(nlinksfrom)]))
    print('статья с наибольшим количеством ссылок:', wg.get_title(nlinksfrom.index(max(nlinksfrom))))
    print('среднее количество ссылок в статье:', (sum(nlinksfrom))/(n-sum(redirect)))
    print('Минимальное количество ссылок на статью:', min(b))
    print('Количество статей с минимальным количеством внешних ссылок:', len([1 for i in range(n) if b[i] == min(b)]))
    print('Максимальное количество ссылок на статью', max(b))
    print('Количество статей с максимальным количеством внешних ссылок',len([1 for i in range(n) if b[i] == max(b)]))
    print('Статья с наибольшим количеством внешних ссылок:', wg.get_title(b.index(max(b))))
    print('среднее количество внешних ссылок на статью:', (sum(b))/(len(b)))
    print('Минимальное количество перенаправлений на статью:', min(c))
    print('Количество статей с минимальным количеством внешних перенаправлений:', len([1 for i in range(n) if c[i] == min(c)]))
    print('Максимальное количество перенаправлений на статью',max(c))
    print('Количество статей с максимальным количеством внешних перенаправлений:', len([1 for i in range(n) if c[i] == max(c)]))
    print('Статья с наибольшим количеством внешних перенаправлений:',wg.get_title(c.index(max(c))))
    print('Среднее количество внешних перенаправлений на статью:', (sum(c))/(len(c)))
    # TODO: статистика и гистограммы