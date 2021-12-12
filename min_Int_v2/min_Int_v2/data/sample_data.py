import bnlearn as bn
import numpy as np
import pandas as pd

N = 5000 # number of samples
bif_file = './insurance.bif' # input bif with distribution
dict_file = './vdic.npy' # save variable and states mapping dict
data_file = './insurance.dat' # output file
csv_file = './insurance.csv' # data csv file

# parse bif file with data
with open(bif_file) as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]
lines = lines[2:]
i = 0
vdict = {}
while lines[i][0:8] == 'variable':
    line = lines[i]
    j = 9
    while line[j] != ' ':
        j += 1
    vname = line[9:j]
    line  = lines[i+1]
    s = line[line.find("{")+1:line.find("}")]
    s = s.replace(" ","")
    states = s.split(',')
    vdict[vname] = states
    i += 3
np.save(dict_file,vdict)
    
# load bif file with bnlearn
model = bn.import_DAG(bif_file)
# sample data
df = bn.sampling(model,n=N)
df.to_csv(csv_file)
# save sampled data to file
key = list(df.keys())
val = np.array(df)
fd = open(data_file, 'w')
for v in key[0:-1]:
    fd.write(str(v)+',')
fd.write(key[-1]+'\n')
for r in val:
    for var,val in zip(key[0:-1],r[0:-1]):
        fd.write(vdict[var][val] + ',')
    fd.write(vdict[key[-1]][r[-1]] + '\n')
fd.close()
