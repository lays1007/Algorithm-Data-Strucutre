
class FlowNetwork:
    """
    FlowNetwork is a class and, it consists a graph with edges that has a capacity and a flow it helps to
    see if we can maximise our choices by looking at the flow
    """

    def __init__(self,edges,experience, no_experience, source,sink,people):
        """

             Function description: To initialise the flow network with a sink, source node, the number of people, the number
             of activity and extra nodes for each activity.

            Approach description: Loops through all the nodes that has been preprocessed by the assign function where
            each node of the graph has an adjacency list to store all the edges

            :Input:
                :param edges: a list of edges where is connects the nodes together
                :param experience: a list which stores the index node of the activity
                :param no_experience: a list which stores the index the nodes of people with no experience
                :param source: the source node of the graph
                :param sink: the sink node of the graph
                :param people: the number of participants

            :Output, return or postcondition: None

             N : the number of participants
            :Time complexity: = O(N)
            :Time complexity analysis: When initialising the graph it will be the number of nodes but the number of nodes
            will always be N+2M+2 and since M is at most N/2 and +2 for source and sink node
            so it means N will have the most significant impact so O(N). After it will loop through all the nodes which is
            O(N) so to connect the edge between the vertices. So overall O(N)


            :Auxiliary Space complexity: O(N^2)
            :Auxiliary Space complexity analysis: O(N^2) the space used will be the number of nodes but since the number of
            nodes is always N+2M+2 so it can be considered as O(N) and for each node it will have at most N so it will be
            O(N), where in this case it will usually be the source node having N elements in its adjacency list
            so it will be O(N^2)

            """
        number_nodes = people+len(experience)+len(no_experience)+2
        self.length = number_nodes
        self.people = people
        self.experience = experience
        self.no_experience = no_experience
        self.source = FlowNetworkVertex(source)
        self.sink = FlowNetworkVertex(sink)
        self.graph = [None]*number_nodes
        self.place = len(experience)



        for i in range(len(edges)):

            node_1 = edges[i][0]
            node_2 = edges[i][1]
            capacity = edges[i][2]


            if self.graph[node_1] == None:

                self.graph[node_1] = FlowNetworkVertex(node_1)

            if self.graph[node_2] == None:
                self.graph[node_2] = FlowNetworkVertex(node_2)

            edge = FlowNetworkEdge(self.graph[node_2],capacity)
            vertex_1 = self.graph[node_1]
            vertex_1.edge.append(edge)

    def __len__(self):
        """

        Function description: return the number of elements in the flow network
        :Input: None
        :return : the number of elements in the flow network
        :Time complexity: O(1)
        :Time complexity analysis: returning an attribute from the flow network is O(1) as it's a constant time operation
        :Auxiliary Space complexity: O(1)
        :Auxiliary Space complexity analysis: returning an attribute from the data structure does not require extra space
         therefore it is O(1)
        """
        return self.length


    def get_flow(self):
        """
           Function description: this function get all the participants with choice in which activity they will pick in a
           list

           Approach description: First loop m times where m is the number of activities to initialise the space for the list
           where the list identifies the indices of participants that will be going to the activity. Then it will loop
           through all the participants to see if there is a flow to an activity. If there is, it means that the participant
           will be taking part of that activity for the whole weekend. When looping through all the participants, it will
           have an inner loop to check if the participant have a flow to an activity if there is then it will break and
           loop m times to check retrieve index of each activity and put the participant into the list.

           :Input:
               None

           :Output, return or postcondition: a list of activities where a list identifying the indices of the participants
           that will be going to the activities.

            N : the number of participants
            M : the number of activities

           :Time complexity: O(N)
           :Time complexity analysis: When looping through the number of places which is activities it will be O(M)
           and after initialising the place then it will loop N times to see which participant has a flow to an activity
           in the for loop there will be another loop where it will loop at most M times to check edge (activity)
            the participant has flow to and there will be another loop O(M)to put the activity to the list that is to be
            return. So total it will be O(M+N*2M) but since M is always at most N/2 so we can simplify it to O(N)


           :Auxiliary Space complexity: O(N)
           :Auxiliary Space complexity analysis: the amount of space used will be N amount as this function will return
           all the participant but in different index of the list based on what activity they pick

        """
        places = []
        for i in range(self.place):
            places.append([])

        for i in range(self.people):
            node = self.graph[i]
            path = None

            #loop through all the edges that the participant is connected to
            for k in range(len(node.edge)):
                edges = node.edge[k]

                if edges.got_flow():

                    #identify which place is it then append it into the list
                    path = edges

                    break
            for j in range(self.place):
                activity = self.experience[j]
                no_experience = self.no_experience[j]
                if activity == path.node.name:
                    places[j].append(node.name)

                elif (no_experience== path.node.name):
                    places[j].append(node.name)
        return places



    def ford_fulkerson(self):
        """
           Function description: this is a function where it will find the maximum flow of the flow network where it will
           create a residual network from the flow network and will keep finding a path using BFS(has_path()) until there is no more
           path. In the end, if the flow is not the max flow it means that it is not feasible.

           Approach description: create a residual network from the flow network and find all the possible path that it can
           travel using .has_path() which is bfs and when an augmented path is found it will update all the path by adding
           or minus the flow for the back or forward edge and increment the flow in the flow network with the minimum flow
           of the augmented path and it will keep continuing until it has no more path.

           :Input:
               None

           :Output, return or postcondition: return the maximum flow of the flow network

            N : the number of participants

           :Time complexity: = O(N^3)
           :Time complexity analysis: Initialising the residual network will be O(N^2) and after initialising the graph
           when we check if there is still a path to the sink node it will be O(N^2) and when we get the path which is
           we augment the path and get the minimum flow from the graph it will be O(N) so overall is O(N^2+N^3) since
           O(N^3) has a more significant impact compared to O(N^2) so the complexity will be O(N^3)

           :Auxiliary Space complexity: O(N^2)
           :Auxiliary Space complexity analysis: Initialising the residual graph will require extra O(N^2) space but
           when we call has.path() and get_path() it will have at most O(N) so since O(N^2) is more significant than
           O(N^2) so the overall complexity will be O(N^2)

        """
        flow = 0
        residual_network = ResidueNetwork(self.graph, self.source.name, self.sink.name, self.length)
        while residual_network.has_path():
            path = residual_network.get_path()
            flow +=path
        return flow





