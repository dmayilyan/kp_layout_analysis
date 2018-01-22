#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd


class layout_match(object):
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
        # print(self.df)

        mydict = dict(zip(self.df.reg, self.df.k_name))
        mydict.update(dict(zip(self.df.cap, self.df.k_name)))
        # return mydict

    def create_key_distance(self):
        '''
        Creating some info on key positions, counting from left top edge
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
        print(self.df)
        # return df


def layout_select(key_symbols: list):
    '''
    Returns the filename to compile the layout filename
    '''
    # [ord(i) in [32:127] for i in key_symbols]
    layouts = {0: 'us_Basic',
               1: 'hy_EasternAlt',
               2: 'hy_Eastern',
               3: 'hy_Western'}

    return layouts[i]


if __name__ == '__main__':
    layout = layout_match()
    # layout.detect_layout()
    layout.read_file('hy_EasternAlt')
    layout.get_symbol_name_dict()
    layout.create_key_distance()
