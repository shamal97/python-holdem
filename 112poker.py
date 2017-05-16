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
        self.numofActivePlayers =0
        for player in self.players:
            if player.playing == True:
                self.numofActivePlayers += 1
        self.turn = startingPlayer
        self.turnIndex = players.index(startingPlayer)
        self.activePlayersIndexes = list(range(self.numofActivePlayers))
        self.betAmount = 0
        self.potSize = 0
        self.calls = 0
        self.foldedPlayers = 0
        self.potIsRight = False
        self.ftr = 0 #1=flop 2=turn 3=river
        self.checkorCall = "Check" #this label changes whether someone has bet
        self.gameOver = False #when only user is left or user has lost
        self.playingPlayers = self.activePlayersIndexes


    def raiseBet(self, amount, moreToCall): #used when a player RAISES the bet
        # self.calls = 1
        self.betAmount += amount
        self.checkorCall = "Call"

    def playerFold(self, player): #used when a player FOLDS
        # self.foldedPlayers += 1
        self.activePlayersIndexes.remove(self.players.index(player))

    def call(self, moreToCall): #used when a player CALLS or CHECKS
        # self.calls +=1
        self.potSize += moreToCall

    def bet(self, betSize):
        self.potSize += betSize

    def newBetting(self): #used after rounds of betting in a hand 
        self.checkorCall = "Check"
        self.betAmount = 0
        self.potIsRight = False
        self.firstToBet = self.onTheButton
        #this solves the complex problem of making sure the first person to
        #bet is the next person in the rotation that is still active in the hand
        if (self.players.index(self.onTheButton) 
            not in self.activePlayersIndexes):
            while (self.players.index(self.firstToBet) 
                not in self.activePlayersIndexes):
                self.firstToBet = self.players[(self.players.index(
                    self.firstToBet) + 1)%len(self.players)]
        self.turn = self.firstToBet
        for player in self.players:
            player.chipsIn = 0
        self.calls = 0

    def newHand(self):
        #called after each hand
        self.activePlayersIndexes = list(range(len(self.players)))
        self.onTheButton = self.players[(self.players.index(self.onTheButton)
            +1)%len(self.players)]
        self.turn = self.onTheButton
        self.betAmount = 0
        self.potSize = 0
        self.calls = 0
        self.foldedPlayers = 0
        self.potIsRight = False
        self.ftr = 0 #1=flop 2=turn 3=river
        for player in self.players:
            #if after a hand, a player has zero chips (meaining they went
            # all in and lost), they remain out of the game.
            player.chipsIn = 0
            if player.chips <= 0:
                self.foldedPlayers += 1
                self.activePlayersIndexes.remove(self.players.index(player))
            if len(self.activePlayersIndexes) == 1:
                self.gameOver == True
        self.playingPlayers = self.activePlayersIndexes
        self.bestType = -1
        self.bestCard = 0
        self.bestPlayer = None

    

    def nextTurn(self, whoFolded): #used after a player makes a decision
        if self.calls == len(self.players)-self.foldedPlayers:
            #everyone who is playing has bet equally and we move on
            self.potIsRight =True
            self.ftr += 1
        x = 0
        skip = 1
        while x == 0:
        #the next turn goes to the next active player in the rotation
            if((self.players.index(self.turn)+skip)%len(self.players) 
                in self.activePlayersIndexes):
                x += 1
                self.turn = self.players[(self.players.index(self.turn)
                    +skip)%len(self.players)]
            else:
                skip += 1
            

    def drawPot(self, canvas, data): #for displaying the value in the pot
        if data.startingGame == False:
            if self.potSize < 0:
                self.potSize = 0
            canvas.create_text(data.width/2,data.height/2+80, text=str(
                self.potSize), font="Marion 30 ")
            canvas.create_text(data.width*3/4, data.height*3/4, text="Bet: "+ 
                str(self.betAmount), font="Marion 20")
            
    def drawWhosTurn(self, canvas, data): #for displaying whos turn it is
        if data.startingGame == False and data.startHand == False and (
            data.board.potIsRight == False):
            canvas.create_oval(self.turn.x-10,self.turn.y-10,self.turn.x+10,
                self.turn.y+10,fill="cyan")

    def drawFlop(self, deck, canvas, data): #draws flop cards when drawn
        for card in range(len(deck.flopCards)):
            try:                
                canvas.create_image(data.width/2-card*(
                    data.cardwidth+data.cardmargin),data.height/2,anchor=CENTER,
                    image=getPlayingCardImage(data, int(
                        deck.flopCards[card][1:]), deck.flopCards[card][:1]))
            except:
                pass #this is for before flop cards are dealt


    def drawTurn(self, deck, canvas, data): #for drawing the next board card
        for card in range(len(deck.turnCard)):
            try:                
                canvas.create_image(data.width/2+(data.cardwidth+data.cardmargin
                    ),data.height/2,anchor=CENTER,
                    image=getPlayingCardImage(data, int(deck.turnCard[card][1:]
                        ), deck.turnCard[card][:1]))
            except:
                pass

    def drawRiver(self, deck, canvas, data): #for drawing the last board card
        for card in range(len(deck.riverCard)):
            try:                
                canvas.create_image(data.width/2+2*(data.cardwidth+
                    data.cardmargin),data.height/2,anchor=CENTER,
                    image=getPlayingCardImage(data, int(
                        deck.riverCard[card][1:]), deck.riverCard[card][:1]))
            except:
                pass

    def checkForWinner(self, deck): 
        #checks if only one player left or who won after last betting
        if len(self.activePlayersIndexes
            ) == 1 and self.gameOver == False and self.ftr != 5:
            return self.players[self.activePlayersIndexes[0]]
        if self.ftr == 4:
            hands = []
            boardCards = deck.flopCards + deck.turnCard + deck.riverCard
            for player in range(len(self.activePlayersIndexes)):
                hands.append({})

            for player in self.activePlayersIndexes:
                #goes through each player and finds all notable combonations
                if self.findHighCard(self.players[player].hand, 
                    boardCards) != None:
                    hands[self.activePlayersIndexes.index(
                        player)][0]=self.findHighCard(
                    self.players[player].hand, boardCards)
                if self.find1Pair(self.players[player].hand, 
                    boardCards) != None:
                    hands[self.activePlayersIndexes.index(
                        player)][1]=self.find1Pair(
                    self.players[player].hand, boardCards)
                if self.find2Pair(self.players[player].hand, 
                    boardCards) != None:
                    hands[self.activePlayersIndexes.index(
                        player)][2]=self.find2Pair(
                    self.players[player].hand, boardCards)
                if self.find3ofaKind(self.players[player].hand, 
                    boardCards) != None:
                    hands[self.activePlayersIndexes.index(
                        player)][3]=self.find3ofaKind(
                    self.players[player].hand, boardCards)
                if self.findStraight(self.players[player].hand, 
                    boardCards) != None:
                    hands[self.activePlayersIndexes.index(
                        player)][4]=self.findStraight(
                    self.players[player].hand, boardCards)
                if self.findFlush(self.players[player].hand, 
                    boardCards) != None:
                    hands[self.activePlayersIndexes.index(
                        player)][5]=self.findFlush(
                    self.players[player].hand, boardCards)
                if self.findFullHouse(self.players[player].hand, 
                    boardCards) != None:
                    hands[self.activePlayersIndexes.index(
                        player)][6]=self.findFullHouse(
                    self.players[player].hand, boardCards)
                if self.find4ofaKind(self.players[player].hand, 
                    boardCards) != None:
                    hands[self.activePlayersIndexes.index(
                        player)][7]=self.find4ofaKind(
                    self.players[player].hand, boardCards)
                if 4 in hands[self.activePlayersIndexes.index(
                    player)] and ( 5 in 
                    hands[self.activePlayersIndexes.index(
                        player)]):
                    hands[self.activePlayersIndexes.index(
                        player)][8]=self.find1Pair(
                    self.players[player].hand, boardCards)
                
            self.bestType = 0
            self.bestCard = 0
            self.bestPlayer = None

            for player in hands:
                #goes through all players combonations and finds best player
                for hand in player:
                    if hand > self.bestType:
                        self.bestType = hand
                        self.bestCard = player[hand]
                        bestPlayer = player
                    elif hand == self.bestType:
                        if player[hand] > self.bestCard:
                            self.bestCard = player[hand]
                            bestPlayer = player

            return self.players[self.activePlayersIndexes[hands.index(
                bestPlayer)]]
        return None


    def findFlushDraw(self, hand, boardCards):
        #this finds 4 cards of the same suit to help AI decide if worthy hand
        suits = self.getCardSuitsDict(hand, boardCards)
        for a in suits:
            if suits[a] >= 4:
                return 1
        return None

    def findStraightDraw(self, hand, boardCards):
        #this finds 4 cards with one missing from a straight to help decision
        cardDict = self.getCardValDict(hand, boardCards)
        straights = []
        misses = 0
        for card in cardDict:
            isStraight = True
            for additional in range(5):
                if card+additional not in cardDict:
                    misses +=1
            if misses <= 1:
                straights.append(card)
        if len(straights) == 0:
            return None
        return max(straights)

    def findHighCard(self, hand, boardCards):
        #finds best card in hand
        return max(self.getCardValDict(hand, boardCards))

    def find1Pair(self, hand, boardCards):#finds best pair
        cardDict = self.getCardValDict( hand, boardCards)
        pairs = []
        for card in cardDict:
            if cardDict[card] == 2:
                pairs.append(card)
        highestPair = -1
        if len(pairs) == 0:
            return None
        else:
            return max(pairs)


    def find2Pair(self, hand, boardCards): #finds best 2 pair
        cardDict = self.getCardValDict(hand, boardCards)
        pairs = []
        for card in cardDict:
            if cardDict[card] == 2:
                pairs.append(card)
        try:
            pairs.remove(1)
        except:
            pass
        if len(pairs) >= 2:
            pairs = max(pairs)
            return pairs
        return None

    def find3ofaKind(self, hand, boardCards): #finds best 3 of a kind
        cardDict = self.getCardValDict(hand, boardCards)
        threes = []
        for card in cardDict:
            if cardDict[card] == 3:
                threes.append(card)
        highestPair = -1
        for card in threes:
            if card > highestPair:
                highestPair = card
        if highestPair == -1:
            return None
        else:
            return highestPair

    def findStraight(self, hand, boardCards): #finds best straight
        cardDict = self.getCardValDict(hand, boardCards)
        straights = []
        for card in cardDict:
            isStraight = True
            for additional in range(5):
                if card+additional not in cardDict:
                    isStraight = False
            if isStraight == True:
                straights.append(card)
        if len(straights) == 0:
            return None
        return max(straights)

    def findFlush(self, hand, boardCards): #finds best flush
        suits = self.getCardSuitsDict(hand, boardCards)
        for a in suits:
            if suits[a] >= 5:
                return 1
        return None

    def findFullHouse(self, hand, boardCards): #finds best full house
        cards = self.getCardValDict(hand, boardCards)
        threeCards = False
        twoCards = False
        val = None
        for card in cards:
            if cards[card] == 3:
                threeCards = True
                val = card
            if cards[card] == 2:
                twoCards = True
        if threeCards == True and twoCards == True:
            return val
        return None

    def find4ofaKind(self, hand, boardCards): #finds best 4 of a kind
        cardDict = self.getCardValDict( hand, boardCards)
        fours = []
        for card in cardDict:
            if cardDict[card] == 4:
                fours.append(card)
        highestFour = -1
        if len(fours) == 0:
            return None
        else:
            return max(fours)

    def getCardValDict(self, hand, boardCards): 
    #creates a dictionary of card vals to number of those card vals in a hand
    #does not include suit
        cards = self.getCardVals( hand, boardCards)
        cardDict = {}
        for card in cards:
            if card not in cardDict:
                cardDict[card] = 1
            else:
                cardDict[card] += 1
        if 1 in cardDict:
            cardDict[14] = cardDict[1]
        return cardDict

    def getCardVals(self, hand, boardCards):
        #creates a set of all the values (not the suits)
        cardVals = []
        for card in hand:
            cardVals.append(int(card[1:]))
        for card in boardCards:
            cardVals.append(int(card[1:]))
        return cardVals

    def getCardSuits(self, hand, boardCards):
        #creates a list of the suits (not vals)
        cardSuits = []
        for card in hand:
            cardSuits.append(card[:1]) 
        for card in boardCards:
            cardSuits.append(card[:1])
        return cardSuits

    def getCardSuitsDict(self, hand, boardCards):
        #creates a dict of suits with quantity of (not vals)
        cards = self.getCardSuits(hand, boardCards)
        cardDict = {}
        suits = "sdch"
        for card in cards:
            if suits.index(card) not in cardDict:
                cardDict[suits.index(card)] = 1
            else:
                cardDict[suits.index(card)] += 1
        return cardDict


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
    #controls the deck of cards for dealing and putting on board
    def __init__(self, allcards):
        self.remainingCards = allcards
        self.flopCards = [None, None, None]
        self.turnCard = [None]
        self.riverCard = [None]

    def deal(self, players): #gives each player their starting cards
        self.remainingCards = copy.copy(cards)
        for player in players:
            if player.chips > 0:
                for card in range(2): #each player gets two cards
                    delt = random.randint(0, len(self.remainingCards))-1
                    player.getCard(self.remainingCards[delt], card)
                    self.remainingCards.pop(delt)
            else:
                player.playing = False

    def flop(self): #when called deals the three flop cards
        for card in range(3):
            delt = random.randint(0, len(self.remainingCards))-1
            self.flopCards[card]=self.remainingCards[delt]
            self.remainingCards.pop(delt)

 
    def turn(self): #when called deals the turn card (4th card on board)
        delt = random.randint(0, len(self.remainingCards))-1
        self.turnCard[0]=self.remainingCards[delt]
        self.remainingCards.pop(delt)

    def river(self): #when called deals the river card (last card on board)
        delt = random.randint(0, len(self.remainingCards))-1
        self.riverCard[0]=self.remainingCards[delt]
        self.remainingCards.pop(delt)



            



