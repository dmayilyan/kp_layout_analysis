#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from collections import OrderedDict
import numpy as np
import pandas as pd
import pprint
import matplotlib
import matplotlib.pyplot as plt

# import plotly.offline as pl
import plotly.graph_objs as gl_obs

# from line_profiler import LineProfiler

MarkDict = {}
s_pair = ()

df = pd.DataFrame()

def uc(l):
    return l + 1377


def abc(u):
    return u - 1377


def make_dicts():
    ''' Making dictionaries and real indices of it for future use.'''
    real_index = {}
    dictlist = [OrderedDict() for x in range(39)]
    # Till ք
    for list_letter in range(36):
        # if uc(list_letter%38) == 1412:
        #     first_char = "և"
        # else:
        real_index[chr(uc(list_letter))] = list_letter
        # print(chr(uc(list_letter)), list_letter)
        for letter2 in range(38):
            dictlist[list_letter][chr(uc(list_letter)) +
                                  chr(uc(letter2 % 38))] = [0.0, 0]

            if uc(letter2 % 38) == 1412:
                dictlist[list_letter][chr(uc(list_letter)) + "և"] = [0.0, 0]
            # if list_letter == 36:
            #     dictlist[list_letter][chr(list_letter+1377)+chr(letter2%38+1377)] = 0

    # Case of և
    real_index["և"] = 36
    # print("և", 36)
    for list_letter in range(38):
        dictlist[36]["և" + chr(uc(list_letter % 38))] = [0.0, 0]

        if uc(list_letter % 38) == 1412:
            dictlist[36]["ևև"] = [0.0, 0]

    # Case of օ,ֆ
    for list_letter in range(37, 39):
        real_index[chr(uc(list_letter - 1))] = list_letter
        # print(chr(uc(list_letter-1)), list_letter)

        for letter2 in range(38):
            dictlist[list_letter][chr(uc(list_letter - 1)) +
                                  chr(uc(letter2 % 38))] = [0.0, 0]

            if uc(letter2 % 38) == 1412:
                dictlist[list_letter][chr(uc(list_letter - 1)) +
                                      "և"] = [0.0, 0]
    # print(type(real_index), end="!!!!!!!!!!!!!!!!!!!!")

    return real_index, dictlist


def plot_all(real_index, dictlist):
    matplotlib.rc('font', **{'sans-serif': 'DejaVu Sans',
                             'family': 'sans-serif'})

    for index, dict_item in enumerate(dictlist):
        if index >= 4:
            continue
        plt.subplot(2, 2, index + 1)
        plt.bar(range(len(dict_item)), [y[0] for x, y in dict_item.items()],
                align='center')
        plt.xticks(range(len(dict_item)), [k for k in dict_item.keys()])

    plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
    plt.show()


def decodef(x):
    return x.decode("utf-8") if x.decode("utf-8") != "" else "_"

# def window_gen(text):
#     yield ([x,x+1] for x in text)


def get_list(arr):
    return "".join(str(x) for [x, _, _] in list(arr))


# Initial edit of the data, detecting problematic characters
def initial_edit():
    ''' Function deals with carriage returns, spaces etc. '''
    global df
    # print(df[2413:2420])
    for u_symbol in range(df.usymb.size - 1):
        if df.usymb[u_symbol] == 13:
            # df.symb[u_symbol] = chr(9166)
            df.loc[u_symbol, 'symb'] = chr(9166)
    #         print('Here is it!', u_symbol)

    # df = df[]
    # df = df[df.symb.null() and df.usymb == 13]
    # df = df[df.symb.notnull()]
    # df = df.reset_index(drop=True)
    # df.reindex(method='ffill', fill_value=chr(9166))
    # indexy = df.index
    # print(indexy, 'HERE')
    # df.symb.reindex(indexy, fill_value=chr(9166))

    print(df[2413:2420])
    # print(df)


# Making Markov chain
def process_block(symbol, s_time, num_symbs=2):
    ''' Go through the letters and make keys with list values '''
    global s_pair
    # dealing with spaces
    if symbol == ' ':
        symbol = chr(9251)

    if len(s_pair) < num_symbs:
        s_pair += (symbol,)
        return

    try:            # df.sym_time[s_time+1]
        MarkDict[s_pair].append((symbol, s_time))
    except KeyError:
        MarkDict[s_pair] = [(symbol, s_time)]

    s_pair = shift(s_pair, symbol)


def shift(t, symbol):
    ''' Shifting to next  '''
    return t[1:] + (symbol,)


def get_datafile():
    ''' Gets files in hardcoded folder '''
    f_list = os.listdir('./time_files')
    for file in f_list:
        if not file.startswith('text'):
            yield file


