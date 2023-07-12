# Amino acid sequence of the protein given as input
seq = 'SGFRKMAFPSGKVEGCMVQVTCGTTTLNGLWLDDTVYCPRHVICTAEDMLNPNYEDLLIRKSNHSFLVQAGNVQLRVIGHSMQNCLLRLKVDTSNPKTPKYKFVRIQPGQTFSVLACYNGSPSGVYQCAMRPNHTIKGSFLNGSCGSVGF'

# Each amino acid is represented by a single letter symbol
# Ala - A
# Cys - C	
# Asp - D	
# Glu - E	
# Phe - F
# Gly - G
# His - H
# Ile - I
# Lys - K
# Leu - L
# Met - M
# Asn - N
# Pro - P
# Gln - Q	
# Arg - R
# Ser - S
# Thr - T
# Val - V	
# Trp - W	
# Tyr - Y

u = 1
# Stored propensity values of each amino acid residue for alpha - helix in a dictionary
p_helix = {
    'E': 1.53, 'A': 1.45, 'L': 1.34, 'H': 1.24, 'M': 1.20,
    'Q': 1.17, 'W': 1.14, 'V': 1.14, 'F': 1.12, 'K': 1.07,
    'I': 1.00, 'D': 0.98, 'T': 0.82, 'S': 0.79, 'R': 0.79,
    'C': 0.77, 'N': 0.73, 'Y': 0.61, 'P': 0.59, 'G': 0.53
}

# Stored propensity values of each amino acid residue for beta - strand in a dictionary
p_strand = {
    'M': 1.67, 'V': 1.65, 'I': 1.60, 'C': 1.30, 'Y': 1.29,
    'F': 1.28, 'Q': 1.23, 'L': 1.22, 'T': 1.20, 'W': 1.19,
    'A': 0.97, 'R': 0.90, 'G': 0.81, 'D': 0.80, 'K': 0.74,
    'S': 0.72, 'H': 0.71, 'N': 0.65, 'P': 0.62, 'E': 0.26
}

# Propensity values of each amino acid residue in the sequence for alpha - helix in a list
prop_helix = [p_helix.get(a,0) for a in seq]

# Propensity values of each amino acid residue in the sequence for beta - strand in a list
prop_strand = [p_strand.get(a,0) for a in seq]

# Initialize helix and strands lists with Z
# Z represents the absence of helix or strand (we could have used any other symbol as well)
# helix is a list that keeps track of where helices are in the sequence
# strands is a list that keeps track of where strands are in the sequence
helix = []
strands = []
for i in range(len(seq)):
    helix.append("Z")
    strands.append("Z")


# Function definitions

# Extend helices and strands to the left and right
def extend(start, end, structure, seq, p_helix, p_strand, helix, strands):

    start = start - u
    end = end + u
    threshold = 4
    
    # Loop to extend the helix or strand to the left
    while start >= 0:

        # Adding one amino acid at a time to the left of the window
        site = ""
        for k in range(4):
            site += seq[start+k]

        # This will store the sum of propensities of the amino acids in the site
        sum_helix = 0

        for j in site:

            # If the structure is helix, we will use the helix propensity values
            if structure == "helix":
                sum_helix += p_helix.get(j, 0)

            # If the structure is strand, we will use the strand propensity values
            else:
                sum_helix += p_strand.get(j, 0)
        

        # If the sum of propensities is >= 4, we will extend the helix to the left
        if sum_helix >= threshold:
            if structure == "helix":
                helix[start] = 'H' 
                start -= u

        # If the sum of propensities is >= 4, we will extend the strand to the left
            elif structure == "strand":
                strands[start] = 'S'
                start -= u

        # If the sum of propensities is < 4, we will stop extending the helix or strand
        elif sum_helix < threshold:
            break


    # Loop to extend the helix or strand to the right
    while end < len(seq):

        # Adding one amino acid at a time to the right of the window
        site = ""
        for k in range(4):
            site += seq[end-k]

        # This will store the sum of propensities of the amino acids in the site
        sum_strand = 0

        for j in site:
            
            # If the structure is helix, we will use the helix propensity values
            if structure == "helix":
                sum_strand += p_helix.get(j, 0)

            # If the structure is strand, we will use the strand propensity values
            else:
                sum_strand += p_strand.get(j, 0)
        

        # If the sum of propensities is >= 4, we will extend the helix to the right
        if sum_strand >= threshold:
            if structure == "helix":
                helix[end] = 'H'
                end += u
        # If the sum of propensities is >= 4, we will extend the strand to the right
            elif structure == "strand":
                strands[end] = 'S'
                end += u

        # If the sum of propensities is < 4, we will stop extending the helix or strand
        elif sum_strand < threshold:
            break