class player(object): 
    #this is the class of the person playing the game
    #sub class of this is the computer AI
    def __init__(self,x,y):
        #x and y are the center coordinates for where the players cards will be
        self.x = x
        self.y = y
        self.hand = [None,None]
        self.playing = True
        self.chips = 100
        self.chipsIn = 0




    def newHand(self): #at the beginning of a new hand reseting whats needed
        self.hand = [None,None]
        self.chipsIn = 0
        if self.chips > 0:
            self.playing = True

    def makeDecision(self, choice, board, deck):
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




    def wonHand(self, board): #to add chips after winning
        self.chips += board.potSize



    def getCard(self, card, pos): #to call and receive a certain card
        self.hand[pos] = card

    def getCards(self): #returns hand
        return self.hand

    def call(self, board): #called when a player calls
        board.calls +=1
        moreToCall = board.betAmount-self.chipsIn
        if moreToCall > self.chips:
            moreToCall=self.chips
        board.call(moreToCall)
        self.chips -= moreToCall
        self.chipsIn += moreToCall


    def fold(self, board): #used when a player folds
        board.foldedPlayers +=1 
        board.playerFold(self)
        self.playing = False

    def bet(self, increase, board): #raise (with set raise value)
        board.calls = 1

        moreToCall = board.betAmount-self.chipsIn
        self.chips -= moreToCall
        self.chipsIn += moreToCall
        board.call(moreToCall)
        board.bet(increase)
        board.raiseBet(increase, moreToCall)
        self.chips -= increase
        self.chipsIn += increase


    def drawChips(self, canvas, data): #to display a users chips
        displaychips = self.chips
        if displaychips < 0:
            displaychips = 0
        if data.currentWinner == self and data.board.ftr == 5:
            #if a player won the hand
            canvas.create_text(self.x,self.y-60, text= str(displaychips),
             font="Marion 30", fill="yellow")
        else:
            canvas.create_text(self.x,self.y-60, text= str(displaychips),
             font="Marion 30")




    def drawCards(self, canvas, data):
        if self.playing == True:
            for card in range(len(self.hand)):
                canvas.create_image(self.x+20*card,self.y+20*card,anchor=CENTER,
                    image=getPlayingCardImage(data, int(self.hand[card][1:]),
                     self.hand[card][:1]))
        else:
            #for when cards have not been dealt
            pass


