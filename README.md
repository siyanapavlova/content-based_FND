This is my Honours Project for my BSc Computing Science at the University of Aberdeen

System Requirements

64-bit Linux/Ubuntu machine
15GB RAM

Dependencies

• Python 2.7 or higher 2.x version
• Python 3.5 or higher 3.x version
• OpenKE 1 - no need to download this as it comes as a part of the project files
• KnowledgeStream 2 - no need to download this either as it comes as a part of the project files
too. However, you will need to download the original KnowledgeStream test data 3 if you
intend to use it.
• Stanford CoreNLP
• MongoDB
• Python packages
– pip and pip3 or easy_install - for installing new packages
– pandas
– numpy
– sklearn
– requests
– bs4
– pymongo
– nltk
– pycorenlp
– neuralcoref

Running the System

1. Start your mongoDB instance with parameters mongod –nojournal –dbpath /path/to/mongo
replacing /path/to/mongo with the path where you have installed mongod

2. Navigate to the folder where you have installed CoreNLP. Start the CoreNLP server with
the command
java -mx8g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -annotators "tok-
enize,ssplit,pos,lemma,parse,sentiment" -port 9000 -timeout 30000

3. Navigate to the main project folder and start the system with python3 main.py
