import numpy
from math import log
from scipy import spatial

#One-time use code for creaing a relation similarity matrix from
#a relation list and a triples list
#This implementation follows the description in
#"Finding Streams in Knowledge Graphs to Support Fact Checking"

triple_file = open('train2id.txt','r')
relation_file = open('relation2id.txt','r')

r = int(relation_file.readline())
t = int(triple_file.readline())

print(t)
print(r)

C = numpy.zeros([r, r])
triple_array = numpy.zeros([t,3])

#Read data
for i in range(0,t):
	line = triple_file.readline()
	triple_array[i][0] = int(line.split('\t')[0])
	triple_array[i][1] = int(line.split('\t')[1])
	triple_array[i][2] = int(line.split('\t')[2])

print(triple_array)

#Create the adjacency matrix for the relations from the graph
for i in range(0,r):
	print(i)
	for j in range(0,t):
		if triple_array[j][2] == i:
			for k in range(0,t):
				if triple_array[k][0] == triple_array[j][0] and triple_array[k][2] != i:
					C[i][int(triple_array[k][2])] += 1
				if triple_array[k][1] == triple_array[j][1] and triple_array[k][2] != i:
					C[i][int(triple_array[k][2])] += 1
				if triple_array[k][0] == triple_array[j][1] and triple_array[k][2] != i:
					C[i][int(triple_array[k][2])] += 1
				if triple_array[k][1] == triple_array[j][0] and triple_array[k][2] != i:
					C[i][int(triple_array[k][2])] += 1

print(C)

C_1 = numpy.zeros([r,r])

idf = numpy.zeros([r])

#Calculate IDF for each column in the matrix
for j in range(0,r):
	count = 0
	for i in range(0,r):
		if C[i][j] > 0:
			count += 1
	if count > 0:
		idf[j] = log(r/float(count))

print(idf)

#Create C' by applying TF-IDF weighing to C
for i in range(0,r):
	print("Calculating tf-idf for row"+str(i))
	for j in range(0,i + 1):
		tf = log(1 + C[i][j])
		C_1[i][j] = tf * idf[j]
		C_1[j][i] = tf * idf[i]

print(C_1)

#Find the relation similarity for for matrix[i][j]
#as the cosine similarity of the i-th and j-th rows oc C'
rs = numpy.zeros([r,r])
for i in range (0,r):
	print('Calculating rs for '+str(i))
	for j in range(0,i + 1):
		rs[i][j] = 1 - spatial.distance.cosine(C_1[i], C_1[j])
		rs[j][i] = rs[i][j]

print(rs)

numpy.save('relsim1.npy',rs)

triple_file.close()
relation_file.close()

print(loadedArray.shape)