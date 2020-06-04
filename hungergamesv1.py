import math
import multiprocessing
import random
import statistics
import sys
import threading
import time
from prettytable import PrettyTable

def simple_notify(title, text, timeout):
	from plyer import notification
	notification.notify(title=title, message=text, app_icon='C:\DLs\python-1.ico', timeout=timeout)

def players_creator(lst):
	global gen_players
	gen_players = []


	for tup in lst:
		if len(tup) == 4:
			morality = tup[3]
		else:
			morality = 3

		gen_players.append({
			'Team': str(tup[0]),
			'Name': str(tup[1]),
			'Nickname': str(tup[2]),
			'Morality': morality,
			'Alive': True,
			'Injured': False,
			'Sanity': 5,
			'Hunger': 0,
			'Thirst': 0,
			'Attack': 1,
			'Defense': 1,
			'Sheltered': False,
			'Asleep': False,
			'Inventory': {'Food': False, 'Medicine': False, 'Camping Gear': False},
			'Killed_by': None,
			'Kills': 0
			})

_for_player_gen = [
	('Crank', 'Crankrune', 'Crank'),
	('Crank', 'Emily Bett Rickards', 'Emily'),
	('Crank', 'Vanessa Morgan', 'Van', 5),
	('Crank', 'Rachel Skarsten', 'Rachel', 2),
	('Cyborg', 'Cyborg', 'Cyborg'),
	('Cyborg', 'Diane Guerrero', 'Diane'),
	('Cyborg', 'Madelaine Petsch', 'Mads'),
	('Cyborg', 'Katie Cassidy', 'Cassidy', 2),
	('Jesus', 'Jesus', 'Jesus'),
	('Jesus', 'Melissa Benoist', 'Melissa'),
	('Jesus', 'Willa Holland', 'Willa'),
	('Jesus', 'Shantel VanSanten', 'Spivot'),
	('Dranshaw', 'Dranshaw', 'Dran', 5),
	('Dranshaw', 'Danielle Panabaker', 'Dani', 4),
	('Dranshaw', 'Lili Reinhart', 'Lili'),
	('Dranshaw', 'Nicole Maines', 'Nicole', 4),
	('Slave', 'Slave', 'Slave'),
	# ('Slave', 'SlaveBot', 'SlaveBot', 2),
	('Slave', 'Jessica De Gouw', 'De Gouw'),
	('Slave', 'Katrina Law', 'Katrina'),
	('Slave', 'Camila Cabello', 'Cabello', 1),
	('Blue', 'Blue', 'Blue'),
	('Blue', 'Kat McNamara', 'Kat'),
	('Blue', 'Katie McGrath', 'McGrath'),
	('Blue', 'Jessica Parker Kennedy', 'JPK'),
	('Hello', 'Hello There', 'Hello'),
	('Hello', 'Amy Jackson', 'Amy'),
	('Hello', 'Candice Patton', 'Candice'),
	('Hello', 'Juliana Harkavy', 'Juliana'),
	('Cavs', 'Cavs1562', 'Cavs'),
	('Cavs', 'Caity Lotz', 'Lotz'),
	('Cavs', 'Violett Beane', 'Violett'),
	('Cavs', 'Chyler Leigh', 'Chyler'),
	('Jerker', 'The Arrow Jerker', 'Jerker'),
	('Jerker', 'Conor Leslie', 'Conor'),
	('Jerker', 'Elizabeth Olsen', 'Elizabeth'),
	('Jerker', 'Jennifer Lawrence', 'JLaw'),
	('dtoole', 'dtoole', 'dtoole'),
	('dtoole', 'Sea Shimooka', 'Sea'),
	('dtoole', 'Camila Mendes', 'Camila M.'),
	('dtoole', 'Meagan Tandy', 'Meagan'),
	('Harry', 'Harry', 'Harry'),
	('Harry', 'Dua Lipa', 'Dua'),
	('Harry', 'Sarah Grey', 'Sarah'),
	('Harry', 'Peyton List', 'Peyton'),
	('LEAGUE', 'Stephen Amell', 'Stephen'),
	('LEAGUE', 'Grant Gustin', 'Grant'),
	('LEAGUE', 'Ruby Rose', 'Ruby'),
	('LEAGUE', 'Tala Ashe', 'Tala'),
	('ROGUE', 'Wentworth Miller', 'Wentworth'),
	('ROGUE', 'Dominic Purcell', 'Dominic'),
	('ROGUE', 'Italia Ricci', 'Italia'),
	('ROGUE', 'Efrat Dor', 'Efrat')
]

_custom_teams_1 = [
	('Harry', 'Harry', 'Harry'),
	('Harry', 'Melissa Benoist', 'Mel'),
	('Harry', 'Dua Lipa', 'Dua'),
	('Harry', 'Shantel VanSanten', 'Shantel'),
	('Crank', 'Crankrune', 'Crank'),
	('Crank', 'Kat McNamara', 'Kat'),
	('Crank', 'Ariana Grande', 'Ariana'),
	('Crank', 'Vanessa Morgan', 'Vanessa'),
	('Cyborg', 'Cyborg', 'Cyborg'),
	('Cyborg', 'Diane Guerrero', 'Diane'),
	('Cyborg', 'Madelaine Petsch', 'Mads'),
	('Cyborg', 'Chyler Leigh', 'Chyler')
]

