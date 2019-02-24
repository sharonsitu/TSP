import math
import random
import datetime

### each city has its index, x axis and y axis
cities = {}
numofcity = 0
### load the file and set up cities
### m is the folder index, n is the instance index
def SetupCities(m,n):
    index = 0
    path = './tsp_problems/'+str(m)+'/instance_'+str(n)+'.txt'
    file = open(path,'r')
    global numofcity
    numofcity = int(file.readline().rstrip())
    for i in range(numofcity):
        city = file.readline().split()
        global cities
        cities[city[0]] = (index,int(city[1]),int(city[2]))
        index += 1     
    file.close()

CitiesDistance = []
### calculate cost for each city pair
def SetupCitiesDistance():
        for i in cities:
                cost = []
                for j in cities:
                        xdiff = cities.get(i)[1]-cities.get(j)[1]
                        ydiff = cities.get(i)[2]-cities.get(j)[2]
                        c = math.sqrt((xdiff**2) + (ydiff**2))
                        cost.append(c)
                ##print(cost)
                global CitiesDistance
                CitiesDistance.append(cost)


def GetRandomTour():
    tour = []
    remains = list(cities.keys())
    tour.append("A")
    del remains[0]
    nextindex = 1
    for i in range(0,len(remains)):
        nextindex = random.randint(0,len(remains)-1)
        nextcity = remains[nextindex]
        tour.append(nextcity)
        del remains[nextindex]
    tour.append("A")
    return tour

def GetNeighbours(tour):
    neighbours = []
    for i in range(0,len(tour)-1):
        n = tour[:]
        temp = n[i]
        n[i] = n[i+1]
        n[i+1] = temp
        if (i == 0):
            n[len(tour)-1] = n[0]
        if (i == len(tour)-2):
            n[0] = n[i+1]
        neighbours.append(n)
    return neighbours

def TotalDistance(tour):
    global CitiesDistance
    dis = 0
    for i in range(0,len(tour)-1):
        city1 = cities.get(tour[i])[0]
        city2 = cities.get(tour[i+1])[0]
        cost = CitiesDistance[city1][city2]
        dis += cost
    return dis

def GetBestNeighbour(tour):
    neighbours = GetNeighbours(tour)
    mincost = TotalDistance(neighbours[0])
    best = neighbours[0]
    for i in range(1,len(neighbours)):
        t = neighbours[i]
        cost = TotalDistance(t)
        if (cost < mincost):
            best = t
            mincost = cost
    ##print(best)
    return best
    
step = 0    
def LocalSearch():
    curtour = GetRandomTour()
    ##print(curtour)
    while (True):
        ##print(curtour)
        global step
        step += 1
        nexttour = GetBestNeighbour(curtour)
        ## change <= to < for strict local optimal
        if TotalDistance(curtour) <= TotalDistance(nexttour):
            break
        curtour = nexttour
    return curtour

def main():
    ## SetupCities(i,j) i is the city number, j is the instance number
    SetupCities(16,1)
    SetupCitiesDistance() 
    global step
    totalstep = 0
    totalq = 0
    match = 0
    time = 0
    altlist = ['A', 'C', 'K', 'M', 'H', 'I', 'G', 'J', 'E', 'F', 'D', 'O', 'N', 'B', 'P', 'L', 'A'] ## BY ASEARCH
    altcost = TotalDistance(altlist)
    for j in range(0, 100):
        tour = LocalSearch()
        mincost = TotalDistance(tour)
        starttime = datetime.datetime.now()
        ## restart time
        for i in range(0,210):
            retry = LocalSearch()
            if (TotalDistance(retry) < mincost):
                tour = retry
                mincost = TotalDistance(retry)
        finishtime = datetime.datetime.now()
        cost = TotalDistance(tour)
        ##print(tour)
        ##print(cost)
        q = cost/altcost
        totalq += q
        runtime = (finishtime - starttime).total_seconds()
        time = time + runtime
        step = 0
    avgq = totalq / 100
    avgtime = time /100
    print(avgq)
    print(avgtime)
    
main()