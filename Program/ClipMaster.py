# ===========================================================================================
# Title: Clip Master
# Version: 0.8
# Author: J-Exodus
# Python Version: Tested on python 3.6 Arch Linux OS
# ===========================================================================================
#
# Below are the user changeable parameters for Clip Master
# Ensure you have read the README.txt for correct setup of your VLC player

# Username and password to access the VLC web interface.
USER_NAME = ''
PASSWORD = 'password'

# File path for videos being processed, in relation to your home folder.
IN_PATH = '/Videos/'

# File path for processed clips to be saved, in relation to your home folder.
OUT_PATH = '/Videos/'

# If you wish to have your processed videos moved to another folder, change the option below to True
# If true, set the location to move your processed videos, in relation to your home folder.
MOVE_PROCESSED = True
MOVE_PATH = '/Videos/processed/'

# ============================================================================================
# ============================================================================================

from os.path import expanduser
import os
import subprocess
import tkinter
import requests
import xml.etree.ElementTree as ElmTree

currentFile = ''
timeIn = '0'
timeOut = '0'
clip_name = ''


def get_info():

    global timeIn
    filename = ''

    s = requests.Session()
    s.auth = (USER_NAME, PASSWORD)  # username blank, password is "password"

    try:
        r = s.get('http://localhost:8080/requests/status.xml', verify=False)

        if'401 Client error' in r.text:
            print('Web Interface Error: Check web interface settings and password.')
            return
    except Exception:
        print("Can not connect with VLC web interface. Please check settings as described in the README.txt file.")
        return

    root = ElmTree.fromstring(r.content)

    for info in root.iter('info'):
        name = info.get('name')

        if name == 'filename':
            filename = info.text

    current_time = root.find('time').text

    return [filename, current_time]


def format_times(seconds, rtn_type):
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)

    if rtn_type == "base":
        return h, m, s
    else:
        h = str(h).zfill(2)
        m = str(m).zfill(2)
        s = str(s).zfill(2)

        return h + ":" + m + ":" + s


def write_to_file():

    global currentFile
    global timeIn
    global timeOut
    global clip_name

    clip_name = app.entry.get()
    app.entry.delete(0, 'end')
    app.save_button.grid_forget()
    app.entry.grid_forget()
    app.mark_button.grid(column=1, row=6, padx=20)

    home = expanduser('~')
    rtn = '\r'

    cut_list = open(home + "/cut_list.txt", 'a')
    cut_list.write(currentFile + rtn + clip_name + rtn + timeIn + rtn + timeOut + rtn)
    cut_list.close()

    app.rest_button.grid_forget()

    app.info_label.config(text='Clip successfully saved for processing.')
    app.info_label.after(3000, app.info_label.config(text='Ready to mark clips...'))

    reset_markers()


def reset_markers():
    global timeIn
    global timeOut
    global currentFile
    global clip_name

    timeIn = '0'
    timeOut = '0'
    currentFile = ''
    clip_name = ''

    app.rest_button.grid_forget()
    app.info_label.config(text='Ready to mark clips...')


def mark_clip():
    global timeOut
    global clip_name
    global timeIn
    global currentFile

    file_data = get_info()

    if timeIn == '0':
        timeIn = file_data[1]
        currentFile = file_data[0]
        mark_in = format_times(file_data[1], "base")

        if mark_in[0] == 0 and mark_in[1] == 0:
            info_msg = "Clip start position marked at {0} seconds.".format(mark_in[2])
        elif mark_in[0] == 0:
            info_msg = "Clip start position marked at {0} mins, {1} seconds.".format(mark_in[1], mark_in[2])
        else:
            info_msg = "Clip start position marked at {0} hours, {1} mins, {2} seconds.".format(mark_in[0], mark_in[1], mark_in[2])
        app.info_label.config(text=info_msg)
        app.rest_button.grid(column=0, row=6, sticky='W', padx=20)
    else:
        timeOut = int(file_data[1]) - int(timeIn)
        timeIn = format_times(timeIn, '0')
        timeOut = format_times(timeOut, '0')
        app.mark_button.grid_forget()
        app.entry.grid(column=0, row=4, sticky='EW', columnspan=2)
        app.entry.focus_set()
        app.save_button.grid(column=1, row=6, padx=20)
        app.info_label.config(text='Enter a clip name and press the save button.')


def process_clips():

    global currentFile
    global timeIn
    global timeOut
    global clip_name

    home = expanduser('~')
    in_path = home + IN_PATH
    out_path = home + OUT_PATH

    lines = [line.rstrip('\n') for line in open(home + '/cut_list.txt')]
    total_lines = len(lines) - 4
    x = 0

    while x <= total_lines:
        subprocess.call(['ffmpeg', '-i', in_path + lines[x], '-ss', lines[x + 2], '-t', lines[x + 3], out_path + lines[x + 1] + ".mp4"])

        if MOVE_PROCESSED:
            os.rename(home + IN_PATH + lines[x], home + OUT_PATH + lines[x])

        x = x + 4

    os.remove(home + '/cut_list.txt')


class TkInterface(tkinter.Tk):
    def __init__(self, parent):
        tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialise()

    def initialise(self):
        width = 300
        height = 200
        self.geometry('{}x{}'.format(width, height))
        self.grid()

        self.entry = tkinter.Entry(self)
        self.entry.grid(column=0, row=4, sticky='EW', pady=5, columnspan=2)
        self.entry.grid_forget()

        self.mark_button = tkinter.Button(self, text=u"Mark Clip", command=mark_clip)
        self.mark_button.grid(column=1, row=6, padx=20)

        self.save_button = tkinter.Button(self, text=u"Save clip for processing", command=write_to_file)
        self.rest_button = tkinter.Button(self, text='Reset', command=reset_markers)
        self.process_clips = tkinter.Button(self, text='Finish and process marked clips', command=process_clips)
        self.process_clips.grid(column=0, row=8, columnspan=2)

        status_label = tkinter.Label(self, text=u'Current status')
        status_label.config(font=("Courier", 16))
        status_label.grid(column=0, row=1, columnspan=2)
        self.info_label = tkinter.Label(self, text='Ready to mark clips...', fg="white", bg="steel blue", pady=10)
        self.info_label.grid(column=0, row=2, sticky='EW', columnspan=2)
        spacer_label = tkinter.Label(self, text=" ")
        spacer_label.grid(column=0, row=3)
        spacer_label1 = tkinter.Label(self, text=" ")
        spacer_label1.grid(column=0, row=4)
        spacer_label2 = tkinter.Label(self, text=" ")
        spacer_label2.grid(column=0, row=5)
        spacer_label3 = tkinter.Label(self, text=" ")
        spacer_label3.grid(column=0, row=7, columnspan=2, sticky='EW')

        self.grid_columnconfigure(0, weight=1)
        self.resizable(False, False)


app = TkInterface(None)
app.title("Clip Master")
app.mainloop()