new_teams_1 = [
	('Anna', 'Anna Brutal', 'Anna'),
	('Anna', 'Katie Cassidy', 'Cassidy'),
	('Anna', 'Jessica Parker Kennedy', 'Jessica'),
	('Anna', 'Jes Macallan', 'Jes'),
	('Cavs', 'Cavs1562', 'Cavs'),
	('Cavs', 'Chyler Leigh', 'Chyler'),
	('Cavs', 'Violett Beane', 'Violett'),
	('Cavs', 'Caity Lotz', 'Caity'),
	('ElementalAxon', 'ElementalAxon', 'ElementalAxon'),
	('ElementalAxon', 'Danielle Panabaker', 'Dani'),
	('ElementalAxon', 'Ruby Rose', 'Ruby'),
	('ElementalAxon', 'Axon-Bot', 'Axon-Bot'),
	('dtoole', 'dtoole', 'dtoole'),
	('dtoole', 'Kayla Compton', 'Kayla'),
	('dtoole', 'Odette Annable', 'Odette'),
	('dtoole', 'Meagan Tandy', 'Meagan'),
	('Jesus & Harry', 'JesusOfAV', 'Jesus'),
	('Jesus & Harry', 'SomeoneHarry', 'Harry'),
	('Jesus & Harry', 'Melissa Benoist', 'Mel'),
	('Jesus & Harry', 'Willa Holland', 'Willa'),
	# ('Anna & Cavs', 'Anna Brutal', "Anna"),
	# ('Anna & Cavs', 'Cavs1562', 'Cavs'),
	# ('Anna & Cavs', 'Katie Cassidy', 'Cassidy'),
	# ('Anna & Cavs', 'Caity Lotz', 'Caity'),
	('Pringle', 'Pringle', 'Pringle'),
	('Pringle', 'Lili Reinhart', 'Lili'),
	('Pringle', 'Brec Bassinger', 'Brec'),
	('Pringle', 'Minka Kelly', 'Minka'),
	('Crank & Cyborg', 'Crankrune', 'Crank'),
	('Crank & Cyborg', 'CyborgDemonMan', 'Cyborg'),
	('Crank & Cyborg', 'Madelaine Petsch', 'Madelaine'),
	('Crank & Cyborg', 'Vanessa Morgan', 'Vanessa'),
	('Blue', 'Blue', 'Blue'),
	('Blue', 'Kat McNamara', 'Kat'),
	('Blue', 'Katie McGrath', 'McGrath'),
	('Blue', 'Natalie Dreyfuss', 'Natalie'),
	('Hello', 'Hello There', 'Hello'),
	('Hello', 'Amy Jackson', 'Amy'),
	('Hello', 'Candice Patton', 'Candice'),
	('Hello', 'Juliana Harkavy', 'Juliana')
]

# _for_player_gen = [x for x in _for_player_gen if x[0] in 
# 				   ['Slave', 'Cyborg', 'Crank', 'Harry']]

# _custom_teams_1 = [x for x in _custom_teams_1 if x[0] in]

# _for_player_gen = _custom_teams_1
_for_player_gen = _custom_teams_1 + [x for x in _for_player_gen if x[0] in ['LEAGUE', 'ROGUE']]
# _for_player_gen = new_teams_1

players_creator(_for_player_gen)

# print(random.choice(players)['Name'])
# print(random.randint(1, 100))

