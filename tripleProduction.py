import nltk
from pycorenlp import *
import collections
import pprint
from neuralcoref import Coref
import re
import pprint
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer
from models import db
import csv
import os

pp = pprint.PrettyPrinter(indent=4)

caps = "([A-Z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"
coref = Coref()

#Make sure sentence is in good format.
#Source code from: https://stackoverflow.com/questions/4576077/python-split-text-on-sentences/9047421#9047421 
def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + caps + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(caps + "[.]" + caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + caps + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences

#Resolve coreference in text using neuracoref
def neuralcorefIt(text):
	sentences = split_into_sentences(text)
	sentences[0] = sentences[0].capitalize()
	for s in sentences:
		if s[-1] == '?':
			sentences.remove(s)
	for i in range(1,len(sentences)):
		clusters = coref.one_shot_coref(utterances=sentences[i], context=sentences[i - 1])
		resolved_utterance_text = coref.get_resolved_utterances()
		sentences[i] = resolved_utterance_text[0].capitalize()
		# print(resolved_utterance_text)
	return ' '.join(sentences)

#Get present tense of verbs in triples using WordNetLemmatizer
def getPresentTense(triples):
	lmtzr = WordNetLemmatizer()
	for t in range(0, len(triples)):
		for i in range(0,len(triples[t])):
			for word in triples[t][i].split(" "):
				triples[t][i] = triples[t][i].replace(word, lmtzr.lemmatize(word,'v'))
	return triples

#Produce the triples for an article using StanfordCoreNLP and return the result
def produceTriples(text):
	triples = []
	processedText = neuralcorefIt(text)
	pp = pprint.PrettyPrinter(indent=4)
	#This is where my CoreNLP server is hosted.
	#It will be running throughout the evaluation time
	#In case there are any issues, you might want to run you own
	#CoreNLP server and replace the address here
	nlp=StanfordCoreNLP("http://35.227.120.108:9000/")

	output = nlp.annotate(processedText, properties={"annotators":"tokenize,ssplit,pos,lemma,depparse,natlog,openie,dcoref",
	                                 "outputFormat": "json","triple.strict":"true"})#, "openie.max_entailments_per_clause":"1"})

	result2 = []

	result = [output["sentences"][0]["openie"] for item in output]
	for i in range(0,len(output["sentences"])):
		result2.append(output['sentences'][i]['openie'])
	for i in range(0,len(result2)):
		for rel in result2[i]:
			subj = rel['subject']
			obj = rel['object']
			for ref in output['corefs']:
				if len(output['corefs'][ref]) > 1 and output['corefs'][ref][1]['position'][0] == i + 1:
					if output['corefs'][ref][1]['text'] == subj:
						subj = output['corefs'][ref][0]['text']

			relationSent=[subj,obj,rel['relation']]
			triples.append(relationSent)
	triples = getPresentTense(triples)
	return triples

#Create newsData folder if it doesn't exist
def createFolder():
	if not os.path.exists('newsData'):
		os.makedirs('newsData')

#Main triple extraction. Extract triples for all articles for which triples have not been extracted
def addTriples():
	createFolder()
	count = 0
	with open("openKE/benchmarks/newsData/textTriples.csv", 'a') as fileWrite:
		fieldnames = ['id','subject','object','predicate']
		writer = csv.DictWriter(fileWrite, fieldnames=fieldnames)
		total = db['_article'].find({'extracted':False}).count()
		print('Extacting triples from %s articles' % (total))
		for article in db['_article'].find({'extracted':False}).batch_size(50):
			count += 1
			print('Article %s / %s' % (count,total))
			if article['extracted'] == False and article['defaultSummary'] != None:
				triples = produceTriples(article['defaultSummary'])
				for triple in triples:
					writer.writerow({'id':article['articleId'],'subject':triple[0], 'object':triple[1], 'predicate':triple[2]})
			db['_article'].update({'_id':article['_id']},{'$set':{'extracted':True}})