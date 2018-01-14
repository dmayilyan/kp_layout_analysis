#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd


def read_file():
    return pd.read_table('./xkb_layouts/hy_Eastern',
                         header=None)



def layout_select(key_symbols: list):
    '''
    Returns the filename to compile the layout filename
    '''
    # [ord(i) in [32:127] for i in key_symbols]
    layouts = {0: 'us_Basic',
               1: 'hy_EasternAlt',
               2: 'hy_Eastern',
               3: 'hy_Western'}

    return layouts[i]  # !!!!!!!!!!!!!


def create_key_distance():
    '''
    Creating some info on key positions
    '''
    df = read_file()
    df.columns = ['k_name', 'dist', 'row']
    # Loops are ugly as keyboard different models are uglier
    for index in df.index:
        if index < 13:
            df.ix[index].loc['dist'] = index + 1
            # Maybe it is better to switch to MultiIndex Meeeh...
            df.ix[index].loc['row'] = 0
        elif index < 26:
            df.ix[index].loc['dist'] = index % 13 + 1
            df.ix[index].loc['row'] = 1
        elif index < 37:
            df.ix[index].loc['dist'] = index % 13 + 1
            df.ix[index].loc['row'] = 2
        else:
            df.ix[index].loc['dist'] = index % 37 + 1
            df.ix[index].loc['row'] = 3

    # df = df['0', '1']
    # df.rename(columns={'reg':'dist'}, inplace=True)
    print(df)
    return df

def get_symbol_name_dict():
    '''
    Returns a dictionary of symbol: key_abbr structure
    '''

    df = read_file()
    df.columns = ['k_name', 'reg', 'cap']
    # print(df)

    mydict = dict(zip(df.reg, df.k_name))
    mydict.update(dict(zip(df.cap, df.k_name)))
    return mydict


if __name__ == '__main__':
    get_symbol_name_dict()
    create_key_distance()
    # layout_select([q,w,e,r,t,y])
