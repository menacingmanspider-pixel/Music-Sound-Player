from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import pygame
import os
import time
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from PIL import Image, ImageTk
import io


root = Tk()
root.title("SoundPlayer")
root.geometry("600x250")
root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)


pygame.mixer.init()
pygame.mixer.music.set_volume(1)
Sounds = os.listdir("Sounds")

currentsound = 0
Playing = False

SoundName = StringVar(value = "SoundName")

def PlayPage():
    PlayPageMainFrame = ttk.Frame(root, borderwidth=1, relief="raised", padding=20)
    PlayPageMainFrame.grid(column=1, row=1, sticky=(N,E,S,W))
    PlayPageMainFrame.rowconfigure(1, weight=1) 
    PlayPageMainFrame.rowconfigure(2, weight=1) 
    PlayPageMainFrame.rowconfigure(3, weight=1) 
    PlayPageMainFrame.columnconfigure(2, weight=1) 


    SoundDisplayFrame = ttk.Frame(PlayPageMainFrame, relief="raised", width=200, height=200, borderwidth=1)
    SoundDisplayFrame.columnconfigure(1, weight=1)
    SoundDisplayFrame.rowconfigure(1, weight=1)
    SoundDisplayFrame.grid_propagate(False)
    SoundDisplayFrame.grid(column=1, row=1, sticky=(W), rowspan=3)

    global SoundDisplayLabel

    SoundDisplayLabel = ttk.Label(
    SoundDisplayFrame,
    text="No Album Art",
    anchor="center"
    )
    SoundDisplayLabel.grid(column=1, row=1, sticky=(W,E,N,S))

    Title1Label = ttk.Label(PlayPageMainFrame, textvariable=SoundName, borderwidth=1, relief="raised", anchor="se")
    Title1Label.grid(column=2, row=1)
    Title2Label = ttk.Label(PlayPageMainFrame, text="lorem ipsum lorem ipsum lorem ipsum lorem ipsum ", borderwidth=1, relief="raised", anchor="se")
    Title2Label.grid(column=2, row=2)

    ButtonsFrame = ttk.Frame(PlayPageMainFrame, relief="raised", borderwidth=1, padding=10)
    ButtonsFrame.grid(row=3, column=2)

    Button1 = ttk.Button(ButtonsFrame, text="Left")
    Button1.grid(column=1, row=1)
    def on():
        global Playing
        Playing = not Playing
        PlaySound()
        if Playing == False:
            StopSound()
    Button2 = ttk.Button(ButtonsFrame, text="Pause / Play", command=on)
    Button2.grid(column=2, row=1)
    Button3 = ttk.Button(ButtonsFrame, text="Right", command=NextSound)
    Button3.grid(column=3, row=1)

def UpdateAlbumArt(path):
    global SoundDisplayLabel
    global album_art_image

    try:
        audio = ID3(path)

        for tag in audio.values():
            if tag.FrameID == "APIC":
                image_data = tag.data

                image = Image.open(io.BytesIO(image_data))
                image = image.resize((180, 180))

                album_art_image = ImageTk.PhotoImage(image)

                SoundDisplayLabel.config(image=album_art_image, text="", anchor="center")
                return

    except Exception as e:
        print("No album art found:", e)

    SoundDisplayLabel.config(image="", text="No Album Art")

def PlaySound():
    global SoundName
    print("Playing")
    path = "Sounds/" + Sounds[currentsound]

    SoundName.set(Sounds[currentsound])
    print(Sounds[currentsound])
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
    UpdateAlbumArt(path)

def StopSound():
    pygame.mixer.music.stop()
    print("meow")

def NextSound():
    global Playing
    global currentsound
    Playing = True
    pygame.mixer.music.stop()
    currentsound += 1
    if currentsound >= len(Sounds):
        currentsound = 0
    PlaySound()

def CheckSound():
    if not pygame.mixer.music.get_busy() and Playing == True:
        print("Playing next")
        NextSound()

    root.after(1000, CheckSound)

PlayPage()
CheckSound()
root.mainloop()