class FlowNetworkVertex:
    """
    FlowNetworkVertex is a class which represent each node in the graph where they have a name attribute and edge attribute
    which are the vertex that they are connected to.

    """
    def __init__(self,name):
        """
        Function description: Initialisation on the attributes that a node needs to have
        :Input:
        name: name of the node
        :Output, return or postcondition: None

        :Time complexity: O(1)
        :Time complexity analysis: all are constant time operations as assign values to an attribute is O(1)
        :Auxiliary Space complexity: O(1)
        :Auxiliary Space complexity analysis: as assigning value to attributes is constant space including an empty list
        therefore, its O(1)
        """
        self.name = name
        self.edge = []




class FlowNetworkEdge:
    """
    This is a FlowNetworkEdge an edge for the flow network graph where it connects two vertex together with a flow and a
    maximum capacity
    """
    def __init__(self, node,capacity):
        """
            Function description: Initialisation on the attributes that a flow network edge needs to have
            :Input:
            node: name of the node
            capacity: the maximum amount of flow that edge can take
            :Output, return or postcondition: None
            :Time complexity: O(1)
            :Time complexity analysis: all are constant time operations as assign values to an attribute is O(1)
            :Auxiliary Space complexity: O(1)
            :Auxiliary Space complexity analysis: as assigning value to attributes is constant space therefore, its O(1)
        """
        self.node = node
        self.flow = 0
        self.capacity = capacity


    def increment_flow(self, flow=1):
        """
            Function description: increment the flow of the edge by 1 (default) or a flow that is pass into the argument


            :Input:
            flow: flow to be incremented to the edge
            :Output, return or postcondition: None
            :Time complexity: O(1)
            :Time complexity analysis: all are constant time operations as doing mathematical operation is O(1)
            :Auxiliary Space complexity: O(1)
            :Auxiliary Space complexity analysis: Incrementing a number is constant space as it does not require any extra
            space
        """
        if self.flow< self.capacity:
            self.flow+=flow

    def got_flow(self):
        """
           Function description: to check if the edge has flow till its max capacity


           :Input:
            None
           :Output, return or postcondition: True / None
           :Time complexity: O(1)
           :Time complexity analysis: comparing integer with integer is  O(1)
           :Auxiliary Space complexity: O(1)
           :Auxiliary Space complexity analysis: no extra space is used when comparing integer so its O(1)
           space
       """
        if self.flow == self.capacity:
            return True



