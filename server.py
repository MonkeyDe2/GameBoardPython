import select
import socket
import random
from tkinter import *
import time
from bs4 import BeautifulSoup
import requests



###SuperSecretPassword
###host:hoster
IP = "127.0.0.1"
PORT=1234
DISPLAY = False
WEB=True

### Create virtual deck
def CreateVirtualDeck():
	initialDeck = []

	ActionCards = {
		'Heart':6,
		'Bear':6,
		'HCON':6,
		'VCON':6,
		'AATK':8,
		'GATK':8,
		'ATK':2,
		'SAB':4,
		'IMP':6,
		'DEF':6,
		'ADEF':6,
		'GDEF':6,
		'BCK':6,
		'PEK':6,
		'OVR':2

	}

	for n in ActionCards:
		for x in range(ActionCards[n]):
			initialDeck.append(n)

	return initialDeck

def CreateDefaultBoard():
	return ['0','0','0','0','0','0','0','2','2','1']



### Remove from deck
def RemoveFromDeck(deck,card):
	deck.remove(card)
	if len(deck) > 0:
		return deck
	else:
		return CreateVirtualDeck()

### Initiate display using tkinter

class tkinterDisplay(Tk):

	def __init__(self,client,name):
		super().__init__()
		self.title(name)
		self.resizable(height=None,width=None)


		self.frame1 = Frame(self,padx=5,pady=5)
		self.frame1.grid(row=0,column=0)

		self.tit = Button(self.frame1,text=name,width=25,height=4,pady=3)

		self.box0 = Button(self.frame1,text="Soldiers:" + client[0],width=25,height=4)
		self.box1 = Button(self.frame1,text="Planes:" + client[1],width=25,height=4)
		self.box2 = Button(self.frame1,text="Ground Def:" + client[2],width=25,height=4)
		self.box3 = Button(self.frame1,text="Air Def:" + client[3],width=25,height=4)

		self.tit.grid(row=0,column=0,columnspan=2)
		self.box0.grid(row=1,column=0)
		self.box1.grid(row=1,column=1)
		self.box2.grid(row=2,column=0)
		self.box3.grid(row=2,column=1)

		self.frame2 = Frame(self,padx=5,pady=5)
		self.frame2.grid(row=1,column=0,columnspan=2)

		self.box4 = Button(self.frame2,text="Stone:" + client[4],width=20,height=10)
		self.box5 = Button(self.frame2,text="Wood:" + client[5],width=20,height=10)
		self.box6 = Button(self.frame2,text="Food:" + client[6],width=20,height=10)

		self.box4.grid(row=0,column=0)
		self.box5.grid(row=0,column=1)
		self.box6.grid(row=0,column=2)

		self.frame3 = Frame(self,padx=5,pady=5)
		self.frame3.grid(row=0,column=1)

		self.box7 = Button(self.frame3,text="Stone W:" + client[7],width=10,height=4)
		self.box8 = Button(self.frame3,text="Wood W:" + client[8],width=10,height=4)
		self.box9 = Button(self.frame3,text="Food W:" + client[9],width=10,height=4)
		
		self.box7.pack()
		self.box8.pack()
		self.box9.pack()

		self.update()

	def updateBoard(self,client):

		self.box0.configure(text="Soldiers:" + client[0])
		self.box1.configure(text="Planes:" + client[1])
		self.box2.configure(text="Ground Def:" + client[2])
		self.box3.configure(text="Air Def:" + client[3])
		self.box4.configure(text="Stone:" + client[4],highlightbackground = 'red')
		self.box5.configure(text="Wood:" + client[5],highlightbackground = 'yellow')
		self.box6.configure(text="Food:" + client[6],highlightbackground = 'blue')
		self.box7.configure(text="Stone W:" + client[7],highlightbackground='red')
		self.box8.configure(text="Wood W:" + client[8],highlightbackground = 'yellow')
		self.box9.configure(text="Food W:" + client[9],highlightbackground = 'blue')

		self.update()


