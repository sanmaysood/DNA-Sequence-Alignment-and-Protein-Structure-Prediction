# IQB ASSIGNMENT 1
# Q3 - Local Alignment


#function to find the maximum of four numbers
def max4(w,x,y,z):
    if w >= x and w >= y and w >= z:
        return w
    elif x >= w and x >= y and x >= z:
        return x
    elif y >= w and y >= x and y >= z:
        return y
    else:
        return z  
    
# function to find the optimal alignments
#parameters: alignment_a and alignment_b are the strings that will be printed as the optimal alignments
#i and j are the indices of the current cell in the pointer matrix


def optimal_alignments(alignment_a, alignment_b, i, j):     

    if Pointer[i][j] == 0:              # Stop when you reach a cell with value 0
        print(alignment_a[::-1])        # print the alignment_a string after reversing it
        print(alignment_b[::-1])        # print the alignment_b string after reversing it
        print("Score:", Score[max_i][max_j])   # print the score of the alignment
        print()
        return

    elif Pointer[i][j] == 9:        # if the current cell is reached from the cell to the left of it
        optimal_alignments(alignment_a + '-', alignment_b + b[j-1], i, j-1)  # add a gap to the alignment_a string and add the character at the current index of the b string to the alignment_b string

    elif Pointer[i][j] == 8:        # if the current cell is reached from the cell above it 
        optimal_alignments(alignment_a + a[i-1], alignment_b + '-', i-1, j) # add a gap to the alignment_b string and add the character at the current index of the a string to the alignment_a string

    elif Pointer[i][j] == 7:        # if the current cell is reached from the cell diagonally above and to the left of it 
        optimal_alignments(alignment_a + a[i-1], alignment_b + b[j-1], i-1, j-1) # add the character at the current index of the a string to the alignment_a string and add the character at the current index of the b string to the alignment_b string

    elif Pointer[i][j] == 17:       # if the current cell is reached from the cell above it or the cell to the left of it (9 + 8)
        optimal_alignments(alignment_a + a[i-1], alignment_b + '-', i-1, j)
        optimal_alignments(alignment_a + '-', alignment_b + b[j-1], i, j-1)

    elif Pointer[i][j] == 16:       # if the current cell is reached from the cell diagonally above and to the left of it or the cell to the left of it (7 + 9)
        optimal_alignments(alignment_a + '-', alignment_b + b[j-1], i, j-1)
        optimal_alignments(alignment_a + a[i-1], alignment_b + b[j-1], i-1, j-1)

    elif Pointer[i][j] == 15:       # if the current cell is reached from the cell diagonally above and to the left of it or the cell above it (7 + 8)
        optimal_alignments(alignment_a + a[i-1], alignment_b + '-', i-1, j)
        optimal_alignments(alignment_a + a[i-1], alignment_b + b[j-1], i-1, j-1)

    elif Pointer[i][j] == 24:       # if the current cell is reached from the cell diagonally above and to the left of it or the cell above it or the cell to the left of it (7 + 8 + 9)
        optimal_alignments(alignment_a + a[i-1], alignment_b + b[j-1], i-1, j-1)
        optimal_alignments(alignment_a + '-', alignment_b + b[j-1], i, j-1)
        optimal_alignments(alignment_a + a[i-1], alignment_b + '-', i-1, j)


# main program
a = 'GATGCGCAG'  # input sequence 1
la = len(a)     # length of sequence 1

b = 'GGCAGTA'   # input sequence 2
lb = len(b)     # length of sequence 2

# scoring scheme
match = 2 
mismatch = 1
gap = 3

# initialize the score matrix and pointer matrix with 0
Score = [[0 for i in range(lb+1)] for j in range(la+1)]

Pointer = [[0 for i in range(lb+1)] for j in range(la+1)]


# initialize the first row and first column of the pointer matrix with 8 and 9 respectively
# 8 means that the cell is reached from the cell above it
# 9 means that the cell is reached from the cell to the left of it
# 7 means that the cell is reached from the cell diagonally above and to the left of it

for i in range(la+1):
    Pointer[i][0] = 8

for j in range(lb+1):
    Pointer[0][j] = 9

# fill the score matrix and pointer matrix using the recurrence relation
# the recurrence relation is:
# Score[i][j] = max(Score[i-1][j-1] + match if a[i] == b[j]     else Score[i-1][j-1] - mismatch, 
#                   Score[i-1][j] - gap, 
#                   Score[i][j-1] - gap,
#                   0)

for i in range(la):
    for j in range(lb):

        if a[i] == b[j]:    # if the two characters are equal, assign the match score to t0
            t0 = Score[i][j] + match  
        else:
            t0 = Score[i][j] - mismatch     # if the two characters are not equal, assign the mismatch score to t0

        t1 = Score[i][j+1] - gap        # assign the gap score to t1
        t2 = Score[i+1][j] - gap        # assign the gap score to t2

        final_value = max4(t0, t1, t2,0)  # find the maximum value among the four values

        Score[i+1][j+1] = final_value   # assign the maximum value to the current cell

        if t0 == final_value:       
            Pointer[i+1][j+1] += 7  # if the maximum value is obtained from the diagonal cell, add 7 to the pointer matrix

        if t1 == final_value:
            Pointer[i+1][j+1] += 8  # if the maximum value is obtained from the cell above the current cell, add 8 to the pointer matrix

        if t2 == final_value:
            Pointer[i+1][j+1] += 9  # if the maximum value is obtained from the cell to the left of the current cell, add 9 to the pointer matrix

# printing the score matrix and pointer matrix
print("Score Matrix")
for i in range(la+1):
    for j in range(lb+1):
        print(f"{Score[i][j]:3}", end=" ")
    print()

print()
print()

print("Pointer Matrix")
for i in range(la+1):
    for j in range(lb+1):
        print(f"{Pointer[i][j]:3}", end=" ")
    print()

print()
print()

# printing the optimal alignments
print("Optimal Alignments")

# finding index of maximum value in the score matrix
max_value = 0
for i in range(la+1):
    for j in range(lb+1):
        if Score[i][j] > max_value:
            max_value = Score[i][j]
            max_i = i
            max_j = j
        
optimal_alignments(" ", " ", max_i, max_j)  # calling the optimal_alignments function with the index of the maximum value in the score matrix
