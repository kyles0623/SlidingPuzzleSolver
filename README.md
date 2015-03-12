# SlidingPuzzleSolver
I was bored and decided to make a program that solves the sliding puzzle at http://mypuzzle.org/sliding

I used A* Search with g(x) being the moves since origin and h(x) being the manhattan distance of each block from its expected position.

You can use this on your machine if you can pinpoint the x,y coordinates of the puzzle on your screen.

I used PIL for the image retrieval and winapi32 for the mouse clicking. 
I have raw copies of the numbers on the board so when the images are initially taken from the board, I can figure out which is which without number recognition software.


<h2>Requirements:</h2>

Windows Machine

<h2>Configuration</h2>

<b>Screen Resolution:</b> 1920x1080 monitor 


<h2>Settings</h2>

These are the settings of the variables used in the python script

    #Starting x and y (in pixels) of the sliding puzzle game on window

    start_x = 116

    start_y = 367

    #width and height (in pixels) of the entire sliding puzzle game from top left corner of first block to bottom right corner of last block --

    width = 299
    height = 299

    #Number_width and height are the width and height of each block --

    number_width = 98
    number_height = 98

    #padding is the padding between each number block --

    number_padding = 2
