"""Start off with list[tup[int]] of total song rankings
by album"""

total_rankings = [(10, 20, 30, 40), 
                  (20, 20, 25),
                  (13, 15, 49)]

total_rankings2 = [(63, 71, 65, 74, 71, 80, 56, 60, 61, 84, 63, 60), 
                   (63, 88, 52, 51, 62, 56, 50, 50, 49, 49, 48, 61), 
                   (61, 63, 78, 74, 59, 63, 75, 66, 65, 70, 57, 70), 
                   (66, 65, 71, 74, 74, 62, 67, 68, 77, 62), 
                   (71, 57, 59, 70, 54, 59, 54, 62, 53, 62, 50), 
                   (59, 61, 59, 52, 53, 55, 55, 52, 59, 50, 64), 
                   (62, 50, 58, 48, 52, 56, 47, 47, 62, 52, 50, 52, 49, 58), 
                   (51, 63, 47, 61, 59, 62, 47, 48, 46, 48, 53), 
                   (42, 45, 41, 49, 49, 50, 37, 39, 41, 53, 40, 39, 50, 60, 56, 42, 42, 41, 41, 45, 41, 39, 44), 
                   (52, 47, 47, 50, 44, 45, 43, 46, 43, 44, 40, 42, 44, 40, 43, 42, 43, 39, 39, 38, 38, 40, 41, 37, 41, 42, 40, 38, 38, 36, 37, 36, 36, 43)]


#Make it set tuples as size of largest album
def create_rankings_csv(total_rankings):
    f = open("ratings.csv", "w")    
    #Calculate length of largest album
    max_length = 0
    album_number = len(total_rankings)
    for ranking in total_rankings:
        if len(ranking)>max_length:
            max_length = len(ranking)
    #Write Column Line
    for i in range(1, album_number+1):
        f.write(f"Album_{i},")
    f.write("Track_#\n")

    #Write Track Lines
    for i in range(max_length):
        for j in range(album_number):
            length = len(total_rankings[j])
            if i < length:
                f.write(f"{total_rankings[j][i]//2},")
            else:
                f.write("0,")
        f.write(f"Track_{i+1}\n")
    f.close()

if __name__=="__main__":
    print("Running \"create_rankings_csv.py\" is reserved for testing...")
    create_rankings_csv(total_rankings2)
    print("here")