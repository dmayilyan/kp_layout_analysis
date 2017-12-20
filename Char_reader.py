#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import sys
import codecs
from collections import OrderedDict

import plotly.offline as pl
import plotly.graph_objs as gl_obs

import matplotlib.pyplot as plt
# import numpy as np

pair_dict = {}
s_pair = ()


# Making Markov chain
def process_block(symbol, num_symbs=2):
    ''' Go through the letters and make keys with list values '''
    global s_pair
    if len(s_pair) < num_symbs:
        s_pair += (symbol,)
        return

    try:
        pair_dict[s_pair].append(symbol)
    except KeyError:
        pair_dict[s_pair] = [symbol]

    s_pair = shift(s_pair, symbol)


def shift(t, symbol):
    ''' Shifting to next  '''
    return t[1:] + (symbol,)

# def window(text):
#     # yield lambda x: (range(x, 2))
#     # for x in text:
#     #     yield x

# def make_chain(text):
#     qwe = window(text)
#     print(type(window(text)))
#     for symbol in qwe:
#         # for i in qwe:
#         print(symbol)


def get_alphabet():
    ''' Making an ordered dictionary of the alphabet '''
    d = OrderedDict()
    for j in range(1377, 1413):
        if j == ord("ւ"):
            d["ու"] = 0
            continue
        # case of ev
        d[chr(j)] = 0
        if j == 1412:
            d["և"] = 0

    return d


def fill_dict(d, text):
    prev_c = ""
    for c in text:
        # if c in punct_marks: continue
        if (ord(c) >= 1369) & (ord(c) <= 1375) | \
           (ord(c) >= 1417) & (ord(c) <= 1418):
            # print("Found punctuation mark", c, "...")
            continue

        # Cheking for alien chars
        if (((ord(c) <= 1328) | (ord(c) >= 1423)) & (ord(c) != 32)):
            # print("Found alien character", c, "...")
            continue

        if (ord(c) >= 1329) & (ord(c) <= 1366):
            c = chr(ord(c) + 48)

        if (ord(c) != 32):
            if (c == "ւ"):
                if (prev_c == "ո"):
                    d["ո"] -= 1
                    if "ու" in d:
                        d["ու"] += 1
                    else:
                        d["ու"] = 1

                if (prev_c == "ե"):
                    d["ե"] -= 1
                    if "և" in d:
                        d["և"] += 1
                    else:
                        d["և"] = 1
            else:
                if (c in d):
                    d[c] += 1
                else:
                    d[c] = 1
        prev_c = c

    return d


def main():
    filename = "Ֆրանց Կաֆկա_Կերպարանափոխություն"

    f = codecs.open(filename, "r", "utf-8")
    text = f.read()
    # print(type(text))
    print("Analyzing file", filename, "...")

    # make_chain(text)
    for symbol in text:
        process_block(symbol)

    pair_dict_new = dict((str(key[0] + key[1]), value)
                         for (key, value) in pair_dict.items())
    # print(pair_dict_new)

    d = get_alphabet()
    print(d)

    d = fill_dict(d, text)
    print(d)

    # print(d)
    e = {}
    num_chars = 4
    for i in range(len(text)):
        if chr(32) in set(text[i: i + num_chars]):
            continue
        if text[i: i + num_chars] in e:
            e[text[i: i + num_chars]] += 1
        else:
            e[text[i: i + num_chars]] = 1

    # x_data = []
    # y_data = []

    # for i in range(0,10):
    #     x_data.append(i)
    #     y_data.append(i**i)
    #     print(y_data)

    # data = [gl_obs.Bar(x_data,y_data)]
    # pl.plot(data)

    # print(d.items())
    # print(type(d))
    #
    #

    layout = gl_obs.Layout(title=filename)

    data_filtered = {}
    data_filtered = e.copy()
    data_filtered = {k: v for k, v in data_filtered.items() if v > 20}

    data = [gl_obs.Bar(x=list(d.keys()),
                       y=list(d.values())
                       )]
    # print(d.values())

    fig = gl_obs.Figure(data=data, layout=layout)

    # pl.plot(fig, filename='basic-bar.html')

    data1 = [gl_obs.Bar(x=list(data_filtered.keys()),
                        y=list(data_filtered.values())
                        )]

    # pl.plot(data1, filename='basic-pie.html')
    # y = list(pair_dict_new['ռո'])
    # plt.hist(x, y, histtype='bar', rwidth='0.8')
    # plt.show()
    # print(pair_dict_new.values())
    # Need to switvh to normal histogram creation NW
    data2 = [gl_obs.Bar(x=list(pair_dict_new.keys()),
                        y=list(pair_dict_new.values())
                        )]

    pl.plot(data2, filename='basic-pie.html')

    # data_qwe = {'a': 4, 'b': 23, 'c': 12}

    # X = np.arange(len(data_qwe))
    # pl.bar(X, data_qwe.values(), align='center', width=0.5)
    # pl.xticks(X, data_qwe.keys())
    # ymax = max(data_qwe.values()) + 1
    # pl.ylim(0,ymax)
    # pl.show()


if __name__ == '__main__':
    main()
