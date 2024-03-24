# Genre-Descriptor

This is a simple Graphical User Interface (GUI), with a title, entry bar and display space that allows a user to
select a valid artist on the Spotify catalogue and generate a graphical representation of that artists most popular
albums (limited to 10), with all of their tracks rated based on their popularity. All data is gathered through Spotify's
Web API, with the only altercation being scaling its 0-100 index ratings to 0-50 index ratings.

This is an individual project by Jacob Kolster.

## How to use

The process of generating a graphical representation is spit up into three steps...
- Generating an access token: Spotify uses an OAuth 2.0 authentication process meaning, to access Spotify's data,
the user must get an `access token` every hour. If performing another search after an access token was generated within the
last hour, this step is not necessary.
- Searching for an artist: The User may enter the name of the artist they are searching for, the display space will show the
artist's image and information, the user may enter `no`, In which case, it will re-prompt the user for confirmation else, they
can hit enter and the stage will terminate.
- Grabbing an artists discography & track ratings: API calls are made to grab the adequate data and track ratings for the artist's
albums. The user must only hit enter when all data is gathered, and they are prompted.
- Creating and displaying a Graph: The display space shows the graphical representation that was generated.

## Generating an access token

Acess tokens to Spotify's stored data last one hour, if this is the first search of a session or an hour has passed a new one will need
to be generated. Do this by running the program, and in the console the long stream of random characters that follows `access token` can be copied,
and pasted between the empty quotations marks that come after the `SPOTIFY_BEARER_TOKEN` variable in the envirionment variable file `.env`. Terminate 
the program by closing the pop-up window, and run again to coninue to the next phase.

## Searching for an artist

To search for an artist, enter the artist's name in the entry bar. If the first artist that comes up is not the one you are looking for, enter "no" and
another artist will pop up. The process will repeat until the user hits enter in the entry bar to confirm the artist, or the program determines that there
are no valid artists of that name.

## Grabbing an artist's discography and track ratings: 

The program does this stage on its own, the user must only hit enter when the program instructs them to.

## Creating and displaying a graph

Hit enter and the program will take time to generate a graph on the display space. To restart the process, end the program by closing the window, and
run it again.
