def dijkstra_shortest_time(self, start_location, graph):
    """
    Function description: This function will find the shortest time to take to go from the source location to
    the rest of the other locations in the graph (gives you shortest path tree)

    Approach: First a MinHeap is initialised with a size of the number of roads in the graph and will add the start
    location into the heap as we are going to compute the shortest travel time from the start location to other location.
    There will be a loop that will keep on looping until the heap is empty and each time a location is finalised (visited)
    then it will perform edge relaxation where it goes through all the edges that is connected to update if there
    are shorter routes to take to minimise the travel time.


    :Input:
     start_location: The source node where it is going to compute the shortest to time to take to all the location
     graph: The graph that is going to travel in

    :Output, return or postcondition: all location have the shortest path where it takes the minimal time to reach to the
    location from the source

    |L| : number of locations
    |R| : number of roads
    :Time complexity: O(|R| Log |L|)
    :Time complexity analysis: Complexity is O(|R| Log |L|) where |R| is the number of roads and |L| is the number
    of locations. The function will have a loop and get the location with the minimum travel time from the source location
    and will only break when the heap is empty means it will loop through all the roads available to find its
    minimum time travel O(|R|) and it will also loop through all the locations that is adjacent to the
    current location. While we loop through there maybe times where the location has found
    a route which has a shorter time so when we update the heap it will be O(log |L|). So the overall complexity will
    be O(|R| Log |L|).

    :Auxiliary Space complexity: O(|R|)
    :Auxiliary Space complexity analysis: where |R| is the number of roads. There will be extra space where the space is |R| to
    create the MinHeap to keep track of the shortest travel time from the source destination.
    """
    explored = MinHeap(self.number_roads)
    starting_location = graph[start_location]
    explored.add((starting_location.time, starting_location.name))

    while len(explored) >= 1:
        current_location = explored.get_Minimimum()
        current_location = graph[current_location[1]]
        current_location.finalise = True

        for edges in current_location.edge:
            neighbour = graph[edges.location_two]
            if neighbour.finalise == False:
                if neighbour.discovered == False:
                    neighbour.time = current_location.time + edges.time
                    neighbour.previous = current_location
                    neighbour.discovered = True
                    explored.add((neighbour.time, neighbour.name))

                else:
                    current_time = current_location.time + edges.time
                    if neighbour.time > current_time:
                        neighbour.time = current_time
                        neighbour.previous = current_location

                        explored.update_key((neighbour.time, neighbour.name))




