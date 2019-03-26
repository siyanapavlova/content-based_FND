import numpy

#One-time use code for creating the adjacency matrix for testing KnowledgeStream
ent = open('./ks_train_plus_test_triples/entity2id.txt','r')
trip = open('./ks_train_plus_test_triples/train2id.txt','r')

entities = int(ent.readline())

triples = int(trip.readline())

adjacencyM = numpy.zeros([triples, 3])
for i in range(0, triples):
	line = trip.readline()
	sub = int(line.split('\t')[0])
	obj = int(line.split('\t')[1])
	pred = int(line.split('\t')[2])
	adjacencyM[i][0] = sub
	adjacencyM[i][1] = obj
	adjacencyM[i][2] = pred


numpy.save('adjacency_test+train.npy',adjacencyM)

loadedArray = numpy.load('adjacency_test+train.npy')
print(loadedArray)

ent.close()
trip.close()

print(loadedArray.shape)