def read_columns(tf):
    ''' Read time data files by columns '''
    global df
    tf = './time_files/' + tf
    df = pd.read_table(tf, sep="\t", header=None,
                       names=["symb", "usymb", "sym_time"])
    return df


def make_plots():
    for k, v in MarkDict.items():
        data = []
        [data.append(x) for _, x in v if x < 3000]
        # [print(x) for _, x in v]

        # Making the histogram title
        grtitle = ''
        for i in k:
            grtitle += i

        if len(data) < 40:
            continue

        # if k[0] == ' ':
        #     k = (chr(9251), k[1])

        # if k[1] == ' ':
        #     k = (k[0], chr(9251))

        # plt.hist(data, bins='sturges')
        plt.hist(data, bins=100)
        plt.title('Letter pair: ' + grtitle)
        plt.show()
        print(grtitle)
        print(data)


def main1():
    for i_symbol in range(df.symb.size - 2):

        # if df.sym_time[i_symbol] == 0.0:
        #     continue
        # str_symb = df.symb[i_symbol]
        # print(i_symbol, ord(str_symb))
        # if (ord(str_symb) == 127):
        #     print("Found Backspace", str_symb)
        #     continue

        # if i_symbol > 4000:
        #     continue
        # print(df.symb[i_symbol], df.sym_time[i_symbol])

        process_block(df.symb[i_symbol], df.sym_time[i_symbol], 3)


    # pprint.pprint(MarkDict, width=50)
    # print(MarkDict)
    # print(df.symb)


def main():
    real_index, dictlist = make_dicts()

    arr = np.genfromtxt("./time_files/time", delimiter="\t",
                        dtype="U1, i4, f8", converters={0: decodef})
    print(arr)

    # return 0

    # d = OrderedDict()
    d = {}

    # Profiler
    # lprofiler = LineProfiler()
    # lpw = lprofiler()
    # lpw =()
    # lprofiler.print_stats()

    # for g in range(len(right_hand)):
    #     print("\"" + chr(ord(right_hand[g])-48) + "\", ", end="")

    left_hand = {"ք", "ո", "ե", "ռ", "տ", "ա", "ս", "դ", "ֆ", "գ", "զ", "ղ", "ց", "վ", "բ", "է", "թ", "փ", "ձ", "ջ",
                 "Ք", "Ո", "Ե", "Ռ", "Տ", "Ա", "Ս", "Դ", "Ֆ", "Գ", "Զ", "Ղ", "Ց", "Վ", "Բ", "Է", "Թ", "Փ", "Ձ", "Ջ"}
    left_hand_signs = {"՝"}
    right_hand = {"ը", "ւ", "ի", "օ", "պ", "խ", "ծ", "շ", "հ", "յ", "կ", "լ", "ն", "մ", "և", "ր", "չ", "ճ", "ժ",
                  "Ը", "Ւ", "Ի", "Օ", "Պ", "Խ", "Ծ", "Շ", "Հ", "Յ", "Կ", "Լ", "Ն", "Մ",      "Ր", "Չ", "Ճ", "Ժ"}  # և is excluded
    right_hand_signs = {",", "․", "՛", "֊"}

    # print(arr)
    text = "".join(str(x) for [x, _, _] in list(arr))
    # mg = window_gen(text)
    # for i in mg:
    #     print(mg.__next__())

    # return 0
    time = [z for [_, _, z] in list(arr)]
    for i in range(len(text) - 1):
        # if text[i:i+2] == "ղջ":
        #     print(time[i+1])
        if time[i + 1] > 1000:
            continue

        if time[i + 1] == 0.0:
            continue

        if (ord(text[i + 1]) == 127) or (ord(text[i]) == 127):
            # print("Found Backspace")
            continue

        # process_block(i,)

        if text[i:i + 2] in d:
            # print(d.get(text[i:i+2]))
            vals = d.get(text[i:i + 2])
            d[text[i:i + 2]] = [x + y for x, y in zip(list(vals),
                                                      [time[i + 1], 1])]

        else:
            d[text[i:i + 2]] = [time[i + 1], 1]

        if (ord(text[i]) >= 1377) and (ord(text[i]) <= 1414) and \
                (ord(text[i + 1]) >= 1377) and (ord(text[i + 1]) <= 1414) and \
                ((text[i] != "_") or (text[i + 1] != "_")):
            # dict_letter = abc(ord(text[i]))
            # print(dict_letter, end="!!!!!!!!!!!!!!!!!!!!!!!")
            # print(dictlist[0]["աա"])

            dict_item = dictlist[real_index[text[i]]]
            # print(dict_item)
            dict_vals = dict_item[text[i:i + 2]]
            # print(dict_vals)

            # print(text[i:i + 2], dictlist[real_index[text[i]]][text[i:i + 2]])

            dictlist[real_index[text[i]]][text[i:i + 2]] = [x + y for x, y in zip(dict_vals, [time[i + 1], 1])]
            # print(dictlist[0])


    print(dictlist)
    for d_element in dictlist:
        dictlist[real_index[list(d_element.keys())[0][0]]] = OrderedDict([x, y] if y[0] == 0. else (x, [y[0] / y[1], y[1]]) for x, y in d_element.items())

    # print(dictlist)
    a_list = []
    for d_element in dictlist:
        # print(d_element.items())
        a_list.append([y[0] for x, y in d_element.items()][4])

    # print(a_list)
    plt.scatter([range(39)], a_list)
    plt.show()

    # print(type(dictlist), end="!!!!")

