#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd

# import scipy.interpolate
import numpy as np
import matplotlib.pyplot as plt


class Layout_match(object):
    '''
    Matching symbols to key names
    '''
    def __init__(self):
        self.filename = ''
        self.df = pd.DataFrame()

    def read_file(self, filename):
        self.df = pd.read_table('./xkb_layouts/' + filename,
                                header=None)

    def get_symbol_name_dict(self):
        '''
        Returns a dictionary of symbol: key_abbr structure
        '''

        self.df.columns = ['k_name', 'reg', 'cap']
        print(self.df)

        # Adding lower case
        mydict = dict(zip(self.df.reg, self.df.k_name))
        #  Adding capitals
        mydict.update(dict(zip(self.df.cap, self.df.k_name)))
        print(mydict)
        # return mydict

    def create_key_distance(self):
        '''
        Creating some info on key positions, counting from left top edge
        This should be modified for each keyboard type !!!
        '''
        self.df.columns = ['k_name', 'dist', 'row']
        # Loops are ugly as keyboard different models are uglier
        for index in self.df.index:
            if index < 13:
                self.df.ix[index].loc['dist'] = index
                # Maybe it is better to switch to MultiIndex Meeeh...
                self.df.ix[index].loc['row'] = 0
            elif index < 26:
                self.df.ix[index].loc['dist'] = index % 13
                self.df.ix[index].loc['row'] = 1
            elif index < 37:
                self.df.ix[index].loc['dist'] = index % 13
                self.df.ix[index].loc['row'] = 2
            else:
                self.df.ix[index].loc['dist'] = index % 37
                self.df.ix[index].loc['row'] = 3

        # self.df = self.df['0', '1']
        # self.df.rename(columns={'reg':'dist'}, inplace=True)
        # print(self.df)
        return self.df

    # def get_key_weights(self, first, second):



def layout_select(key_symbols):
    '''
    Returns the filename to compile the layout filename
    '''
    # [ord(i) in [32:127] for i in key_symbols]
    layouts = {0: 'us_Basic',
               1: 'hy_EasternAlt',
               2: 'hy_Eastern',
               3: 'hy_Western'}

    return layouts[i]


def arrange_keys(key_list, row_list):
    shift_val = 0
    for i in range(len(row_list)):
        if row_list[i] == 1:
            shift_val = 1.5
            # print(shift_val)
        elif row_list[i] == 2:
            shift_val = 1.5 + 0.2
        elif row_list[i] == 3:
            shift_val = 1.5 + 0.2 + 0.5

        # print(shift_val)
        key_list[i] += shift_val
        # print(row_list[i], key_list[i])

        # print(key_list)
    return key_list


def make_plot(key_dist, area):
    x = key_dist['dist'].tolist()
    print(len(key_dist))
    y = key_dist['row'].tolist()
    x = arrange_keys(x, y)
    y = [3.5 - i for i in y]

    # fig, ax = plt.subplots()
    fig = plt.figure(figsize=(10, 3))
    ax = fig.add_subplot(111)
    ax.xaxis.set_ticks(range(14))
    ax.yaxis.set_ticks(range(5))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(True)

    plt.scatter(x, y, s=area)


    # plt.hist2d(x, y, bins=52)
    plt.xlim(-0.5, 14)
    plt.ylim(0, 4)
    # plt.axis('off')

    # plt.plot(x, y, marker='o', linestyle='None', weights)
    plt.show()


if __name__ == '__main__':
    # import matplotlib.cm as cm
    layout = Layout_match()
    layout.read_file('hy_EasternAlt')
    layout.get_symbol_name_dict()
    key_dist = layout.create_key_distance()
    print(key_dist)

    area = (15 * np.random.rand(12))**2
    make_plot(key_dist, area)
