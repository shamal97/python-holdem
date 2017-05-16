from tkinter import *
import random
import copy

cards = [
"c1","c2","c3","c4","c5","c6","c7","c8","c9","c10","c11","c12","c13",
"d1","d2","d3","d4","d5","d6","d7","d8","d9","d10","d11","d12","d13",
"h1","h2","h3","h4","h5","h6","h7","h8","h9","h10","h11","h12","h13",
"s1","s2","s3","s4","s5","s6","s7","s8","s9","s10","s11","s12","s13"]


class deck(object):
    def __init__(self, allcards):
        self.remainingCards = allcards

    def deal(self, players):
        self.remainingCards = cards
        for player in players:
            for card in range(2): #each player gets two cards
                delt = random.randint(0, len(self.remainingCards))-1
                player.getCard(self.remainingCards[delt], card)
                self.remainingCards.pop(delt)
                print(len(self.remainingCards))

class player(object):
    #this is the class of the person playing the game
    def __init__(self,x,y):
        #x and y are the center coordinates for where the players cards will be
        self.x = x
        self.y = y
        self.hand = [None,None]
        self.playing = True

    def getCard(self, card, pos):
        self.hand[pos] = card

    def getCards(self):
        return self.hand

    def fold(self):
        self.playing = False



    def drawCards(self, canvas, data):
        if self.playing == True:
            for card in range(len(self.hand)):
                # print(self.hand[card])
                canvas.create_image(self.x+20*card,self.y+20*card,anchor=CENTER,
                    image=getPlayingCardImage(data, int(self.hand[card][1:]), self.hand[card][:1]))

class computerPlayer(player):
    def __init__(self,x,y):
        super().__init__(x,y)
    def drawCards(self, canvas, data):
        if self.playing == True:
            for card in range(len(self.hand)):
                # print(self.hand[card])
                canvas.create_image(self.x+20*card,self.y+20*card,anchor=CENTER,
                    image=getPlayingCardImage(data, 1, "x"))





def drawStatics(canvas, data):
    #create table and static elements
    canvas.create_rectangle(0,0,data.width,data.height,fill=rgbString(51,0,0),width=0)
    canvas.create_oval(0,0,data.width,data.height,fill=rgbString(139,69,19), width=0)
    canvas.create_oval(data.tablemargin, data.tablemargin, 
        data.width - data.tablemargin, data.height - data.tablemargin, fill=rgbString(0,100,0), width=0)
    canvas.create_image(data.width/2-2*(data.cardwidth+data.cardmargin), data.height/2,
        anchor=CENTER, image=getPlayingCardImage(data, 1, "x"))
    print(getPlayingCardImage(data, 1, "x"))
    for button in range(3):
        canvas.create_rectangle(data.width-(button+1)*(data.buttonwidth+data.buttonmargin),
            data.height-data.buttonheight-data.buttonmargin,
            data.width-button*(data.buttonwidth+data.buttonmargin)-data.buttonmargin,
            data.height-data.buttonmargin,fill="white")
        canvas.create_text(data.width-(button+1)*(data.buttonwidth+data.buttonmargin)+data.buttonwidth/2,
            data.height-data.buttonheight/2-data.buttonmargin,anchor=CENTER, text=data.labels[button])






def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)


def init(data):
    loadPlayingCardImages(data)
    data.user = player(data.width/2,data.height-80)
    data.players = [data.user] + [0]*5
    data.opponentPositions = [(50, data.height/2), (data.width/4, data.height/5), (
        data.width/2, 80),(data.width*3/4,data.height/5), (data.width-70, data.height/2)]
    for opponents in range(5):
        data.players[opponents+1] = player(data.opponentPositions[opponents][0],
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
    data.liveDeck = deck(cards)

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
    if event.keysym == "space":
        data.liveDeck.deal(data.players)
        data.handsDealt = True
    elif event.keysym == "0":
        print("ok")
        data.players[2].fold()

def timerFired(data):
    pass

def redrawAll(canvas, data):
    drawStatics(canvas, data)
    if data.handsDealt == True:
        for player in data.players:
            player.drawCards(canvas, data)  
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
    data.timerDelay = 999999 # milliseconds
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