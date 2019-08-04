import eyed3
import os
import glob
import tkinter as tk
from tkinter import ttk
from pygame import mixer

## Placement params from tkinter
W = tk.W 
N = tk.N 
E = tk.E 
S = tk.S 

class GUI(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        ## Get list with all mp3 file in directory
        self.mp3List = glob.glob("*.mp3")

        ## StringVar from tkinter for Entries
        self.mp3Name = tk.StringVar()
        self.trackArtist = tk.StringVar()
        self.trackTitle = tk.StringVar()

        ## Init pointer to current  mp3 file 
        self.mp3NumList = 0
        self.mp3Name.set(self.mp3List[self.mp3NumList])

        ## Name of program
        self.parent.title('Simpsort.Music')
        self.pack(fill="both", expand=True)

        self.center_window()
        self.track_edit()
        self.widgets_control()

        ## Binds for keyboard control
        self.bind_all('<KeyPress-Left>', self.prevMp3)
        self.bind_all('<KeyPress-Right>', self.nextMp3)

    def track_edit(self):
        """
        Main method for editing of mp3 tags.
        """

        ## Get current mp3 for eyed3
        self.audiofile = eyed3.load(self.mp3List[self.mp3NumList])

        ## Check if tags exists
        ## Otherwise itit tags
        if hasattr(self.audiofile.tag, 'artist'):
            pass
        else:
            self.audiofile.initTag()

        ## Check if tag 'artist' not empty in mp3 file
        ## Else get artist of track from mp3 file name
        if self.audiofile.tag.artist != None:
            self.trackArtist.set(self.audiofile.tag.artist)
        else:
            self.trackArtist.set(self.mp3List[self.mp3NumList][0:self.mp3List[self.mp3NumList].find(' - ')])

        ## Check if tag 'title' not empty in mp3 file
        ## Else get titile of track from mp3 file name
        if self.audiofile.tag.title != None:
            self.trackTitle.set(self.audiofile.tag.title)
        else:
            self.trackTitle.set(self.mp3List[self.mp3NumList][(self.mp3List[self.mp3NumList].find(' - ') + 3):(self.mp3List[self.mp3NumList].find('.'))])

    def center_window(self):
        """
        Method for centering window.
        """
        width = 700
        height = 500

        screenWidth = self.parent.winfo_screenwidth()
        screenHeight = self.parent.winfo_screenheight()

        centerX = (screenWidth - width) / 2
        centerY = (screenHeight - height) / 2

        self.parent.geometry('%dx%d+%d+%d' % (width, height, centerX, centerY))

    def widgets_control(self):
        """
        Create all the widgets.
        """
        self.columnconfigure(1, weight=1)
        self.rowconfigure(6, weight=1)
        
        ## Label and entry with mp3 file name
        labelName = tk.Label(self, text="MP3 file name: ")
        labelName.grid(row=0, column=0, sticky=W, pady=5, padx=5)

        self.entryName = ttk.Entry(self, textvariable=self.mp3Name)
        self.entryName.grid(row=1, column=0, columnspan=3, sticky=E+W+N, pady=5, padx=5)

        ## Label and entry with track artist
        labelArtist = tk.Label(self, text="Artists of track: ")
        labelArtist.grid(row=2, column=0, sticky=W, pady=5, padx=5)

        self.entryArtist = ttk.Entry(self, textvariable=self.trackArtist)
        self.entryArtist.grid(row=3, column=0, columnspan=3, sticky=E+W+N, pady=5, padx=5)

        ## Label and entry with track title
        labelTitle = tk.Label(self, text="Title of track: ")
        labelTitle.grid(row=4, column=0, sticky=W, pady=5, padx=5)

        self.entryTitle = ttk.Entry(self, textvariable=self.trackTitle)
        self.entryTitle.grid(row=5, column=0, columnspan=3, sticky=E+W+N, pady=5, padx=5)

        ## Previous track button
        buttonPrev = ttk.Button(self, text="Prev", command=self.prevMp3)
        buttonPrev.grid(row=6, column=0, pady=5, padx=5, sticky=W+S)

        ## Applay changes button
        buttonApply = ttk.Button(self, text="Apply", command=self.applyChanges)
        buttonApply.grid(row=6, column=1, pady=5, padx=5, sticky=S)

        ## Next track button
        buttonNext = ttk.Button(self, text="Next", command=self.nextMp3)
        buttonNext.grid(row=6, column=2, pady=5, padx=5, sticky=E+S)

    def nextMp3(self, _event=None):
        """
        Method for moving forward in list with return back
        """
        if self.mp3NumList != len(self.mp3List) - 1:
            self.mp3NumList += 1
        else:
            self.mp3NumList = 0
        self.mp3Name.set(self.mp3List[self.mp3NumList])
        self.track_edit()

    def prevMp3(self, _event=None):
        """
        Method for moving backward in list with return forward
        """
        if self.mp3NumList != 0:
            self.mp3NumList -= 1
        else:
            self.mp3NumList = len(self.mp3List) - 1
        self.mp3Name.set(self.mp3List[self.mp3NumList])
        self.track_edit()

        # mixer.init()
        # mixer.music.load(self.mp3List[self.mp3NumList])
        # mixer.music.play()

    def applyChanges(self, _event=None):
        """
        Method for applying changes. Name of mp3 file will be rewritten, tags will be added.
        """
        self.audiofile.tag.artist = self.trackArtist.get()
        self.audiofile.tag.title = self.trackTitle.get()
        self.audiofile.tag.save()

        os.rename(self.mp3List[self.mp3NumList], self.entryName.get())
        self.mp3List[self.mp3NumList] = self.entryName.get()

        self.nextMp3()

## Create main window
root = tk.Tk()
## Window not sizable
root.resizable(0,0)
iconImg = tk.PhotoImage(file='dave-vinyl.png')
root.tk.call('wm', 'iconphoto', root._w, iconImg)
ui = GUI(root)
root.mainloop()