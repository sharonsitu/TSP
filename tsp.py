import math
import queue
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
        ##print(cities)

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
        

### get MST from the start city, to list of unvisited cities
def MST(start,unvisit):
        curcity = start
        nextcity = ""
        edges = []
        unvisitcities = unvisit[:]
        miniSpanningTree = []
        ##print(start,unvisit)
        while (True):
                miniDist = 0
                unvisitcities.remove(curcity)
                for i in range(len(unvisitcities)):
                        city = unvisitcities[i]
                        index1 = cities.get(curcity)[0]
                        index2 = cities.get(city)[0]
                        weight = CitiesDistance[index1][index2]
                        edges.append([curcity,city,weight])
                ##print(edges)
                for j in range(len(edges)):
                        city1 = edges[j][0]
                        city2 = edges[j][1]
                        weight = edges[j][2]
                        if (nextcity == ""): ## first add
                                if (city2 in unvisitcities):
                                        curcity = city1
                                        nextcity = city2
                                        miniDist = weight
                        else:
                                if (city2 in unvisitcities and weight < miniDist):
                                        curcity = city1
                                        nextcity = city2
                                        miniDist = weight
                miniSpanningTree.append([curcity,nextcity,miniDist])
                edges.remove([curcity,nextcity,miniDist])
                curcity = nextcity
                nextcity = ""
                if (len(miniSpanningTree) == (len(unvisit) - 1)):
                        break
        ## count the cost for the tree
        totalcost = 0
        for k in miniSpanningTree:
                totalcost += k[2]
        return totalcost

### find list of cities that are not visited
def UnvisitCities(visited):
        unvisit = []
        for city in cities:
                if (city not in visited):
                        unvisit.append(city)
        return unvisit

### use PriorityQueue to store the visited cities, use the (actual cost for visited citites + estimated cost for unvisit cities) as priority
OrderCities = queue.PriorityQueue()
### use to count the node
node = 1
### Doing A* search on TSP, return(OrderCities,distance,number of nodes)
def ASearch():
        ### one city case
        if (len(cities) == 1):
                return(["A"],0,1)
        ### start with city A, now the cost is 0
        OrderCities.put((0,["A"]))
        global node
        while (OrderCities):
                fn, visited = OrderCities.get()
                unvisit = UnvisitCities(visited)
                ## count the cost for visited cities
                precost = 0
                for i in range(0,len(visited)-1):
                        city1 = cities.get(visited[i])[0]
                        city2 = cities.get(visited[i+1])[0]
                        cost = CitiesDistance[city1][city2]
                        precost += cost
                ## when all the cities are visited and back to A
                if (len(visited) == (numofcity + 1)):
                        return (visited,precost,node)
                ## last visited city
                lastvisit = visited[-1]
                ## count MST for unvisit cities and setup PQ
                visitlist = visited[:]
                for j in range(0,len(unvisit)):
                        node += 1
                        unvisitlist = unvisit[:]
                        visited = visitlist[:]
                        if (len(visited) >= 1):
                                unvisitlist.insert(0,"A")
                        if (len(unvisit) >= 1):
                                mst = MST(unvisitlist[j],unvisitlist)
                        visited.append(unvisit[j])
                        c1 = cities.get(lastvisit)[0]
                        c2 = cities.get(unvisit[j])[0]
                        f = precost + mst + CitiesDistance[c1][c2]
                        OrderCities.put((f,visited))
                ## when all the cities are visited, we need to go back to A
                if (len(unvisit) == 0):
                        visited.append("A")
                        c1 = cities.get(lastvisit)[0]
                        f = precost + 0 + CitiesDistance[c1][0]
                        OrderCities.put((f,visited))


        
def main():
        ##for i in range(1,17):
                ##totalnode = 0
                ##for j in range(1,11):
                        ## i is the city number, j is the instance number
                        SetupCities(16,1)
                        SetupCitiesDistance()
                        starttime = datetime.datetime.now()
                        output = ASearch()
                        finishtime = datetime.datetime.now()
                        ##totalnode += output[2]
                        print(output)
                        print((finishtime - starttime).total_seconds())
                        global cities
                        global numofcity
                        global CitiesDistance
                        global OrderCities
                        global node
                        cities = {}
                        numofcity = 0
                        CitiesDistance = []
                        OrderCities = queue.PriorityQueue()
                        node = 1                              
                ##avgnode = totalnode / 10
                ##outputfile = open("OutputTSP.txt","a")
                ##outputfile.write(str(avgnode)+'\n')
                ##outputfile.close()                
                          
main()