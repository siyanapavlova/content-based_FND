from summariser import summarise
from newsFetcher import fetchAll
from tripleProduction import addTriples
from modelGeneration import generateModel

#Make main menu
def main_menu():
	print("What would you like to do?\n")
	print("1. Fetch articles\n")
	print("2. Get summaries of current articles\n")
	print("3. Add new triples\n")
	print("4. Generate model\n")
	print("5. Exit\n")
	print("Please choose an option 1 - 5")

#Define quit
def quit():
	raise SystemExit

#Define invalid inpit function
def invalid():
	print("Invalid selection. Press any key to restart.")

if __name__ == "__main__":
	#Main loop
	while True:
		main_menu()
		choice = input('\n[1-5] --> ')

		#Option '1' for fetching new articles
		if choice == '1':
			print('\nRunning Fetcher...')
			fetchAll()
			print('\nDone!\n')
		#Option '2' for summarising articles in db
		elif choice == '2':
			print('\nRunning Summariser...')
			summarise()
			print('\nDone!\n')
		#Option '3' for extracting triples
		elif choice == '3':
			print('\nRunning Triple Extraction...')
			addTriples()
			print('\nDone!\n')
		#Option '4' for generating an embedding model
		elif choice == '4':
			print('\nRunning Model Generation')
			generateModel("d")
			print('\nDone!\n')
		#Option '5' to exit the program
		elif choice == '5':
			print("\nExiting...")
			quit()
		#Invalid input. Try again
		else:
			invalid()
			choice = input(' --> ')
