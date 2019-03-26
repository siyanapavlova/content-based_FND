import uuid
from models import db
from datetime import datetime

# Define Article class.
# Used for creating Article objects
# for upload to MongoDB
class Article(object):
	def __init__(self,url):
		self.title=None
		self.body=None
		self.url=url
		self.articleId=str(uuid.uuid4())
		self.source=None
		self.datePublished=None
		self.extracted = False
		self.defaultSummary = None
		self.metadata={
		    'createdDate':datetime.now(),
		    'createdBy':'fetcher',
		    'updatedDate':datetime.now(),
		    'updatedBy':'fetcher'
		}

		pass