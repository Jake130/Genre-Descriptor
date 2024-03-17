import tkinter as tk
from PIL import ImageTk, Image
import urllib.request
import io
import spotify_requests as spr
import https_requests as mxr
import sys
from create_rankings_csv import create_rankings_csv
import display_album_ranking as dar

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
        self.stored_data = []           #Used as temporary storage for functions that are called
        self.selected_artist = None
        self.discography = None
        self.albums_data = []
        self.top_ten = []
        self.album_number = 0
        self.ratings = []

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
        self.reprompt_searched_artist()
        #self.entry.bind("<Return>", self.reprompt_searched_artist)

    def confirm_artist(self, event):
        input = self.get_input()
        if input.lower()=="no" or input.lower()=="no\n":
            self.reset_display()
            #self.reprompt_searched_artist(self.stored_data[0])
            self.reprompt_searched_artist()
        else:
            self.reset_display()
            #Create Data to be used throughout the program
            self.selected_artist = self.stored_data[-1]
            self.stored_data = []
            self.display_text("This exists...")
            self.discography = spr.get_discography(self.selected_artist['id'])
            if self.discography==[]:
                print("There are no artists under this name. Quiting...")
                sys.exit()
            self.display_text("Getting albums data...")
            self.albums_data = spr.get_album_data(self.discography)
            self.display_text("Making top ten...")
            self.top_ten = spr.make_top_ten(self.albums_data)
            self.album_number = len(self.top_ten)
            #print(self.top_ten)
            self.display_text("Getting track ratings...")
            self.ratings = spr.get_tracks_popularity(self.top_ten)
            #print(self.ratings)
            self.ratings = spr.partition_rankings(self.top_ten, self.ratings)
            self.display_text("Press enter to generate popularity index.")
            self.entry.bind("<Return>", self.generate_graph)
            #print(self.ratings)

            #print(self.discography)
            #print(len(self.discography))
            
            #self.top_albums = mxr.match_albums(self.discography, self.selected_artist['name'])
            #self.album_total_dict = mxr.map_album_total(self.top_albums, self.discography)
            #print(self.top_albums)
            #print(self.album_total_dict)
            #self.display_text("Now enter a valid mood...")
            #self.entry.bind("<Return>", self.get_mood)


    #def get_mood(self, event):
    #    mood = self.get_input()
    #    self.selected_mood = mood
    #   #Check if mood is an adjective
    #    self.reset_display()
    #    self.display_text("Creating Mood Visualization...")
    #    self.all_tracks = mxr.get_top_album_tracks(self.top_albums, self.album_total_dict)
    #    pass



    #------------------------------------
    def reprompt_searched_artist(self):
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
            self.display_photo()
        else:
            self.display_photo(image_url=this_artist['images'][1]['url'])
        self.stored_data.append(this_artist)
        self.entry.bind("<Return>", self.confirm_artist)

    def generate_graph(self, event):
        self.reset_display()
        create_rankings_csv(self.ratings)
        dar.make_graph()
        self.display_albums()
        self.display_photo(image_file="seaborn_plot.jpg")
        self.entry.bind("<Return>", self.do_nothing)

    def do_nothing(self, event):
        print("There's nothing else to do...")
        


    def display_photo(self, image_url:str=None, image_file:str=None):
        if image_url==None and image_file==None:
            img = Image.open("No_Picture.png")
            img = img.resize((320, 320))
            photo = ImageTk.PhotoImage(img)
        elif image_file!=None:
            img = Image.open(image_file)
            img = img.resize ((100+(self.album_number*85), 500))
            photo = ImageTk.PhotoImage(img)
        elif image_url!=None:
            with urllib.request.urlopen(image_url) as u:
                raw_data = u.read()
            img = Image.open(io.BytesIO(raw_data))
            photo = ImageTk.PhotoImage(img)
        photo_env = tk.Label(self.display_frame, image=photo)
        photo_env.photo = photo
        photo_env.pack()
    
    def display_albums(self):
        album_frame = tk.Frame(master=self.display_frame, bg='#fadd82')
        grey_img = Image.open("grey.png")
        grey_img = grey_img.resize((100, 85))
        grey_photo = ImageTk.PhotoImage(grey_img)
        grey_env = tk.Label(album_frame, image=grey_photo, padx=0)
        grey_env.grid(row=0,column=0,sticky="news")
        i = 1
        for album in self.top_ten:
            if album['images'][0]!=[]:
                with urllib.request.urlopen(album['images'][0]['url']) as u:
                    raw_data = u.read()
                img = Image.open(io.BytesIO(raw_data))
                img = img.resize((85,85))
                photo = ImageTk.PhotoImage(img)
            photo_env = tk.Label(album_frame, image=photo)
            photo_env.photo = photo
            photo_env.grid(row=0, column=i, sticky="news", padx=0)
            i += 1
        album_frame.pack()


    
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
    print(spr.get_access())
    gui = GUI()
    gui.mainloop()