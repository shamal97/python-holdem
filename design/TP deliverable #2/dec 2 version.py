from tkinter import *
import random
import copy

cards = [
"c1","c2","c3","c4","c5","c6","c7","c8","c9","c10","c11","c12","c13",
"d1","d2","d3","d4","d5","d6","d7","d8","d9","d10","d11","d12","d13",
"h1","h2","h3","h4","h5","h6","h7","h8","h9","h10","h11","h12","h13",
"s1","s2","s3","s4","s5","s6","s7","s8","s9","s10","s11","s12","s13"]


class board(object): #this controls the flow of betting
    def __init__(self, startingPlayer, players):
        self.onTheButton = startingPlayer
        self.players = players
        self.turn = startingPlayer
        self.turnIndex = players.index(startingPlayer)
        self.activePlayersIndexes = list(range(len(players)))
        self.betAmount = 5
        self.potSize = 0
        self.calls = 0
        self.foldedPlayers = 0
        self.potIsRight = False
        self.ftr = 0 #1=flop 2=turn 3=river

    def raiseBet(self, amount): #used when a player RAISES the bet
        # self.calls = 1
        self.betAmount += amount

    def playerFold(self, player): #used when a player FOLDS
        # self.foldedPlayers += 1
        self.activePlayersIndexes.remove(self.players.index(player))

    def call(self): #used when a player CALLS or CHECKS
        # self.calls +=1
        self.potSize += self.betAmount

    def bet(self, betSize):
        self.potSize += betSize

    def newBetting(self): #used after the flop/river/turn 
        self.betAmount = 0
        self.potIsRight = False
        self.firstToBet = self.onTheButton
        if self.players.index(self.onTheButton) not in self.activePlayersIndexes:
            while self.players.index(self.firstToBet) not in self.activePlayersIndexes:
                self.firstToBet = self.players[(self.players.index(self.firstToBet) + 1)%len(self.players)]
        self.turn = self.firstToBet
        for player in self.players:
            player.chipsIn = 0
        self.calls = 0

    def newHand(self):
        self.activePlayersIndexes = list(range(len(self.players)))
        print(self.activePlayersIndexes)
        self.onTheButton = self.players[(self.players.index(self.onTheButton)+1)%len(self.players)]
        self.turn = self.onTheButton
        self.betAmount = 5
        self.potSize = 0
        self.calls = 0
        self.foldedPlayers = 0
        self.potIsRight = False
        self.ftr = 0 #1=flop 2=turn 3=river

    

    def nextTurn(self, whoFolded): #used after a player makes a decision
        print(self.turn)
        if self.calls == len(self.players)-self.foldedPlayers:
            self.potIsRight =True
            self.ftr += 1
        
        # if whoFolded != None:
        #     x = 0
        #     while(((self.players.index(self.turn+1))%len(self.players) not in self.activePlayersIndexes) and x == 0):
        #         self.turn = self.players[(self.players.index(self.turn))%len(self.players)]
        #         x += 1
        # else:
        x = 0
        skip = 1
        print(self.turn)
        print(self.players.index(self.turn))
        # while(((self.players.index(self.turn)+1)%len(self.players) not in self.activePlayersIndexes) and x != 1):
        while x == 0:
            if((self.players.index(self.turn)+skip)%len(self.players) in self.activePlayersIndexes):
                print(self.players.index(self.turn))
                print(self.turn)
                x += 1
                self.turn = self.players[(self.players.index(self.turn)+skip)%len(self.players)]
            else:
                skip += 1
            
            # self.turn = self.players[self.activePlayersIndexes[(self.activePlayers.index(self.turn)+1)%len(self.activePlayers)]]


    def drawPot(self, canvas, data): #for displaying the value in the pot
        canvas.create_text(data.width/2,data.height/2+80, text=str(self.potSize), font="Times 30 bold")

    def drawWhosTurn(self, canvas, data): #for displaying whos turn it is
        canvas.create_oval(self.turn.x-10,self.turn.y-10,self.turn.x+10,self.turn.y+10,fill="cyan")

    def drawFlop(self, deck, canvas, data):
        for card in range(len(deck.flopCards)):
            try:                
                canvas.create_image(data.width/2-card*(data.cardwidth+data.cardmargin),data.height/2,anchor=CENTER,
                    image=getPlayingCardImage(data, int(deck.flopCards[card][1:]), deck.flopCards[card][:1]))
            except:
                pass
            # self.potIsRight = False

    def drawTurn(self, deck, canvas, data):
        for card in range(len(deck.turnCard)):
            try:                
                canvas.create_image(data.width/2+(data.cardwidth+data.cardmargin),data.height/2,anchor=CENTER,
                    image=getPlayingCardImage(data, int(deck.turnCard[card][1:]), deck.turnCard[card][:1]))
            except:
                pass

    def drawRiver(self, deck, canvas, data):
        for card in range(len(deck.riverCard)):
            try:                
                canvas.create_image(data.width/2+2*(data.cardwidth+data.cardmargin),data.height/2,anchor=CENTER,
                    image=getPlayingCardImage(data, int(deck.riverCard[card][1:]), deck.riverCard[card][:1]))
            except:
                pass

    def checkForWinner(self, deck):
        if len(self.activePlayersIndexes) == 1:
            print("foundwinner")
            return self.players[self.activePlayersIndexes[0]]
        if self.ftr == 4:
            hands = []
            boardCards = deck.flopCards + deck.turnCard + deck.riverCard
            for player in range(len(self.activePlayersIndexes)):
                hands.append({})
            print(self.activePlayersIndexes)

            for player in self.activePlayersIndexes:
                print(player)
                if self.findHighCard(self.players[player].hand, boardCards) != None:
                    hands[self.activePlayersIndexes.index(player)][0]=self.findHighCard(
                    self.players[player].hand, boardCards)
                # if find1Pair(player.hand, boardCards) != None:
                #     hands[self.activePlayers.index(player)][1]=find1Pair(
                #     player.hand, boardCards)
                # if find2Pair(player.hand, boardCards) != None:
                #     hands[self.activePlayers.index(player)][2]=find2Pair(
                #     player.hand, boardCards)
                # if find3ofaKind(player.hand, boardCards) != None:
                #     hands[self.activePlayers.index(player)][3]=find3ofaKind(
                #     player.hand, boardCards)
                # if findStraight(player.hand, boardCards) != None:
                #     hands[self.activePlayers.index(player)][4]=findStraight(
                #     player.hand, boardCards)
                # if findFlush(player.hand, boardCards) != None:
                #     hands[self.activePlayers.index(player)][5]=findFlush(
                #     player.hand, boardCards)
                # if findFullHouse(player.hand, boardCards) != None:
                #     hands[self.activePlayers.index(player)][6]=findFullHouse(
                #     player.hand, boardCards)
                # if find4ofaKind(player.hand, boardCards) != None:
                #     hands[self.activePlayers.index(player)][7]=find4ofaKind(
                #     player.hand, boardCards)
                # if findStraightFlush(player.hand, boardCards) != None:
                #     hands[self.activePlayers.index(player)][8]=findStraightFlush(
                #     player.hand, boardCards)

            bestType = 0
            bestCard = 0
            bestPlayer = None

            for player in hands:
                for hand in player:
                    if hand > bestType:
                        bestType = hand
                        bestPlayer = player
                    elif hand == bestType:
                        if player[hand] > bestCard:
                            bestCard = player[hand]
                            bestPlayer = player

            return self.players[self.activePlayersIndexes[hands.index(bestPlayer)]]
        return None

    def findHighCard(self, hand, boardCards):
        return max(self.getCardVals(hand, boardCards))


    def getCardVals(self, hand, boardCards):
        cardVals = []
        for card in hand:
            cardVals.append(int(card[1:]))
        for card in boardCards:
            cardVals.append(int(card[1:]))
        return cardVals


