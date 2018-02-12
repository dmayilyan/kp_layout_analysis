import tempfile
import atexit

import os

import wikipedia as wiki


def in_range_arm(s):
    other_chars = (' ', '(', ')')
    if 1328 < ord(s) < 1423 or s in other_chars:
        return 0
    else:
        return 1

# Do the ckeaning. Need to decide on cleaning patter
def cleanup(p_content):
    for lin in p_content:
        if '=' in lin:
            continue
        if len(lin) == 0:
            continue
        print(lin)
        print('/////////////////////////')
        lin = ''.join([s for s in lin if not in_range_arm(s)])
        #  Use double spaces to reset the pattern detection
        print(lin)
        print('????')


def wiki_parse():
    wiki.set_lang('hy')
    t = wiki.random()
    page = wiki.page(title=t)
    print(page.title)
    p_content = page.content
    print(p_content)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    p_content = page.content.splitlines()

    cleanup(p_content)

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


if __name__ == '__main__':
    wiki_parse()