class ResidueNetwork:
    """
    This is a ResidueNetwork class where it is a copy of the flow network graph but with back and forward edges to travel
    on
    """

    def __init__(self,graph,start,end,number_nodes):
        """
        Function description: To initialise a residue network it will take in the graph, source, sink node and the number
        of nodes there will be in this graph


        Approach description: loop through all the nodes and in the inner loop it will also loop through all the edges
        the node has and for each edge it sees it will add a forward and backward edge to the node.

        :Input:
            :param graph: the flow network graph to initialise the residual graph
            :param start: source node name of the graph
            :param end: the sink node name of the graph
            :param number_nodes: the number of nodes in the flow network graph


        :Output, return or postcondition: None

         N : the number of participants
        :Time complexity: = O(N^2)
        :Time complexity analysis: When initialising the graph it will be O(N) as the number of nodes will always be
        N+2M+2 and since M is at most N/2 so it means N will have the most significant impact so O(N). It later it will
        loop O(N) to get all nodes from the graph and for each node it will loop through its edges and the maximum amount of
        edges is O(N) so it will be O(N^2) as the source node will link with all the participants O(N) while the participant nodes will
        just be at most 2M. When looping the edges creating a forward and backward graph which is both O(1). So the overall
        complexity is O(N^2)


        :Auxiliary Space complexity: O(N^2)
        :Auxiliary Space complexity analysis: O(N^2). initialising the graph requires O(N) and since this is an adjacency list graph
        so when we add the edge into the vertex it will have at most N where is the number of participants
        as the source node will always connect to all the participants which is O(N). So overall extra space used is
        O(N^2)

        """

        self.length = number_nodes
        self.graph = [None]*len(graph)

        self.source = ResidueNetworkVertex(start)
        self.sink = ResidueNetworkVertex(end)

        self.graph[start] = self.source
        self.graph[end] = self.sink

        for i in range(number_nodes):

            vertex_name = graph[i].name
            if self.graph[vertex_name] == None:
                vertex = ResidueNetworkVertex(vertex_name)
                self.graph[vertex_name] = vertex
            else:
                vertex = self.graph[vertex_name]

            for j in range(len(graph[i].edge)):
                edge = graph[i].edge[j]

                if self.graph[edge.node.name] == None:
                    vertex_2 = ResidueNetworkVertex(edge.node.name)
                    self.graph[edge.node.name] = vertex_2
                else:
                    vertex_2 = self.graph[edge.node.name]

                if (edge.capacity == edge.flow):

                    flow = edge.capacity

                    forward_flow = 0
                    backward_flow = flow

                else:

                    flow = edge.capacity - edge.flow
                    if edge.flow == 0:
                        forward_flow = edge.capacity
                        backward_flow = 0
                    else:
                        forward_flow = flow
                        backward_flow = edge.flow

                forward_edge = ResidueNetworkForwardEdge(vertex_2, forward_flow, edge)
                backward_edge = ResidueNetworkBackwardEdge(vertex, backward_flow, edge)

                # reference to forward and backward edge
                forward_edge.backward = backward_edge
                backward_edge.forward = forward_edge
                vertex.edge.append(forward_edge)
                vertex_2.edge.append(backward_edge)



    def __len__(self):
        """

        Function description: return the number of elements in the residue network
        :Input: None
        :return : the number of elements in the residue network
        :Time complexity: O(1)
        :Time complexity analysis: returning an attribute from the residue network is O(1) as it's a constant time operation
        :Auxiliary Space complexity: O(1)
        :Auxiliary Space complexity analysis: returning an attribute from the data structure does not require extra space
         therefore it is O(1)
        """
        return self.length

    def has_path(self):
        """
            Function description: This function will find the shortest path to take to go from the source node to
            the sink node and if there is a path then it will return true or else it will return false.

            Approach: First a Circular Queue is initialised with a size of the number of nodes in the graph and will add the source
            location into the queue. Then we will continuously loop through all the nodes that have been added into the
            queue (through edge relaxation) until it has found the sink node then it will return a boolean value
            where if the sink node is found then it will be True else it will be False


            :Input:
             None

            :Output, return or postcondition: Boolean True/False

             n is the number of participants
            :Time complexity: O(n^2)
            :Time complexity analysis: Initialising the circular queue with the len(self) which is the number of nodes in this
            graph. The number of nodes will always be n+2m +2, 2m because there will be a node for an experience people
            and another node for non-experience people for each activity and +2 for the sink and source node.
            So the complexity to loop through all the nodes to reset is O(n+2m+2) where it
            can be simplified to O(n) as m<=n/2 so 2m will be 2m <=n and n still overpowers so O(n). The while loop will
            at most run O(n) times until the queue is empty which mean it has visited all the nodes. In the loop
            it will always perform an edge relaxation where it goes through all the edges that the current node is being connected
            which will at most be O(n) as the maximum amount of edges it can be is the source node connected to all of
            n participants so O(n) and checking if it can be travel or not would be O(1). So overall is  O(n+n*n) simplified
            it to be O(n^2)

            :Auxiliary Space complexity: O(n)
            :Auxiliary Space complexity analysis: It requires n extra space due to the initialisation of the Circular Queue
            with the number of nodes will always be n+2m +2, 2m because there will be a node
            for an experience people and another node for non-experience people for each activity and +2 for the sink and source node.
            So the complexity to loop through all the nodes to reset is O(n+2m+2) where it
            can be simplified to O(n) as m<=n/2 so 2m will be 2m <=n and n still overpowers so O(n).
        """
        found = CircularQueue(len(self))
        path = []
        found.append(self.source)
        while len(found)>=1:

            current = found.serve()

            current.finalise = True
            path.append(current)
            if current.name == self.sink.name:
                return True

            for edges in current.edge:

                if edges.no_path() == False:
                    activity = self.graph[edges.node.name]

                    if activity.finalise == False:
                        if activity.discovered == False:

                            found.append(activity)
                            activity.discovered = True
                            activity.previous = current
                            activity.previous_edge = edges



        return False

    def get_path(self):
        """
            Function description: Gets the augmented path by backtracking from the sink node to the source node and minus
            or adding flow according to the edges if it's a forward or backwards flow and in the end it will return the
            minimum flow.

            Approach: Initialise a stack using [] to store the path from the sink to the source when backtracking and at the
            same time find the minimum flow in the augmented path and after backtracking we pop the edge out from the
            stack, one by one and minus or adding the minimum flow to the edge depending if it's a backward or forward flow and
            at the same time also update the flow in the network flow.

            :Input:
             None

            :Output, return or postcondition: minimum flow of the augmented path

            n = number of participants
            m = number of activities
            e = number of edges in the path

            :Time complexity: O(n)
            :Time complexity analysis: when backtracking path from the sink node it will take O(e) where e is the number of
            edges it needs to travel to reach the source node and finding the minimum flow while backtracking will be
            constant time O(1) as comparing int is O(1). After that, we pop all the edges our from path list which will also
            take O(e) time. After augmenting the path, then we will loop through all the nodes which are O(nodes) where
            nodes are the number of nodes in the graph. In the graph the number of nodes will always be n+2m +2, 2m because
            there will be a node for an experience people and another node for non-experience people for each activity and
            +2 for the sink and source node. So the complexity to loop through all the nodes to reset is O(n+2m+2) where it
            can be simplified to O(n) as m<=n/2 so 2m will be 2m <=n and n still overpowers so O(n). Adding all the
            complexity together it will be O(2e+n) but n will have the most significant impact as the number of edges
            for a path will always be e=n-1 so overall complexity is O(n)


            :Auxiliary Space complexity: O(e)
            :Auxiliary Space complexity analysis: where e is the number of edges which will be at most n-1 where n is the
             number of nodes which to that will append into the stack when
            we backtrack and looping through all the nodes in the graph to reset() O(1) will take O(1) auxiliary space as
            no extra space were use when resetting the attributes of the vertex of the graph.
        """
        path = []

        length = 0
        location = self.sink

        minimum = 0

        if location.previous.name!= 0:
            minimum = location.previous_edge.flow
        while location.previous != None:

            if location.previous_edge.flow < minimum:
                minimum = location.previous_edge.flow
            path.append(location.previous_edge)

            location = location.previous
            length +=1


        while length>=1:
            location = path.pop()

            #update the flow network residual network
            location.update(minimum)

            length-=1
        for i in range(self.length):
            self.graph[i].reset()

        return minimum