#0 = nothing
#1 = 1 Pair
#2 = 2 Pair
#3 = 3 of a King
#4 = Straight
#5 = Flush
#6 = Full House
#7 = 4 of a Kind
#8 = Straight Flush


class deck(object):
    def __init__(self, allcards):
        self.remainingCards = allcards
        self.flopCards = [None, None, None]
        self.turnCard = [None]
        self.riverCard = [None]

    def deal(self, players): #gives each player their starting cards
        self.remainingCards = copy.copy(cards)
        for player in players:
            for card in range(2): #each player gets two cards
                delt = random.randint(0, len(self.remainingCards))-1
                player.getCard(self.remainingCards[delt], card)
                self.remainingCards.pop(delt)

    def flop(self):
        for card in range(3):
            delt = random.randint(0, len(self.remainingCards))-1
            self.flopCards[card]=self.remainingCards[delt]
            self.remainingCards.pop(delt)

    def river(self):
        delt = random.randint(0, len(self.remainingCards))-1
        self.riverCard[0]=self.remainingCards[delt]
        self.remainingCards.pop(delt)

    def turn(self):
        delt = random.randint(0, len(self.remainingCards))-1
        self.turnCard[0]=self.remainingCards[delt]
        self.remainingCards.pop(delt)



            



class player(object): 
    #this is the class of the person playing the game, sub class of this is the computer AI
    def __init__(self,x,y):
        #x and y are the center coordinates for where the players cards will be
        self.x = x
        self.y = y
        self.hand = [None,None]
        self.playing = True
        self.chips = 100
        self.chipsIn = 0


    def newHand(self):
        self.hand = [None,None]
        self.playing = True
        self.chipsIn = 0

    def makeDecision(self, choice, board):
        whoFolded = None

        if choice == "fold": #fold
            whoFolded = self
            self.fold(board)
            self.playing = False

        if choice == "call": #call/check
            self.call(board)

        if choice == "bet": #bet
            self.bet(5, board)

        board.nextTurn(whoFolded)


    def wonHand(self, board):
        self.chips += board.potSize



    def getCard(self, card, pos):
        self.hand[pos] = card

    def getCards(self):
        return self.hand

    def call(self, board):
        board.calls +=1
        board.call()
        moreToCall = board.betAmount-self.chipsIn
        self.chips -= moreToCall
        self.chipsIn += moreToCall


    def fold(self, board):
        board.foldedPlayers +=1 
        board.playerFold(self)
        self.playing = False

    def bet(self, increase, board): #raise (with set raise value)
        board.calls = 1

        moreToCall = board.betAmount-self.chipsIn
        self.chips -= moreToCall
        self.chipsIn += moreToCall
        board.call()
        board.bet(increase)
        board.raiseBet(increase)
        self.chips -= increase
        self.chipsIn += increase


    def drawChips(self, canvas, data):
        canvas.create_text(self.x,self.y-60, text=str(self.chips), font="Times 30 bold")




    def drawCards(self, canvas, data):
        if self.playing == True:
            for card in range(len(self.hand)):
                canvas.create_image(self.x+20*card,self.y+20*card,anchor=CENTER,
                    image=getPlayingCardImage(data, int(self.hand[card][1:]), self.hand[card][:1]))
        else:
            canvas.create_oval(self.x-30,self.y-30,self.x+30,self.y+30,fill="black")

