#!/usr/bin/env python
"""Module to catch keystrokes typed by the user."""
import subprocess
import sys
import tty
import termios
import os
import time
import hashlib


class _GetchUnix:
    def __call__(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


def getKey():
    """Get a key."""
    inkey = _GetchUnix()
    for i in range(sys.maxsize):
        k = inkey()
        if (k != ''):
            break
    return k


def make_dir(file_path):
    """Check data directory existance. If it doesn't exist, create it."""
    if os.path.isdir(file_path) is False:
        # print('Data folder doesn't exists\nMaking the folder')
        print('Պանակը գոյություն չունի\n\nՍտեղծում եմ...')

    try:
        os.mkdir(file_path)
        # print('Data folder succesfully created')
        print('Տվյալների պանակը հաջողությամբ ստեղծվեց\n')
        print('Տեքստը հասանելի կլինի %s հասցեով' % (file_path))
    except OSError:
        # print('\nData folder exists\n Jumping to the main code')
        print('\nՏվյալների պանակը գոյություն ունի\nԱնցնենք բուն գործին\n')
        print('Տեքստը հասանելի կլինի %s հասցեով' % (file_path))
        pass
    except PermissionError:
        # print('\nDon't have permission to create the folder')
        print('\nՊանակ ստեղծելու արտոնություն չունեմ :')
        pass


def write_kb_info(f_path, identifier):
    """Write keyboard info of the writer."""
    filename = f_path + identifier + '_kb_info'
    with open(filename, 'w') as f:
        subprocess.Popen(['setxkbmap', '-query'], stdout=f)


def do_tagging(f_path, t_posfix, d_posfix, ident):
    """Update text and data files with hash of the data file."""
    os.rename(f_path + t_posfix, f_path + ident + t_posfix)
    os.rename(f_path + d_posfix, f_path + ident + d_posfix)


def get_hash(filename):
    """Get hash of the data file."""
    md5 = hashlib.md5()
    with open(filename, 'rb') as f:
        file_content = f.read(65536)
        md5.update(file_content)

    return md5.hexdigest()


def main():
    keys = []
    keys_clean = []
    timelist = []

    # filename = time.strftime('%d.%m.%Y_', time.localtime())
    file_path = './data_files/'
    text_postfix = '_text'
    data_postfix = '_data'

    # Creating the work folder
    make_dir(file_path)

    print('Տպեք տեքստը ստորև\n------------------------------')
    while True:
        k = getKey()
        # Exiting on [Esc] key
        if k == '\x1b':
            print('\n\nProgram Stopped Manually!\n' +
                  '------------------------------\n' +
                  'Ծրագիրը հաջողությամբ ավարտվեց\n' +
                  'Ձեր հավաքած տեքստը հասանելի է պանակում')
            break
        # Next line is hit
        if ord(k) == 13:
            print(k)
        if k != chr(127):
            t = time.time()
            timelist.append(t)
            keys.append(k)
            keys_clean.append(k)
            sys.stdout.write(k)
            sys.stdout.flush()
        else:
            t = time.time()
            timelist.append(t)
            keys.append(k)
            keys_clean.pop()
            sys.stdout.write('\b \b')
            sys.stdout.flush()
            # print(chr(8))

    out_keys = sys.stdout
    out_keys = open(file_path + text_postfix, 'w')
    out_time = sys.stdout
    out_time = open(file_path + data_postfix, 'w')
    for k in range(len(keys)):
        if k == 0:
            t0 = timelist[0]
            out_time.write('%s\t%d\t%f\n' % (keys[k], ord(keys[k]), 0.0))
        else:
            # print(keys[k], ord(keys[k]), (timelist[k] - t0) * 1000)
            out_time.write('%s\t%d\t%f\n' % (keys[k], ord(keys[k]),
                                             (timelist[k] - t0) * 1000))
            t0 = timelist[k]

    for k in range(len(keys_clean)):
        out_keys.write(keys_clean[k])

    out_keys.close()
    out_time.close()

    print('Here you are!!!')
    subprocess.check_call(['xdg-open', './data_files'])

    print('Writing kb info')
    identifier = get_hash(file_path + data_postfix)
    write_kb_info(file_path, identifier)
    print('Attaching identifiers to the files')
    do_tagging(file_path, text_postfix, data_postfix, identifier)


if __name__ == '__main__':
    main()