class ResidueNetworkVertex:
    """
    ResidueNetworkVertex class an object that represent the node of the residue graph
    """
    def __init__(self,name):
        """
           Function description: Initialisation on the attributes that a node needs to have
           :Input:
           name: name of the node
           :Output, return or postcondition: None
           :Time complexity: O(1)
           :Time complexity analysis: all are constant time operations as assign values to an attribute is O(1)
           :Auxiliary Space complexity: O(1)
           :Auxiliary Space complexity analysis: as assigning value to attributes is constant space including an empty list
           therefore, its O(1)
        """
        self.edge = []
        self.name = name
        self.discovered = False
        self.finalise = False
        self.previous = None
        self.previous_edge = None


    def reset(self):
        """
       Function description: reset some of the attributes back to its default values so that when has_path is called
       it can run again without having the values from the previous call

       :Input: None
       :Output, return or postcondition: None
       :Time complexity: O(1)
       :Time complexity analysis: all are constant time operations as assigning default value to an attribute is O(1)
       :Space complexity: O(1)
       :Space complexity analysis: change the attributes back to its default value does not require any extra
       space therefore its O(1)
        """
        self.discovered = False
        self.finalise = False
        self.previous = None
        self.previous_edge = None




class ResidueNetworkForwardEdge:
    """
     ResidueNetworkForwardEdge class is used represent remaining flow that can be travel from one node to another
     which is a forward edge in the residue network and, it will do operation such as
     updating the flow according to the flow inputted update() and checking to see if the edge can still be travel or not
     no_path().
    """
    def __init__(self,node,flow,flow_network):
        """
           Function description: Initialisation a residue network forward edge by initialising the node that is connected to
           the flow and the reference to same flow network edge.

           :Input:
           node: a vertex object that the current node is connected to
           flow: flow between two nodes
           flow_network: reference to the flow_network edge
           :Output, return or postcondition: None
           :Time complexity: O(1)
           :Time complexity analysis: all are constant time operations as assign values to an attribute is O(1)
           :Auxiliary Space complexity: O(1)
           :Auxiliary Space complexity analysis: as assigning value to attributes is constant space so O(1)
        """
        self.node =node
        self.flow = flow
        self.flow_network = flow_network
        self.backward = None

    def update(self,amount):
        """
           Function description: Used to update the flow between the edges of the graph depending if its a forward flow
           then it will - the flow and it will + the flow to the backward edge flow and at the same time update the
           flow in the flow_network with the input amount

           :Input:
            amount: the amount of flow that will be added or minus from the edges
           :Output, return or postcondition: None
           :Time complexity: O(1)
           :Time complexity analysis: incrementing and decrementing operation are O(1)
           :Auxiliary Space complexity: O(1)
           :Auxiliary Space complexity analysis: incrementing and decrementing does not require extra space so O(1)
        """
        self.flow -= amount
        self.flow_network.flow += amount
        self.backward.flow += amount

    def no_path(self):
        """
           Function description: check if the edges still has a flow or not if the flow is 0 means there is no more path
           between the two nodes.

           :Input:
            None
           :Output, return or postcondition: None

           :Time complexity: O(1)
           :Time complexity analysis: complexity of comparing two integers are O(1) and return a boolean is also O(1)
           so overall complexity O(1)
           :Auxiliary Space complexity: O(1)
           :Auxiliary Space complexity analysis: incrementing and decrementing does not require extra space so O(1)
        """
        if self.flow == 0 :
            return True
        else:
            return False