class computerPlayer(player):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.showCards = False


    def drawCards(self, canvas, data):
        if self.playing == True:
            for card in range(len(self.hand)):
                if self.showCards == False:
                    canvas.create_image(self.x+20*card,self.y+20*card,anchor=CENTER,
                        image=getPlayingCardImage(data, 1, "x"))
                else:
                    canvas.create_image(self.x+20*card,self.y+20*card,anchor=CENTER,
                        image=getPlayingCardImage(data, int(self.hand[card][1:]), self.hand[card][:1]))
        else:
            canvas.create_oval(self.x-30,self.y-30,self.x+30,self.y+30,fill="black")

    def makeDecision(self, board):
        # choice  = random.randint(0,2)
        choice = 1
        whoFolded = None


        if choice == 0: #fold
            whoFolded = board.players.index(self)
            self.fold(board)
            self.playing = False
            print(self.playing)

        if choice == 1: #call/check
            self.call(board)

        if choice == 2: #bet
            self.bet(5, board)

        board.nextTurn(whoFolded)









def drawStatics(canvas, data):
    #create table and static elements
    canvas.create_rectangle(0,0,data.width,data.height,fill=rgbString(51,0,0),width=0)
    canvas.create_oval(0,0,data.width,data.height,fill=rgbString(139,69,19), width=0)
    canvas.create_oval(data.tablemargin, data.tablemargin, 
        data.width - data.tablemargin, data.height - data.tablemargin, fill=rgbString(0,100,0), width=0)
    canvas.create_image(data.width/2-3*(data.cardwidth+data.cardmargin), data.height/2,
        anchor=CENTER, image=getPlayingCardImage(data, 1, "x"))
    
def drawButtons(canvas, data):
    if data.board.turn == data.user:
        for button in range(3):
            canvas.create_rectangle(data.width-(button+1)*(data.buttonwidth+data.buttonmargin),
                data.height-data.buttonheight-data.buttonmargin,
                data.width-button*(data.buttonwidth+data.buttonmargin)-data.buttonmargin,
                data.height-data.buttonmargin,fill="white")
            canvas.create_text(data.width-(button+1)*(data.buttonwidth+data.buttonmargin)+data.buttonwidth/2,
                data.height-data.buttonheight/2-data.buttonmargin,anchor=CENTER, text=data.labels[button])
    else:
        pass





def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)


