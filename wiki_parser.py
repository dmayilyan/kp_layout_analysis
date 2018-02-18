import tempfile
import atexit

import os

import wikipedia as wiki
import sqlite3
# from itertools import chain

# conn = sqlite3.connect(':memory:')


# if os.path.isfile('./Databases/hy_wiki.db'):

# else:
conn = sqlite3.connect('./Databases/hy_wiki.db')


c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS pairs (
             key_pair text,
             use_count integer
             )''')


pair_dict = {}
# article_set = set()


def in_range_arm(s):
    # other_chars = (' ', '(', ')', ',')
    other_chars = (' ', ',')
    if 1328 < ord(s) < 1423 or s in other_chars:
        return 1
    else:
        return 0


def are_all_chars_out(line):
    '''
    Check if all chars in the list are out of the selected language range.
    '''
    if any([in_range_arm(i) for i in line]):
        # print('False')
        return 0
    else:
        # print('True')
        return 1

# def is_unicode_av_out(line):
#     un_sum = 0
#     for i in line:
#         un_sum += ord(i)

#     print(un_sum)


# Do the ckeaning. Need to decide on cleaning patter
def cleanup(p_content):
    out_list = []
    for lin in p_content:
        # print(type(lin))
        if '=' in lin:
            continue
        if len(lin) == 0:
            continue
        if are_all_chars_out(lin):
            continue
        temp_str = ''
        for s in lin:
            if in_range_arm(s):
                if temp_str.endswith(' ') and s == ' ':
                    continue
                temp_str += s

        # This nuimber choice is not perfect for latin languages
        if len(set(temp_str)) < 5:
            continue

        lin = temp_str
        out_list.append(lin)

    return out_list


def count_pairs(line):
    for i in range(len(line) - 1):
        pair = ''.join(line[i:i + 2])

        if pair in pair_dict:
            pair_dict[pair] += 1
        else:
            pair_dict[pair] = 1


def key_exist(symbols):
    c.execute('''SELECT EXISTS(SELECT 1 FROM pairs
                                      WHERE key_pair=:key_pair)''',
              {'key_pair': symbols})

    return c.fetchone()[0]


def insert_db(cont):
    for line in cont:
        count_pairs(line)

    for (key, value) in pair_dict.items():
        # print(key, value)
        if key_exist(key):
            c.execute(''' SELECT * FROM pairs WHERE key_pair=:key_pair''',
                      {'key_pair': key})
            old_val = c.fetchone()
            # print(old_val)
            c.execute('''UPDATE pairs SET use_count=:new_count
                         WHERE key_pair=:key_pair''',
                      {'key_pair': key, 'new_count': old_val[1] + value})
        else:
            c.execute('INSERT INTO pairs VALUES (:key_pair, :use_count)',
                      {'key_pair': key, 'use_count': value})

    conn.commit()


def wiki_parse():
    wiki.set_lang('hy')
    fo = open('./Databases/hy_article_list', 'a+')
    article_set = set(fo.readlines())
    for i in range(200):
        try:
            print(article_set)
            t = wiki.random()
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

            content_clean = cleanup(p_content)

            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print(content_clean)
            print(len(content_clean))

            insert_db(content_clean)

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



    # f, path = create_temp()
    # with open(path, 'w') as temp_f:
    #     temp_f.write(p_content)

    # print('--------------------------')
    # print(path)
    # with open(path, 'r+') as temp_f:
    # # for line in f:
    #     print(temp_f.read())


# Creating a temp file
def create_temp(prefix='tmp'):
    f, path = tempfile.mkstemp(prefix)
    # tempfile.mkstemp
    remove_at_exit(f, path)
    return f, path


# Cleaning up at the end
def remove_at_exit(f, path):
    # atexit.register(os.close, f)
    atexit.register(os.remove, path)
    # conn.close()


if __name__ == '__main__':
    wiki_parse()