class computerPlayer(player):
    #sub class for the non user player
    def __init__(self,x,y):
        super().__init__(x,y)
        self.showCards = False
        self.chips = 100


    def drawCards(self, canvas, data): #to display cards
        if self.playing == True:
            for card in range(len(self.hand)):
                if self.showCards == False: #showing the card backs
                    canvas.create_image(self.x+20*card,self.y+20*card,
                        anchor=CENTER,
                        image=getPlayingCardImage(data, 1, "x"))
                else: #shows cards when hand is over
                    canvas.create_image(self.x+20*card,self.y+20*card,
                        anchor=CENTER,
                        image=getPlayingCardImage(data, 
                            int(self.hand[card][1:]), self.hand[card][:1]))
        else:
            #for when cards have not been dealt
            pass

    def getDecisionFromWindow(self, board, window): 
    #this is standard method used for decision once window has been decided
        decision = random.randint(0,100)
        choice = 0
        if decision < window/2:
            choice = 2
        if window/2 <= decision <= window:
            choice = 1
        if board.betAmount-self.chipsIn == 0:
            choice = 1
        if self.chips == 0 and choice ==2:
            choice = 1 
        return choice

    def initialHandDecision(self, board):
    #creates the window for the first round of betting
        initialWindow = 50
        for card in self.hand:
            if int(card[1:]) >= 10:
                initialWindow += 5
            if int(card[1:]) == 1:
                initialWindow += 10
        if self.hand[0][1:] == self.hand[1][1:]:
            if int(self.hand[0][1:]) >= 10:
                initialWindow = 90
            elif int(self.hand[0][1:]) <= 5:
                initialWindow = 50
            else:
                initialWindow = 75
        decision = random.randint(0,100)
        choice = 0
        if decision < initialWindow/3:
            choice = 2
        if initialWindow/3 <= decision <= initialWindow:
            choice = 1
        if board.betAmount-self.chipsIn == 0 and choice == 0:
            choice = 1
        return choice

    def notLastDecision(self, board, deck):
        #creates decision for rounds of betting when not all cards are out
        initialWindow = 30
        if board.find1Pair(self.hand, deck.flopCards) != None:
            initialWindow = 70
        if board.find2Pair(self.hand, deck.flopCards) != None:
            initialWindow = 100
        if board.find3ofaKind(self.hand, deck.flopCards) != None:
            initialWindow = 140
        if board.findFlushDraw(self.hand, deck.flopCards) != None:
            initialWindow = 85
        if board.findStraightDraw(self.hand, deck.flopCards) != None:
            initialWindow = 80
        if len(board.activePlayersIndexes) <= 2:
            initialWindow += 15
        return self.getDecisionFromWindow(board, initialWindow)


    def lastDecision(self, board, deck):
        #creates window for last round of betting
        initialWindow = 70
        if board.find1Pair(self.hand, deck.flopCards) != None:
            initialWindow = 95
        if board.find2Pair(self.hand, deck.flopCards) != None:
            initialWindow = 100
        if board.find3ofaKind(self.hand, deck.flopCards) != None:
            initialWindow = 110
        if board.findFlush(self.hand, deck.flopCards) != None:
            initialWindow = 140
        if board.findStraight(self.hand, deck.flopCards) != None:
            initialWindow = 120
        if board.findFullHouse(self.hand, deck.flopCards) != None:
            initialWindow = 150
        return self.getDecisionFromWindow(board,initialWindow)

    def makeDecision(self, board, deck):
        #called when a player has to make a decision
        choice = 1
        whoFolded = None
        if board.ftr == 0:
            choice = self.initialHandDecision(board)
        if board.ftr == 1:
            choice = self.notLastDecision(board, deck)
        if board.ftr == 2:
            choice = self.notLastDecision(board, deck)
        if board.ftr == 3:
            choice = self.lastDecision(board, deck)
        


        if choice == 0: #fold
            whoFolded = board.players.index(self)
            self.fold(board)
            self.playing = False

        if choice == 1: #call/check
            self.call(board)

        if choice == 2: #bet
            self.bet(5, board)

        board.nextTurn(whoFolded)









