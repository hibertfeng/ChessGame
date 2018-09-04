
################### MAIN #####################
# Import object classes
from chessgui3.board import *
from chessgui3.engine import *
import pygame, sys
from pygame.locals import *



b=Board()
e=Engine()


coor = [
    'a8','b8','c8','d8','e8','f8','g8','h8',
    'a7','b7','c7','d7','e7','f7','g7','h7',
    'a6','b6','c6','d6','e6','f6','g6','h6',
    'a5','b5','c5','d5','e5','f5','g5','h5',
    'a4','b4','c4','d4','e4','f4','g4','h4',
    'a3','b3','c3','d3','e3','f3','g3','h3',
    'a2','b2','c2','d2','e2','f2','g2','h2',
    'a1','b1','c1','d1','e1','f1','g1','h1',
]
decode = {
  'a':8,'b':7,'c':6,'d':5,
  'e':4,'f':3,'g':2,'h':1
}
encode = {
  1:'h',2:'g',3:'f',4:'e',
  5:'d',6:'c',7:'b',8:'a'
}
##################################################
def search(coor,code):
  for i in range(64):
    if code == coor[i]:
      return i
bN = pygame.image.load("Media\\bN.png")
bK = pygame.image.load("Media\\bK.png")
bQ = pygame.image.load("Media\\bQ.png")
bP = pygame.image.load("Media\\bP.png")
bB = pygame.image.load("Media\\bB.png")
bR = pygame.image.load("Media\\bR.png")
wN = pygame.image.load("Media\\wN.png")
wK = pygame.image.load("Media\\wK.png")
wQ = pygame.image.load("Media\\wQ.png")
wP = pygame.image.load("Media\\wP.png")
wB = pygame.image.load("Media\\wB.png")
wR = pygame.image.load("Media\\wR.png")
Greendot = pygame.image.load("Media\\green_circle_small.png")
Greenatack = pygame.image.load("Media\\green_circle_neg.png")
yellow_box = pygame.image.load("Media\\yellow_box.png")

#################################################
pygame.font.init()
myfont = pygame.font.SysFont("Comic Sans MS", 30)
win = myfont.render("You Win!", 1, (255,255,0))
lose = myfont.render("You Lose!", 1, (255,255,0))
stale = myfont.render("Stalemate!", 1, (255,255,0))
#################################################
def show(str,color, x,y):
  if color == 'black':
    if str == 'KING':
      DISPLAYSURF.blit(bK,chess_to_pixel_coord(x,y))
    if str == 'QUEEN':
      DISPLAYSURF.blit(bQ,chess_to_pixel_coord(x,y))
    if str == 'BISHOP':
      DISPLAYSURF.blit(bB,chess_to_pixel_coord(x,y))
    if str == 'KNIGHT':
      DISPLAYSURF.blit(bN,chess_to_pixel_coord(x,y))
    if str == 'PAWN':
      DISPLAYSURF.blit(bP,chess_to_pixel_coord(x,y))
    if str == 'ROOK':
      DISPLAYSURF.blit(bR,chess_to_pixel_coord(x,y))
  if color == 'white':
    if str == 'KING':
      DISPLAYSURF.blit(wK,chess_to_pixel_coord(x,y))
    if str == 'QUEEN':
      DISPLAYSURF.blit(wQ,chess_to_pixel_coord(x,y))
    if str == 'BISHOP':
      DISPLAYSURF.blit(wB,chess_to_pixel_coord(x,y))
    if str == 'KNIGHT':
      DISPLAYSURF.blit(wN,chess_to_pixel_coord(x,y))
    if str == 'PAWN':
      DISPLAYSURF.blit(wP,chess_to_pixel_coord(x,y))
    if str == 'ROOK':
      DISPLAYSURF.blit(wR,chess_to_pixel_coord(x,y))
####################################################
def pixel_coord_to_chess(pixel_coord):
    x,y = pixel_coord[0]/80, pixel_coord[1]/80
    #See comments for chess_coord_to_pixels() for an explanation of the
    #conditions seen here:
    return (9-x,9-y)
def chess_to_pixel_coord(x, y):
  pixel_coord_x = (8-x)*80
  pixel_coord_y = (8-y)*80
  return (pixel_coord_x,pixel_coord_y)
def showBoard(b):
  for i in range(64):
      if b.cases[i].nom != '.':
          it = coor[i]
          x = decode[it[0]]
          y = int(it[1])
          show(b.cases[i].nom,b.cases[i].couleur,x,y)
#################################################
def pos2code(x1,y1):
  x = encode[x1]
  y = str(y1)
  return x+y
