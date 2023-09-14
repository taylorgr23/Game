from copy import deepcopy

class GameDatabase(object):
	def __init__(self):
		self.player = None
		self.startLoc = None
		self.npcs = dict()
		self.enemies = dict()
		self.items = dict()
		self.locations = dict()

	def getNPC(self, npcName):
		if npcName in self.npcs:
			return self.npcs[npcName]
		return None

	def getEnemy(self, enemyName):
		if enemyName in self.enemies:
			return self.enemies[enemyName]
		return None

	def getItem(self, itemName):
		if itemName in self.items:
			return deepcopy(self.items[itemName])
		return None

	def getLocation(self, locationName):
		if locationName in self.locations:
			return self.locations[locationName]
		return None

	def addNPC(self, npc):
		self.npcs[npc.name] = npc 

	def addEnemy(self, enemy):
		self.enemies[enemy.name] = enemy 

	def addItem(self, item):
		self.items[item.name] = item

	def addLocation(self, location):
		self.locations[location.name] = location