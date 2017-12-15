#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict
import numpy as np

import matplotlib
import matplotlib.pyplot as plt

# import plotly.offline as pl
import plotly.graph_objs as gl_obs


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
            dictlist[list_letter][chr(uc(list_letter)) + chr(uc(letter2 % 38))] = [0.0, 0]

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
            dictlist[list_letter][chr(uc(list_letter - 1)) + chr(uc(letter2 % 38))] = [0.0, 0]

            if uc(letter2 % 38) == 1412:
                dictlist[list_letter][chr(uc(list_letter - 1)) + "և"] = [0.0, 0]
    # print(type(real_index), end="!!!!!!!!!!!!!!!!!!!!")

    return real_index, dictlist


def plot_all(real_index, dictlist):
    matplotlib.rc('font', **{'sans-serif': 'DejaVu Sans',
                             'family': 'sans-serif'})

    for index, dict_item in enumerate(dictlist):
        if index >= 4:
            continue
        plt.subplot(2, 2, index + 1)
        plt.bar(range(len(dict_item)), [y[0] for x, y in dict_item.items()], align='center')
        plt.xticks(range(len(dict_item)), [k for k in dict_item.keys()])

    plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
    plt.show()


def decodef(x):
    return x.decode("utf-8") if x.decode("utf-8") != "" else "_"

# def window_gen(text):
#     yield ([x,x+1] for x in text)

def main():
    real_index, dictlist = make_dicts()

    arr = np.genfromtxt("./time_files/time", delimiter="\t",
                        dtype="U1, i4, f8", converters={0: decodef})
    print(arr)

    # return 0

    # d = OrderedDict()
    d = {}

    # for g in range(len(right_hand)):
    #     print("\"" + chr(ord(right_hand[g])-48) + "\", ", end="")

    left_hand = {"ք", "ո", "ե", "ռ", "տ", "ա", "ս", "դ", "ֆ", "գ", "զ", "ղ", "ց", "վ", "բ", "է", "թ", "փ", "ձ", "ջ",
                 "Ք", "Ո", "Ե", "Ռ", "Տ", "Ա", "Ս", "Դ", "Ֆ", "Գ", "Զ", "Ղ", "Ց", "Վ", "Բ", "Է", "Թ", "Փ", "Ձ", "Ջ"}
    left_hand_signs = {"՝"}
    right_hand = {"ը", "ւ", "ի", "օ", "պ", "խ", "ծ", "շ", "հ", "յ", "կ", "լ", "ն", "մ", "և", "ր", "չ", "ճ", "ժ",
                  "Ը", "Ւ", "Ի", "Օ", "Պ", "Խ", "Ծ", "Շ", "Հ", "Յ", "Կ", "Լ", "Ն", "Մ",      "Ր", "Չ", "Ճ", "Ժ"}  # և is excluded
    right_hand_signs = {",", "․", "՛", "֊"}

    # print(arr)
    text = "".join(str(x) for [x, y, z] in list(arr))
    # mg = window_gen(text)
    # for i in mg:
    #     print(mg.__next__())

    return 0
    # return 0
    time = [z for [x, y, z] in list(arr)]
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

        if text[i:i + 2] in d:
            # print(d.get(text[i:i+2]))
            vals = d.get(text[i:i + 2])
            d[text[i:i + 2]] = [x + y for x, y in zip(list(vals), [time[i + 1], 1])]
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

    for d_element in dictlist:
        dictlist[real_index[list(d_element.keys())[0][0]]] = OrderedDict([x, y] if y[0] == 0. else (x, [y[0] / y[1], y[1]]) for x, y in d_element.items())

    print(dictlist)
    a_list = []
    for d_element in dictlist:
        # print(d_element.items())
        a_list.append([y[0] for x,y in d_element.items()][4])

    print(a_list)
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
    main()
