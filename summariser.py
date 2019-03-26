from models import db

#Make default summary from title and text
def makeDefaultSummary(title, text):
	if len(text.split('. ')) >= 2:
		summary = title + '. ' + '. '.join(text.split('. ')[0:2]) + '.'
	else:
		summary = title + '. ' + text
	return summary

#Main summarise function. Summarises all articles in db that do not have a summary
def summarise():
	count = 0
	total = db['_article'].find({'defaultSummary':None}).count()
	print('Summarising %s articles' %(total))
	for article in db['_article'].find({'defaultSummary':None}):
		if article['body'] != None and article['title'] != None:
			count += 1
			print('Article %s / %s' % (count,total))
			summary = makeDefaultSummary(article['title'],article['body'])
			out = db['_article'].update_one({'articleId': article['articleId']}, {'$set':{'defaultSummary':summary}})
			# print("Created default summary for article ", article['title'])