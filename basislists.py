#%%
import itertools
from collections import Counter
#recursive methods that will generate all combinations of putting n cards into c categories
#returns multiple lists combinations length n, where the kth elment in a combination maps to which category the kth card is put into
#chatgpt made this dont ask me to explain it

def generate_combinations(cards, categories, current_combination=[], all_combinations=[]):
    if len(current_combination) == cards:
        all_combinations.append(current_combination.copy())
        return
    
    for category in range(1, categories + 1):
        current_combination.append(category)
        generate_combinations(cards, categories, current_combination, all_combinations)
        current_combination.pop()

def get_all_combinations(cards, categories):
    all_combinations = []
    generate_combinations(cards, categories, [], all_combinations)
    return all_combinations    

def generate(cards: list, decksizes: list):
    blueCards = ["sk", "r", "sc"]
    redCards = ["b", "f", "ft"]
    greenCards = ["o", "a", "m"]
    yellowCards = ["c", "sp", "cl"]
    blueCount = len(list(filter(lambda x: x in blueCards, cards)))
    redCount = len(list(filter(lambda x: x in redCards, cards)))
    greenCount = len(list(filter(lambda x: x in greenCards, cards)))
    yellowCount = len(list(filter(lambda x: x in yellowCards, cards)))
    count = [blueCount, redCount, greenCount, yellowCount]
    #a prelist is the top n cards of a command line disregarding order
    #this generates all possible prelists
    prelists = list()
    for i in decksizes:
        prelists += list(itertools.combinations(cards,i))

    #prelists = list(itertools.combinations(cards,6))#this number countrols the number of cards filled in the commandline
    #basislists are the same as prelists but also account for levels of cards
    basislists = []

    for prelist in prelists:
        #card counts of the prelist
        locblueCount = prelist.count("sk") + prelist.count("r") + prelist.count("sc")
        locredCount = prelist.count("b") + prelist.count("f") + prelist.count("ft")
        locgreenCount = prelist.count("o") + prelist.count("a") + prelist.count("m")
        locyellowCount = prelist.count("c") + prelist.count("sp") + prelist.count("cl")
        locCards = [list(filter(lambda x: x in blueCards, prelist)),list(filter(lambda x: x in redCards, prelist)),list(filter(lambda x: x in greenCards, prelist)),list(filter(lambda x: x in yellowCards, prelist))]
        locCount = [locblueCount, locredCount, locgreenCount, locyellowCount]
        partialcmd =[]
        i = 0
        #want to divide the prelist into colors, and then create all possible partial monocolor command lines and combine them at the end to generate all possible basislists
        for color in locCount:
            templist = []
            if color == 0:
                i+=1
                continue
            numberCards = count[i]-locCount[i]
            #if no left over cards for a color
            if numberCards == 0:
                if not partialcmd:
                    partialcmd.append(locCards[i])  
                else:
                    for k in range(len(partialcmd)):
                        partialcmd[k]= partialcmd[k]+locCards[i]
                i+=1
                continue
            #+1 accounts for empty bucket
            categories = color + 1
            combinations = get_all_combinations(numberCards, categories)
            #Stores all the possible partial basislists into templist for a single color
            for combination in combinations:  
                tempLocCards = locCards[i].copy()
                for j in range(len(tempLocCards)):
                    x = combination.count(j+1)
                    if x > 2:
                        x = 2
                    if x != 0:
                        tempLocCards[j] = tempLocCards[j] + str(x+1)
                if all(Counter(tempLocCards)!=Counter(temp) for temp in templist):
                    templist.append(tempLocCards)
            if len(partialcmd)==0:
                partialcmd = templist
            else:
                newpartialcmd = []
                #adds all current partial basislists to all past partial basislists combining the partial basislists of different colors
                for partial in partialcmd:
                    for temp in templist:
                        newpartialcmd.append(partial + temp)
                        partialcmd = newpartialcmd    
            i+=1
        #checks repeats before adding to basislists 
        if basislists:
            for partial in partialcmd:
                if partial not in basislists:
                    basislists.append(partial)
        else:
            basislists = partialcmd
    return basislists
if __name__ == "__main__":
    decksizes = range(7)
    #cards = ["b", "c", "f", "o", "o", "sk", "sp"]#puzzle 2
    cards = ["b", "cl", "cl", "c", "c","c", "f", "ft", "o", "sp"]#puzzle 9
    for basis in generate(cards, decksizes):
        print(basis)
        

# %%
