from SlidingPuzzleSearch import Node, AStar
from math import sqrt

from PIL import ImageGrab, ImageOps, Image, ImageChops
import win32api, win32con, time, os


'''
8-Tile Node represents:

-1 1 2
 3 4 5
 6 7 8

where -1 is the empty tile
'''


'''
Windows Code
'''

'''
Left Mouse click down
'''
def leftDown():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.1)

'''
Left Mouse Click Up
'''
def leftUp():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

'''
get current mouse coordinates
'''
def get_cords(start_x,start_y):
    x,y = win32api.GetCursorPos()
    x = x - start_x
    y = y - start_y
    print x,y

    return (x,y)


'''
Perform Entire Left CLick
'''
def leftClick():
    leftDown()
    leftUp()


'''
Set mouse to coordinates given
'''
def mousePos(cord):
    win32api.SetCursorPos(cord)


'''
Game Grab Code
'''

global start_x,start_Y,width,height, number_width,number_height,number_padding



'''
Grabs entire screen
'''
def screenGrab():

    box = (start_x,start_y,start_x+width,start_y+height)
    im = ImageGrab.grab(box)
    #print "Time: "+datetime.datetime.now().time()
    url = os.path.abspath(os.path.dirname(__file__)) + '\\full_snapp__'+str(int(time.time()))+'.png'
    print url
    im.save(url,'PNG')


'''
Returns PIL.IMAGE of the number on the board at row and height given
'''
def getNumberImage(row=0,col=0,filename='number'):

    str_X = start_x +(row*number_width) + (row*number_padding)
    end_Y = start_y + (col*number_height)+ (col*number_padding)
    box = (str_X,end_Y,str_X+number_width,end_Y+number_height)
    im = ImageGrab.grab(box)
    #print "Time: "+datetime.datetime.now().time()
    #url = os.path.abspath(os.path.dirname(__file__)) + '\\'+filename+'.png'
    return im

global images
images = []
'''
Compares two PIL.Image objects to see if they are exactly the same
'''
def imagesEqual(im1, im2):
    return ImageChops.difference(im1, im2).getbbox() is None


'''
Returns of block in Sliding Tile game by comparing it to known image
'''
def getNumber(image):
    for i in range(0,len(images)):
        if imagesEqual(image,images[i]):
            return i+1
    return -1


'''
Loads images from disk to compare new images too
'''
def loadImages():
    for i in range(1,9):
        image = Image.open(os.path.abspath(os.path.dirname(__file__)) + '\\num_'+str(i)+'.png')
        images.append(image)


'''
Retrieves board configuration by getting images from a screen shot and
comparing each block in the puzzle to a block saved in disk.
'''
def getBoardConfiguration():
    board = []
    '''
    Board is 3x3 so using
    '''
    for j in range(0,3):
        for i in range(0,3):
            filename = str(i)+","+str(j)
            image = getNumberImage(i,j,filename)
            #print filename, getNumber(image)
            board.append(getNumber(image))
    return board

'''
Go to Position and Click.
'''
def moveMouseAndClick((x,y)):
    time.sleep(0.05)
    mousePos((x,y))
    time.sleep(0.05)
    leftClick()



'''

Puzzle at: http://mypuzzle.org/sliding

Starting x and y (in pixels) of the sliding puzzle game on window

width and height (in pixels) of the entire sliding puzzle game
from top left corner of first block to bottom right corner of last block

Number_width and height are the width and height of each block

padding is the padding between each number block

'''
start_x = 116
start_y = 367
width = 299
height = 299

number_width = 98
number_height = 98
number_padding = 2



loadImages()

a = getBoardConfiguration()


b = [1,2,3,4,5,6,7,8,-1]


t = Node(None,b)

print a,b
g = AStar(a,b)

if g is False:
    print "Not found"
    exit()

stack = []

print g

while g is not None:
    stack.append(g)
    g = g.parent
    #print g

mouse_padding = 50

print "Number of Moves: ",len(stack)-1



while len(stack) > 0:
    t = stack.pop()
    #print "\nLevel: ",t.level
    #print "\nMove: ",t.MOVE_CLICKED
    if t.MOVE_CLICKED is not None:
        x = (start_x+(number_width*t.MOVE_CLICKED[0])+mouse_padding)
        y = (start_y+(number_height*t.MOVE_CLICKED[1])+mouse_padding)
        moveMouseAndClick((x,y))
    #print "\nh(x): ",t.getHeuristic()
    #print t
