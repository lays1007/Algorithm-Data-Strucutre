
def boyer_moore(string,pat):
    comparison =0
    #list to store matching substring index position
    match_position = []

    #generate a 2 by pattern length size bad character table
    bad_suffix = generate_bad_suffix_table(pat,2)
    pat_len = len(pat) -1
    previous_mismatch = None
    galil_optimise = False

    matching_prefix, good_suffix_array = good_suffix(pat)
    last_char_pat = get_index(pat[pat_len])
    right_most_occur = bad_suffix[last_char_pat][pat_len]
    shift_more = False
    mismatch = 0
    extra_shift = 0

    # if the right most occurrence last character in the pattern excluding itself exist means there is a possibility
    # where we can shift more instead of constantly shifting one
    if right_most_occur is not None:

        shift_more = True
        extra_shift = (pat_len) - right_most_occur

    #initialise pointer for comparison later
    pat_pointer = pat_len
    start_pointer = pat_len
    moving_pointer = pat_len

    #initialise these variable in the case where galil optimisation when come to use
    previous_sp = -1
    start_skip_comp = -1
    stop_skip_comp = -1

    while True:

        # it will go through this code when the end point of the string is within the area where it has been compared
        # before in previous iteration
        if start_pointer - (pat_len) <= previous_sp:

            # if the pointer on the pattern is currently within the range of the stop and start index where previously
            # the matching suffix of the string has already compared then it will keep these index range between stop and start
            # point and continue comparing
                if pat_pointer == stop_skip_comp:
                    # if start skip_comp is 0 means that it can skip to the end of the string so it can call the
                    # good_suffix shift to compare the next set of substring
                    if start_skip_comp == 0:

                        moving_pointer = start_pointer - pat_len
                        match_position.append(moving_pointer + 1)
                        previous_sp, pat_pointer, previous_mismatch, start_pointer, moving_pointer, shift = found_match(good_suffix_array, pat, matching_prefix,
                                         start_pointer, string)

                        #if start pointer is None it means we cannot shift to the right anymore
                        if start_pointer is None:
                            break


                    else:

                        moving_pointer -= stop_skip_comp - start_skip_comp + 1
                        pat_pointer = start_skip_comp - 1

        if string[moving_pointer] == pat[pat_pointer]:

            comparison+=1

            # when we found a substring in the string that matches with the pattern
            if pat_pointer == 0:
                # add the matching position
                match_position.append(moving_pointer + 1)

                previous_sp, pat_pointer, previous_mismatch, start_pointer, moving_pointer,shift =\
                    (found_match(good_suffix_array, pat, matching_prefix, start_pointer,string))
                galil_optimise = True

                if start_pointer is None:
                    break

            else:
                # continue scanning through the text by decremented by 1, to check the whole substring
                pat_pointer-=1
                moving_pointer-=1

        else:
            # if there is a mismatch

            comparison+=1


            good_shift = get_shift_good(good_suffix_array, pat_pointer, pat, matching_prefix)
            bad_shift = get_bad_shift(bad_suffix,pat_pointer,string[moving_pointer])

            if pat_pointer < pat_len:
                #if there is a mismatch then the previous end point will store at the last matched string position
                previous_mismatch= pat_pointer
                galil_optimise = True
                previous_sp = start_pointer


            shift_amount = max(good_shift,bad_shift)



           #binary boyer moore optimisation where it will shift to the next occurrence of the last character in the
            if shift_more:

                if pat_len == pat_pointer:
                    mismatch+=1
                    if mismatch == extra_shift:
                        # if the shift amount computed with the bad character and good suffix is larger than we will
                        # take that shift amount instead of this shift amount
                        max_shift = max(shift_amount, extra_shift + 1)
                        if start_pointer + max_shift <= len(string) - 1:

                            start_pointer += max_shift
                            moving_pointer = start_pointer
                            mismatch = 0


                            continue
                        else:
                            break

            pat_pointer = pat_len
            # to check if we shift will it outside the range of string or still within if
            # its outside the range of the string then it will break the loop
            if start_pointer + shift_amount <= len(string)-1:
                 start_pointer += shift_amount
                 moving_pointer = start_pointer

            else:
                break

        # if previously there were match in the string then it will find the index of which index they should skip for the comparison
        if galil_optimise:
            if previous_mismatch is not None:
                if good_suffix_array[previous_mismatch+1] is not None:
                    start_skip_comp = good_suffix_array[previous_mismatch+1] - pat_len + previous_mismatch+1
                    stop_skip_comp = good_suffix_array[previous_mismatch+1]

                else:
                    start_skip_comp = 0
                    stop_skip_comp = matching_prefix[previous_mismatch+1]-1

                galil_optimise = False

    print("Number of comparison made: ",comparison)
    return match_position



