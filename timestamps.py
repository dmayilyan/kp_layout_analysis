import subprocess
import sys
import os
import time


class _GetchUnix:
    def __init__(self):
        # import termios now or else you'll get the Unix version on the Mac
        import tty
        # import termios

    def __call__(self):
        import sys
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


def getKey():
    inkey = _GetchUnix()
    for i in range(sys.maxsize):
        k = inkey()
        if (k != ''):
            break
    return k


keys = []
keys_clean = []
timelist = []


# if os.path.isdir("./time_file"):
#     print("\nData folder exists\n")
# else:
#     print("Data folder doesn't exists\nMaking the folder")
#     os.mkdir("./time_file")
#     print("Data folder succesfully created")
def make_dir(text_filename):
    if os.path.isdir("./data_files") is False:
        # print("Data folder doesn't exists\nMaking the folder")
        print("Պանակը գոյություն չունի\n\nՍտեղծում եմ...")

    try:
        os.mkdir("./data_files")
        # print("Data folder succesfully created")
        print("Տվյալների պանակը հաջողությամբ ստեղծվեց\n")
        print("Տեքստը հասանելի կլինի %s հասցեով" % (text_filename))
    except file.exists:  # ????????????????????????????????????????????????????
        # print("\nData folder exists\n Jumping to the main code")
        print("\nՏվյալների պանակը գոյություն ունի\nԱնցնենք բուն գործին\n")
        print("Տեքստը հասանելի կլինի %s հասցեով" % (text_filename))
        pass
    except PermissionError:
        # print("\nDon't have permission to create the folder")
        print("\nՊանակ ստեղծելու արտոնություն չունեմ :/")
        pass


filename = time.strftime("%d.%m.%Y_%H:%M", time.localtime())
text_filename = "./data_files/text_" + filename
data_filename = "./data_files/data_" + filename

# Creating the work folder
make_dir(text_filename)


print("Տպեք տեքստը ստորև\n------------------------------")
while True:
    k = getKey()
    # Exiting on Esc key
    if k == "\x1b":
        print("\n\nProgram Stopped Manually!\n" +
              "------------------------------\n" +
              "Ծրագիրը հաջողությամբ ավարտվեց\n" +
              "Ձեր հավաքած տեքստը հասանելի է պանակում")
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
        sys.stdout.write("\b \b")
        sys.stdout.flush()
        # print(chr(8))


out_keys = sys.stdout
out_keys = open(text_filename, "w")
out_time = sys.stdout
out_time = open(data_filename, "w")
for k in range(len(keys)):
    if k == 0:
        t0 = timelist[0]
        out_time.write("%s\t%d\t%f\n" % (keys[k], ord(keys[k]), 0.0))
    else:
        print(keys[k], ord(keys[k]), (timelist[k] - t0) * 1000)
        out_time.write("%s\t%d\t%f\n" % (keys[k], ord(keys[k]),
                                         (timelist[k] - t0) * 1000))
        t0 = timelist[k]

for k in range(len(keys_clean)):
    out_keys.write(keys_clean[k])

# for j in range(1,len(timelist)):
#     print(keys[j], ord(keys[j]), (timelist[j] - t0)*1000)
#     t0 = timelist[j]

out_keys.close()
out_time.close()

print("Here you are!!!")
subprocess.check_call(['xdg-open', "./data_files"])