def drawStatics(canvas, data):
    #create table and static elements
    canvas.create_rectangle(0,0,data.width,data.height,fill=rgbString(51,0,0),
        width=0)
    canvas.create_oval(0,0,data.width,data.height,fill=rgbString(139,69,19), 
        width=0)
    canvas.create_oval(data.tablemargin, data.tablemargin, 
        data.width - data.tablemargin, data.height - data.tablemargin, 
        fill=rgbString(0,100,0), width=0)
    canvas.create_image(data.width/2-3*(data.cardwidth+data.cardmargin), 
        data.height/2,
        anchor=CENTER, image=getPlayingCardImage(data, 1, "x"))
    
def drawButtons(canvas, data):
    #for making all buttons and dynamic screens
    data.labels = ["Fold", data.board.checkorCall, "Raise"]
    if data.board.turn == data.user and data.startingGame == False and (
        data.startHand == False and data.board.potIsRight == False):
        for button in range(3):
            canvas.create_rectangle(data.width-(button+1)*(
                data.buttonwidth+data.buttonmargin),
                data.height-data.buttonheight-data.buttonmargin,
                data.width-button*(data.buttonwidth+data.buttonmargin
                    )-data.buttonmargin,
                data.height-data.buttonmargin,fill="white", 
                activefill=rgbString(204,204,204), activewidth=5)
            canvas.create_text(data.width-(button+1)*(
                data.buttonwidth+data.buttonmargin)+data.buttonwidth/2,
                data.height-data.buttonheight/2-data.buttonmargin,
                anchor=CENTER, text=data.labels[button], font="Marion 20")
    if data.startingGame == False:
        canvas.create_rectangle(
            data.width-data.buttonmargin-data.buttonwidth, data.buttonmargin,
            data.width-(data.buttonmargin),
            data.buttonmargin+data.buttonheight, fill="white", 
            activefill=rgbString(204,204,204), activewidth=5)
        canvas.create_text(data.width-(1)*(
            data.buttonwidth+data.buttonmargin)+data.buttonwidth/2,
        data.buttonmargin+data.buttonheight/2,
            anchor=CENTER,text="Quit",font="Marion 20")
    if data.startingGame == True:
        canvas.create_image(data.width/2,data.height/2,anchor=CENTER,
         image=getPlayingCardImage(data, 3, "x"))
        # background for title screen http://media.salon.com/2013/09/poker_game.jpg
        canvas.create_rectangle(data.width/2-data.buttonwidth-10, 
        data.height*4/5-data.buttonheight/2, data.width/2+data.buttonwidth+10, 
        data.height*4/5+data.buttonheight/2,fill="white",
         activefill=rgbString(204,204,204), activewidth=5 )
        canvas.create_text(data.width/2, data.height*4/5,anchor=CENTER,
            text="Start Game",font= "Marion 30")
        canvas.create_text(data.width/2, data.height/2-60, anchor=CENTER,
         text="In this version of poker, all bets and raises are 5 chips.",
          font ="Marion 30")
        canvas.create_text(data.width/2, data.height/2-20, anchor=CENTER,
         text="It's you versus 5 computer players, and the last one",
          font ="Marion 30")
        canvas.create_text(data.width/2, data.height/2+20, anchor=CENTER,
         text="remaining wins. Let's see if you can beat my code!", font="Marion 30")

        canvas.create_text(data.width/2, data.height*1/5,
         text  = "112 Poker", font ="Marion 80", fill ="black")

    if data.startHand == True and data.userLost == False:

        canvas.create_rectangle(data.width/2-data.buttonwidth/2-20,
         data.height/2-data.buttonheight-70, data.width/2+data.buttonwidth/2+20,
          data.height/2-70,fill="white", activefill=rgbString(204,204,204),
           activewidth=5 )
        canvas.create_text(data.width/2, data.height/2-70-data.buttonheight/2,
         text="Next Hand")

