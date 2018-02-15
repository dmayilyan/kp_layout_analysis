import tempfile
import atexit

import os

import wikipedia as wiki
import sqlite3
# from itertools import chain

conn = sqlite3.connect(':memory:')

c = conn.cursor()

c.execute('''CREATE TABLE pairs (
             key_pair text,
             count integer
             )''')


pair_dict = {'a': 0}

def in_range_arm(s):
    other_chars = (' ', '(', ')', ',')
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
        # print(lin)
        # print('/////////////////////////')
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
        # lin = ''.join([s for s in lin if not in_range_arm(s)])
        #  Use double spaces to reset the pattern detection
        # print(lin)
        # print('????')
        out_list.append(lin)

    return out_list


def count_pairs(line):
    for i in range(len(line) - 1):
        pair = ''.join(line[i:i + 2])

        if pair in pair_dict:
            pair_dict[pair] += 1
        else:
            pair_dict[pair] = 1


def insert_db(cont):
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    for line in cont:
        count_pairs(line)

    for (key, value) in pair_dict.items():
        # print(key, value)
        c.execute('INSERT INTO pairs VALUES (:key_pair, :count)',
                  {'key_pair': key, 'count': value})

    conn.commit()


def wiki_parse():
    # qwe = 'խւէ'
    # are_all_chars_out(qwe)
    # qwe = 'qwe'
    # are_all_chars_out(qwe)
    wiki.set_lang('hy')
    t = wiki.random()
    page = wiki.page(title=t)
    # page = wiki.page('Համշեն_արեւմտահայերէն')
    print(page.title)
    # p_content = page.content
    p_content = page.content.splitlines()
    print(p_content)
    print(len(p_content))

    content_clean = cleanup(p_content)

    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print(content_clean)
    print(len(content_clean))

    insert_db(content_clean)
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