def int2pos(num):
  code = coor[num]
  x = decode[code[0]]
  y = int(code[1])
  X,Y = chess_to_pixel_coord(x,y)
  return X,Y
#################################################
def Highlight(pos,promot):
  mlist=[]
  if b.cases[pos].nom == 'PAWN':
    mlist += b.cases[pos].pos2_PAWN(pos,b.cases[pos].couleur,b)
  if b.cases[pos].nom == 'ROOK':
    mlist += b.cases[pos].pos2_ROOK(pos,oppColor(b.cases[pos].couleur),b)
  if b.cases[pos].nom == 'KNIGHT':
    mlist += b.cases[pos].pos2_KNIGHT(pos,oppColor(b.cases[pos].couleur),b)
  if b.cases[pos].nom == 'BISHOP':
    mlist += b.cases[pos].pos2_BISHOP(pos,oppColor(b.cases[pos].couleur),b)
  if b.cases[pos].nom == 'KING':
    mlist += b.cases[pos].pos2_KING(pos,oppColor(b.cases[pos].couleur),b,False)
  if b.cases[pos].nom == 'QUEEN':
    mlist += b.cases[pos].pos2_ROOK(pos,oppColor(b.cases[pos].couleur),b)
    mlist += b.cases[pos].pos2_BISHOP(pos,oppColor(b.cases[pos].couleur),b)
  for pos1 in range(64):
    if((pos,pos1,promot) in mlist):
      x,y = int2pos(pos1)
      if b.cases[pos1].nom == '.':
        DISPLAYSURF.blit(Greendot, (x, y))
      else:
        DISPLAYSURF.blit(Greenatack, (x, y))
#################################################
def colorPath(src,des,flag):
  if flag:
    x,y = int2pos(src)
    DISPLAYSURF.blit(yellow_box, (x, y))
    x,y = int2pos(des)
    DISPLAYSURF.blit(yellow_box, (x, y))
#################################################
def oppColor(c):
  if c == 'black':
    return 'white'
  else:
    return 'black'
#################################################

#################################################
pygame.init()
FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()
WHITE = (255, 255, 255)
DISPLAYSURF = pygame.display.set_mode((600,600))
pygame.display.set_caption('chessgame')
background = pygame.image.load("Media\\board.png")
size_of_bg = background.get_rect().size
square_width = size_of_bg[0]/8
square_height = size_of_bg[1]/8
DISPLAYSURF = pygame.display.set_mode(size_of_bg)

###################-Main-######################
click = 0
code = ''
code1 = ''
Promot = ''
num = -5
userclick = False
StaleGame = -1
src = 1
des = 1
flag = False

while True: # the main game loop
    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(background, (0, 0))
    showBoard(b)
    if e.print_result(b) == 1:
       DISPLAYSURF.blit(lose, (240,240))
    if e.print_result(b) == 0:
       DISPLAYSURF.blit(win, (240,240))
    if e.print_result(b) == 2:
       DISPLAYSURF.blit(stale, (240,240))
    if userclick:
       userclick = False
       src,des = e.search(b)
       flag = True
       print('side to move: '+ b.side2move)
    colorPath(src,des,flag)
    if num!= None:
      Highlight(num,Promot)
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
          click +=1
          pos = pygame.mouse.get_pos()
          X,Y =  pixel_coord_to_chess(pos)
          x,y = chess_to_pixel_coord(int(X),int(Y))
          code += pos2code(int(X),int(Y))
          if click == 1:
            num = search(coor,code)
            if num != None:
              if (b.cases[num].nom == 'PAWN' and b.cases[num].couleur == 'white'
              and num in (48, 49, 50, 51, 52, 53, 54, 55)) or( 
              b.cases[num].nom == 'PAWN' and b.cases[num].couleur == 'black'
              and num in (8,  9, 10, 11, 12, 13, 14, 15)):
                Promot = 'q'
              else:
                Promot = ''
          if click == 2:
            f = True
            cnow = pos2code(int(X),int(Y))
            if b.cases[search(coor,cnow)].couleur == 'black':
              code = cnow
              click = 1
              f = False
              num = search(coor,cnow)
            if num!= None:
              if (b.cases[num].nom == 'PAWN' and b.cases[num].couleur == 'white'
              and num in (48, 49, 50, 51, 52, 53, 54, 55)) or( 
              b.cases[num].nom == 'PAWN' and b.cases[num].couleur == 'black'
              and num in (8,  9, 10, 11, 12, 13, 14, 15)):
                code+='q'
            if f:
              click = 0
            else:
              click = 1
            if e.usermove(b,code):
              userclick = True
              code = ''
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    fpsClock.tick(FPS)
