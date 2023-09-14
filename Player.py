from Quest import Quest

class Player(object):
	def __init__(self, maxHp):
		self.maxHp = maxHp
		self.hp = self.maxHp
		self.location = None
		self.quests = []

	# This function moves the player from region to region
	def move(self, destination):
		destination = destination.title()
		# Don't move if you're already there.
		if destination in self.location.name:
			return False

		# Check your neighboring Locations 
		for edge in self.location.edges:
			# If we can go to a neighbor and the destination we entered is part of a valid
			# neighbor's name, then go to it.
			if edge.isOpen and (destination in edge.A.name or destination in edge.B.name):
				# Set the location and spawn in the Entities.
				self.location = edge.A if destination in edge.A.name else edge.B
				self.location.loadQuestContent(self)
				print("You moved to " + self.location.name + "\n")
				return True
		return False

	def setLocation(self, location):
		self.location = location

	def addQuest(self, quest):
		self.quests.append(quest)

	# Update completed Quests and remove them from the Quest list.
	def checkQuestStatus(self):
		questsDone = []
		for quest in self.quests:
			if quest.done:
				print("Quest Complete! [" + quest.name + "]")
				questsDone.append(quest)

		for quest in questsDone:
			self.quests.remove(quest)

	def getQuests(self):
		return self.quests

	def printQuests(self):
		print("Quests: ")
		for quest in self.quests:
			print(quest.getThisQuestAsString())

	def getHp(self):
		return self.hp

	def reset(self):
		self.hp = self.maxHp