### Update webpage
def websiteUpdater(x,n):

		newUnits = client[n][0]
		x += 1

		data = requests.get('http://localhost:5000')
		soup = BeautifulSoup(data.text,'html.parser')

		td = soup.find_all('td')
		nameId = str(x) + 'f'
		name = soup.find(id=nameId)
		print(nameId, name)
		name.string.replace_with(n)

		for line in td:
			if int(str(line)[8]) == x:
				if str(line)[9] == '1':
					line.string.replace_with("Soldiers: " + newUnits[0])
				if str(line)[9] == '2':
					line.string.replace_with("Planes: " + newUnits[1])
				if str(line)[9] == '3':
					line.string.replace_with("Stone: " + newUnits[7])
				if str(line)[9] == '4':
					line.string.replace_with("Ground Def: " + newUnits[2])
				if str(line)[9] == '5':
					line.string.replace_with("Air Def: " + newUnits[3])
				if str(line)[9] == '6':
					line.string.replace_with("Wood: " + newUnits[8])
				if str(line)[9] == '7':
					line.string.replace_with("Food: " + newUnits[9])
				if str(line)[9] == '8':
					line.string.replace_with("Stone: " + newUnits[4])
				if str(line)[9] == '9':
					line.string.replace_with("Wood: " + newUnits[5])
				if str(line)[9] == '0':
					line.string.replace_with("Food: " +newUnits[6])

		with open("templates/index.html","w") as file:
			file.write(str(soup))



############## Functions ##################

### Show cards
def ShowCard(client,user):
	cardsOnHands = client[user][1]
	if len(cardsOnHands) == 0:
		return None
	cardsOnHands = ",".join(cardsOnHands)
	return cardsOnHands

### Show board
def ShowBoard(client,user):
	board = client[user][0]
	board = ",".join(board)
	return board


### Draw from deck
def DrawCard(deck, user):
	randomCard = random.choice(deck)
	deck = RemoveFromDeck(deck, randomCard)
	return deck, randomCard

### HAK, add 1 to anything
def Hak1(newUnits,index):
	newUnits[index] = str(int(newUnits[index]) + 1)
	clientSocket.send(str("ADDED").encode('utf-8'))

### SUB, sub 1 to anything
def Sub1(newUnits,index):
	if int(newUnits[index]) > 0:
		newUnits[index] = str(int(newUnits[index]) - 1)
		clientSocket.send(str("SUBTRACTED").encode('utf-8'))
	else:
		clientSocket.send(str("Already 0").encode('utf-8'))

