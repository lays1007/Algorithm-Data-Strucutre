
def binary_search(lists, element):
    return binary_search_rec(0,len(lists),element,lists)

#reference from FIT 1008 Lecture slide Week 10 pg 21
def binary_search_rec(left,right,element,list_elements):
    if left == right:
        return right
    #take the position of the current list
    number_item = left+right
    position =  number_item// 2

    #if we found the element in this position then we will return it
    if list_elements[position] == element:
        return position

    elif list_elements[position]> element:
        return binary_search_rec(left, position, element, list_elements)

    elif list_elements[position]<element:
        return binary_search_rec(position + 1, right, element, list_elements)



class Node:
    def __init__(self,t,root = False):
        self.key = []
        self.child = []
        self.count = 0
        self.root = root
        self.leaf = True
        self.degree = t
        self.number_child =[]

    def check_reach_max(self):
        if len(self.key)==(2*self.degree)-1:
            return True
        elif len(self.key)<(2*self.degree)-1:
            return False

    def check_min(self):
        if len(self.key)==self.degree-1:
            return True
        elif len(self.key)>self.degree-1:
            return False



class B_Tree:
    def __init__(self,t):
        self.root = Node(t,True)
        self.degree = t

    def add_element(self,element,index,node):
        if index == len(node.key):
            node.key.append(element)
        else:
            # to update the ones after this element
            node.key.insert(index, element)
        node.count+=1

    def delete(self,element_list):
        for element in element_list:
            self.delete_rec(element,self.root)

    def delete_rec(self,element,node:Node):

        element_position = binary_search(node.key,element)
        #if the element position is within the list and the element exist in the current node then
        #we will perform a case 1 or case 2a,2b,2c if it's an internal node
        if element_position<len(node.key) and node.key[element_position] == element:

            if node.leaf:
                #we will usually check if the node is minimum before we go in so
                #if when the node here is at its minimum and its means that the root
                #node is actually a leaf node too
                if node.check_min():
                    if node.root:
                        node.key.pop(element_position)
                        node.count-=1
                        return True
                else:
                    #case 1
                    node.key.pop(element_position)
                    node.count-=1
                    return True

            else:

                #deleting an internal node
                #we check if the left node is not minimum then we will step down
                #and find the largest element from the left subtree and replace it as the internal
                #node value that we are currently deleting

                if not node.child[element_position].check_min():

                    #find and delete the largest number from the left subtree  and return it to be replace in this key's
                    #position

                    #this will be case 2a where when the left child node is not minimum so we can step in and
                    # find the predecessor from the left child
                    left_child = node.child[element_position]
                    largest_element = self.find_biggest(left_child,element)

                    #after it recursively found and deleted the predecessor then it will replace the current
                    #element with the predecessor
                    node.key[element_position] = largest_element
                    success = True

                elif not node.child[element_position+1].check_min():

                    #this will be a case 2b where the right child node is not full so we can step in
                    #find the successor number from the right subtree 2b

                    right_child = node.child[element_position+1]
                    smallest_element = self.find_smallest(right_child,element,node)

                    node.key[element_position] = smallest_element
                    success=True
                    #since it was deleted from the right node so we plus 1 to element position
                    element_position=element_position+1

                else:
                    #both left and right child is at minimum then we will merge and recursive delete the element
                    next_node,index = self.merge(node, element_position, element_position, element_position + 1)
                    element_position = index
                    success = self.delete_rec(element,next_node)

                #the amount of keys of the node we traverse down previous to delete from the leaf
                counter = node.number_child[element_position]
                #if delete was successful then we will decrement the counter by 1
                if success:
                    node.number_child[element_position] = counter - 1
                return success

        else:
            if node.leaf:
                #element don't exist
                return False

            else:
                next_node = node.child[element_position]
                #if the next node we want to traverse down has minimum number of element
                if next_node.check_min():
                    #element position is at 0 meaning we must traverse down the left child
                    if element_position == 0:

                        # we will check if the right sibling has any key to spare
                        right_sibling = node.child[element_position+1]

                        if not right_sibling.check_min():
                            #if it has keys to spare then they will rotate from the right to left
                            #so in this case the next node that is return will be the left subtree
                            next_node = self.rotate_right(right_sibling,node,element_position,next_node)

                        else:

                            # if previously the right element does not have any elements to spare then it will merge the node
                            next_node,index = self.merge(node,element_position,element_position,element_position+1)
                            element_position = index

                        success = self.delete_rec(element,next_node)


                    #when the element position at the end of the keys lists then it means it will go down the right child
                    elif element_position == len(node.key):
                        #now our element position is pointing to the right node so we -1 to get the left sibling
                        left_sibling = node.child[element_position-1]

                        #if the left sibling has a node to spare then it will rotate the element from the left ot right node
                        #where we want to travel
                        if not left_sibling.check_min():

                            next_node = self.rotate_left(left_sibling,node,element_position,next_node)


                        else:

                            # if the left sibling has nothing to spare then it will do a case 3b
                            next_node,index = self.merge(node, element_position-1, element_position-1, element_position)
                            element_position = index

                        success = self.delete_rec(element, next_node)

                    else:
                        # means the element position is in the middle
                        right_sibling = node.child[element_position+1]
                        left_sibling = node.child[element_position - 1]

                        #check if sibling nodes has an element to spare
                        if not right_sibling.check_min():
                            #rotate
                            next_node = self.rotate_right(right_sibling,node,element_position, next_node)

                        elif not left_sibling.check_min():

                            next_node = self.rotate_left(left_sibling,node,element_position,next_node)

                        else:

                            #when sibling nodes has no elements to spare then it will merge
                            next_node,index = self.merge(node,element_position,element_position,element_position+1)

                            element_position = index

                        success = self.delete_rec(element, next_node)

                else:
                    #when the next node is not minimum
                    success = self.delete_rec(element,next_node)

            # the amount of keys of the node we traverse down previous to delete from the leaf
            counter = node.number_child[element_position]
            if success:
                # if delete was successful then we will decrement the counter by 1
                node.number_child[element_position] = counter -1
            return success

    def rotate_right(self,right_sibling,node,element_position,next_node):
        # take smallest from right sibling
        smallest_elem = right_sibling.key[0]


        current_node_element = node.key[element_position]

        # put the smallest element from the right sibling to the node we are standing on
        node.key[element_position] = smallest_elem


        # update right subtree amount on standing node
        right_subtree_amount = node.number_child[element_position + 1]

        # decrement it by one as we borrowed it to the left subtree
        node.number_child[element_position + 1] = right_subtree_amount - 1


        next_node.key.append(current_node_element)

        #increment by one as we added a new key in order for us to step in later
        next_node.count += 1


        # update left subtree amount
        node.number_child[element_position] += 1

        #if the node we are going to step in is not a leaf node, it means it is an internal node
        if not next_node.leaf:
            #previously the most left subtree of this node will now become the left subtree's most right subtree
            right_link = right_sibling.child[0]

            next_node.child.append(right_link)

            #delete the most left subtree of the right sibling
            right_sibling.child.pop(0)


            # add the most left subtree amount of the right sibling into the left subtree
            right_counter = right_sibling.number_child[0]

            next_node.number_child.append(right_counter)

            right_sibling.number_child.pop(0)

            # move the child so also have to update the amount of the right subtree standing on
            node.number_child[element_position + 1] -= right_counter

            # update left subtree amount in standing node
            node.number_child[element_position] += right_counter

        #now pop the actual key that was borrowed
        right_sibling.key.pop(0)
        right_sibling.count -= 1
        return next_node

    def rotate_left(self,left_sibling,node,element_position,next_node):
        #borrow an element from the left sibling

        last_elem = left_sibling.count

        #the biggest element in the left sibling
        biggest_elem = left_sibling.key[last_elem - 1]


        # since we are borrowing it to the right subtree then we will decrement the amount of the left subtree
        node.number_child[element_position-1]-=1



        current_node_element = node.key[element_position - 1]
        # replace the parent element with this
        node.key[element_position - 1] = biggest_elem

        # it will be the smallest element when it's on the right side
        #when rotate the key value that we were standing on will then be place at the first element of the right sibling
        next_node.key.insert(0, current_node_element)

        next_node.count += 1

        # update the amount that of the next node that we are going to step in
        node.number_child[element_position] += 1

        #when the next node that we are about to step in is not a leaf node
        if not next_node.leaf:
            # the right most child of the left sibling will be place to the right sibling now which is the node that we
            # are going to step in
            left_link = left_sibling.child[last_elem]

            #insert it at the front of the list as it will be the left most child now
            next_node.child.insert(0, left_link)
            left_sibling.child.pop()

            # take the total amount of element it has on the left sibling
            left_counter = left_sibling.number_child[last_elem]
            next_node.number_child.insert(0, left_counter)
            left_sibling.number_child.pop()

            # move the child to the right so need to update the left subtree amount from the standing node
            node.number_child[element_position - 1] -= left_counter

            # update the right subtree from the standing node
            node.number_child[element_position] += left_counter

        # remove the element that was rotated
        left_sibling.key.pop()
        left_sibling.count -= 1
        return next_node

    def merge(self,node,position,left,right):

        #the node only got one element which is usually the root node
        if node.count ==1:

            #the left sibling will be at index 0
            left=0

            left_node = node.child[0]
            right_node = node.child[1]

            #the element to merge down
            merge_element = node.key[0]

            #add the element that merged down into the keys of the left node
            left_node.key.append(merge_element)
            #then we will increment the counter by one
            left_node.count+=1

            #then add all the keys from the right node to the left node
            left_node.key += right_node.key
            # and increment the count by the number of keys the right node had
            left_node.count+=right_node.count

            #if the node was a root
            if node.root:
                #now the left node will be the new root node
                left_node.root = True
                self.root = left_node

            #if the left node was previously not a leaf that means it was an internal node
            if not left_node.leaf:
                #add all the right node child to the left node's child list
                left_node.child+= right_node.child

                #update the number of child
                left_node.number_child+= right_node.number_child

        else:

            #the element to merge
            merge_element = node.key[position]


            left_node = node.child[left]
            right_node = node.child[right]

            #add the merge element into the key list
            left_node.key.append(merge_element)

            #push the element down to the left node so we increment the subtree amount
            node.number_child[left]+=1
            left_node.count += 1

            #add the keys from the right node to the left node
            left_node.key += right_node.key
            left_node.count += right_node.count

            #add the amount of the right subtree to the left since we merge
            node.number_child[left] +=node.number_child[right]

            # if left is an internal node
            if not left_node.leaf:

                left_node.child+=right_node.child
                left_node.number_child += right_node.number_child

            #delete the element that was merge down
            node.key.pop(position)
            #decrement the count by 1
            node.count-=1
            #pop of the right node since we merge the node with left node
            node.child.pop(right)
            node.number_child.pop(right)
        #the next node you will travel to is the left node since we merge all of our element to that node
        return left_node,left

    def find_biggest(self,node,element):
        #this function will basically delete the biggest element in this subtree
        if node.leaf:
            if not node.check_min():
                largest_elem = node.key.pop()
                node.count-=1
                return largest_elem
        else:
            #it will always go to the right most child as we want to find the predecessor
            last_elem_index = node.count
            next_node = node.child[last_elem_index]

            # if the next node we want to step in is a minimum then we will perform a case 3a or a 3b
            if next_node.check_min():
                # since we will always go right to find the largest element so we if we need to borrow an element it will
                # be from its left sibling
                left_sibling = node.child[last_elem_index-1]


                if not left_sibling.check_min():
                    #if the left sibling as an element to spare then we will rotate
                    next_node = self.rotate_left(left_sibling,node,last_elem_index,next_node)


                else:
                    #if both sibling have minimum elements then they will merge into one node
                    next_node,index = self.merge(node, last_elem_index-1, last_elem_index - 1, last_elem_index)
                    last_elem_index = index


                #then we will travel down the node to continue to find the predecessor
                largest_elem = self.find_biggest(next_node,element)
                # decrement the child after it has deleted the element
                node.number_child[last_elem_index] -= 1
                return largest_elem
            else:
                # if the next node does not have minimum elements then they will continue to traverse down
                largest_elem = self.find_biggest(next_node,element)
                #decrement the child after it has deleted the element
                node.number_child[last_elem_index]-= 1
                return largest_elem

    def find_smallest(self,node,element,original_node):

        #if the node is a leaf then we can pop the first key in the node as its the smallest in the subtree
        if node.leaf:
            if not node.check_min():
                smallest_elem = node.key.pop(0)
                node.count-=1
                return smallest_elem
        else:
            #always get the first element as it's the smallest
            next_node = node.child[0]
            #if the next node we want to step on has minimum amount of elements then we will do a case 3a or 3b
            if next_node.check_min():
                # the right sibling will always be 1 as the left node is at the 0 position
                right_sibling = node.child[1]

                if not right_sibling.check_min():
                    # take smallest from right sibling since it has an element to spare
                    next_node = self.rotate_right(right_sibling,node,0,next_node)

                else:
                    # merge the nodes since right sibling has no element to spare
                    next_node,index = self.merge(node, 0, 0, 1)

                smallest_elem = self.find_smallest(next_node, element, original_node)

                node.number_child[0] -= 1
                return smallest_elem
            else:
                #if the next node was not at minimum elements then it will go down to the next node
                smallest_elem  = self.find_smallest(next_node,element,original_node)

                node.number_child[0] -= 1
                return smallest_elem


    def insert_rec(self,elements):
        for i in range(len(elements)):
            self.insert_element(elements[i],self.root)


    def insert_element(self,element,node:Node):

        #if the current node we are on is a leaf, and it is not a full node

        if node.leaf and (not node.check_reach_max()):
            index = binary_search(node.key,element)
            self.add_element(element,index,node)


            return
        else:
            #when the node we are entering is a full node, in this case its usually the root node
            #as usually when we go to down a node, we will check before stepping in

            if node.check_reach_max():

                if node.root:
                    #need to make a new node where it will increase the height of the btree
                    new_node = Node(self.degree,root=True)
                    #find the median key of the current node and pull it up
                    median = node.count//2

                    middle_element = node.key[median]
                    #and add it into the new node
                    self.add_element(middle_element,0,new_node)


                    #denode this node as the new root of the tree
                    self.root = new_node
                    #right node
                    right_node = Node(self.degree)

                    right_element = node.key[median+1:]
                    right_node.key = right_element
                    #update the count
                    right_node.count = len(right_element)

                    #now the current node we are standing on will be the left node of the tree
                    node.key = node.key[:median]

                    #it will no longer be the root
                    node.root = False
                    node.count = len(node.key)

                    #if the root node previous had child nodes then we need to relink all child nodes base on the
                    #split nodes
                    if not node.leaf:

                        #split the left and the right child according to the median
                        right_node.child = node.child[median+1:]
                        node.child = node.child[:median+1]


                        #update the number of subtree under the node
                        right_node.number_child = node.number_child[median+1:]
                        node.number_child = node.number_child[:median + 1]

                        #calculate the total keys in the left subtree of the root
                        #and the right subtree of the root
                        left_tree_amount = sum(node.number_child)+node.count
                        right_num_amount = sum(right_node.number_child) +right_node.count

                        #add it into the subtree storage of the node
                        new_node.number_child.append(left_tree_amount)
                        new_node.number_child.append(right_num_amount)

                        #since the node previously is not a leaf so after it split, it also won't be a leaf
                        right_node.leaf = False


                    else:

                        new_node.number_child.append(node.count)
                        new_node.number_child.append(right_node.count)

                    new_node.leaf = False

                    #add the left and right child of the new node into the child list of the new node
                    new_node.child.append(node)
                    new_node.child.append(right_node)

                    #binary search from the root again to see which node to go next
                    next_position = binary_search(new_node.key,element)
                    next_node = new_node.child[next_position]

                    self.insert_element(element, next_node)


                    #after finishing inserting update the length of the subtree
                    counter = new_node.number_child[next_position]
                    new_node.number_child[next_position] = counter+1



            #if the node we are on is not full
            elif not node.check_reach_max():
                #then it will find the next node that it needs to travel to
                position = binary_search(node.key,element)
                next_node = node.child[position]

                #if the next node we are traveling to travel to is not full then it will go down the node
                if not next_node.check_reach_max():

                    self.insert_element(element,next_node)
                    #increment the subtree amount after inserting
                    counter = node.number_child[position]
                    node.number_child[position] = counter + 1

                else:

                    #internal node needs to go up
                    #find the median of the keys and add it to the current node we are standing on
                    median = len(next_node.key)//2
                    middle_element = next_node.key[median]
                    self.add_element(middle_element,position,node)


                    #create a new node to store all right elements of the next node
                    right_node = Node(self.degree)
                    right_element = next_node.key[median+1:]

                    #the next_node will be the left node
                    next_node.key = next_node.key[:median]

                    right_node.key = right_element

                    #update the number of keys in the node
                    next_node.count = len(next_node.key)
                    right_node.count = len(right_element)


                    node.child.insert(position+1, right_node)

                    #add it into the lists first and later update accordingly
                    node.number_child.insert(position+1,right_node.count)


                    #relink all the child
                    if not next_node.leaf:

                        right_node.number_child = next_node.number_child[median+1:]
                        next_node.number_child = next_node.number_child[:median+1]



                        #split the child node of the next node since its node a leaf node
                        right_node.child = next_node.child[median+1:]
                        next_node.child = next_node.child[:median+1]

                        right_node.leaf = False

                        # calculate the total number of subtrees for left and right
                        total_num_left = sum(next_node.number_child)+next_node.count
                        total_num_right = sum(right_node.number_child) + right_node.count

                        #then it will update the amount accordingly
                        node.number_child[position] = total_num_left
                        node.number_child[position+1] = total_num_right

                    else:
                        #if it was a leaf node then the total amount of the subtrees will be the numbers of keys in that
                        #node
                        node.number_child[position] = next_node.count
                        node.number_child[position+1] = right_node.count


                    #after merging up we then binary search again then go down to the next node
                    position = binary_search(node.key,element)

                    next_node = node.child[position]
                    #continue to traverse down
                    self.insert_element(element,next_node)

                    #when com back from inserting then increment the amount of the subtree
                    counter = node.number_child[position]
                    node.number_child[position] = counter+1

                    return

        return
