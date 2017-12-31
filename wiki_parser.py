import tempfile
import atexit

import os

import wikipedia as wiki


# Do the ckeaning. Need to decide on cleaning patter
# def cleanup():


def wiki_parse():
    wiki.set_lang('hy')
    t = wiki.random()
    page = wiki.page(title=t)
    print(page.title)
    p_content = page.content
    print(p_content)

    f, path = create_temp()
    with open(path, 'w') as temp_f:
        temp_f.write(p_content)

    print('--------------------------')
    with open(path, 'r+') as temp_f:
    # for line in f:
        print(temp_f.read())


# Creating a temp file
def create_temp(prefix='tmp'):
    f, path = tempfile.mkstemp(prefix)
    tempfile.mkstemp
    tempfile.mkstemp
    remove_at_exit(f, path)
    return f, path


# Cleaning up at the end
def remove_at_exit(f, path):
    # atexit.register(os.close, f)
    atexit.register(os.remove, path)


if __name__ == '__main__':
    wiki_parse()
