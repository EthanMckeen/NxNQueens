#Output: for different values of N: 4, 8, 16, 64, 100, 1000, 10000, 100000, measure the execution times for each case.

import timeit
import random

case = { '1' : 4,
         '2' : 8,
         '3' : 16,
         '4' : 64,
         '5' : 100,
         '6' : 1000,
         '7' : 10000,
         '8' : 100000}
V = {}
C= {}
E = {}
dom = [] #domain for all is the same numbers 1-N
solution = {}
randum = [True, False, False, False, True]
M = 0

def initVdom(N):
    global M
    global randum
    global V
    global dom
    M = N-1
    randum = [False, False, False, False, True]
    b = 0
    while(b < 100):
        random.shuffle(randum)
        b += 1
    V.clear()
    dom.clear()
    a = 1
    while(a <= N):
        V.setdefault(a, "NULL") #creates a dict with N variables with no assigned values
        solution.setdefault(a, 0) # creates what a solution should out put
        dom.append(a)  #adds to the domain 1-N
        a+=1               #iterate forward

def heuristic(F, N): #gives h(n) for a single given world
    C.clear()
    a = 1
    while(a <= N):
        C.setdefault(a, 0)  # sets each var to start with 0 contradictions
        a+=1
    #calc errors
    for i in F: # for each var
        r = i + 1 #a pointer to the right of x          
        l = i - 1 #a pointer to the left of x                 
        rhFound = False
        lhFound = False
        trdFound = False 
        brdFound = False
        tldFound = False             
        bldFound = False             
        while(r < N+1 or l > 0): #check each element around
            if(r < N+1): #check if pointer r is in bounds
                if(not rhFound and F[r] == F[i]):   #these elements are in the same row right with no pieces between
                    C[i] += 1       #this var has +1 error
                    #print("ERROR H WITH c", i, "and ", r)
                    rhFound = True
                if(not trdFound and F[i] - r+i == F[r]): #these elements are in the same diag right with no pieces between
                    C[i] += 1    #this var has +1 error
                    #print("ERROR trD WITH c", i, "and", r)
                    trdFound = True
                if(not brdFound and F[i] + r-i == F[r] ): #these elements are in the same diag right with no pieces between
                    C[i] += 1    #this var has +1 error
                    #print("ERROR brD WITH c", i, "and ", r)
                    brdFound = True

            if(l > 0): #check if pointer l is in bounds
                if(not lhFound and F[l] == F[i]):  #these elements are in the same row left with no pieces between
                    C[i] += 1   #this var has +1 error
                    #print("ERROR H WITH c", i, "and ", l)
                    lhFound = True
                if(not tldFound and F[i] - i+l == F[l]): #these elements are in the same diag right with no pieces between
                    C[i] += 1    #this var has +1 error
                    #print("ERROR tlD WITH c", i, "and", l)
                    tldFound = True
                if(not bldFound and F[i] + i-l == F[l]): #these elements are in the same diag right with no pieces between
                    C[i] += 1    #this var has +1 error
                    #print("ERROR blD WITH c", i, "and ", l)
                    bldFound = True
            r += 1
            l -= 1
        #by going left and right from the var this way makes it so that if
        #three are in a row/diag the middle one will have 2 errors and the 
        #ends only one (that is the purpose of Found)
        #plus with struct restriction only one piece per column we just check the 2 diagonal squares from I in column r or l
        
    return C
            
def eval(N):
    global V
    global E
    for i in V: # for each var
        F = V.copy()    #copies the current world
        j = 1
        temp=[]
        err = 0
        while(j <= N): # dom is 1-N
            err= 0
            F[i] = j   # moves queen to create a nieghbor
            h = heuristic(F, N)
            for a in h:
                err+= h[a]#summ total error
            err = err//2 #each connection between 2 pieces is double counted
            temp.append(err)
            j+=1
        E[i] = temp
                  
def findBest(N): #greedy descent
    global M
    global E
    loc=[]
    temp=[]
    E.clear()
    eval(N) #evaluate all nieghbors
    #print('\nCUR MIN ', M)
    for c in E:
        for r in range(len(E[c])): #trickniess ahead so r is the index of the row not the value ie row1 = 0
            if(E[c][r]<M):    #new low found
                M = E[c][r]   #what is that low
                #print('\nNEW MIN ', M)
                loc = [c, r + 1]    # what is its location r+1 to give dom value
                temp.clear()    #clear all loc of prev Min
                temp.append(loc)    #add loc to a list for this min
            elif(M==E[c][r]):   #new loc with = min
                loc = [c, r + 1] #what is its location r+1 to give dom value
                temp.append(loc)
    if(temp == []):
        temp.append('NULL')
    return random.choice(temp)  #break ties with random choice
         
        
def modify(N):
    err=0
    global V
    global M
    if(random.choice(randum)):  #random step
        x = random.choice(dom)    #random Col bc dom(rows) = col 
        V[x] = random.choice(dom)  #move that piece to a rand row
    else:
        loc = findBest(N)   #find what move improves h(n)
        if(loc == 'NULL'): #if at local min with no = moves force restart
            r = 1
            while (r <= N):
                V[r] = random.choice(dom) 
                r+=1
            print("Restart WORLD\n\n")
            h = heuristic(V, N)
            for a in h:
               err+= h[a]#summ total error
            M = err//2 #set cur min
        else:
            V[loc[0]]= loc[1]   #move to that loc


def doLocalSearch(N):
    global V
    global M
    r = 1
    err = 0
    while(1):
        while (r <= N):
            V[r] = random.choice(dom) 
            r+=1
        print("Restart WORLD\n")
        h = heuristic(V, N)
        for a in h:
           err+= h[a]#summ total error
        M = err//2 #set cue MIN
        while(heuristic(V, N) != solution): #lets use Greedy with random restart
            if(random.choice(randum)): #randomly restarts
                break
            else:
                modify(N)
                print("NEW WORLD\n")

        if(heuristic(V, N) == solution):
            break
    print("SOLUTION FOUND ", V)







#driver
initVdom(case['3'])
doLocalSearch(case['3'])