class ResidueNetworkBackwardEdge:
    """
     ResidueNetworkBackwardEdge class is used represent flow that can be canceled
     which is a backward edge in the residue network, and it will do operation such as
     updating the flow according to the flow inputted update() and checking to see if the edge can still be travel or not
     no_path().

    """
    def __init__(self,node,flow,flow_network):
        """
           Function description: Initialisation a residue network backward edge by initialising the node that is connected to
           the flow and the reference to same flow network edge

           :Input:
           node: a vertex object that the current node is connected to
           flow: flow between two nodes
           flow_network: reference to the flow_network edge
           :Output, return or postcondition: None
           :Time complexity: O(1)
           :Time complexity analysis: all are constant time operations as assign values to an attribute is O(1)
           :Auxiliary Space complexity: O(1)
           :Auxiliary Space complexity analysis: as assigning value to attributes is constant space so O(1)
        """
        self.node = node
        self.flow = flow
        self.forward = None
        self.flow_network = flow_network


    def update(self,amount):
        """
           Function description: Used to update the flow between the edges of the graph depending if it's a backward flow
           then it will - the flow and it will + the flow to the forward edge flow and at the same time update the
           flow in the flow_network with the input amount

           :Input:
            amount: the amount of flow that will be added or minus from the edges
           :Output, return or postcondition: None
           :Time complexity: O(1)
           :Time complexity analysis: incrementing and decrementing operation are O(1)
           :Auxiliary Space complexity: O(1)
           :Auxiliary Space complexity analysis: incrementing and decrementing does not require extra space so O(1)
        """
        self.flow -= amount
        self.flow_network.flow -= amount
        self.forward.flow+= amount

    def no_path(self):
        """
          Function description: check if the edges still has a flow or not if the flow is 0 means there is no more path
          between the two nodes.

          :Input:
           None
          :Output, return or postcondition: None

          :Time complexity: O(1)
          :Time complexity analysis: complexity of comparing two integers are O(1) and return a boolean is also O(1)
          so overall complexity O(1)
          :Auxiliary Space complexity: O(1)
          :Auxiliary Space complexity analysis: incrementing and decrementing does not require extra space so O(1)
       """
        if self.flow == 0:
            return True
        else:
            return False




