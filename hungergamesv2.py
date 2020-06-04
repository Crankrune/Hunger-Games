import math
import random
import statistics
import sys
import threading
import time
from multiprocessing.pool import ThreadPool

def simple_notify(title, text, timeout):
	from plyer import notification
	notification.notify(title=title, message=text, app_icon='C:\DLs\python-1.ico', timeout=timeout)

class Player(object):
	def __init__(self, team, name, nickname, morality=3):
		self.team = team
		self.name = name
		self.nickname = nickname
		self.morality = morality
		self.alive = True
		self.injured = False
		self.sanity = 5
		self.attack = 1
		self.defense = 1
		self.sheltered = False
		self.asleep = False
		self.medicine = False
		self.camping = False
		self.killed_by = None
		self.kills = 0
		self.turn_taken = False
		self.last_action = None

		self.fl = sys.stdout

	def no_print(self):
		self.fl = open('nul', 'w')

	def same_team(self):
		tms = [x.team for x in self.opponents]
		if tms.count(self.team) == len(tms):
			return True
		else:
			return False

	def all_dead(self):
		status = [x.alive for x in self.opponents]
		if status.count(False) == len(status):
			return True
		else:
			return False

	def stat_check(self):
		def stat_fix(val):
			if val >= 5:
				return 5
			elif val <= 0:
				return 1
			else:
				return val
		self.attack = stat_fix(self.attack)
		self.defense = stat_fix(self.defense)
		self.sanity = stat_fix(self.sanity)
		pass

	def get_action(self, opponents, rnd):
		assert self.alive
		self.opponents = opponents
		viable_opps = [x for x in self.opponents if x.alive and not x.turn_taken and x is not self]
		all_team = self.same_team()
		self.stat_check()

		if self.all_dead():
			self.win_act()
			raise Exception(f'[DEBUG] {self.nickname} has won.', 'You forgot this, didn\'t you?')

		actions = [self.fight, self.hunt, self.interaction, self.sleep, self.construct, self.plan,
				   self.practice, self.meditate, self.pray, self.heal, self.sponsored, self.injure,
				   self.suicide, self.nothing, self.passive, self.multi_fight]
		act_wghts = [.20, .10, .05, .05, .05, .10, .10, .02, .02, .05, .01, .02, .01, .03, .03, .10]

		rnds = ['Morning', 'Midday', 'Night']
		self.round_type, self.day, self.round = rnd.get()
		inverse = [0, 5, 4, 3, 2, 1]

		if len(viable_opps) == 0:
			act_wghts[0] = 0
			act_wghts[2] = 0
		elif len(viable_opps) == 1:
			act_wghts[0] = act_wghts[0] * (self.attack / 6) + ((self.day-1)/4)
		elif len(viable_opps) <= 3:
			act_wghts[0] = 1
		elif len(viable_opps) > 0 and all_team:
			act_wghts[0] = (.03 * inverse[self.morality]) * (self.attack / 6) + ((self.day-1)/4)
		else:
			act_wghts[0] = act_wghts[0] * (self.attack / 6) + ((self.day-1)/4)

		act_wghts[4] = act_wghts[4] * 5 if self.camping else act_wghts[4]
		act_wghts[6] = act_wghts[6] * (inverse[self.attack] / 2)
		act_wghts[7] = .01 if self.sanity >= 3 else .20
		act_wghts[8] = .02 if self.sanity >= 3 else .05
		act_wghts[9] = 2 if self.medicine and self.injured else 0
		act_wghts[11] = .2 if self.injured else .05
		act_wghts[12] = .1 if self.sanity < 2 else .01
		# act_wghts[15] = 0 if act_wghts[15] == 0 else act_wghts[2] / 2 # Multi-Fight
		act_wghts[15] = .1 if 3 <= len(viable_opps) <= 4 else 0 # Multi-Fight

		act_pick = random.choices(actions, act_wghts)[0]
		if act_pick not in [self.fight, self.hunt, self.sleep, self.suicide, self.injure, self.meditate, self.pray] and self.sanity > 1:
			if random.choices([True, False], [.15, .9])[0]:
				act_pick = self.go_crazy

		act_pick()
		self.last_action = act_pick.__name__

	def cornucopia(self, opponents):
		assert self.alive
		self.opponents = opponents
		viable_opps = [x for x in opponents if x.alive and not x.turn_taken]
		viable_opps.remove(self)
		all_team = self.same_team()
		self.stat_check()

		actions = [self.run, self.grab, self.fight]
		weights = [.75, .40, .20]
		# action = random.choices([self.run, self.grab, self.fight], [.75, .40, .20])[0]
		action = random.choices(actions, weights)[0]
		if len(viable_opps) == 0:
			action = random.choices(actions[:2], weights[:2])

		action()


	def nothing(self):
		print( f'{self.nickname} literally just stands there and does nothing.', file=self.fl )
		self.turn_taken = True
		pass

	def heal(self):
		self.injured = False
		self.turn_taken = True

	def passive(self):
		sel = random.choice(['{0} attempts to start a fire, but is unsuccessful', '{0} loses sight of where they are', '{0} climbs a tree to rest'])

		print(sel.format(self.nickname), file=self.fl)
		self.turn_taken = True

	def construct(self):
		sel = random.choice(['{0} constructs a simple wooden shack, gaining {1} defense', '{0} sets up a campsite in a cave, gaining {1} defense', '{0} finds a wrecked and plane and sets up camp, gaining {1} defense'])

		increase = random.choices([1, 2], [.7, .3])[0]
		self.defense += increase
		self.sheltered = True
		print( sel.format(self.nickname, increase), file=self.fl )
		self.turn_taken = True

	def injure(self):
		chance_of_death = .1 if self.injured else .02
		death = random.choices([True, False], [chance_of_death, .98])[0]
		if death:
			self.accident_death()
		else:
			sel = random.choice(['{0} trips and sprains their ankle', '{0} narrowly escapes a battle, injuring themselves', '{0} injures them self', '{0} crosses a moderator, and is muted, injuring them',
								 '{0} IS INJURED!', '{0} is exposed to Kryptonite, injuring them', '{0} catches Coronavirus, and is weakened'])

			self.injured = True
			self.defense = int(self.defense / 2)

			print( sel.format(self.nickname), file=self.fl )
			self.turn_taken = True

	def accident_death(self):
		sel = random.choice(['{0} steps on a land mine, dying instantly', '{0} trips and falls into a ravine, dying', '{0} slips and falls into a pit, dying', '{0} misfires while cleaning their gun, killing them',
							 '{0} falls to their death while climbing a tree', '{0} catches the Coronavirus, and dies coughing in the woods'])

		self.alive = False
		self.killed_by = self.name

		print( sel.format(self.nickname), file=self.fl )
		self.turn_taken = True

	def practice(self):
		sel = random.choice(['{0} uses tennis balls to practice with their bow, gaining {1} attack', '{0} trains on the salmon ladder, gaining {1} attack', '{0} sharpens their sword, gaining {1} attack',
							 '{0} crafts a spear, increasing their attack by {1}', '{0} injects themselves with Mirakuru, gaining {1} attack', '{0} forms a tree branch into a shiv, gaining {1} attack'])

		increase = random.choices([1, 2, 3], [.75, .5, .25])[0]
		self.attack += increase

		print( sel.format(self.nickname, increase), file=self.fl )
		self.turn_taken = True

	def hunt(self):
		sel = random.choice(['{0} dons their hood and begins the hunt, gaining {1} attack', '{0} puts on their cowl, and takes to the woods to hunt, gaining {1} attack',
							 '{0} grabs their bow and quiver, and starts hunting, gaining {1} attack', '{0} hunts for other tributes, gaining {1} attack'])

		self.attack += 1
		print( sel.format(self.nickname, 1), file=self.fl )
		self.turn_taken = True

	def get_opponent(self, count=1, fight=False):
		opponents = [x for x in self.opponents if all([not x.turn_taken, x.alive, x is not self])]

		opps, wght = [], []
		morality_scale = [0, .95, .25, .01, .005, 0]
		for opp in opponents:
			opps.append(opp)
			if self.team == opp.team:
				wght.append( morality_scale[opp.morality] )
			else:
				wght.append(.95)

		opp_choices = []
		opp_list = opponents
		for _ in range(count):
			choice = random.choice(opp_list)
			opp_choices.append( choice )
			opp_list.remove( choice )

		if not fight:
			return opp_choices
		elif fight:
			opp_picks = []
			for _ in range(count):
				opponent = random.choices(opps, wght)[0]

				while opponent in opp_picks:
					opponent = random.choices(opps, wght)[0]
				opp_picks.append(opponent)

			if len(opp_picks) == 1:
				return opponent
			else:
				return opp_picks

	def fight(self):
		opponent = self.get_opponent(fight=True)

		if len(self.opponents) == 1:
			wgts = [.50 * self.attack, .10 * opponent.defense, .50 * opponent.attack]
		else:
			wgts = [.50 * self.attack, .50 * opponent.defense, .10 * opponent.attack]

		random.choices([self.kill, self.escape, self.counter], wgts)[0](opponent)
		self.turn_taken = True

	def kill(self, opponent):
		sel = random.choice(['{0} bashes {1}\'s head against a rock repeatedly', '{0} draws their bow and shoots {1} in the chest', '{0} phases their hand through {1}\'s heart',
							 '{0} stabs {1} through the abdomen with their sword', '{0} uses their heat vision to burn {1} alive', '{0} strangles {1}', '{0} strangles {1} with a rope',
							 '{0} throws a batarang into {1}\'s head', '{0} runs {1} through with a spear', '{0} uses an explosive to blow up {1}', '{0} defeats {1} in a league duel',
							 '{0} fights {1} and snaps their neck', '{0} uses their server admin powers to ban {1}, killing them', '{0} shoots a hole through {1}\'s abdomen with their gun',
							 '{0} decapitates {1} with a sword', '{0} repeatedly stabs {1} to death with sais', '{0} finds {1} dying but chooses not to save them, and sits with them while they go',
							 '{0} finds {1} dead at the bottom of a ravine', '{0} sees {1} dead, it seems they took their own life', '{1} asks {0} to kill them, they reluctantly oblige',
							 '{0} strangles {1} until they see the life fade from their eyes', '{0} quietly sneaks up behind {1} and swiftly snaps their neck, killing them instantly',
							 '{0} kills {1} for their supplies', '{0} stabs {1} in the back with a trident', '{0} cuts {1}\'s throat while they rest', '{0} kills {1} in their sleep',
							 '{0} uses their frost powers to freeze {1}. then shatters them', '{0} drowns {1} in the river', '{0} kills {1} with a barrage of punches (Ora ora ora)'])

		opponent.alive = False
		opponent.killed_by = self.name
		self.kills += 1
		opponent.turn_taken = True
		self._placement(opponent)

		print( sel.format(self.nickname, opponent.nickname), file=self.fl )

	def escape(self, opponent):
		sel = random.choice(['{0} tries to kill {1}, but can\'t bring themselves to do it', '{0} shoots an arrow at {1}, but misses', '{0} attempts to kill {1}, but they plead for mercy and survive',
							 '{1} asks {0} to kill them, but {0} refuses', '{0} aims at {1} but can\'t take the shot', '{0} sets a trap for {1}, but they disarm it and move on'])

		opponent.turn_taken = True
		print( sel.format(self.nickname, opponent.nickname), file=self.fl )

	def counter(self, opponent):
		sel = random.choice(['{1} tries to blow {0} up but fails and kills them self', '{1} attempts to trap {0}, but steps into it them self, dying as a result of their mistake', '{1} challenges {0} to a duel, and loses',
							 '{1} attacks {0}, but kills them self in confusion', '{1} swings at {0}, but trips and breaks their neck', '{1} misinterpreted their dream, and didn\'t see {0}\'s attack, killing them',
							 '{1}, poisons {0}\'s drink, but mistakes it for their own and dies', '{1} convinces {0} not to kill them, only to kill them instead'])

		opponent.kills += 1
		self.alive = False
		self.killed_by = opponent.name
		opponent.turn_taken = True
		print( sel.format(opponent.nickname, self.nickname), file=self.fl )

	def interaction(self):
		viable_opps = [x for x in self.opponents if x.alive and not x.turn_taken and x is not self]
		max_int = 3 if len(viable_opps) >= 3 else len(viable_opps)

		# count = random.choices([2,3,4], [.6, .3, .1])[0]
		count = random.randint(1, max_int)+1
		player_list = [self] + [x for x in self.get_opponent(count=count-1)]

		player_nicks = [p.nickname for p in player_list]

		if count == 2:
			sel = random.choice(['{0} and {1} run into each other and decide to go their separate ways', '{0} sees {1} resting in their camp, but chooses not to fight them', '{0} hears {1} walking in the woods, but maintains social distancing and leaves them be',
								 '{0} and {1} agree to a truce, and move on'])
		elif count == 3:
			sel = random.choice(['{0} brings up a good plan for them to do, but {1} thinks it sucks, so {2} suggests that they stick to the plan either way', '{0} overhears {1} and {2} talking in the distance',
								 '{0}, {1}, and {2} run into each other, but all back away, declining to fight', '{0} is about to kill {1}, but {2} steps in to save them. {0} runs away in the commotion'])
		elif count == 4:
			sel = random.choice(['{0} tries to make the plan happen, {1} then executes the plan as an example on how it\'ll work, but {2} expects that the plan would go off the rails either way. So {3} throws away the plan out of shame.',
								 '{0}, {1}, {2}, and {3} run into each other, weapons drawn. They decide not to risk it, and all back away slowly'])

		print( sel.format(*player_nicks), file=self.fl )
		for p in player_list: p.turn_taken = True

	def sponsored(self):
		def _food():
			pass

		def _medicine():
			self.medicine = True
			print( f'{self.nickname} received medicine from an unknown sponsor', file=self.fl )

		def _weapon():
			_increase = random.choices([1, 2, 3], [.75, .5, .25])[0]
			weap_atk = ['a sword', 'a bow', 'a dagger', 'some Mirakuru', 'some batarangs', 'a gun']
			weap_def = ['a shield', 'some armor']
			_stat = random.choice(['Attack', 'Defense'])
			if _stat == 'Attack':
				self.attack += _increase
				_weap = random.choice(weap_atk)
			elif _stat == 'Defense':
				self.defense += _increase
				_weap = random.choice(weap_def)

			print( '{0} is given {1} by an unknown sponsor, and gains {2} {3}'.format(self.nickname, _weap, _increase, _stat), file=self.fl )

		def _camping():
			self.camping = True
			print( f'{self.nickname} received camping gear from an unknown sponsor', file=self.fl )

		to_grab = [_food, _medicine, _weapon, _camping]
		grab_weights = [0, .1, .4, .1]
		grab_choice = random.choices(to_grab, grab_weights)[0]
		grab_choice()
		self.turn_taken = True

	def sleep(self):
		round_type = self.round_type.lower()
		print('{0} sleeps through the {1}'.format(self.nickname, round_type), file=self.fl)
		self.turn_taken = True

	def suicide(self):
		text = random.choice(['The pressure gets to {0}, and they take their own life', '{0} insults Nicole, and is banned by Admin Crankrune (suicide)', '{0} gives up, and commits seppuku'])
		print( text.format(self.nickname), file=self.fl )
		self.alive = False
		self.killed_by = self.name
		self.turn_taken = True

	def meditate(self):
		increase = random.choices([0, 1, 2], [.2, .6, .2])[0]
		if increase == 0:
			print('{0} tries to meditate, but can\'t concentrate and gains 0 sanity.'.format(self.nickname), file=self.fl)
		else:
			text = random.choice(['{0} takes time to meditate, and gains {1} sanity.', '{0} is comforted by the thought of their friends and gains {1} sanity.', '{0} cleans up in the river, feeling refreshed and gaining {1} sanity.'])
			print( text.format(self.nickname, increase), file=self.fl )
			self.sanity += increase
		self.turn_taken = True

	def pray(self):
		increase = random.choices([1, 2, 3, 4, -1, 0], [.75, .5, .05, .05, .15, .15])[0]
		self.sanity += increase
		if increase > 0:
			print( '{0} prays to Jesus of the Arrowverse, and gains {1} sanity.'.format(self.nickname, increase), file=self.fl )
		elif increase == 0:
			text = random.choice(['{0} prays to Cyborg, who ignores their prayers. Their sanity is unchanged.', '{0} prays to Harry, who doesn\'t care about their prayers. Their sanity is unchanged.'])
			print( text.format(self.nickname, increase), file=self.fl )
		else:
			print( '{0} prays to Elmo of the Fire Hell, and loses {1} sanity.'.format(self.nickname, increase), file=self.fl )
		self.turn_taken = True

	def go_crazy(self):
		how_crazy = random.choices([1, 2, 3], [.5, .5, .2])[0]
		if how_crazy == 3:
			text = random.choice(['{0} sees ghosts from their past and loses 3 sanity.'])
			print( text.format(self.nickname), file=self.fl )
			# print( '{0} sees ghosts from their past and loses 3 sanity.'.format(self.nickname), file=self.fl )
		elif how_crazy == 2:
			text = random.choice(['{0} is depressed and and loses 2 sanity.'])
			print( text.format(self.nickname), file=self.fl )
			# print( '{0} is depressed and and loses 2 sanity.'.format(self.nickname), file=self.fl )
		elif how_crazy == 1:
			text = random.choice(['{0} feels homesick, and loses 1 sanity.', '{0} blames themselves for their mistakes, and loses 1 sanity'])
			print( text.format(self.nickname), file=self.fl )
			# print( '{0} feels homesick, and loses 1 sanity.'.format(self.nickname), file=self.fl )

		self.sanity -= how_crazy
		self.turn_taken = True

	def plan(self):
		sel_atk = random.choice(['{0} crafts a spear from tree branches, gaining {1} {2}', '{0} sharpens a rock into a knife, gaining {1} {2}', '{0} climbs a tree to scout the area, gaining {1} {2}'])

		sel_def = random.choice(['{0} fashions a shield out of plane wreckage, gaining {1} {2}', '{0} uses sticks and twine to make armor, gaining {1} {2}', '{0} survey\'s the woods, gaining {1} {2}'])

		stat = random.choice(['attack', 'defense'])
		increase = random.choices([1, 2, 3], [.75, .5, .25])[0]
		if stat == 'attack':
			self.attack += increase
			print( sel_atk.format(self.nickname, increase, stat), file=self.fl )
		elif stat == 'defense':
			self.defense += increase
			print( sel_def.format(self.nickname, increase, stat), file=self.fl )
		self.turn_taken = True

	def multi_fight(self):
		viable_opps = [x for x in self.opponents if x.alive and not x.turn_taken and x is not self]
		max_int = 3 if len(viable_opps) >= 3 else len(viable_opps)

		count = random.randint(2, max_int) + 1
		count = random.choices([3,4][:count], [.3, .1][:count])[0]
		# player_list = [self] + [x for x in self.get_opponent(count=count-1, fight=True)]
		opp = self.get_opponent(count=count-1, fight=True)
		if not isinstance(opp, list): opp = [opp]
		player_list = [self] + [x for x in opp]
		random.shuffle(player_list)

		player_nicks = [p.nickname for p in player_list]
		killer, victims = player_list[0], player_list[1:]

		# count = 2
		if count == 2:
			# self.fight()
			raise Exception('Count=2')
		if count == 3:
			text = random.choice(['{0} uses an explosive to kill {1} and {2}', '{1} and {2} both attack {0}. But {0} kills them both in the skirmish.', '{0} kills both {1} and {2} with just a pencil',
								  '{0} finds {1} and {2} dead, seems they killed each other in battle'])
			print( text.format(*player_nicks), file=self.fl )
		if count == 4:
			text = random.choice(['{0} uses an explosive to kill {1}, {2}, {3}', '{0} is surrounded by {1}, {2}, and {3}. {0} takes Velocity-9 and snaps all their necks in the blink of an eye'])
			print( text.format(*player_nicks), file=self.fl )
		print('[MULTI-FIGHT] Look up', file=self.fl)

		for v in victims:
			v.alive = False
			v.killed_by = killer.name
			killer.kills += 1
		for p in player_list:
			p.turn_taken = True
			if p is not self:
				self._placement(p)


	def grab(self):
		to_grab = ['Food', 'Medicine', 'Weapon', 'Camping Gear']
		grab_choice = random.choices(to_grab, [0, .3, .4, .1])[0]
		success = random.choices([True, False], [.3, .1])
		syntax = ' a' if grab_choice == 'Weapon' else ''
		if success:
			print( self.nickname, f'grabs{syntax}', grab_choice, file=self.fl )
			if grab_choice == 'Weapon':
				self.attack += random.choices([1,2,3], [.5, .25, .1])[0]
			elif grab_choice == 'Medicine':
				self.medicine = True
			elif grab_choice == 'Camping Gear':
				self.camping = True
		else:
			print( self.nickname, 'runs away from the cornucopia.', file=self.fl )
		self.turn_taken = True

	def run(self):
		print(self.nickname, 'runs away from the cornucopia.', file=self.fl)
		self.turn_taken = True

	def win_act(self):
		win_texts = random.choice(['{0} realizes they\'re the only one left, and relaxes. They have won.'])
		print( win_texts.format(self.nickname), file=self.fl )
		self.turn_taken = True

	def _placement(self, opponent=None, win=False):
		global places, place_nums
		if self in [x[1] for x in places] or opponent in [x[1] for x in places]:
			return
		if win:
			places.append((place_nums[0], self))
			place_nums.pop(0)
		elif opponent:
			if not opponent.alive and opponent not in places:
				places.append((place_nums[0], opponent))
				place_nums.pop(0)
		elif not self.alive and self not in places:
			places.append( (place_nums[0], self) )
			place_nums.pop(0)

	def _return_player(self):
		global players
		plyrs = {x.nickname: x for x in players}
		plyr_self = plyrs[self.nickname]
		players[players.index(plyr_self)] = self

