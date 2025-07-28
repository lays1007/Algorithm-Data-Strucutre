
class Trie:
    """
    This is a data structure where it can store strings for efficient string retrival
    """
    def __init__(self):
        """
        Function description: To initialise a trie with the possible amount of characters that will exist and initiliase
        space for the number of character


        :Input:
            None

        :Output, return or postcondition: None


        :Time complexity: = O(1)
        :Time complexity analysis: When iniliasing the space with Node class it despite it being 63 it will also be
        constant time as the input will also be 63 so the complexity will be O(1)


        :Auxiliary Space complexity: O(1)
        :Auxiliary Space complexity analysis: It will be O(1) as the array will always have a fix size of 63
        therefore, it will still be constant so O(1)

        """
        self.root = Node(63)
        self.unique_words = 0

    def get_index(self,character):
        """
        Function description: Takes in a character and finds its ascii value to determine the position of the characters
        index in the Node .link attribute array


        :Input:
            None

        :Output, return or postcondition: None


        :Time complexity: = O(1)
        :Time complexity analysis: O(1) as comparing integers with another integer is constant time and doing
        arithmetic operation is also O(1)


        :Auxiliary Space complexity: O(1)
        :Auxiliary Space complexity analysis: O(1) as storing value into variable like index which is a single value
        would only require O(1) auxiliary space complexity.

        """
        ascii = ord(character)
        index = None
        if ascii >= 48 and ascii <= 57:
            index = ascii - 47
        elif ascii >= 65 and ascii <= 90:
            index = ascii - 54
        elif ascii >= 97 and ascii <= 122:
            index = ascii - 60
        return index

    def insert_recur(self,key,data):
        """
        Function description: Inserts the word into the trie using a helper function
        insert_recur_aux to manage the recursive calls.


        :Input:
            key: the key that will to where the data will be stored at
            data: the data that will be stored in the key node

        :Output, return or postcondition: None

        N : the number of characters in the input word which is key in this case
        :Time complexity: = O(N)
        :Time complexity analysis: O(N) as when it calls insert_recursive aux function then it in aux function
        it will call itself until it reaches the last character of the key and store the data
         into the leaf node which is the terminal



        :Auxiliary Space complexity: O(N)
        :Auxiliary Space complexity analysis: O(N) it will use O(N) extra space as when insert_recur_aux it will store all
        the character into the trie.

        """
        current = self.root
        self.insert_recur_aux(current,key,data,level =0)


    def insert_recur_aux(self,current,key,data,level):
        """
        Function description: A recursive function that will call itself until all character
        in the input has been stored in the trie and when upon returning from the recursive call it will return
        some of the words attributes like the frequency, index and id of the word and add it into the current nodes
        next_node list which is a list of potential words it can return when it has to autocorrect.

        Approach description: It will first store all the characters in the input words one by one in the trie by recursively
        calling itself until it reached the end of the word then it will store the whole word in the leaf node which is
        at index =0. Upon coming back from the recursive call it will return the frequency of the word that has been
        input, the index of the character and will add it into the current nodes attribute call next_node where it stores
        the potential words that it will go to if the user input this character. But the list that is store in next_node attribute
        will always be at most 3 elements so when it already consists of 3 elements then if the value has a higher priority
        then the one in the list that has the least priority then it will take its place.

        :Input:
            current: current node
            key: the key that will to where the data will be stored at
            data: the data that will be stored in the key node
            level: current level the trie is at

        :Output, return or postcondition:
            frequency, index, id
            frequency: the frequency of the word appearing in the trie
            index: the index that the character is in the trie
            id: the id of the word to identify if the word is the same word or different

        N : the number of characters in the input word which is key in this case
        :Time complexity: = O(N)
        :Time complexity analysis: Complexity is O(N) as it will call itself N times for it to reach the end of the word
        and store the word in the leaf node. When return back from the recursive call it will add the return value and
        add it into next_node O(1) list and sort the next_node list. Each node will have a next_node list where it will have
        at most 3 elements as the list consist of the tuple where it stores the frequency, index and id of the current
        character. Therefore, even though sorting will take O(m log m) where it m is the number of elements in next_node list
        but since the next_node list will have at most 3 elements it means that it has an upper bound which make the sort()
        operation constant O(1). So the overall complexity will be O(N).



        :Auxiliary Space complexity: O(N)
        :Auxiliary Space complexity analysis: O(N) it will use O(N) extra space as when insert_recur_aux it will store all
        the character into the trie. When returning back from the recursive call it will also take the return value and
        store the current node next_node attribute. Which will take extra space but since the next_node attribute list
        will always be at most 3 element it means that it has an upper bound of 3 so, therefore it will be constant space.
        So O(N) for storing all the characters in the trie will still be the dominating complexity so overall
        space complexity is O(N)

        """
        if len(key) == level:
            index = 0

            if current.link[0] is not None:
                current = current.link[index]
                # the word already exist
                current.frequency+=1
            else:
                # create a new node
                current.link[0] = Node(63)
                current = current.link[index]
                current.frequency += 1
                self.unique_words+=1
                current.id = self.unique_words

            current.data = data

            return current.frequency, index, current.id

        else:

            index = self.get_index(key[level])
            level+=1

            if current.link[index] is not None:
                current = current.link[index]
                next_node = self.insert_recur_aux(current,key,data,level)

            else:
                # create a new node
                current.link[index] = Node(63)
                current = current.link[index]
                next_node = self.insert_recur_aux(current,key,data,level)

            current.add_word(next_node)
            current.next_node.sort(key=lambda node: (-node[0],node[1]))
            current.frequency = next_node[0]

            return next_node[0],index,next_node[2]



    def search_rec(self,key):
        """
        Function description: search the word into the trie using a helper function
        search_recur_aux to manage the recursive calls if lists_word return None means the
        word exist in the trie and if it does not exist in the trie but some characters match it will return
        at most 3 potential words to be autocorrect to.


        :Input:
            key: the word that needs to be found in the trie


        :Output, return or postcondition: None
        M: the length of the string input
        U: the total number of characters in the correct output

        When No words match string or word actually exist in trie:

        :Time complexity: = O(M)
        :Time complexity analysis: When no words match or the word exist in the trie
        then search_recur_aux() have a complexity of O(M) where it will just recursively call itself and if all words match or
        no words match then it will return back from the recursive call and return a None or an empty list.

        :Auxiliary Space complexity: O(1)
        :Auxiliary Space complexity analysis: As there are no match words it means that it will not require extra space
        to store the suggested correct words as there are no match so O(1)

        When word don't exist in trie but some characters match the words in the trie:

        :Time complexity: = O(M+U)
        :Time complexity analysis: When called the recursive function search_recur_aux(), it will have a complexity of
        O(M+U) as it will first recursively call itself O(M) until it meets the end of the string or an unmatch character.
        When it does not have a match string then it will find its potential words which will be O(U)  and return a
        list of words which will at most be 3.


        :Auxiliary Space complexity: O(U)
        :Auxiliary Space complexity analysis: O(U) it will require extra O(U) space for the correct words that will be contained
        in the list to return to the check() function.


        """
        current = self.root
        lists_words = self.search_recur_aux(current, key, 0)
        if lists_words is None:
            return []
        else:
            return lists_words


    def search_recur_aux(self, current, word, level, previous=False):
        """
        Function description: A recursive function that will call itself until all it has either found the input character.
        If it does not find the input character it will then return the top 3 suggested words based on the prefix of the input
        string, the frequency it occurs in the trie and last is based on lexicographical order by calling search_correct()
        function and if the list already has 3 elements then it will return the list of suggested words.

        Approach description: It will recursively call itself until it reach the end of the word or reaches a character
        that does not match the characters in the trie. When it reaches the end of the word, and it has a terminal node
        which is in index 0 then it means the word exist and it will return a None. If it reaches the end of the string, and
        it does not have a terminal node then it will return a [] list then it will search for the potential words
        that can be return. If when halfway through recursive calling itself and the character does not match it will
        return a [] and find the potential words and add it into the empty list. The way to find the potential words
        it will get the index by calling get_next_index() and it will follow the index that is store in the tuple and recursively
        go down to the leaf node according to the index that has been given by get_next_index() to see which is the next_node
        in the .next_node attribute in the node.
        Last case is when all the character don't match any of the characters in the trie then it will also return a []

        :Input:
            current: current node
            word: word to be search/autocorrect
            level: current level the trie is at
            previous: to check if previous input characters are previously match

        :Output, return or postcondition:
            list - a list that contains top 3 suggested words
            None - when the words/prefix does not exist in the trie

         M: the length of the string input
         U: the total number of characters in the correct output

        When No words match string or word actually exist in trie:

        :Time complexity: = O(M)
        :Time complexity analysis: When there are no string match there the character or the word
        does not exist in the trie then it will just recursively call itself until the end of
        string and when coming back from the recursive calls it find if any of the characters
        in the input word matches with characters in the trie. If no match then it will just return an empty list. So the
        complexity will be O(M).

        :Auxiliary Space complexity: O(1)
        :Auxiliary Space complexity analysis: As there are no match words it means that it will not require extra space
        to store the suggested correct words as there are no match so O(1)


        When word don't exist in trie but some characters match the words in the trie:

        :Time complexity: = O(M+U)
        :Time complexity analysis: After recursively calling itself O(M) until it reaches the end of the input string
        of meets a character that does not match with the words in the trie. It will call will loop at most three times
        for each node when coming back from the recursive call and when looping it will loop through all the potential
        words that can be autocorrect to and retrieve that words and when retrieving it by calling search_correct()
        each time we retrieve it is going to be O(N) where N is the number of character in the correct word. So when it reaches
        3 elements it means it has already run O(U) times to retrieve all the correct words that will be autocorrect to then
        it will return back the word list with the top 3 word suggestion that it can autocorrect to.

        :Auxiliary Space complexity: O(U)
        :Auxiliary Space complexity analysis: O(U) it will require extra O(U) space for the correct words that will be contained
        in the list to return to the check() function.

        """

        if len(word) == level:

            if current.link[0] is not None:
                current = current.link[0]

                #the word exist in the file so does not need to be autocorrect
                if current.data is not None:

                    return None

            else:
                # word ended but no terminal node means it needs to autocorrect
                return []
        else:
            index = self.get_index(word[level])

            level+=1

            if current.link[index] is not None:
                previous = current
                current = current.link[index]
                search = self.search_recur_aux(current, word, level, True)

                if search is None:
                    return None
                else:
                    # search for all the possible autocorrect
                    if len(search) ==3:
                        return search
                    else:

                        current_char = previous.link[index]
                        for i in range(current_char.number_word):
                            if len(search) < 3:

                                if current_char.exist():
                                    return search
                                else:

                                    search_word = self.search_correct(previous.link[index])
                                    if search_word is not None:
                                        search.append(search_word)
                    return search
            else:
                #if previous string did not match then continue to call
                if previous == False:
                    search = self.search_recur_aux(current, word, level)
                    return search
                else:
                    #previously characters have match so return an empty list to store all the potential words
                    return []





    def reset_all(self,word):
        """
        Function description: Go through all the alphabet in the input to reset its nodes
        to next_index to its default value so that the search_correct function can be reuse later to find the
        3 words that needs to be suggested for autocorrect.


        :Input:
        word: the word that needs to be reset in the trie


        :Output, return or postcondition: None

        char: the number of characters in the input
        :Time complexity: = O(char) it will be O(char) as it will have to loop through all the characters
        of the input word and get the index of the character and reset its Node object to default value
        :Time complexity analysis: O(char) it will be O(char) as it will have to loop through all the characters
        of the input word and get the index of the character and reset its Node object to default value


        :Auxiliary Space complexity: O(1)
        :Auxiliary Space complexity analysis: looping through all the character to change its attribute
        to default value which is 0 does not require extra space so O(1)

        """
        current = self.root
        for character in word:
            index = self.get_index(character)
            if index != None:
                if current.link[index] is not None:
                    current.reset()

                    current = current.link[index]
        current.reset()



    def search_correct(self,current):
        """
         Function description: Search for the suggested word to be autocorrect to recursively  and return the word

         Approach description: It will first check if number_word is 0 it means there is no other potential words which
         means it is at the leaf node so it can retrieve the word from the trie. Else it will check if the word already exist
         in the list or not by calling .exist() where if the next_index integer is already the same length as the next_node
         list it means it already has been traverse here previously. If it does not exist then it will get the index
         for then info of the next potential word that is store in next_node attribute of the node by calling get_next_index()
         then it will recursively call itself until it reach the leaf node.

         :Input:
         current: a node object where it holds the potential words that it can go to for autocorrect suggestion



         :Output, return or postcondition: word_return (returns a word) / None

         char: the number of characters in the input
         :Time complexity: = O(char) it will recursively call itself O(char) times
         until the end of the suggested word so it will be
         O(char) and return back the word.


         :Auxiliary Space complexity: O(1)
         :Auxiliary Space complexity analysis: recursively calling itself to find the leaf node and retrieve the word
         will not use any extra space so it will be O(1)

         """
        if current.number_word == 0:

            return current.data
        else:


            if current.exist() == False:

                index = current.get_next_index()
                next = current.next_node[index]
                #index for the next word
                word = next[1]
                next_node = current.link[word]
                word_return = self.search_correct(next_node)
                return word_return
            else:
                # if exist in list already
                return None


