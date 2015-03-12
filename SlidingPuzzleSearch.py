import Queue, copy
from math import sqrt
from sets import Set
from time import clock

SIZE = 9
last_time = clock()


#Return SquareRoot of size of board as int (need for indexes)
def getSQRTSize():
    return int(sqrt(SIZE))

'''
Represents a Table configuration.

Stores Move and parent Node
'''
class Node:
    def __init__(self,p,d=None):

        '''
        Initialize Move clicked to get to current configuration
        from parent node
        '''
        self.MOVE_CLICKED = None

        '''
        If there isn't a configuration, set configuration to parents configuraiton
        If there isnt' a configuration, parent is expected to exist.

        '''
        if d == None:
            print ''
            self.data = copy.deepcopy(p.data)
            self.goal = copy.deepcopy(p.goal)
        else:
            self.data = d
            self.goal = None

        '''
        Set parent to passed value
        '''
        self.parent = p

        '''

        '''
        if p == None:
            self.level = 0
        else:
            self.level = p.level + 1

    def __str__(self):
        out = ""

        for i in range(0,len(self.data)):
            if i % getSQRTSize() == 0:
                out += "\n"
            out += str(self.data[i])+"   "
        return out

    def __eq__(self, other):
        if isinstance(other,Node):
            return cmp(self.data,other.data) == 0;
        return False

    def __hash__(self):
        return hash(str(self.data))

    def __cmp__(self,other):
        return cmp(self.getHeuristic(),other.getHeuristic())

    def setGoal(self,g):
        self.goal = g

    '''
    Retrieves heuristic based on manhattan distance
    '''
    def getHeuristic(self):
        total = self.level

        for i in range(0,SIZE-1):


            #Expected value of board based on i
            expected_x = ((self.goal[i+1])%getSQRTSize())
            expected_y = ((self.goal[i+1])/getSQRTSize())

            #Actual vaue of board based on current board configuraiton
            actual_x = ((self.data[i+1])%getSQRTSize())
            actual_y = ((self.data[i+1])/getSQRTSize())

            ##Manhattan Distance with a multiplier giving special interest to top left problems
            amt = (abs(expected_x-actual_x) + abs(expected_y-actual_y) ) * ((expected_x)+(expected_y))

            total += amt
        return total


    def equal(self,n):
        return cmp(self.data,n.data) == 0

    def getEmptyIndex(self):
        return self.data.index(-1)

    def slideFromLeft(self):
        index = self.getEmptyIndex()
        if index % getSQRTSize() == 0:
            return False
        b = index - 1

        '''
        Set click location so AI knows what to do
        '''
        moved_x = ((b)%getSQRTSize())
        moved_y = ((b)/getSQRTSize())
        self.MOVE_CLICKED = (moved_x,moved_y)

        self.data[index],self.data[b] = self.data[b], self.data[index]
        return True

    def slideFromRight(self):
        index = self.getEmptyIndex()
        if index % getSQRTSize() == getSQRTSize()-1:
            return False
        b = index + 1
        '''
        Set click location so AI knows what to do
        '''
        moved_x = ((b)%getSQRTSize())
        moved_y = ((b)/getSQRTSize())
        self.MOVE_CLICKED = (moved_x,moved_y)

        self.data[index],self.data[b] = self.data[b], self.data[index]
        return True

    def slideFromBottom(self):
        index = self.getEmptyIndex()

        if index > SIZE - (getSQRTSize()+1):
            return False

        b = index + getSQRTSize()

        '''
        Set click location so AI knows what to do
        '''
        moved_x = ((b)%getSQRTSize())
        moved_y = ((b)/getSQRTSize())
        self.MOVE_CLICKED = (moved_x,moved_y)

        self.data[index],self.data[b] = self.data[b], self.data[index]
        return True

    def slideFromTop(self):
        index = self.getEmptyIndex()

        if index < getSQRTSize():
            return False

        b = index - getSQRTSize()

        '''
        Set click location so AI knows what to do
        '''
        moved_x = ((b)%getSQRTSize())
        moved_y = ((b)/getSQRTSize())
        self.MOVE_CLICKED = (moved_x,moved_y)

        self.data[index],self.data[b] = self.data[b], self.data[index]
        return True


found = Set()


'''
Breadth-First Search
'''
def BFS(init,toFind):
    start = Node(None,init)
    goal = Node(None,toFind)

    queue = Queue.Queue()

    queue.put(start)

    #print start

    #print goal

    count = 0

    while(queue.empty() == False):
        t = queue.get()


        count = count + 1
        if t.equal(goal):
            return t



        a = Node(t)

        if(a.slideFromTop() and a not in found):
            found.add(a)
            queue.put(a)

        b = Node(t)

        if(b.slideFromBottom()  and  b not in found):
            found.add(b)
            queue.put(b)

        c = Node(t)

        if(c.slideFromLeft()  and c not in found):
            found.add(c)
            queue.put(c)

        d = Node(t)

        if(d.slideFromRight()  and d not in found):
            found.add(d)
            queue.put(d)




    return False


'''
Depth-First Search of Puzzle Solution
'''
def DFS(init,toFind,limit = -1):
    found.clear()
    start = Node(None,init)
    goal = Node(None,toFind)

    queue = []

    queue.append(start)

    #print start

    #print goal

    count = 0

    while(len(queue) > 0 ):
        t = queue.pop()


        count = count + 1

        if t.equal(goal):
            return t



        a = Node(t)

        if(a.slideFromTop()
            and a not in found
            and (limit == -1 or a.level <= limit)):

            found.add(a)
            queue.append(a)

        b = Node(t)

        if(b.slideFromBottom()  and  b not in found
            and (limit == -1 or b.level <= limit)):
            found.add(b)
            queue.append(b)

        c = Node(t)

        if(c.slideFromLeft()  and c not in found
            and (limit == -1 or c.level <= limit)):
            found.add(c)
            queue.append(c)

        d = Node(t)

        if(d.slideFromRight()  and d not in found
            and (limit == -1 or d.level <= limit)):
            found.add(d)
            queue.append(d)




    return False

'''
Iterative deepening search
'''
def IDS(init,toFind):

    limit = 1

    g = AStar(init,toFind,limit)

    while g is False:
        limit = limit + 1
        g = DFS(init,toFind,limit)

    return g


'''
AStar search for sliding puzzle nodes
g(x) = # of moves from initial state
h(x) = Summation of all blocks manhattan distance from expected position

'''
def AStar(init,toFind):

    global last_time

    start = Node(None,init)
    goal = Node(None,toFind)

    start.setGoal(toFind)

    queue = Queue.PriorityQueue()

    queue.put(start)

    #print start

    #print goal

    count = 0

    while(queue.empty() == False ):
        t = queue.get()

        if clock() - last_time > 5:
            print "getHeuristic: ",t.getHeuristic()
            print t
            last_time = clock()

        count = count + 1
        if t.equal(goal):
            return t



        a = Node(t)

        if(a.slideFromTop() and a not in found):
            found.add(a)
            queue.put(a)

        b = Node(t)

        if(b.slideFromBottom()  and  b not in found):
            found.add(b)
            queue.put(b)

        c = Node(t)

        if(c.slideFromLeft()  and c not in found):
            found.add(c)
            queue.put(c)

        d = Node(t)

        if(d.slideFromRight()  and d not in found):
            found.add(d)
            queue.put(d)
    return False