# todo
    for key, value in d.items():
        # print("%s\t%f\t%i\n" %(key, d[key][0], d[key][1]))
        d[key][0] /= d[key][1]
        # print(key, d[key][0])
        # dictlist[real_index[text[i]]][]    dict((x,(y[0],y[1]/y[0])) for x,y in d.items())

    # asd = dictlist[real_index["ա"]]
    # print(type(asd), asd, end="!!!!!!!!!!!!!!!!1\n")
    # lambda (x,y): asd

    # print(asd, end="!!!!!!!!!!!!!!!!1\n")

    # f = dict(filter(lambda x: real_index["ա"]))

    # data_av = d.copy()
    # data_av = {(k: v[0] = v[0] / v[1]) for k, v in data_av.items()}

    data = [gl_obs.Bar(x=list(d.keys()),
                       # if d[k][0] < 20000
                       y=[d[k][0] for k in d if d[k][0] > 1],
                       text=[d[k][1] for k in d]
                       )]

    # print(d)
    # matplotlib.rc('font', family='Arial')

    # matplotlib.rc('font', **{'sans-serif': 'DejaVu Sans',
    #                          'family': 'sans-serif'})

    # matplotlib.pyplot.bar(range(len(d)), [d[k][0] for k in d], align='center')
    # matplotlib.pyplot.xticks(range(len(d)), [k for k in d.keys()])
    # matplotlib.pyplot.show()

    plot_all(real_index, dictlist)
    # print(dict_item.keys())

    # plt.Axes.set_ybound(lower=None, upper=200)
    # plt.axis([, , 0, max(data.x)])

    # pl.plot(data, filename='basic-bar.html')

    # counters for key switches
    left_right_counter = 0
    left_left_counter = 0
    right_left_counter = 0
    right_right_counter = 0

    # Time summation for key switches
    left_right_time = 0.
    left_left_time = 0.
    right_left_time = 0.
    right_right_time = 0.

    for i in range(len(text) - 1):
        if (text[i] == "_") or (text[i + 1] == "_"):
            continue
        is_left_hand_i = bool(text[i] in
                              left_hand | left_hand_signs)
        # if ((text[i] in left_hand) or (text[i] in left_hand_signs)):
        #     is_left_hand_i = True
        # else:
        #     is_left_hand_i = False
        is_left_hand_ip1 = not bool(text[i + 1] in
                                    right_hand | right_hand_signs)
        # print(is_left_hand_ip1)
        # if (text[i + 1] in right_hand) or (text[i + 1] in right_hand_signs):
        #     is_left_hand_ip1 = False
        # else:
        #     is_left_hand_ip1 = True

        # print(is_left_hand_ip1, end="\n-------------------------\n")

        if is_left_hand_i:
            if is_left_hand_ip1:
                left_left_counter += 1
                left_left_time += time[i + 1]
            else:
                left_right_counter += 1
                left_right_time += time[i + 1]
        else:
            if is_left_hand_ip1:
                right_left_counter += 1
                right_left_time += time[i + 1]
            else:
                right_right_counter += 1
                right_right_time += time[i + 1]

    # print(left_right_counter, left_left_counter, right_left_counter, right_right_counter)

    print("Left to Left:\t%f\nLeft to Right:\t%f\nRight to Left:\t%f\nRight to Right:\t%f"
          % (left_left_time / left_left_counter,
             left_right_time / left_right_counter,
             right_left_time / right_left_counter,
             right_right_time / right_right_counter))


if __name__ == '__main__':
    time_files = get_datafile()
    for tf in time_files:
        read_columns(tf)
        initial_edit()

        main1()
        print('Started analysing file: %s' % tf)
        print(len(MarkDict))

    # pprint.pprint(MarkDict, width=50)
    make_plots()

    # main()
