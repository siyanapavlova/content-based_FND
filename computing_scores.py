import glob
import csv

#One-time use code for calculating the average and max scores for test data for KnowledgeStrem
#Results saved in scores_file_avg.csv and scores_file_max.csv accordingly
def get_positive_scores():
	with open('scores_file_avg.csv', 'w') as avg_fileWrite:
		fieldnames = ['score','class']
		avg_writer = csv.DictWriter(avg_fileWrite, fieldnames=fieldnames)
		with open('scores_file_max.csv', 'w') as max_fileWrite:
			max_writer = csv.DictWriter(max_fileWrite, fieldnames=fieldnames)

			scores_file_avg = open('scores_file_avg.csv','w')
			scores_file_max = open('scores_file_max.csv','w')

			print("Getting positive scores")
			in_path = './kstreamnew/output/400pos/*.csv'
			txt_list = glob.glob(in_path)
			for article in txt_list:
				print(article)
				with open(article, 'r') as csvfile:
					readCSV = csv.reader(csvfile, delimiter=',')
					count = 0
					max_score = 0
					total = 0
					for row in readCSV:
						if(row[6] != 'score'):
							total += float(row[6])
							count += 1
							if float(row[6]) > max_score:
								max_score = float(row[6])
				avg_writer.writerow({'score':total/float(count),'class':1})
				max_writer.writerow({'score':max_score,'class':1})

			print("Getting negative scores")
			in_path = './kstreamnew/output/400neg/*.csv'
			txt_list = glob.glob(in_path)
			for article in txt_list:
				print(article)
				with open(article, 'r') as csvfile:
					readCSV = csv.reader(csvfile, delimiter=',')
					count = 0
					max_score = 0
					total = 0
					for row in readCSV:
						if(row[6] != 'score'):
							total += float(row[6])
							count += 1
							if float(row[6]) > max_score:
								max_score = float(row[6])
				avg_writer.writerow({'score':total/float(count),'class':0})
				max_writer.writerow({'score':max_score,'class':0})

if __name__ == "__main__":
	get_positive_scores()

