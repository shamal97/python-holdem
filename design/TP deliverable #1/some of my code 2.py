import random
import copy


cards = [
"12",
"13",
"14",
"15",
"16",
"17",
"18",
"19",
"1T",
"1J",
"1Q",
"1K",
"1A",
"22",
"23",
"24",
"25",
"26",
"27",
"28",
"29",
"2T",
"2J",
"2Q",
"2K",
"2A",
"32",
"33",
"34",
"35",
"36",
"37",
"38",
"39",
"3T",
"3J",
"3Q",
"3K",
"3A",
"42",
"43",
"44",
"45",
"46",
"47",
"48",
"49",
"4T",
"4J",
"4Q",
"4K",
"4A",]

def make2dList(rows, cols):
    a=[]
    for row in range(rows): a += [[0]*cols]
    return a

liveDeck = copy.copy(cards)
board = [0]*5
burn = []
numberOfPlayers = 6
hands = make2dList(numberOfPlayers,2)

#0 = nothing
#1 = 1 Pair
#2 = 2 Pair
#3 = 3 of a King
#4 = Straight
#5 = Flush
#6 = Full House
#7 = 4 of a Kind
#8 = Straight Flush
#9 = Royal Flush
playerHas = [0]*numberOfPlayers


#dealing cards
for player in range(len(hands)):
    for card in range(len(hands[0])):
        delt = random.randint(0, len(liveDeck))-1
        hands[player][card] = liveDeck[delt]
        liveDeck.pop(delt)



# dealing board test
for i in range(5):
    delt = random.randint(0, len(liveDeck))-1
    board[i] = liveDeck[delt]
    liveDeck.pop(delt)


# board = ['44', '43', '22', '3A', '35']
#Flushes 
for player in range(len(hands)):
    suits = {}
    for card in hands[player]:
        if int(card[0]) not in suits:
            suits[int(card[0])] = 1
        else:
            suits[int(card[0])] +=1
    for card in board:
        if int(card[0]) not in suits:
            suits[int(card[0])] = 1
        else:
            suits[int(card[0])] +=1
    # print(suits, player)
    for suit in suits:
        if suits[suit] >= 5:
            if playerHas[player] < 5:
                print("flushhhhh", player)
                playerHas[player] = 5


def getPlayersVals(board, hand):
    #creates a set of vals the player has access to
    vals = []
    for card in hands[player]:
        if card[1] == "T":
            vals.append("10")
        elif card[1] == "J":
            vals.append("11")
        elif card[1] == "Q":
            vals.append("12")
        elif card[1] == "K":
            vals.append("13")
        elif card[1] == "A":
            vals.append("1")
            vals.append("14")
        else:
            vals.append(card[1])
    for card in board:
        if card[1] == "T":
            vals.append("10")
        elif card[1] == "J":
            vals.append("11")
        elif card[1] == "Q":
            vals.append("12")
        elif card[1] == "K":
            vals.append("13")
        elif card[1] == "A":
            vals.append("14")
            vals.append("1")
        else:
            vals.append(card[1])
    return vals

# def getPlayersSuits(board, hand):


#Straights
for player in range(len(hands)):
    vals = getPlayersVals(board, player)
    for val in vals:
        hasStraight=True
        for x in range(5):
            if str(int(val)+x) not in vals:
                hasStraight=False
        if hasStraight == True:
            print("straightttt   " + str(player)+ "   " + str(int(val)+4))

#Full House
for player in range(len(hands)):
    vals = getPlayersVals(board, player)
    mostCount = 0
    secondCount = 0
    mostVal = None
    secondVal = None
    for val in vals:
        count = 0
        yeet = None
        for x in vals:
            if val == x:
                # print(int(player), x, val)
                count+=1
                yeet = val
        if mostCount > count > secondCount:
            secondCount = count
            secondVal = yeet
        elif count > mostCount:
            mostCount = count
            mostVal = yeet
        if mostCount == 3 and secondCount == 2:
            print("full house", player)

    print( "Player",player, "has", mostCount, mostVal, "and", secondCount,secondVal)




print(hands)
print(board)
