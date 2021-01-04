# --- Warpyn ---
import numpy as np

def createStandardVector(num_states, specific_int):
    standard_vector = np.zeros((num_states,1))
    standard_vector[specific_int-1][0] = 1
    return standard_vector

def giveStandardVectorNumber(array):
    for index in range(len(array)):
        if array[index][0] == 1:
            return index+1

def backToChordsTwoDim(num_array, chord_array):
    chord_cycle = num_array.copy()
    for i in range(0, len(num_array)):
        for j in range(0, len(num_array[i])):
            state = num_array[i][j]
            curr_chord = chord_array[state-1]
            chord_cycle[i][j] = curr_chord

    return chord_cycle

def chordProgMult(str_prog2, str_prog1):
    # --- Section 1: Convert Input to Arrays ---
    # the numbers 1 and 2 refer to the order of multiplication aka R -> L here
    prog1 = str_prog1.split(' ')
    prog2 = str_prog2.split(' ')

    # Section 1.5: If there are repeating chords in any progression, then return an error message.

    if len(prog1) != len(set(prog1)):
        return "Invalid Input: Duplicate Chords Found"
    if len(prog2) != len(set(prog2)):
        return "Invalid Input: Duplicate Chords Found"
    if len(prog1) == 0 or len(prog2) == 0:
        return "Invalid Input: No Progression Detected"

    # --- Section 2: Rewriting Progressions with Integers aka Cycle Notation ---
    unique_chord_num = 0
    int_prog1 = []
    int_prog2 = []
    all_chords = []

    for chord1 in prog1:
        if all_chords.count(chord1)==0:
            unique_chord_num += 1
            int_prog1.append(unique_chord_num)
            all_chords.append(chord1)

        else:
            int_prog1.append(all_chords.index(chord1)+1)

    for chord2 in prog2:
        if all_chords.count(chord2)==0:
            unique_chord_num += 1
            int_prog2.append(unique_chord_num)
            all_chords.append(chord2)
        else:
            int_prog2.append(all_chords.index(chord2)+1)

    # --- Section 3: Creating Permutation Matrices ---
    matrixp1 = np.zeros((unique_chord_num, unique_chord_num))
    matrixp2 = np.zeros((unique_chord_num, unique_chord_num))

    # for Progression 1
    for index in range(0,unique_chord_num):
        col_num = index + 1
        if int_prog1.count(col_num) > 0:
            next_index = (int_prog1.index(col_num) + 1)%len(int_prog1)
            # print(next_index)
            next_state = int_prog1[next_index]
            matrixp1[next_state-1][index] = 1
        else:
            matrixp1[index][index] = 1

    # for Progression 2
    for index in range(0,unique_chord_num):
        col_num = index + 1
        if int_prog2.count(col_num) > 0:
            next_index = (int_prog2.index(col_num) + 1)%len(int_prog2)
            # print(next_index)
            next_state = int_prog2[next_index]
            matrixp2[next_state-1][index] = 1
        else:
            matrixp2[index][index] = 1

    # --- Section 4: Identify a Standard Basis Vector From an Integer ---
    # (done with other functions)

    # --- Section 5: Multiplication Process ---
    numbers_left = []
    for index in range(1,unique_chord_num+1):
        numbers_left.append(index)

    current_state = numbers_left[0]

    totalmatrix = matrixp2.dot(matrixp1)

    all_product_cycles = []
    current_cycle = []

    while (len(numbers_left) >= 0):
        if (len(numbers_left) == 0):
            all_product_cycles.append(current_cycle)
            current_cycle = []
            break
        elif (current_cycle.count(current_state) > 0):
            all_product_cycles.append(current_cycle)
            current_cycle = []
            current_state = numbers_left[0]
        else:
            current_cycle.append(current_state)
            numbers_left.remove(current_state)
            state_vector = createStandardVector(unique_chord_num, current_state)
            next_vector = totalmatrix.dot(state_vector)
            # print(next_vector)
            next_state = giveStandardVectorNumber(next_vector)
            current_state = next_state

    # --- Section 6: Convert Simplified Integer Cycles Back to Chords ---
    # (made function)
    final_decomp = backToChordsTwoDim(all_product_cycles, all_chords)

    # --- Section 7: Return Final Cycles in Cycle Notation as a String ---
    final_decomp_str = ""

    for end_cycle in final_decomp:
        final_decomp_str += "("
        for end_chord in end_cycle:
            final_decomp_str += end_chord
            if end_cycle.index(end_chord) == len(end_cycle)-1:
                final_decomp_str += ")"
            else:
                final_decomp_str += " "

    return final_decomp_str