class MinHeap:
    """
    This MinHeap data structure is a heavily modified version of Brendon Taylor and Jackson Goerner's Max Heap data
    structure from FIT 1008.
    This MinHeap class is a priority queue data structure that sorts according to the smallest key

    """
    MINIMUM_CAPACITY = 1

    def __init__(self, size):
        """
        Function description: Initialisation of MinHeap where it consists of an array to store all the items in the queue
        and an array with the exact same size to keep track of where each location is place in the MinHeap.

        :Input:
        size: size of the MinHeap
        :Output, return or postcondition: None
        :Time complexity: O(n) where n is the size of the heap
        :Time complexity analysis: it has to create n space for the array, so it has to put n None into the array
        :Auxiliary Space complexity: O(n)
        :Auxiliary Space complexity analysis: it has to create n space for the array, so it needs to have
        n extra space so aux space complexity is O(n)
        """
        self.length = 0
        if size == 0:
            size = 1
        self.index = [None] * (size + 1)
        self.heap = [None] * (size + 1)

    def rise(self, index):
        """
        Function description: rise the element added into the end of the heap to its correct position in the heap according
        to its key
        :Input:
         index: index of where the element is currently located at
        :Output, return or postcondition: None

        :Time complexity: O(Log |L|)
        :Time complexity analysis: |L| is the number of locations in this heap. When an element is rise
        it will either be at the left or right side of the heap so either way it will only be on one side therefore it
        will be at most Log |L| for it to rise to its correct position

        :Auxiliary Space complexity: O(1)
        :Auxiliary Space complexity analysis: Rise function just uses extra constant space to store temporary variable to switch
        elements to make sure the element is rise to its correct location.
        """

        location = self.heap[index]
        while index >= 2 and location < self.heap[index // 2]:
            item_switched = self.heap[index // 2]
            self.heap[index] = item_switched

            self.index[item_switched[1]] = index

            index = index // 2

        self.index[location[1]] = index
        self.heap[index] = location

    def add(self, data):
        """
        Function description: add an item into the heap by adding it to the end of the list and call the rise function
        to rise it to its correct position.
        :Input:
        data: a tuple which consist of a (key, data) to be added into the heap
        :Output, return or postcondition: None
        :Time complexity: O(Log |L|)
        :Time complexity analysis: It takes O(Log |L|) to add an item into the heap as it will be added into the end of the
        heap O(1) and will rise to its correct position which is O(Log |L|) where the rise operation will only rise on side,
        so it only needs to travel half of the locations in the heap to find its correct position.

        :Auxiliary Space complexity: O(1)
        :Auxiliary Space complexity analysis: As space was already created during the initialisation, so it just need extra space
        to store current data which is constant space O(1) that is going to be swapped in order to let the element
        that has just been added in to rise up to its correct position
        """

        self.length += 1
        self.heap[self.length] = data
        self.rise(self.length)

    def sink(self, position):
        """
        Function description: used to sink the element to its correct position from the top of the heap to the bottom position
        where it belongs to.
        :Input:
        position: the current position of where the item is place in the heap
        :Output, return or postcondition: None
        :Time complexity: O(log |L|)
        :Time complexity analysis: the complexity is O(log |L|) as it will sink to either the left side of the heap or the right
        side so either way it will not travel through all the location but instead it will at most travel half of
        the location in the heap.
        :Auxiliary Space complexity: O(1)
        :Auxiliary Space complexity analysis: As it only use extra space for temporary variables to store the position and
        index therefore it is constant space O(1)
        """
        location = self.heap[position]
        while self.length >= 2 * position + 1:

            if self.heap[2 * position] > self.heap[2 * position + 1]:
                minimum_child = 2 * position + 1
            else:
                minimum_child = 2 * position

            if self.heap[minimum_child] >= location:
                break

            item = self.heap[minimum_child]
            self.heap[position] = item

            self.index[item[1]] = position
            position = minimum_child
        self.heap[position] = location

        self.index[location[1]] = position

    def __len__(self):
        """
        Function description: return the number of elements in the heap
        :Input: None
        :return : the number of elements in the heap
        :Time complexity: O(1)
        :Time complexity analysis: returning an attribute from the heap is O(1) as it's a constant time operation
        :Auxiliary Space complexity: O(1)
        :Auxiliary Space complexity analysis: returning an attribute from the data structure does not require extra space
         therefore it is O(1)
        """
        return self.length

    def get_Minimimum(self):
        """
        Function description: get the top most element from the heap and return it as it is the minimum value in the heap

        :Input: None
        :Output, return or postcondition: return the minimum element in the heap
        :Time complexity: O(Log |L|)
        :Time complexity analysis: |L| being the number of locations in the heap. In this function return the location
        with the least time needed to travel and switch place with the location that has the longest travel time and
        sink it to its correct position which is O(Log |L|)
        :Auxiliary Space complexity: O(1)
        :Auxiliary Space complexity analysis: removing the smallest element from the heap will be O(1) as no extra space is used
        """

        if self.length == 0:
            raise IndexError
        smallest_item = self.heap[1]
        if self.heap[self.length] is not None:
            largest_item = self.heap[self.length]
            self.heap[1] = largest_item
            self.index[largest_item[1]] = 1
            self.sink(1)

        self.length -= 1
        return smallest_item

    def update_key(self, data):
        """
        Function description: updates the key of a specific value where the key is now lesser than before, so it will
        perform a rise operation to put it at is correct place
        :Input:
          data: the element that needs to be updated
        :Output, return or postcondition: None
        :Time complexity: O(log |L|)
        :Time complexity analysis: when we access the self.index array to get the items current position of the item that
        needs to be updated the complexity will be O(1) and update their key to the updated key and rise the item which is
        O(log |L|)
        :Auxiliary Space complexity: O(1)
        :Auxiliary Space complexity analysis: Updating a key will be O(1) as it only use constant space for reassigning values
        """
        position = self.index[data[1]]
        self.heap[position] = data
        self.rise(position)
