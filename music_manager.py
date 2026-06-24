"""
Menu driven, console based music management application. 

The program allows the user to create and save/load a json file of songs/albums, search, count and remove entries.

"""

import json

class Media:
    def __init__(self, title, year):
        self.title = title 
        self.year = year
    
    def display(self):
        print(f"Title: {self.title} | Year: {self.year} | ", end="")

class Song(Media):
    def __init__(self, title, year, artist, duration):
        super().__init__(title, year)
        self.artist = artist
        self.duration = duration
    
    def display(self):
        super().display()
        print(f"Artist: {self.artist} | Duration: {self.duration}s")

class Album(Media):
    def __init__(self, title, year, artist, tracklist):
        super().__init__(title, year)
        self.artist = artist
        self.tracklist = tracklist 
    
    def display(self):
        count = len(self.tracklist)
        super().display()   
        print(f"Artist: {self.artist} | Tracks: {count}")    
            
class Collection:
    def __init__(self, media):
        self.media = media
    
    def add_song(self):
        title = input("Enter title: ").strip()
        
        while True:
            year = input("Enter year: ").strip()
            if year.isdigit() and len(year) == 4:
                year = int(year)
                break
            else:
                print("Year must be a four digit number.")
        
        artist = input("Enter artist name: ").strip()
        
        while True:
            duration = input("Enter duration (seconds): ").strip()
            if duration.isdigit():
                duration = int(duration)
                break
            else:
                print("Duration must be a number.")
        
        new_song = Song(title, year, artist, duration)        
        self.media.append(new_song)
        print(f"New song: {title} added to list!")    
    
    def add_album(self):
        tracklist = []
        
        title = input("Enter title: ").strip()
        
        while True:
            year = input("Enter year: ").strip()
            if year.isdigit() and len(year) == 4:
                year = int(year)
                break
            else:
                print("Year must be a four digit number.")
        
        artist = input("Enter artist name: ").strip()
        
        while True:
            track_num = input("Enter number of tracks: ").strip()
            if track_num.isdigit():
                track_num = int(track_num)
                break
            else:
                print("Must be a number.")
        
        for x in range(track_num):
            new_track = input("Enter track title: ").strip()
            tracklist.append(new_track)
            print(f"{new_track} added to album!")
        
        new_album = Album(title, year, artist, tracklist)
        self.media.append(new_album)
        print(f"New album: {title} added to list!")           
        
    def display_all(self):
        for entry in self.media:
            entry.display()    
            
    def search_by_artist(self, artist):
        for entry in self.media:
            if entry.artist.lower().strip() == artist:
                entry.display() 
    
    def remove_by_title(self, title):
        self.media = [entry for entry in self.media if entry.title.lower() != title]
    
    def count_by_type(self):
        song_count = 0  
        album_count = 0
        
        for entry in self.media:
            if isinstance(entry, Song):
                song_count = song_count + 1
            else:    
                album_count = album_count + 1
        
        print(f"Song count: {song_count} | Album count: {album_count}")     
        
    def sort_by_year(self):
        ascending = sorted(self.media, key=lambda x: x.year)
        for entry in ascending:
            entry.display()
               
           
                        
def menu():
     
    #if file already exists, open file and convert saved dicts into song/album objects, appending them to empty collections list then convert list to collections obj
    try:
        with open("collection.json", "r") as file:
            collection_list = []
            collection = json.load(file)
            for entry in collection:
                if entry["type"] == "song":
                    entry = Song(entry["title"], entry["year"], entry["artist"], entry["duration"])
                    collection_list.append(entry)
                else:
                    entry = Album(entry["title"], entry["year"], entry["artist"], entry["tracklist"])
                    collection_list.append(entry)      
            collection_list = Collection(collection_list)                
    #if file does not exist, create new collections object from empty list                           
    except (FileNotFoundError, json.JSONDecodeError):
        collection_list = Collection([])
    
    run = True
    
    while run == True:
        print("=== Music Collection Manager ===")
        print("1. Add a song")
        print("2. Add an album")
        print("3. View all")
        print("4. Search by artist")
        print("5. Remove an item")
        print("6. View collection stats")
        print("7. Sort by year")
        print("8. Save and quit")
        
        while True:
            option = input("Enter option from menu: ")
            if option in ("1", "2", "3", "4", "5", "6", "7"):
                break
            else:
                print("Enter valid option from the menu.")
        
        if option == "1":
            collection_list.add_song()
        
        if option == "2":
            collection_list.add_album()
        
        if option == "3":
            collection_list.display_all()    
        
        if option == "4":
            artist = input("Enter artist name to search: ").lower().strip()
            collection_list.search_by_artist(artist) 
        
        if option == "5": 
            title = input("Enter title name to remove: ").lower().strip()
            collection_list.remove_by_title(title)
        
        if option == "6":
            collection_list.count_by_type()
            
        if option == "7":
            collection_list.sort_by_year()    
            
        if option == "8":
            my_collection = []
            with open("collection.json", "w") as file:
                for entry in collection_list.media:
                    if isinstance(entry, Song):
                        entry_dict = vars(entry)
                        entry_dict["type"] = "song" #tags the dict so it can be rebuilt as the correct class on reload
                    else:
                        entry_dict = vars(entry)
                        entry_dict["type"] = "album"
                    my_collection.append(entry_dict)    
                json.dump(my_collection, file)
            print("Collection saved!")    
            break
                    
                                                                            
menu()                 
        
        
        
        
                
            
       
            
        
        