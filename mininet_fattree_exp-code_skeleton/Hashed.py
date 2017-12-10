'''algorithm code is taken from http://www.gilles-bertrand.com/2014/03/disjkstra-algorithm-description-shortest-path-pseudo-code-data-structure-example-image.html'''

def HashHelperFunction(topoG,k,src,dst):
    ''' hash's helper function:

    makes link dictionary without the certain core switches
    calls dijkstras on it

    make a new graph that blocks all 

    '''
    
    #change topoG to topo & change topo input to topo object
    #k = topo.k
    # topoG = topo.g

    print '+'*50
    #print 'src: ' + src
    #print 'dst: ' + dst

    # del results['A']

    print 'k: ' + k

    pathSummary = hash(src+dst)
    print 'path: ' + str(pathSummary)
    print pathSummary%4

    graphDic = {} #empty dictionary
    for node in topoG.nodes(): # make switch dictionary without links
        graphDic[node] = {}
    for edge in topoG.edges(): # adds each link to each switch
        graphDic[edge[0]][edge[1]] = 1
        graphDic[edge[1]][edge[0]] = 1

    print 'linkDictionary: '
    print graphDic
    j = HashedDijkstra(graphDic,src,dst)
    print j
    return j
    print '+'*50



def HashedDijkstra(graph,src,dest,visited=[],distances={},predecessors={}):
    """ calculates a shortest path tree routed in src
    """    
    # a few sanity checks

    if src not in graph:
        raise TypeError('The root of the shortest path tree cannot be found')
    if dest not in graph:
        raise TypeError('The target of the shortest path cannot be found')    
    # ending condition

    if src == dest: #if source and destination are the same print out shorest path and exit
        # We build the shortest path and display it
        path=[]
        pred=dest
        while pred != None: # create 
            path.append(pred) # append list path to show the prgevious predecessors
            pred=predecessors.get(pred,None) # get next predecessor and if none return none this breaks the next loop
        print('shortest path: '+str(path)+" cost="+str(distances[dest])) #print out the path and distances
        print('shortest path: '+str(tuple(reversed(path)))+" cost="+str(distances[dest])) #print out the path and distances
        return str(tuple(reversed(path)))

    else :     
        # if it is the initial  run, initializes the cost
        if not visited: #this sets the source destination to 0 once because visited list
            distances[src]=0
        # visit the neighbors
        for neighbor in graph[src] : #each neighbor for the new starting node
            if neighbor not in visited: # if the neighbor hasnt been visited, check for new better paths
                new_distance = distances[src] + graph[src][neighbor] # create new weight for this new node + weight of source node
                if new_distance < distances.get(neighbor,float('inf')): # if new distance is less than the neightbor weight(if no weight assume infinity)
                    distances[neighbor] = new_distance #set distances of this new neighboring node to the new distance
                    predecessors[neighbor] = src #set the predecessors of this new neighbor to the "current node"
        # mark as visited
        visited.append(src) # add "current node" to visited

        # now that all neighbors have been visited: recurse                         
        # select the non visited node with lowest distance 'x'
        # run Dijskstra with src='x'
        unvisited={} # create unvisited dictionary
        for k in graph: # for each node
            if k not in visited: #if node is not in visited,
                unvisited[k] = distances.get(k,float('inf')) # add the weigths of every unvisited node
        x=min(unvisited, key=unvisited.get) # get the lowest weighted node 
        return hashedDijkstra(graph,x,dest,visited,distances,predecessors) # run dijkstra's algorithm on cheapest node
                


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    #unittest.main()

    # switches:
    # 0_0_1 0_1_1 0_2_1 0_3_1 1_0_1 1_1_1 1_2_1 1_3_1 2_0_1 2_1_1 2_2_1 2_3_1 3_0_1 3_1_1 3_2_1 3_3_1 4_1_1 4_1_2 4_2_1 4_2_2 

    graph = {'s': {'a': 2, 'b': 1},
            'a': {'s': 3, 'b': 4, 'c':8},
            'b': {'s': 4, 'a': 2, 'd': 2},
            'c': {'a': 2, 'd': 7, 't': 4},
            'd': {'b': 1, 'c': 11, 't': 5},
            't': {'c': 3, 'd': 5}}
    
    # check for same source and destination hosts
    # hash the results or hash source and destination
    '''
	hash source and destination on initial call
	hash[0]:	run dijkstra's once
	hash[1]:	run dijkstra's twice? skipping initial
				how do you block the first initial path and make it search another?

	hash[2]:
	hash[3]:
    '''
    # hashedDijkstra(graph,'s','t',visited=[],distances={},predecessors={})
    HashHelperFunction(graph,'s','t')


    # hash1 = hash('0_0_1 0_1_1')
    # print hash1
    # print hash1%4
    # hash2 = hash('1_1_1 1_2_1')
    # print hash2
    # print hash2%4    
    # hash3 = hash('2_3_1 3_0_1')
    # print hash3
    # print hash3%4    
    # hash4 = hash('0_0_1 0_1_1')
    # print hash4
    # print hash4%4    
    # hash5 = hash('4_1_1 4_1_2')
    # print hash5
    # print hash5%4