class CircularQueue:
    """
        This CircularQueue data structure is a heavily modified version of Maria Garcia de la Banda's CircularQueue data
        structure from FIT 1008.
        This CircularQueue class is where it follows a first in first out structure

    """

    def __init__(self,max_size=1):
        """
        Function description: Initialising a circular queue with array [None] and * size that has been input.

        :Input:
        min_size: the size inputted
        :Output, return or postcondition: None

        :Time complexity: O(n) where n is the size of the circular queue
        :Time complexity analysis: O(n) as it will take n times to initialise the space for the circular queue using
        [None]*max_size
        :Auxiliary Space complexity: O(n)
        :Auxiliary Space complexity analysis: it has to create n space for the array, so it needs to have
        n extra space so aux space complexity is O(n)
        """
        self.length = 0
        self.front = 0
        self.back = 0
        self.queue = [None]*max_size
        self.size = max_size

    def append(self,element):
        """
        Function description: Add an element to the rear of the queue which is to the back of the queue as it follows
        a first in first out order.

        :Input:
        element: the element that needs to be added into the queue
        :Output, return or postcondition: None

        :Time complexity: O(1)
        :Time complexity analysis: assigning the element to the back of the queue is O(1) as we previously have already
        initialise the space
        :Auxiliary Space complexity: O(1)
        :Auxiliary Space complexity analysis: putting an element to a queue is O(1) as previously we already have initialise
        the space so no extra space required
        """
        self.queue[self.back] = element
        self.length+=1
        self.back = (self.back + 1) % self.size

    def serve(self):
        """
        Function description: to delete the first element of the list and return that element that has been serve

        :Input:
        None
        :Output, return or postcondition:
        element: the first element in the queue

        :Time complexity: O(1)
        :Time complexity analysis: accessing the array to get the element is O(1) and recalculating the front index is also
        O(1)
        :Auxiliary Space complexity: O(1)
        :Auxiliary Space complexity analysis: access the array and recalculating the front index does not require any extra
        space so its O(1)
        """
        element = self.queue[self.front]
        self.length -= 1
        self.front = (self.front +1) % self.size
        return element

    def __len__(self):
        """
        Function description: return the number of elements in the CircularQueue
        :Input: None
        :return : the number of elements in the Circular Queue
        :Time complexity: O(1)
        :Time complexity analysis: returning an attribute from the CircularQueue is O(1) as it's a constant time operation
        :Auxiliary Space complexity: O(1)
        :Auxiliary Space complexity analysis: returning an attribute from the data structure does not require extra space
         therefore it is O(1)
        """
        return self.length