def game(players, printing=True, delay=True):
	if not printing:
		fl = open('nul', 'w')
	else:
		fl = sys.stdout

	print('Welcome to the Hunger Games\nWritten and Designed by Crankrune', file=fl)
	print('-' * 35, file=fl)
	team_counter = {}
	for player in players:
		if player['Team'] in team_counter.keys():
			team_counter[player['Team']] += 1
		else:
			team_counter[player['Team']] = 1
	for team in team_counter.items():
		print(f'Team {team[0]} has {team[1]} Players', file=fl)
		print( '|', ', '.join([x['Name'] for x in players if x['Team'] == team[0]]), file=fl )

	actions = {
		'Cornucopia': ['run', 'grab', 'fight'],
		'Base': ['fight', 'hunt', 'interaction', 'sleep', 'construct', 'plan', 'practice',
				 'meditate', 'pray', 'heal', 'sponsored', 'accident', 'suicide']
		}
	action_weights = {
		'Cornucopia': [.75, .40, .20],
		'Base': [.20, .10, .05, .05, .05, .10, .10, .02, .02, .05, .01, .02, .01],
		'Morning': [.20, .10, .05, .02, .05, .10, .10, .02, .02, .05, .01, .02, .01],
		'Midday': [.20, .10, .05, .05, .05, .10, .10, .02, .02, .05, .01, .02, .01],
		'Night': [.20, .10, .05, .20, .05, .10, .10, .02, .02, .05, .01, .02, .01]
	}
	print( list(zip(actions['Base'], action_weights['Base'])) )
	print( list(zip(actions['Base'], action_weights['Morning'])) )
	print( list(zip(actions['Base'], action_weights['Midday'])) )
	print( list(zip(actions['Base'], action_weights['Night'])) )

	def all_same(lst):
		if lst.count(lst[0]) == len(lst):
			return True
		else:
			return False

	def get_kill_text(killer, killed):
		sel = random.choice(['{0} bashes {1}\'s head against a rock repeatedly', '{0} draws their bow and shoots {1} in the chest', '{0} phases their hand through {1}\'s heart',
							 '{0} stabs {1} through the abdomen with their sword', '{0} uses their heat vision to burn {1} alive', '{0} strangles {1}', '{0} strangles {1} with a rope',
							 '{0} throws a batarang into {1}\'s head', '{0} runs {1} through with a spear', '{0} uses an explosive to blow up {1}', '{0} defeats {1} in a league duel',
							 '{0} fights {1} and snaps their neck', '{0} uses their server admin powers to ban {1}, killing them', '{0} shoots a hole through {1}\'s abdomen with their gun',
							 '{0} decapitates {1} with a sword', '{0} repeatedly stabs {1} to death with sais', '{0} finds {1} dying but chooses not to save them, and sits with them while they go',
							 '{0} finds {1} dead at the bottom of a ravine', '{0} sees {1} dead, it seems they took their own life', '{1} asks {0} to kill them, they reluctantly oblige',
							 '{0} strangles {1} until they see the life fade from their eyes', '{0} quietly sneaks up behind {1} and swiftly snaps their neck, killing them instantly',
							 '{0} kills {1} for their supplies', '{0} stabs {1} in the back with a trident', '{0} cuts {1}\'s throat while they rest', '{0} kills {1} in their sleep'])
		return sel.format(killer, killed)

	def get_counter_text(killer, killed):
		sel = random.choice(['{1} tries to blow {0} up but fails and kills them self', '{1} attempts to trap {0}, but steps into it them self, dying as a result of their mistake', '{1} challenges {0} to a duel, and loses',
							 '{1} attacks {0}, but kills them self in confusion', '{1} swings at {0}, but trips and breaks their neck', '{1} misinterpreted their dream, and didn\'t see {0}\'s attack, killing them',
							 '{1}, poisons {0}\'s drink, but mistakes it for their own and dies'])
		return sel.format(killed, killer)

	def get_practice_text(name, increase):
		sel = random.choice(['{0} uses tennis balls to practice with their bow, gaining {1} attack', '{0} trains on the salmon ladder, gaining {1} attack', '{0} sharpens their sword, gaining {1} attack',
							 '{0} crafts a spear, increasing their attack by {1}', '{0} injects themselves with Mirakuru, gaining {1} attack', '{0} forms a tree branch into a shiv, gaining {1} attack'])
		return sel.format(name, increase)

	def get_hunt_text(name, increase):
		sel = random.choice(['{0} dons their hood and begins the hunt, gaining {1} attack', '{0} puts on their cowl, and takes to the woods to hunt, gaining {1} attack',
							 '{0} grabs their bow and quiver, and starts hunting, gaining {1} attack', '{0} hunts for other tributes, gaining {1} attack'])
		return sel.format(name, increase)

	def get_planning_text(name, stat, increase):
		sel_atk = random.choice(['{0} crafts a spear from tree branches, gaining {1} {2}', '{0} sharpens a rock into a knife, gaining {1} {2}', '{0} climbs a tree to scout the area, gaining {1} {2}'])

		sel_def = random.choice(['{0} fashions a shield out of plane wreckage, gaining {1} {2}', '{0} uses sticks and twine to make armor, gaining {1} {2}', '{0} survey\'s the woods, gaining {1} {2}'])

		if stat == 'Attack':
			return sel_atk.format(name, increase, stat)
		elif stat == 'Defense':
			return sel_def.format(name, increase, stat)

	def get_construct_text(name, increase):
		sel = random.choice(['{0} constructs a simple wooden shack, gaining {1} defense', '{0} sets up a campsite in a cave, gaining {1} defense', '{0} finds a wrecked and plane and sets up camp, gaining {1} defense'])

		return sel.format(name, increase)

	def get_escape_test(killer, escapee):
		sel = random.choice(['{0} tries to kill {1}, but can\'t bring themselves to do it', '{0} shoots an arrow at {1}, but misses', '{0} attempts to kill {1}, but they plead for mercy and survive',
							 '{1} asks {0} to kill them, but {0} refuses', '{0} aims at {1} but can\'t take the shot', '{0} sets a trap for {1}, but they disarm it and move on'])
		return sel.format(killer, escapee)

	def get_injure_text(name):
		sel = random.choice(['{0} trips and sprains their ankle', '{0} narrowly escapes a battle, injuring themselves', '{0} injures them self', '{0} crosses a moderator, and is muted, injuring them',
							 '{0} IS INJURED!', '{0} is exposed to Kryptonite, injuring them', '{0} catches Coronavirus, and is weakened'])

		return sel.format(name)

	def get_accident_death_text(name):
		sel = random.choice(['{0} steps on a land mine, dying instantly', '{0} trips and falls into a ravine, dying', '{0} slips and falls into a pit, dying', '{0} misfires while cleaning their gun, killing them',
							 '{0} falls to their death while climbing a tree', '{0} catches the Coronavirus, and dies coughing in the woods'])
		return sel.format(name)

	def get_passive_text(name):
		sel = random.choice(['{0} attempts to start a fire, but is unsuccessful', '{0} loses sight of where they are', '{0} climbs a tree to rest'])

		return sel.format(name)

	def get_interaction_text(count, player_list):
		if count == 2:
			sel = random.choice(['{0} and {1} run into each other and decide to go their separate ways', '{0} sees {1} resting in their camp, but chooses not to fight them', '{0} hears {1} walking in the woods, but maintains social distancing and leaves them be'])
		elif count == 3:
			sel = random.choice(['{0} brings up a good plan for them to do, but {1} thinks it sucks, so {2} suggests that they stick to the plan either way', '{0} overhears {1} and {2} talking in the distance',
				'{0}, {1}, and {2} run into each other, but all back away, declining to fight'])
		elif count == 4:
			sel = random.choice(['{0} tries to make the plan happen, {1} then executes the plan as an example on how it\'ll work, but {2} expects that the plan would go off the rails either way. So {3} throws away the plan out of shame.'])
		
		# return sel.format(player_list)
		# print(count, [x['Nickname'] for x in player_list])
		return sel.format(*[x['Nickname'] for x in player_list])

	# Cornucopia
	round_type = 'Cornucopia'
	turn_taken = []
	random.shuffle(players)

	print('-'*35, f'\nCornucopia Round Commencing\n{len(players)} player game\n', '-'*35, sep='', file=fl)
	places = []
	_nums = list(range(len(players)+1))
	_nums.reverse()

	for player in players:
		if not player['Alive']:
			turn_taken.append(player)
			continue
		elif player in turn_taken:
			continue

		action = random.choices(actions[round_type], action_weights[round_type])[0]
		if player == players[-1]:
			action = random.choices(['run', 'grab'], [.75, .40])[0]
		# print( player['Nickname'], 'will' , action )
		
		if action == 'fight':
			# opp_choices = [x for x in players if x not in turn_taken + [player]]
			# opponent = random.choice(opp_choices)

			opp_choice_master = []
			for p in players:
				if p in turn_taken + [player] or p is player or not p['Alive']:
					continue
				else:
					if p['Team'] == player['Team']:
						opp_choice_master.append((p, .05))
					else:
						opp_choice_master.append((p, .95))

			ops, wght = [], []
			for x, y in opp_choice_master:
				ops.append(x)
				wght.append(y)

			if len(ops) == 0:
				print(player['Nickname'], 'freezes, and does nothing', file=fl)
				continue

			opponent = random.choices(ops, wght)[0]

			outcome = random.choices(['Kill', 'Escape', 'Counter'], 
				[.50 * player['Attack'], .50 * opponent['Defense'], .10 * opponent['Attack']])[0]

			if outcome == 'Kill':
				# kill_text = random.choice(['stabs', 'shanks', 'murders', 'strangles'])
				# print( player['Nickname'], kill_text, opponent['Nickname'], file=fl )
				print( get_kill_text(player['Nickname'], opponent['Nickname']), file=fl )
				opponent['Alive'] = False
				opponent['Killed_by'] = player['Name']
				places.append( (_nums[0], opponent) )
				_nums.pop(0)
				player['Kills'] += 1
			elif outcome == 'Escape':
				print( player['Nickname'], 'is unable to kill', opponent['Nickname'], file=fl )
				turn_taken.append(opponent)
			elif outcome == 'Counter':
				# print( opponent['Nickname'], 'turns the tables and kills', player['Nickname'], file=fl )
				print( get_counter_text(player['Nickname'], opponent['Nickname']), file=fl )
				player['Alive'] = False
				player['Killed_by'] = opponent['Name']
				places.append( (_nums[0], player) )
				_nums.pop(0)
				opponent['Kills'] += 1

		if action == 'grab':
			to_grab = ['Food', 'Medicine', 'Weapon', 'Camping Gear']
			grab_choice = random.choices(to_grab, [0, .3, .4, .1])[0]
			success = random.choices([True, False], [.3, .1])[0]
			syntax = ' a' if grab_choice == 'Weapon' else ''
			if success:
				print( player['Nickname'], f'grabs{syntax}', grab_choice, file=fl )
				if grab_choice == 'Weapon':
					player['Attack'] += random.choice([1, 2, 3])
				else:
					player['Inventory'][grab_choice] = True
			else:
				print( player['Nickname'], f'tries and fails to get{syntax}', grab_choice, file=fl )

		if action == 'run':
			print( player['Nickname'], 'runs away from the cornucopia.', file=fl )

		# if len(players) != 8:
		# 	print('ERROR, LESS THAN 8 PLAYERS')
		
		# if player not in turn_taken:
		# 	turn_taken.append(player)
		if player['Name'] not in [x['Name'] for x in turn_taken]:
			turn_taken.append(player)
		# if not player['Alive']:
		# 	places.append( (_nums[0], player) )
		# 	_nums.pop(0)

	if not len(turn_taken) == len(players):
		print(sorted([x['Nickname'] for x in turn_taken]), file=fl)
		print(sorted([x['Nickname'] for x in players]), file=fl)

	# Main Game
	round_type = 'Morning'
	day = 1
	round_num = 1

	# while len([x for x in players if x['Alive']]) > 1:
	while len(players) > 1:
		print('', file=fl)
		
		if len([x for x in players if x['Alive']]) == 1:
			break

		# turn_taken = [x for x in players if not x['Alive']]
		# still_alive = [x for x in players if x['Alive']]
		turn_taken = []
		random.shuffle(players)

		print( 'It is {round_type} of Day {day}, {people} people remain'.format(round_type=round_type, day=day, people=len([x for x in players if x['Alive']])), file=fl )
		
		# players = [x for x in players if x['Alive']]

		# [players.remove(x) for x in players if not x['Alive']]
		# print([x['Nickname'] for x in players if not x['Alive']])

		for player in players:
			if not player['Alive']:
				turn_taken.append(player)
				continue
			if len(players) == 1:
				break
			elif player in turn_taken:
				continue

			inverse = [0, 5, 4, 3, 2, 1]
			inverse2 = [8, 7, 6, 5, 4, 3, 2, 1]

			# print('Sanity', player['Sanity'])
			if player['Sanity'] > 5:
				player['Sanity'] = 5
			elif player['Sanity'] <= 0:
				player['Sanity'] = 1

			opp_lst = []
			for p in players:
				if p in turn_taken + [player] or p is player or not p['Alive']:
					continue
				else:
					opp_lst.append(p['Team'])

			# weighting stuff
			new_weights = action_weights[round_type]
			
			if len(opp_lst) == 0:
				new_weights[0] = 0
			elif len(opp_lst) == 1:
				new_weights[0] = new_weights[0] * (player['Attack'] / 6) + ((day - 1)/4)
			elif len(opp_lst) <= 3:
				new_weights[0] = 1
			elif len(opp_lst) > 0 and all_same(opp_lst):
				new_weights[0] = (.03 * inverse[player['Morality']]) * (player['Attack'] / 6) + ((day - 1)/4) # Fight
			else:
				new_weights[0] = new_weights[0] * (player['Attack'] / 6) + ((day - 1)/4) # Fight

			new_weights[0] = new_weights[0] / 3

			# new_weights[0] = new_weights[0] * (player['Attack'] / 2) + (day - 1) # Fight
			# new_weights[0] = new_weights[0] * (player['Attack'] / 3) + ((day - 1)/2) # Fight
			# new_weights[1] = new_weights[1] * player['Attack'] # Hunt
			new_weights[2] = 0 if len(opp_lst) <= 4 else new_weights[2] * (player['Morality'] / 2) # Team-up
			# new_weights[2] = 0 # Team-up
			# new_weights[3] = new_weights[3] * inverse[int(player['Sanity'])] # Sleep
			new_weights[4] = new_weights[4] * 5 if player['Inventory']['Camping Gear'] else new_weights[4] # Construct
			new_weights[5] = new_weights[5] # Plan
			new_weights[6] = new_weights[6] * (player['Attack'] / 2) # Practice
			new_weights[7] = .01 if player['Sanity'] >= 3 else .05 # Meditate
			new_weights[8] = .02 if player['Sanity'] >= 3 else .10 # * inverse[player['Sanity']] # Pray
			new_weights[9] = 2 if player['Inventory']['Medicine'] and player['Injured'] else 0 # Heal
			# new_weights[10] = new_weights[10] + (player['Kills'] / 3) # Sponsor
			new_weights[10] = new_weights[10] # Sponsor
			if player['Inventory']['Medicine'] and player['Inventory']['Camping Gear']:
				new_weights[10] = 0
			new_weights[11] = .05 / player['Defense'] # Accident
			new_weights[12] = 0 if player['Sanity'] > 2 else 1 / player['Sanity'] # Suicide

			# Stat Check
			if player['Sanity'] > 5:
				player['Sanity'] = 5
				new_weights[7], new_weights[8] = 0, 0
			if player['Attack'] > 5:
				player['Attack'] = 5
				new_weights[5], new_weights[6] = 0, 0
			if player['Defense'] > 5:
				player['Defense'] = 5
				new_weights[5], new_weights[6] = 0, 0
			if player['Sheltered']:
				new_weights[4] = 0.01


			action = random.choices(actions['Base'], new_weights)[0]
			if player == players[-1]:
				acts = [x for x in actions['Base'] if x != 'fight']
				new_weights.pop(0)
				action = random.choices(acts, new_weights)[0]
				new_weights.insert(0, .10)

			# debugging only
			if action in ['fight', 'interaction'] and len(opp_lst) == 0:
				print( '[debug]', player['Nickname'], f'ACTION: {action}', len(opp_lst), new_weights[0] )

			if action not in ['fight', 'hunt', 'sleep', 'suicide', 'accident', 'meditate', 'pray'] and player['Sanity'] > 1:
				go_crazy = random.choices([True, False], [.15, .9])[0]
				if go_crazy:
					action = 'go_crazy'
				else:
					action = action
				
				player['Sanity'] = player['Sanity'] - random.choices([0, 1, 2], [.85, .15, .02])[0]

			if action == 'fight':
				# opp_choices = [x for x in players if x not in turn_taken + [player]]
				# opp_choices = [x for x in opp_choices if x['Alive']]
				# if len(opp_choices) == 0:
				# 	continue
				# opponent = random.choice(opp_choices)

				opp_choice_master = []
				for p in players:
					if p in turn_taken + [player] or p is player or not p['Alive']:
						continue
					else:
						if p['Team'] == player['Team']:
							# opp_choice_master.append((p, .01 * inverse[player['Morality']]))
							morality_scale = [0, .95, .25, .01, .005, 0]
							opp_choice_master.append((p, morality_scale[player['Morality']]))
						else:
							# opp_choice_master.append((p, .65 * player['Morality']))
							opp_choice_master.append((p, .95))

				ops, wght = [], []
				for x, y in opp_choice_master:
					ops.append(x)
					wght.append(y)

				if len(ops) == 0:
					continue

				opponent = random.choices(ops, wght)[0]

				# Team Kill Debug
				# if player['Team'] == opponent['Team'] and len(ops) not in [1, 2]:
				# 	print( player['Nickname'], player['Morality'], opponent['Nickname'], [x['Team'] for x in ops], [x[1] for x in opp_choice_master] )
				# 	raise Exception('Team Kill Detected!')

				if len(ops) == 1:
					wgts = [.50 * player['Attack'], .10 * opponent['Defense'], .50 * opponent['Attack']]
				else:
					wgts = [.50 * player['Attack'], .50 * opponent['Defense'], .10 * opponent['Attack']]

				outcome = random.choices(['Kill', 'Escape', 'Counter'], wgts)[0]

				if outcome == 'Kill':
					# add in Arrowverse themed kill text
					# kill_text = random.choice(['stabs', 'shanks', 'murders', 'strangles'])
					# print( player['Nickname'], kill_text, opponent['Nickname'], file=fl )
					print( get_kill_text(player['Nickname'], opponent['Nickname']), file=fl )
					opponent['Alive'] = False
					opponent['Killed_by'] = player['Name']
					places.append( (_nums[0], opponent) )
					_nums.pop(0)
					player['Kills'] += 1
				elif outcome == 'Escape':
					# print( player['Nickname'], 'is unable to kill', opponent['Nickname'], file=fl )
					print( get_escape_test(player['Nickname'], opponent['Nickname']), file=fl )
					turn_taken.append(opponent)
				elif outcome == 'Counter':
					# print( opponent['Nickname'], 'turns the tables and kills', player['Nickname'], file=fl )
					print( get_counter_text(player['Nickname'], opponent['Nickname']), file=fl )
					player['Alive'] = False
					player['Killed_by'] = opponent['Name']
					places.append( (_nums[0], player) )
					_nums.pop(0)
					opponent['Alive'] = True
					opponent['Kills'] += 1
					turn_taken.append(opponent)

			elif action == 'hunt':
				player['Attack'] += 1
				# print( '{0} starts hunting for enemies, gains 1 Attack'.format(player['Nickname']), file=fl )
				print( get_hunt_text(player['Nickname'], 1), file=fl )
				pass

			elif action == 'interaction':
				ops = []
				for p in players:
					if p in turn_taken + [player] or p is player or not p['Alive']:
						continue
					else:
						ops.append(p)

				if len(ops) == 0:
					continue

				min_int = 1
				max_int = 2 if len(ops) >= 2 else len(ops)

				ops_count = math.floor(abs(random.random() - random.random()) * (1 + max_int - min_int) + min_int)

				opponents = random.choices(ops, k=ops_count)
				all_players = [player] + opponents

				# print( '[INTERACTION]', get_interaction_text(ops_count+1, all_players), file=fl )
				print( get_interaction_text(ops_count+1, all_players), file=fl )
				for op in opponents:
					turn_taken.append(op)
				# raise Exception('INTERACTION')
				pass

			elif action == 'sleep':
				print('{0} sleeps through the {1}'.format(player['Nickname'], round_type), file=fl)
				pass

			elif action == 'construct':
				increase = random.choices([1, 2], [.7, .3])[0]
				player['Defense'] += increase
				player['Sheltered'] = True
				# print( '{0} constructs a shelter, gains {1} defense.'.format(player['Nickname'], increase), file=fl )
				print( get_construct_text(player['Nickname'], increase), file=fl )
				pass

			elif action == 'plan':
				stat = random.choice(['Attack', 'Defense'])
				increase = random.choices([1, 2, 3], [.75, .5, .25])[0]
				player[stat] += increase
				# opt = random.choice(['{0} plans their next move, gains {1} {2}'])
				# print( opt.format(player['Nickname'], increase, stat), file=fl )
				print( get_planning_text(player['Nickname'], stat, increase), file=fl )
				pass

			elif action == 'practice':
				increase = random.choices([1, 2, 3], [.75, .5, .25])[0]
				player['Attack'] += increase
				# opt = random.choice(['{0} practices with their bow, and gains {1} attack.'])
				# print( opt.format(player['Nickname'], increase), file=fl )
				print( get_practice_text(player['Nickname'], increase), file=fl )
				pass

			elif action == 'meditate':
				increase = random.choices([0, 1, 2], [.2, .6, .2])[0]
				if increase == 0:
					print('{0} tries to meditate, but can\'t concentrate and gains 0 sanity.'.format(player['Nickname']), file=fl)
				else:
					print( '{0} takes time to meditate, and gains {1} sanity.'.format(player['Nickname'], increase), file=fl )
					player['Sanity'] += increase
				pass

			elif action == 'pray':
				increase = random.choices([1, 2, 3, 4, -1, 0], [.75, .5, .05, .05, .15, .15])[0]
				player['Sanity'] += increase
				if increase > 0:
					print( '{0} prays to Jesus of the Arrowverse, and gains {1} sanity.'.format(player['Nickname'], increase), file=fl )
				elif increase == 0:
					print( '{0} prays to Cyborg, who ignores their prayers. Giving them 0 sanity.'.format(player['Nickname'], increase), file=fl )
				else:
					print( '{0} prays to Elmo of the Fire Hell, and loses {1} sanity.'.format(player['Nickname'], increase), file=fl )
				pass

			elif action == 'heal':
				player['Injured'] = False
				player['Inventory']['Medicine'] = False
				player['Defense'] += 1
				print( '{0} uses some medicine, and feels good as new!'.format(player['Nickname']), file=fl )
				pass

			elif action == 'sponsored':
				to_grab = ['Food', 'Medicine', 'Weapon', 'Camping Gear']
				
				grab_weights = [0, .1, .4, .1]
				grab_weights[0] = 0 if player['Inventory']['Food'] else grab_weights[0]
				grab_weights[1] = 0 if player['Inventory']['Medicine'] else grab_weights[1]
				grab_weights[3] = 0 if player['Inventory']['Camping Gear'] else grab_weights[3]

				grab_choice = random.choices(to_grab, grab_weights)[0]
				syntax = ' a' if grab_choice == 'Weapon' else ''
				if grab_choice == 'Weapon':
					# player['Attack'] += random.choice([1, 2, 3])
					# print('{0} received a weapon from an unknown sponsor'.format(player['Nickname']), file=fl)
					increase = random.choices([1, 2, 3], [.75, .5, .25])[0]
					stat = random.choice(['Attack', 'Defense'])
					weap_atk = ['a sword', 'a bow', 'a dagger', 'some Mirakuru', 'some batarangs', 'a gun']
					weap_def = ['a shield', 'some armor']
					if stat == 'Attack':
						weap = random.choice(weap_atk)
					else:
						weap = random.choice(weap_def)
					print( '{0} is given {1} by an unknown sponsor, and gains {2} {3}'.format(player['Nickname'], weap, increase, stat), file=fl )
					player[stat] += increase

				else:
					player['Inventory'][grab_choice] = True
					print('{0} received {1} from an unknown sponsor'.format(player['Nickname'], grab_choice), file=fl)

			elif action == 'go_crazy':
				how_crazy = random.choices([1, 2, 3], [.5, .5, .2])[0]
				if how_crazy == 3:
					print( '{0} sees ghosts from their past and loses 3 sanity.'.format(player['Nickname']), file=fl )
				elif how_crazy == 2:
					print( '{0} is depressed and and loses 2 sanity.'.format(player['Nickname']), file=fl )
				elif how_crazy == 1:
					print( '{0} feels homesick, and loses 1 sanity.'.format(player['Nickname']), file=fl )

				player['Sanity'] = player['Sanity'] - how_crazy

			elif action == 'accident':
				chance_of_death = .1 if player['Injured'] else .02
				death = random.choices([True, False], [chance_of_death, .98])[0]
				if death:
					print( get_accident_death_text(player['Nickname']), file=fl )
					player['Alive'] = False
					player['Killed_by'] = player['Name']
				else:
					# print( '{0} trips and breaks their ankle'.format(player['Nickname']), file=fl )
					print( get_injure_text(player['Nickname']), file=fl )
					player['Injured'] = True
					player['Defense'] = player['Defense']
				pass


			elif action == 'suicide':
				text = random.choices(['The pressure gets to {0}, and they take their own life', '{0} insults Nicole, and is banned by Admin Crankrune (suicide)'], [.6, .3])[0]
				print( text.format(player['Nickname']), file=fl )
				player['Alive'] = False
				player['Killed_by'] = player['Name']
				pass

			if player['Name'] not in [x['Name'] for x in turn_taken]:
				turn_taken.append(player)

			# if not player['Alive']:
			# 	players.remove(player)

			if not player['Alive'] and player['Nickname'] not in [x[1]['Nickname'] for x in places]:
				places.append( (_nums[0], player) )
				_nums.pop(0)

		# Round Survivors
		counter = {x['Team']:0 for x in players}
		# counter = {x['Team']:counter[x['Team']]+1 for x in players if x['Alive']}
		for item in [x for x in players if x['Alive']]:
			counter[item['Team']] += 1
		alive_counter = sorted(counter.items(), key=lambda x: x[1], reverse=True)
		print(', '.join([f'{x}: {y}' for x,y in alive_counter if y]), file=fl)

		# Round Type
		if round_type == 'Morning':
			round_type = 'Midday'
		elif round_type == 'Midday':
			round_type = 'Night'
		elif round_type == 'Night':
			round_type = 'Morning'
			day += 1

		round_num += 1
		# if not len(turn_taken) == len(players):
		# 	print(sorted([x['Nickname'] for x in turn_taken]))
		# 	print(sorted([x['Nickname'] for x in players]))
		# time.sleep(.2)

	if delay:
		print('Delay')
		time.sleep(300)
		pass
	winner = [x for x in players if x['Alive']][0]
	print(winner['Name'], 'has won the Hunger Games!', file=fl)
	# print('Attack: {0}, Defense: {1}, Sanity: {2}, Kills: {3}'.format(
		# winner['Attack'], winner['Defense'], winner['Sanity'], winner['Kills']), file=fl)
	# print([(x[0], x[1]['Nickname']) for x in places], file=fl)

	# Leaderboard
	places.append( (1, winner) )
	places.reverse()

	# CHecking
	if len([x for x in places if x[0] == 1]) > 1:
		raise Exception('Leaderboard is fucked!')

	team_counter, kills_counter = {}, {}
	for place, p in places:
		print( '{0}: {1}, {2} Kill(s), {3} Atk, {4} Def, {5} Sanity, Killed by {6}'.format(place,
			p['Name'], p['Kills'], p['Attack'], p['Defense'], p['Sanity'], p['Killed_by']), file=fl )
		# print( '{0:>02}: {1} '.format(place, p['Name'], ), file=fl )
		
		if p['Team'] in team_counter.keys():
			team_counter[p['Team']].append(place)
		else:
			team_counter[p['Team']] = [place]

		if p['Team'] in kills_counter.keys():
			kills_counter[p['Team']] += p['Kills']
		else:
			kills_counter[p['Team']] = p['Kills']

	# headers = ['#', 'Name', 'Kills', 'Atk', 'Def', 'Sanity', 'Killer']
	# t = PrettyTable(headers)
	# for place, p in places:
	# 	t.add_row([place, p['Name'], p['Kills'], p['Attack'], p['Defense'], p['Sanity'], p['Killed_by']])
	# print(t)

	teams_counter2 = sorted(team_counter.items(), key=lambda x: statistics.mean(x[1]))
	kills_counter2 = sorted(kills_counter.items(), key=lambda x: x[1], reverse=True)

	print( '| Team Leaderboard', file=fl )
	for n, item in enumerate(teams_counter2):
		x, y = item
		avg_place = statistics.mean(y)
		# print( f'Team {x}: {statistics.mean(y)}', file=fl )
		# print( f'{n+1}: Team {x}', file=fl )
		print( f'{n+1}: Team {x} ({avg_place})', file=fl )
		pass

	print( '| Kills Leaderboard', file=fl )
	for x, y in kills_counter2:
		print( f'Team {x}: {y}', file=fl )
		pass

	# print(winner['Team'])
	return winner['Team']