class HGRound(object):
	def __init__(self):
		self.round_type = 'Morning'
		self.day = 1
		self.round = 1

	def cycle(self):
		self.round += 1
		if self.round_type == 'Morning':
			self.round_type = 'Midday'
		elif self.round_type == 'Midday':
			self.round_type = 'Night'
		elif self.round_type == 'Night':
			self.round_type = 'Morning'
			self.day += 1
		return (self.round_type, self.day, self.round)

	def get(self):
		return (self.round_type, self.day, self.round)

class PlayerPool(object):
	def __init__(self, player_list, no_print=False):
		global places, place_nums
		self.player_list = player_list
		places = []
		place_nums = list(range(len(players)+1))
		place_nums.reverse()
		self.fl = sys.stdout
		if no_print:
			self.fl = open('nul', 'w')
			for p in self.player_list:
				p.fl = self.fl

	def _player_reset(self, players):
		for p in players:
			if p.alive:
				p.turn_taken = False

	def game(self):
		self.run_intro()
		self.run_cornucopia()
		self.run_game()
		self.run_outro()

	def run_intro(self):
		players = self.player_list
		print('Welcome to the Hunger Games v2\nWritten and Designed by Crankrune', file=self.fl)
		print('-' * 35, file=self.fl)
		team_counter = {}
		for player in players:
			if player.team in team_counter.keys():
				team_counter[player.team] += 1
			else:
				team_counter[player.team] = 1
		for team in team_counter.items():
			print(f'Team {team[0]} has {team[1]} Players', file=self.fl)
			print('|', ', '.join([x.name for x in players if x.team == team[0]]), file=self.fl)

	def run_cornucopia(self):
		# Run the Cornucopia
		players = self.player_list
		random.shuffle(players)
		print('-' * 35, f'\nCornucopia Round Commencing\n{len(players)} player game\n', '-' * 35, sep='', file=self.fl)
		for player in players:
			if player.alive and not player.turn_taken:
				player.cornucopia(players)
				player._return_player()
				player._placement()

				self._player_reset(players)
		print(file=self.fl)

	def run_game(self):
		living_players = [x for x in players if x.alive]
		rnd = HGRound()
		while len(living_players) > 1:
			random.shuffle(players)

			round_type, day, round_num = rnd.get()
			print('It is {0} of Day {1}, {2} people remain.'.format(round_type, day, len(living_players)), file=self.fl)

			for player in players:
				if player.alive and not player.turn_taken:
					player.get_action(players, rnd=rnd)
					player._return_player()
					player._placement()

			if not all([x.turn_taken for x in players]):
				print([(x.nickname, x.alive, x.last_action) for x in players if not x.turn_taken])
				raise Exception('Not everyone took their turn!')

			self._player_reset(players)

			living_players = [x for x in players if x.alive]

			# team counter
			counter = {p.team:0 for p in players}
			for item in [x for x in players if x.alive]:
				counter[item.team] += 1
			alive_counter = sorted(counter.items(), key=lambda x: x[1], reverse=True)
			print(', '.join([f'{x}: {y}' for x, y in alive_counter if y]), file=self.fl)

			rnd.cycle()

			print(file=self.fl)

		if len(living_players) == 1:
			print(f'{living_players[0].name} has won the Hunger Games!', file=self.fl)
			self.winner = living_players[0]
			self.winner._placement(win=True)
			places.reverse()
			return self.winner.team

	def run_outro(self):
		print(file=self.fl)
		team_counter, kills_counter = {}, {}
		for place, p in places:
			print('{0}: {1.name}, {1.kills} Kill(s), {1.attack} Atk, {1.defense} Def, {1.sanity} Sanity, Killed by {1.killed_by}'.format(place, p), file=self.fl)

			if p.team in team_counter.keys():
				team_counter[p.team].append(place)
			else:
				team_counter[p.team] = [place]

			if p.team in kills_counter.keys():
				kills_counter[p.team] += p.kills
			else:
				kills_counter[p.team] = p.kills

		teams_counter2 = sorted(team_counter.items(), key=lambda x: statistics.mean(x[1]))
		kills_counter2 = sorted(kills_counter.items(), key=lambda x: x[1], reverse=True)

		print('| Team Leaderboard', file=self.fl)
		for n, item in enumerate(teams_counter2):
			x, y = item
			avg_place = statistics.mean(y)
			# print( f'Team {x}: {statistics.mean(y)}', file=fl )
			# print( f'{n+1}: Team {x}', file=fl )
			print(f'{n + 1}: Team {x} ({avg_place})', file=self.fl)
			pass

		print('| Kills Leaderboard', file=self.fl)
		for x, y in kills_counter2:
			print(f'Team {x}: {y}', file=self.fl)
			pass

	def _thread_prep(self):
		self.fl = open('nul', 'w')
		# for p in self.player_list:
		# 	p.fl = self.fl
		global players
		players = [Player(*x) for x in _for_player_gen]
		for p in players:
			p.fl = self.fl
		self.__init__(players)

	def threading(self, runs, thread_coumt=8):
		# global counter, games_ran
		counter = {}
		games_ran = 0

		def _for_thread(_=None):
			self._thread_prep()
			# games_ran += 1
			return self.run_game()

		with ThreadPool(8) as pool:
			results = pool.map(_for_thread, range(runs))
		print(len(results))

_for_player_gen = [
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

def _debug(runs):
	global players
	run_count = 0
	for r in range(runs):
		try:
			players = [Player(*x) for x in _for_player_gen]
			g1 = PlayerPool(players, no_print=True)
			g1.game()
			run_count += 1
		except Exception as e:
			print(e)
			pass
	print( f'[Debugger] {run_count:,d}/{runs:,d} games ran successfully.' )

if __name__ == '__main__':
	players = [Player(*x) for x in _for_player_gen]
	g1 = PlayerPool(players)
	g1.game()
	# g1.threading(10)
	# _debug(1000)