if __name__ == "__main__":
	currentDeck = CreateVirtualDeck()
	lobby = True
	client = {}

	### Create a socket listener
	socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socketServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
	socketServer.bind((IP,PORT))
	socketServer.listen()

	socketLists = [socketServer]

	while True:

		if lobby == True:

			readySocks,_,_ = select.select(socketLists,[],[])
			for sock in readySocks:
				if sock == socketServer:
					clientSocket, _ = socketServer.accept()

					command = clientSocket.recv(64)
					command = command.decode('utf-8')
					socketLists.append(clientSocket)

		### Create user data on server
		
			if command[:4] == 'USER':
				if command[4:] in client:
					print(str(command[4:]), 'ALREADY IN SERVER')
					command = ''
				else:
					client[command[4:]] = [CreateDefaultBoard(),[],clientSocket]
					print(str(command[4:]),"Joined the server")
					command = ''

				clientSocket.send(str("Waiting for players").encode('utf-8'))

			if len(client) >= 2:
				time.sleep(2)
				for n in client:
					client[n][2].send(str("Starting match now").encode('utf-8'))
					if DISPLAY == True:
						client[n][2] = tkinterDisplay(client[n][0],n)
				socketServer.close()

				### Create new socket listener
				socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				socketServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
				socketServer.bind((IP,PORT))
				socketServer.listen()
				

				lobby = False

			if lobby == True:
				print("Waiting for players")



		else:
			clientSocket, _ = socketServer.accept()
			command = clientSocket.recv(64)
			command = command.decode('utf-8')
			### Functions
			print(command)

			if command[:3] == 'CMD':
				currentUser = command[7:]
				currentAction = command[3:7]


				### Show cards
				if currentAction == 'SHOW':
					cardsOnHands = ShowCard(client,currentUser)
					board = ShowBoard(client,currentUser)
					
					if cardsOnHands == None:
						clientSocket.send(board.encode('utf-8'))
					else:
						together = board + 'z' +cardsOnHands
						clientSocket.send(together.encode('utf-8'))

				### Draw cards
				if currentAction == 'DRAW':
					currentDeck, randomCard = DrawCard(currentDeck, currentUser)
					client[currentUser][1].append(randomCard)
					clientSocket.send(randomCard.encode('utf-8'))
					print(str(currentUser),'drew a',str(randomCard))

				### Use a card
				if currentAction[:3] == 'USE':
					holding = client[currentUser][1]
					if len(holding) < int(currentAction[3]):
						clientSocket.send(str('Out Of Bounds').encode('utf-8'))

					else:
						usedCard = holding[int(currentAction[3])-1]
						print(usedCard)
					
						if usedCard != 'PEK':
							client[currentUser][1].pop(int(currentAction[3])-1 )
							clientSocket.send(str('Card Used').encode('utf-8'))
						else:
							allclients = []
							for n in client.keys():
								 if n != currentUser:
								 	allclients.append(n)
							print(allclients)
							clientSocket.send(str(allclients).encode('utf-8'))
							picked = clientSocket.recv(16)
							pickedHolding = client[allclients[int(picked.decode('utf-8'))-1]][1]
							random2 = random.sample(pickedHolding,2)
							print(random2)
							client[currentUser][1].pop(int(currentAction[3])-1 )
							clientSocket.send(str(random2).encode('utf-8'))


				### Add units
				if currentAction[:3] == 'ADD':
					newUnits = client[currentUser][0]

					### 1
					if currentAction[3] == '1':
						if int(newUnits[4]) >= 2 and int(newUnits[6]) >=1:
							newUnits[0] = str(int(newUnits[0]) + 1)
							newUnits[4] = str(int(newUnits[4]) - 2)
							newUnits[6] = str(int(newUnits[6]) - 1)
							clientSocket.send(str("Soldier Added").encode('utf-8'))
						else:
							clientSocket.send(str("Not enough resource").encode('utf-8'))

					### 2
					if currentAction[3] == '2':
						if int(newUnits[5]) >= 2 and int(newUnits[6]) >=1:
							newUnits[1] = str(int(newUnits[1]) + 1)
							newUnits[5] = str(int(newUnits[5]) - 2)
							newUnits[6] = str(int(newUnits[6]) - 1)
							clientSocket.send(str("Plane Added").encode('utf-8'))
						else:
							clientSocket.send(str("Not enough resource").encode('utf-8'))

					### 3
					if currentAction[3] == '3':
						if int(newUnits[4]) >= 2 and int(newUnits[5]) >=2:
							newUnits[2] = str(int(newUnits[2]) + 1)
							newUnits[4] = str(int(newUnits[4]) - 2)
							newUnits[5] = str(int(newUnits[5]) - 2)
							clientSocket.send(str("Air Def Added").encode('utf-8'))
						else:
							clientSocket.send(str("Not enough resource").encode('utf-8'))

					### 4
					if currentAction[3] == '4':
						if int(newUnits[4]) >= 2 and int(newUnits[5]) >=2:
							newUnits[3] = str(int(newUnits[3]) + 1)
							newUnits[4] = str(int(newUnits[4]) - 2)
							newUnits[5] = str(int(newUnits[5]) - 2)
							clientSocket.send(str("Ground Def Added").encode('utf-8'))
						else:
							clientSocket.send(str("Not enough resource").encode('utf-8'))

				### Hack to add 1
				if currentAction[:3] == "HAK":
					newUnits = client[currentUser][0]

					Hak1(newUnits,int(currentAction[3]))

				### Hack to add 1
				if currentAction[:3] == "SUB":
					newUnits = client[currentUser][0]

					Sub1(newUnits,int(currentAction[3]))


				### Collect resources
				if currentAction[:3] == 'COL':
					newUnits = client[currentUser][0]

					newUnits[4] = str(int(newUnits[4]) + int(newUnits[7]))
					newUnits[5] = str(int(newUnits[5]) + int(newUnits[8]))
					newUnits[6] = str(int(newUnits[6]) + int(newUnits[9]))
					clientSocket.send(str("Collected resources").encode('utf-8'))

				if currentAction == 'DIST':
					newUnits = client[currentUser][0]
					totalWork = newUnits[7] + ',' + newUnits[8] + ',' + newUnits[9]
					clientSocket.send(totalWork.encode('utf-8'))
					proposedWork = clientSocket.recv(16)
					proposedWork = proposedWork.decode('utf-8')
					print(proposedWork)
					proposedWork = proposedWork.split(',')

					newUnits[7] = str(proposedWork[0])
					newUnits[8] = str(proposedWork[1])
					newUnits[9] = str(proposedWork[2])

					clientSocket.send(str("Updated Workers").encode('utf-8'))

			if WEB == True:
				for x,n in enumerate(client):
					websiteUpdater(x,n)

			if DISPLAY == True:
				for n in client:
					client[n][2].updateBoard(client[n][0])
			print(client)
			print(len(currentDeck))

