#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pandas as pd
import pprint
import matplotlib.pyplot as plt

# from line_profiler import LineProfiler

MarkDict = {}
s_pair = ()

df = pd.DataFrame()


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

    # df = df[df.symb.notnull()]
    # df = df.reset_index(drop=True)
    # df.reindex(method='ffill', fill_value=chr(9166))

    # print(df[2413:2420])


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

        # Making the histogram title
        grtitle = ''
        for i in k:
            grtitle += i

        if len(data) < 100:
            continue

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

        process_block(df.symb[i_symbol], df.sym_time[i_symbol], 2)


    left_hand = {'ք', 'ո', 'ե', 'ռ', 'տ', 'ա', 'ս', 'դ', 'ֆ', 'գ',
                 'զ', 'ղ', 'ց', 'վ', 'բ', 'է', 'թ', 'փ', 'ձ', 'ջ',
                 'Ք', 'Ո', 'Ե', 'Ռ', 'Տ', 'Ա', 'Ս', 'Դ', 'Ֆ', 'Գ',
                 'Զ', 'Ղ', 'Ց', 'Վ', 'Բ', 'Է', 'Թ', 'Փ', 'Ձ', 'Ջ'}
    left_hand_signs = {'՝'}
    right_hand = {'ը', 'ւ', 'ի', 'օ', 'պ', 'խ', 'ծ', 'շ', 'հ', 'յ',
                  'կ', 'լ', 'ն', 'մ', 'և', 'ր', 'չ', 'ճ', 'ժ',
                  'Ը', 'Ւ', 'Ի', 'Օ', 'Պ', 'Խ', 'Ծ', 'Շ', 'Հ', 'Յ',
                  'Կ', 'Լ', 'Ն', 'Մ',      'Ր', 'Չ', 'Ճ', 'Ժ'}  # և is excluded
    right_hand_signs = {',', '․', '՛', '֊'}

    # pprint.pprint(MarkDict, width=50)
    # print(MarkDict)
    # print(df.symb)


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