def multi_simulator(runs):
	counter = {}
	games_ran = 0
	for x in range(runs):
		try:
			players_creator(_for_player_gen)
			winning_team = game(gen_players, printing=False, delay=False)
			games_ran += 1
			if winning_team in counter.keys():
				counter[winning_team] += 1
			else:
				counter[winning_team] = 1
		except:
			continue

	error_rate = (runs - games_ran) / runs
	print( f'{games_ran} games ran successfully, {error_rate:.2%} error rate.' )
	for item in sorted(counter.items(), key=lambda x: x[1], reverse=True):
		percent = (item[1] / games_ran)
		print( f'{item[0]}: {percent:.2%}' )

	win_perc = [x[1] for x in counter.items()]
	win_perc2 = [x[1] / games_ran for x in counter.items()]
	print('Standard Deviation: {0:.2%}'.format(statistics.pstdev(win_perc2)))
	print('Data Range: {0:.2%}'.format(max(win_perc2)-min(win_perc2)))

def multi_simulator_thread(runs, thread_count=8):
	global counter, games_ran
	counter = {}
	games_ran = 0

	global _for_thread
	def _for_thread(x=0):
		global games_ran
		try:
			players_creator(_for_player_gen)
			winning_team = game(gen_players, printing=False, delay=False)
			games_ran += 1
			if winning_team in counter.keys():
				counter[winning_team] += 1
			else:
				counter[winning_team] = 1
		except:
			pass

	for x in range(int(runs/thread_count)):
		threads = []
		for _ in range(thread_count):
			t = threading.Thread(target=_for_thread)
			# t = multiprocessing.Process(target=_for_thread)
			t.start()
			threads.append(t)
		for e, thread in enumerate(threads):
			thread.join(timeout=1)
			# print(f'thread {e+1} joined [{x*8+e}]')
		# print('Halp')
		# time.sleep(.01)

	# threads = []
	# for _ in range(runs):
	# 	t = threading.Thread(target=_for_thread)
	# 	t.start()
	# 	threads.append(t)
		# print( f'thread {_} started' )
	# for e, thread in enumerate(threads):
	# 	thread.join()
	# 	print( f'thread {e} joined' )

	error_rate = (runs - games_ran) / runs
	print( f'{games_ran}/{runs} games ran successfully, {error_rate:.2%} error rate.' )
	for item in sorted(counter.items(), key=lambda x: x[1], reverse=True):
		percent = (item[1] / games_ran)
		print( f'{item[0]}: {percent:.2%}' )

	win_perc = [x[1] for x in counter.items()]
	win_perc2 = [x[1] / games_ran for x in counter.items()]
	print('Standard Deviation: {0:.2%}'.format(statistics.pstdev(win_perc2)))
	print('Data Range: {0:.2%}'.format(max(win_perc2)-min(win_perc2)))
	simple_notify('Hunger Games', 'Multi-Sim Finished', 5)

# game(players)
game(gen_players, delay=False)

# multi_simulator(500)

if __name__ == '__main__':
	# multi_simulator_thread(100, thread_count=8)
	pass