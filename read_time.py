#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pandas as pd
import numpy as np
import pprint
import matplotlib.pyplot as plt
from scipy import optimize
from astropy import modeling

import symbols

# from line_profiler import LineProfiler

from wiki_parser import read_db


class Chain(object):
    '''
    Read data files and fills them to a DataFrame.
    '''
    def __init__(self):
        self.MarkDict = {}
        self.s_pair = ()
        self.delta_dict = {}
        # self.MarkFrame = pd.DataFrame()
        self.df = pd.DataFrame()

        self.data_folder = ''

    def __str__(self):
        return '(%s, %s) : time' % (self.s_pair[0], self.s_pair[1])

    def get_datafiles(self):
        ''' Gets files form the hardcoded folder. '''
        f_list = os.listdir(self.data_folder)
        if f_list:
            for file in f_list:
                if not file.startswith('text'):
                    # Extra debug check
                    # if not file.startswith('data_'):
                    yield file
        else:
            raise Exception('Data folder \"%s\" is empty' % self.data_folder)

    def process_files(self):
        '''
        Gets the list of files in the fixed data folder
        and reads columns to a DataFrame.
        '''
        self.data_folder = './time_files/'
        # Checking directory existance
        self.is_dir()
        time_files = self.get_datafiles()
        # time_files = ['time']  # !!!!!!!!!!!!!!!!!!!!!!DEBUG
        for tf in time_files:
            # print(tf)
            self.read_columns(tf)
            self.initial_edit()

            print('Analysing file: %s' % tf)
            for i_symbol in range(self.df.symb.size - 1):

                # if df.sym_time[i_symbol] == 0.0:
                #     continue
                # str_symb = df.symb[i_symbol]
                # if (ord(str_symb) == 127):
                #     print("Found Backspace", str_symb)
                #     continue

                # if i_symbol > 400:
                #     continue

                # print(self.df.symb[i_symbol], self.df.sym_time[i_symbol])

                self.process_block(self.df.symb[i_symbol],
                                   self.df.sym_time[i_symbol],
                                   1)  # Number of symbols

    def get_pairs(self):
        '''
        '''
        self.data_folder = './time_files/'
        # Checking directory existance
        self.is_dir()
        time_files = self.get_datafiles()
        for tf in time_files:
            print(tf)
            # if i_symbol > 4:
            #     continue



    def is_dir(self):
        ''' Checking data directory existance. '''
        if os.path.isdir(self.data_folder) is False:
            print('Data folder  doesn\'t exists\nExiting')
            raise Exception('Folder \"%s\" doesn\'t exist' % self.data_folder)

    def read_columns(self, tf):
        ''' Read time data files by columns. '''
        tf = self.data_folder + tf
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
        t: time to the next symbol after the input of the symbol sequence
        '''
        # dealing with spaces
        if symbol == ' ':
            symbol = chr(9251)

        # Making markov
        if len(self.s_pair) < num_symbs:
            self.s_pair += (symbol,)
            return

        try:
            self.MarkDict[self.s_pair].append((symbol, s_time))
        except KeyError:
            self.MarkDict[self.s_pair] = [(symbol, s_time)]


        # Making pair dict
        s_pair_str = str_compile(self.s_pair)
        s_pair_str = str_compile((s_pair_str, symbol))
        # print(s_pair_str)

        try:
            self.delta_dict[s_pair_str].append((s_time))
        except KeyError:
            self.delta_dict[s_pair_str] = [s_time]


        # temp_list = []
        # temp_list.append(s_pair_str)
        # temp_list.append(symbol)
        # temp_list.append(s_time)
        # self.MarkFrame.append(temp_list)
        # print(self.MarkFrame)
        self.s_pair = self.s_pair[1:] + (symbol,)


# #########################################
def str_compile(s_pair):
    ''' String from a tuple. '''
    return ''.join(i for i in s_pair)

# #########################################


key_dict_ratio = {}


def get_weighted_dict(pair):
    cur = read_db()
    key_dict = dict(cur.fetchall())
    count_all = sum(key_dict.values())
    key_dict_ratio = dict(((item[0], (item[1] / count_all))
                          for item in key_dict.items()))
    print('Weight in all is ', key_dict_ratio[pair] * 100)

    # cols = [column[0] for column in cur.description]
    # weight_df = pd.DataFrame.from_records(data=cur.fetchall(), columns=cols)

    # total_count = weight_df['use_count'].sum()
    # print(total_count)

    # weight_df['use_count'] = weight_df['use_count'].div(total_count)
    # # weight_df.set_index('key_pair')
    # print(weight_df.loc[:, lambda df: df.key_pair == 'ու', :])
    # print(weight_df)


def gaussian(x, amplitude, mean, stddev):
    return amplitude * np.exp(-((x - mean) / 4 / stddev)**2)


def plot_pair(d, pair):
    '''
    Makes plot from a dict values
    '''

    hist, bin_edges = np.histogram(d[pair], bins=200, range=(0, 1000))
    # plt.bar(bin_edges[:-1], hist, width=2)

    nonz_hist = np.where(hist != 0, hist, np.nan)
    # mean_val = np.mean(nonz_hist)
    mean_val = np.nanmean(d[pair], 0)
    variance = np.var(d[pair])
    sigma = np.sqrt(variance)
    print(mean_val, sigma)

    fitter = modeling.fitting.LevMarLSQFitter()
    model = modeling.models.Gaussian1D(15, mean_val, sigma)
    fitted_model = fitter(model, bin_edges[:-1], hist)

    plt.plot(bin_edges[:-1], hist)
    plt.plot(bin_edges[:-1], fitted_model(bin_edges[:-1]))


    plt.title('Letter pair: %s, Mean is: %f' % (pair, mean_val))
    plt.xlim(min(bin_edges), max(bin_edges))
    plt.show()



def make_plots(MarkDict, key_dist):
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

    # pprint.pprint(MarkDict)
    for k, v in MarkDict.items():
        # print(k,v)

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


        if len(data) < 60:
            continue

        # Making the histogram title
        grtitle = str_compile(k)


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


        # symbols.make_plot(key_dist, )


        # if grtitle in key_dict_ratio.keys():
        #     print('Weight in all combinations ', key_dict_ratio[grtitle])

        print(grtitle)
        plt.show()
        # print(data)


def main():
    chain_item = Chain()
    # chain_item.get_pairs()
    chain_item.process_files()
    # pprint.pprint(chain_item.MarkDict)
    # print(chain_item.delta_dict)
    for key in chain_item.delta_dict.keys():
        if len(chain_item.delta_dict[key]) < 50:
            continue
        try:
            get_weighted_dict(key)
        except Exception:
            pass
        plot_pair(chain_item.delta_dict, key)
    # # print(chain_item)


    # # return 0

    # layout = symbols.layout_match()
    # layout.read_file('hy_EasternAlt')
    # layout.get_symbol_name_dict()
    # key_dist = layout.create_key_distance()
    
    # make_plots(chain_item.MarkDict, key_dist)




if __name__ == '__main__':
    main()
