
valid_chars = ('A', 'T', 'C', 'G')  # Letras validas en secuencia
seq_len = 4  # Longitud de la secuencia a buscar
verbose = False


def check_content(mutmatrix):
    result = all(all(char in valid_chars for char in row) for row in mutmatrix)
    return result


def check_type(mutarray):
    result = (
        (type(mutarray) == list) and 
        (all(type(word) == str for word in mutarray)) and
        (len(mutarray) >= seq_len) and
        (all(len(word) == len(mutarray) for word in mutarray))
    )
    return result


def split_upper(word):
    return list(char.upper() for char in word)


def to_matrix(mut):
    if check_type(mut):
        mutmatrix = list(split_upper(word) for word in mut)
        if check_content(mutmatrix):
            return mutmatrix
    return False


def rot90(mutmatrix):
    mut_90_matrix = [[mutmatrix[j][i] for j in range(len(mutmatrix))] for i in range(len(mutmatrix[0]))]
    return mut_90_matrix


def rot45(mutmatrix):
    dim_array = len(mutmatrix[0])
    dist = dim_array - seq_len
    mut_45_matrix = []
    for diag in range(-dist, dist+1, 1):
        mut_45_row = []
        for index,row in enumerate(mutmatrix):
            if index+diag < 0: continue
            if index+diag > dim_array - 1: break
            mut_45_row.append(row[index+diag])
        mut_45_matrix.append(mut_45_row)
    return mut_45_matrix


def find_match(mutmatrix):
    for row in mutmatrix:
        for start_index in range(len(row) - seq_len + 1):
            seq = row[start_index:start_index+seq_len]
            result = all(elem == seq[0] for elem in seq)
            if verbose: print(seq,': ', sep='', end='')
            if verbose: print(result)
            if result: return result
    return result


def is_mut(mutarray):

    mutmatrix = to_matrix(mutarray)
    if not mutmatrix:
        raise TypeError("ADN Sequence Incorrect")

    match = find_match(mutmatrix)
    if verbose: print(f"Horizontal: {match}\n")

    if not match:
        match = find_match(rot90(mutmatrix))
        if verbose: print(f"Vertical: {match}\n")

    if not match:
        match = find_match(rot45(mutmatrix))
        if verbose: print(f"Diagonal: {match}\n")

    return match


if __name__ == '__main__':
    mut_5x5 = ['ATGCGA', 'CAGTGC', 'TTATGT', 'AGAAGG', 'CCCCTA', 'TCACTG']
    mut_8x8 = ['ATGCGAGT', 'CAGTGCAA', 'TTATGTTG', 'AGAAGGCA', 'CCCCTAGT', 'TCACTGGA', 'CATGCATG', 'CAGACAGA']
    mut_5x5_no = ['GCTAGC', 'ATTGCT', 'AGTCGT', 'GTCTCT', 'CACAGG', 'GCGTAT']

    try:
        result = is_mut(mut_5x5_no)
    except TypeError as e:
        print("Error:", e.args[0])
    else:
        msg = "Is Mutant!" if result else "Not mutant"
        print(f"Result: {msg}")
