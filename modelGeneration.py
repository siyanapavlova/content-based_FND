import csv
import os
import execnet

#Create files in format acceptable for OpenKE and save then in openKE/benchmarks/newsData
def createOpenkeFiles():
	count = 0

	entities2id = open('./openKE/benchmarks/newsData/entity2id.txt','w')
	triples2id = open('./openKE/benchmarks/newsData/train2id.txt','w')
	relation2id = open('./openKE/benchmarks/newsData/relation2id.txt','w')
	type_constrain = open('./openKE/benchmarks/newsData/type_constrain.txt','w')

	entities = []
	relations = []
	constrains = {}

	n = 0

	entities2id.write("               \n")
	relation2id.write("               \n")
	triples2id.write("               \n")

	with open('openKE/benchmarks/newsData/textTriples.csv', 'r') as csvfile:
	    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
	    for row in reader:
	    	count += 1
	    	if count < 28000:
		        print(count)

		        if row[1 - n] not in entities:
		        	entities.append(row[1 - n])
		        	entities2id.write(row[1 - n] + '	' + str(entities.index(row[1 - n])) + '\n')

		        if row[3 - n] not in relations:
		        	relations.append(row[3 - n])
		        	relation2id.write(row[3 - n] + '	' + str(relations.index(row[3 - n])) + '\n')
		        	head = [row[1 - n]]
		        	tail = [row[2 - n]]
		        	constrains[str(row[3 - n])] = {'head':head, 'tail':tail}
		        else:
		        	if row[1 - n] not in constrains[str(row[3 - n])]['head']:
		        		constrains[str(row[3 - n])]['head'].append(row[1 - n])
		        	if row[2 - n] not in constrains[str(row[3 - n])]['tail']:
		        		constrains[str(row[3 - n])]['tail'].append(row[2 - n])

		        if row[2 - n] not in entities:
		        	entities.append(row[2 - n])
	        		entities2id.write(row[2 - n] + '	' + str(entities.index(row[2 - n])) + '\n')

	        	triples2id.write(str(entities.index(row[1 - n])) + '	' + str(entities.index(row[2 - n])) + '	' + str(relations.index(row[3 - n])) + '\n')
	
	type_constrain.write(str(len(relations))+'\n')

	for key in constrains:
		# print(key)
		type_constrain.write(str(relations.index(key))+'\t')
		type_constrain.write(str(len(constrains[key]['head'])))
		for i in range(len(constrains[key]['head'])):
			type_constrain.write('\t'+str(entities.index(constrains[key]['head'][i])))
		type_constrain.write('\n')

		type_constrain.write(str(relations.index(key))+'\t')
		type_constrain.write(str(len(constrains[key]['tail'])))
		for i in range(len(constrains[key]['tail'])):
			type_constrain.write('\t'+str(entities.index(constrains[key]['tail'][i])))
		type_constrain.write('\n')
		# print(constrains[key])


	entities2id.seek(0)
	entities2id.write(str(len(entities)))

	relation2id.seek(0)
	relation2id.write(str(len(relations)))

	triples2id.seek(0)
	triples2id.write(str(count))

	entities2id.close()
	triples2id.close()
	relation2id.close()
	type_constrain.close()

#Calling a different python version.
#Needed because OpenKE is in Python2 and this project is in Python3
def call_python_version(Version, Module, Function, ArgumentList):
	gw = execnet.makegateway("popen//python=python%s" % Version)
	channel = gw.remote_exec("""
		from %s import % s as the_function
		channel.send(the_function(*channel.receive()))
	""" % (Module,Function))
	channel.send(ArgumentList)
	return channel.receive()

#Main model generation. Dummy variable needed as it is expected by call_python_function
#Calling OpenKE's 'example_train_transe.py' file which produces the embedding model
def generateModel(dummy):
	createOpenkeFiles()
	owd = os.getcwd()
	os.chdir('openKE/')

	call_python_version("2.7","example_train_transe","example", "d")

	os.chdir(owd)

	

