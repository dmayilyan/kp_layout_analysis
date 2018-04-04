#!/usr/bin/env python
# -*- coding: utf-8 -*-

import atexit
# import os
import sys

import wikipedia as wiki
import sqlite3


class Wiki_parser:
    def __init__(self, lang):
        self.lang = lang
        db_name = './Databases/' + lang + '_wiki.db'
        self.art_list = './Databases/' + lang + '_article_list'
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()

        self.pair_dict = dict()

    def insert_db(self, cont):
        self._create_db()

        for line in cont:
            self.count_pairs(line)

        for (key, value) in self.pair_dict.items():
            # print(key, value)
            if self.key_exist(key):
                self.cur.execute(''' SELECT * FROM pairs WHERE
                                 key_pair=:key_pair''',
                                 {'key_pair': key})
                old_val = self.cur.fetchone()
                # print(old_val)
                self.cur.execute(''' UPDATE pairs SET use_count=:new_count
                                 WHERE key_pair=:key_pair''',
                                 {'key_pair': key,
                                  'new_count': old_val[1] + value})
            else:
                self.cur.execute(''' INSERT INTO pairs VALUES
                                 (:key_pair, :use_count)''',
                                 {'key_pair': key,
                                  'use_count': value})

        self.conn.commit()

    def key_exist(self, symbols):
        self.cur.execute('''SELECT EXISTS(SELECT 1 FROM pairs
                         WHERE key_pair=:key_pair)''',
                         {'key_pair': symbols})

        return self.cur.fetchone()[0]

    def count_pairs(self, line):
        for i in range(len(line) - 1):
            pair = ''.join(line[i:i + 2])

            if pair in self.pair_dict:
                self.pair_dict[pair] += 1
            else:
                self.pair_dict[pair] = 1

    def _create_db(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS pairs (
                     key_pair text,
                     use_count integer
                     )''')

    def read_db(self):
        atexit.register(self.conn.close())
        # conn = sqlite3.connect(db_name)
        # cur = conn.cursor()
        return self.cur.execute(''' SELECT * FROM pairs ''')
        # return(cur.fetchall())

    def are_all_chars_out(self, line):
        '''
        Check if all chars in the list are out of the selected language range.
        '''
        if any([in_range(self.lang, i) for i in line]):
            return 0
        else:
            return 1

    # Do the cleaning. Need to decide on cleaning pattern
    def cleanup(self, p_content):
        out_list = []
        for lin in p_content:
            # print(type(lin))
            if '=' in lin:
                continue
            if len(lin) == 0:
                continue
            if self.are_all_chars_out(lin):
                continue
            temp_str = ''
            for s in lin:
                if in_range(self.lang, s):
                    if temp_str.endswith(' ') and s == ' ':
                        continue
                    temp_str += s

            # This number choice is not perfect for latin languages
            if len(set(temp_str)) < 5:
                continue

            lin = temp_str
            out_list.append(lin)

        return out_list

    def parse(self):
        # print(str(self.lang))
        wiki.set_lang(self.lang)
        # wiki.set_lang('de')
        fo = open(self.art_list, 'a+')
        article_set = set(fo.readlines())
        t = wiki.random()
        for i in range(500):
            try:
                print(article_set)
                t = wiki.random()
                print('HERE', t)
                if t in article_set:
                    return 0
                else:
                    article_set.add(t)
                page = wiki.page(title=t)
                # page = wiki.page('Համշեն_արեւմտահայերէն')
                print(page.title)
                # p_content = page.content
                p_content = page.content.splitlines()
                # p_content = ['ու ու ուզցգզցգզցգծ']
                print(p_content)
                print(len(p_content))

                content_clean = self.cleanup(p_content)

                print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                print(content_clean)
                print(len(content_clean))

                self.insert_db(content_clean)


                # c.execute('SELECT Count(*) FROM pairs')
                # print(c.fetchall())

                # r = c.execute('SELECT * FROM pairs')
                # print(c.fetchall())

                # print(c['ու'], end=' qweqweqweq')

                # print(key_exist('ու')[0], end=' !!!!!!!!!!!!!!!!!!!!!!!!\n\n\n')

                print(article_set)
            except Exception:
                pass
        article_set = map(lambda x: x + '\n', article_set)
        print(article_set)
        fo.writelines(article_set)
        fo.close()


def in_range(lang, s):
    lang_detect = {'hy': (1328, 1423),
                   'en': (33, 126),
                   'de': (33, 126)}  # check with German keyboard keys

    lang_other_syms = {'hy': (' ', ',',),
                       'en': (' ',),
                       'de': (' ',)}

    lang_other_chars = {'hy': (),
                        'en': (),
                        'de': ('ä', 'Ä', 'ö', 'Ö', 'ü', 'Ü', 'ß')}

    # print(type(lang_other_syms[lang]))
    in_range = lang_detect[lang][0] <= ord(s) <= lang_detect[lang][1]
    if in_range or s in (lang_other_syms[lang] + lang_other_chars[lang]):
        return 1
    else:
        return 0


# def is_unicode_av_out(line):
#     un_sum = 0
#     for i in line:
#         un_sum += ord(i)

#     print(un_sum)

# Cleaning up at the end
# def remove_at_exit(f, path):
    # atexit.register(os.close, f)
    # atexit.register(os.remove, path)
    # conn.close()


def main(arg):
    wiki_data = Wiki_parser(arg)
    wiki_data.parse()


# Language preference is taken from argument
if __name__ == '__main__':
    lang_list = {'hy', 'en', 'de'}
    try:
        if len(sys.argv[1:]) != 1:
            raise ValueError
        if sys.argv[1] not in lang_list:
            raise Exception

        main(sys.argv[1])
    except ValueError:
        sys.exit('Too many or too few arguments, expect 1.')
    except Exception:
        sys.exit('Expect a value from %s set.' % lang_list)