def init(data):
    loadPlayingCardImages(data)
    data.user = player(data.width/2,data.height-80)
    data.players = [data.user] + [0]*5
    data.opponentPositions = [(50, data.height/2), (data.width/4, data.height/5), (
        data.width/2, 80),(data.width*3/4,data.height/5), (data.width-70, data.height/2)]
    for opponents in range(5):
        data.players[opponents+1] = computerPlayer(data.opponentPositions[opponents][0],
            data.opponentPositions[opponents][1])
    data.step = 0
    data.tablemargin = 20
    data.cardmargin = 5
    data.buttonwidth = 80
    data.buttonheight = 50
    data.buttonmargin = 10
    data.labels = ["Fold", "Check", "Raise"]
    data.cardheight = getPlayingCardImage(data, 2, "Clubs").height()
    data.cardwidth  = getPlayingCardImage(data, 2, "Clubs").width()
    data.handsDealt = False
    data.liveDeck = deck(copy.deepcopy(cards))
    data.board = board(data.players[0],data.players)
    data.startNewHand = False

def loadPlayingCardImages(data): #from example from notes
    cards = 55 # cards 1-52, back, joker1, joker2
    data.cardImages = [ ]
    for card in range(cards):
        rank = (card%13)+1
        suit = "cdhsx"[card//13]
        filename = "playing-card-gifs/%s%d.gif" % (suit, rank)
        data.cardImages.append(PhotoImage(file=filename))

def getPlayingCardImage(data, rank, suitName): #from example from notes
    suitName = suitName[0].lower() # only car about first letter
    suitNames = "cdhsx"
    assert(1 <= rank <= 13)
    assert(suitName in suitNames)
    suit = suitNames.index(suitName)
    return data.cardImages[13*suit + rank - 1]



def mousePressed(event, data):
    pass

def keyPressed(event, data):
    # print(event.keysym)
    if event.keysym == "space":
        for player in data.players:
            player.showCards = False

            player.playing = True
        data.board.newHand()
        # data.board.__init__(data.players[0],data.players)
        data.liveDeck.__init__(copy.copy(cards))
        data.liveDeck.deal(data.players)
        data.handsDealt = True
    elif event.keysym == "0":
        # print("ok")
        data.user.makeDecision("call", data.board)

    elif event.keysym == "1":
        print(data.board.ftr)

    # elif event.keysym == "minus":

        # data.players[2].bet(5, data.board)
    # elif event.keysym == "Return":
    #     init(data)
    elif event.keysym == "minus":
        data.liveDeck.flop()

    # if event.keysym == "5":
        
    #     data.board.newHand()
    #     # data.board.__init__(data.players[0],data.players)
    #     data.liveDeck.__init__(copy.copy(cards))
    #     data.liveDeck.deal(data.players)
    #     data.handsDealt = True
    #     for player in data.players:
    #         try:
    #             player.newHand()
    #         except:
    #             pass

def timerFired(data):
    if data.board.potIsRight == True and data.board.ftr == 1:
        data.liveDeck.flop()
        data.board.newBetting()
        # print(data.board.activePlayers)
    if data.board.potIsRight == True and data.board.ftr == 2:
        data.liveDeck.turn()
        data.board.newBetting()
    if data.board.potIsRight == True and data.board.ftr == 3:
        data.liveDeck.river()
        data.board.newBetting()
    if data.board.ftr == 5: 
        for player in data.players:
            try:
                player.showCards = True
                player.playing = True

            except:
                pass    
    elif data.board.checkForWinner(data.liveDeck) != None:
        
        print("WINNER", data.board.checkForWinner(data.liveDeck), data.board.ftr)
        data.board.checkForWinner(data.liveDeck).wonHand(data.board)
        data.board.ftr = 5
        # data.liveDeck.__init__(copy.deepcopy(cards))
        # data.board.newHand()
        #hand over DECIDE WINNER
    if data.board.turn != data.user and data.board.potIsRight==False:
        data.board.turn.makeDecision(data.board)
    
    # print(data.board.activePlayers)



def redrawAll(canvas, data):
    drawStatics(canvas, data)
    drawButtons(canvas, data)
    if data.handsDealt == True:
        for player in data.players:
            # print(data.players)
            player.drawCards(canvas, data)
            player.drawChips(canvas, data) 

    data.board.drawPot(canvas, data)
    data.board.drawWhosTurn(canvas, data)
    data.board.drawFlop(data.liveDeck, canvas, data)
    data.board.drawRiver(data.liveDeck, canvas, data)
    data.board.drawTurn(data.liveDeck, canvas, data)

        # print("oya", data.user.getCards())


####################################
# use the run function as-is
####################################

def run(width=800, height=600):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Create root before calling init (so we can create images in init)
    root = Tk()
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 300 # milliseconds
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run()