def drawUserLost(canvas, data): #when the user loses the game
    if data.userLost == True:
        canvas.create_rectangle(data.width/2-120, data.height/2-50 -50,
            data.width/2+120, data.height/2+50 -50, fill="white")
        canvas.create_text(data.width/2,data.height/2-50,text="You Lose!",
         font ="Marion 50", fill="black")
        canvas.create_rectangle(data.width/2-data.buttonwidth-10, 
        data.height*4/5-data.buttonheight/2, data.width/2+data.buttonwidth+10, 
        data.height*4/5+data.buttonheight/2,fill="white",
         activefill=rgbString(204,204,204), activewidth=5 )
        canvas.create_text(data.width/2, data.height*4/5,anchor=CENTER,
            text="Start Over",font= "Marion 30")


def drawWinnerHand(canvas, data): #shows the yellow text of the winners hand
    if data.board.ftr == 5:
        if data.board.bestType == -1:
            data.winningType = "Last Player Remaining"
        if data.board.bestType == 0:
            data.winningType = "High Card"
        if data.board.bestType == 1:
            data.winningType = "Pair"
        if data.board.bestType == 2:
            data.winningType = "Two Pair"
        if data.board.bestType == 3:
            data.winningType = "Three of a Kind"
        if data.board.bestType == 4:
            data.winningType = "Straight"
        if data.board.bestType == 5:
            data.winningType = "Flush"
        if data.board.bestType == 6:
            data.winningType = "Full House"
        if data.board.bestType == 7:
            data.winningType = "Four of a Kind"
        if data.board.bestType == 8:
            data.winningType = "Straight Flush"
        canvas.create_text(data.width*1/4, data.height*3/4,
         text=data.winningType, font="Marion 20", fill="yellow")


