#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pandas as pd
import numpy as np
import pprint
import matplotlib.pyplot as plt

import symbols

# from line_profiler import LineProfiler


class chain(object):
    '''
    Read data files and fills them to a DataFrame.
    '''
    def __init__(self):
        self.MarkDict = {}
        self.s_pair = ()
        self.MarkFrame = pd.DataFrame()
        self.df = pd.DataFrame()

    def __str__(self):
        return '(%s, %s) : time' % (self.s_pair[0], self.s_pair[1])

    def get_datafiles(self):
        ''' Gets files form the hardcoded folder. '''
        f_list = os.listdir('./data_files')
        if f_list:
            for file in f_list:
                if not file.startswith('text'):
                    yield file
        else:
            raise Exception('Data folder is empty')

    def process_files(self):
        '''
        Gets the list of files in the fixed data folder
        and reads columns to a DataFrame.
        '''
        # Checking directory existance
        self.is_dir()
        time_files = self.get_datafiles()
        for tf in time_files:
            print()
            self.read_columns(tf)
            self.initial_edit()

            print('Started analysing file: %s' % tf)
            # for i_symbol in range(self.df.symb.size - 1):

                # if df.sym_time[i_symbol] == 0.0:
                #     continue
                # str_symb = df.symb[i_symbol]
                # if (ord(str_symb) == 127):
                #     print("Found Backspace", str_symb)
                #     continue

                # if i_symbol > 4000:
                #     continue

                # print(self.df.symb[i_symbol], self.df.sym_time[i_symbol])

                # self.process_block(self.df.symb[i_symbol],
                #                    self.df.sym_time[i_symbol],
                #                    2)  # Number of symbols

    def is_dir(self):
        ''' Checking data directory existance. '''
        if os.path.isdir('./data_files/') is False:
            print('Data folder doesn\'t exists\nExiting')
            raise Exception('Folder doesn\'t exist')

    def read_columns(self, tf):
        ''' Read time data files by columns. '''
        tf = './data_files/' + tf
        self.df = pd.read_table(tf, sep="\t", header=None,
                                names=["symb", "usymb", "sym_time"])

    def initial_edit(self):
        ''' Function deals with carriage returns, spaces etc. '''
        # print(df[2413:2420])
        for u_symbol in range(self.df.usymb.size - 1):
            if self.df.usymb[u_symbol] == 13:
                # self.df.symb[u_symbol] = chr(9166)
                self.df.loc[u_symbol, 'symb'] = chr(9166)
        #         print('Here is it!', u_symbol)

        # self.df = self.df[self.df.symb.notnull()]
        # self.df = self.df.reset_index(drop=True)
        # self.df.reindex(method='ffill', fill_value=chr(9166))

        # print(df[2413:2420])

    # Making Markov chain
    def process_block(self, symbol, s_time, num_symbs=2):
        '''
        Go through the letters and make (k,k ... k):[t] structure dictionary,
        where:

        k: num_symbs [default: 2] times symbol sequence
        t: time to the next symbol after the imput of the symbol sequence
        '''
        # dealing with spaces
        if symbol == ' ':
            symbol = chr(9251)

        if len(self.s_pair) < num_symbs:
            self.s_pair += (symbol,)
            return

        try:
            self.MarkDict[self.s_pair].append((symbol, s_time))
        except KeyError:
            self.MarkDict[self.s_pair] = [(symbol, s_time)]

        temp_list = []
        s_pair_str = str_compile(self.s_pair)

        temp_list.append(s_pair_str)
        temp_list.append(symbol)
        temp_list.append(s_time)
        # print(s_pair_str)
        self.MarkFrame.append(temp_list)
        self.s_pair = self.s_pair[1:] + (symbol,)


def str_compile(s_pair):
    ''' String from a tuple. '''
    return ''.join(i for i in s_pair)


def make_plots(MarkDict):
    ''' Doing some analysis '''

    left_hand = {'ք', 'ո', 'ե', 'ռ', 'տ', 'ա', 'ս', 'դ', 'ֆ', 'գ',
                 'զ', 'ղ', 'ց', 'վ', 'բ', 'է', 'թ', 'փ', 'ձ', 'ջ',
                 'Ք', 'Ո', 'Ե', 'Ռ', 'Տ', 'Ա', 'Ս', 'Դ', 'Ֆ', 'Գ',
                 'Զ', 'Ղ', 'Ց', 'Վ', 'Բ', 'Է', 'Թ', 'Փ', 'Ձ', 'Ջ'}
    left_hand_signs = {'՝'}
    right_hand = {'ը', 'ւ', 'ի', 'օ', 'պ', 'խ', 'ծ', 'շ', 'հ', 'յ',
                  'կ', 'լ', 'ն', 'մ', 'և', 'ր', 'չ', 'ճ', 'ժ',
                  'Ը', 'Ւ', 'Ի', 'Օ', 'Պ', 'Խ', 'Ծ', 'Շ', 'Հ', 'Յ',
                  'Կ', 'Լ', 'Ն', 'Մ', 'Ր', 'Չ', 'Ճ', 'Ժ'}  # և is excluded
    right_hand_signs = {',', '․', '՛', '֊'}

    for k, v in MarkDict.items():
        # print(v)

        # Making hand lists for graphing
        data = []
        data_ll = []
        data_rr = []
        last_letter = k[len(k) - 1]
        [data.append(x) for _, x in v if x < 3000]
        # looping through inner list
        for symbol, x in v:
            # if x < 3000:
            #     continue

            if last_letter in (left_hand | left_hand_signs):
                if symbol in (left_hand | left_hand_signs):
                    data_ll.append(x)

            if last_letter in (right_hand | right_hand_signs):
                if symbol in (right_hand | right_hand_signs):
                    data_rr.append(x)

        # Making the histogram title
        grtitle = str_compile(k)

        if len(data) < 60:
            continue

        # bins = numpy.linspace(0, 2000, 400)
        # plt.hist(data, bins='sturges')
        plt.hist(data, bins=100, range=(0, 3000), alpha=0.3, label='all')
        if data_ll:
            plt.hist(data_ll, bins=100, range=(0, 3000),
                     alpha=0.3, label='Left-Left hand')
        if data_rr:
            plt.hist(data_rr, bins=100, range=(0, 3000),
                     alpha=0.3, label='Right-Right hand')
        plt.title('Letter pair: ' + grtitle)
        plt.legend(loc='upper right')

        # plt.show()
        # print(grtitle)
        # print(data)


def main():
    chain_item = chain()
    chain_item.process_files()
    print(chain_item)
    make_plots(chain_item.MarkDict)

    layout = symbols.layout_match()
    layout.read_file('hy_EasternAlt')
    layout.get_symbol_name_dict()
    key_dist = layout.create_key_distance()

    symbols.make_plot(key_dist, TODO)


if __name__ == '__main__':
    main()
