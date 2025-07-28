def z_algorithms(string):
    length_str = len(string)

    # initializing a z-array for the string
    z_array = [None]*length_str

    #the first position will store the length of the string
    z_array[0] = length_str

    #the right most of the z-box will start with from 0 which means there is no z-box for now
    right_z = 0

    #k is the index where it will start to compare from
    k=1
    for i in range(1,length_str):

        index_one = 0
        index_two = i

        # the character is in the z-box then it will take k and store it into t z-arrya as the z-value
        if i<=right_z:

            #take the z-value from the position where it compare
            z_value = z_array[k]
            remaining = right_z-i+1

            #if the remaining values in the z-box is more than the z-value it means it
            # can copy its z-array values as they are the same characters
            if z_value<remaining:
                k+=1
                z_array[i] = z_value

            #if the z-value is the same as the remaining characters that has not have a z-value in the z-array
            #then it will have to do explicit comparison after the z-box to see if there potentially be a match

            elif z_value==remaining:
                k=1

                index_one = z_value
                index_two = remaining+i


                checked_string = check_string(string, index_one, index_two)
                box_length = checked_string[0]


                z_array[i] = box_length
                if box_length > 0:
                    right_z = checked_string[1] - 1

                z_array[i] = remaining+box_length
            elif z_value>remaining:
                z_array[i] = remaining
                k += 1

        #if the character is outside the z-box then it will have to do explicit comparison
        elif i>=right_z:


            k= 1
            #check to see how long the string matches, and it will return the length of the match string with is the length of the z-box
            checked_string = check_string(string,index_one, index_two)
            box_length = checked_string[0]

            # then it will store it to its box length which is the z-value into the z-array according to iteration number
            #which is where the matching string starts
            z_array[i] = box_length

            # if there is a match then it will store the right position of the z-box which is where the match ends
            if box_length >0:

                right_z = checked_string[1] -1

    return z_array


def check_string(string,index_one,index_two):
    box_length = 0
    # use to check if the characters in the string is the same as the pattern
    # if it's the same the box length will increase
    while index_two < len(string) and string[index_one] == string[index_two]:

        box_length += 1
        index_one += 1
        index_two += 1

    return box_length,index_two
