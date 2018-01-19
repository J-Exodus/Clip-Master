from os.path import expanduser
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
    s.auth = ('', 'password')  # username blank, password is "password"

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


def format_times(seconds):
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)

    h = str(h).zfill(2)
    m = str(m).zfill(2)
    s = str(s).zfill(2)

    return h + ":" + m + ":" + s


def mark_position():

    global timeIn
    global timeOut
    global currentFile

    file_data = get_info()

    if timeIn == '0':
        timeIn = file_data[1]
        currentFile = file_data[0]
    else:
        timeOut = int(file_data[1]) - int(timeIn)
        timeIn = format_times(timeIn)
        timeOut = format_times(timeOut)
        write_to_file(file_data[0])


def write_to_file(file_id):

    global currentFile
    global timeIn
    global timeOut

    home = expanduser('~')
    rtn = '\r'

    cut_list = open(home + "/cut_list.txt", 'a')

    if file_id == currentFile:
        cut_list.write(timeIn + rtn + timeOut)


def mark_clip():
    global timeOut
    global clip_name

    mark_position()

    if timeOut != '0':
        app.entry.focus_set()
        clip_name = app.entry.get()
        app.entry.config(text='')


def get_clip_name():
    global clip_name

    clip_name = app.entry.get()
    print(clip_name)


class TkInterface(tkinter.Tk):
    def __init__(self, parent):
        tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialise()

    def initialise(self):
        self.grid()

        self.entry = tkinter.Entry(self)
        self.entry.grid(column=0, row=0, sticky='EW')
#        self.entry.bind("<Return>",lambda command=get_clip_name)

        mark_button = tkinter.Button(self, text=u"Mark Clip", command=mark_clip)
        mark_button.grid(column=1, row=0)

        info_label = tkinter.Label(self, text='Ready to mark clips...', anchor="w", fg="white", bg="blue")
        info_label.grid(column=0, row=2, sticky='EW')

        self.grid_columnconfigure(0, weight=1)
        self.resizable(False, False)


app = TkInterface(None)
app.title("Clip Master")
app.mainloop()


print("Time in is " + timeIn + " and time out is " + timeOut)
print("file is " + currentFile)