def drawPlayerWon(canvas, data): #if the user wins the entire game
    if data.board.gameOver == True:
        canvas.create_rectangle(data.width/2-120, data.height/2-50 -50,
            data.width/2+120, data.height/2+50 -50, fill="white")
        canvas.create_text(data.width/2,data.height/2-50,text="You Win!!!",
         font ="Marion 50", fill="black")
        canvas.create_rectangle(data.width/2-data.buttonwidth-10, 
        data.height*4/5-data.buttonheight/2, data.width/2+data.buttonwidth+10, 
        data.height*4/5+data.buttonheight/2,fill="white",
         activefill=rgbString(204,204,204), activewidth=5 )
        canvas.create_text(data.width/2, data.height*4/5,anchor=CENTER,
            text="Start Over",font= "Marion 30")





def rgbString(red, green, blue): #from the course page
    return "#%02x%02x%02x" % (red, green, blue)


def init(data):
    loadPlayingCardImages(data)
    data.user = player(data.width/2,data.height-80)
    data.players = [data.user] + [0]*5
    data.opponentPositions = [(50, data.height/2), (data.width/4, 
        data.height/5), (
        data.width/2, 80),(data.width*3/4,data.height/5), (data.width-70,
         data.height/2)]
    for opponents in range(5):
        data.players[opponents+1] = (
            computerPlayer(data.opponentPositions[opponents][0],
            data.opponentPositions[opponents][1]))
    data.step = 0
    data.tablemargin = 20
    data.cardmargin = 5
    data.buttonwidth = 80
    data.buttonheight = 50
    data.buttonmargin = 10
    data.cardheight = getPlayingCardImage(data, 2, "Clubs").height()
    data.cardwidth  = getPlayingCardImage(data, 2, "Clubs").width()
    data.handsDealt = False
    data.liveDeck = deck(copy.deepcopy(cards)) #the object I use as my deck
    data.board = board(data.players[0],data.players) 
    data.labels = ["Fold", data.board.checkorCall, "Raise"]
    #check or call is check when no one has bet, and call when someone has bet
    data.startNewHand = False
    data.startingGame = True
    data.startHand = False
    data.userLost = False
    data.winningType = "High Card"
    data.currentWinner = None