class Node:
    """
    Node class is to store of the attributes of the trie node to keep track of certain information when we insert or search
    """
    def __init__(self,size=63,item=None):
        """
            Function description: To initialise a node object it requires the size which will be the possible number of
            characters to initialise the array to store the data later.


            :Input:
                size: the size of the link array
                item: the data that wants to be stored in this node

            :Output, return or postcondition: None

            size: the number in the size input
            :Time complexity: = O(size)
            :Time complexity analysis: the size will always be O(size) in this case which means to initialise the space
            it takes O(size) times and assigning value to a attribute is O(1) so overall complexity will be o(size)

            :Auxiliary Space complexity: O(size)
            :Auxiliary Space complexity analysis: When initialising the array it will take up O(size) extra space
            while the other attribute will at most take O(1) space so overall complexity is O(size)

        """
        self.id = None
        self.frequency = 0
        self.link = [None]*size
        self.data = item
        self.next_node = []
        self.number_word = 0
        self.next_index = 0


    def reset(self):
        """
            Function description: To reset the next_index attribute to 0 which is the default value so that
            it can autocorrect for another word later


            :Input:
                None

            :Output, return or postcondition: None


            :Time complexity: = O(1)
            :Time complexity analysis: assigning an integer to an object attribute is a constant operation

            :Auxiliary Space complexity: O(1)
            :Auxiliary Space complexity analysis: Assigning a single value to an attribute does up any extra space so its
            O(1)

        """
        self.next_index = 0

    def add_word(self,item):
        """
        Function description: add tuple which contains consist of its frequency, index, and id (to identify the word) into
        the next_node attribute, which will contain the at most 3 words when the user input a word that does not exist

        Approach description: It will first loop through all the words in the next_node attribute to check if the word
        is already in the list and if it is it will just replace with the new tuple as it means it has updated its frequency
        and return. If it is not in the list and the list still does not have 3 elements it will be added into the list.
        If there is 3 words in the next_node list then it will first loop through the elements in next_node to find the
        value with the least priority which is (have a lesser frequency, higher ascii value). After finding the value
        which have a lesser frequency or higher ascii value then it will compare it with the input element
        if the input element has a higher priority (higher frequency or lower ascii value) then the input will replace
        the into its position.


        :Input:
            None

        :Output, return or postcondition: None


        :Time complexity: = O(1)

        :Time complexity analysis: O(1) Even though it will always loop through the number_word that is in the next_node list
        so it will be O(N) where N is the number of element in the list. However, next_node list will always have at most
        3 elements in the list. So since it is either fixed size of 3 or lesser, the loop will always run a constant
        number of times as it will have an upper bound of 3.

        :Auxiliary Space complexity: O(1)
        :Auxiliary Space complexity analysis: next_node list will either contains a fixed size of 3 at most
        or lesser means that the means that the space used by the list will not grow with the side of the input
        unless it has not reached its upper bound which is 3.

        """

        for i in range(self.number_word):
            element = self.next_node[i]
            # if same word, so just update the frequency
            if item[2] == element[2]:
                self.next_node[i] = item
                return


        #it not in the list yet
        if self.number_word<3:
            self.next_node.append(item)
            self.number_word+=1
        else:

            minimum,index = self.find_min()

            if minimum[0] < item[0]:
                self.next_node[index] = item
            elif minimum[0] == item[0]:
                # if frequency same, then check alphabet
                if minimum[1] > item[1]:
                    self.next_node[index] = item

    def exist(self):
        """
        Function description: to check if the there are any more words that is not in the list of words that will be return
        to check function

        Approach description: To check if the word is already in the words list is to see if it has already been traverse.
        so if the next_index attribute has already reached the length of the list then it means all the words in next_node
        is already in the list.

        :Input:
            None

        :Output, return or postcondition: Boolean - to indicate if all the next_node element words already exist in the
        word list.


        :Time complexity: = O(1)

        :Time complexity analysis: O(1) as comparing integer is constant operation

        :Auxiliary Space complexity: O(1)
        :Auxiliary Space complexity analysis: comparing integer does not require extra space therefore, is O(1)

        """
        if self.number_word == 1:
            if self.next_index>0:
                return True
            else:
                return False
        if self.next_index >= self.number_word:
            return True
        else:
            return False

    def get_next_index(self):
        """
        Function description: Return the index that it needs to travel to get the next word suggested word for autocorrect
        :Input:
            None

        :Output, return or postcondition: index - the next index where the next word will be


        :Time complexity: = O(1)

        :Time complexity analysis: Assigning a single integer value and incrementing the value is constant operation
        therefore, O(1).

        :Auxiliary Space complexity: O(1)
        :Auxiliary Space complexity analysis: O(1) assigning a single value integer to a variable is constant space and
        incrementing an integer does not require extra space so its O(1).


        """
        index = self.next_index
        self.next_index+=1
        return index


    def find_min(self):
        """
        Function description: called when the next_node list is full and requires to find the element
        with the least priority which is has a lesser frequency, higher ascii value and return the element and its index
        where it is place in the list.


        :Input:
            None

        :Output, return or postcondition:
        minimum: element that has the least priority which is has a lesser frequency, higher ascii value
        minimum_index: the index where the minimum element is place in next_node list


        :Time complexity: = O(1)

        :Time complexity analysis: O(1) Even though it will always loop through the number_word that is in the next_node list
        so it will be O(N) where N is the number of element in the list. However, next_node list will always have at most
        3 elements in the list. So since it is either fixed size of 3 or lesser, the loop will always run a constant
        number of times as it will have an upper bound of 3. In addition, comparing integer value with each other is also
        constant operation O(1). So overall complexity is O(1).

        :Auxiliary Space complexity: O(1)
        :Auxiliary Space complexity analysis: when looping through a list it does not require any extra space and assigning
        a single value to a variable is constant space so O(1).

        """

        minimum = self.next_node[0]
        minimum_index = 0
        for i in range(1,self.number_word):

            #check frequency
            if minimum[0]>self.next_node[i][0]:
                minimum = self.next_node[i]
                minimum_index = i
            elif minimum[0] == self.next_node[i][0]:

                # if frequency same, then ascii value
                if minimum[1]<self.next_node[i][1]:
                    minimum = self.next_node[i]
                    minimum_index = i


        return minimum,minimum_index