def found_match(good_suffix_array,pat,matching_prefix,start_pointer,string):
    shift = 0
    shift_amount = get_shift_good(good_suffix_array, 0, pat, matching_prefix)

    previous_sp = start_pointer

    pat_pointer = len(pat)-1

    previous_mismatch = 0

    # before changing we shift we check if after we shift we will surpass the end of the string
    # if yes then it will break the loop or if not it will continue with the shift amount we computed
    if start_pointer + shift_amount <= len(string) - 1:
        start_pointer += shift_amount
        moving_pointer = start_pointer
        shift += shift_amount
    else:
        start_pointer = None
        moving_pointer = None

    return previous_sp, pat_pointer,previous_mismatch,start_pointer,moving_pointer,shift

def generate_bad_suffix_table(pat,number_char):

    # initialising the bad character table
    bad_array = [None]*number_char
    for j in range(len(bad_array)):
        bad_array[j] = [None]*len(pat)

    #the loop will loop through the pattern starting from the back to fill up the table with its right most occurrence
    # of the character
    for i in range(len(pat) - 1, -1, -1):

        index = get_index(pat[i])

        next_index = i + 1
        # loop to the right if the right position have not store the right most occurrence of the characters position
        while next_index != len(pat) and bad_array[index][next_index] is None:
            bad_array[index][next_index] = i
            next_index += 1

    return bad_array


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

            #take the z-value from the position where it compared
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

                # check to see how long the string matches, and it will return the length of the
                # match string with is the length of the z-box
                checked_string = check_string(string, index_one, index_two)
                box_length = checked_string[0]


                z_array[i] = box_length
                if box_length > 0:
                    right_z = checked_string[1] - 1

                z_array[i] = remaining+box_length

            # if the z_value bigger than the amount of remaining characters in the z-box then it will its z_value
            #will just be the remaining values they have left in the z box
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
    # if it's the same the z box length will increase
    while index_two < len(string) and string[index_one] == string[index_two]:
        box_length += 1
        index_one += 1
        index_two += 1

    return box_length,index_two

def get_bad_shift(bad_char_array,mismatch_index,letter):

    #k is the point of mismatch
    shift = 0
    index_char = get_index(letter)

    #rx is the right most occurrence of the character that cause the mismatch in the string
    rx = bad_char_array[index_char][mismatch_index]
    if rx is not None:
        shift = mismatch_index - rx

    #the minimum shift will be 1 or the bad character shift, we take the larger shift
    return max(1,shift)

def get_shift_good(suffix_array,k,string,match_prefix):

    #get the good shift from the good suffix from the position of after the mismatch
    #if there is no value then we take from the match prefix array
    string_length = len(string)
    if suffix_array[k+1] is not None:
        shift_position = string_length-suffix_array[k+1]-1

        return shift_position
    else:

        return string_length- match_prefix[k+1]


def good_suffix(pat):

    string = ""
    pat_length = len(pat)
    #initialise matching prefix array
    match_prefix =  [None]*(pat_length+1)
    #the last position of the match prefix always will be 0 as there are not matches
    match_prefix[pat_length] = 0

    #reverse the string so that we can get the z value in backward order when we reverse it back
    for i in range(pat_length-1,-1,-1): #O(m) m=pat
        string+=pat[i]


    z_array = z_algorithms(string)
    z_array.reverse()

    index = 0
    previous = 0
    #compute for match prefix array
    for k in range(pat_length-1, -1, -1):
        if z_array[index] > previous:

            match_prefix[k] = z_array[index]
            previous = z_array[index]
        else:
            match_prefix[k] = previous
        index+=1

    #initialising a good suffix array
    good_suffix_array = [None]*(pat_length+1)

    #calculating good suffix array
    for j in range(len(pat)-1):
        position = pat_length -z_array[j]
        good_suffix_array[position] = j

    return match_prefix, good_suffix_array


def get_index(char):
    # get the index of the binary character
    return ord(char)-48