def assign(preference,places):
    """
    Function description: To assign each person to an activity for the weekend


    Approach description: First loop through all the activities to calculate the index of them so that they can be placed
    in the graph and each activity will have two nodes one for experience and another for non-experience participants
    and after it will loop through the preference list to check the preference of each participant for each activity. It
    will then loop through activities again to get the capacity of each activity then it will input the preprocess list_nodes
    into FlowNetwork and call ford_fulkerson to find is there a way for all participants to participate in the activities
    and if there is a way for all the participant to participate in the activity then it will return a list of the result
    else it will be None.


    :Input:
        :preference - preference of each person
        :places - the capacity for each activity

    :Output, return or postcondition:
        :None - When the flow_network is not feasible
        :lists - a list which consist of which participant will be in which activity

     N : the number of participants
     M: the number of activities
    :Time complexity: = O(N^3)
    :Time complexity analysis: It will loop m times to calculate the index for activity and it will later loop N*M times
     to get the preference for each activity. It will then later loop m times again to get the capacity of each
     activity. When we initialise a flow network it will be O(N) complexity but when we call ford_fulkerson the complexity
     will be O(N^3) and to get the result of the ford_fulkerson we call.get_flow() O(N). So O(N^3) is the has the most significant
     impact so it is O(N^3).


    :Auxiliary Space complexity: O(N^2)
    :Auxiliary Space complexity analysis: The total amount of extra space it has used is 2M for the activities index, N
    for the lists_nodes and when initializing flow_network it will be O(N^2) and calling ford_fulkerson will also need extra
    O(N^2) and getting the result of the input will be O(M) so it will be O(2M+2(N^2)+M). Since M is at most N/2 so the
    N^2 is the most significant impact so it will be O(N^2).

    """
    lists_nodes = []
    number_people = len(preference)
    number_activity = len(places)
    number_nodes = len(preference)+(len(places)*2)-1
    experience = []
    no_experience = []
    source = number_nodes+1
    sink = source+1
    normie = 0

    for place in range(number_activity):
        index_experience = number_people + place
        index_not_experience = number_people + number_activity + place
        experience.append(index_experience)
        no_experience.append(index_not_experience)

    for i in range(len(preference)):

        lists_nodes.append((source,i,1))
        person = preference[i]

        for interest in range(len(person)):

            if person[interest] == 1:

                lists_nodes.append((i,no_experience[interest],1))
                normie+=1
            elif person[interest] == 2:
                lists_nodes.append((i,experience[interest],1))

    for activities in range(len(places)):
        space = places[activities]
        if normie >0:
            place = space-2
        else:
            place = 0
        #link no experience node to experience node
        lists_nodes.append((no_experience[activities],experience[activities],place))
        #actvity to sink node
        lists_nodes.append((experience[activities],sink,space))

    flow_network = FlowNetwork(lists_nodes,experience,no_experience,source,sink,number_people)
    max_flow = flow_network.ford_fulkerson()

    if max_flow == number_people:

        place = flow_network.get_flow()
        return place
    else:
        return None