def loadPlayingCardImages(data): #from example from notes
    cards = 55 # cards 1-52, back, joker1, joker2
    data.cardImages = [ ]
    for card in range(cards):
        rank = (card%13)+1
        suit = "cdhsx"[card//13]
        filename = "playing-card-gifs/%s%d.gif" % (suit, rank)
        data.cardImages.append(PhotoImage(file=filename))

def getPlayingCardImage(data, rank, suitName): #from example from notes
    suitName = suitName[0].lower() # only care about first letter
    suitNames = "cdhsx"
    assert(1 <= rank <= 13)
    assert(suitName in suitNames)
    suit = suitNames.index(suitName)
    return data.cardImages[13*suit + rank - 1]



def mousePressed(event, data):
    if data.startingGame == False:
        if data.width-data.buttonwidth-data.buttonmargin < event.x < (
            data.width-data.buttonmargin) and data.buttonmargin < event.y < (
            data.buttonmargin+data.buttonheight):
            init(data)
    if data.board.turn == data.user and data.startingGame == False:
        if data.width - (data.buttonwidth+data.buttonmargin) < event.x < (
            data.width - data.buttonmargin) and (
            data.height -data.buttonheight- data.buttonmargin < event.y < 
            data.height - data.buttonmargin):
            data.user.makeDecision("fold", data.board, data.liveDeck)
        if data.width - 2*(data.buttonwidth+data.buttonmargin) < event.x < (
            data.width)-(data.buttonwidth+
            data.buttonmargin)-data.buttonmargin and (
            data.height -data.buttonheight- data.buttonmargin < event.y < 
            data.height - data.buttonmargin):
            data.user.makeDecision("call", data.board, data.liveDeck)
        if data.width - 3*(data.buttonwidth+data.buttonmargin) < event.x < (
        data.width) - 2*(data.buttonwidth+data.buttonmargin
            )- data.buttonmargin and (
            data.height -data.buttonheight- data.buttonmargin < event.y < 
            data.height - data.buttonmargin):
            data.user.makeDecision("bet", data.board, data.liveDeck)
    if data.startingGame == True:
        if data.width/2 -data.buttonwidth-10 < event.x < (
            data.width/2+data.buttonwidth+10) and (
            data.height*4/5-data.buttonheight/2 < event.y < (
                data.height*4/5+data.buttonheight/2) ):
                data.startingGame = False
                for player in data.players:
                    player.showCards = False 
                    player.playing = True
                data.board.newHand()
                # data.board.__init__(data.players[0],data.players)
                data.liveDeck.__init__(copy.copy(cards))
                data.liveDeck.deal(data.players)
                data.handsDealt = True
    if data.userLost == True:
        if data.width/2 -data.buttonwidth-10 < event.x < (
            data.width/2+data.buttonwidth+10) and (
            data.height*4/5-data.buttonheight/2 < event.y < (
                data.height*4/5+data.buttonheight/2) ):
            init(data)
    if data.board.gameOver == True:
        if data.width/2 -data.buttonwidth-10 < event.x < (
            data.width/2+data.buttonwidth+10) and (
            data.height*4/5-data.buttonheight/2 < event.y < (
                data.height*4/5+data.buttonheight/2) ):
            init(data)
    if data.startHand == True:
        if data.width/2 -data.buttonwidth/2-20 < event.x < (
            data.width/2+data.buttonwidth/2+20) and (
            data.height/2-data.buttonheight -70 < event.y < data.height/2-70):
                data.startingGame = False
                for player in data.players:
                    player.showCards = False

                    player.playing = True
                data.board.newHand()
                data.liveDeck.__init__(copy.copy(cards))
                data.liveDeck.deal(data.players)
                data.handsDealt = True
                data.startHand = False

    # if data.startHand == True:
    #     if 




def keyPressed(event, data):
    pass

def timerFired(data):
    if data.board.potIsRight == True and data.board.ftr == 1:
        data.liveDeck.flop()
        data.board.newBetting()
    if data.board.potIsRight == True and data.board.ftr == 2:
        data.liveDeck.turn()
        data.board.newBetting()
    if data.board.potIsRight == True and data.board.ftr == 3:
        data.liveDeck.river()
        data.board.newBetting()
    if data.board.ftr == 5: 
        for player in data.players:
            try:
                if player.playing == True:
                    player.showCards = True
                # player.playing = True

            except:
                pass
        data.startHand = True
    if data.board.ftr == 5 and data.user.chips <= 0:
        data.userLost = True
    
    elif data.board.checkForWinner(data.liveDeck) != None:
        data.currentWinner = data.board.checkForWinner(data.liveDeck)
        data.board.checkForWinner(data.liveDeck).wonHand(data.board)
        data.board.ftr = 5
        # data.liveDeck.__init__(copy.deepcopy(cards))
        # data.board.newHand()
        #hand over DECIDE WINNER
    if len(data.board.playingPlayers) == 1 and data.board.ftr == 5:
        gameogre = True
        for player in data.board.players:
            if player != data.user:
                if player.chips != 0:
                    gameogre = False

        data.board.gameOver = gameogre

    if data.board.turn != data.user and data.board.potIsRight==False:
        data.board.turn.makeDecision(data.board, data.liveDeck)
    



def redrawAll(canvas, data):
    drawStatics(canvas, data)
    drawButtons(canvas, data)
    if data.handsDealt == True:
        for player in data.players:
            player.drawCards(canvas, data)
            player.drawChips(canvas, data) 

    data.board.drawPot(canvas, data)
    data.board.drawWhosTurn(canvas, data)
    data.board.drawFlop(data.liveDeck, canvas, data)
    data.board.drawRiver(data.liveDeck, canvas, data)
    data.board.drawTurn(data.liveDeck, canvas, data)
    drawUserLost(canvas, data)
    drawPlayerWon(canvas, data)
    drawWinnerHand(canvas, data)


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
    data.timerDelay = 500 # milliseconds
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

run()