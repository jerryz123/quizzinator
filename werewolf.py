# Werewolf!
from collections import Counter
import copy

import random

class Player:
	def __init__(self, middle):
		self.name = input('Name? ')
		self.originalrole = middle.pop(random.randint(0, len(middle) - 1))
		self.role = self.originalrole
	def vote(self):
		return input('Who do you want to kill, '+ self.name + '?')
	def play(self):
		print('It is', self.name + "'s turn")
		input()
		print('You originally were a ' + self.originalrole.name)
		self.originalrole.nightaction(self, players, middle)
	def reveal(self):
		print(self.name + ', you are now ' + self.role.name)

class Role:
	def __init__(self):
		self.why = 'sigh'

class Werewolf(Role):
	order = 3
	name = 'werewolf'
	team = 'werewolf'
	def nightaction(self, myself, players, middle):
		werewolves = [p.name for p in players if (p.originalrole.name == 'werewolf' or hasattr(p.role, 'secret_name') and p.role.secret_name == 'werewolf') and p != myself]
		if len(werewolves):
			print('The other werewolves are: ' + str(werewolves))
		else:
			print('There are no other werewolves.')
			print('Which cards do you want to take (0, 1, 2)?')
			c1 = middle[int(input('Card index:'))]
			print('One of the middle cards is ' + c1.name)

class Minion(Werewolf):
	order = 4
	name = 'minion'
	def nightaction(self, myself, players, middle):
		werewolves = [p.name for p in players if p.originalrole.name == 'werewolf']
		print('The werewolves are: ' + str(werewolves))


class Villager(Role):
	order = 0
	name = 'villager'
	team = 'villager'
	def nightaction(self, myself, players, middle):
		return None

class Seer(Villager):
	order = 2
	name = 'seer'
	def nightaction(self, myself, players, middle):
		action = input("Do you want to (1) see someone's card or (2) look at two in the middle?")
		if action == '1':
			person = input("Whose card?")
			p = [x for x in players if x.name == person][0]
			print(person + "'s card is " + p.role.name)
		else:
			print('Which cards do you want to take (0, 1, 2)?')
			c1 = middle[int(input('Card index:'))]
			c2 = middle[int(input('Card index:'))]
			print('Two of the middle cards are: ' + c1.name + 'and ' + c2.name)

class Robber(Villager):
	order = 6
	name = 'robber'
	def nightaction(self, myself, players, middle):
		person = input('Who do you wanna rob?')
		p = [x for x in players if x.name == person][0]
		myself.role, p.role = p.role, myself.role
		print('You are now ' + myself.role.name)

class Insomniac(Villager):
	order = 8
	name = 'insomniac'
	def nightaction(self, myself, players, middle):
		print('You are now ' + myself.role.name)

#DRUNK DOESNT WORK YET
class Drunk(Villager):
	name = 'drunk'
	def nightaction(self, myself, players, middle):
		print('Which card do you want to take (0, 1, 2)?')
		pick = int(input('Card index:'))
		players[pick], myself.role = myself.role, players[pick]

class Troublemaker(Villager):
	order = 7
	name = 'troublemaker'
	def nightaction(self, myself, players, middle):
		print('Who do you want to switch?')
		p1 = str(input('1. '))
		p2 = str(input('2. '))
		p1 = [x for x in players if x.name == p1][0]
		p2 = [x for x in players if x.name == p2][0]
		p1.role, p2.role = p2.role, p1.role

class Doppelganger(Role):
	order = -1
	name = 'doppelganger'
	def nightaction(self, myself, players, middle):
		p1 = input('Whose card do you want to see?' )
		p1 = [x for x in players if x.name == p1][0]
		myself.role = copy.copy(p1.role)
		myself.role.secret_name = myself.role.name
		print('You have become a ' + myself.role.secret_name)
		myself.role.name = 'doppelganger'
		if myself.role.secret_name in 'minion robber troublemaker seer':
			myself.role.nightaction(myself, players, middle)
		if myself.role.secret_name == 'insomniac':
			players.append(players.pop(0))
		

class Mason(Villager):
	order = 5
	name = 'mason'
	def nightaction(self, myself, players, middle):
		masons = [p.name for p in players if (p.originalrole.name == 'mason' or hasattr(p.role, 'secret_name') and p.role.secret_name == 'mason') and p != myself]
		print('The other masons are: ' + str(masons))

class Tanner(Role):
	order = 1
	name = 'tanner'
	team = 'tanner'
	def nightaction(self, myself, players, middle):
		print('Lol have fun')

def win(dead):
	d = [x for x in players if x.name in dead]
	for p in d:
		if p.role.name == 'tanner':
			return 'tanner wins!'
	for p in d:
		if p.role.name == 'werewolf':
			return 'villagers win!'
	if len(dead) == 0:
		for p in players:
			if p.role.team == 'werewolf':
				return 'werewolves win!'
	return 'villagers win!'


### THE GAME ###
middle = [Doppelganger(), Werewolf(), Tanner(), Robber(), Troublemaker(), Seer(), Minion()]
players = [Player(middle) for x in range(4)]
players.sort(key = lambda p: p.originalrole.order)
for p in players:
	p.play()
	input()
	print("\033c")
input('Guys, deliberate for a bit. Press enter when ready to vote.')
votes = []
for p in players:
	votes.append(p.vote())
	print("\033c")
max_count = max([votes.count(x) for x in votes])
voteset = list(set(votes))
dead = [x for x in voteset if votes.count(x) == max_count]
print(win(dead))
for p in players:
	p.reveal()