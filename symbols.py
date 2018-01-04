#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd

def layout_select():
    '''
    Returns the filename to compile the layout filename
    '''
    layouts = {0: 'us_Basic',
               1: 'hy_EasternAlt',
               2: 'hy_Eastern',
               3: 'hy_Western'}

    return layouts[i] # !!!!!!!!!!!!!


def get_symbol_dict():
    '''
    Returns a Dictionary of KEY_NAME: (symbol, SYMBOL) structure
    '''

    df = pd.read_table('./xkb layouts/hy_Eastern',
                       header=None,
                       names=['sy', 'reg', 'cap'])
    # for (b, B)
    mydict = dict(zip(df.sy, zip(df.reg, df.cap)))
    print(mydict)
    return mydict


if __name__ == '__main__':
    get_symbol_dict()
