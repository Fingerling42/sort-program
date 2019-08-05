import eyed3
import os
import glob
import tkinter as tk
from tkinter import ttk
from pygame import mixer

# Placement params from tkinter
W = tk.W 
N = tk.N 
E = tk.E 
S = tk.S 


class GUI(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        # Name of program
        self.parent.title('Simpsort.Music')
        self.pack(fill="both", expand=True)


        # Get list with all mp3 file in directory
        self.mp3List = glob.glob("*.mp3")

        # StringVar from tkinter for Entries
        self.mp3Name = tk.StringVar()
        self.trackArtist = tk.StringVar()
        self.trackTitle = tk.StringVar()

        # Init pointer to current  mp3 file
        self.mp3NumList = 0
        self.mp3Name.set(self.mp3List[self.mp3NumList])

        self.center_window()
        self.track_edit()
        self.widgets_control()

        # Binds for keyboard control
        self.bind_all('<KeyPress-Left>', self.prevMp3)
        self.bind_all('<KeyPress-Right>', self.nextMp3)

    def track_edit(self):
        """
        Main method for editing of mp3 tags.
        """

        # Get current mp3 for eyed3
        self.audiofile = eyed3.load(self.mp3List[self.mp3NumList])

        # Check if tags not exists itit tags
        if hasattr(self.audiofile.tag, 'artist') == False or hasattr(self.audiofile, 'tag') == False:
            self.audiofile.initTag()

        # Check if tag 'artist' not empty in mp3 file
        # Else get artist of track from mp3 file name
        if self.audiofile.tag.artist is not None:
            self.trackArtist.set(self.audiofile.tag.artist)
        else:
            self.trackArtist.set(self.mp3List[self.mp3NumList][0:self.mp3List[self.mp3NumList].find(' - ')])

        # Check if tag 'title' not empty in mp3 file
        # Else get title of track from mp3 file name
        if self.audiofile.tag.title is not None:
            self.trackTitle.set(self.audiofile.tag.title)
        else:
            self.trackTitle.set(self.mp3List[self.mp3NumList][(self.mp3List[self.mp3NumList].find(' - ') + 3):(self.mp3List[self.mp3NumList].find('.'))])

    def center_window(self):
        """
        Method for centering window.
        """
        width = 900
        height = 600

        screenWidth = self.parent.winfo_screenwidth()
        screenHeight = self.parent.winfo_screenheight()

        centerX = (screenWidth - width) / 2
        centerY = (screenHeight - height) / 2

        self.parent.geometry('%dx%d+%d+%d' % (width, height, centerX, centerY))

    def widgets_control(self):
        """
        Create all the widgets.
        """
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(4, weight=1)
        self.rowconfigure(8, weight=2)

        # Test lebel
        labelTest = tk.Label(self, text="Genres (sometimes...)")
        labelTest.grid(row=0, column=0, rowspan=10, sticky=W+S, pady=5, padx=5)
        
        # Label and entry with mp3 file name
        labelName = tk.Label(self, text="MP3 file name: ")
        labelName.grid(row=0, column=1, sticky=W, pady=5, padx=5)

        self.entryName = ttk.Entry(self, textvariable=self.mp3Name)
        self.entryName.grid(row=1, column=1, columnspan=4, sticky=W+E, pady=5, padx=5)

        # Label and entry with track artist
        labelArtist = tk.Label(self, text="Artists of track: ")
        labelArtist.grid(row=2, column=1, sticky=W, pady=5, padx=5)

        self.entryArtist = ttk.Entry(self, textvariable=self.trackArtist)
        self.entryArtist.grid(row=3, column=1, columnspan=4, sticky=W+E, pady=5, padx=5)

        # Label with track title and album title
        labelTitle = tk.Label(self, text="Title of track: ")
        labelTitle.grid(row=4, column=1, sticky=W, pady=5, padx=5)

        labelAlbum = tk.Label(self, text="Title of album: ")
        labelAlbum.grid(row=4, column=3, sticky=W, pady=5, padx=5)

        # Entry with track title and album title
        self.entryTitle = ttk.Entry(self, textvariable=self.trackTitle)
        self.entryTitle.grid(row=5, column=1, sticky=W+E, columnspan=2, pady=5, padx=5)

        self.entryAlbum = ttk.Entry(self)
        self.entryAlbum.grid(row=5, column=3, columnspan=2, sticky=W+E, pady=5, padx=5)

        # Label with year and genre
        labelYear = tk.Label(self, text="Year of realise: ")
        labelYear.grid(row=6, column=1, sticky=W, pady=5, padx=5)

        labelGenre = tk.Label(self, text="Genre: ")
        labelGenre.grid(row=6, column=3, sticky=W, pady=5, padx=5)

        # Entry with year and genre
        self.entryYear = ttk.Entry(self)
        self.entryYear.grid(row=7, column=1,  columnspan=2, sticky=W+E, pady=5, padx=5)

        self.entryGenre = ttk.Entry(self)
        self.entryGenre.grid(row=7, column=3, columnspan=2, sticky=W+E, pady=5, padx=5)

        # Play button
        buttonPlay = ttk.Button(self, text="Play")
        buttonPlay.grid(row=8, column=1, pady=5, padx=5, sticky=W+S)

        # Previous track button
        buttonPrev = ttk.Button(self, text="Prev", command=self.prevMp3)
        buttonPrev.grid(row=9, column=1, pady=5, padx=5, sticky=W+S)

        # Apply changes button
        buttonApply = ttk.Button(self, text="Apply", command=self.applyChanges)
        buttonApply.grid(row=9, column=2, pady=5, padx=5, sticky=S)

        # Move track to final folder
        buttonFinal = ttk.Button(self, text="Finalize")
        buttonFinal.grid(row=9, column=3, pady=5, padx=5, sticky=S)

        # Next track button
        buttonNext = ttk.Button(self, text="Next", command=self.nextMp3)
        buttonNext.grid(row=9, column=4, pady=5, padx=5, sticky=E+S)

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

# Create main window
root = tk.Tk()
# Window not sizable
root.resizable(0,0)
iconImg = tk.PhotoImage(file='dave-vinyl.png')
root.tk.call('wm', 'iconphoto', root._w, iconImg)
ui = GUI(root)
root.mainloop()
