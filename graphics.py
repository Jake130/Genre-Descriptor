import tkinter as tk
from PIL import ImageTk, Image
import urllib.request
import io
import spotify_requests as spr
import https_requests as mxr
import sys

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("500x500")
        self.root.configure(bg='#fadd82')
        self.root.title("Mood Visualization Project")

        #The header which stays static
        self.header = tk.Frame(master=self.root, bg='#fc9247')
        self.label = tk.Label(self.header, text="Mood Visualization Project", bg="#f7bf31", font=('Tekton Pro', 45))
        self.label.pack(padx=20, pady=20)

        self.text_var = tk.StringVar()
        self.entry = tk.Entry(self.header, textvariable=self.text_var, font=("Bell Gothic Std Light", 16))
        self.entry.pack(padx=20, pady=20)
        self.header.pack(fill='x')
        self.entry.bind('<Return>', self.start_search)

        self.display_frame = tk.Frame(master=self.root, bg='#fadd82')
        self.display_frame.pack()

        #Data we store throughout the program
        self.stored_data = []       #Used as temporary storage for functions that are called
        self.selected_artist = None
        self.discography = None
        self.selected_mood = None

    #Variables
    def get_input(self):
        text = self.text_var.get()
        #print(text)
        self.text_var.set("")
        return text


    """You need to make some functions corresponding to each phase of user
    input. These functions all use the get_input() function when called to 
    determine whether their phase has been satisfied with proper user input.
    Upon doing so, it performs functionality and binds a different function 
    to the entry."""

    def start_search(self, event):
        """Phase 1, the program wants a valid artist to search for..."""
        input = self.get_input()
        artist = spr.search_artist(input)
        #If it is a 400 error, end the program
        #TODO
        self.stored_data.append(artist)
        self.stored_data.append(-1)
        self.entry.bind("<Return>", self.reprompt_searched_artist)

    def confirm_artist(self, event):
        input = self.get_input()
        if input.lower()=="no" or input.lower()=="no\n":
            self.reset_display()
            self.reprompt_searched_artist(self.stored_data[0], )
        else:
            self.reset_display()

            self.selected_artist = self.stored_data[-1]
            self.stored_data = []
            self.discography = spr.get_discography(self.selected_artist['id'])
            print(self.discography)
            print(len(self.discography))
            if self.discography==[]:
                print("There are no artists under this name. Quiting...")
            #self.entry.bind("<Return", )
            #Then get discography

    def get_mood(self):
        mood = self.get_input()
        pass



    #------------------------------------
    def reprompt_searched_artist(self, event):
        #Stores the index in entry[1]
        self.stored_data[1] += 1
        if self.stored_data[1]>=self.stored_data[0]['artists']['limit']:
            print("There are no other artists under this name... quitting program")
            self.root.destroy()
            sys.exit()
        this_artist = self.stored_data[0]['artists']['items'][self.stored_data[1]]
        res = f"Is the artist you're looking for: {this_artist['name']}?\n"
        #Print all artist's genres and followers
        res += f"Followers: {this_artist['followers']['total']}\n"
        if this_artist['genres']!=[]:
            res += "\tKnown Genres: "
            for genre in this_artist['genres']:
                res += genre + ", "
            res += "\n"
        res += "Enter 'no' if this is not the case"
        self.display_reprompting(res)
        if this_artist['images']==[]:
            self.display_artist_photo(None)
        else:
            self.display_artist_photo(this_artist['images'][1]['url'])
        self.stored_data.append(this_artist)
        self.entry.bind("<Return>", self.confirm_artist)

    def reprompt_musixmatch(self, event):
        res = "Matching artist with their lyrics...\n"
        res += "Do they also go by these aliases?: "
        searched_artist = mxr.search_artist(self.selected_artist['name'])
        pass



    def display_artist_photo(self, image_url:str):
        if image_url==None:
            img = Image.open("No_Picture.png")
            img = img.resize((320, 320))
            photo = ImageTk.PhotoImage(img)
        else:
            with urllib.request.urlopen(image_url) as u:
                raw_data = u.read()
            img = Image.open(io.BytesIO(raw_data))
            photo = ImageTk.PhotoImage(img)
        artist_photo = tk.Label(self.display_frame, image=photo)
        artist_photo.photo = photo
        artist_photo.pack()
    
    def display_text(self, text:str):
        label = tk.Label(self.display_frame, text=text)
        label.pack()

    def reset_display(self):
        for widget in self.display_frame.winfo_children():
            widget.destroy()

    def display_reprompting(self, res:str):
        re_prompt = tk.Label(self.display_frame, text=res)
        re_prompt.pack()
    

    def mainloop(self):
        self.root.mainloop()


if __name__=="__main__":
    #print(spr.get_access())
    gui = GUI()
    gui.mainloop()