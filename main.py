import https_requests as mxr
import spotify_requests as spr
import sys




def main():
    arguments = sys.argv
    if len(sys.argv)<3:
        raise RuntimeError("There are too little arguments!")
    if len(sys.argv)>5:
        raise RuntimeError("More than four arguments were entered!")
    #Allow the user to search for the artist they're looking for
    #print(spr.get_access())
    searched_artist = spr.search_artist(arguments[1])
    index = 0
    while True:
        response = spr.reprompt_searched_artist(searched_artist, index)
        index += 1
        if response==False:
            break
    index -= 1
    selected_artist = searched_artist['artists']['items'][index]['id']
    #Make album list from Spotify API
    album_list = spr.get_discography(selected_artist)
    print(album_list)
    if album_list==[]:
        print("There are no albums under this artist's name. Quiting...")
        sys.exit()
    



if __name__=="__main__":
    main()