# Function that prints the secondary structure
def print_secondary_structure(seq, secondary_structure):
    for i in range(5):
        print()

    print("Sequence: ", end="  ")
    print("".join(seq))
    print("Structure: ", end=" ")
    print("".join(secondary_structure))

    for i in range(5):
        print()


# Function to find overlaps between helices and strands
def finding_overlaps(seq, helix, strands, p_helix, p_strand):

    # Creating a list to store the secondary structure of the protein
    # Initially, all residues are marked as "-" which means that they are not part of a helix or a strand
    # If a residue is part of a helix, it will be marked as "H"
    # If a residue is part of a strand, it will be marked as "S"
    secondary_structure = ["-"] * len(seq)
    
    # Initializing the index variable to iterate through the sequence
    i = 0
    
    # Loop through the sequence
    while i < len(seq):

        # If the current residue is part of a helix, mark it as a helix in the secondary structure list
        if helix[i] == "H" and strands[i] == "Z":
            secondary_structure[i] = "H"
        
        # If the current residue is part of a strand, mark it as a strand in the secondary structure list
        elif helix[i] == "Z" and strands[i] == "S":
            secondary_structure[i] = "S"
        
        # If the current residue is part of a helix and a strand, determine the overlap between the two structures

        elif helix[i] == "H" and strands[i] == "S":

            # Find the index of the next residue that is not part of a helix
            ind_h = next((p for p in range(i, len(helix)) if helix[p] != "H"), len(helix))
            
            # Find the index of the next residue that is not part of a strand
            ind_s = next((k for k in range(i, len(strands)) if strands[k] != "S"), len(strands))
            
            # Determine the sequence overlap between the helix and the strand
            overlap = seq[i:min(ind_h, ind_s)]
            
            # Calculate the score of the overlap in the helix and the strand using the propensity values
            score_h = sum(p_helix.get(aa, 0) for aa in overlap)
            score_s = sum(p_strand.get(aa, 0) for aa in overlap)
            
            # Determine if the overlap is more likely to be part of a helix or a strand and mark the corresponding residues
            if score_s >= score_h:
                secondary_structure[i:min(ind_h, ind_s)] = ["S"] * len(overlap)

            else:
                secondary_structure[i:min(ind_h, ind_s)] = ["H"] * len(overlap)
                
            
            # Update the index variable to skip over the residues that were just marked
            i = min(ind_h, ind_s)
            continue
        
        # If the current residue is not part of a helix or a strand, leave it marked as a dash
        i = i + u
    
    # Return the final secondary structure
    return secondary_structure




# Finding helix nucleation sites and updating the helix list
# We iterate through the sequence using a sliding window of size 6
# len(seq)-5 ensures that the final window has 6 amino acids
for i in range(len(seq)-5):
    
    # The current window of 6 amino acids
    window = seq[i:i+6]
    
    # Storing the propensities for each amino acid in the window
    helix_formers = [p_helix.get(aa, 0) for aa in window]
    
    # Counting the number of amino acids in the window that have a propensity >= 1
    num_helix_formers = sum([1 for x in helix_formers if x >= 1])
    
    # If there are 4 or more helix-forming amino acids in the window, mark the entire window as a helix

    if num_helix_formers >= 4:
        # set the 6 amino acids in the window to "H" to label them as a helix
        helix[i:i+6] = ["H"] * 6
        
        # Call the extend function to extend the helix to the left and right
        extend(i, i+5, "helix", seq, p_helix, p_strand, helix, strands)


# Find strand nucleation sites and update the strands list
# We iterate through the sequence using a sliding window of size 5
# len(seq)-4 ensures that the final window has 5 amino acids
for i in range(len(seq)-4):

    # The current window of 5 amino acids
    window = seq[i:i+5]

    # Storing the propensities for each amino acid in the window in a list
    strand_formers = [p_strand.get(aa, 0) for aa in window]

    # Counting the number of amino acids in the window that have a propensity >= 1
    num_strand_formers = sum([1 for x in strand_formers if x >= 1])

    # If there are 3 or more strand-forming amino acids in the window, mark the entire window as a strand
    if num_strand_formers >= 3:
        # set the 5 amino acids in the window to "S" to label them as a strand
        strands[i:i+5] = ["S"] * 5

        # Call the extend function to extend the strand to the left and right
        extend(i, i+4, "strand", seq, p_helix, p_strand, helix, strands)



# Finding the secondary structure of the protein using the function defined above
secondary_structure = finding_overlaps(seq, helix, strands, p_helix, p_strand)

# Printing the secondary structure using the function defined above
print_secondary_structure(seq, secondary_structure)
