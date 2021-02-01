import socket
import random
import time

IP = '127.0.0.1'
PORT = 1234


def printBoard(board):
	print('Soldiers: ',board[0])
	print('Planes: ',board[1])
	print('Air Def: ',board[2])
	print('Ground Def: ',board[3])
	print('Stone: ',board[4])
	print('Wood: ',board[5])
	print('Food: ',board[6])
	print('Stone Worker: ',board[7])
	print('Wood Worker: ',board[8])
	print('Food Worker: ',board[9])

usernameHeader = 'USER'
username = input("Username: ")

allowedCommands = ['DRAW','SHOW','COLL','DIST', \
					'ADD1','ADD2','ADD3','ADD4', \
					'HAK0','HAK1','HAK2','HAK3','HAK4','HAK5','HAK6','HAK7','HAK8','HAK9', \
					'USE1','USE2','USE3','USE4','USE5','USE6','USE7','USE8','USE9', \
					'SUB0','SUB1','SUB2','SUB3','SUB4','SUB5','SUB6','SUB7','SUB8','SUB9']

time.sleep(1)

print(f'Username {username} has been entered and attempting to log in')
### Create user data on server
socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

socketClient.connect((IP,PORT))
print('Connected to server.')
socketClient.send((usernameHeader + username).encode('utf-8'))
msg = socketClient.recv(32)
print(msg.decode('utf-8'))

while True:
	msg = socketClient.recv(32)
	if msg.decode('utf-8')[:5] != 'Start':
		pass
	else:
		break
print(msg.decode('utf-8'))

socketClient.close()


print('-'*30)
print('\n'*10)
print('Type HELP to view available commands')
print('\n'*2)


while True:
	cmd = input("Type your command here: ")
	cmd = cmd.upper()
	cmd = ''.join(cmd.split())

	print('\n'*3)
	print('-'*30)
	print('\n')
	# print(cmd)
	if cmd in allowedCommands:

		socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socketClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
		socketClient.connect((IP,PORT))

		### Convert cmd
		fullcmd = 'CMD' + cmd + username
		#######
		socketClient.send(fullcmd.encode('utf-8'))
		msg = socketClient.recv(64)
		
		msg = msg.decode('utf-8')

		### SHOW
		if cmd == 'SHOW':
			msg = msg.split('z')
			board = msg[0]
			if len(msg) > 1:
				cards = msg[1]
				cards = cards.split(',')
				print(f'You are holding {len(cards)} cards')
				print('You have the following cards:')
				print(cards,'\n')
				
			print("Your board currently has: ")
			board = board.split(',')
			printBoard(board)
			

		### DRAW
		if cmd == 'DRAW':
			print("You have drawn a", str(msg))

		if cmd[:3] == 'USE':
			if msg == 'Out Of Bounds':
				pass
			elif msg == 'Card Used':
				print('You have used your card, type SHOW to see what you have left')
			else:
				print(msg)
				x = input('Enter the player you want to peek at (The number): ')
				socketClient.send(x.encode('utf-8'))
				random2 = socketClient.recv(16)
				print(random2.decode('utf-8'))

		
		if cmd[:3] == 'ADD':
			print(msg)

		if cmd[:3] == 'COL':
			print(msg)

		if cmd == 'DIST':
			msg = msg.split(',')
			total = int(msg[0]) + int(msg[1]) + int(msg[2])
			print(f"You have {total} workers")
			while True:
				SWork = input("S: ")
				WWork = input("W: ")
				FWork = input("F: ")
				if (int(SWork) + int(WWork) + int(FWork)) == total:
					break
				print("Does not add up")


			newDist = SWork + ',' + WWork + ',' + FWork
			socketClient.send(newDist.encode('utf-8'))
			recvConfim = socketClient.recv(16)
			print(recvConfim.decode('utf-8'))


		if cmd[:3] == 'SUB':
			print(msg)

		if cmd[:3] == 'HAK':
			print(msg)



	elif cmd == 'HELP':
		print('Show : Shows all current cards')
		print('"N" : is used to denote an integer 1-9')
		print('UseN : Use the Nth card')
		print('Draw : Draw a card from the draw pile')
		print('Roll : Rolls a 6 sided dice')
		print('Coll : Collect resources')
		print('Dist : Redistribute workers')
		print('AddN : Buy 1 unit, cost calculated automatically')
		print('SubN : Subtract 1 from any box')
		print('HakN : Add 1 to any box for free')

	elif cmd == 'ROLL':
		print('You rolled a',random.randrange(1,7))


	else:
		print("Not a command")

	print('\n')
	print('-'*30)
	print('\n'*2)