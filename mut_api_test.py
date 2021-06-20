import requests

mut_5x5 = ['ATGCGA', 'CAGTGC', 'TTATGT', 'AGAAGG', 'CCCCTA', 'TCACTG']
mut_8x8 = ['ATGCGAGT', 'CAGTGCAA', 'TTATGTTG', 'AGAAGGCA', 'CCCCTAGT', 'TCACTGGA', 'CATGCATG', 'CAGACAGA']
mut_5x5_no = ['GCTAGC', 'ATTGCT', 'AGTCGT', 'GTCTCT', 'CACAGG', 'GCGTAT']
mut_5x5_bad = ['1CTAGC', 'GCT', 'AGTCGT', 'GTCTCT', 'CACAGG', 'GCGTAT']

res = requests.post('http://localhost:5000/mutant/', json={"dna":mut_5x5})
print(res.status_code, res.text)