class SpellChecker:
    """
    A class where it takes a file as an input and, it can help check if the input needs to be autocorrect or not based on
    user's previous message sent which is the file.
    """

    def __init__(self, file):
        """
        Function description: To initialise the spell checker by accepting a file input and initialising a trie to store
        all the words in the file.

        Approach description: First take the string in the file and filter out all the non-alphanumeric symbol and each time
        if there is a non-alphanumeric symbol then it will be viewed as a seperator. To check if its non-alphanumeric symbol
        it will call the function .get_index which it then returns None then it means it is a non-alphanumeric symbol.
        After filtering out all the non-alphanumeric symbol, then it will insert all the words one by one into the trie.

        :Input:
            file: text file name

        :Output, return or postcondition:
            None

        T : The total number of characters in the text_file
        :Time complexity: = O(T)
        :Time complexity analysis: Initialising a trie will be a constant operation as it will always have 63 nodes so
        O(63) is constant. and it will then loop through the lines in the file and loop through the characters in the of the line
        the complexity of it would be O(N*M)  where N is the number of lines in the file and M is the number of characters
        in the line which can also be written as O(T) as we loop all the characters in the file.
        And when it meets a symbol like ?,>,* etc. Then it will join all the word together and, it will be one
        word, and it will then be appended into all_word list. Join complexity will be O(j) where j will be the number of
        characters than needs to be joined together. In worse scenario it will be O(T) when it does not have a seperator.
        After removing all the symbols in and appending the words into the all_word list then it will loop through the
        list which will be O(number of words in the list) and insert it into the trie which will be O(T) to insert all the
        words into the trie. So the most dominating complexity is O(T) compared to others so it is O(T).

        :Auxiliary Space complexity: O(T)
        :Auxiliary Space complexity analysis: When we filter out all the non-alphanumeric symbol then it will use at most
        O(T) if all the characters in the file does not have a seperator and when we insert the words into the trie it will
        also take up O(T) space. So it is O(T) extra space.

        """

        self.file = open(file,"r")
        self.trie = Trie()
        word = []
        all_word = []

        for line in self.file:

            for character in line:
                index = self.trie.get_index(character)
                if index is None:
                    if word:
                        all_word.append(''.join(word))
                        word = []
                else:
                    word.append(character)

        if word:
            all_word.append(''.join(word))


        for i in range(len(all_word)):
            self.trie.insert_recur(all_word[i],all_word[i])
        self.file.close()




    def check(self,input):
        """
        Function description: To check if the word exist, if it does not exist or exist then it will return an []. But if
        some of the characters match some of the characters in the trie but not all then it will return a list of words
        where it will be at most 3 where the list contains words that it can potentially be autocorrect to.

        Approach description:

        :Input:
           input: a single string word

        :Output, return or postcondition:
            list: either empty or a list with at most 3 potential words that the input can be corrected to

        When No words match string or word actually exist in SpellChecker:

        :Time complexity: = O(M)
        :Time complexity analysis: When there are no string match there the character or the word
        does not exist in the SpellChecker then it will just recursively call itself until the end of
        string and when coming back from the recursive calls it find if any of the characters
        in the input word matches with characters in the trie. If no match then it will just return an empty list. So the
        complexity will be O(M).

        :Auxiliary Space complexity: O(1)
        :Auxiliary Space complexity analysis: As there are no match words it means that it will not require extra space
        to store the suggested correct words as there are no match so O(1)


        When word don't exist in trie but some characters match the words in the SpellChecker:

        :Time complexity: = O(M+U)
        :Time complexity analysis: After recursively calling itself O(M) until it reaches the end of the input string
        of meets a character that does not match with the words in the trie. It will call will loop at most three times
        for each node when coming back from the recursive call and when looping it will loop through all the potential
        words that can be autocorrect to and retrieve that words and when retrieving it by calling search_correct()
        each time we retrieve it is going to be O(N) where N is the number of character in the correct word. So when it reaches
        3 elements it means it has already run O(U) times to retrieve all the correct words that will be autocorrect to then
        it will return back the word list with the top 3 word suggestion that it can autocorrect to. Upon returning from
        the search_rec() call it will reset all the nodes that has been return back into lists which will have a
        complexity of O(U) as it will search through each character of the correct word list and reset its nodes
        to default setting so that the check/search_rec can be reuse again for other words. So it will be O(M+2U) which can
        be simplified to O(M+U)

        :Auxiliary Space complexity: O(U)
        :Auxiliary Space complexity analysis: O(U) it will require extra O(U) space for the correct words that will be contained
        in the list and resetting the correct words node back to its default setting does not require any extra space so O(1).
        So overall it will be O(U).

        """

        output = self.trie.search_rec(input)
        #reset all the value
        for i in range(len(output)):
            word = output[i]

            self.trie.reset_all(word)
        return output
